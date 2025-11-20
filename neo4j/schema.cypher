// ============================================================================
// AVELO AIRLINES CREW PAY MANAGEMENT SYSTEM
// Neo4j Knowledge Graph Schema
// ============================================================================
// Purpose: Model complex regulatory and contractual relationships for
// intelligent pay calculation and compliance checking
// ============================================================================

// ============================================================================
// CONSTRAINTS & INDEXES
// ============================================================================

// Unique constraints ensure data integrity
CREATE CONSTRAINT rule_code_unique IF NOT EXISTS
FOR (r:Rule) REQUIRE r.code IS UNIQUE;

CREATE CONSTRAINT contract_term_code_unique IF NOT EXISTS
FOR (c:ContractTerm) REQUIRE c.code IS UNIQUE;

CREATE CONSTRAINT scenario_id_unique IF NOT EXISTS
FOR (s:Scenario) REQUIRE s.id IS UNIQUE;

CREATE CONSTRAINT pay_component_type_unique IF NOT EXISTS
FOR (p:PayComponent) REQUIRE p.type IS UNIQUE;

CREATE CONSTRAINT crew_member_employee_id_unique IF NOT EXISTS
FOR (cm:CrewMember) REQUIRE cm.employeeId IS UNIQUE;

CREATE CONSTRAINT flight_id_unique IF NOT EXISTS
FOR (f:Flight) REQUIRE f.id IS UNIQUE;

// Indexes for performance
CREATE INDEX rule_category_idx IF NOT EXISTS
FOR (r:Rule) ON (r.category);

CREATE INDEX contract_category_idx IF NOT EXISTS
FOR (c:ContractTerm) ON (c.category);

CREATE INDEX scenario_complexity_idx IF NOT EXISTS
FOR (s:Scenario) ON (s.complexity);

CREATE INDEX crew_position_idx IF NOT EXISTS
FOR (cm:CrewMember) ON (cm.position);

// ============================================================================
// NODE LABELS
// ============================================================================

// Rule: FAA regulations and union contract terms
// Properties:
//   - code: Unique identifier (e.g., "Part117.23")
//   - category: Type of rule (FDP_limits, rest_requirements, etc.)
//   - title: Human-readable title
//   - text: Full regulation text
//   - effectiveDate: When the rule became active
//   - appliesTo: Array of crew positions
//   - priority: Conflict resolution priority (1-10)

// ContractTerm: Specific union agreement terms
// Properties:
//   - code: Unique identifier (e.g., "ALPA_Section_5.A")
//   - category: Type of term (guarantee, premium, rig, etc.)
//   - title: Human-readable title
//   - text: Full contract language
//   - formula: Calculation formula (JSON)
//   - effectiveDate: When the term became active
//   - appliesTo: Array of crew positions

// Scenario: Specific pay calculation situations
// Properties:
//   - id: Unique identifier
//   - description: What this scenario represents
//   - complexity: Simple, Moderate, Complex, Expert
//   - tags: Array of descriptive tags
//   - exampleCalculation: Sample calculation (JSON)

// PayComponent: Types of pay (flight_pay, overtime, per_diem, etc.)
// Properties:
//   - type: Component identifier
//   - description: What this component represents
//   - calculationMethod: How it's calculated
//   - baseFormula: Mathematical formula

// CrewMember: Digital twin of crew member
// Properties:
//   - id: UUID from Postgres
//   - employeeId: Employee number
//   - position: Crew position
//   - baseLocation: Home base
//   - seniorityNumber: Seniority ranking
//   - unionStatus: Union membership status

// Flight: Digital twin of flight
// Properties:
//   - id: UUID from Postgres
//   - flightNumber: Flight identifier
//   - origin: Origin airport
//   - destination: Destination airport
//   - scheduledDeparture: Scheduled departure time
//   - actualDeparture: Actual departure time
//   - blockTime: Flight duration in hours

// ============================================================================
// RELATIONSHIP TYPES
// ============================================================================

// APPLIES_TO: Rule/ContractTerm applies to a Scenario
// Properties:
//   - priority: Application priority (1-10)
//   - conditions: When this applies (JSON)
//   - exceptions: When this doesn't apply (JSON)

// REQUIRES: Scenario requires a PayComponent
// Properties:
//   - mandatory: Boolean
//   - conditions: When this is required (JSON)

// CONFLICTS_WITH: Rule conflicts with another Rule
// Properties:
//   - resolutionMethod: How to resolve ("most_restrictive", "most_recent", etc.)
//   - notes: Explanation of conflict

// SUPERSEDES: Rule replaces another Rule
// Properties:
//   - effectiveDate: When supersession took effect
//   - reason: Why it was superseded

// EXEMPTS: Rule provides exemption from Scenario
// Properties:
//   - conditions: When exemption applies
//   - scope: Full or partial exemption

// CALCULATES: PayComponent calculates using a formula
// Properties:
//   - formula: Calculation formula
//   - inputs: Required inputs
//   - outputs: Expected outputs

// ASSIGNED_TO: Flight assigned to CrewMember
// Properties:
//   - position: Operating, deadhead, reserve
//   - dutyStart: Duty start time
//   - dutyEnd: Duty end time
//   - checkIn: Check-in time
//   - checkOut: Check-out time

// FLEW: CrewMember flew on Flight
// Properties:
//   - creditHours: Credit hours earned
//   - dutyHours: Duty hours worked
//   - blockTime: Block time
//   - perDiemHours: Per diem eligible hours

// TRIGGERS: Scenario triggers PayComponent calculation
// Properties:
//   - conditions: Triggering conditions
//   - calculationPriority: Order of calculation

// DEPENDS_ON: PayComponent depends on another PayComponent
// Properties:
//   - dependencyType: "input", "modifier", "prerequisite"
//   - formula: How dependency is used

// ============================================================================
// EXAMPLE GRAPH PATTERN
// ============================================================================

// Pattern for complex pay scenario:
//
// (Rule:FAA)-[:APPLIES_TO]->(Scenario:LongDutyDay)
// (ContractTerm:DutyRig)-[:APPLIES_TO]->(Scenario)
// (Scenario)-[:REQUIRES]->(PayComponent:FlightPay)
// (Scenario)-[:TRIGGERS]->(PayComponent:DelayPay)
// (PayComponent:FlightPay)-[:DEPENDS_ON]->(PayComponent:DutyRig)
// (CrewMember)-[:FLEW]->(Flight)
// (Flight)-[:MATCHES]->(Scenario)

// ============================================================================
// QUERY PATTERNS
// ============================================================================

// Pattern 1: Find all rules applicable to a scenario
// MATCH (r:Rule)-[:APPLIES_TO]->(s:Scenario {id: $scenarioId})
// RETURN r ORDER BY r.priority DESC

// Pattern 2: Calculate pay for a specific flight
// MATCH (cm:CrewMember {employeeId: $employeeId})-[flew:FLEW]->(f:Flight {id: $flightId})
// MATCH (f)-[:MATCHES]->(s:Scenario)-[:TRIGGERS]->(pc:PayComponent)
// RETURN pc, flew, s

// Pattern 3: Find conflicting rules
// MATCH (r1:Rule)-[c:CONFLICTS_WITH]->(r2:Rule)
// WHERE r1.appliesTo CONTAINS $position
// RETURN r1, c, r2

// Pattern 4: Trace rule interpretation path
// MATCH path = (r:Rule)-[:APPLIES_TO*]->(s:Scenario)-[:REQUIRES]->(pc:PayComponent)
// WHERE r.code = $ruleCode
// RETURN path

// Pattern 5: Find all pay components for a crew member's duties
// MATCH (cm:CrewMember {employeeId: $employeeId})-[:FLEW]->(f:Flight)
// MATCH (f)-[:MATCHES]->(s:Scenario)-[:TRIGGERS]->(pc:PayComponent)
// RETURN DISTINCT pc.type, collect(f.flightNumber) as flights

// ============================================================================
// NOTES
// ============================================================================

// This schema is designed to support:
// 1. Complex rule interpretation with conflict resolution
// 2. Multi-step pay calculation workflows
// 3. Intelligent scenario matching for edge cases
// 4. Compliance checking against FAA and union rules
// 5. Historical rule tracking (supersession)
// 6. Explanation of pay calculations (graph traversal)
//
// The knowledge graph complements the Postgres transactional database by
// providing:
// - Fast traversal of complex rule relationships
// - Pattern matching for scenario identification
// - Conflict resolution logic
// - Historical rule evolution tracking
