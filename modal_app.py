"""Modal backend: serves MiniCPM-V on vLLM with an OpenAI-compatible API.

Deploy:
  modal secret create bonsai-api MODAL_API_KEY=<shared-secret>
  modal deploy modal_app.py

The deploy prints a URL; the OpenAI base_url is that URL + "/v1". Put it in the
HF Space secret MODAL_ENDPOINT_URL, and set MODAL_API_KEY to the same shared
secret.

vLLM's structured outputs (`guided_json`, xgrammar backend) guarantee the
receipt JSON is schema-valid, so the Space never has to repair model output.

Pin VLLM_VERSION to whatever the MiniCPM-V-4_5 model card lists as supported
before deploying — this model uses custom code (`--trust-remote-code`).
"""
from __future__ import annotations

import modal

MODEL_ID = "openbmb/MiniCPM-V-4_5"
VLLM_VERSION = "vllm==0.10.2"  # MiniCPM-V-4_5 model card lists vLLM support from 0.10.2
GPU = "L4"                      # int4 ~7GB; L4/A10G are plenty for 8B
PORT = 8000


def _download():
    from huggingface_hub import snapshot_download
    snapshot_download(MODEL_ID)


image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(VLLM_VERSION, "transformers==4.55.2", "huggingface_hub[hf_transfer]", "pillow")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .run_function(_download)  # bake weights into the image -> no per-request download
)

app = modal.App("bonsai-minicpm", image=image)


@app.function(
    gpu=GPU,
    scaledown_window=600,
    timeout=900,
    max_containers=1,
    secrets=[modal.Secret.from_name("bonsai-api")],
)
@modal.concurrent(max_inputs=20)
@modal.web_server(port=PORT, startup_timeout=900)
def serve():
    import os
    import subprocess

    api_key = os.environ["MODAL_API_KEY"]
    cmd = [
        "vllm", "serve", MODEL_ID,
        "--host", "0.0.0.0", "--port", str(PORT),
        "--trust-remote-code",
        "--max-model-len", "8192",
        "--guided-decoding-backend", "xgrammar",
        "--api-key", api_key,
        "--limit-mm-per-prompt", '{"image": 2}',
    ]
    subprocess.Popen(cmd)


# Quick local smoke test:  modal run modal_app.py
@app.local_entrypoint()
def main():
    print("Deploy with:  modal deploy modal_app.py")
    print("Then set MODAL_ENDPOINT_URL = <printed-url>/v1 and MODAL_API_KEY to your shared secret.")
