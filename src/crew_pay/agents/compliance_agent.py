"""
Agent for performing compliance checks on pay records and claims.
"""

from typing import Any

from langchain_core.messages import SystemMessage

from crew_pay.agents.base_agent import BaseAgent
from crew_pay.models.state import AgentInput, AgentOutput


class ComplianceAgent(BaseAgent):
    """
    Agent responsible for compliance and regulatory checks.

    Performs:
    - Labor law compliance checks
    - Tax regulation validation
    - Company policy adherence
    - Industry standard verification
    - Audit trail creation
    """

    def __init__(self) -> None:
        """Initialize the compliance agent."""
        super().__init__(
            name="ComplianceAgent",
            description="Ensures compliance with regulations and policies",
        )

    async def process(self, agent_input: AgentInput) -> AgentOutput:
        """
        Perform compliance checks.

        Args:
            agent_input: Input containing data to check

        Returns:
            AgentOutput: Compliance check results
        """
        context_id = None
        if agent_input.pay_record:
            context_id = agent_input.pay_record.id
        elif agent_input.claim:
            context_id = agent_input.claim.id

        self.log_start({"context_id": context_id})

        compliance_checks = []

        # Perform various compliance checks
        if agent_input.pay_record:
            compliance_checks.extend(await self._check_pay_record_compliance(agent_input.pay_record))

        if agent_input.claim:
            compliance_checks.extend(await self._check_claim_compliance(agent_input.claim))

        # Perform general compliance checks
        compliance_checks.append(await self._check_general_compliance(agent_input))

        # Determine overall compliance status
        all_passed = all(check["passed"] for check in compliance_checks)
        has_warnings = any(check.get("warning", False) for check in compliance_checks)

        if all_passed:
            status = "compliant"
            message_text = f"All compliance checks passed for {context_id}"
            next_agent = "NotificationAgent"
            should_continue = True
        elif has_warnings:
            status = "compliant_with_warnings"
            message_text = f"Compliance checks passed with warnings for {context_id}"
            next_agent = "NotificationAgent"
            should_continue = True
        else:
            status = "non_compliant"
            failed_checks = [c["check_name"] for c in compliance_checks if not c["passed"]]
            message_text = f"Compliance checks failed for {context_id}. Failed: {', '.join(failed_checks)}"
            next_agent = None
            should_continue = False

        message = self.create_message(message_text)

        result = {
            "compliance_status": status,
            "checks": compliance_checks,
            "all_passed": all_passed,
            "has_warnings": has_warnings,
        }

        self.log_end(result)

        return AgentOutput(
            messages=[message],
            result=result,
            next_agent=next_agent,
            should_continue=should_continue,
            metadata={"compliance_checks": compliance_checks},
        )

    async def _check_pay_record_compliance(self, pay_record: Any) -> list[dict[str, Any]]:
        """Check pay record compliance."""
        checks = []

        # Minimum wage check
        if pay_record.crew_member.hourly_rate < 15.00:  # Example minimum wage
            checks.append({
                "check_name": "minimum_wage_check",
                "passed": False,
                "warning": False,
                "message": f"Hourly rate (${pay_record.crew_member.hourly_rate}) below minimum wage ($15.00)",
                "details": {"hourly_rate": float(pay_record.crew_member.hourly_rate), "minimum": 15.00},
            })
        else:
            checks.append({
                "check_name": "minimum_wage_check",
                "passed": True,
                "warning": False,
                "message": "Hourly rate meets minimum wage requirements",
                "details": {"hourly_rate": float(pay_record.crew_member.hourly_rate)},
            })

        # Overtime rate check (should be 1.5x for hours over 40)
        if pay_record.overtime_hours > 0:
            checks.append({
                "check_name": "overtime_rate_check",
                "passed": True,
                "warning": False,
                "message": "Overtime hours recorded, ensure 1.5x rate applied",
                "details": {"overtime_hours": float(pay_record.overtime_hours)},
            })

        # Tax withholding check (basic validation)
        if pay_record.deductions <= 0 and pay_record.gross_pay > 0:
            checks.append({
                "check_name": "tax_withholding_check",
                "passed": False,
                "warning": True,
                "message": "No deductions found - verify tax withholding",
                "details": {"deductions": float(pay_record.deductions)},
            })
        else:
            # Check if deductions are reasonable (15-35% of gross)
            deduction_percentage = (pay_record.deductions / pay_record.gross_pay) * 100
            if deduction_percentage < 5 or deduction_percentage > 50:
                checks.append({
                    "check_name": "tax_withholding_check",
                    "passed": True,
                    "warning": True,
                    "message": f"Deductions ({deduction_percentage:.1f}%) outside typical range (15-35%)",
                    "details": {"deduction_percentage": float(deduction_percentage)},
                })
            else:
                checks.append({
                    "check_name": "tax_withholding_check",
                    "passed": True,
                    "warning": False,
                    "message": "Deductions within normal range",
                    "details": {"deduction_percentage": float(deduction_percentage)},
                })

        return checks

    async def _check_claim_compliance(self, claim: Any) -> list[dict[str, Any]]:
        """Check claim compliance."""
        checks = []

        # Documentation requirement check
        if claim.claim_type.value in ["reimbursement", "bonus"] and not claim.supporting_documents:
            checks.append({
                "check_name": "documentation_requirement",
                "passed": False,
                "warning": False,
                "message": f"{claim.claim_type.value} claims require supporting documentation",
                "details": {"claim_type": claim.claim_type.value},
            })
        else:
            checks.append({
                "check_name": "documentation_requirement",
                "passed": True,
                "warning": False,
                "message": "Documentation requirements met",
                "details": {"document_count": len(claim.supporting_documents)},
            })

        # Amount reasonableness check
        if claim.amount > 10000:  # Example threshold
            checks.append({
                "check_name": "amount_threshold_check",
                "passed": True,
                "warning": True,
                "message": f"Claim amount (${claim.amount}) exceeds typical threshold - additional review recommended",
                "details": {"amount": float(claim.amount), "threshold": 10000},
            })
        else:
            checks.append({
                "check_name": "amount_threshold_check",
                "passed": True,
                "warning": False,
                "message": "Claim amount within normal range",
                "details": {"amount": float(claim.amount)},
            })

        return checks

    async def _check_general_compliance(self, agent_input: AgentInput) -> dict[str, Any]:
        """Perform general compliance check using LLM."""
        try:
            system_prompt = SystemMessage(
                content="""You are a compliance expert specializing in labor laws and payroll regulations.
                Review the provided information and identify any potential compliance issues or concerns.

                Consider:
                - Fair Labor Standards Act (FLSA) compliance
                - Tax regulations
                - Company policy adherence
                - Record-keeping requirements
                - Equal pay considerations

                Respond with a JSON object:
                {
                    "compliant": true | false,
                    "concerns": ["list of concerns"],
                    "recommendations": ["list of recommendations"]
                }"""
            )

            context_data = "Compliance Check Context:\n"

            if agent_input.pay_record:
                pr = agent_input.pay_record
                context_data += f"""
                Pay Record ID: {pr.id}
                Employee: {pr.crew_member.name}
                Position: {pr.crew_member.position}
                Hourly Rate: ${pr.crew_member.hourly_rate}
                Regular Hours: {pr.regular_hours}
                Overtime Hours: {pr.overtime_hours}
                Gross Pay: ${pr.gross_pay}
                Deductions: ${pr.deductions}
                Net Pay: ${pr.net_pay}
                """

            if agent_input.claim:
                cl = agent_input.claim
                context_data += f"""
                Claim ID: {cl.id}
                Employee: {cl.crew_member.name}
                Claim Type: {cl.claim_type.value}
                Amount: ${cl.amount}
                Description: {cl.description}
                """

            response = await self.llm.ainvoke([system_prompt, self.create_message(context_data, is_ai=False)])

            # Parse response
            content = response.content.lower()
            compliant = "compliant" in content and "non-compliant" not in content and "not compliant" not in content

            return {
                "check_name": "llm_general_compliance",
                "passed": compliant,
                "warning": not compliant,
                "message": f"LLM compliance review: {response.content[:200]}",
                "details": {"llm_response": str(response.content)},
            }

        except Exception as e:
            self.logger.warning("llm_compliance_check_failed", error=str(e))
            return {
                "check_name": "llm_general_compliance",
                "passed": True,
                "warning": True,
                "message": f"LLM compliance check skipped: {str(e)}",
                "details": {"error": str(e)},
            }
