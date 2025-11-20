# Architecture

## Overview

The Crew Pay system is a LangGraph-based multi-agent orchestration system for crew pay validation and claims processing. It uses specialized agents to handle different aspects of payroll processing in a coordinated workflow.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Crew Pay System                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────────────────────────────────────┐      │
│  │         LangGraph Orchestrator                     │      │
│  │                                                     │      │
│  │  ┌──────────────┐    ┌──────────────┐            │      │
│  │  │ Pay Record   │    │    Claim     │            │      │
│  │  │  Workflow    │    │  Workflow    │            │      │
│  │  └──────┬───────┘    └──────┬───────┘            │      │
│  │         │                    │                     │      │
│  └─────────┼────────────────────┼────────────────────┘      │
│            │                    │                            │
│  ┌─────────▼────────────────────▼────────────────────┐      │
│  │              Agent Layer                           │      │
│  │                                                     │      │
│  │  ┌──────────────┐  ┌───────────────┐             │      │
│  │  │     Pay      │  │    Claims     │             │      │
│  │  │  Validation  │  │  Processing   │             │      │
│  │  │    Agent     │  │     Agent     │             │      │
│  │  └──────┬───────┘  └───────┬───────┘             │      │
│  │         │                   │                      │      │
│  │         └────────┬──────────┘                      │      │
│  │                  │                                  │      │
│  │         ┌────────▼─────────┐                       │      │
│  │         │   Compliance     │                       │      │
│  │         │      Agent       │                       │      │
│  │         └────────┬─────────┘                       │      │
│  │                  │                                  │      │
│  │         ┌────────▼─────────┐                       │      │
│  │         │  Notification    │                       │      │
│  │         │      Agent       │                       │      │
│  │         └──────────────────┘                       │      │
│  └─────────────────────────────────────────────────────┘      │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐      │
│  │              Core Components                         │      │
│  │                                                     │      │
│  │  ┌────────────┐  ┌───────────┐  ┌──────────┐      │      │
│  │  │   Models   │  │  Config   │  │  Utils   │      │      │
│  │  └────────────┘  └───────────┘  └──────────┘      │      │
│  └─────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Agents

### 1. PayValidationAgent

**Purpose**: Validates crew pay records for accuracy and compliance.

**Responsibilities**:
- Hours validation (regular and overtime)
- Pay calculation accuracy
- Compliance with pay period rules
- Data completeness and consistency
- LLM-based semantic validation

**Input**: PayRecord
**Output**: ValidationReport

### 2. ClaimsProcessingAgent

**Purpose**: Processes and evaluates crew pay claims.

**Responsibilities**:
- Claim validation and verification
- Supporting document review
- Claim amount assessment
- Approval/rejection decisions
- Next steps determination

**Input**: Claim
**Output**: ClaimDecision

### 3. ComplianceAgent

**Purpose**: Ensures compliance with regulations and policies.

**Responsibilities**:
- Labor law compliance checks
- Tax regulation validation
- Company policy adherence
- Industry standard verification
- Audit trail creation

**Input**: PayRecord or Claim
**Output**: ComplianceReport

### 4. NotificationAgent

**Purpose**: Sends notifications and alerts to stakeholders.

**Responsibilities**:
- Email notifications
- SMS alerts
- System notifications
- Audit logging
- Status updates

**Input**: Workflow context
**Output**: NotificationReceipt

## Workflows

### Pay Record Validation Workflow

```
Start → PayValidationAgent → ComplianceAgent → NotificationAgent → End
```

1. **PayValidationAgent**: Validates the pay record
2. **ComplianceAgent**: Performs compliance checks (if enabled)
3. **NotificationAgent**: Sends notifications to stakeholders

### Claim Processing Workflow

```
Start → ClaimsProcessingAgent → ComplianceAgent → NotificationAgent → End
```

1. **ClaimsProcessingAgent**: Evaluates and decides on the claim
2. **ComplianceAgent**: Ensures compliance (if enabled)
3. **NotificationAgent**: Sends notifications about the decision

## State Management

The system uses LangGraph's StateGraph for managing workflow state:

```python
class WorkflowState(TypedDict):
    messages: List[BaseMessage]
    pay_record: Optional[PayRecord]
    claim: Optional[Claim]
    validation_report: Optional[ValidationReport]
    claim_decision: Optional[ClaimDecision]
    current_agent: str
    next_agent: Optional[str]
    workflow_status: str
    error_message: Optional[str]
    workflow_id: str
    started_at: datetime
    completed_at: Optional[datetime]
    iteration_count: int
    metadata: Dict[str, Any]
```

## LLM Integration

The system integrates LLMs (OpenAI GPT-4) for:
- Semantic validation of pay records
- Intelligent claim evaluation
- Compliance assessment
- Anomaly detection

## Configuration

Configuration is managed through:
- Environment variables (.env)
- Settings class (Pydantic)
- WorkflowConfig for runtime configuration

## Extensibility

The system is designed for extensibility:

1. **New Agents**: Create new agents by extending `BaseAgent`
2. **Custom Workflows**: Build custom workflows using LangGraph
3. **Integration Points**: Connect to external systems via agents
4. **Custom Validation**: Add custom validation rules

## Error Handling

- Custom exception hierarchy
- Comprehensive logging with structlog
- Graceful degradation
- Retry mechanisms

## Monitoring and Logging

- Structured logging (JSON format)
- Workflow tracing
- Agent execution tracking
- Performance metrics
