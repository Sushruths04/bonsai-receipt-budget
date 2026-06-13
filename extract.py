"""Receipt extraction via MiniCPM-V served on Modal (vLLM, OpenAI-compatible).

The model is constrained with ``guided_json`` to the :class:`schema.Receipt`
JSON Schema, so the response always parses. We still reconcile line items
against the printed total and surface mismatches for the user to fix.
"""
from __future__ import annotations

import base64
import json
import mimetypes

from openai import OpenAI

import config
from schema import Receipt, guided_json_schema

_EXTRACT_PROMPT = (
    "You are reading a shopping receipt. Extract the store name, purchase date "
    "(YYYY-MM-DD), currency code, every line item with its quantity, unit price "
    "and line total, and the grand total. Transcribe product names exactly as "
    "printed. If a text field is missing, use an empty string. If a price or "
    "quantity is missing, use 0. Respond with JSON only."
)


def _client() -> OpenAI:
    if not config.MODAL_ENDPOINT_URL:
        raise RuntimeError(
            "MODAL_ENDPOINT_URL is not set. Deploy modal_app.py and set the "
            "Space secret, or enable USE_ZEROGPU_FALLBACK."
        )
    return OpenAI(base_url=config.MODAL_ENDPOINT_URL, api_key=config.MODAL_API_KEY or "x")


def _data_url(image_path: str) -> str:
    mime = mimetypes.guess_type(image_path)[0] or "image/jpeg"
    with open(image_path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    return f"data:{mime};base64,{b64}"


def extract_receipt(image_path: str) -> Receipt:
    """Return a validated :class:`Receipt` from a receipt image path."""
    if config.USE_ZEROGPU_FALLBACK:
        from zerogpu_backend import extract_json  # local in-Space model
        raw = extract_json(image_path, _EXTRACT_PROMPT, guided_json_schema())
    else:
        resp = _client().chat.completions.create(
            model=config.MODEL_ID,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": _EXTRACT_PROMPT},
                    {"type": "image_url", "image_url": {"url": _data_url(image_path)}},
                ],
            }],
            temperature=0,
            max_tokens=2048,
            extra_body={"guided_json": guided_json_schema()},
        )
        raw = resp.choices[0].message.content

    data = json.loads(raw)  # guaranteed valid by guided decoding
    receipt = Receipt.model_validate(data)
    if receipt.total is None and receipt.items:
        receipt.total = receipt.line_sum()
    return receipt
