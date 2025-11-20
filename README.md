# Avelo Airlines Crew Pay Management System

> Production-ready database architecture for intelligent crew pay management with proactive discrepancy detection and automated claims processing.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Database: Postgres](https://img.shields.io/badge/Database-PostgreSQL-316192.svg)](https://www.postgresql.org/)
[![ORM: Prisma](https://img.shields.io/badge/ORM-Prisma-2D3748.svg)](https://www.prisma.io/)
[![Graph: Neo4j](https://img.shields.io/badge/Graph-Neo4j-008CC1.svg)](https://neo4j.com/)

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Neon Postgres account (https://neon.tech)
- Neo4j Aura account (https://neo4j.com/cloud/aura/)

### Installation

```bash
# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
nano .env

# Generate Prisma Client
npm run db:generate

# Run migrations
npm run db:migrate

# Seed database with sample data
npm run db:seed
```

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Database Schema](#database-schema)
- [Setup Instructions](#setup-instructions)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [Database Management](#database-management)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)

---

## 🎯 Overview

The Avelo Airlines Crew Pay Management System is designed to:

1. **Proactively detect pay discrepancies** before crew members notice them
2. **Automate claims processing** using AI agents with rule interpretation
3. **Ensure FAA and union contract compliance** for all pay calculations
4. **Provide full transparency** with detailed audit trails and explanations

### Key Capabilities

- ✅ **Proactive Detection**: AI agents scan every pay calculation for discrepancies
- ✅ **Auto-Correction**: Minor discrepancies are automatically fixed and reported
- ✅ **Intelligent Claims**: Crew-submitted claims are reviewed by AI with contract knowledge
- ✅ **Compliance Checking**: FAA Part 117 and union contract validation
- ✅ **Transparency**: Detailed explanations for every pay calculation and decision

---

## 🏗️ Architecture

### Hybrid Database Design

```
┌─────────────────────────────────────────────────────────┐
│              APPLICATION LAYER                          │
│        (Prisma ORM + Neo4j Driver)                     │
└─────────────┬──────────────────────┬────────────────────┘
              │                      │
              ▼                      ▼
    ┌──────────────────┐   ┌─────────────────────┐
    │  NEON POSTGRES   │   │  NEO4J KNOWLEDGE   │
    │  (Transactional) │   │  GRAPH (Rules)     │
    └──────────────────┘   └─────────────────────┘
```

**Why Hybrid?**

- **Postgres**: Handles transactional data (crew, flights, pay calculations) with ACID guarantees
- **Neo4j**: Models complex rule relationships (FAA regulations, contract terms, scenarios)

This architecture enables:
- Fast transactional queries for crew operations
- Complex pattern matching for rule interpretation
- Efficient traversal of regulatory relationships
- Conflict resolution between overlapping rules

---

## ✨ Features

### 1. Proactive Discrepancy Detection

```typescript
// AI agent automatically checks every pay calculation
const discrepancy = await detectDiscrepancy({
  crewMemberId: "uuid",
  payPeriodId: "uuid",
  expectedPay: 12000.00,
  actualPay: 11850.00
});

// Auto-fix if within threshold
if (discrepancy.severity === "MEDIUM" && discrepancy.amount < 100) {
  await autoCorrectAndNotify(discrepancy);
}
```

### 2. Automated Claims Processing

```typescript
// AI agent reviews claim with full contract knowledge
const claimReview = await reviewClaim({
  claimId: "CLM-2024-0001",
  flightData: fetchFlightData(),
  contractTerms: queryNeo4j("MATCH (c:ContractTerm)..."),
  faaRules: queryNeo4j("MATCH (r:Rule)...")
});

// Generate detailed rationale
console.log(claimReview.decisionRationale);
// "Per ALPA Section 13.B, delays exceeding 30 minutes due to
//  maintenance are compensated at 50% of hourly rate..."
```

### 3. Complex Pay Calculations

```typescript
// Calculate pay with duty rig, premiums, and guarantees
const pay = await calculatePay({
  crewMemberId: "uuid",
  payPeriodId: "uuid",
  flights: getFlightsForPeriod(),
  rules: {
    dutyRig: "1:3",  // One hour credit per 3 hours duty
    redEyePremium: 1.5,  // 50% premium for 22:00-05:59
    monthlyGuarantee: 70  // Minimum 70 hours
  }
});
```

### 4. Rule Interpretation with Neo4j

```cypher
// Find all applicable rules for a delayed red-eye flight
MATCH (s:Scenario {id: 'delayed_flight_controllable'})
MATCH (r)-[:APPLIES_TO]->(s)
MATCH (s)-[:REQUIRES]->(pc:PayComponent)
RETURN r.code, r.title, pc.type, r.priority
ORDER BY r.priority DESC
```

---

## 🗄️ Database Schema

### Core Tables (14 Total)

| Table | Purpose | Records |
|-------|---------|---------|
| **crew_members** | Crew profiles and employment data | ~500 |
| **flights** | All flight operations | ~50,000/year |
| **crew_assignments** | Links crew to flights | ~150,000/year |
| **pay_periods** | Payroll cycles | ~24/year |
| **pay_calculations** | Computed pay per crew/period | ~12,000/year |
| **discrepancies** | Detected pay issues | ~500/year |
| **claims** | Crew-submitted claims | ~100/year |
| **faa_rules** | FAA Part 117, 121 regulations | ~50 |
| **union_contract_terms** | ALPA, AFA contract terms | ~100 |
| **rule_interpretations** | Complex scenario guidance | ~200 |
| **notifications** | All crew notifications | ~5,000/year |
| **audit_log** | Full audit trail (append-only) | ~100,000/year |

### Entity Relationship Diagram

View the ERD at: https://dbdiagram.io

```bash
# Upload docs/database-erd.dbml to dbdiagram.io
# for interactive visualization
```

---

## 🛠️ Setup Instructions

### 1. Create Neon Postgres Database

1. Sign up at https://neon.tech
2. Create a new project: `crew-copilot-production`
3. Create three branches:
   - `main` (production)
   - `staging`
   - `dev`
4. Enable connection pooling (pgBouncer)
5. Copy connection strings to `.env`

**Connection String Format:**
```
postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/crew_copilot_production?sslmode=require&pgbouncer=true
```

### 2. Create Neo4j Knowledge Graph

1. Sign up at https://neo4j.com/cloud/aura/
2. Create a new instance (Free tier or Professional)
3. Save credentials (username, password, URI)
4. Copy connection details to `.env`

**Connection String Format:**
```
neo4j+s://xxx.databases.neo4j.io
```

### 3. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Neon Postgres
DATABASE_URL="postgresql://user:pass@ep-xxx.aws.neon.tech/crew_copilot_production?sslmode=require&pgbouncer=true"
DIRECT_URL="postgresql://user:pass@ep-xxx.aws.neon.tech/crew_copilot_production?sslmode=require"

# Neo4j
NEO4J_URI="neo4j+s://xxx.databases.neo4j.io"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="your-password"

# Application
NODE_ENV="development"
SERVICE_ROLE_KEY="your-service-key"
AI_AGENT_USER_ID="ai-agent-service-account"
```

### 4. Initialize Databases

```bash
# Install dependencies
npm install

# Generate Prisma Client
npm run db:generate

# Run migrations (creates all tables)
npm run db:migrate

# Seed Postgres with sample data
npm run db:seed

# Load Neo4j schema and seed data
# (Manual step - see Neo4j Setup below)
```

### 5. Load Neo4j Data

Using Neo4j Browser or cypher-shell:

```bash
# Load schema
cat neo4j/schema.cypher | cypher-shell -u neo4j -p <password>

# Load seed data
cat neo4j/seed.cypher | cypher-shell -u neo4j -p <password>

# Verify
cypher-shell -u neo4j -p <password> "MATCH (n) RETURN labels(n), count(*)"
```

---

## 🔧 Environment Configuration

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Pooled Postgres connection | `postgresql://...?pgbouncer=true` |
| `DIRECT_URL` | Direct Postgres connection (migrations) | `postgresql://...` |
| `SHADOW_DATABASE_URL` | Shadow DB for migrations | `postgresql://...shadow` |
| `NEO4J_URI` | Neo4j connection URI | `neo4j+s://xxx.databases.neo4j.io` |
| `NEO4J_USER` | Neo4j username | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j password | `your-password` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NODE_ENV` | Environment | `development` |
| `PORT` | Application port | `3000` |
| `SERVICE_ROLE_KEY` | Service role for RLS bypass | (generated) |

---

## 🚀 Running the Application

### Development

```bash
# Start development server with hot reload
npm run dev

# Open Prisma Studio (database GUI)
npm run db:studio
```

### Production

```bash
# Build application
npm run build

# Run migrations
npm run db:migrate:deploy

# Start production server
npm start
```

---

## 💾 Database Management

### Migrations

```bash
# Create new migration
npm run db:migrate -- --name add_new_field

# Apply migrations to production
npm run db:migrate:deploy

# Reset database (⚠️ DESTRUCTIVE)
npm run db:reset
```

### Seeding

```bash
# Seed database with sample data
npm run db:seed

# The seed script creates:
# - 15 crew members (3 captains, 4 FOs, 8 FAs)
# - 8 flights across 3 bases
# - 4 pay periods
# - 5 FAA rules (Part 117, 121)
# - 7 union contract terms
# - 2 rule interpretations
# - Sample pay calculations, discrepancies, claims
```

### Backup & Restore

```bash
# Backup Postgres
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore Postgres
psql $DATABASE_URL < backup_20241120.sql

# Backup Neo4j
cypher-shell -u neo4j -p password \
  "CALL apoc.export.cypher.all('backup.cypher', {})"

# Restore Neo4j
cypher-shell -u neo4j -p password < backup.cypher
```

### Neon Branching

```bash
# Create a database branch for testing
# (via Neon Console)
neon branches create --parent main --name feature-test

# Point .env to new branch
DATABASE_URL="postgresql://...@ep-feature-test.aws.neon.tech/..."
```

---

## 🧪 Testing

### Database Tests

```bash
# Run database tests
npm run test:db

# The test script verifies:
# - All tables created successfully
# - Foreign key constraints working
# - Indexes created
# - Sample queries execute correctly
# - RLS policies enforced
```

### Performance Tests

```bash
# Test with 10,000 flight assignments
npm run test:performance

# Expected results:
# - Simple queries: < 100ms
# - Complex joins: < 500ms
# - Bulk calculations: < 30s for 1,000 crew
# - Discrepancy detection: < 5 min for full pay period
```

### Sample Queries

```typescript
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

// Get crew member's pay history
const payHistory = await prisma.payCalculation.findMany({
  where: { crewMemberId: "uuid" },
  include: { payPeriod: true },
  orderBy: { calculationDate: 'desc' },
  take: 12
});

// Find unresolved discrepancies
const openDiscrepancies = await prisma.discrepancy.findMany({
  where: {
    resolutionStatus: { in: ['OPEN', 'INVESTIGATING'] }
  },
  include: { crewMember: true, flight: true },
  orderBy: { severity: 'desc' }
});

// Get claims pending review
const pendingClaims = await prisma.claim.findMany({
  where: { status: 'UNDER_REVIEW' },
  include: { crewMember: true, payPeriod: true }
});
```

---

## 📚 Documentation

### Architecture & Design

- [Database Schema Documentation](docs/database-schema.md)
- [Entity Relationship Diagram](docs/database-erd.dbml)

### API Documentation

- Prisma Schema: [prisma/schema.prisma](prisma/schema.prisma)
- Neo4j Schema: [neo4j/schema.cypher](neo4j/schema.cypher)

### External Resources

- [Prisma Documentation](https://www.prisma.io/docs)
- [Neon Documentation](https://neon.tech/docs)
- [Neo4j Documentation](https://neo4j.com/docs)

---

## 🔐 Security

### Row-Level Security (RLS)

RLS policies ensure data isolation:

- **Crew Members**: Can only view their own pay, claims, and notifications
- **Administrators**: Full access to all data
- **AI Agents**: Service role access for automated operations
- **Audit Log**: Append-only, no updates or deletes

### Best Practices

1. ✅ Never commit `.env` files
2. ✅ Rotate database credentials quarterly
3. ✅ Use read-only replicas for reporting
4. ✅ Enable SSL/TLS for all connections
5. ✅ Audit all sensitive operations
6. ✅ Use parameterized queries (Prisma handles this)

---

## 🚦 Monitoring

### Key Metrics

- Connection pool utilization
- Query latency (p50, p95, p99)
- Discrepancy detection rate
- Claim approval rate
- Database size growth

### Logging

All operations are logged to `audit_log` table with:
- Entity type and ID
- Action performed
- Actor (user, admin, AI agent)
- Before/after changes (JSONB)
- Timestamp and IP address

---

## 🤝 Contributing

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test
3. Run migrations: `npm run db:migrate`
4. Commit with clear message
5. Push and create pull request

### Schema Changes

All schema changes must go through Prisma Migrate:

```bash
# Edit prisma/schema.prisma
nano prisma/schema.prisma

# Create migration
npm run db:migrate -- --name your_migration_name

# Review migration in prisma/migrations/
# Commit migration files with your changes
```

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙋 Support

### Issues

Report issues at: [GitHub Issues](https://github.com/avelo-airlines/crew-pay/issues)

### Documentation

- [Database Schema Docs](docs/database-schema.md)
- [ERD Diagram](docs/database-erd.dbml)

### Contact

For questions about the system:
- Technical: engineering@aveloair.com
- Payroll: payroll@aveloair.com

---

## 🎯 Roadmap

- [ ] Real-time sync with flight operations system
- [ ] Mobile app for crew claims submission
- [ ] Advanced analytics dashboard
- [ ] Machine learning for discrepancy prediction
- [ ] Integration with accounting systems
- [ ] Multi-currency support for international crews

---

**Built with ❤️ by Avelo Airlines Engineering Team**
