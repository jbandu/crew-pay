"""
Base agent class for all agents in the system.
"""

from abc import ABC, abstractmethod
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI

from crew_pay.config.settings import get_settings
from crew_pay.models.state import AgentInput, AgentOutput
from crew_pay.utils.logging import get_logger


class BaseAgent(ABC):
    """
    Base class for all agents in the crew pay system.

    All agents should inherit from this class and implement the process method.
    """

    def __init__(self, name: str, description: str) -> None:
        """
        Initialize the agent.

        Args:
            name: Agent name
            description: Agent description
        """
        self.name = name
        self.description = description
        self.logger = get_logger(f"agent.{name}")
        self.settings = get_settings()
        self.llm = self._create_llm()

    def _create_llm(self) -> ChatOpenAI:
        """Create LLM instance."""
        return ChatOpenAI(
            model=self.settings.openai_model,
            temperature=self.settings.temperature,
            api_key=self.settings.openai_api_key,
        )

    @abstractmethod
    async def process(self, agent_input: AgentInput) -> AgentOutput:
        """
        Process the input and return output.

        Args:
            agent_input: Input data for the agent

        Returns:
            AgentOutput: Processing result
        """
        pass

    def create_message(self, content: str, is_ai: bool = True) -> BaseMessage:
        """
        Create a message.

        Args:
            content: Message content
            is_ai: Whether this is an AI message

        Returns:
            BaseMessage: Created message
        """
        if is_ai:
            return AIMessage(content=content)
        return HumanMessage(content=content)

    def log_start(self, context: dict[str, Any]) -> None:
        """Log agent start."""
        self.logger.info(
            "agent_started",
            agent=self.name,
            context=context,
        )

    def log_end(self, result: dict[str, Any]) -> None:
        """Log agent end."""
        self.logger.info(
            "agent_completed",
            agent=self.name,
            result=result,
        )

    def log_error(self, error: Exception) -> None:
        """Log agent error."""
        self.logger.error(
            "agent_error",
            agent=self.name,
            error=str(error),
            error_type=type(error).__name__,
        )
