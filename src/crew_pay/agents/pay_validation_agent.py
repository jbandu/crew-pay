"""
Agent for validating crew pay records.
"""

from datetime import datetime
from decimal import Decimal

from langchain_core.messages import SystemMessage

from crew_pay.agents.base_agent import BaseAgent
from crew_pay.config.settings import get_settings
from crew_pay.models.schemas import ValidationReport, ValidationResult, ValidationStatus
from crew_pay.models.state import AgentInput, AgentOutput
from crew_pay.utils.exceptions import ValidationError


class PayValidationAgent(BaseAgent):
    """
    Agent responsible for validating crew pay records.

    Performs various validation checks including:
    - Hours validation (regular and overtime)
    - Pay calculation accuracy
    - Compliance with pay period rules
    - Data completeness and consistency
    """

    def __init__(self) -> None:
        """Initialize the pay validation agent."""
        super().__init__(
            name="PayValidationAgent",
            description="Validates crew pay records for accuracy and compliance",
        )
        self.settings = get_settings()

    async def process(self, agent_input: AgentInput) -> AgentOutput:
        """
        Validate a pay record.

        Args:
            agent_input: Input containing pay record to validate

        Returns:
            AgentOutput: Validation results
        """
        self.log_start({"pay_record_id": agent_input.pay_record.id if agent_input.pay_record else None})

        if not agent_input.pay_record:
            raise ValidationError("No pay record provided for validation")

        pay_record = agent_input.pay_record

        # Perform validation checks
        validation_results = []

        # 1. Hours limit check
        validation_results.append(self._validate_hours(pay_record))

        # 2. Pay calculation check
        validation_results.append(self._validate_pay_calculation(pay_record))

        # 3. Pay period consistency
        validation_results.append(self._validate_pay_period(pay_record))

        # 4. Data completeness
        validation_results.append(self._validate_data_completeness(pay_record))

        # 5. LLM-based semantic validation
        llm_validation = await self._validate_with_llm(pay_record)
        validation_results.append(llm_validation)

        # Determine overall status
        overall_status = self._determine_overall_status(validation_results)

        # Create validation report
        validation_report = ValidationReport(
            pay_record_id=pay_record.id,
            overall_status=overall_status,
            validation_results=validation_results,
            summary=self._create_summary(validation_results, overall_status),
        )

        # Create response message
        message = self.create_message(
            f"Completed validation for pay record {pay_record.id}. "
            f"Status: {overall_status.value}. "
            f"Passed: {sum(1 for r in validation_results if r.status == ValidationStatus.PASSED)}/{len(validation_results)} checks."
        )

        result = {
            "validation_report": validation_report,
            "pay_record_id": pay_record.id,
            "overall_status": overall_status.value,
        }

        self.log_end(result)

        return AgentOutput(
            messages=[message],
            result=result,
            next_agent="ComplianceAgent" if overall_status != ValidationStatus.FAILED else None,
            should_continue=overall_status != ValidationStatus.FAILED,
            metadata={"validation_report": validation_report.model_dump()},
        )

    def _validate_hours(self, pay_record: Any) -> ValidationResult:
        """Validate hours worked."""
        total_hours = pay_record.regular_hours + pay_record.overtime_hours
        max_total_hours = (
            self.settings.max_regular_hours_per_week + self.settings.max_overtime_hours_per_week
        ) * 2  # Assuming bi-weekly

        if total_hours > max_total_hours:
            return ValidationResult(
                check_name="hours_limit_check",
                status=ValidationStatus.FAILED,
                message=f"Total hours ({total_hours}) exceeds maximum allowed ({max_total_hours})",
                details={
                    "total_hours": float(total_hours),
                    "max_hours": max_total_hours,
                    "regular_hours": float(pay_record.regular_hours),
                    "overtime_hours": float(pay_record.overtime_hours),
                },
            )

        if total_hours > max_total_hours * 0.9:
            return ValidationResult(
                check_name="hours_limit_check",
                status=ValidationStatus.WARNING,
                message=f"Total hours ({total_hours}) approaching maximum limit",
                details={
                    "total_hours": float(total_hours),
                    "max_hours": max_total_hours,
                },
            )

        return ValidationResult(
            check_name="hours_limit_check",
            status=ValidationStatus.PASSED,
            message="Hours within acceptable limits",
            details={"total_hours": float(total_hours)},
        )

    def _validate_pay_calculation(self, pay_record: Any) -> ValidationResult:
        """Validate pay calculations."""
        # Calculate expected gross pay
        regular_pay = pay_record.regular_hours * pay_record.crew_member.hourly_rate
        overtime_rate = pay_record.crew_member.hourly_rate * Decimal("1.5")
        overtime_pay = pay_record.overtime_hours * overtime_rate
        expected_gross = regular_pay + overtime_pay

        # Allow for small rounding differences
        difference = abs(pay_record.gross_pay - expected_gross)
        tolerance = Decimal("0.01")

        if difference > tolerance:
            return ValidationResult(
                check_name="pay_calculation_check",
                status=ValidationStatus.FAILED,
                message=f"Pay calculation mismatch. Expected: ${expected_gross}, Got: ${pay_record.gross_pay}",
                details={
                    "expected_gross_pay": float(expected_gross),
                    "actual_gross_pay": float(pay_record.gross_pay),
                    "difference": float(difference),
                },
            )

        # Validate net pay
        expected_net = pay_record.gross_pay - pay_record.deductions
        if abs(pay_record.net_pay - expected_net) > tolerance:
            return ValidationResult(
                check_name="pay_calculation_check",
                status=ValidationStatus.FAILED,
                message="Net pay calculation mismatch",
                details={
                    "expected_net_pay": float(expected_net),
                    "actual_net_pay": float(pay_record.net_pay),
                },
            )

        return ValidationResult(
            check_name="pay_calculation_check",
            status=ValidationStatus.PASSED,
            message="Pay calculations are accurate",
            details={
                "gross_pay": float(pay_record.gross_pay),
                "net_pay": float(pay_record.net_pay),
            },
        )

    def _validate_pay_period(self, pay_record: Any) -> ValidationResult:
        """Validate pay period consistency."""
        if pay_record.pay_period_end <= pay_record.pay_period_start:
            return ValidationResult(
                check_name="pay_period_check",
                status=ValidationStatus.FAILED,
                message="Pay period end date must be after start date",
                details={
                    "start_date": pay_record.pay_period_start.isoformat(),
                    "end_date": pay_record.pay_period_end.isoformat(),
                },
            )

        # Check if pay period length matches type
        days_diff = (pay_record.pay_period_end - pay_record.pay_period_start).days
        expected_days = {
            "weekly": 7,
            "bi_weekly": 14,
            "semi_monthly": 15,
            "monthly": 30,
        }

        expected = expected_days.get(pay_record.pay_period_type.value, 14)
        if abs(days_diff - expected) > 2:  # Allow 2 days tolerance
            return ValidationResult(
                check_name="pay_period_check",
                status=ValidationStatus.WARNING,
                message=f"Pay period length ({days_diff} days) doesn't match type ({pay_record.pay_period_type.value})",
                details={
                    "actual_days": days_diff,
                    "expected_days": expected,
                    "pay_period_type": pay_record.pay_period_type.value,
                },
            )

        return ValidationResult(
            check_name="pay_period_check",
            status=ValidationStatus.PASSED,
            message="Pay period is valid",
            details={"days": days_diff},
        )

    def _validate_data_completeness(self, pay_record: Any) -> ValidationResult:
        """Validate data completeness."""
        missing_fields = []

        if not pay_record.crew_member.name:
            missing_fields.append("crew_member.name")
        if not pay_record.crew_member.employee_id:
            missing_fields.append("crew_member.employee_id")
        if pay_record.regular_hours < 0:
            missing_fields.append("regular_hours (invalid)")
        if pay_record.gross_pay <= 0:
            missing_fields.append("gross_pay (invalid)")

        if missing_fields:
            return ValidationResult(
                check_name="data_completeness_check",
                status=ValidationStatus.FAILED,
                message=f"Missing or invalid required fields: {', '.join(missing_fields)}",
                details={"missing_fields": missing_fields},
            )

        return ValidationResult(
            check_name="data_completeness_check",
            status=ValidationStatus.PASSED,
            message="All required data is present",
            details={},
        )

    async def _validate_with_llm(self, pay_record: Any) -> ValidationResult:
        """Use LLM for semantic validation."""
        try:
            system_prompt = SystemMessage(
                content="""You are a payroll validation expert. Review the following pay record and identify any anomalies,
                inconsistencies, or concerns. Consider industry standards and best practices.

                Respond with a JSON object containing:
                {
                    "status": "passed" | "warning" | "failed",
                    "message": "Brief explanation",
                    "concerns": ["list", "of", "any", "concerns"]
                }"""
            )

            pay_data = f"""
            Employee: {pay_record.crew_member.name} ({pay_record.crew_member.employee_id})
            Position: {pay_record.crew_member.position}
            Department: {pay_record.crew_member.department}
            Hourly Rate: ${pay_record.crew_member.hourly_rate}

            Pay Period: {pay_record.pay_period_start} to {pay_record.pay_period_end}
            Regular Hours: {pay_record.regular_hours}
            Overtime Hours: {pay_record.overtime_hours}

            Gross Pay: ${pay_record.gross_pay}
            Deductions: ${pay_record.deductions}
            Net Pay: ${pay_record.net_pay}
            """

            response = await self.llm.ainvoke([system_prompt, self.create_message(pay_data, is_ai=False)])

            # Parse response (simplified - in production would use structured output)
            content = response.content.lower()
            if "failed" in content or "reject" in content:
                status = ValidationStatus.FAILED
            elif "warning" in content or "concern" in content:
                status = ValidationStatus.WARNING
            else:
                status = ValidationStatus.PASSED

            return ValidationResult(
                check_name="llm_semantic_check",
                status=status,
                message=f"LLM validation: {response.content[:200]}",
                details={"llm_response": str(response.content)},
            )

        except Exception as e:
            self.logger.warning("LLM validation failed", error=str(e))
            return ValidationResult(
                check_name="llm_semantic_check",
                status=ValidationStatus.WARNING,
                message=f"LLM validation skipped due to error: {str(e)}",
                details={"error": str(e)},
            )

    def _determine_overall_status(self, results: list[ValidationResult]) -> ValidationStatus:
        """Determine overall validation status."""
        if any(r.status == ValidationStatus.FAILED for r in results):
            return ValidationStatus.FAILED
        if any(r.status == ValidationStatus.REQUIRES_REVIEW for r in results):
            return ValidationStatus.REQUIRES_REVIEW
        if any(r.status == ValidationStatus.WARNING for r in results):
            return ValidationStatus.WARNING
        return ValidationStatus.PASSED

    def _create_summary(self, results: list[ValidationResult], overall_status: ValidationStatus) -> str:
        """Create validation summary."""
        passed = sum(1 for r in results if r.status == ValidationStatus.PASSED)
        warnings = sum(1 for r in results if r.status == ValidationStatus.WARNING)
        failed = sum(1 for r in results if r.status == ValidationStatus.FAILED)

        summary = f"Validation completed with status: {overall_status.value}. "
        summary += f"Checks: {passed} passed, {warnings} warnings, {failed} failed."

        if failed > 0:
            failed_checks = [r.check_name for r in results if r.status == ValidationStatus.FAILED]
            summary += f" Failed checks: {', '.join(failed_checks)}"

        return summary
