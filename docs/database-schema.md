# Avelo Airlines Crew Pay Management System
## Database Architecture Documentation

---

## Table of Contents
1. [Overview](#overview)
2. [Architecture Design](#architecture-design)
3. [Database Stack](#database-stack)
4. [Schema Design](#schema-design)
5. [Data Flow](#data-flow)
6. [Row-Level Security (RLS)](#row-level-security)
7. [Query Examples](#query-examples)
8. [Backup & Recovery](#backup-and-recovery)
9. [Performance Optimization](#performance-optimization)

---

## Overview

The Avelo Airlines Crew Pay Management System uses a **hybrid database architecture** combining:

- **Neon Postgres** (with pgBouncer pooling) for transactional data
- **Neo4j** knowledge graph for complex rule relationships and interpretations

This architecture enables:
- ✅ Proactive pay discrepancy detection
- ✅ Automated claims processing with AI agents
- ✅ Complex FAA and union contract compliance checking
- ✅ Intelligent pay calculations with rule interpretation
- ✅ Full audit trail of all operations

---

## Architecture Design

### Hybrid Database Approach

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│           (Prisma ORM + Neo4j Driver)                       │
└─────────────┬───────────────────────────┬───────────────────┘
              │                           │
              ▼                           ▼
┌─────────────────────────┐   ┌─────────────────────────────┐
│   NEON POSTGRES          │   │   NEO4J KNOWLEDGE GRAPH     │
│   (Transactional Data)   │   │   (Rule Relationships)      │
├─────────────────────────┤   ├─────────────────────────────┤
│ • Crew Members          │   │ • FAA Rules                 │
│ • Flights               │   │ • Contract Terms            │
│ • Assignments           │   │ • Scenarios                 │
│ • Pay Calculations      │   │ • Pay Components            │
│ • Discrepancies         │   │ • Rule Conflicts            │
│ • Claims                │   │ • Interpretations           │
│ • Audit Logs            │   │ • Dependencies              │
└─────────────────────────┘   └─────────────────────────────┘
```

### Why Hybrid Architecture?

| Aspect | Postgres | Neo4j |
|--------|----------|-------|
| **Use Case** | ACID transactions, crew data, pay records | Complex rule relationships, pattern matching |
| **Strengths** | Data integrity, strong consistency | Graph traversal, relationship queries |
| **Queries** | Relational joins, aggregations | Path finding, scenario matching |
| **Example** | "Get all flights for crew XP001" | "Find all rules that apply to a delayed red-eye flight" |

---

## Database Stack

### Neon Postgres Configuration

**Features:**
- **Connection Pooling**: pgBouncer for efficient connection management
- **Branching**: Separate dev, staging, production databases
- **Auto-scaling**: Serverless Postgres with automatic scaling
- **Point-in-time Recovery**: Continuous backup with PITR
- **SSL/TLS**: Encrypted connections by default

**Environment Variables:**
```bash
DATABASE_URL=postgresql://user:pass@ep-xxx.aws.neon.tech/crew_copilot_production?sslmode=require&pgbouncer=true
DIRECT_URL=postgresql://user:pass@ep-xxx.aws.neon.tech/crew_copilot_production?sslmode=require
SHADOW_DATABASE_URL=postgresql://user:pass@ep-xxx.aws.neon.tech/crew_copilot_shadow?sslmode=require
```

### Neo4j Knowledge Graph

**Features:**
- **Graph Database**: Optimized for relationship queries
- **Cypher Query Language**: Declarative graph pattern matching
- **ACID Transactions**: Full transactional support
- **Clustering**: High availability and read replicas

**Environment Variables:**
```bash
NEO4J_URI=neo4j+s://xxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
```

---

## Schema Design

### Core Tables (Postgres)

#### 1. crew_members
**Purpose**: Store crew member profiles and employment details

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| employee_id | VARCHAR(20) | Unique employee number (indexed) |
| first_name | VARCHAR(100) | First name |
| last_name | VARCHAR(100) | Last name |
| position | ENUM | CAPTAIN, FIRST_OFFICER, FLIGHT_ATTENDANT |
| base_location | VARCHAR(10) | Home base (BUR, IFP, HVN) |
| hire_date | DATE | Date of hire |
| seniority_number | INTEGER | Seniority ranking (indexed) |
| base_hourly_rate | DECIMAL(10,2) | Current hourly rate |
| union_status | ENUM | UNION_MEMBER, NON_UNION, PROBATIONARY |
| contract_type | ENUM | FULL_TIME, PART_TIME, CONTRACTOR |

**Indexes:**
- `employee_id` (unique)
- `seniority_number`
- `base_location`
- `position`

**Relationships:**
- One-to-many → crew_assignments
- One-to-many → pay_calculations
- One-to-many → discrepancies
- One-to-many → claims

---

#### 2. flights
**Purpose**: Track all flight operations

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| flight_number | VARCHAR(10) | Flight identifier (e.g., XP101) |
| origin_airport | VARCHAR(4) | Origin ICAO code |
| destination_airport | VARCHAR(4) | Destination ICAO code |
| scheduled_departure | TIMESTAMPTZ | Scheduled departure time |
| scheduled_arrival | TIMESTAMPTZ | Scheduled arrival time |
| actual_departure | TIMESTAMPTZ | Actual departure time |
| actual_arrival | TIMESTAMPTZ | Actual arrival time |
| block_time_hours | DECIMAL(5,2) | Actual flight duration |
| delay_minutes | INTEGER | Total delay in minutes |
| delay_code | VARCHAR(10) | Delay code (WX, MX, ATC, etc.) |
| delay_reason | TEXT | Detailed delay reason |
| aircraft_type | VARCHAR(20) | Aircraft model |
| aircraft_registration | VARCHAR(20) | Tail number |

**Indexes:**
- `flight_number`
- `scheduled_departure`
- `actual_departure`
- `(origin_airport, destination_airport)` (composite)

---

#### 3. crew_assignments
**Purpose**: Link crew members to flights

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| crew_member_id | UUID | FK → crew_members |
| flight_id | UUID | FK → flights |
| position | ENUM | OPERATING, DEADHEAD, RESERVE, STANDBY |
| duty_start_time | TIMESTAMPTZ | Duty period start |
| duty_end_time | TIMESTAMPTZ | Duty period end |
| check_in_time | TIMESTAMPTZ | Actual check-in |
| check_out_time | TIMESTAMPTZ | Actual check-out |

**Indexes:**
- `crew_member_id`
- `flight_id`
- `duty_start_time`

---

#### 4. pay_periods
**Purpose**: Define payroll cycles

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| start_date | DATE | Period start date |
| end_date | DATE | Period end date |
| pay_date | DATE | Payment date |
| status | ENUM | OPEN, CLOSED, PAID, PROCESSING |

**Indexes:**
- `(start_date, end_date)` (composite)
- `status`

---

#### 5. pay_calculations
**Purpose**: Store computed pay for each crew member per pay period

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| crew_member_id | UUID | FK → crew_members |
| pay_period_id | UUID | FK → pay_periods |
| flight_pay_hours | DECIMAL(8,2) | Credit hours earned |
| flight_pay_amount | DECIMAL(10,2) | Base flight pay |
| overtime_hours | DECIMAL(8,2) | Overtime hours |
| overtime_amount | DECIMAL(10,2) | Overtime pay |
| delay_pay_amount | DECIMAL(10,2) | Delay compensation |
| per_diem_amount | DECIMAL(10,2) | Per diem total |
| premium_pay_amount | DECIMAL(10,2) | Red-eye, holiday premiums |
| guarantee_hours | DECIMAL(8,2) | Monthly guarantee hours |
| total_gross_pay | DECIMAL(10,2) | Total gross pay |
| calculation_date | TIMESTAMPTZ | When calculated |
| validated_at | TIMESTAMPTZ | When validated |
| validated_by | VARCHAR(100) | Who validated |

**Indexes:**
- `crew_member_id`
- `pay_period_id`
- `calculation_date`

---

#### 6. discrepancies
**Purpose**: Track proactively detected pay issues

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| crew_member_id | UUID | FK → crew_members |
| pay_period_id | UUID | FK → pay_periods |
| flight_id | UUID | FK → flights (nullable) |
| discrepancy_type | ENUM | UNDERPAYMENT, MISSING_PREMIUM, etc. |
| expected_amount | DECIMAL(10,2) | What should have been paid |
| actual_amount | DECIMAL(10,2) | What was paid |
| difference_amount | DECIMAL(10,2) | Delta |
| severity | ENUM | CRITICAL, HIGH, MEDIUM, LOW |
| detected_by | ENUM | PROACTIVE_AGENT, CREW_CLAIM, SYSTEM_CHECK |
| detected_at | TIMESTAMPTZ | Detection timestamp |
| resolution_status | ENUM | OPEN, INVESTIGATING, RESOLVED, CLOSED |
| resolution_date | TIMESTAMPTZ | When resolved |
| resolved_by | VARCHAR(100) | Who resolved |
| resolution_notes | TEXT | Resolution details |

**Indexes:**
- `crew_member_id`
- `pay_period_id`
- `resolution_status`
- `detected_at`
- `severity`

---

#### 7. claims
**Purpose**: Track crew-submitted pay claims

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| claim_number | VARCHAR(20) | Unique claim ID (e.g., CLM-2024-0001) |
| crew_member_id | UUID | FK → crew_members |
| pay_period_id | UUID | FK → pay_periods |
| flight_ids | TEXT[] | Array of related flight IDs |
| claim_type | ENUM | UNDERPAYMENT, MISSING_FLIGHT, etc. |
| description | TEXT | Crew's explanation |
| claimed_amount | DECIMAL(10,2) | Amount claimed |
| submitted_at | TIMESTAMPTZ | Submission time |
| submitted_by | VARCHAR(100) | Submitter employee ID |
| status | ENUM | SUBMITTED, UNDER_REVIEW, APPROVED, DENIED |
| reviewed_at | TIMESTAMPTZ | Review timestamp |
| reviewed_by | VARCHAR(100) | Reviewer (human or AI) |
| decision | ENUM | APPROVE, DENY, PARTIAL_APPROVE |
| decision_rationale | TEXT | Detailed explanation |
| approved_amount | DECIMAL(10,2) | Approved amount |
| payment_date | DATE | When paid |
| payment_status | ENUM | PENDING, PROCESSING, PAID, FAILED |
| appeal_submitted_at | TIMESTAMPTZ | Appeal timestamp |
| appeal_notes | TEXT | Appeal details |

**Indexes:**
- `crew_member_id`
- `claim_number` (unique)
- `status`
- `submitted_at`

---

#### 8. faa_rules
**Purpose**: Store FAA regulations (Part 117, Part 121, etc.)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| rule_code | VARCHAR(50) | Unique code (e.g., Part117.23) |
| rule_category | ENUM | FLIGHT_DUTY_PERIOD, REST_REQUIREMENTS, etc. |
| rule_title | VARCHAR(255) | Human-readable title |
| rule_text | TEXT | Full regulation text |
| effective_date | DATE | When rule took effect |
| expiration_date | DATE | When rule expires (nullable) |
| applies_to | ENUM[] | PILOTS, FLIGHT_ATTENDANTS, ALL_CREW |

**Indexes:**
- `rule_code` (unique)
- `rule_category`

---

#### 9. union_contract_terms
**Purpose**: Store union agreement terms

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| term_code | VARCHAR(50) | Unique code (e.g., ALPA_Section_5.A) |
| term_category | ENUM | PAY_RATES, GUARANTEES, PREMIUMS, etc. |
| term_title | VARCHAR(255) | Human-readable title |
| term_text | TEXT | Full contract language |
| calculation_formula | JSONB | Formula structure |
| effective_date | DATE | When term took effect |
| expiration_date | DATE | When term expires (nullable) |
| applies_to | ENUM[] | Crew positions |

**Indexes:**
- `term_code` (unique)
- `term_category`

**Example calculation_formula:**
```json
{
  "type": "monthly_guarantee",
  "hours": 70,
  "proration": "calendar_days"
}
```

---

#### 10. rule_interpretations
**Purpose**: Store complex scenario interpretations

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| scenario_description | TEXT | Description of scenario |
| applicable_faa_rule_ids | UUID[] | Related FAA rules |
| applicable_contract_term_ids | UUID[] | Related contract terms |
| interpretation | TEXT | How rules apply |
| example_calculation | JSONB | Sample calculation |
| confidence_score | INTEGER | Confidence (0-100) |
| validated_by | VARCHAR(100) | Who validated |

---

#### 11. notifications
**Purpose**: Track all crew notifications

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| crew_member_id | UUID | FK → crew_members |
| notification_type | ENUM | PROACTIVE_FIX, CLAIM_STATUS, etc. |
| title | VARCHAR(255) | Notification title |
| message | TEXT | Full message |
| related_entity_type | VARCHAR(50) | Entity type (discrepancy, claim, etc.) |
| related_entity_id | UUID | Related entity ID |
| sent_at | TIMESTAMPTZ | Send timestamp |
| read_at | TIMESTAMPTZ | Read timestamp (nullable) |
| delivery_method | ENUM | EMAIL, SMS, APP_PUSH, IN_APP |

**Indexes:**
- `crew_member_id`
- `sent_at`
- `read_at`

---

#### 12. audit_log
**Purpose**: Full audit trail (append-only)

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| entity_type | VARCHAR(50) | Type of entity |
| entity_id | UUID | Entity ID |
| action | ENUM | CREATED, UPDATED, DELETED, APPROVED, DENIED |
| actor_id | VARCHAR(100) | Who performed action |
| actor_type | ENUM | CREW, ADMIN, AI_AGENT, SYSTEM |
| changes | JSONB | Before/after values |
| reason | TEXT | Optional reason |
| ip_address | VARCHAR(45) | IP address |
| user_agent | TEXT | User agent string |
| created_at | TIMESTAMPTZ | Action timestamp |

**Indexes:**
- `(entity_type, entity_id)` (composite)
- `actor_id`
- `created_at`

**Append-Only Policy**: Audit logs cannot be updated or deleted.

---

## Data Flow

### 1. Flight Assignment to Pay Calculation

```
┌──────────────┐
│  Flight      │
│  Created     │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Crew            │
│  Assigned        │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐     ┌─────────────────────┐
│  Flight          │────→│  Neo4j: Match       │
│  Completed       │     │  Scenario Pattern   │
└──────┬───────────┘     └─────────┬───────────┘
       │                           │
       │                           ▼
       │                 ┌─────────────────────┐
       │                 │  Get Applicable     │
       │                 │  Rules & Formulas   │
       │                 └─────────┬───────────┘
       │                           │
       ▼                           ▼
┌──────────────────────────────────────────┐
│  Calculate Pay Components:               │
│  • Flight Pay (with duty rig)            │
│  • Per Diem                              │
│  • Premiums (if applicable)              │
│  • Delay Pay (if applicable)             │
└──────┬───────────────────────────────────┘
       │
       ▼
┌──────────────────┐
│  Pay Period      │
│  Aggregation     │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐     ┌─────────────────────┐
│  Proactive       │────→│  Discrepancy        │
│  Check           │     │  Detected?          │
└──────────────────┘     └─────────┬───────────┘
                                   │
                         ┌─────────┴─────────┐
                         │                   │
                         ▼                   ▼
                  ┌──────────┐      ┌───────────────┐
                  │  Auto-   │      │  Notify Crew  │
                  │  Fix     │      │  & Create     │
                  │          │      │  Discrepancy  │
                  └──────────┘      └───────────────┘
```

### 2. Claim Processing Flow

```
┌──────────────┐
│  Crew        │
│  Submits     │
│  Claim       │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Create Claim    │
│  Record          │
│  (status:        │
│   SUBMITTED)     │
└──────┬───────────┘
       │
       ▼
┌──────────────────────────────────┐
│  AI Agent Review:                │
│  1. Fetch flight data            │
│  2. Query Neo4j for rules        │
│  3. Recalculate expected pay     │
│  4. Compare to actual pay        │
│  5. Generate decision rationale  │
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────┐
│  Update Claim:   │
│  • Decision      │
│  • Rationale     │
│  • Amount        │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Notify Crew     │
│  of Decision     │
└──────────────────┘
```

---

## Row-Level Security (RLS)

### Security Policies

**Crew Member Access:**
```sql
-- Crew can only see their own data
CREATE POLICY crew_own_data ON crew_members
  FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY crew_own_assignments ON crew_assignments
  FOR SELECT
  USING (crew_member_id = auth.uid());

CREATE POLICY crew_own_pay ON pay_calculations
  FOR SELECT
  USING (crew_member_id = auth.uid());

CREATE POLICY crew_own_claims ON claims
  FOR SELECT
  USING (crew_member_id = auth.uid());
```

**Admin Access:**
```sql
-- Admins can see all data
CREATE POLICY admin_all_data ON crew_members
  FOR ALL
  USING (auth.role() = 'admin');
```

**AI Agent Access:**
```sql
-- AI agents have service role for automated operations
CREATE POLICY ai_agent_service_role ON pay_calculations
  FOR ALL
  USING (auth.role() = 'service_role');
```

**Audit Log Protection:**
```sql
-- Audit log is append-only
CREATE POLICY audit_append_only ON audit_log
  FOR INSERT
  WITH CHECK (true);

-- Prevent updates and deletes
CREATE POLICY audit_no_update ON audit_log
  FOR UPDATE
  USING (false);

CREATE POLICY audit_no_delete ON audit_log
  FOR DELETE
  USING (false);
```

---

## Query Examples

### Common Postgres Queries

#### 1. Get crew member's pay history
```sql
SELECT
  pp.start_date,
  pp.end_date,
  pc.flight_pay_hours,
  pc.total_gross_pay,
  pc.validated_at
FROM pay_calculations pc
JOIN pay_periods pp ON pc.pay_period_id = pp.id
WHERE pc.crew_member_id = $1
ORDER BY pp.start_date DESC
LIMIT 12;
```

#### 2. Find unresolved discrepancies
```sql
SELECT
  cm.employee_id,
  cm.first_name,
  cm.last_name,
  d.discrepancy_type,
  d.difference_amount,
  d.severity,
  d.detected_at
FROM discrepancies d
JOIN crew_members cm ON d.crew_member_id = cm.id
WHERE d.resolution_status IN ('OPEN', 'INVESTIGATING')
ORDER BY d.severity DESC, d.detected_at ASC;
```

#### 3. Calculate monthly utilization
```sql
SELECT
  cm.employee_id,
  cm.position,
  SUM(pc.flight_pay_hours) as total_hours,
  pc.guarantee_hours,
  CASE
    WHEN SUM(pc.flight_pay_hours) > pc.guarantee_hours
    THEN 'Over Guarantee'
    ELSE 'Under Guarantee'
  END as status
FROM pay_calculations pc
JOIN crew_members cm ON pc.crew_member_id = cm.id
JOIN pay_periods pp ON pc.pay_period_id = pp.id
WHERE pp.start_date >= DATE_TRUNC('month', CURRENT_DATE)
GROUP BY cm.employee_id, cm.position, pc.guarantee_hours
ORDER BY total_hours DESC;
```

### Common Neo4j Queries

#### 1. Find all rules for a delayed red-eye flight
```cypher
MATCH (s:Scenario {id: 'delayed_flight_controllable'})
MATCH (r)-[:APPLIES_TO]->(s)
RETURN r.code, r.title, r.priority
ORDER BY r.priority DESC;
```

#### 2. Get pay components and their dependencies
```cypher
MATCH (pc:PayComponent {type: 'overtime'})
MATCH path = (pc)-[:DEPENDS_ON*]->(dependency)
RETURN path;
```

#### 3. Find rule conflicts
```cypher
MATCH (r1:Rule)-[c:CONFLICTS_WITH]->(r2:Rule)
WHERE r1.appliesTo CONTAINS 'CAPTAIN'
RETURN r1.code, r2.code, c.resolutionMethod, c.notes;
```

---

## Backup and Recovery

### Neon Postgres Backup Strategy

**Automated Backups:**
- Continuous backup with Write-Ahead Log (WAL) archiving
- Point-in-time recovery (PITR) up to 7 days
- Daily full backups retained for 30 days
- Weekly backups retained for 90 days

**Manual Backup:**
```bash
# Export database to SQL file
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore from backup
psql $DATABASE_URL < backup_20241120.sql
```

**Branch-Based Recovery:**
```bash
# Create a database branch from a specific timestamp
# (via Neon Console or API)
neon branches create --parent main --name recovery-20241120 --timestamp 2024-11-20T10:00:00Z
```

### Neo4j Backup Strategy

**Automated Backups:**
- Neo4j Aura provides automatic daily backups
- Retained for 30 days

**Manual Export:**
```bash
# Export entire graph to Cypher script
cypher-shell -u neo4j -p password \
  "CALL apoc.export.cypher.all('backup.cypher', {})"

# Restore from Cypher script
cypher-shell -u neo4j -p password < backup.cypher
```

---

## Performance Optimization

### Index Strategy

**Postgres:**
- All foreign keys are indexed
- Frequently queried columns (employee_id, claim_number) have unique indexes
- Composite indexes on date ranges and multi-column queries
- BRIN indexes for time-series data (created_at columns)

**Neo4j:**
- Unique constraints on all identifier fields
- Indexes on category and type fields
- Composite indexes for complex pattern matching

### Query Optimization

**Use EXPLAIN ANALYZE:**
```sql
EXPLAIN ANALYZE
SELECT * FROM pay_calculations
WHERE crew_member_id = $1 AND pay_period_id = $2;
```

**Connection Pooling:**
- pgBouncer pool size: 100 connections
- Transaction mode for short-lived queries
- Session mode for migrations

**Caching Strategy:**
- Application-level caching for:
  - FAA rules (rarely change)
  - Contract terms (change annually)
  - Crew member profiles (change infrequently)
- Cache invalidation on updates

### Performance Testing Requirements

Test with 10,000+ flight assignments:
- Query response time < 100ms for simple queries
- Query response time < 500ms for complex joins
- Bulk pay calculation < 30 seconds for 1,000 crew members
- Discrepancy detection < 5 minutes for full pay period

---

## Maintenance Tasks

### Daily
- Monitor slow queries (> 1 second)
- Check connection pool utilization
- Review error logs

### Weekly
- Analyze query performance
- Update table statistics
- Review index usage

### Monthly
- Vacuum and analyze tables
- Archive old audit logs (> 1 year)
- Review and optimize slow queries

### Quarterly
- Database performance review
- Schema evolution planning
- Backup restoration testing

---

## Migration Strategy

### Schema Changes

All schema changes must be done through **Prisma Migrate**:

```bash
# Create migration
npm run db:migrate -- --name add_new_field

# Apply migration to production
npm run db:migrate:deploy
```

### Data Migration

For data transformations:

```typescript
// prisma/migrations/[timestamp]_data_migration.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  // Perform data transformation
  await prisma.$executeRaw`
    UPDATE crew_members
    SET base_location = 'BUR'
    WHERE base_location IS NULL;
  `;
}

main();
```

---

## Security Best Practices

1. **Never commit .env files** - Use .env.example as template
2. **Rotate database credentials** quarterly
3. **Use read-only replicas** for reporting queries
4. **Enable SSL/TLS** for all database connections
5. **Implement RLS policies** for multi-tenant data
6. **Audit all sensitive operations** in audit_log table
7. **Encrypt PII** (personally identifiable information)
8. **Use parameterized queries** to prevent SQL injection

---

## Monitoring and Alerting

### Key Metrics

**Database Health:**
- Connection pool utilization
- Query latency (p50, p95, p99)
- Slow query count
- Database size growth
- Index hit ratio

**Application Metrics:**
- Discrepancy detection rate
- Claim approval rate
- Average claim processing time
- Pay calculation accuracy

**Alerts:**
- Connection pool > 80% utilized
- Query latency > 1 second
- Failed migrations
- Discrepancy detection failures
- Claim processing failures

---

## Support and Documentation

**Prisma Documentation:**
- https://www.prisma.io/docs

**Neon Documentation:**
- https://neon.tech/docs

**Neo4j Documentation:**
- https://neo4j.com/docs

**Internal Wiki:**
- [Database Schema Changelog]
- [Emergency Runbook]
- [Query Optimization Guide]

---

## Appendix: Schema Evolution History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-11-20 | Initial schema with 14 tables |

---

**Document Version**: 1.0.0
**Last Updated**: 2024-11-20
**Maintained By**: Avelo Airlines Engineering Team
