"""Receipt extraction via MiniCPM-V served on Modal (vLLM, OpenAI-compatible).

The model is constrained with ``guided_json`` to the :class:`schema.Receipt`
JSON Schema. We still validate and normalise because difficult receipt photos
can produce OCR mistakes even when the response shape is correct.
"""
from __future__ import annotations

import base64
from io import BytesIO
import json
import mimetypes

from openai import OpenAI
from PIL import Image

import config
from schema import Receipt, guided_json_schema

MAX_IMAGE_SIDE = 1400
REQUEST_TIMEOUT = 150

_EXTRACT_PROMPT = (
    "You are reading a shopping receipt. Extract the store name, purchase date "
    "(YYYY-MM-DD), currency code, every line item with its quantity, unit price "
    "and line total, and the grand total. Transcribe product names exactly as "
    "printed. Do not duplicate a line item unless it appears multiple times on "
    "the receipt. For numeric product codes or PLU codes, keep them in the name; "
    "do not use them as quantity. If a text field is missing, use an empty "
    "string. If a price or quantity is missing, use 0. Respond with JSON only."
)


def _client() -> OpenAI:
    if not config.MODAL_ENDPOINT_URL:
        raise RuntimeError(
            "MODAL_ENDPOINT_URL is not set. Deploy modal_app.py and set the "
            "Space secret, or enable USE_ZEROGPU_FALLBACK."
        )
    return OpenAI(
        base_url=config.MODAL_ENDPOINT_URL,
        api_key=config.MODAL_API_KEY or "x",
        timeout=REQUEST_TIMEOUT,
    )


def _data_url(image_path: str) -> str:
    mime = mimetypes.guess_type(image_path)[0] or "image/jpeg"
    try:
        with Image.open(image_path) as image:
            image.thumbnail((MAX_IMAGE_SIDE, MAX_IMAGE_SIDE))
            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")
            out = BytesIO()
            image.save(out, format="JPEG", quality=85, optimize=True)
            b64 = base64.b64encode(out.getvalue()).decode()
            return f"data:image/jpeg;base64,{b64}"
    except Exception:
        # Fall back to the original file for uncommon image formats PIL cannot decode.
        pass
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

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "The model returned incomplete JSON for this image. Try a closer, "
            "single-receipt crop with less background."
        ) from exc
    for key in ("store", "date", "currency"):
        if data.get(key) == "":
            data[key] = None
    for item in data.get("items", []):
        if item.get("unit_price") == 0:
            item["unit_price"] = None
        _normalise_item_numbers(item, data.get("total"))
    receipt = Receipt.model_validate(data)
    if receipt.total is None and receipt.items:
        receipt.total = receipt.line_sum()
    if receipt.total and receipt.total > 1000 and receipt.line_sum() < receipt.total * 0.25:
        receipt.total = receipt.line_sum()
    return receipt


def _normalise_item_numbers(item: dict, receipt_total: float | None) -> None:
    """Fix common OCR mistakes before validation.

    Receipts often put PLU/product codes next to names. Vision models sometimes
    read those as quantities, producing impossible lines like 365 x 4.99.
    """
    try:
        qty = float(item.get("qty") or 0)
        unit_price = item.get("unit_price")
        unit_price = None if unit_price is None else float(unit_price)
        line_total = float(item.get("line_total") or 0)
        total = None if receipt_total is None else float(receipt_total)
    except (TypeError, ValueError):
        return

    if unit_price is None or qty <= 50:
        return
    looks_like_code = qty >= 100 and abs(line_total - qty * unit_price) <= 0.05
    looks_like_code_column = qty >= 100 and line_total >= 50
    impossible_against_total = total is not None and line_total > max(total * 2, unit_price * 5)
    if looks_like_code or looks_like_code_column or impossible_against_total:
        item["qty"] = 1
        item["line_total"] = round(unit_price, 2)
