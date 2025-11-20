"""
Example usage of the crew pay system.
"""

import asyncio
from datetime import date
from decimal import Decimal

from crew_pay.models.schemas import (
    Claim,
    ClaimType,
    CrewMember,
    PayPeriodType,
    PayRecord,
)
from crew_pay.orchestrator.workflow import CrewPayWorkflow
from crew_pay.utils.logging import configure_logging


async def validate_pay_record_example() -> None:
    """Example: Validate a pay record."""
    print("=" * 80)
    print("Example 1: Validate Pay Record")
    print("=" * 80)

    # Create a crew member
    crew_member = CrewMember(
        id="crew-001",
        name="John Doe",
        employee_id="EMP-12345",
        department="Engineering",
        position="Senior Engineer",
        hourly_rate=Decimal("75.50"),
        email="john.doe@example.com",
        phone="+1-555-0100",
    )

    # Create a pay record
    pay_record = PayRecord(
        id="pay-2024-001",
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

    # Create workflow and validate
    workflow = CrewPayWorkflow()
    result = await workflow.validate_pay_record(pay_record)

    # Print results
    print(f"\nWorkflow ID: {result.workflow_id}")
    print(f"Status: {result.status}")
    print(f"Duration: {result.duration_seconds:.2f}s")

    if result.validation_report:
        print(f"\nValidation Status: {result.validation_report.overall_status.value}")
        print(f"Summary: {result.validation_report.summary}")
        print(f"\nValidation Checks:")
        for check in result.validation_report.validation_results:
            print(f"  - {check.check_name}: {check.status.value}")
            print(f"    {check.message}")

    print("\n")


async def process_claim_example() -> None:
    """Example: Process a claim."""
    print("=" * 80)
    print("Example 2: Process Claim")
    print("=" * 80)

    # Create a crew member
    crew_member = CrewMember(
        id="crew-002",
        name="Jane Smith",
        employee_id="EMP-67890",
        department="Operations",
        position="Operations Manager",
        hourly_rate=Decimal("85.00"),
        email="jane.smith@example.com",
        phone="+1-555-0200",
    )

    # Create a claim
    claim = Claim(
        id="claim-2024-001",
        crew_member=crew_member,
        claim_type=ClaimType.OVERTIME,
        amount=Decimal("500.00"),
        description="Overtime work on emergency deployment over the weekend. "
        "Worked additional 10 hours on Saturday and Sunday to resolve critical production issues.",
        supporting_documents=["timesheet_weekend.pdf", "deployment_log.txt"],
    )

    # Create workflow and process claim
    workflow = CrewPayWorkflow()
    result = await workflow.process_claim(claim)

    # Print results
    print(f"\nWorkflow ID: {result.workflow_id}")
    print(f"Status: {result.status}")
    print(f"Duration: {result.duration_seconds:.2f}s")

    if result.claim_decision:
        print(f"\nClaim Decision: {result.claim_decision.decision.value}")
        print(f"Approved Amount: ${result.claim_decision.approved_amount}")
        print(f"Rationale: {result.claim_decision.rationale}")
        print(f"\nNext Steps:")
        for step in result.claim_decision.next_steps:
            print(f"  - {step}")

    print("\n")


async def main() -> None:
    """Run all examples."""
    # Configure logging
    configure_logging()

    # Run examples
    await validate_pay_record_example()
    await process_claim_example()


if __name__ == "__main__":
    asyncio.run(main())
