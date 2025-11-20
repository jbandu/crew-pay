# Usage Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/crew-pay.git
cd crew-pay

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Configuration

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and add your configuration:

```env
# Required
OPENAI_API_KEY=your-api-key-here

# Optional
OPENAI_MODEL=gpt-4-turbo-preview
TEMPERATURE=0.7
MAX_ITERATIONS=10
TIMEOUT_SECONDS=300
LOG_LEVEL=INFO
```

## Command-Line Interface

### Validate a Pay Record

```bash
crew-pay validate-pay examples/example_pay_record.json

# Save results to file
crew-pay validate-pay examples/example_pay_record.json --output results.json
```

### Process a Claim

```bash
crew-pay process-claim examples/example_claim.json

# Save results to file
crew-pay process-claim examples/example_claim.json --output results.json
```

### View System Information

```bash
crew-pay info
```

## Python API

### Basic Usage

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
    email="john.doe@example.com",
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
    print(f"Duration: {result.duration_seconds:.2f}s")

    if result.validation_report:
        print(f"Validation: {result.validation_report.overall_status.value}")

asyncio.run(main())
```

### Processing Claims

```python
from crew_pay.models.schemas import Claim, ClaimType

# Create a claim
claim = Claim(
    id="claim-2024-001",
    crew_member=crew_member,
    claim_type=ClaimType.OVERTIME,
    amount=Decimal("500.00"),
    description="Overtime work on emergency deployment",
    supporting_documents=["timesheet.pdf"],
)

# Process the claim
async def process():
    workflow = CrewPayWorkflow()
    result = await workflow.process_claim(claim)

    if result.claim_decision:
        print(f"Decision: {result.claim_decision.decision.value}")
        print(f"Approved: ${result.claim_decision.approved_amount}")

asyncio.run(process())
```

### Custom Workflow Configuration

```python
from crew_pay.models.state import WorkflowConfig

# Create custom configuration
config = WorkflowConfig(
    max_iterations=20,
    timeout_seconds=600,
    enable_human_in_loop=True,
    compliance_checks_required=True,
    auto_approve_claim_threshold=100.0,
)

# Use custom configuration
workflow = CrewPayWorkflow(config=config)
```

## Input Data Formats

### Pay Record JSON

```json
{
  "id": "pay-2024-001",
  "crew_member": {
    "id": "crew-001",
    "name": "John Doe",
    "employee_id": "EMP-12345",
    "department": "Engineering",
    "position": "Senior Engineer",
    "hourly_rate": "75.50",
    "email": "john.doe@example.com"
  },
  "pay_period_start": "2024-01-01",
  "pay_period_end": "2024-01-15",
  "pay_period_type": "bi_weekly",
  "regular_hours": "80.0",
  "overtime_hours": "5.0",
  "gross_pay": "6415.00",
  "deductions": "1283.00",
  "net_pay": "5132.00"
}
```

### Claim JSON

```json
{
  "id": "claim-2024-001",
  "crew_member": {
    "id": "crew-002",
    "name": "Jane Smith",
    "employee_id": "EMP-67890",
    "department": "Operations",
    "position": "Operations Manager",
    "hourly_rate": "85.00",
    "email": "jane.smith@example.com"
  },
  "claim_type": "overtime",
  "amount": "500.00",
  "description": "Overtime work on emergency deployment",
  "supporting_documents": ["timesheet.pdf", "logs.txt"]
}
```

## Output Formats

### Validation Result

```json
{
  "workflow_id": "workflow-abc123",
  "status": "completed",
  "validation_report": {
    "pay_record_id": "pay-2024-001",
    "overall_status": "passed",
    "validation_results": [
      {
        "check_name": "hours_limit_check",
        "status": "passed",
        "message": "Hours within acceptable limits"
      }
    ],
    "summary": "All validation checks passed"
  },
  "duration_seconds": 12.5
}
```

### Claim Decision Result

```json
{
  "workflow_id": "workflow-xyz789",
  "status": "completed",
  "claim_decision": {
    "claim_id": "claim-2024-001",
    "decision": "approved",
    "approved_amount": "500.00",
    "rationale": "Claim approved based on valid documentation",
    "next_steps": [
      "Process payment",
      "Notify crew member"
    ]
  },
  "duration_seconds": 8.3
}
```

## Error Handling

Errors are logged and returned in the result:

```python
result = await workflow.validate_pay_record(pay_record)

if result.status == "failed":
    print(f"Workflow failed: {result.error_message}")
```

## Best Practices

1. **Always validate input data** before processing
2. **Use environment variables** for configuration
3. **Enable logging** to track workflow execution
4. **Handle errors gracefully** in production
5. **Monitor workflow duration** for performance
6. **Review validation reports** before finalizing payments
7. **Store audit trails** for compliance

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure `OPENAI_API_KEY` is set in `.env`
   - Verify the key is valid

2. **Validation Failures**
   - Check input data format
   - Review validation error messages
   - Ensure all required fields are present

3. **Timeout Errors**
   - Increase `TIMEOUT_SECONDS` in configuration
   - Check LLM API availability

4. **Import Errors**
   - Ensure package is installed: `pip install -e .`
   - Check Python version (3.10+)

## Examples

See the `examples/` directory for:
- `example_pay_record.json` - Sample pay record
- `example_claim.json` - Sample claim
- `usage_example.py` - Complete Python examples
