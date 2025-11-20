"""
Helper utilities for crew pay system.
"""

import uuid
from datetime import datetime
from typing import Any


def generate_id(prefix: str = "") -> str:
    """Generate a unique identifier."""
    unique_id = str(uuid.uuid4())
    if prefix:
        return f"{prefix}-{unique_id}"
    return unique_id


def get_current_timestamp() -> datetime:
    """Get current timestamp."""
    return datetime.now()


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"${amount:,.2f}"


def calculate_duration(start: datetime, end: datetime) -> float:
    """Calculate duration in seconds between two timestamps."""
    return (end - start).total_seconds()


def safe_dict_get(data: dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get value from dictionary."""
    return data.get(key, default)


def merge_dicts(*dicts: dict[str, Any]) -> dict[str, Any]:
    """Merge multiple dictionaries."""
    result: dict[str, Any] = {}
    for d in dicts:
        result.update(d)
    return result
