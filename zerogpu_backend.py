"""In-Space ZeroGPU fallback for when Modal is unavailable.

Only used when USE_ZEROGPU_FALLBACK=1. Requires the Space to run on ZeroGPU
hardware (HF PRO) and the heavy deps (torch, transformers) to be added to
requirements.txt. Kept out of the default path so the Space stays a light CPU
container. This loads MiniCPM-V locally and mimics extract.py / categorize.py's
JSON contract.

NOTE: ZeroGPU + custom-code vision models can be finicky; treat this as a
break-glass option, not the primary backend.
"""
from __future__ import annotations

import json

import config

_model = None
_tokenizer = None


def _load():
    global _model, _tokenizer
    if _model is not None:
        return
    import torch
    from transformers import AutoModel, AutoTokenizer

    _model = AutoModel.from_pretrained(
        config.MODEL_ID, trust_remote_code=True,
        attn_implementation="sdpa", torch_dtype=torch.bfloat16,
    ).eval().cuda()
    _tokenizer = AutoTokenizer.from_pretrained(config.MODEL_ID, trust_remote_code=True)


def _chat(content):
    import spaces  # noqa: F401  (import guarded for non-ZeroGPU envs)

    @spaces.GPU(duration=120)
    def _run():
        _load()
        return _model.chat(msgs=[{"role": "user", "content": content}], tokenizer=_tokenizer)

    return _run()


def extract_json(image_path: str, prompt: str, schema: dict) -> str:
    from PIL import Image
    img = Image.open(image_path).convert("RGB")
    raw = _chat([img, prompt + " Respond with JSON only, matching this schema: " + json.dumps(schema)])
    return _coerce_json(raw)


def chat_json(prompt: str, schema: dict) -> str:
    raw = _chat([prompt])
    return _coerce_json(raw)


def _coerce_json(raw: str) -> str:
    """Without vLLM guided decoding we must defensively parse here."""
    s = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    start, end = s.find("{"), s.rfind("}")
    return s[start:end + 1] if start != -1 and end != -1 else "{}"
