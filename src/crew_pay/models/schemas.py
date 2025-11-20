"""
Data schemas for crew pay validation and claims processing.
"""

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class PayPeriodType(str, Enum):
    """Type of pay period."""

    WEEKLY = "weekly"
    BI_WEEKLY = "bi_weekly"
    SEMI_MONTHLY = "semi_monthly"
    MONTHLY = "monthly"


class PayStatus(str, Enum):
    """Status of pay record."""

    PENDING = "pending"
    VALIDATED = "validated"
    REJECTED = "rejected"
    PROCESSED = "processed"
    PAID = "paid"


class ClaimType(str, Enum):
    """Type of claim."""

    OVERTIME = "overtime"
    REIMBURSEMENT = "reimbursement"
    BONUS = "bonus"
    ADJUSTMENT = "adjustment"
    DISPUTE = "dispute"


class ClaimStatus(str, Enum):
    """Status of claim."""

    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"


class ValidationStatus(str, Enum):
    """Validation result status."""

    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    REQUIRES_REVIEW = "requires_review"


class CrewMember(BaseModel):
    """Crew member information."""

    id: str = Field(..., description="Unique crew member identifier")
    name: str = Field(..., description="Full name")
    employee_id: str = Field(..., description="Employee ID")
    department: str = Field(..., description="Department")
    position: str = Field(..., description="Job position")
    hourly_rate: Decimal = Field(..., description="Hourly rate", gt=0)
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "crew-001",
                "name": "John Doe",
                "employee_id": "EMP-12345",
                "department": "Engineering",
                "position": "Senior Engineer",
                "hourly_rate": "75.50",
                "email": "john.doe@example.com",
                "phone": "+1-555-0100",
            }
        }


class PayRecord(BaseModel):
    """Pay record for a crew member."""

    id: str = Field(..., description="Unique pay record identifier")
    crew_member: CrewMember = Field(..., description="Crew member details")
    pay_period_start: date = Field(..., description="Start date of pay period")
    pay_period_end: date = Field(..., description="End date of pay period")
    pay_period_type: PayPeriodType = Field(..., description="Type of pay period")
    regular_hours: Decimal = Field(default=Decimal("0"), description="Regular hours worked", ge=0)
    overtime_hours: Decimal = Field(default=Decimal("0"), description="Overtime hours", ge=0)
    gross_pay: Decimal = Field(..., description="Gross pay amount", ge=0)
    deductions: Decimal = Field(default=Decimal("0"), description="Total deductions", ge=0)
    net_pay: Decimal = Field(..., description="Net pay amount", ge=0)
    status: PayStatus = Field(default=PayStatus.PENDING, description="Pay record status")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Update timestamp")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @field_validator("pay_period_end")
    @classmethod
    def validate_pay_period(cls, v: date, info: Any) -> date:
        """Validate that pay period end is after start."""
        if "pay_period_start" in info.data and v < info.data["pay_period_start"]:
            raise ValueError("Pay period end must be after start date")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "id": "pay-2024-001",
                "crew_member": CrewMember.Config.json_schema_extra["example"],
                "pay_period_start": "2024-01-01",
                "pay_period_end": "2024-01-15",
                "pay_period_type": "bi_weekly",
                "regular_hours": "80.0",
                "overtime_hours": "5.0",
                "gross_pay": "6415.00",
                "deductions": "1283.00",
                "net_pay": "5132.00",
                "status": "pending",
            }
        }


class Claim(BaseModel):
    """Claim submitted by crew member."""

    id: str = Field(..., description="Unique claim identifier")
    crew_member: CrewMember = Field(..., description="Crew member details")
    claim_type: ClaimType = Field(..., description="Type of claim")
    amount: Decimal = Field(..., description="Claim amount", gt=0)
    description: str = Field(..., description="Claim description")
    supporting_documents: list[str] = Field(
        default_factory=list, description="List of document URLs/paths"
    )
    submitted_date: datetime = Field(
        default_factory=datetime.now, description="Submission timestamp"
    )
    status: ClaimStatus = Field(default=ClaimStatus.SUBMITTED, description="Claim status")
    reviewer_notes: Optional[str] = Field(None, description="Reviewer notes")
    approved_amount: Optional[Decimal] = Field(None, description="Approved amount", ge=0)
    reviewed_at: Optional[datetime] = Field(None, description="Review timestamp")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "claim-2024-001",
                "crew_member": CrewMember.Config.json_schema_extra["example"],
                "claim_type": "overtime",
                "amount": "500.00",
                "description": "Overtime work on emergency deployment",
                "supporting_documents": ["doc1.pdf", "timesheet.xlsx"],
                "status": "submitted",
            }
        }


class ValidationResult(BaseModel):
    """Result of validation check."""

    check_name: str = Field(..., description="Name of validation check")
    status: ValidationStatus = Field(..., description="Validation status")
    message: str = Field(..., description="Validation message")
    details: dict[str, Any] = Field(default_factory=dict, description="Additional details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "check_name": "hours_limit_check",
                "status": "passed",
                "message": "Total hours within acceptable limits",
                "details": {"total_hours": 85, "limit": 100},
            }
        }


class ValidationReport(BaseModel):
    """Comprehensive validation report."""

    pay_record_id: str = Field(..., description="Pay record identifier")
    overall_status: ValidationStatus = Field(..., description="Overall validation status")
    validation_results: list[ValidationResult] = Field(
        default_factory=list, description="Individual validation results"
    )
    created_at: datetime = Field(default_factory=datetime.now, description="Report timestamp")
    summary: str = Field(..., description="Summary of validation")

    class Config:
        json_schema_extra = {
            "example": {
                "pay_record_id": "pay-2024-001",
                "overall_status": "passed",
                "validation_results": [
                    ValidationResult.Config.json_schema_extra["example"]
                ],
                "summary": "All validation checks passed successfully",
            }
        }


class ClaimDecision(BaseModel):
    """Decision on a claim."""

    claim_id: str = Field(..., description="Claim identifier")
    decision: ClaimStatus = Field(..., description="Claim decision")
    approved_amount: Decimal = Field(..., description="Approved amount", ge=0)
    rationale: str = Field(..., description="Decision rationale")
    reviewer: str = Field(..., description="Reviewer identifier")
    reviewed_at: datetime = Field(default_factory=datetime.now, description="Review timestamp")
    next_steps: list[str] = Field(default_factory=list, description="Next steps to take")

    class Config:
        json_schema_extra = {
            "example": {
                "claim_id": "claim-2024-001",
                "decision": "approved",
                "approved_amount": "500.00",
                "rationale": "Overtime work verified and approved",
                "reviewer": "manager-001",
                "next_steps": ["Process payment", "Notify crew member"],
            }
        }
