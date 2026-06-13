"""Spending insights — rule-based, non-punitive copy. Deterministic so the
dashboard never says anything embarrassing on demo day. (A short MiniCPM-
generated line can be layered on later behind a flag; the rules stand alone.)
"""
from __future__ import annotations

from datetime import date

import config
import db


def _pct(part: float, whole: float) -> int:
    return round(100 * part / whole) if whole else 0


def headline() -> str:
    spent = db.month_total()
    budget = db.get_monthly_budget()
    today = date.today()
    import calendar
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days_left = days_in_month - today.day
    if spent <= budget:
        remaining = budget - spent
        per_day = remaining / days_left if days_left else remaining
        return (f"You've spent {config.money(spent)} of your {config.money(budget)} "
                f"budget. That leaves about {config.money(per_day)} a day for the "
                f"rest of the month.")
    over = spent - budget
    return (f"You're {config.money(over)} over your {config.money(budget)} budget "
            f"this month. Worth a look at the breakdown below — no judgement.")


def category_note() -> str:
    totals = db.category_totals_month()
    spent = sum(totals.values())
    if not spent:
        return "Add a receipt to see where your money is going."
    top = max(totals, key=totals.get)
    return (f"Your biggest slice this month is {config.CATEGORY_LABEL[top].lower()} "
            f"at {config.money(totals[top])} ({_pct(totals[top], spent)}%).")
