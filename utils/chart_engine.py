from __future__ import annotations

import pandas as pd
import plotly.express as px
from utils.profiling import profile_dataset, find_column_mentioned


def generate_chart(question: str, df: pd.DataFrame):
    profile = profile_dataset(df)
    metrics = profile["measure_columns"]
    dimensions = profile["dimension_columns"]
    dates = profile["datetime_columns"]
    q = (question or "").lower()
    if not metrics:
        return None

    metric = find_column_mentioned(q, metrics) or profile["default_metric"]
    dimension = find_column_mentioned(q, dimensions)
    date_col = find_column_mentioned(q, dates) or profile["date_column"]

    if any(k in q for k in ("trend", "over time", "timeline", "forecast", "monthly", "daily")) and date_col:
        work = df[[date_col, metric]].copy()
        work[date_col] = pd.to_datetime(work[date_col], errors="coerce", format="mixed")
        work[metric] = pd.to_numeric(work[metric], errors="coerce")
        work = work.dropna().sort_values(date_col).groupby(date_col, as_index=False)[metric].sum()
        if work.empty:
            return None
        return px.line(work, x=date_col, y=metric, markers=True, title=f"{metric} over time")

    if dimension is None and dimensions:
        dimension = dimensions[0]
    if dimension:
        work = df[[dimension, metric]].copy()
        work[metric] = pd.to_numeric(work[metric], errors="coerce")
        grouped = work.dropna().groupby(dimension, as_index=False)[metric].sum().sort_values(metric, ascending=False).head(25)
        if grouped.empty:
            return None
        return px.bar(grouped, x=dimension, y=metric, title=f"{metric} by {dimension}")

    values = pd.to_numeric(df[metric], errors="coerce").dropna()
    if values.empty:
        return None
    return px.histogram(values, x=metric, title=f"Distribution of {metric}")
