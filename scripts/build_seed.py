"""Build seed.db from your real receipts so the dashboard looks alive on boot.

Two ways to use it:

(A) From receipt images (runs the live pipeline, then you hand-correct):
      BONSAI_DB_PATH=seed.db python scripts/build_seed.py --images path/to/receipts/*.jpg
    Requires MODAL_ENDPOINT_URL to be set.

(B) From a CSV you fill in by hand (fastest, fully offline):
      BONSAI_DB_PATH=seed.db python scripts/build_seed.py --csv scripts/seed_receipts.csv
    CSV columns: store,date,currency,item,qty,unit_price,line_total,category

Commit the resulting seed.db. This is also your Backyard AI proof — it's *your*
spending, three months of it.
"""
from __future__ import annotations

import argparse
import csv
import glob
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("BONSAI_DB_PATH", "seed.db")

import db  # noqa: E402  (after env + path are set)


def reset_db() -> None:
    """Create seed databases from scratch so repeated runs do not duplicate rows."""
    path = os.environ["BONSAI_DB_PATH"]
    if os.path.exists(path):
        os.remove(path)


def from_csv(path: str) -> None:
    reset_db()
    db.init_db()
    receipts: dict[tuple, list] = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            key = (row["store"], row["date"], row.get("currency", "EUR"))
            receipts[key].append(row)
    for (store, date_, currency), rows in receipts.items():
        items = [{
            "name": r["item"], "qty": float(r.get("qty", 1) or 1),
            "unit_price": float(r["unit_price"]) if r.get("unit_price") else None,
            "line_total": float(r["line_total"]), "category": r.get("category", "other"),
        } for r in rows]
        total = round(sum(i["line_total"] for i in items), 2)
        db.save_receipt(store=store, purchase_date=date_, currency=currency,
                        total=total, items=items)
    print(f"Seeded {len(receipts)} receipts into {os.environ['BONSAI_DB_PATH']}")


def from_images(patterns: list[str]) -> None:
    import categorize
    from extract import extract_receipt
    reset_db()
    db.init_db()
    paths = [p for pat in patterns for p in glob.glob(pat)]
    for p in paths:
        r = extract_receipt(p)
        cats = categorize.categorize([it.name for it in r.items])
        items = [{"name": it.name, "qty": it.qty, "unit_price": it.unit_price,
                  "line_total": it.line_total, "category": cats.get(it.name, "other")}
                 for it in r.items]
        db.save_receipt(store=r.store, purchase_date=(r.date or "").__str__(),
                        currency=r.currency, total=r.total or r.line_sum(), items=items)
        print(f"  + {p}: {len(items)} items")
    print("Review seed.db and hand-correct any mistakes before committing.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv")
    ap.add_argument("--images", nargs="*")
    args = ap.parse_args()
    if args.csv:
        from_csv(args.csv)
    elif args.images:
        from_images(args.images)
    else:
        ap.error("pass --csv FILE or --images GLOB ...")
