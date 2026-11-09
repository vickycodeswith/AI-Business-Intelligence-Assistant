"""Simple, transparent baseline forecasting for any suitable numeric measure."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from utils.profiling import profile_dataset


def _future_dates(dates: pd.Series, periods: int) -> pd.DatetimeIndex:
    unique = pd.DatetimeIndex(sorted(pd.to_datetime(dates, errors="coerce").dropna().unique()))
    if len(unique) == 0:
        return pd.DatetimeIndex([])
    freq = None
    if len(unique) >= 3:
        try:
            freq = pd.infer_freq(unique)
        except (TypeError, ValueError):
            freq = None
    if freq:
        return pd.date_range(start=unique[-1], periods=periods + 1, freq=freq)[1:]
    if len(unique) >= 2:
        delta_days = max(1, int(round(np.median(np.diff(unique.values).astype("timedelta64[s]").astype(float) / 86400))))
    else:
        delta_days = 1
    return pd.date_range(start=unique[-1] + pd.Timedelta(days=delta_days), periods=periods, freq="D")


def forecast_series(df: pd.DataFrame, value_column: str, date_column: str | None = None,
                    periods: int = 7, aggregation: str = "sum") -> dict:
    if value_column not in df.columns:
        raise ValueError(f"Numerical column '{value_column}' was not found.")
    if periods < 1 or periods > 365:
        raise ValueError("Forecast horizon must be between 1 and 365 periods.")

    work = df.copy()
    work[value_column] = pd.to_numeric(work[value_column], errors="coerce")
    work = work.dropna(subset=[value_column])
    if work.empty:
        raise ValueError(f"Column '{value_column}' has no usable numeric values.")

    uses_dates = date_column is not None and date_column in work.columns
    if uses_dates:
        work[date_column] = pd.to_datetime(work[date_column], errors="coerce", format="mixed")
        work = work.dropna(subset=[date_column]).sort_values(date_column)
        if work.empty:
            raise ValueError(f"Column '{date_column}' could not be parsed as dates.")
        if aggregation == "mean":
            series = work.groupby(date_column)[value_column].mean().sort_index()
        else:
            series = work.groupby(date_column)[value_column].sum().sort_index()
        x_history = series.index
        y = series.to_numpy(dtype=float)
        x_future = _future_dates(pd.Series(series.index), periods)
        if len(x_future) != periods:
            raise ValueError("Could not determine future dates for this dataset.")
        # Regression runs on observation order; actual dates are retained for display.
    else:
        y = work[value_column].to_numpy(dtype=float)
        x_history = np.arange(len(y))
        x_future = np.arange(len(y), len(y) + periods)

    if len(y) < 5:
        raise ValueError(f"At least 5 usable observations are required; found {len(y)}.")
    if np.allclose(y, y[0]):
        predicted = np.repeat(float(y[0]), periods)
        model_name = "Constant baseline (series has no variation)"
    else:
        x = np.arange(len(y)).reshape(-1, 1)
        model = LinearRegression()
        model.fit(x, y)
        future_idx = np.arange(len(y), len(y) + periods).reshape(-1, 1)
        predicted = model.predict(future_idx)
        model_name = "Linear regression trend baseline"

    return {
        "value_column": value_column,
        "date_column": date_column if uses_dates else None,
        "history_x": list(x_history),
        "history_y": y.tolist(),
        "forecast_x": list(x_future),
        "forecast_y": np.asarray(predicted, dtype=float).tolist(),
        "next_value": float(predicted[0]),
        "periods": periods,
        "method": model_name,
        "aggregation": aggregation,
    }


def forecast_sales(df):
    """Backward-compatible wrapper; no longer requires a column literally named Sales."""
    profile = profile_dataset(df)
    metric = profile["default_metric"]
    if not metric:
        return None, None
    date_col = profile["date_column"]
    try:
        result = forecast_series(df, metric, date_col, periods=1)
    except ValueError:
        return None, None
    return result["next_value"], (result["history_x"] + result["forecast_x"],
                                  result["history_y"] + result["forecast_y"])
