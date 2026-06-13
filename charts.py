"""Plotly figures for the dashboard. Quiet, editorial styling — no default
Plotly chrome, no gridline clutter, palette driven by config.CATEGORY_COLOR.
"""
from __future__ import annotations

import calendar
from datetime import date

import pandas as pd
import plotly.graph_objects as go

import config

_FONT = dict(family="Inter, system-ui, sans-serif", color="#2b2b2b")
_TRANSPARENT = "rgba(0,0,0,0)"


def _empty(msg: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=msg, showarrow=False, font=dict(_FONT, size=14, color="#9aa0a6"))
    fig.update_layout(
        paper_bgcolor=_TRANSPARENT, plot_bgcolor=_TRANSPARENT,
        xaxis_visible=False, yaxis_visible=False, margin=dict(l=8, r=8, t=8, b=8),
    )
    return fig


def donut(category_totals: dict[str, float]) -> go.Figure:
    data = [(config.CATEGORY_LABEL[k], category_totals[k], config.CATEGORY_COLOR[k])
            for k in config.CATEGORY_KEYS if category_totals.get(k, 0) > 0]
    if not data:
        return _empty("No spending recorded this month yet")
    labels, values, colors = zip(*data)
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.62, sort=False,
        marker=dict(colors=colors, line=dict(color="#ffffff", width=2)),
        textinfo="percent", textfont=dict(_FONT, size=12, color="#ffffff"),
        hovertemplate="%{label}<br>%{percent} · %{value:.2f}<extra></extra>",
    ))
    fig.update_layout(
        showlegend=True, legend=dict(font=dict(_FONT, size=12), orientation="v"),
        paper_bgcolor=_TRANSPARENT, plot_bgcolor=_TRANSPARENT,
        margin=dict(l=8, r=8, t=8, b=8), font=_FONT,
    )
    return fig


def trend(rows: list[dict], months_back: int = 3) -> go.Figure:
    """Stacked bar of spend by category across the last N months."""
    if not rows:
        return _empty("Add a few receipts to see your 3-month trend")
    df = pd.DataFrame(rows)
    months = sorted(df["month"].unique())[-months_back:]
    labels = [f"{calendar.month_abbr[int(m[5:7])]} {m[:4]}" for m in months]
    fig = go.Figure()
    for k in config.CATEGORY_KEYS:
        sub = df[df["category"] == k].set_index("month")["total"]
        vals = [round(float(sub.get(m, 0)), 2) for m in months]
        if sum(vals) == 0:
            continue
        fig.add_bar(
            name=config.CATEGORY_LABEL[k], x=labels, y=vals,
            marker_color=config.CATEGORY_COLOR[k],
            hovertemplate="%{fullData.name}: %{y:.2f}<extra></extra>",
        )
    fig.update_layout(
        barmode="stack", paper_bgcolor=_TRANSPARENT, plot_bgcolor=_TRANSPARENT,
        font=_FONT, margin=dict(l=8, r=8, t=8, b=8),
        legend=dict(font=dict(_FONT, size=11), orientation="h", y=-0.18),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#eee", zeroline=False),
    )
    return fig
