"""
Application configuration and settings.
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    openai_model: str = Field(default="gpt-4-turbo-preview", description="OpenAI model to use")
    temperature: float = Field(default=0.7, description="LLM temperature", ge=0, le=2)

    # Agent Configuration
    max_iterations: int = Field(default=10, description="Max workflow iterations", ge=1)
    timeout_seconds: int = Field(default=300, description="Workflow timeout", ge=1)

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or text")

    # Database (Optional)
    database_url: Optional[str] = Field(None, description="Database connection URL")

    # External Services (Optional)
    payroll_api_url: Optional[str] = Field(None, description="Payroll service API URL")
    claims_api_url: Optional[str] = Field(None, description="Claims service API URL")
    notification_service_url: Optional[str] = Field(
        None, description="Notification service API URL"
    )

    # Feature Flags
    enable_human_in_loop: bool = Field(default=False, description="Enable human approval")
    enable_notifications: bool = Field(default=True, description="Enable notifications")
    enable_compliance_checks: bool = Field(default=True, description="Enable compliance checks")

    # Validation Thresholds
    max_regular_hours_per_week: float = Field(
        default=40.0, description="Max regular hours per week", ge=0
    )
    max_overtime_hours_per_week: float = Field(
        default=20.0, description="Max overtime hours per week", ge=0
    )
    auto_approve_claim_threshold: Optional[float] = Field(
        None, description="Auto-approve claims under this amount", ge=0
    )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get settings instance (singleton pattern)."""
    global _settings
    if _settings is None:
        _settings = Settings()  # type: ignore
    return _settings


def reset_settings() -> None:
    """Reset settings instance (useful for testing)."""
    global _settings
    _settings = None
