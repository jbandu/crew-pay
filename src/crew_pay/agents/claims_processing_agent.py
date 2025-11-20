"""
Agent for processing crew pay claims.
"""

from datetime import datetime
from decimal import Decimal

from langchain_core.messages import SystemMessage

from crew_pay.agents.base_agent import BaseAgent
from crew_pay.config.settings import get_settings
from crew_pay.models.schemas import ClaimDecision, ClaimStatus
from crew_pay.models.state import AgentInput, AgentOutput
from crew_pay.utils.exceptions import ValidationError


class ClaimsProcessingAgent(BaseAgent):
    """
    Agent responsible for processing crew pay claims.

    Handles:
    - Claim validation and verification
    - Supporting document review
    - Claim amount assessment
    - Approval/rejection decisions
    - Next steps determination
    """

    def __init__(self) -> None:
        """Initialize the claims processing agent."""
        super().__init__(
            name="ClaimsProcessingAgent",
            description="Processes and evaluates crew pay claims",
        )
        self.settings = get_settings()

    async def process(self, agent_input: AgentInput) -> AgentOutput:
        """
        Process a claim.

        Args:
            agent_input: Input containing claim to process

        Returns:
            AgentOutput: Processing decision and next steps
        """
        self.log_start({"claim_id": agent_input.claim.id if agent_input.claim else None})

        if not agent_input.claim:
            raise ValidationError("No claim provided for processing")

        claim = agent_input.claim

        # Perform basic validation
        validation_result = self._validate_claim(claim)
        if not validation_result["is_valid"]:
            decision = ClaimDecision(
                claim_id=claim.id,
                decision=ClaimStatus.REJECTED,
                approved_amount=Decimal("0"),
                rationale=validation_result["message"],
                reviewer=self.name,
                next_steps=["Notify crew member of rejection", "Request additional information"],
            )

            message = self.create_message(
                f"Claim {claim.id} rejected: {validation_result['message']}"
            )

            result = {
                "claim_decision": decision,
                "claim_id": claim.id,
                "decision": ClaimStatus.REJECTED.value,
            }

            self.log_end(result)

            return AgentOutput(
                messages=[message],
                result=result,
                next_agent="NotificationAgent",
                should_continue=True,
                metadata={"claim_decision": decision.model_dump()},
            )

        # Check auto-approval threshold
        if self.settings.auto_approve_claim_threshold and claim.amount <= Decimal(
            str(self.settings.auto_approve_claim_threshold)
        ):
            decision = await self._auto_approve_claim(claim)
        else:
            decision = await self._evaluate_claim_with_llm(claim)

        # Update next steps based on decision
        next_agent = self._determine_next_agent(decision)

        message = self.create_message(
            f"Claim {claim.id} processed. Decision: {decision.decision.value}. "
            f"Approved amount: ${decision.approved_amount}"
        )

        result = {
            "claim_decision": decision,
            "claim_id": claim.id,
            "decision": decision.decision.value,
            "approved_amount": float(decision.approved_amount),
        }

        self.log_end(result)

        return AgentOutput(
            messages=[message],
            result=result,
            next_agent=next_agent,
            should_continue=True,
            metadata={"claim_decision": decision.model_dump()},
        )

    def _validate_claim(self, claim: Any) -> dict[str, Any]:
        """Validate claim data."""
        # Check required fields
        if not claim.description or len(claim.description.strip()) < 10:
            return {
                "is_valid": False,
                "message": "Claim description is too short or missing",
            }

        if claim.amount <= 0:
            return {
                "is_valid": False,
                "message": "Claim amount must be greater than zero",
            }

        # Check claim type specific rules
        if claim.claim_type.value == "overtime":
            if not self._validate_overtime_claim(claim):
                return {
                    "is_valid": False,
                    "message": "Overtime claim validation failed - missing timesheet documentation",
                }

        if claim.claim_type.value == "reimbursement":
            if not claim.supporting_documents:
                return {
                    "is_valid": False,
                    "message": "Reimbursement claims require supporting documents",
                }

        return {"is_valid": True, "message": "Claim validation passed"}

    def _validate_overtime_claim(self, claim: Any) -> bool:
        """Validate overtime-specific requirements."""
        # Check for timesheet or similar documentation
        required_docs = ["timesheet", "time", "hours", "schedule"]
        has_required_doc = any(
            any(keyword in doc.lower() for keyword in required_docs)
            for doc in claim.supporting_documents
        )
        return has_required_doc or len(claim.supporting_documents) > 0

    async def _auto_approve_claim(self, claim: Any) -> ClaimDecision:
        """Auto-approve small claims."""
        self.logger.info(
            "auto_approving_claim",
            claim_id=claim.id,
            amount=float(claim.amount),
            threshold=self.settings.auto_approve_claim_threshold,
        )

        return ClaimDecision(
            claim_id=claim.id,
            decision=ClaimStatus.APPROVED,
            approved_amount=claim.amount,
            rationale=f"Auto-approved: claim amount (${claim.amount}) below threshold",
            reviewer=self.name,
            next_steps=[
                "Process payment",
                "Update payroll system",
                "Notify crew member of approval",
            ],
        )

    async def _evaluate_claim_with_llm(self, claim: Any) -> ClaimDecision:
        """Evaluate claim using LLM."""
        try:
            system_prompt = SystemMessage(
                content="""You are a claims processing expert. Evaluate the following claim and provide a decision.

                Consider:
                - Claim type and amount
                - Supporting documentation
                - Description clarity and completeness
                - Company policies and industry standards
                - Reasonableness of the request

                Respond with a JSON object containing:
                {
                    "decision": "approved" | "rejected" | "under_review",
                    "approved_amount": <number>,
                    "rationale": "Detailed explanation for decision",
                    "concerns": ["list of any concerns"],
                    "next_steps": ["list of recommended next steps"]
                }"""
            )

            claim_data = f"""
            Claim ID: {claim.id}
            Crew Member: {claim.crew_member.name} ({claim.crew_member.employee_id})
            Position: {claim.crew_member.position}
            Department: {claim.crew_member.department}

            Claim Type: {claim.claim_type.value}
            Requested Amount: ${claim.amount}
            Description: {claim.description}

            Supporting Documents: {', '.join(claim.supporting_documents) if claim.supporting_documents else 'None'}
            Submitted Date: {claim.submitted_date}
            """

            response = await self.llm.ainvoke([system_prompt, self.create_message(claim_data, is_ai=False)])

            # Parse LLM response (simplified - in production use structured output)
            content = response.content.lower()

            # Determine decision
            if "approved" in content and "rejected" not in content:
                decision = ClaimStatus.APPROVED
                approved_amount = claim.amount
                rationale = f"Approved based on LLM evaluation. {response.content[:300]}"
                next_steps = [
                    "Process payment",
                    "Update payroll system",
                    "Notify crew member of approval",
                ]
            elif "rejected" in content or "deny" in content:
                decision = ClaimStatus.REJECTED
                approved_amount = Decimal("0")
                rationale = f"Rejected based on LLM evaluation. {response.content[:300]}"
                next_steps = [
                    "Notify crew member of rejection",
                    "Provide feedback for resubmission",
                ]
            else:
                decision = ClaimStatus.UNDER_REVIEW
                approved_amount = Decimal("0")
                rationale = f"Requires additional review. {response.content[:300]}"
                next_steps = [
                    "Request additional documentation",
                    "Escalate to manager for review",
                    "Schedule review meeting",
                ]

            return ClaimDecision(
                claim_id=claim.id,
                decision=decision,
                approved_amount=approved_amount,
                rationale=rationale,
                reviewer=self.name,
                next_steps=next_steps,
            )

        except Exception as e:
            self.logger.error("llm_evaluation_failed", error=str(e))

            # Fallback decision
            return ClaimDecision(
                claim_id=claim.id,
                decision=ClaimStatus.UNDER_REVIEW,
                approved_amount=Decimal("0"),
                rationale=f"Automatic evaluation unavailable. Manual review required. Error: {str(e)}",
                reviewer=self.name,
                next_steps=[
                    "Manual review required",
                    "Escalate to human reviewer",
                ],
            )

    def _determine_next_agent(self, decision: ClaimDecision) -> str:
        """Determine the next agent in the workflow."""
        if decision.decision == ClaimStatus.APPROVED:
            if self.settings.enable_compliance_checks:
                return "ComplianceAgent"
            else:
                return "NotificationAgent"
        elif decision.decision == ClaimStatus.REJECTED:
            return "NotificationAgent"
        else:  # UNDER_REVIEW
            # In production, might route to human review system
            return "NotificationAgent"
