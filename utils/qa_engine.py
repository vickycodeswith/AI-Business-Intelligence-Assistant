"""Deterministic, schema-aware answers for common dataset questions."""
from __future__ import annotations

import pandas as pd
from utils.profiling import profile_dataset, find_column_mentioned


def answer_question(question: str, df: pd.DataFrame, insights: dict | None = None):
    q = question.strip().lower()
    if not q:
        return None
    profile = profile_dataset(df)
    insights = insights or {}
    metrics = profile["measure_columns"]
    dimensions = profile["dimension_columns"]

    if any(word in q for word in ("how many rows", "number of rows", "row count", "record count")):
        return f"The dataset contains {len(df):,} rows."
    if any(word in q for word in ("how many columns", "number of columns", "column count")):
        return f"The dataset contains {len(df.columns):,} columns."
    if "missing" in q:
        return f"The dataset contains {int(df.isna().sum().sum()):,} missing cells."
    if "duplicate" in q:
        return f"The dataset contains {int(df.duplicated().sum()):,} duplicate rows."

    chosen_metric = find_column_mentioned(q, metrics) or profile["default_metric"]
    wants_average = any(w in q for w in ("average", "mean", "on average"))
    wants_min = any(w in q for w in ("minimum", "lowest", "smallest"))
    wants_max = any(w in q for w in ("maximum", "highest", "largest", "top", "best"))
    wants_count = "count" in q or "how many" in q
    wants_sum = any(w in q for w in ("total", "sum", "overall"))

    mentioned_dimension = find_column_mentioned(q, dimensions)
    if mentioned_dimension and chosen_metric and any(w in q for w in ("by", "per", "across", "group", "top", "highest", "best")):
        work = df[[mentioned_dimension, chosen_metric]].copy()
        work[chosen_metric] = pd.to_numeric(work[chosen_metric], errors="coerce")
        grouped = work.dropna().groupby(mentioned_dimension)[chosen_metric].sum().sort_values(ascending=False)
        if grouped.empty:
            return f"There are no usable values to summarize {chosen_metric} by {mentioned_dimension}."
        if wants_max:
            return f"The highest {chosen_metric} total is for {grouped.index[0]}: {grouped.iloc[0]:,.2f}."
        return "Totals by " + mentioned_dimension + ":\n" + grouped.head(15).to_string()

    if chosen_metric:
        values = pd.to_numeric(df[chosen_metric], errors="coerce").dropna()
        if values.empty:
            return f"Column {chosen_metric} does not contain usable numeric values."
        if wants_average:
            return f"Average {chosen_metric}: {values.mean():,.2f}"
        if wants_min:
            return f"Minimum {chosen_metric}: {values.min():,.2f}"
        if wants_max:
            return f"Maximum {chosen_metric}: {values.max():,.2f}"
        if wants_count:
            return f"Non-missing numeric observations in {chosen_metric}: {values.count():,}"
        if wants_sum or any(w in q for w in ("revenue", "sales", "profit", "amount", "spend")):
            return f"Total {chosen_metric}: {values.sum():,.2f}"

    if any(w in q for w in ("columns", "fields", "schema")):
        return "Available columns: " + ", ".join(map(str, df.columns))
    return None
