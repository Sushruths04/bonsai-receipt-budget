"""Two-tier item categorisation.

1. Fast path: an offline lookup built from Open Food Facts (NOVA processing
   group + Nutri-Score + category path). No model call, accurate, and
   defensible — we can point at a real food database for the labels.
2. Fallback: a single guided-decoding call to MiniCPM for items the lookup
   doesn't cover.

Resolved names are cached in SQLite so repeats never re-resolve.

Building the lookup table is a data step (see scripts/build_off_lookup.py in the
plan): it writes ``off_lookup.json`` mapping normalised product name -> category
key. Until that file exists we rely on the override map + model fallback, so the
app still runs end to end.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

import config
import db

OFF_LOOKUP_PATH = "off_lookup.json"

# Hand-pinned hero items so the live demo is never wrong on camera. Keep small.
_OVERRIDES: dict[str, str] = {
    "cola": "drinks", "coca cola": "drinks", "fanta": "drinks", "bier": "drinks",
    "wasser": "drinks", "water": "drinks", "kaffee": "drinks", "milch": "groceries",
    "chips": "junk", "schokolade": "junk", "chocolate": "junk", "haribo": "junk",
    "eis": "junk", "kekse": "junk", "banane": "healthy", "bananen": "healthy",
    "apfel": "healthy", "äpfel": "healthy", "salat": "healthy", "tomate": "healthy",
    "tomaten": "healthy", "gurke": "healthy", "brot": "groceries",
    "vollkornbrot": "groceries", "brötchen": "groceries", "ei": "groceries",
    "eier": "groceries", "pasta": "groceries", "nudeln": "groceries",
    "haferflocken": "groceries", "spülmittel": "household", "kino": "activities",
    "kinoticket": "activities", "restaurant": "activities", "döner": "activities",
}


def normalise(name: str) -> str:
    n = name.lower().strip()
    n = re.sub(r"\d+[.,]?\d*\s*(g|kg|ml|l|stk|x)?\b", " ", n)  # drop weights/qty
    n = re.sub(r"[^a-zäöüß ]", " ", n)
    return re.sub(r"\s+", " ", n).strip()


@lru_cache(maxsize=1)
def _off_lookup() -> dict[str, str]:
    p = Path(OFF_LOOKUP_PATH)
    if p.exists():
        return json.loads(p.read_text())
    return {}


def _local_category(name: str) -> str | None:
    norm = normalise(name)
    if not norm:
        return None
    if norm in _OVERRIDES:
        return _OVERRIDES[norm]
    cached = db.cache_get(norm)
    if cached:
        return cached
    lookup = _off_lookup()
    if norm in lookup:
        return config.normalise_category(lookup[norm])
    # token-level match against OFF / overrides (e.g. "bio bananen 1kg")
    for token in norm.split():
        if token in _OVERRIDES:
            return _OVERRIDES[token]
        if token in lookup:
            return config.normalise_category(lookup[token])
    return None


def categorize(names: list[str]) -> dict[str, str]:
    """Map each item name -> category key. Resolves locally first, then model."""
    result: dict[str, str] = {}
    unknown: list[str] = []
    for name in names:
        cat = _local_category(name)
        if cat:
            result[name] = cat
        else:
            unknown.append(name)

    if unknown:
        for name, cat in _model_categorize(unknown).items():
            result[name] = cat
            db.cache_put(normalise(name), cat)
    return result


def _model_categorize(names: list[str]) -> dict[str, str]:
    """One guided-decoding call returning {name: category} for unknown items."""
    enum = list(config.CATEGORY_KEYS)
    schema = {
        "type": "object",
        "properties": {n: {"type": "string", "enum": enum} for n in names},
        "required": names,
    }
    prompt = (
        "Classify each shopping item into exactly one category from "
        f"{enum}. 'junk' = snacks/sweets/fast food, 'healthy' = fresh produce, "
        "'drinks' = any beverage, 'groceries' = staples like bread/eggs/pasta, "
        "'household' = non-food, 'activities' = eating out/entertainment. "
        f"Items: {names}. Respond with JSON only."
    )
    try:
        if config.USE_ZEROGPU_FALLBACK:
            from zerogpu_backend import chat_json
            raw = chat_json(prompt, schema)
        else:
            from openai import OpenAI
            client = OpenAI(base_url=config.MODAL_ENDPOINT_URL, api_key=config.MODAL_API_KEY or "x")
            resp = client.chat.completions.create(
                model=config.MODEL_ID,
                messages=[{"role": "user", "content": prompt}],
                temperature=0, max_tokens=512,
                extra_body={"guided_json": schema},
            )
            raw = resp.choices[0].message.content
        return {n: config.normalise_category(c) for n, c in json.loads(raw).items()}
    except Exception:
        # Never block the user on categorisation; they can fix it in the review grid.
        return {n: "other" for n in names}
