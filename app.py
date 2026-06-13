"""Bonsai — receipt-based budget tracker. Gradio frontend.

Flow: upload a receipt -> MiniCPM-V (on Modal) extracts items -> we categorise
them -> you review & fix in a grid -> save -> the dashboard updates.
"""
from __future__ import annotations

import json
from datetime import date

import gradio as gr
import pandas as pd

import categorize
import charts
import config
import db
import insights
from extract import extract_receipt
from ui import theme

db.init_db()

GRID_COLS = ["Item", "Qty", "Unit price", "Line total", "Category"]
CAT_HINT = " / ".join(config.CATEGORY_KEYS)


# --- Step 1: extract --------------------------------------------------------
def on_upload(image_path):
    if not image_path:
        raise gr.Error("Upload a receipt photo first.")
    try:
        receipt = extract_receipt(image_path)
    except Exception as exc:  # surface a clean message, keep the app alive
        raise gr.Error(f"Couldn't read that receipt: {exc}")

    cats = categorize.categorize([it.name for it in receipt.items])
    rows = [[it.name, it.qty, it.unit_price, it.line_total, cats.get(it.name, "other")]
            for it in receipt.items]
    df = pd.DataFrame(rows, columns=GRID_COLS)

    meta = {
        "store": receipt.store or "",
        "date": (receipt.date or date.today()).isoformat(),
        "currency": receipt.currency or config.DEFAULT_CURRENCY,
        "total": receipt.total or receipt.line_sum(),
    }
    warn = "" if receipt.totals_match() else (
        f"⚠ Line items add up to {config.money(receipt.line_sum())} but the printed "
        f"total is {config.money(receipt.total)}. Check the rows before saving.")
    return (df, json.dumps(meta), gr.update(value=meta["store"]), gr.update(value=meta["date"]),
            gr.update(value=warn, visible=bool(warn)), gr.update(selected="review"))


# --- Step 2: save -----------------------------------------------------------
def on_save(df: pd.DataFrame, meta_json: str, store: str, purchase_date: str):
    if df is None or len(df) == 0:
        raise gr.Error("Nothing to save.")
    meta = json.loads(meta_json or "{}")
    items = []
    for _, r in df.iterrows():
        try:
            line_total = float(r["Line total"] or 0)
        except (ValueError, TypeError):
            line_total = 0.0
        items.append({
            "name": str(r["Item"]).strip(),
            "qty": float(r["Qty"] or 1),
            "unit_price": _to_float(r["Unit price"]),
            "line_total": line_total,
            "category": config.normalise_category(str(r["Category"])),
        })
    total = round(sum(i["line_total"] for i in items), 2)
    db.save_receipt(
        store=store or meta.get("store"), purchase_date=purchase_date or meta["date"],
        currency=meta.get("currency", config.DEFAULT_CURRENCY), total=total, items=items,
    )
    gr.Info(f"Saved {len(items)} items · {config.money(total)}")
    return (*dashboard_state(), gr.update(selected="dashboard"))


def _to_float(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


# --- Step 3: dashboard ------------------------------------------------------
def on_set_budget(value: float):
    db.set_setting("monthly_budget", str(float(value or 0)))
    return dashboard_state()


def dashboard_state():
    spent = db.month_total()
    budget = db.get_monthly_budget()
    import calendar
    today = date.today()
    days_left = max(1, calendar.monthrange(today.year, today.month)[1] - today.day)
    per_day = max(0, (budget - spent)) / days_left
    over = spent > budget

    kpis = (
        theme.kpi_html("Spent this month", config.money(spent), warn=over)
        + theme.kpi_html("Budget left", config.money(max(0, budget - spent)),
                         sub=("Over budget" if over else f"{days_left} days left"), warn=over)
        + theme.kpi_html("Daily allowance", config.money(per_day),
                         sub="for the rest of the month")
    )
    return (
        gr.update(value=kpis),
        gr.update(value=theme.budget_bar_html(spent, budget)),
        gr.update(value=theme.insight_html(insights.headline(), insights.category_note())),
        charts.donut(db.category_totals_month()),
        charts.trend(db.category_by_month(3)),
    )


# --- Layout -----------------------------------------------------------------
def build() -> gr.Blocks:
    with gr.Blocks(theme=theme.THEME, css=theme.css(), title="Bonsai") as demo:
        meta_state = gr.State("{}")
        gr.HTML(theme.header_html())

        with gr.Tabs() as tabs:
            # ---- Add receipt ------------------------------------------------
            with gr.Tab("Add receipt", id="add"):
                with gr.Row():
                    with gr.Column(scale=1):
                        image = gr.Image(type="filepath", label="Receipt photo",
                                         sources=["upload", "webcam"], height=360)
                        read_btn = gr.Button("Read receipt", variant="primary",
                                             elem_classes="primary")
                    with gr.Column(scale=1):
                        gr.Markdown("### How it works")
                        gr.Markdown(
                            "1. Snap or upload a receipt.\n"
                            "2. Bonsai reads the items and tags each one.\n"
                            "3. You fix anything that's off, then save.\n\n"
                            "Your data stays in this Space — nothing is shared.")

            # ---- Review & edit ---------------------------------------------
            with gr.Tab("Review", id="review"):
                warn_box = gr.Markdown(visible=False)
                with gr.Row():
                    store_in = gr.Textbox(label="Store", scale=2)
                    date_in = gr.Textbox(label="Date (YYYY-MM-DD)", scale=1)
                grid = gr.Dataframe(
                    headers=GRID_COLS, datatype=["str", "number", "number", "number", "str"],
                    label=f"Items — category: {CAT_HINT}", interactive=True, wrap=True)
                save_btn = gr.Button("Save to my month", variant="primary",
                                     elem_classes="primary")

            # ---- Dashboard --------------------------------------------------
            with gr.Tab("Dashboard", id="dashboard"):
                kpi_row = gr.HTML()
                with gr.Row():
                    with gr.Column(scale=2):
                        budget_bar = gr.HTML()
                        with gr.Row():
                            budget_in = gr.Number(label="Monthly budget",
                                                  value=db.get_monthly_budget(), scale=2)
                            budget_btn = gr.Button("Update", scale=1)
                        insight_box = gr.HTML()
                    with gr.Column(scale=1):
                        donut_plot = gr.Plot(label="This month by category")
                trend_plot = gr.Plot(label="Last 3 months")

        # wiring
        read_btn.click(
            on_upload, inputs=image,
            outputs=[grid, meta_state, store_in, date_in, warn_box, tabs],
            show_api=False)
        save_btn.click(
            on_save, inputs=[grid, meta_state, store_in, date_in],
            outputs=[kpi_row, budget_bar, insight_box, donut_plot, trend_plot, tabs],
            show_api=False)
        budget_btn.click(on_set_budget, inputs=budget_in,
                         outputs=[kpi_row, budget_bar, insight_box, donut_plot, trend_plot],
                         show_api=False)
        demo.load(dashboard_state,
                  outputs=[kpi_row, budget_bar, insight_box, donut_plot, trend_plot],
                  show_api=False)
    return demo


if __name__ == "__main__":
    build().launch(show_api=False)
