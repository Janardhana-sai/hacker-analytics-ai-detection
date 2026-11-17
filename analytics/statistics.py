"""
Descriptive statistics utilities built on Pandas.
Computes metrics strictly from actually available numeric values.
"""

from __future__ import annotations

from typing import Iterable

import pandas as pd


def safe_percentage(part: float, total: float) -> float:
    """Compute a percentage safely, returning 0.0 if total is zero or negative."""
    if total <= 0:
        return 0.0
    return round((part / total) * 100.0, 2)


def compute_numeric_summary(values: Iterable[float | int | None]) -> dict[str, float | int | None]:
    """
    Compute descriptive statistics for a sequence of numeric values.
    Returns None values when no valid numbers are present (never fabricates metrics).
    """
    cleaned = [float(v) for v in values if v is not None]
    if not cleaned:
        return {
            "count": 0,
            "sum": None,
            "mean": None,
            "median": None,
            "min": None,
            "max": None,
        }

    series = pd.Series(cleaned, dtype="float64")
    return {
        "count": int(series.count()),
        "sum": round(float(series.sum()), 2),
        "mean": round(float(series.mean()), 2),
        "median": round(float(series.median()), 2),
        "min": round(float(series.min()), 2),
        "max": round(float(series.max()), 2),
    }

