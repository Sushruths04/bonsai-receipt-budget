"""Central configuration: env, spending categories, and the visual palette.

Categories are deliberately descriptive, not moralising. "junk" is just a label
for the kind of thing it is, not a judgement about the person buying it.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

# --- Runtime / services -----------------------------------------------------
MODAL_ENDPOINT_URL = os.getenv("MODAL_ENDPOINT_URL", "").rstrip("/")
MODAL_API_KEY = os.getenv("MODAL_API_KEY", "")
MODEL_ID = os.getenv("MODEL_ID", "openbmb/MiniCPM-V-4_5")
DB_PATH = os.getenv("BONSAI_DB_PATH", "data/bonsai.db")
SEED_DB_PATH = os.getenv("BONSAI_SEED_DB", "seed.db")
USE_ZEROGPU_FALLBACK = os.getenv("USE_ZEROGPU_FALLBACK", "0") == "1"

DEFAULT_CURRENCY = "EUR"
CURRENCY_SYMBOL = {"EUR": "€", "USD": "$", "GBP": "£", "INR": "₹"}


@dataclass(frozen=True)
class Category:
    key: str
    label: str
    color: str  # editorial palette, intentionally NOT the default Gradio orange


# Order matters: it's the order shown in tables, legends and the donut.
CATEGORIES: tuple[Category, ...] = (
    Category("groceries", "Groceries", "#2f6f4e"),
    Category("healthy", "Fresh & healthy", "#5ba672"),
    Category("drinks", "Drinks", "#3a7ca5"),
    Category("junk", "Snacks & junk", "#c2613f"),
    Category("household", "Household", "#8a7a66"),
    Category("activities", "Going out", "#9b6a9e"),
    Category("other", "Other", "#9aa0a6"),
)

CATEGORY_KEYS: tuple[str, ...] = tuple(c.key for c in CATEGORIES)
CATEGORY_LABEL = {c.key: c.label for c in CATEGORIES}
CATEGORY_COLOR = {c.key: c.color for c in CATEGORIES}


def normalise_category(value: str | None) -> str:
    """Map any model/free-text value onto a known category key."""
    if not value:
        return "other"
    v = value.strip().lower()
    if v in CATEGORY_KEYS:
        return v
    aliases = {
        "snacks": "junk", "snack": "junk", "sweets": "junk", "candy": "junk",
        "fast food": "junk", "fruit": "healthy", "vegetables": "healthy",
        "produce": "healthy", "beverages": "drinks", "beverage": "drinks",
        "soda": "drinks", "alcohol": "drinks", "staples": "groceries",
        "pantry": "groceries", "cleaning": "household", "entertainment": "activities",
    }
    return aliases.get(v, "other")


def money(amount: float | None, currency: str = DEFAULT_CURRENCY) -> str:
    sym = CURRENCY_SYMBOL.get(currency, currency + " ")
    return f"{sym}{(amount or 0):,.2f}"
