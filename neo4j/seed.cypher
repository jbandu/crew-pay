// ============================================================================
// AVELO AIRLINES CREW PAY MANAGEMENT SYSTEM
// Neo4j Knowledge Graph Seed Data
// ============================================================================

// ============================================================================
// 1. CREATE FAA RULES
// ============================================================================

// Part 117 Flight Duty Period Limits
CREATE (fdp:Rule {
  code: 'Part117.23',
  category: 'FDP_limits',
  title: 'Flight Duty Period: Unaugmented Operations',
  text: 'Except as provided for in §117.15, no certificate holder may assign and no flightcrew member may accept an assignment if the scheduled flight duty period will exceed the limits specified in Table B of this part.',
  effectiveDate: datetime('2014-01-04'),
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
  priority: 10,
  maxFDP: {
    '1-2_segments': {
      '0500-0559': 14, '0600-0659': 14, '0700-1159': 13,
      '1200-1259': 12, '1300-1659': 12, '1700-2159': 12,
      '2200-2259': 11, '2300-0459': 10
    },
    '3_segments': {
      '0500-0559': 13, '0600-0659': 13, '0700-1159': 12,
      '1200-1259': 12, '1300-1659': 11, '1700-2159': 11,
      '2200-2259': 10, '2300-0459': 9
    }
  }
});

// Part 117 Rest Requirements
CREATE (rest:Rule {
  code: 'Part117.25',
  category: 'rest_requirements',
  title: 'Rest Period',
  text: 'No certificate holder may assign and no flightcrew member may accept assignment to any reserve or flight duty period unless the flightcrew member is given a rest period of at least 30 consecutive hours in the 168 consecutive hour period that precedes the completion of the assignment.',
  effectiveDate: datetime('2014-01-04'),
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
  priority: 10,
  minimumRestHours: 30,
  windowHours: 168
});

// Part 117 Flight Time Limits
CREATE (ftl:Rule {
  code: 'Part117.11',
  category: 'flight_time_limits',
  title: 'Flight Time Limitation',
  text: 'No certificate holder may schedule and no flightcrew member may accept an assignment if the total flight time will exceed: (1) 100 hours in any 672 consecutive hours; (2) 1,000 hours in any 365 consecutive calendar day period.',
  effectiveDate: datetime('2014-01-04'),
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
  priority: 10,
  limits: {
    '28_days': 100,
    '365_days': 1000
  }
});

// Part 117 FDP Extensions
CREATE (fdpExt:Rule {
  code: 'Part117.19',
  category: 'FDP_extensions',
  title: 'Flight Duty Period Extensions',
  text: 'For augmented and unaugmented operations, if unforeseen operational circumstances arise prior to takeoff, the pilot in command and the certificate holder may extend the maximum flight duty period up to 2 hours.',
  effectiveDate: datetime('2014-01-04'),
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
  priority: 8,
  maxExtensionHours: 2,
  requiresPICApproval: true
});

// Part 121.467 Flight Attendant Duty Limits
CREATE (faDuty:Rule {
  code: 'Part121.467',
  category: 'FA_duty_limits',
  title: 'Flight Attendant Duty Period Limitations',
  text: 'No certificate holder may schedule a flight attendant for a duty period of more than 14 hours. Each flight attendant must be relieved from all duty for at least 24 consecutive hours during any 7 consecutive calendar days.',
  effectiveDate: datetime('1995-03-20'),
  appliesTo: ['FLIGHT_ATTENDANT'],
  priority: 10,
  maxDutyHours: 14,
  minRestIn7Days: 24
});

// ============================================================================
// 2. CREATE UNION CONTRACT TERMS
// ============================================================================

// Monthly Guarantee - Pilots
CREATE (pilotGuarantee:ContractTerm {
  code: 'ALPA_Section_5.A',
  category: 'guarantee',
  title: 'Monthly Guarantee - Pilots',
  text: 'All pilots shall be guaranteed a minimum of 70 credit hours per calendar month, or the prorated amount for partial months.',
  formula: {
    type: 'monthly_guarantee',
    hours: 70,
    proration: 'calendar_days'
  },
  effectiveDate: datetime('2023-01-01'),
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
  priority: 9
});

// Monthly Guarantee - Flight Attendants
CREATE (faGuarantee:ContractTerm {
  code: 'AFA_Section_7.B',
  category: 'guarantee',
  title: 'Monthly Guarantee - Flight Attendants',
  text: 'All flight attendants shall be guaranteed a minimum of 75 credit hours per calendar month.',
  formula: {
    type: 'monthly_guarantee',
    hours: 75,
    proration: 'calendar_days'
  },
  effectiveDate: datetime('2023-01-01'),
  appliesTo: ['FLIGHT_ATTENDANT'],
  priority: 9
});

// Red-Eye Premium
CREATE (redEye:ContractTerm {
  code: 'ALPA_Section_12.C',
  category: 'premium',
  title: 'Red-Eye Premium',
  text: 'Flights departing between 22:00 and 05:59 local time shall receive a 50% premium on the applicable hourly rate for all hours flown during that period.',
  formula: {
    type: 'premium_multiplier',
    multiplier: 1.5,
    timeRange: {
      start: '22:00',
      end: '05:59'
    }
  },
  effectiveDate: datetime('2023-01-01'),
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER', 'FLIGHT_ATTENDANT'],
  priority: 7
});

// Duty Rig
CREATE (dutyRig:ContractTerm {
  code: 'ALPA_Section_6.E',
  category: 'rig',
  title: 'Duty Rig',
  text: 'Pilots shall be credited with the greater of actual flight time or one hour for every three hours of duty time (1:3 duty rig).',
  formula: {
    type: 'rig',
    ratio: 3,
    comparison: 'greater_of'
  },
  effectiveDate: datetime('2023-01-01'),
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
  priority: 8
});

// Per Diem - Pilots
CREATE (pilotPerDiem:ContractTerm {
  code: 'ALPA_Section_8.D',
  category: 'per_diem',
  title: 'Per Diem - Domestic',
  text: 'Pilots shall receive $2.50 per hour for all duty time away from base, calculated from check-in to check-out.',
  formula: {
    type: 'per_diem',
    rate: 2.50,
    calculation: 'duty_hours'
  },
  effectiveDate: datetime('2023-01-01'),
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
  priority: 5
});

// Per Diem - Flight Attendants
CREATE (faPerDiem:ContractTerm {
  code: 'AFA_Section_9.A',
  category: 'per_diem',
  title: 'Per Diem - Flight Attendants',
  text: 'Flight attendants shall receive $2.25 per hour for all duty time away from base.',
  formula: {
    type: 'per_diem',
    rate: 2.25,
    calculation: 'duty_hours'
  },
  effectiveDate: datetime('2023-01-01'),
  appliesTo: ['FLIGHT_ATTENDANT'],
  priority: 5
});

// Overtime
CREATE (overtime:ContractTerm {
  code: 'ALPA_Section_10.A',
  category: 'overtime',
  title: 'Overtime Pay',
  text: 'All credit hours in excess of 70 hours in a calendar month shall be compensated at 150% of the applicable hourly rate.',
  formula: {
    type: 'overtime',
    threshold: 70,
    multiplier: 1.5
  },
  effectiveDate: datetime('2023-01-01'),
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
  priority: 6
});

// Delay Pay
CREATE (delayPay:ContractTerm {
  code: 'ALPA_Section_13.B',
  category: 'delay_pay',
  title: 'Delay Pay',
  text: 'Delays exceeding 30 minutes due to maintenance or other controllable factors shall be compensated at 50% of the hourly rate for the delay period.',
  formula: {
    type: 'delay_compensation',
    threshold_minutes: 30,
    multiplier: 0.5,
    eligible_codes: ['MX', 'OPS', 'CREW']
  },
  effectiveDate: datetime('2023-01-01'),
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER', 'FLIGHT_ATTENDANT'],
  priority: 7
});

// ============================================================================
// 3. CREATE PAY COMPONENTS
// ============================================================================

CREATE (flightPay:PayComponent {
  type: 'flight_pay',
  description: 'Base pay for flight hours',
  calculationMethod: 'credit_hours * hourly_rate',
  baseFormula: 'max(block_time, duty_rig_credit)',
  priority: 1
});

CREATE (overtimePay:PayComponent {
  type: 'overtime',
  description: 'Premium pay for hours over monthly guarantee',
  calculationMethod: '(credit_hours - guarantee) * hourly_rate * 1.5',
  baseFormula: 'if credit_hours > guarantee then (credit_hours - guarantee) * rate * 1.5',
  priority: 2
});

CREATE (perDiemPay:PayComponent {
  type: 'per_diem',
  description: 'Expense allowance for time away from base',
  calculationMethod: 'duty_hours * per_diem_rate',
  baseFormula: '(checkout_time - checkin_time) * rate',
  priority: 3
});

CREATE (premiumPay:PayComponent {
  type: 'premium',
  description: 'Additional pay for red-eye, holiday, or international flights',
  calculationMethod: 'qualifying_hours * hourly_rate * premium_multiplier',
  baseFormula: 'hours_in_premium_window * rate * multiplier',
  priority: 4
});

CREATE (delayPayComp:PayComponent {
  type: 'delay_pay',
  description: 'Compensation for controllable delays',
  calculationMethod: '(delay_minutes / 60) * hourly_rate * 0.5',
  baseFormula: 'if delay > 30min and eligible then delay_hours * rate * 0.5',
  priority: 5
});

CREATE (guaranteePay:PayComponent {
  type: 'guarantee',
  description: 'Minimum monthly pay guarantee',
  calculationMethod: 'max(actual_credit_hours, guarantee_hours) * hourly_rate',
  baseFormula: 'guarantee_hours * rate if credit_hours < guarantee',
  priority: 6
});

// ============================================================================
// 4. CREATE SCENARIOS
// ============================================================================

CREATE (normalFlight:Scenario {
  id: 'normal_flight',
  description: 'Standard flight with no delays or premiums',
  complexity: 'Simple',
  tags: ['routine', 'daytime', 'domestic'],
  exampleCalculation: {
    block_time: 2.5,
    duty_time: 4.0,
    credit_hours: 2.5,
    components: ['flight_pay', 'per_diem']
  }
});

CREATE (delayedFlight:Scenario {
  id: 'delayed_flight_controllable',
  description: 'Flight delayed due to maintenance or controllable factors',
  complexity: 'Moderate',
  tags: ['delay', 'maintenance', 'compensation'],
  exampleCalculation: {
    block_time: 2.5,
    delay_minutes: 45,
    duty_time: 4.75,
    credit_hours: 2.5,
    delay_pay: 0.375,
    components: ['flight_pay', 'delay_pay', 'per_diem']
  }
});

CREATE (redEyeFlight:Scenario {
  id: 'red_eye_flight',
  description: 'Overnight flight departing 22:00-05:59',
  complexity: 'Moderate',
  tags: ['red_eye', 'premium', 'overnight'],
  exampleCalculation: {
    block_time: 3.0,
    duty_time: 5.0,
    credit_hours: 3.0,
    premium_hours: 3.0,
    components: ['flight_pay', 'premium', 'per_diem']
  }
});

CREATE (longDutyDay:Scenario {
  id: 'long_duty_day',
  description: 'Extended duty day approaching FDP limits',
  complexity: 'Complex',
  tags: ['extended_duty', 'fdp_limit', 'fatigue'],
  exampleCalculation: {
    block_time: 8.0,
    duty_time: 13.5,
    credit_hours: 8.0,
    fdp_check: 'required',
    components: ['flight_pay', 'per_diem', 'duty_rig']
  }
});

CREATE (guaranteeShortfall:Scenario {
  id: 'guarantee_shortfall',
  description: 'Monthly credit hours below guarantee',
  complexity: 'Simple',
  tags: ['guarantee', 'minimum_pay'],
  exampleCalculation: {
    actual_hours: 65,
    guarantee_hours: 70,
    shortfall: 5,
    components: ['guarantee', 'flight_pay']
  }
});

CREATE (overtimeMonth:Scenario {
  id: 'overtime_month',
  description: 'Credit hours exceed monthly guarantee',
  complexity: 'Moderate',
  tags: ['overtime', 'high_utilization'],
  exampleCalculation: {
    actual_hours: 85,
    guarantee_hours: 70,
    overtime_hours: 15,
    components: ['flight_pay', 'overtime', 'per_diem']
  }
});

// ============================================================================
// 5. CREATE RELATIONSHIPS - RULE APPLICATIONS
// ============================================================================

// FDP limits apply to long duty days
MATCH (r:Rule {code: 'Part117.23'}), (s:Scenario {id: 'long_duty_day'})
CREATE (r)-[:APPLIES_TO {
  priority: 10,
  conditions: {check: 'duty_period_hours', threshold: 12},
  enforcement: 'hard_limit'
}]->(s);

// Rest requirements apply to all flight scenarios
MATCH (r:Rule {code: 'Part117.25'}), (s:Scenario)
WHERE s.id IN ['normal_flight', 'delayed_flight_controllable', 'red_eye_flight', 'long_duty_day']
CREATE (r)-[:APPLIES_TO {
  priority: 10,
  conditions: {check: 'prior_168_hours', minimum_rest: 30},
  enforcement: 'hard_limit'
}]->(s);

// FDP extensions apply to delayed flights
MATCH (r:Rule {code: 'Part117.19'}), (s:Scenario {id: 'delayed_flight_controllable'})
CREATE (r)-[:APPLIES_TO {
  priority: 8,
  conditions: {requires: 'PIC_approval', max_extension: 2},
  exceptions: {weather: 'allowed', maintenance: 'allowed'}
}]->(s);

// Duty rig applies to all pilot scenarios
MATCH (c:ContractTerm {code: 'ALPA_Section_6.E'}), (s:Scenario)
WHERE s.id IN ['normal_flight', 'delayed_flight_controllable', 'long_duty_day']
CREATE (c)-[:APPLIES_TO {
  priority: 8,
  conditions: {calculate: 'greater_of', comparison: ['block_time', 'duty_time/3']},
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER']
}]->(s);

// Red-eye premium applies to red-eye flights
MATCH (c:ContractTerm {code: 'ALPA_Section_12.C'}), (s:Scenario {id: 'red_eye_flight'})
CREATE (c)-[:APPLIES_TO {
  priority: 7,
  conditions: {departure_time: {start: '22:00', end: '05:59'}},
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER', 'FLIGHT_ATTENDANT']
}]->(s);

// Delay pay applies to delayed flights
MATCH (c:ContractTerm {code: 'ALPA_Section_13.B'}), (s:Scenario {id: 'delayed_flight_controllable'})
CREATE (c)-[:APPLIES_TO {
  priority: 7,
  conditions: {delay_minutes: {threshold: 30}, delay_codes: ['MX', 'OPS', 'CREW']},
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER', 'FLIGHT_ATTENDANT']
}]->(s);

// Guarantee applies to shortfall scenarios
MATCH (c:ContractTerm {code: 'ALPA_Section_5.A'}), (s:Scenario {id: 'guarantee_shortfall'})
CREATE (c)-[:APPLIES_TO {
  priority: 9,
  conditions: {monthly_hours: {less_than: 70}},
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER']
}]->(s);

// Overtime applies to high-hour months
MATCH (c:ContractTerm {code: 'ALPA_Section_10.A'}), (s:Scenario {id: 'overtime_month'})
CREATE (c)-[:APPLIES_TO {
  priority: 6,
  conditions: {monthly_hours: {greater_than: 70}},
  appliesTo: ['CAPTAIN', 'FIRST_OFFICER']
}]->(s);

// ============================================================================
// 6. CREATE RELATIONSHIPS - PAY COMPONENT REQUIREMENTS
// ============================================================================

// Normal flight requires flight pay and per diem
MATCH (s:Scenario {id: 'normal_flight'}), (p:PayComponent)
WHERE p.type IN ['flight_pay', 'per_diem']
CREATE (s)-[:REQUIRES {mandatory: true}]->(p);

// Delayed flight requires flight pay, delay pay, and per diem
MATCH (s:Scenario {id: 'delayed_flight_controllable'}), (p:PayComponent {type: 'flight_pay'})
CREATE (s)-[:REQUIRES {mandatory: true}]->(p);

MATCH (s:Scenario {id: 'delayed_flight_controllable'}), (p:PayComponent {type: 'delay_pay'})
CREATE (s)-[:REQUIRES {
  mandatory: true,
  conditions: {delay_minutes: {greater_than: 30}}
}]->(p);

MATCH (s:Scenario {id: 'delayed_flight_controllable'}), (p:PayComponent {type: 'per_diem'})
CREATE (s)-[:REQUIRES {mandatory: true}]->(p);

// Red-eye flight requires flight pay, premium, and per diem
MATCH (s:Scenario {id: 'red_eye_flight'}), (p:PayComponent)
WHERE p.type IN ['flight_pay', 'premium', 'per_diem']
CREATE (s)-[:REQUIRES {mandatory: true}]->(p);

// Guarantee shortfall requires guarantee payment
MATCH (s:Scenario {id: 'guarantee_shortfall'}), (p:PayComponent {type: 'guarantee'})
CREATE (s)-[:REQUIRES {mandatory: true}]->(p);

// Overtime month requires overtime payment
MATCH (s:Scenario {id: 'overtime_month'}), (p:PayComponent {type: 'overtime'})
CREATE (s)-[:REQUIRES {
  mandatory: true,
  conditions: {credit_hours: {greater_than: 70}}
}]->(p);

// ============================================================================
// 7. CREATE RELATIONSHIPS - PAY COMPONENT DEPENDENCIES
// ============================================================================

// Overtime depends on flight pay calculation
MATCH (p1:PayComponent {type: 'overtime'}), (p2:PayComponent {type: 'flight_pay'})
CREATE (p1)-[:DEPENDS_ON {
  dependencyType: 'input',
  formula: 'requires credit_hours from flight_pay'
}]->(p2);

// Guarantee depends on flight pay calculation
MATCH (p1:PayComponent {type: 'guarantee'}), (p2:PayComponent {type: 'flight_pay'})
CREATE (p1)-[:DEPENDS_ON {
  dependencyType: 'prerequisite',
  formula: 'compare credit_hours to guarantee_hours'
}]->(p2);

// Premium modifies flight pay
MATCH (p1:PayComponent {type: 'premium'}), (p2:PayComponent {type: 'flight_pay'})
CREATE (p1)-[:DEPENDS_ON {
  dependencyType: 'modifier',
  formula: 'multiplies base_rate for qualifying hours'
}]->(p2);

// ============================================================================
// 8. CREATE RULE SUPERSESSION RELATIONSHIPS
// ============================================================================

// Example: If Part 117 superseded an older rule (hypothetical)
// CREATE (new:Rule {code: 'Part117.23', ...})
// CREATE (old:Rule {code: 'Part121.471', ...})
// MATCH (new), (old)
// CREATE (new)-[:SUPERSEDES {
//   effectiveDate: datetime('2014-01-04'),
//   reason: 'FAA modernization of flight and duty time regulations'
// }]->(old);

// ============================================================================
// 9. CREATE RULE CONFLICTS (for conflict resolution testing)
// ============================================================================

// Example: FDP limit vs. operational extension
// In practice, Part 117.19 allows exceptions to Part 117.23
MATCH (ext:Rule {code: 'Part117.19'}), (limit:Rule {code: 'Part117.23'})
CREATE (ext)-[:MODIFIES {
  resolutionMethod: 'conditional_override',
  notes: 'Extension allowed up to 2 hours with PIC approval for unforeseen circumstances'
}]->(limit);

// ============================================================================
// VERIFICATION QUERIES
// ============================================================================

// Count nodes
// MATCH (n) RETURN labels(n) as Type, count(*) as Count;

// Count relationships
// MATCH ()-[r]->() RETURN type(r) as Relationship, count(*) as Count;

// View all scenarios with their required pay components
// MATCH (s:Scenario)-[:REQUIRES]->(p:PayComponent)
// RETURN s.id, s.description, collect(p.type) as required_components;

// View all rules applying to a specific scenario
// MATCH (r)-[:APPLIES_TO]->(s:Scenario {id: 'delayed_flight_controllable'})
// RETURN r.code, r.title, r.priority ORDER BY r.priority DESC;

// Find pay component dependencies
// MATCH (p1:PayComponent)-[d:DEPENDS_ON]->(p2:PayComponent)
// RETURN p1.type, d.dependencyType, p2.type;
