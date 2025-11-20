"""
Crew Pay - LangGraph-based multi-agent orchestration system.

A system for crew pay validation and claims processing using specialized AI agents.
"""

__version__ = "0.1.0"

from crew_pay.agents import (
    ClaimsProcessingAgent,
    ComplianceAgent,
    NotificationAgent,
    PayValidationAgent,
)
from crew_pay.models import (
    Claim,
    ClaimDecision,
    ClaimStatus,
    ClaimType,
    CrewMember,
    PayPeriodType,
    PayRecord,
    PayStatus,
    ValidationReport,
    ValidationResult,
    ValidationStatus,
    WorkflowConfig,
    WorkflowResult,
)
from crew_pay.orchestrator import CrewPayWorkflow

__all__ = [
    # Agents
    "ClaimsProcessingAgent",
    "ComplianceAgent",
    "NotificationAgent",
    "PayValidationAgent",
    # Models
    "Claim",
    "ClaimDecision",
    "ClaimStatus",
    "ClaimType",
    "CrewMember",
    "PayPeriodType",
    "PayRecord",
    "PayStatus",
    "ValidationReport",
    "ValidationResult",
    "ValidationStatus",
    "WorkflowConfig",
    "WorkflowResult",
    # Orchestrator
    "CrewPayWorkflow",
]
