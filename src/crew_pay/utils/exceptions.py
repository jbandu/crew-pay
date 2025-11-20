"""
Custom exceptions for crew pay system.
"""


class CrewPayError(Exception):
    """Base exception for crew pay system."""

    pass


class ValidationError(CrewPayError):
    """Error during validation."""

    pass


class AgentError(CrewPayError):
    """Error during agent execution."""

    pass


class WorkflowError(CrewPayError):
    """Error during workflow execution."""

    pass


class ConfigurationError(CrewPayError):
    """Error in configuration."""

    pass


class DataError(CrewPayError):
    """Error in data processing."""

    pass


class ExternalServiceError(CrewPayError):
    """Error communicating with external service."""

    pass
