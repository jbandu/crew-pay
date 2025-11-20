"""Tests for configuration."""

import os

import pytest

from crew_pay.config.settings import Settings, get_settings, reset_settings


def test_settings_creation() -> None:
    """Test creating settings with environment variables."""
    # Set environment variables
    os.environ["OPENAI_API_KEY"] = "test-key-123"
    os.environ["OPENAI_MODEL"] = "gpt-4"
    os.environ["TEMPERATURE"] = "0.5"

    # Reset settings to pick up new env vars
    reset_settings()

    settings = get_settings()

    assert settings.openai_api_key == "test-key-123"
    assert settings.openai_model == "gpt-4"
    assert settings.temperature == 0.5


def test_settings_defaults() -> None:
    """Test settings default values."""
    os.environ["OPENAI_API_KEY"] = "test-key"
    reset_settings()

    settings = get_settings()

    assert settings.openai_model == "gpt-4-turbo-preview"
    assert settings.temperature == 0.7
    assert settings.max_iterations == 10
    assert settings.log_level == "INFO"


def test_settings_singleton() -> None:
    """Test that settings is a singleton."""
    os.environ["OPENAI_API_KEY"] = "test-key"
    reset_settings()

    settings1 = get_settings()
    settings2 = get_settings()

    assert settings1 is settings2
