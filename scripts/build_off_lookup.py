"""Build off_lookup.json: normalised product name -> Bonsai category.

Source: Open Food Facts (`openfoodfacts/product-database` on the HF Hub).
We derive the category from NOVA processing group + Nutri-Score + the OFF
category path, using the same mapping the app documents. This gives an offline,
no-GPU, data-backed categoriser for the common case.

Run (needs `datasets`):  python scripts/build_off_lookup.py
Output is written to ./off_lookup.json (committed to the repo).

This is intentionally conservative — it only keeps confident mappings so the
fast path stays accurate; everything else falls through to the model.
"""
from __future__ import annotations

import json
import re
import sys
import argparse
import os
from collections import Counter
from pathlib import Path

OUT = Path("off_lookup.json")

# Map OFF signals -> Bonsai category keys (see config.CATEGORIES).
JUNK_CATS = {"snacks", "sweet-snacks", "chocolates", "candies", "biscuits", "chips",
             "ice-cream", "sodas", "pastries"}
HEALTHY_CATS = {"fruits", "vegetables", "fresh-vegetables", "fresh-fruits", "salads",
                "legumes", "fresh-foods"}
DRINK_CATS = {"beverages", "waters", "juices", "sodas", "teas", "coffees",
              "alcoholic-beverages", "beers", "wines"}
GROCERY_CATS = {"breads", "pastas", "rice", "dairies", "eggs", "cereals", "flours",
                "cooking-oils", "canned-foods", "milks", "cheeses"}


def _name_text(name) -> str:
    if isinstance(name, list):
        by_lang = {
            str(part.get("lang", "")): str(part.get("text", ""))
            for part in name
            if isinstance(part, dict) and part.get("text")
        }
        name = by_lang.get("main") or by_lang.get("en") or by_lang.get("de") or by_lang.get("fr") or ""
    elif isinstance(name, dict):
        name = str(name.get("text", ""))
    return name if isinstance(name, str) else ""


def _norm(name) -> str:
    name = _name_text(name)
    if not isinstance(name, str):
        return ""
    n = name.lower().strip()
    n = re.sub(r"[^a-zäöüß ]", " ", n)
    return re.sub(r"\s+", " ", n).strip()


def _category(product: dict) -> str | None:
    tags = {t.split(":")[-1] for t in (product.get("categories_tags") or [])}
    nova = product.get("nova_group")
    nutri = (product.get("nutriscore_grade") or "").lower()

    if tags & DRINK_CATS:
        return "drinks"
    if tags & JUNK_CATS or nova == 4:
        return "junk"
    if tags & HEALTHY_CATS or nutri in {"a", "b"}:
        return "healthy"
    if tags & GROCERY_CATS:
        return "groceries"
    return None


def main(limit: int = 50_000, progress_every: int = 5_000) -> None:
    try:
        from datasets import load_dataset
    except ImportError:
        sys.exit("pip install datasets  (then re-run)")

    ds = load_dataset("openfoodfacts/product-database", split="food", streaming=True)
    votes: dict[str, Counter] = {}
    seen = 0
    for product in ds:
        seen += 1
        if progress_every and seen % progress_every == 0:
            print(f"Scanned {seen} products...", flush=True)
        if seen > limit:
            break
        name = product.get("product_name")
        if not name:
            continue
        cat = _category(product)
        if not cat:
            continue
        key = _norm(name)
        if 3 <= len(key) <= 40:
            votes.setdefault(key, Counter())[cat] += 1

    lookup = {k: c.most_common(1)[0][0] for k, c in votes.items()}
    OUT.write_text(json.dumps(lookup, ensure_ascii=False))
    print(f"Wrote {len(lookup)} entries to {OUT} (scanned {seen} products)", flush=True)
    os._exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50_000)
    parser.add_argument("--progress-every", type=int, default=5_000)
    args = parser.parse_args()
    main(limit=args.limit, progress_every=args.progress_every)
