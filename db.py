"""SQLite data layer.

On first boot we copy the bundled ``seed.db`` (the user's real ~3 months of
receipts) into the writable working path, so the dashboard looks real
immediately. New entries are written to the working db. On Hugging Face the
working path lives under ``/data`` which persists *only* if persistent storage
is enabled on the Space — otherwise it resets on rebuild and the seed is
re-applied. That trade-off is documented in the README.
"""
from __future__ import annotations

import shutil
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, timedelta
from pathlib import Path

import config

_SCHEMA = """
CREATE TABLE IF NOT EXISTS receipts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    store        TEXT,
    purchase_date TEXT NOT NULL,
    currency     TEXT NOT NULL DEFAULT 'EUR',
    total        REAL NOT NULL DEFAULT 0,
    raw_json     TEXT,
    created_at   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id  INTEGER NOT NULL REFERENCES receipts(id) ON DELETE CASCADE,
    name        TEXT NOT NULL,
    qty         REAL NOT NULL DEFAULT 1,
    unit_price  REAL,
    line_total  REAL NOT NULL DEFAULT 0,
    category    TEXT NOT NULL DEFAULT 'other'
);
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT
);
CREATE TABLE IF NOT EXISTS category_cache (
    name_norm TEXT PRIMARY KEY,
    category  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_items_receipt ON items(receipt_id);
CREATE INDEX IF NOT EXISTS idx_receipts_date ON receipts(purchase_date);
"""


def init_db() -> None:
    path = Path(config.DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() and Path(config.SEED_DB_PATH).exists():
        shutil.copy(config.SEED_DB_PATH, path)
    with _connect() as con:
        con.executescript(_SCHEMA)
        if con.execute("SELECT value FROM settings WHERE key='monthly_budget'").fetchone() is None:
            con.execute("INSERT INTO settings(key, value) VALUES('monthly_budget', '500')")


@contextmanager
def _connect():
    con = sqlite3.connect(config.DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        yield con
        con.commit()
    finally:
        con.close()


# --- Settings ---------------------------------------------------------------
def get_setting(key: str, default: str | None = None) -> str | None:
    with _connect() as con:
        row = con.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    with _connect() as con:
        con.execute(
            "INSERT INTO settings(key, value) VALUES(?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )


def get_monthly_budget() -> float:
    return float(get_setting("monthly_budget", "500") or 500)


# --- Category cache ---------------------------------------------------------
def cache_get(name_norm: str) -> str | None:
    with _connect() as con:
        row = con.execute(
            "SELECT category FROM category_cache WHERE name_norm=?", (name_norm,)
        ).fetchone()
        return row["category"] if row else None


def cache_put(name_norm: str, category: str) -> None:
    with _connect() as con:
        con.execute(
            "INSERT INTO category_cache(name_norm, category) VALUES(?, ?) "
            "ON CONFLICT(name_norm) DO UPDATE SET category=excluded.category",
            (name_norm, category),
        )


# --- Receipts ---------------------------------------------------------------
def save_receipt(
    *, store: str | None, purchase_date: str, currency: str, total: float,
    items: list[dict], raw_json: str | None = None,
) -> int:
    with _connect() as con:
        cur = con.execute(
            "INSERT INTO receipts(store, purchase_date, currency, total, raw_json, created_at) "
            "VALUES(?,?,?,?,?,?)",
            (store, purchase_date, currency, total, raw_json, datetime.utcnow().isoformat()),
        )
        rid = cur.lastrowid
        con.executemany(
            "INSERT INTO items(receipt_id, name, qty, unit_price, line_total, category) "
            "VALUES(?,?,?,?,?,?)",
            [(rid, it["name"], it.get("qty", 1), it.get("unit_price"),
              it["line_total"], it.get("category", "other")) for it in items],
        )
        return rid


# --- Aggregations -----------------------------------------------------------
def _month_bounds(d: date) -> tuple[str, str]:
    start = d.replace(day=1)
    nxt = (start + timedelta(days=32)).replace(day=1)
    return start.isoformat(), nxt.isoformat()


def month_total(d: date | None = None) -> float:
    d = d or date.today()
    start, end = _month_bounds(d)
    with _connect() as con:
        row = con.execute(
            "SELECT COALESCE(SUM(total),0) AS t FROM receipts "
            "WHERE purchase_date >= ? AND purchase_date < ?", (start, end)
        ).fetchone()
        return float(row["t"])


def category_totals_month(d: date | None = None) -> dict[str, float]:
    d = d or date.today()
    start, end = _month_bounds(d)
    with _connect() as con:
        rows = con.execute(
            "SELECT i.category AS c, COALESCE(SUM(i.line_total),0) AS t "
            "FROM items i JOIN receipts r ON r.id = i.receipt_id "
            "WHERE r.purchase_date >= ? AND r.purchase_date < ? GROUP BY i.category",
            (start, end),
        ).fetchall()
        return {r["c"]: float(r["t"]) for r in rows}


def category_by_month(months_back: int = 3) -> list[dict]:
    """Per-category spend for each of the last ``months_back`` calendar months.

    Returns rows like {"month": "2026-04", "category": "junk", "total": 38.0}.
    """
    today = date.today()
    first = today.replace(day=1)
    for _ in range(months_back - 1):
        first = (first - timedelta(days=1)).replace(day=1)
    with _connect() as con:
        rows = con.execute(
            "SELECT substr(r.purchase_date,1,7) AS month, i.category AS category, "
            "       COALESCE(SUM(i.line_total),0) AS total "
            "FROM items i JOIN receipts r ON r.id = i.receipt_id "
            "WHERE r.purchase_date >= ? GROUP BY month, category ORDER BY month",
            (first.isoformat(),),
        ).fetchall()
        return [dict(r) for r in rows]
