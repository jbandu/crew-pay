"""
State management for LangGraph orchestration.
"""

from datetime import datetime
from typing import Annotated, Any, Optional, Sequence

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from crew_pay.models.schemas import (
    Claim,
    ClaimDecision,
    PayRecord,
    ValidationReport,
)


def add_messages(left: Sequence[BaseMessage], right: Sequence[BaseMessage]) -> list[BaseMessage]:
    """Add messages to the state."""
    return list(left) + list(right)


class WorkflowState(TypedDict):
    """
    State for the crew pay workflow orchestration.

    This state is passed between agents in the LangGraph workflow.
    """

    # Messages exchanged between agents
    messages: Annotated[Sequence[BaseMessage], add_messages]

    # Input data
    pay_record: Optional[PayRecord]
    claim: Optional[Claim]

    # Processing results
    validation_report: Optional[ValidationReport]
    claim_decision: Optional[ClaimDecision]

    # Workflow control
    current_agent: str
    next_agent: Optional[str]
    workflow_status: str  # "in_progress", "completed", "failed"
    error_message: Optional[str]

    # Metadata
    workflow_id: str
    started_at: datetime
    completed_at: Optional[datetime]
    iteration_count: int
    metadata: dict[str, Any]


class AgentInput(BaseModel):
    """Input for an agent."""

    messages: list[BaseMessage] = Field(default_factory=list, description="Conversation messages")
    context: dict[str, Any] = Field(default_factory=dict, description="Additional context")
    pay_record: Optional[PayRecord] = Field(None, description="Pay record to process")
    claim: Optional[Claim] = Field(None, description="Claim to process")


class AgentOutput(BaseModel):
    """Output from an agent."""

    messages: list[BaseMessage] = Field(default_factory=list, description="Response messages")
    result: dict[str, Any] = Field(default_factory=dict, description="Processing result")
    next_agent: Optional[str] = Field(None, description="Next agent to invoke")
    should_continue: bool = Field(True, description="Whether workflow should continue")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class WorkflowConfig(BaseModel):
    """Configuration for workflow execution."""

    max_iterations: int = Field(default=10, description="Maximum workflow iterations", ge=1)
    timeout_seconds: int = Field(default=300, description="Workflow timeout in seconds", ge=1)
    enable_human_in_loop: bool = Field(
        default=False, description="Enable human approval steps"
    )
    notification_enabled: bool = Field(default=True, description="Enable notifications")
    compliance_checks_required: bool = Field(
        default=True, description="Require compliance checks"
    )
    auto_approve_threshold: Optional[float] = Field(
        None, description="Auto-approve threshold for claims", ge=0
    )


class WorkflowResult(BaseModel):
    """Final result of workflow execution."""

    workflow_id: str = Field(..., description="Workflow identifier")
    status: str = Field(..., description="Final status")
    pay_record: Optional[PayRecord] = Field(None, description="Processed pay record")
    claim: Optional[Claim] = Field(None, description="Processed claim")
    validation_report: Optional[ValidationReport] = Field(None, description="Validation report")
    claim_decision: Optional[ClaimDecision] = Field(None, description="Claim decision")
    messages: list[BaseMessage] = Field(default_factory=list, description="Workflow messages")
    started_at: datetime = Field(..., description="Start timestamp")
    completed_at: datetime = Field(..., description="Completion timestamp")
    duration_seconds: float = Field(..., description="Execution duration")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
