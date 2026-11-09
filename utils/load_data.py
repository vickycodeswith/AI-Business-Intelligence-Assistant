"""Robust CSV and Excel loading with minimal, transparent cleanup."""
from __future__ import annotations

import pandas as pd


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    cleaned = []
    seen: dict[str, int] = {}
    for idx, raw in enumerate(df.columns):
        name = str(raw).replace("\ufeff", "").strip()
        if not name or name.lower().startswith("unnamed:"):
            name = f"column_{idx + 1}"
        count = seen.get(name, 0)
        seen[name] = count + 1
        cleaned.append(name if count == 0 else f"{name}_{count + 1}")
    df.columns = cleaned
    # Drop fully empty columns, but do not silently remove rows or real values.
    df = df.dropna(axis=1, how="all")
    if df.empty or len(df.columns) == 0:
        raise ValueError("The uploaded file contains no usable data.")
    return df


def load_file(uploaded_file) -> pd.DataFrame:
    name = str(getattr(uploaded_file, "name", "uploaded_file")).lower()
    if name.endswith(".csv"):
        last_error = None
        for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin1"):
            for sep in (None, ",", ";", "\t", "|"):
                try:
                    uploaded_file.seek(0)
                    if sep is None:
                        frame = pd.read_csv(uploaded_file, encoding=encoding, sep=None, engine="python")
                    else:
                        frame = pd.read_csv(uploaded_file, encoding=encoding, sep=sep)
                    if len(frame.columns) > 1 or len(frame) > 0:
                        return _clean_columns(frame)
                except Exception as exc:  # try the next encoding/delimiter
                    last_error = exc
        raise ValueError(f"Unable to read this CSV. Check its delimiter and encoding. Details: {last_error}")

    if name.endswith((".xlsx", ".xls")):
        uploaded_file.seek(0)
        try:
            return _clean_columns(pd.read_excel(uploaded_file))
        except Exception as exc:
            raise ValueError(f"Unable to read this Excel file: {exc}") from exc

    raise ValueError("Unsupported file format. Please upload CSV, XLSX or XLS.")
