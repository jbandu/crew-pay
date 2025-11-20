"""Pytest configuration and fixtures."""

import os
from datetime import date
from decimal import Decimal

import pytest

from crew_pay.config.settings import reset_settings
from crew_pay.models.schemas import (
    Claim,
    ClaimType,
    CrewMember,
    PayPeriodType,
    PayRecord,
)


@pytest.fixture(autouse=True)
def setup_test_env() -> None:
    """Set up test environment variables."""
    os.environ["OPENAI_API_KEY"] = "test-key-for-testing"
    os.environ["LOG_LEVEL"] = "ERROR"  # Reduce log noise in tests
    reset_settings()


@pytest.fixture
def sample_crew_member() -> CrewMember:
    """Create a sample crew member for testing."""
    return CrewMember(
        id="crew-test-001",
        name="Test User",
        employee_id="EMP-TEST-001",
        department="Engineering",
        position="Engineer",
        hourly_rate=Decimal("75.00"),
        email="test@example.com",
    )


@pytest.fixture
def sample_pay_record(sample_crew_member: CrewMember) -> PayRecord:
    """Create a sample pay record for testing."""
    return PayRecord(
        id="pay-test-001",
        crew_member=sample_crew_member,
        pay_period_start=date(2024, 1, 1),
        pay_period_end=date(2024, 1, 15),
        pay_period_type=PayPeriodType.BI_WEEKLY,
        regular_hours=Decimal("80.0"),
        overtime_hours=Decimal("5.0"),
        gross_pay=Decimal("6375.00"),
        deductions=Decimal("1275.00"),
        net_pay=Decimal("5100.00"),
    )


@pytest.fixture
def sample_claim(sample_crew_member: CrewMember) -> Claim:
    """Create a sample claim for testing."""
    return Claim(
        id="claim-test-001",
        crew_member=sample_crew_member,
        claim_type=ClaimType.OVERTIME,
        amount=Decimal("500.00"),
        description="Overtime work on weekend deployment",
        supporting_documents=["timesheet.pdf", "approval.pdf"],
    )
