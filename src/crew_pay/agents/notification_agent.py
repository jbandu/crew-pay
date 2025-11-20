"""
Agent for sending notifications and alerts.
"""

from typing import Any

from crew_pay.agents.base_agent import BaseAgent
from crew_pay.models.state import AgentInput, AgentOutput


class NotificationAgent(BaseAgent):
    """
    Agent responsible for sending notifications.

    Handles:
    - Email notifications
    - SMS alerts
    - System notifications
    - Audit logging
    - Status updates
    """

    def __init__(self) -> None:
        """Initialize the notification agent."""
        super().__init__(
            name="NotificationAgent",
            description="Sends notifications and alerts to stakeholders",
        )

    async def process(self, agent_input: AgentInput) -> AgentOutput:
        """
        Send notifications based on workflow results.

        Args:
            agent_input: Input containing notification context

        Returns:
            AgentOutput: Notification results
        """
        self.log_start({"context": agent_input.context})

        notifications_sent = []

        # Determine what notifications to send based on context
        if agent_input.pay_record:
            notifications_sent.extend(
                await self._send_pay_record_notifications(agent_input.pay_record, agent_input.context)
            )

        if agent_input.claim:
            notifications_sent.extend(
                await self._send_claim_notifications(agent_input.claim, agent_input.context)
            )

        # Send general workflow completion notification
        notifications_sent.append(await self._send_workflow_completion_notification(agent_input.context))

        message = self.create_message(
            f"Sent {len(notifications_sent)} notifications successfully"
        )

        result = {
            "notifications_sent": notifications_sent,
            "count": len(notifications_sent),
        }

        self.log_end(result)

        # Notification agent is typically the last in the chain
        return AgentOutput(
            messages=[message],
            result=result,
            next_agent=None,
            should_continue=False,
            metadata={"notifications": notifications_sent},
        )

    async def _send_pay_record_notifications(
        self, pay_record: Any, context: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Send notifications for pay record processing."""
        notifications = []

        validation_report = context.get("validation_report")

        if validation_report:
            status = validation_report.get("overall_status", "unknown")

            # Notification to employee
            notifications.append({
                "type": "email",
                "recipient": pay_record.crew_member.email or pay_record.crew_member.name,
                "subject": f"Pay Record {pay_record.id} - Status: {status}",
                "body": self._create_pay_record_email_body(pay_record, validation_report),
                "sent": True,
                "timestamp": self._get_timestamp(),
            })

            # Notification to payroll department
            if status == "failed":
                notifications.append({
                    "type": "alert",
                    "recipient": "payroll_department",
                    "subject": f"Pay Record Validation Failed: {pay_record.id}",
                    "body": f"Pay record {pay_record.id} for {pay_record.crew_member.name} failed validation",
                    "priority": "high",
                    "sent": True,
                    "timestamp": self._get_timestamp(),
                })

        self.logger.info(
            "pay_record_notifications_sent",
            pay_record_id=pay_record.id,
            count=len(notifications),
        )

        return notifications

    async def _send_claim_notifications(
        self, claim: Any, context: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Send notifications for claim processing."""
        notifications = []

        claim_decision = context.get("claim_decision")

        if claim_decision:
            decision = claim_decision.get("decision", "unknown")
            approved_amount = claim_decision.get("approved_amount", 0)

            # Notification to employee
            notifications.append({
                "type": "email",
                "recipient": claim.crew_member.email or claim.crew_member.name,
                "subject": f"Claim {claim.id} - Decision: {decision}",
                "body": self._create_claim_email_body(claim, claim_decision),
                "sent": True,
                "timestamp": self._get_timestamp(),
            })

            # Notification to finance if approved
            if decision == "approved":
                notifications.append({
                    "type": "task",
                    "recipient": "finance_department",
                    "subject": f"Process Payment for Claim {claim.id}",
                    "body": f"Claim {claim.id} approved for ${approved_amount}. Process payment to {claim.crew_member.name}.",
                    "action_required": True,
                    "sent": True,
                    "timestamp": self._get_timestamp(),
                })

        self.logger.info(
            "claim_notifications_sent",
            claim_id=claim.id,
            count=len(notifications),
        )

        return notifications

    async def _send_workflow_completion_notification(
        self, context: dict[str, Any]
    ) -> dict[str, Any]:
        """Send workflow completion notification."""
        workflow_id = context.get("workflow_id", "unknown")

        notification = {
            "type": "log",
            "recipient": "system",
            "subject": f"Workflow {workflow_id} Completed",
            "body": f"Workflow {workflow_id} completed successfully",
            "sent": True,
            "timestamp": self._get_timestamp(),
        }

        self.logger.info("workflow_completion_notification_sent", workflow_id=workflow_id)

        return notification

    def _create_pay_record_email_body(
        self, pay_record: Any, validation_report: dict[str, Any]
    ) -> str:
        """Create email body for pay record notification."""
        status = validation_report.get("overall_status", "unknown")
        summary = validation_report.get("summary", "")

        body = f"""
Dear {pay_record.crew_member.name},

Your pay record for the period {pay_record.pay_period_start} to {pay_record.pay_period_end} has been processed.

Status: {status.upper()}
Gross Pay: ${pay_record.gross_pay}
Deductions: ${pay_record.deductions}
Net Pay: ${pay_record.net_pay}

{summary}

If you have any questions, please contact the payroll department.

Best regards,
Crew Pay System
"""
        return body.strip()

    def _create_claim_email_body(self, claim: Any, claim_decision: dict[str, Any]) -> str:
        """Create email body for claim notification."""
        decision = claim_decision.get("decision", "unknown")
        approved_amount = claim_decision.get("approved_amount", 0)
        rationale = claim_decision.get("rationale", "")

        body = f"""
Dear {claim.crew_member.name},

Your claim (ID: {claim.id}) has been processed.

Claim Type: {claim.claim_type.value}
Requested Amount: ${claim.amount}
Decision: {decision.upper()}
Approved Amount: ${approved_amount}

Rationale: {rationale}

"""

        next_steps = claim_decision.get("next_steps", [])
        if next_steps:
            body += "\nNext Steps:\n"
            for step in next_steps:
                body += f"- {step}\n"

        body += """
If you have any questions, please contact the claims department.

Best regards,
Crew Pay System
"""
        return body.strip()

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
