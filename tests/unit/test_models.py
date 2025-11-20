"""Tests for data models."""

from datetime import date, datetime
from decimal import Decimal

import pytest

from crew_pay.models.schemas import (
    Claim,
    ClaimStatus,
    ClaimType,
    CrewMember,
    PayPeriodType,
    PayRecord,
    PayStatus,
    ValidationResult,
    ValidationStatus,
)


def test_crew_member_creation() -> None:
    """Test creating a crew member."""
    crew_member = CrewMember(
        id="crew-001",
        name="John Doe",
        employee_id="EMP-12345",
        department="Engineering",
        position="Senior Engineer",
        hourly_rate=Decimal("75.50"),
        email="john.doe@example.com",
    )

    assert crew_member.id == "crew-001"
    assert crew_member.name == "John Doe"
    assert crew_member.hourly_rate == Decimal("75.50")


def test_pay_record_creation() -> None:
    """Test creating a pay record."""
    crew_member = CrewMember(
        id="crew-001",
        name="John Doe",
        employee_id="EMP-12345",
        department="Engineering",
        position="Senior Engineer",
        hourly_rate=Decimal("75.50"),
    )

    pay_record = PayRecord(
        id="pay-001",
        crew_member=crew_member,
        pay_period_start=date(2024, 1, 1),
        pay_period_end=date(2024, 1, 15),
        pay_period_type=PayPeriodType.BI_WEEKLY,
        regular_hours=Decimal("80.0"),
        overtime_hours=Decimal("5.0"),
        gross_pay=Decimal("6415.00"),
        deductions=Decimal("1283.00"),
        net_pay=Decimal("5132.00"),
    )

    assert pay_record.id == "pay-001"
    assert pay_record.status == PayStatus.PENDING
    assert pay_record.regular_hours == Decimal("80.0")


def test_pay_record_invalid_dates() -> None:
    """Test pay record with invalid date range."""
    crew_member = CrewMember(
        id="crew-001",
        name="John Doe",
        employee_id="EMP-12345",
        department="Engineering",
        position="Senior Engineer",
        hourly_rate=Decimal("75.50"),
    )

    with pytest.raises(ValueError, match="Pay period end must be after start date"):
        PayRecord(
            id="pay-001",
            crew_member=crew_member,
            pay_period_start=date(2024, 1, 15),
            pay_period_end=date(2024, 1, 1),  # End before start
            pay_period_type=PayPeriodType.BI_WEEKLY,
            regular_hours=Decimal("80.0"),
            gross_pay=Decimal("6000.00"),
            net_pay=Decimal("5000.00"),
        )


def test_claim_creation() -> None:
    """Test creating a claim."""
    crew_member = CrewMember(
        id="crew-002",
        name="Jane Smith",
        employee_id="EMP-67890",
        department="Operations",
        position="Manager",
        hourly_rate=Decimal("85.00"),
    )

    claim = Claim(
        id="claim-001",
        crew_member=crew_member,
        claim_type=ClaimType.OVERTIME,
        amount=Decimal("500.00"),
        description="Overtime work on weekend",
        supporting_documents=["timesheet.pdf"],
    )

    assert claim.id == "claim-001"
    assert claim.status == ClaimStatus.SUBMITTED
    assert claim.amount == Decimal("500.00")
    assert len(claim.supporting_documents) == 1


def test_validation_result_creation() -> None:
    """Test creating a validation result."""
    result = ValidationResult(
        check_name="hours_check",
        status=ValidationStatus.PASSED,
        message="Hours within limits",
        details={"total_hours": 85},
    )

    assert result.check_name == "hours_check"
    assert result.status == ValidationStatus.PASSED
    assert result.details["total_hours"] == 85
