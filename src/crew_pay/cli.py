"""
Command-line interface for crew pay system.
"""

import asyncio
import json
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from crew_pay.config.settings import get_settings
from crew_pay.models.schemas import (
    Claim,
    ClaimType,
    CrewMember,
    PayPeriodType,
    PayRecord,
)
from crew_pay.orchestrator.workflow import CrewPayWorkflow
from crew_pay.utils.logging import configure_logging

app = typer.Typer(
    name="crew-pay",
    help="LangGraph-based multi-agent system for crew pay validation and claims processing",
)
console = Console()


@app.command()
def validate_pay(
    pay_record_file: Path = typer.Argument(..., help="Path to pay record JSON file"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file for results"),
) -> None:
    """Validate a pay record."""
    configure_logging()

    try:
        # Load pay record
        with open(pay_record_file) as f:
            data = json.load(f)

        # Parse dates
        data["pay_period_start"] = datetime.fromisoformat(data["pay_period_start"]).date()
        data["pay_period_end"] = datetime.fromisoformat(data["pay_period_end"]).date()

        # Convert to Decimal
        for field in ["hourly_rate", "regular_hours", "overtime_hours", "gross_pay", "deductions", "net_pay"]:
            if field in data.get("crew_member", {}):
                data["crew_member"][field] = Decimal(str(data["crew_member"][field]))
            if field in data:
                data[field] = Decimal(str(data[field]))

        pay_record = PayRecord(**data)

        console.print(f"[bold blue]Validating pay record: {pay_record.id}[/bold blue]")

        # Run validation workflow
        workflow = CrewPayWorkflow()
        result = asyncio.run(workflow.validate_pay_record(pay_record))

        # Display results
        _display_workflow_result(result)

        # Save results if output specified
        if output:
            with open(output, "w") as f:
                json.dump(result.model_dump(mode="json"), f, indent=2, default=str)
            console.print(f"\n[green]Results saved to {output}[/green]")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def process_claim(
    claim_file: Path = typer.Argument(..., help="Path to claim JSON file"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file for results"),
) -> None:
    """Process a claim."""
    configure_logging()

    try:
        # Load claim
        with open(claim_file) as f:
            data = json.load(f)

        # Convert to Decimal
        if "amount" in data:
            data["amount"] = Decimal(str(data["amount"]))
        if "approved_amount" in data and data["approved_amount"]:
            data["approved_amount"] = Decimal(str(data["approved_amount"]))

        # Convert crew member fields
        if "crew_member" in data and "hourly_rate" in data["crew_member"]:
            data["crew_member"]["hourly_rate"] = Decimal(str(data["crew_member"]["hourly_rate"]))

        claim = Claim(**data)

        console.print(f"[bold blue]Processing claim: {claim.id}[/bold blue]")

        # Run claims processing workflow
        workflow = CrewPayWorkflow()
        result = asyncio.run(workflow.process_claim(claim))

        # Display results
        _display_workflow_result(result)

        # Save results if output specified
        if output:
            with open(output, "w") as f:
                json.dump(result.model_dump(mode="json"), f, indent=2, default=str)
            console.print(f"\n[green]Results saved to {output}[/green]")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def info() -> None:
    """Display system information."""
    configure_logging()
    settings = get_settings()

    table = Table(title="Crew Pay System Information")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("OpenAI Model", settings.openai_model)
    table.add_row("Temperature", str(settings.temperature))
    table.add_row("Max Iterations", str(settings.max_iterations))
    table.add_row("Timeout", f"{settings.timeout_seconds}s")
    table.add_row("Human in Loop", str(settings.enable_human_in_loop))
    table.add_row("Notifications", str(settings.enable_notifications))
    table.add_row("Compliance Checks", str(settings.enable_compliance_checks))

    console.print(table)


def _display_workflow_result(result: Any) -> None:
    """Display workflow result."""
    # Status
    status_color = "green" if result.status == "completed" else "red"
    console.print(f"\n[bold {status_color}]Status: {result.status.upper()}[/bold {status_color}]")

    # Timing
    console.print(f"Duration: {result.duration_seconds:.2f}s")

    # Validation report
    if result.validation_report:
        console.print("\n[bold]Validation Report:[/bold]")
        console.print(f"Overall Status: {result.validation_report.overall_status.value}")
        console.print(f"Summary: {result.validation_report.summary}")

        table = Table(title="Validation Checks")
        table.add_column("Check", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Message")

        for check in result.validation_report.validation_results:
            status_symbol = "✓" if check.status.value == "passed" else "✗"
            table.add_row(check.check_name, f"{status_symbol} {check.status.value}", check.message)

        console.print(table)

    # Claim decision
    if result.claim_decision:
        console.print("\n[bold]Claim Decision:[/bold]")
        console.print(f"Decision: {result.claim_decision.decision.value}")
        console.print(f"Approved Amount: ${result.claim_decision.approved_amount}")
        console.print(f"Rationale: {result.claim_decision.rationale}")

        if result.claim_decision.next_steps:
            console.print("\nNext Steps:")
            for step in result.claim_decision.next_steps:
                console.print(f"  • {step}")

    # Error message
    if result.error_message:
        console.print(f"\n[bold red]Error: {result.error_message}[/bold red]")


if __name__ == "__main__":
    app()
