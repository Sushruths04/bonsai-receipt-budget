"""Gradio theme + small HTML builders shared by app.py."""
from __future__ import annotations

from pathlib import Path

import gradio as gr

import config

THEME = gr.themes.Soft(
    primary_hue=gr.themes.colors.green,
    neutral_hue=gr.themes.colors.stone,
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
).set(
    body_background_fill="#faf9f6",
    block_background_fill="#ffffff",
    block_border_width="1px",
    block_radius="16px",
)


def css() -> str:
    return (Path(__file__).parent / "styles.css").read_text()


def header_html() -> str:
    return (
        '<div id="bonsai-header">'
        '<span class="mark">Bonsai</span>'
        '<span class="tag">See where it goes — receipt by receipt.</span>'
        "</div>"
    )


def kpi_html(label: str, value: str, sub: str = "", warn: bool = False) -> str:
    cls = "value warn" if warn else "value"
    sub_html = f'<div class="sub">{sub}</div>' if sub else ""
    return (f'<div class="kpi"><div class="label">{label}</div>'
            f'<div class="{cls}">{value}</div>{sub_html}</div>')


def budget_bar_html(spent: float, budget: float) -> str:
    pct = min(100, round(100 * spent / budget)) if budget else 0
    over = spent > budget
    cls = "budget-fill over" if over else "budget-fill"
    caption = (f"{config.money(spent)} of {config.money(budget)}"
               + (" — over budget" if over else ""))
    return (f'<div class="budget-track"><div class="{cls}" style="width:{pct}%"></div></div>'
            f'<div class="sub" style="margin-top:6px;color:#6b736e">{caption}</div>')


def insight_html(headline: str, note: str) -> str:
    return (f'<div class="insight">{headline}'
            f'<div class="muted" style="margin-top:6px">{note}</div></div>')
