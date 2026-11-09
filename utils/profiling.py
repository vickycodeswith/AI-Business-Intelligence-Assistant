"""Dataset profiling and lightweight semantic column detection."""
from __future__ import annotations

import re
from typing import Any

import pandas as pd


DATE_NAME_HINTS = ("date", "datetime", "timestamp", "time", "month", "day")
ID_NAME_HINTS = ("id", "uuid", "guid", "key", "code", "zip", "postal", "phone")
METRIC_NAME_HINTS = (
    "sales", "revenue", "amount", "profit", "income", "cost", "expense",
    "spend", "price", "value", "total", "quantity", "qty", "units",
    "demand", "stock", "balance", "clicks", "impressions", "conversion",
    "orders", "count", "salary", "charges", "usage", "hours", "score",
    "rate", "roas", "ctr", "discount", "returns", "target",
)

# Lower values mean a stronger default candidate. Column meaning is still
# ambiguous in many real datasets, so the UI lets the user choose the measure.
METRIC_PRIORITY = (
    "revenue", "sales", "profit", "actual_demand", "demand", "amount",
    "total_value", "income", "orders", "conversions", "units_sold",
    "quantity", "qty", "ad_spend", "spend", "cost", "expense",
    "charges", "usage", "stock", "balance", "salary", "score", "rate",
    "price", "impressions", "clicks", "discount",
)


def _metric_priority(column_name: str) -> tuple[int, int]:
    name = _norm(column_name)
    for rank, hint in enumerate(METRIC_PRIORITY):
        if name == hint or name.endswith("_" + hint) or name.startswith(hint + "_"):
            return rank, len(name)
    return len(METRIC_PRIORITY), len(name)


def _norm(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _looks_like_datetime(series: pd.Series, column_name: str) -> bool:
    if pd.api.types.is_datetime64_any_dtype(series):
        return True
    if pd.api.types.is_numeric_dtype(series) or pd.api.types.is_bool_dtype(series):
        return False
    non_null = series.dropna()
    if len(non_null) < 3:
        return False
    name_hint = any(hint in _norm(column_name) for hint in DATE_NAME_HINTS)
    # Avoid treating arbitrary category strings as dates unless the column name supports it.
    sample = non_null.astype(str).head(100)
    try:
        parsed = pd.to_datetime(sample, errors="coerce", format="mixed")
    except (TypeError, ValueError):
        parsed = pd.to_datetime(sample, errors="coerce")
    ratio = float(parsed.notna().mean())
    return ratio >= (0.60 if name_hint else 0.90) and (name_hint or parsed.nunique() >= 3)


def _is_identifier(series: pd.Series, column_name: str) -> bool:
    name = _norm(column_name)
    if any(hint in name.split("_") or name.endswith(hint) for hint in ID_NAME_HINTS):
        return True
    non_null = series.dropna()
    if len(non_null) >= 20:
        unique_ratio = non_null.nunique() / max(1, len(non_null))
        if unique_ratio >= 0.98 and not any(hint in name for hint in METRIC_NAME_HINTS):
            return True
    return False


def profile_dataset(df: pd.DataFrame) -> dict[str, Any]:
    if df is None or not isinstance(df, pd.DataFrame):
        raise TypeError("Expected a pandas DataFrame.")

    datetime_columns: list[str] = []
    numeric_columns: list[str] = []
    categorical_columns: list[str] = []
    boolean_columns: list[str] = []
    identifier_columns: list[str] = []
    measure_columns: list[str] = []
    dimension_columns: list[str] = []
    column_rows: list[dict[str, Any]] = []

    for col in df.columns:
        series = df[col]
        is_date = _looks_like_datetime(series, str(col))
        is_bool = pd.api.types.is_bool_dtype(series) or (
            series.dropna().nunique() == 2
            and set(map(str, series.dropna().unique())).issubset({"0", "1", "True", "False", "true", "false"})
        )
        is_num = pd.api.types.is_numeric_dtype(series) and not is_bool
        is_cat = (pd.api.types.is_object_dtype(series)
                  or isinstance(series.dtype, pd.CategoricalDtype)
                  or pd.api.types.is_string_dtype(series)) and not is_date
        is_id = _is_identifier(series, str(col))

        if is_date:
            datetime_columns.append(str(col))
        elif is_num:
            numeric_columns.append(str(col))
            if not is_id:
                measure_columns.append(str(col))
        elif is_bool:
            boolean_columns.append(str(col))
            if series.dropna().nunique() > 1:
                dimension_columns.append(str(col))
        elif is_cat:
            categorical_columns.append(str(col))

        if is_cat and not is_id:
            # Keep high-cardinality text columns out of default chart dimensions.
            nunique = series.nunique(dropna=True)
            if 1 < nunique <= min(100, max(20, len(df) // 2)):
                dimension_columns.append(str(col))
        if is_id and not is_date:
            identifier_columns.append(str(col))

        column_rows.append({
            "Column": str(col),
            "Data type": str(series.dtype),
            "Non-null": int(series.notna().sum()),
            "Missing": int(series.isna().sum()),
            "Unique": int(series.nunique(dropna=True)),
            "Detected role": (
                "Date/time" if is_date else
                "Identifier" if is_id else
                "Boolean" if is_bool else
                "Numerical measure candidate" if is_num else
                "Categorical dimension" if is_cat else "Other"
            ),
        })

    # Prioritize plausible business measures, while retaining all other numeric measures.
    measure_columns.sort(key=lambda col: (
        _metric_priority(col),
        numeric_columns.index(col),
    ))

    date_column = datetime_columns[0] if datetime_columns else None
    default_metric = measure_columns[0] if measure_columns else None

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "datetime_columns": datetime_columns,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "boolean_columns": boolean_columns,
        "identifier_columns": identifier_columns,
        "measure_columns": measure_columns,
        "dimension_columns": dimension_columns,
        "date_column": date_column,
        "default_metric": default_metric,
        "column_details": pd.DataFrame(column_rows),
    }


def find_column_mentioned(question: str, columns: list[str]) -> str | None:
    q = _norm(question)
    candidates = sorted(columns, key=len, reverse=True)
    for col in candidates:
        name = _norm(col)
        if name and (name in q or name.replace("_", " ") in question.lower()):
            return col
    return None
