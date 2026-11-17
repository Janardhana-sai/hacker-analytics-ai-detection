"""
General-purpose helper functions for timestamps, hashing, JSON serialization, and formatting.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def format_timestamp(ts_str: str | None) -> str:
    """Format an ISO-8601 timestamp string into a readable display string."""
    if not ts_str:
        return "N/A"
    try:
        cleaned = ts_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except (ValueError, TypeError):
        return str(ts_str)


def safe_json_dumps(data: Any, default: str = "{}") -> str:
    """Safely serialize Python objects to a JSON string."""
    try:
        return json.dumps(data, ensure_ascii=False, indent=2)
    except (TypeError, ValueError):
        return default


def safe_json_loads(raw: str | None, default: Any = None) -> Any:
    """Safely deserialize a JSON string, returning default on error."""
    if not raw:
        return default
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return default


def truncate_text(text: str | None, max_length: int = 120) -> str:
    """Truncate text cleanly with an ellipsis if it exceeds max_length."""
    if not text:
        return ""
    text = str(text).strip()
    if len(text) <= max_length:
        return text
    return text[: max(0, max_length - 3)].rstrip() + "..."


def compute_code_hash(code: str) -> str:
    """Compute a SHA-256 hash of normalized source code text."""
    return hashlib.sha256(code.encode("utf-8", errors="replace")).hexdigest()


def count_non_empty_fields(profile_data: dict[str, Any]) -> int:
    """
    Count how many meaningful public fields were collected for a HackerRank profile.
    Does not count internal metadata keys.
    """
    tracked_scalar_keys = [
        "username",
        "display_name",
        "profile_url",
        "description",
        "country",
    ]
    tracked_list_keys = [
        "programming_languages",
        "skills",
        "badges",
        "certificates",
        "statistics",
        "recent_activity",
    ]

    count = 0
    for key in tracked_scalar_keys:
        val = profile_data.get(key)
        if isinstance(val, str) and val.strip():
            count += 1
        elif val is not None and not isinstance(val, str):
            count += 1

    for key in tracked_list_keys:
        val = profile_data.get(key)
        if isinstance(val, list) and len(val) > 0:
            count += 1

    return count

