"""
LangGraph-based workflow orchestrator for crew pay processing.
"""

from datetime import datetime
from typing import Any, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph import END, StateGraph

from crew_pay.agents.claims_processing_agent import ClaimsProcessingAgent
from crew_pay.agents.compliance_agent import ComplianceAgent
from crew_pay.agents.notification_agent import NotificationAgent
from crew_pay.agents.pay_validation_agent import PayValidationAgent
from crew_pay.config.settings import get_settings
from crew_pay.models.state import AgentInput, WorkflowConfig, WorkflowResult, WorkflowState
from crew_pay.utils.exceptions import WorkflowError
from crew_pay.utils.helpers import calculate_duration, generate_id
from crew_pay.utils.logging import get_logger

logger = get_logger("orchestrator.workflow")


class CrewPayWorkflow:
    """
    LangGraph-based orchestrator for crew pay validation and claims processing.

    This class manages the multi-agent workflow using LangGraph's StateGraph.
    """

    def __init__(self, config: WorkflowConfig | None = None) -> None:
        """
        Initialize the workflow orchestrator.

        Args:
            config: Workflow configuration
        """
        self.config = config or WorkflowConfig()
        self.settings = get_settings()
        self.logger = logger

        # Initialize agents
        self.pay_validation_agent = PayValidationAgent()
        self.claims_processing_agent = ClaimsProcessingAgent()
        self.compliance_agent = ComplianceAgent()
        self.notification_agent = NotificationAgent()

        # Build the workflow graph
        self.graph = self._build_graph()

    def _build_graph(self) -> Any:
        """Build the LangGraph workflow."""
        # Create the state graph
        workflow = StateGraph(WorkflowState)

        # Add nodes for each agent
        workflow.add_node("pay_validation", self._run_pay_validation)
        workflow.add_node("claims_processing", self._run_claims_processing)
        workflow.add_node("compliance", self._run_compliance)
        workflow.add_node("notification", self._run_notification)

        # Define edges and routing
        workflow.add_conditional_edges(
            "pay_validation",
            self._route_from_pay_validation,
            {
                "compliance": "compliance",
                "notification": "notification",
                "end": END,
            },
        )

        workflow.add_conditional_edges(
            "claims_processing",
            self._route_from_claims_processing,
            {
                "compliance": "compliance",
                "notification": "notification",
                "end": END,
            },
        )

        workflow.add_conditional_edges(
            "compliance",
            self._route_from_compliance,
            {
                "notification": "notification",
                "end": END,
            },
        )

        workflow.add_edge("notification", END)

        # Set entry point based on workflow type
        # This will be determined dynamically when running

        return workflow.compile()

    async def _run_pay_validation(self, state: WorkflowState) -> WorkflowState:
        """Run pay validation agent."""
        self.logger.info("running_pay_validation", workflow_id=state["workflow_id"])

        agent_input = AgentInput(
            messages=list(state["messages"]),
            pay_record=state["pay_record"],
            context=state["metadata"],
        )

        output = await self.pay_validation_agent.process(agent_input)

        # Update state
        state["messages"] = list(state["messages"]) + output.messages
        state["current_agent"] = "pay_validation"
        state["next_agent"] = output.next_agent
        state["iteration_count"] += 1

        # Store validation report if present
        if "validation_report" in output.result:
            state["validation_report"] = output.result["validation_report"]
            state["metadata"]["validation_report"] = output.result

        if not output.should_continue:
            state["workflow_status"] = "failed"
            state["error_message"] = "Pay validation failed"

        return state

    async def _run_claims_processing(self, state: WorkflowState) -> WorkflowState:
        """Run claims processing agent."""
        self.logger.info("running_claims_processing", workflow_id=state["workflow_id"])

        agent_input = AgentInput(
            messages=list(state["messages"]),
            claim=state["claim"],
            context=state["metadata"],
        )

        output = await self.claims_processing_agent.process(agent_input)

        # Update state
        state["messages"] = list(state["messages"]) + output.messages
        state["current_agent"] = "claims_processing"
        state["next_agent"] = output.next_agent
        state["iteration_count"] += 1

        # Store claim decision if present
        if "claim_decision" in output.result:
            state["claim_decision"] = output.result["claim_decision"]
            state["metadata"]["claim_decision"] = output.result

        return state

    async def _run_compliance(self, state: WorkflowState) -> WorkflowState:
        """Run compliance agent."""
        self.logger.info("running_compliance", workflow_id=state["workflow_id"])

        agent_input = AgentInput(
            messages=list(state["messages"]),
            pay_record=state["pay_record"],
            claim=state["claim"],
            context=state["metadata"],
        )

        output = await self.compliance_agent.process(agent_input)

        # Update state
        state["messages"] = list(state["messages"]) + output.messages
        state["current_agent"] = "compliance"
        state["next_agent"] = output.next_agent
        state["iteration_count"] += 1

        # Store compliance results
        state["metadata"]["compliance"] = output.result

        if not output.should_continue:
            state["workflow_status"] = "failed"
            state["error_message"] = "Compliance check failed"

        return state

    async def _run_notification(self, state: WorkflowState) -> WorkflowState:
        """Run notification agent."""
        self.logger.info("running_notification", workflow_id=state["workflow_id"])

        agent_input = AgentInput(
            messages=list(state["messages"]),
            pay_record=state["pay_record"],
            claim=state["claim"],
            context=state["metadata"],
        )

        output = await self.notification_agent.process(agent_input)

        # Update state
        state["messages"] = list(state["messages"]) + output.messages
        state["current_agent"] = "notification"
        state["next_agent"] = None
        state["iteration_count"] += 1

        # Store notification results
        state["metadata"]["notifications"] = output.result

        # Mark workflow as completed
        if state["workflow_status"] != "failed":
            state["workflow_status"] = "completed"
        state["completed_at"] = datetime.now()

        return state

    def _route_from_pay_validation(
        self, state: WorkflowState
    ) -> Literal["compliance", "notification", "end"]:
        """Route from pay validation agent."""
        if state["workflow_status"] == "failed":
            return "notification"

        if state["next_agent"] == "ComplianceAgent" and self.config.compliance_checks_required:
            return "compliance"

        return "notification"

    def _route_from_claims_processing(
        self, state: WorkflowState
    ) -> Literal["compliance", "notification", "end"]:
        """Route from claims processing agent."""
        if state["workflow_status"] == "failed":
            return "notification"

        if state["next_agent"] == "ComplianceAgent" and self.config.compliance_checks_required:
            return "compliance"

        return "notification"

    def _route_from_compliance(
        self, state: WorkflowState
    ) -> Literal["notification", "end"]:
        """Route from compliance agent."""
        if state["workflow_status"] == "failed":
            return "notification"

        return "notification"

    async def validate_pay_record(self, pay_record: Any) -> WorkflowResult:
        """
        Validate a pay record through the workflow.

        Args:
            pay_record: Pay record to validate

        Returns:
            WorkflowResult: Workflow execution result
        """
        workflow_id = generate_id("workflow")
        started_at = datetime.now()

        self.logger.info(
            "workflow_started",
            workflow_id=workflow_id,
            type="pay_validation",
            pay_record_id=pay_record.id,
        )

        # Initialize state
        initial_state: WorkflowState = {
            "messages": [],
            "pay_record": pay_record,
            "claim": None,
            "validation_report": None,
            "claim_decision": None,
            "current_agent": "",
            "next_agent": "PayValidationAgent",
            "workflow_status": "in_progress",
            "error_message": None,
            "workflow_id": workflow_id,
            "started_at": started_at,
            "completed_at": None,
            "iteration_count": 0,
            "metadata": {"workflow_id": workflow_id, "type": "pay_validation"},
        }

        try:
            # Create a graph with pay_validation as entry point
            workflow = StateGraph(WorkflowState)
            workflow.add_node("pay_validation", self._run_pay_validation)
            workflow.add_node("compliance", self._run_compliance)
            workflow.add_node("notification", self._run_notification)

            workflow.add_conditional_edges(
                "pay_validation",
                self._route_from_pay_validation,
                {
                    "compliance": "compliance",
                    "notification": "notification",
                    "end": END,
                },
            )

            workflow.add_conditional_edges(
                "compliance",
                self._route_from_compliance,
                {
                    "notification": "notification",
                    "end": END,
                },
            )

            workflow.add_edge("notification", END)
            workflow.set_entry_point("pay_validation")

            graph = workflow.compile()

            # Run the workflow
            final_state = await graph.ainvoke(initial_state)

            completed_at = final_state.get("completed_at") or datetime.now()
            duration = calculate_duration(started_at, completed_at)

            result = WorkflowResult(
                workflow_id=workflow_id,
                status=final_state["workflow_status"],
                pay_record=pay_record,
                claim=None,
                validation_report=final_state.get("validation_report"),
                claim_decision=None,
                messages=list(final_state["messages"]),
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=duration,
                error_message=final_state.get("error_message"),
                metadata=final_state["metadata"],
            )

            self.logger.info(
                "workflow_completed",
                workflow_id=workflow_id,
                status=result.status,
                duration=duration,
            )

            return result

        except Exception as e:
            self.logger.error(
                "workflow_failed",
                workflow_id=workflow_id,
                error=str(e),
                error_type=type(e).__name__,
            )

            completed_at = datetime.now()
            duration = calculate_duration(started_at, completed_at)

            return WorkflowResult(
                workflow_id=workflow_id,
                status="failed",
                pay_record=pay_record,
                claim=None,
                validation_report=None,
                claim_decision=None,
                messages=[],
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=duration,
                error_message=str(e),
                metadata={"error": str(e), "error_type": type(e).__name__},
            )

    async def process_claim(self, claim: Any) -> WorkflowResult:
        """
        Process a claim through the workflow.

        Args:
            claim: Claim to process

        Returns:
            WorkflowResult: Workflow execution result
        """
        workflow_id = generate_id("workflow")
        started_at = datetime.now()

        self.logger.info(
            "workflow_started",
            workflow_id=workflow_id,
            type="claim_processing",
            claim_id=claim.id,
        )

        # Initialize state
        initial_state: WorkflowState = {
            "messages": [],
            "pay_record": None,
            "claim": claim,
            "validation_report": None,
            "claim_decision": None,
            "current_agent": "",
            "next_agent": "ClaimsProcessingAgent",
            "workflow_status": "in_progress",
            "error_message": None,
            "workflow_id": workflow_id,
            "started_at": started_at,
            "completed_at": None,
            "iteration_count": 0,
            "metadata": {"workflow_id": workflow_id, "type": "claim_processing"},
        }

        try:
            # Create a graph with claims_processing as entry point
            workflow = StateGraph(WorkflowState)
            workflow.add_node("claims_processing", self._run_claims_processing)
            workflow.add_node("compliance", self._run_compliance)
            workflow.add_node("notification", self._run_notification)

            workflow.add_conditional_edges(
                "claims_processing",
                self._route_from_claims_processing,
                {
                    "compliance": "compliance",
                    "notification": "notification",
                    "end": END,
                },
            )

            workflow.add_conditional_edges(
                "compliance",
                self._route_from_compliance,
                {
                    "notification": "notification",
                    "end": END,
                },
            )

            workflow.add_edge("notification", END)
            workflow.set_entry_point("claims_processing")

            graph = workflow.compile()

            # Run the workflow
            final_state = await graph.ainvoke(initial_state)

            completed_at = final_state.get("completed_at") or datetime.now()
            duration = calculate_duration(started_at, completed_at)

            result = WorkflowResult(
                workflow_id=workflow_id,
                status=final_state["workflow_status"],
                pay_record=None,
                claim=claim,
                validation_report=None,
                claim_decision=final_state.get("claim_decision"),
                messages=list(final_state["messages"]),
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=duration,
                error_message=final_state.get("error_message"),
                metadata=final_state["metadata"],
            )

            self.logger.info(
                "workflow_completed",
                workflow_id=workflow_id,
                status=result.status,
                duration=duration,
            )

            return result

        except Exception as e:
            self.logger.error(
                "workflow_failed",
                workflow_id=workflow_id,
                error=str(e),
                error_type=type(e).__name__,
            )

            completed_at = datetime.now()
            duration = calculate_duration(started_at, completed_at)

            return WorkflowResult(
                workflow_id=workflow_id,
                status="failed",
                pay_record=None,
                claim=claim,
                validation_report=None,
                claim_decision=None,
                messages=[],
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=duration,
                error_message=str(e),
                metadata={"error": str(e), "error_type": type(e).__name__},
            )
