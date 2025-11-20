# Crew Pay - Multi-Agent Orchestration System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A LangGraph-based multi-agent orchestration system for crew pay validation and claims processing, powered by Large Language Models (LLMs).

## Overview

Crew Pay is an intelligent payroll processing system that leverages multiple specialized AI agents to validate pay records, process claims, ensure compliance, and notify stakeholders. Built on LangGraph, it provides a flexible and extensible framework for automated payroll workflows.

## Features

- **Multi-Agent Architecture**: Specialized agents for different aspects of payroll processing
  - PayValidationAgent: Validates crew pay records
  - ClaimsProcessingAgent: Processes and evaluates claims
  - ComplianceAgent: Ensures regulatory compliance
  - NotificationAgent: Sends alerts and notifications

- **LangGraph Orchestration**: Coordinated workflows using LangGraph's StateGraph
- **LLM Integration**: Intelligent decision-making with OpenAI GPT models
- **Comprehensive Validation**: Multiple validation checks including hours, calculations, and compliance
- **Flexible Configuration**: Environment-based configuration with sensible defaults
- **Structured Logging**: JSON-based logging for monitoring and debugging
- **Type Safety**: Full type hints with Pydantic models
- **CLI Interface**: Command-line tools for easy interaction
- **Extensible Design**: Easy to add new agents and workflows

## Architecture

```
┌─────────────────────────────────────────┐
│      LangGraph Orchestrator             │
├─────────────────────────────────────────┤
│                                         │
│  PayValidation ──> Compliance ──>      │
│                      │                  │
│  ClaimsProcessing ──┘                  │
│                      │                  │
│                      ▼                  │
│                 Notification            │
└─────────────────────────────────────────┘
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture information.

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/crew-pay.git
cd crew-pay

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Configuration

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
TEMPERATURE=0.7
```

### Usage

#### Command Line Interface

Validate a pay record:

```bash
crew-pay validate-pay examples/example_pay_record.json
```

Process a claim:

```bash
crew-pay process-claim examples/example_claim.json
```

View system information:

```bash
crew-pay info
```

#### Python API

```python
import asyncio
from decimal import Decimal
from datetime import date

from crew_pay.models.schemas import CrewMember, PayRecord, PayPeriodType
from crew_pay.orchestrator.workflow import CrewPayWorkflow
from crew_pay.utils.logging import configure_logging

# Configure logging
configure_logging()

# Create a crew member
crew_member = CrewMember(
    id="crew-001",
    name="John Doe",
    employee_id="EMP-12345",
    department="Engineering",
    position="Senior Engineer",
    hourly_rate=Decimal("75.50"),
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

# Validate the pay record
async def main():
    workflow = CrewPayWorkflow()
    result = await workflow.validate_pay_record(pay_record)

    print(f"Status: {result.status}")
    if result.validation_report:
        print(f"Validation: {result.validation_report.overall_status.value}")

asyncio.run(main())
```

See [docs/USAGE.md](docs/USAGE.md) for complete usage documentation.

## Project Structure

```
crew-pay/
├── src/crew_pay/
│   ├── agents/              # Agent implementations
│   │   ├── base_agent.py
│   │   ├── pay_validation_agent.py
│   │   ├── claims_processing_agent.py
│   │   ├── compliance_agent.py
│   │   └── notification_agent.py
│   ├── orchestrator/        # LangGraph workflow orchestration
│   │   └── workflow.py
│   ├── models/              # Data models and schemas
│   │   ├── schemas.py
│   │   └── state.py
│   ├── config/              # Configuration management
│   │   └── settings.py
│   ├── utils/               # Utilities
│   │   ├── logging.py
│   │   ├── exceptions.py
│   │   └── helpers.py
│   └── cli.py               # Command-line interface
├── tests/                   # Unit and integration tests
│   ├── unit/
│   └── conftest.py
├── examples/                # Example usage
│   ├── example_pay_record.json
│   ├── example_claim.json
│   └── usage_example.py
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md
│   └── USAGE.md
├── pyproject.toml           # Project configuration
├── requirements.txt         # Dependencies
└── README.md
```

## Agents

### PayValidationAgent

Validates crew pay records for accuracy and compliance:
- Hours validation (regular and overtime)
- Pay calculation verification
- Pay period consistency checks
- Data completeness validation
- LLM-based semantic validation

### ClaimsProcessingAgent

Processes and evaluates crew pay claims:
- Claim validation and verification
- Supporting document review
- Amount assessment
- Approval/rejection decisions
- Auto-approval for small claims

### ComplianceAgent

Ensures regulatory and policy compliance:
- Labor law compliance checks
- Tax regulation validation
- Company policy adherence
- Industry standard verification

### NotificationAgent

Sends notifications and alerts:
- Email notifications to crew members
- Alerts to payroll/finance departments
- System notifications
- Audit logging

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/crew_pay --cov-report=html

# Run specific tests
pytest tests/unit/test_models.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff src/ tests/

# Type checking
mypy src/
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | LLM model to use | `gpt-4-turbo-preview` |
| `TEMPERATURE` | LLM temperature | `0.7` |
| `MAX_ITERATIONS` | Max workflow iterations | `10` |
| `TIMEOUT_SECONDS` | Workflow timeout | `300` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_FORMAT` | Log format (json/text) | `json` |

See `.env.example` for all available options.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please:
- Open an issue on GitHub
- Check the [documentation](docs/)
- Review the [examples](examples/)

## Roadmap

- [ ] Human-in-the-loop approval workflow
- [ ] Integration with external payroll systems
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Web dashboard interface
- [ ] Batch processing capabilities
- [ ] Custom validation rules engine

## Acknowledgments

Built with:
- [LangGraph](https://github.com/langchain-ai/langgraph) - Multi-agent orchestration
- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
- [Pydantic](https://github.com/pydantic/pydantic) - Data validation
- [OpenAI](https://openai.com/) - LLM models