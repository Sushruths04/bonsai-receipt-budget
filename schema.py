"""Pydantic schema for receipt extraction.

The JSON Schema produced here is handed to the model as a `guided_json`
constraint, so the model is *forced* to emit conforming JSON. That means we
never have to strip code fences or repair malformed output downstream.
"""
from __future__ import annotations

import datetime as dt

from pydantic import BaseModel, Field


class LineItem(BaseModel):
    name: str = Field(description="Product name exactly as printed on the receipt")
    qty: float = Field(default=1, description="Quantity; 1 if not printed")
    unit_price: float | None = Field(default=None, description="Price per unit")
    line_total: float = Field(description="Total paid for this line")


class Receipt(BaseModel):
    store: str | None = Field(default=None, description="Shop / merchant name")
    date: dt.date | None = Field(default=None, description="Purchase date")
    currency: str = Field(default="EUR", description="ISO currency code, e.g. EUR")
    items: list[LineItem] = Field(default_factory=list)
    total: float | None = Field(default=None, description="Grand total paid")

    def line_sum(self) -> float:
        return round(sum(i.line_total for i in self.items), 2)

    def totals_match(self, tol: float = 0.05) -> bool:
        """True if line items roughly reconcile with the printed total."""
        if self.total is None or not self.items:
            return True
        return abs(self.line_sum() - self.total) <= max(tol, 0.02 * self.total)


def guided_json_schema() -> dict:
    """JSON Schema passed to vLLM as `guided_json`.

    Keep this intentionally simple: vLLM's XGrammar backend supports a smaller
    JSON Schema subset than Pydantic emits for optional/date fields.
    """
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "store": {"type": "string"},
            "date": {"type": "string"},
            "currency": {"type": "string"},
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "name": {"type": "string"},
                        "qty": {"type": "number"},
                        "unit_price": {"type": "number"},
                        "line_total": {"type": "number"},
                    },
                    "required": ["name", "qty", "unit_price", "line_total"],
                },
            },
            "total": {"type": "number"},
        },
        "required": ["store", "date", "currency", "items", "total"],
    }
