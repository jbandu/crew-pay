"""Tests for helper utilities."""

from datetime import datetime

from crew_pay.utils.helpers import (
    calculate_duration,
    format_currency,
    generate_id,
    merge_dicts,
    safe_dict_get,
)


def test_generate_id() -> None:
    """Test ID generation."""
    id1 = generate_id()
    id2 = generate_id("test")

    assert isinstance(id1, str)
    assert len(id1) > 0
    assert id2.startswith("test-")


def test_format_currency() -> None:
    """Test currency formatting."""
    assert format_currency(1000.00) == "$1,000.00"
    assert format_currency(1234.56) == "$1,234.56"
    assert format_currency(100) == "$100.00"


def test_calculate_duration() -> None:
    """Test duration calculation."""
    start = datetime(2024, 1, 1, 10, 0, 0)
    end = datetime(2024, 1, 1, 10, 5, 30)

    duration = calculate_duration(start, end)

    assert duration == 330.0  # 5 minutes 30 seconds


def test_safe_dict_get() -> None:
    """Test safe dictionary get."""
    data = {"key1": "value1", "key2": "value2"}

    assert safe_dict_get(data, "key1") == "value1"
    assert safe_dict_get(data, "missing") is None
    assert safe_dict_get(data, "missing", "default") == "default"


def test_merge_dicts() -> None:
    """Test dictionary merging."""
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    dict3 = {"e": 5}

    merged = merge_dicts(dict1, dict2, dict3)

    assert merged == {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
