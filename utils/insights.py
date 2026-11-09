"""Dataset-independent numeric summaries and categorical breakdowns."""
from __future__ import annotations

import pandas as pd
from utils.profiling import profile_dataset


def generate_insights(df: pd.DataFrame) -> dict:
    profile = profile_dataset(df)
    metrics = {}
    for col in profile["measure_columns"]:
        values = pd.to_numeric(df[col], errors="coerce").dropna()
        if values.empty:
            continue
        metrics[col] = {
            "sum": float(values.sum()),
            "mean": float(values.mean()),
            "median": float(values.median()),
            "min": float(values.min()),
            "max": float(values.max()),
            "count": int(values.count()),
        }

    breakdowns = {}
    metric = profile["default_metric"]
    if metric:
        for dimension in profile["dimension_columns"]:
            grouped = df[[dimension, metric]].copy()
            grouped[metric] = pd.to_numeric(grouped[metric], errors="coerce")
            result = grouped.dropna().groupby(dimension, dropna=True)[metric].sum().sort_values(ascending=False)
            if not result.empty:
                breakdowns[dimension] = {
                    "metric": metric,
                    "top_category": str(result.index[0]),
                    "top_value": float(result.iloc[0]),
                    "values": result.head(10).to_dict(),
                }

    return {
        "profile": profile,
        "metrics": metrics,
        "default_metric": metric,
        "breakdowns": breakdowns,
    }


def generate_recommendations(insights: dict) -> list[str]:
    recommendations = []
    metrics = insights.get("metrics", {})
    profile = insights.get("profile", {})
    metric = insights.get("default_metric")

    if not metrics:
        recommendations.append("No numerical measure was detected. Add or select a numeric field to calculate quantitative KPIs.")
    elif metric:
        values = metrics[metric]
        recommendations.append(
            f"Use {metric} as the primary measure for this dataset. Its total is {values['sum']:,.2f} "
            f"and its average is {values['mean']:,.2f}."
        )

    for dimension, summary in insights.get("breakdowns", {}).items():
        recommendations.append(
            f"{summary['top_category']} has the highest {summary['metric']} total among the values in {dimension}. "
            "Review this segment to understand what is driving the result."
        )
        if len(recommendations) >= 4:
            break

    if profile.get("missing_values", 0):
        recommendations.append(
            f"Review the {profile['missing_values']:,} missing cells before relying on results that use those columns."
        )
    return recommendations
