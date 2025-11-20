import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting database seeding...\n');

  // ============================================================================
  // 1. CREATE CREW MEMBERS
  // ============================================================================
  console.log('👥 Creating crew members...');

  const crews = await Promise.all([
    // Captains
    prisma.crewMember.create({
      data: {
        employeeId: 'XP001',
        firstName: 'Sarah',
        lastName: 'Mitchell',
        position: 'CAPTAIN',
        baseLocation: 'BUR',
        hireDate: new Date('2019-03-15'),
        seniorityNumber: 1,
        baseHourlyRate: 165.50,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP002',
        firstName: 'Michael',
        lastName: 'Chen',
        position: 'CAPTAIN',
        baseLocation: 'IFP',
        hireDate: new Date('2019-08-22'),
        seniorityNumber: 2,
        baseHourlyRate: 162.75,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP003',
        firstName: 'James',
        lastName: 'Rodriguez',
        position: 'CAPTAIN',
        baseLocation: 'HVN',
        hireDate: new Date('2020-01-10'),
        seniorityNumber: 3,
        baseHourlyRate: 158.25,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),

    // First Officers
    prisma.crewMember.create({
      data: {
        employeeId: 'XP101',
        firstName: 'Emily',
        lastName: 'Johnson',
        position: 'FIRST_OFFICER',
        baseLocation: 'BUR',
        hireDate: new Date('2020-06-15'),
        seniorityNumber: 10,
        baseHourlyRate: 98.50,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP102',
        firstName: 'David',
        lastName: 'Thompson',
        position: 'FIRST_OFFICER',
        baseLocation: 'IFP',
        hireDate: new Date('2020-09-01'),
        seniorityNumber: 11,
        baseHourlyRate: 96.75,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP103',
        firstName: 'Jennifer',
        lastName: 'Martinez',
        position: 'FIRST_OFFICER',
        baseLocation: 'BUR',
        hireDate: new Date('2021-02-15'),
        seniorityNumber: 12,
        baseHourlyRate: 94.25,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP104',
        firstName: 'Robert',
        lastName: 'Williams',
        position: 'FIRST_OFFICER',
        baseLocation: 'HVN',
        hireDate: new Date('2021-07-01'),
        seniorityNumber: 13,
        baseHourlyRate: 92.50,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),

    // Flight Attendants
    prisma.crewMember.create({
      data: {
        employeeId: 'XP201',
        firstName: 'Amanda',
        lastName: 'Davis',
        position: 'FLIGHT_ATTENDANT',
        baseLocation: 'BUR',
        hireDate: new Date('2021-03-20'),
        seniorityNumber: 20,
        baseHourlyRate: 28.50,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP202',
        firstName: 'Jessica',
        lastName: 'Brown',
        position: 'FLIGHT_ATTENDANT',
        baseLocation: 'IFP',
        hireDate: new Date('2021-05-15'),
        seniorityNumber: 21,
        baseHourlyRate: 27.75,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP203',
        firstName: 'Christopher',
        lastName: 'Taylor',
        position: 'FLIGHT_ATTENDANT',
        baseLocation: 'HVN',
        hireDate: new Date('2021-08-01'),
        seniorityNumber: 22,
        baseHourlyRate: 27.25,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP204',
        firstName: 'Ashley',
        lastName: 'Anderson',
        position: 'FLIGHT_ATTENDANT',
        baseLocation: 'BUR',
        hireDate: new Date('2022-01-10'),
        seniorityNumber: 23,
        baseHourlyRate: 26.50,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP205',
        firstName: 'Matthew',
        lastName: 'Wilson',
        position: 'FLIGHT_ATTENDANT',
        baseLocation: 'IFP',
        hireDate: new Date('2022-04-15'),
        seniorityNumber: 24,
        baseHourlyRate: 26.00,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP206',
        firstName: 'Nicole',
        lastName: 'Moore',
        position: 'FLIGHT_ATTENDANT',
        baseLocation: 'HVN',
        hireDate: new Date('2022-07-01'),
        seniorityNumber: 25,
        baseHourlyRate: 25.75,
        unionStatus: 'UNION_MEMBER',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP207',
        firstName: 'Ryan',
        lastName: 'Jackson',
        position: 'FLIGHT_ATTENDANT',
        baseLocation: 'BUR',
        hireDate: new Date('2022-10-01'),
        seniorityNumber: 26,
        baseHourlyRate: 25.50,
        unionStatus: 'PROBATIONARY',
        contractType: 'FULL_TIME',
      },
    }),
    prisma.crewMember.create({
      data: {
        employeeId: 'XP208',
        firstName: 'Lauren',
        lastName: 'White',
        position: 'FLIGHT_ATTENDANT',
        baseLocation: 'IFP',
        hireDate: new Date('2023-01-15'),
        seniorityNumber: 27,
        baseHourlyRate: 25.25,
        unionStatus: 'PROBATIONARY',
        contractType: 'FULL_TIME',
      },
    }),
  ]);

  console.log(`✅ Created ${crews.length} crew members\n`);

  // ============================================================================
  // 2. CREATE PAY PERIODS
  // ============================================================================
  console.log('📅 Creating pay periods...');

  const payPeriods = await Promise.all([
    prisma.payPeriod.create({
      data: {
        startDate: new Date('2024-01-01'),
        endDate: new Date('2024-01-15'),
        payDate: new Date('2024-01-20'),
        status: 'PAID',
      },
    }),
    prisma.payPeriod.create({
      data: {
        startDate: new Date('2024-01-16'),
        endDate: new Date('2024-01-31'),
        payDate: new Date('2024-02-05'),
        status: 'PAID',
      },
    }),
    prisma.payPeriod.create({
      data: {
        startDate: new Date('2024-02-01'),
        endDate: new Date('2024-02-15'),
        payDate: new Date('2024-02-20'),
        status: 'CLOSED',
      },
    }),
    prisma.payPeriod.create({
      data: {
        startDate: new Date('2024-02-16'),
        endDate: new Date('2024-02-29'),
        payDate: new Date('2024-03-05'),
        status: 'OPEN',
      },
    }),
  ]);

  console.log(`✅ Created ${payPeriods.length} pay periods\n`);

  // ============================================================================
  // 3. CREATE FLIGHTS
  // ============================================================================
  console.log('✈️  Creating flights...');

  const flights = await Promise.all([
    // BUR routes
    prisma.flight.create({
      data: {
        flightNumber: 'XP101',
        originAirport: 'BUR',
        destinationAirport: 'SFO',
        scheduledDeparture: new Date('2024-02-20T08:00:00Z'),
        scheduledArrival: new Date('2024-02-20T09:30:00Z'),
        actualDeparture: new Date('2024-02-20T08:15:00Z'),
        actualArrival: new Date('2024-02-20T09:45:00Z'),
        blockTimeHours: 1.50,
        delayMinutes: 15,
        delayCode: 'WX',
        delayReason: 'Weather at origin',
        aircraftType: '737-800',
        aircraftRegistration: 'N801AV',
      },
    }),
    prisma.flight.create({
      data: {
        flightNumber: 'XP102',
        originAirport: 'SFO',
        destinationAirport: 'BUR',
        scheduledDeparture: new Date('2024-02-20T11:00:00Z'),
        scheduledArrival: new Date('2024-02-20T12:30:00Z'),
        actualDeparture: new Date('2024-02-20T11:05:00Z'),
        actualArrival: new Date('2024-02-20T12:35:00Z'),
        blockTimeHours: 1.50,
        delayMinutes: 5,
        aircraftType: '737-800',
        aircraftRegistration: 'N801AV',
      },
    }),
    prisma.flight.create({
      data: {
        flightNumber: 'XP201',
        originAirport: 'BUR',
        destinationAirport: 'PDX',
        scheduledDeparture: new Date('2024-02-20T14:00:00Z'),
        scheduledArrival: new Date('2024-02-20T16:30:00Z'),
        actualDeparture: new Date('2024-02-20T14:00:00Z'),
        actualArrival: new Date('2024-02-20T16:30:00Z'),
        blockTimeHours: 2.50,
        delayMinutes: 0,
        aircraftType: '737-800',
        aircraftRegistration: 'N802AV',
      },
    }),
    prisma.flight.create({
      data: {
        flightNumber: 'XP202',
        originAirport: 'PDX',
        destinationAirport: 'BUR',
        scheduledDeparture: new Date('2024-02-20T18:00:00Z'),
        scheduledArrival: new Date('2024-02-20T20:30:00Z'),
        actualDeparture: new Date('2024-02-20T18:45:00Z'),
        actualArrival: new Date('2024-02-20T21:15:00Z'),
        blockTimeHours: 2.50,
        delayMinutes: 45,
        delayCode: 'MX',
        delayReason: 'Maintenance issue - hydraulic system check',
        aircraftType: '737-800',
        aircraftRegistration: 'N802AV',
      },
    }),
    // IFP routes
    prisma.flight.create({
      data: {
        flightNumber: 'XP301',
        originAirport: 'IFP',
        destinationAirport: 'LAX',
        scheduledDeparture: new Date('2024-02-21T09:00:00Z'),
        scheduledArrival: new Date('2024-02-21T10:15:00Z'),
        actualDeparture: new Date('2024-02-21T09:00:00Z'),
        actualArrival: new Date('2024-02-21T10:15:00Z'),
        blockTimeHours: 1.25,
        delayMinutes: 0,
        aircraftType: '737-800',
        aircraftRegistration: 'N803AV',
      },
    }),
    prisma.flight.create({
      data: {
        flightNumber: 'XP302',
        originAirport: 'LAX',
        destinationAirport: 'IFP',
        scheduledDeparture: new Date('2024-02-21T12:00:00Z'),
        scheduledArrival: new Date('2024-02-21T13:15:00Z'),
        actualDeparture: new Date('2024-02-21T12:00:00Z'),
        actualArrival: new Date('2024-02-21T13:15:00Z'),
        blockTimeHours: 1.25,
        delayMinutes: 0,
        aircraftType: '737-800',
        aircraftRegistration: 'N803AV',
      },
    }),
    // HVN routes
    prisma.flight.create({
      data: {
        flightNumber: 'XP401',
        originAirport: 'HVN',
        destinationAirport: 'MCO',
        scheduledDeparture: new Date('2024-02-22T07:00:00Z'),
        scheduledArrival: new Date('2024-02-22T10:00:00Z'),
        actualDeparture: new Date('2024-02-22T07:00:00Z'),
        actualArrival: new Date('2024-02-22T10:00:00Z'),
        blockTimeHours: 3.00,
        delayMinutes: 0,
        aircraftType: '737-800',
        aircraftRegistration: 'N804AV',
      },
    }),
    prisma.flight.create({
      data: {
        flightNumber: 'XP402',
        originAirport: 'MCO',
        destinationAirport: 'HVN',
        scheduledDeparture: new Date('2024-02-22T12:00:00Z'),
        scheduledArrival: new Date('2024-02-22T15:00:00Z'),
        actualDeparture: new Date('2024-02-22T12:30:00Z'),
        actualArrival: new Date('2024-02-22T15:30:00Z'),
        blockTimeHours: 3.00,
        delayMinutes: 30,
        delayCode: 'ATC',
        delayReason: 'Air traffic control ground stop',
        aircraftType: '737-800',
        aircraftRegistration: 'N804AV',
      },
    }),
  ]);

  console.log(`✅ Created ${flights.length} flights\n`);

  // ============================================================================
  // 4. CREATE CREW ASSIGNMENTS
  // ============================================================================
  console.log('👨‍✈️ Creating crew assignments...');

  const assignments = await Promise.all([
    // XP101 crew
    prisma.crewAssignment.create({
      data: {
        crewMemberId: crews[0].id,
        flightId: flights[0].id,
        position: 'OPERATING',
        dutyStartTime: new Date('2024-02-20T07:00:00Z'),
        dutyEndTime: new Date('2024-02-20T10:00:00Z'),
        checkInTime: new Date('2024-02-20T07:05:00Z'),
        checkOutTime: new Date('2024-02-20T09:55:00Z'),
      },
    }),
    prisma.crewAssignment.create({
      data: {
        crewMemberId: crews[3].id,
        flightId: flights[0].id,
        position: 'OPERATING',
        dutyStartTime: new Date('2024-02-20T07:00:00Z'),
        dutyEndTime: new Date('2024-02-20T10:00:00Z'),
        checkInTime: new Date('2024-02-20T07:05:00Z'),
        checkOutTime: new Date('2024-02-20T09:55:00Z'),
      },
    }),
    prisma.crewAssignment.create({
      data: {
        crewMemberId: crews[7].id,
        flightId: flights[0].id,
        position: 'OPERATING',
        dutyStartTime: new Date('2024-02-20T07:00:00Z'),
        dutyEndTime: new Date('2024-02-20T10:00:00Z'),
        checkInTime: new Date('2024-02-20T07:10:00Z'),
        checkOutTime: new Date('2024-02-20T09:50:00Z'),
      },
    }),
    // XP102 crew (same crew returns)
    prisma.crewAssignment.create({
      data: {
        crewMemberId: crews[0].id,
        flightId: flights[1].id,
        position: 'OPERATING',
        dutyStartTime: new Date('2024-02-20T10:00:00Z'),
        dutyEndTime: new Date('2024-02-20T13:00:00Z'),
        checkInTime: new Date('2024-02-20T10:30:00Z'),
        checkOutTime: new Date('2024-02-20T12:45:00Z'),
      },
    }),
    prisma.crewAssignment.create({
      data: {
        crewMemberId: crews[3].id,
        flightId: flights[1].id,
        position: 'OPERATING',
        dutyStartTime: new Date('2024-02-20T10:00:00Z'),
        dutyEndTime: new Date('2024-02-20T13:00:00Z'),
        checkInTime: new Date('2024-02-20T10:30:00Z'),
        checkOutTime: new Date('2024-02-20T12:45:00Z'),
      },
    }),
    prisma.crewAssignment.create({
      data: {
        crewMemberId: crews[7].id,
        flightId: flights[1].id,
        position: 'OPERATING',
        dutyStartTime: new Date('2024-02-20T10:00:00Z'),
        dutyEndTime: new Date('2024-02-20T13:00:00Z'),
        checkInTime: new Date('2024-02-20T10:30:00Z'),
        checkOutTime: new Date('2024-02-20T12:45:00Z'),
      },
    }),
    // XP201 crew
    prisma.crewAssignment.create({
      data: {
        crewMemberId: crews[1].id,
        flightId: flights[2].id,
        position: 'OPERATING',
        dutyStartTime: new Date('2024-02-20T13:00:00Z'),
        dutyEndTime: new Date('2024-02-20T17:30:00Z'),
        checkInTime: new Date('2024-02-20T13:05:00Z'),
        checkOutTime: new Date('2024-02-20T17:00:00Z'),
      },
    }),
    prisma.crewAssignment.create({
      data: {
        crewMemberId: crews[4].id,
        flightId: flights[2].id,
        position: 'OPERATING',
        dutyStartTime: new Date('2024-02-20T13:00:00Z'),
        dutyEndTime: new Date('2024-02-20T17:30:00Z'),
        checkInTime: new Date('2024-02-20T13:05:00Z'),
        checkOutTime: new Date('2024-02-20T17:00:00Z'),
      },
    }),
    prisma.crewAssignment.create({
      data: {
        crewMemberId: crews[8].id,
        flightId: flights[2].id,
        position: 'OPERATING',
        dutyStartTime: new Date('2024-02-20T13:00:00Z'),
        dutyEndTime: new Date('2024-02-20T17:30:00Z'),
        checkInTime: new Date('2024-02-20T13:10:00Z'),
        checkOutTime: new Date('2024-02-20T17:00:00Z'),
      },
    }),
  ]);

  console.log(`✅ Created ${assignments.length} crew assignments\n`);

  // ============================================================================
  // 5. CREATE FAA RULES
  // ============================================================================
  console.log('📜 Creating FAA regulations...');

  const faaRules = await Promise.all([
    prisma.faaRule.create({
      data: {
        ruleCode: 'Part117.23',
        ruleCategory: 'FLIGHT_DUTY_PERIOD',
        ruleTitle: 'Flight Duty Period: Unaugmented Operations',
        ruleText:
          'Except as provided for in §117.15, no certificate holder may assign and no flightcrew member may accept an assignment if the scheduled flight duty period will exceed the limits specified in Table B of this part.',
        effectiveDate: new Date('2014-01-04'),
        appliesTo: ['PILOTS'],
      },
    }),
    prisma.faaRule.create({
      data: {
        ruleCode: 'Part117.25',
        ruleCategory: 'REST_REQUIREMENTS',
        ruleTitle: 'Rest period',
        ruleText:
          '(a) No certificate holder may assign and no flightcrew member may accept assignment to any reserve or flight duty period unless the flightcrew member is given a rest period of at least 30 consecutive hours in the 168 consecutive hour period that precedes the completion of the assignment.',
        effectiveDate: new Date('2014-01-04'),
        appliesTo: ['PILOTS'],
      },
    }),
    prisma.faaRule.create({
      data: {
        ruleCode: 'Part117.11',
        ruleCategory: 'FLIGHT_DUTY_PERIOD',
        ruleTitle: 'Flight time limitation',
        ruleText:
          '(a) No certificate holder may schedule and no flightcrew member may accept an assignment if the flightcrew member\'s total flight time will exceed the following: (1) 100 hours in any 672 consecutive hours; (2) 1,000 hours in any 365 consecutive calendar day period.',
        effectiveDate: new Date('2014-01-04'),
        appliesTo: ['PILOTS'],
      },
    }),
    prisma.faaRule.create({
      data: {
        ruleCode: 'Part121.467',
        ruleCategory: 'FLIGHT_DUTY_PERIOD',
        ruleTitle: 'Flight attendant duty period limitations',
        ruleText:
          'No certificate holder may schedule a flight attendant for a duty period of more than 14 hours. Each flight attendant must be relieved from all duty for at least 24 consecutive hours during any 7 consecutive calendar days.',
        effectiveDate: new Date('1995-03-20'),
        appliesTo: ['FLIGHT_ATTENDANTS'],
      },
    }),
    prisma.faaRule.create({
      data: {
        ruleCode: 'Part117.19',
        ruleCategory: 'CUMULATIVE_LIMITS',
        ruleTitle: 'Flight duty period extensions',
        ruleText:
          '(a) For augmented and unaugmented operations, if unforeseen operational circumstances arise prior to takeoff: (1) The pilot in command and the certificate holder may extend the maximum flight duty period permitted in Tables B or C of this part up to 2 hours.',
        effectiveDate: new Date('2014-01-04'),
        appliesTo: ['PILOTS'],
      },
    }),
  ]);

  console.log(`✅ Created ${faaRules.length} FAA rules\n`);

  // ============================================================================
  // 6. CREATE UNION CONTRACT TERMS
  // ============================================================================
  console.log('📋 Creating union contract terms...');

  const contractTerms = await Promise.all([
    prisma.unionContractTerm.create({
      data: {
        termCode: 'ALPA_Section_5.A',
        termCategory: 'GUARANTEES',
        termTitle: 'Monthly Guarantee - Pilots',
        termText:
          'All pilots shall be guaranteed a minimum of 70 credit hours per calendar month, or the prorated amount for partial months.',
        calculationFormula: {
          type: 'monthly_guarantee',
          hours: 70,
          proration: 'calendar_days',
        },
        effectiveDate: new Date('2023-01-01'),
        appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
      },
    }),
    prisma.unionContractTerm.create({
      data: {
        termCode: 'AFA_Section_7.B',
        termCategory: 'GUARANTEES',
        termTitle: 'Monthly Guarantee - Flight Attendants',
        termText:
          'All flight attendants shall be guaranteed a minimum of 75 credit hours per calendar month.',
        calculationFormula: {
          type: 'monthly_guarantee',
          hours: 75,
          proration: 'calendar_days',
        },
        effectiveDate: new Date('2023-01-01'),
        appliesTo: ['FLIGHT_ATTENDANT'],
      },
    }),
    prisma.unionContractTerm.create({
      data: {
        termCode: 'ALPA_Section_12.C',
        termCategory: 'PREMIUMS',
        termTitle: 'Red-Eye Premium',
        termText:
          'Flights departing between 22:00 and 05:59 local time shall receive a 50% premium on the applicable hourly rate for all hours flown during that period.',
        calculationFormula: {
          type: 'premium_multiplier',
          multiplier: 1.5,
          time_range: {
            start: '22:00',
            end: '05:59',
          },
        },
        effectiveDate: new Date('2023-01-01'),
        appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
      },
    }),
    prisma.unionContractTerm.create({
      data: {
        termCode: 'ALPA_Section_8.D',
        termCategory: 'PER_DIEM',
        termTitle: 'Per Diem - Domestic',
        termText:
          'Pilots shall receive $2.50 per hour for all duty time away from base, calculated from check-in to check-out.',
        calculationFormula: {
          type: 'per_diem',
          rate: 2.50,
          calculation: 'duty_hours',
        },
        effectiveDate: new Date('2023-01-01'),
        appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
      },
    }),
    prisma.unionContractTerm.create({
      data: {
        termCode: 'AFA_Section_9.A',
        termCategory: 'PER_DIEM',
        termTitle: 'Per Diem - Flight Attendants',
        termText:
          'Flight attendants shall receive $2.25 per hour for all duty time away from base.',
        calculationFormula: {
          type: 'per_diem',
          rate: 2.25,
          calculation: 'duty_hours',
        },
        effectiveDate: new Date('2023-01-01'),
        appliesTo: ['FLIGHT_ATTENDANT'],
      },
    }),
    prisma.unionContractTerm.create({
      data: {
        termCode: 'ALPA_Section_6.E',
        termCategory: 'RIGS',
        termTitle: 'Duty Rig',
        termText:
          'Pilots shall be credited with the greater of actual flight time or one hour for every three hours of duty time (1:3 duty rig).',
        calculationFormula: {
          type: 'rig',
          ratio: 3,
          comparison: 'greater_of',
        },
        effectiveDate: new Date('2023-01-01'),
        appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
      },
    }),
    prisma.unionContractTerm.create({
      data: {
        termCode: 'ALPA_Section_10.A',
        termCategory: 'OVERTIME',
        termTitle: 'Overtime Pay',
        termText:
          'All credit hours in excess of 70 hours in a calendar month shall be compensated at 150% of the applicable hourly rate.',
        calculationFormula: {
          type: 'overtime',
          threshold: 70,
          multiplier: 1.5,
        },
        effectiveDate: new Date('2023-01-01'),
        appliesTo: ['CAPTAIN', 'FIRST_OFFICER'],
      },
    }),
  ]);

  console.log(`✅ Created ${contractTerms.length} union contract terms\n`);

  // ============================================================================
  // 7. CREATE RULE INTERPRETATIONS
  // ============================================================================
  console.log('🧠 Creating rule interpretations...');

  const interpretations = await Promise.all([
    prisma.ruleInterpretation.create({
      data: {
        scenarioDescription:
          'Long duty day with mechanical delay - determining if FDP extension is allowed and calculating delay pay',
        applicableFaaRuleIds: [faaRules[0].id, faaRules[4].id],
        applicableContractTermIds: [contractTerms[0].id, contractTerms[5].id],
        interpretation:
          'When a mechanical delay occurs, FAA Part 117.19 allows the PIC to extend the FDP up to 2 hours if unforeseen operational circumstances arise prior to takeoff. The duty rig (1:3) still applies, and the pilot is entitled to delay pay if the delay exceeds 30 minutes and is within the company\'s control.',
        exampleCalculation: {
          scenario: 'Flight delayed 45 minutes due to maintenance',
          faa_compliance: {
            original_fdp: '10 hours',
            extended_fdp: '10.75 hours',
            extension_allowed: true,
            rule: 'Part117.19',
          },
          pay_calculation: {
            actual_flight_time: 4.5,
            duty_time: 10.75,
            duty_rig_credit: 3.58,
            credit_hours: 4.5,
            delay_pay: 'Eligible if maintenance within company control',
          },
        },
        confidenceScore: 95,
        validatedBy: 'Chief Pilot',
      },
    }),
    prisma.ruleInterpretation.create({
      data: {
        scenarioDescription:
          'Red-eye flight with duty rig calculation - determining premium pay and credit hours',
        applicableFaaRuleIds: [faaRules[0].id],
        applicableContractTermIds: [contractTerms[2].id, contractTerms[5].id],
        interpretation:
          'For red-eye flights departing between 22:00-05:59, pilots receive a 50% premium on hours flown during that window. The duty rig (1:3) is applied to the base flight time, not the premium-adjusted time.',
        exampleCalculation: {
          scenario: 'Flight departs 23:00, arrives 02:00 (3 hours block time)',
          pay_calculation: {
            block_time: 3.0,
            red_eye_hours: 3.0,
            base_rate: 165.50,
            red_eye_premium: 82.75,
            total_hourly_rate: 248.25,
            duty_time: 8.0,
            duty_rig_credit: 2.67,
            credit_hours: 3.0,
            total_pay: 744.75,
          },
        },
        confidenceScore: 98,
        validatedBy: 'Union Contract Administrator',
      },
    }),
  ]);

  console.log(`✅ Created ${interpretations.length} rule interpretations\n`);

  // ============================================================================
  // 8. CREATE PAY CALCULATIONS
  // ============================================================================
  console.log('💰 Creating pay calculations...');

  const payCalculations = await Promise.all([
    // Sarah Mitchell (Captain) - First pay period
    prisma.payCalculation.create({
      data: {
        crewMemberId: crews[0].id,
        payPeriodId: payPeriods[0].id,
        flightPayHours: 72.5,
        flightPayAmount: 12000.00,
        overtimeHours: 2.5,
        overtimeAmount: 620.00,
        delayPayAmount: 150.00,
        perDiemAmount: 245.00,
        premiumPayAmount: 0,
        guaranteeHours: 70,
        totalGrossPay: 13015.00,
        calculationDate: new Date('2024-01-16'),
        validatedAt: new Date('2024-01-17'),
        validatedBy: 'Payroll System',
      },
    }),
    // Emily Johnson (First Officer) - First pay period
    prisma.payCalculation.create({
      data: {
        crewMemberId: crews[3].id,
        payPeriodId: payPeriods[0].id,
        flightPayHours: 68.0,
        flightPayAmount: 6700.00,
        overtimeHours: 0,
        overtimeAmount: 0,
        delayPayAmount: 0,
        perDiemAmount: 210.00,
        premiumPayAmount: 0,
        guaranteeHours: 70,
        totalGrossPay: 6910.00,
        calculationDate: new Date('2024-01-16'),
        validatedAt: new Date('2024-01-17'),
        validatedBy: 'Payroll System',
      },
    }),
    // Amanda Davis (Flight Attendant) - First pay period with underpayment
    prisma.payCalculation.create({
      data: {
        crewMemberId: crews[7].id,
        payPeriodId: payPeriods[0].id,
        flightPayHours: 73.0,
        flightPayAmount: 2080.50,
        overtimeHours: 0,
        overtimeAmount: 0,
        delayPayAmount: 0,
        perDiemAmount: 185.00,
        premiumPayAmount: 0,
        guaranteeHours: 75,
        totalGrossPay: 2265.50,
        calculationDate: new Date('2024-01-16'),
        validatedAt: new Date('2024-01-17'),
        validatedBy: 'Payroll System',
      },
    }),
  ]);

  console.log(`✅ Created ${payCalculations.length} pay calculations\n`);

  // ============================================================================
  // 9. CREATE DISCREPANCIES
  // ============================================================================
  console.log('⚠️  Creating discrepancies...');

  const discrepancies = await Promise.all([
    prisma.discrepancy.create({
      data: {
        crewMemberId: crews[7].id,
        payPeriodId: payPeriods[0].id,
        flightId: flights[0].id,
        discrepancyType: 'MISSING_PREMIUM',
        expectedAmount: 42.75,
        actualAmount: 0,
        differenceAmount: 42.75,
        severity: 'MEDIUM',
        detectedBy: 'PROACTIVE_AGENT',
        detectedAt: new Date('2024-01-17T10:30:00Z'),
        resolutionStatus: 'RESOLVED',
        resolutionDate: new Date('2024-01-18'),
        resolvedBy: 'AI Agent',
        resolutionNotes:
          'Weather delay premium automatically applied and corrected. Additional $42.75 credited to next pay period.',
      },
    }),
    prisma.discrepancy.create({
      data: {
        crewMemberId: crews[3].id,
        payPeriodId: payPeriods[1].id,
        discrepancyType: 'GUARANTEE_NOT_MET',
        expectedAmount: 6895.00,
        actualAmount: 6700.00,
        differenceAmount: 195.00,
        severity: 'HIGH',
        detectedBy: 'SYSTEM_CHECK',
        detectedAt: new Date('2024-02-01T08:00:00Z'),
        resolutionStatus: 'RESOLVED',
        resolutionDate: new Date('2024-02-02'),
        resolvedBy: 'Payroll Administrator',
        resolutionNotes:
          'Monthly guarantee of 70 hours not met (68 hours flown). Difference of $195 paid to meet guarantee.',
      },
    }),
  ]);

  console.log(`✅ Created ${discrepancies.length} discrepancies\n`);

  // ============================================================================
  // 10. CREATE CLAIMS
  // ============================================================================
  console.log('📝 Creating claims...');

  const claims = await Promise.all([
    prisma.claim.create({
      data: {
        claimNumber: 'CLM-2024-0001',
        crewMemberId: crews[1].id,
        payPeriodId: payPeriods[1].id,
        flightIds: [flights[3].id],
        claimType: 'DELAY_PAY',
        description:
          'Flight XP202 was delayed 45 minutes due to maintenance. Per contract, delays over 30 minutes due to maintenance should be compensated. This delay pay was not included in my paycheck.',
        claimedAmount: 75.00,
        submittedAt: new Date('2024-02-10T14:30:00Z'),
        submittedBy: crews[1].employeeId,
        status: 'APPROVED',
        reviewedAt: new Date('2024-02-11T09:15:00Z'),
        reviewedBy: 'AI Claims Agent',
        decision: 'APPROVE',
        decisionRationale:
          'Claim verified. Flight XP202 experienced a 45-minute maintenance delay on 2024-02-20. Per ALPA Section 13.B, maintenance delays exceeding 30 minutes are eligible for delay pay. Calculation: 0.75 hours × $162.75/hr × 0.5 = $61.03. Approved amount adjusted to actual calculation.',
        approvedAmount: 61.03,
        paymentStatus: 'PAID',
        paymentDate: new Date('2024-02-20'),
      },
    }),
    prisma.claim.create({
      data: {
        claimNumber: 'CLM-2024-0002',
        crewMemberId: crews[8].id,
        payPeriodId: payPeriods[2].id,
        flightIds: [flights[2].id, flights[3].id],
        claimType: 'INCORRECT_PER_DIEM',
        description:
          'My per diem for the PDX turnaround was calculated incorrectly. I should have received per diem for the entire duty period (7.5 hours) but only received credit for 4 hours.',
        claimedAmount: 78.75,
        submittedAt: new Date('2024-02-23T16:45:00Z'),
        submittedBy: crews[8].employeeId,
        status: 'UNDER_REVIEW',
        reviewedAt: new Date('2024-02-24T10:00:00Z'),
        reviewedBy: 'AI Claims Agent',
        decision: 'PARTIAL_APPROVE',
        decisionRationale:
          'Per diem calculation reviewed. Flight attendant per diem is $2.25/hr for duty time away from base. Duty period: 13:00-20:30 (7.5 hours). Current payment shows 4 hours. Discrepancy: 3.5 hours × $2.25 = $7.88. Approved for the correct differential amount.',
        approvedAmount: 7.88,
        paymentStatus: 'PROCESSING',
      },
    }),
  ]);

  console.log(`✅ Created ${claims.length} claims\n`);

  // ============================================================================
  // 11. CREATE NOTIFICATIONS
  // ============================================================================
  console.log('🔔 Creating notifications...');

  const notifications = await Promise.all([
    prisma.notification.create({
      data: {
        crewMemberId: crews[7].id,
        notificationType: 'PROACTIVE_FIX',
        title: 'Pay Discrepancy Auto-Corrected',
        message:
          'We detected a missing weather delay premium of $42.75 for flight XP101 on 02/20. This has been automatically corrected and will appear in your next paycheck.',
        relatedEntityType: 'discrepancy',
        relatedEntityId: discrepancies[0].id,
        sentAt: new Date('2024-01-18T11:00:00Z'),
        readAt: new Date('2024-01-18T15:30:00Z'),
        deliveryMethod: 'EMAIL',
      },
    }),
    prisma.notification.create({
      data: {
        crewMemberId: crews[1].id,
        notificationType: 'CLAIM_STATUS',
        title: 'Claim Approved - CLM-2024-0001',
        message:
          'Your claim for delay pay on flight XP202 has been approved. Amount: $61.03. Payment will be included in your February 20th paycheck.',
        relatedEntityType: 'claim',
        relatedEntityId: claims[0].id,
        sentAt: new Date('2024-02-11T09:30:00Z'),
        readAt: new Date('2024-02-11T12:15:00Z'),
        deliveryMethod: 'APP_PUSH',
      },
    }),
    prisma.notification.create({
      data: {
        crewMemberId: crews[8].id,
        notificationType: 'CLAIM_STATUS',
        title: 'Claim Under Review - CLM-2024-0002',
        message:
          'Your per diem claim is being reviewed. We\'ve identified a calculation discrepancy and are processing a partial approval of $7.88.',
        relatedEntityType: 'claim',
        relatedEntityId: claims[1].id,
        sentAt: new Date('2024-02-24T10:15:00Z'),
        deliveryMethod: 'EMAIL',
      },
    }),
  ]);

  console.log(`✅ Created ${notifications.length} notifications\n`);

  // ============================================================================
  // 12. CREATE AUDIT LOGS
  // ============================================================================
  console.log('📊 Creating audit logs...');

  const auditLogs = await Promise.all([
    prisma.auditLog.create({
      data: {
        entityType: 'discrepancy',
        entityId: discrepancies[0].id,
        action: 'CREATED',
        actorId: 'ai-agent-001',
        actorType: 'AI_AGENT',
        changes: {
          status: 'created',
          detected_by: 'proactive_agent',
        },
        reason: 'Automated discrepancy detection during pay calculation validation',
        ipAddress: '10.0.1.50',
        userAgent: 'Avelo-AI-Agent/1.0',
      },
    }),
    prisma.auditLog.create({
      data: {
        entityType: 'claim',
        entityId: claims[0].id,
        action: 'APPROVED',
        actorId: 'ai-agent-002',
        actorType: 'AI_AGENT',
        changes: {
          status: {
            from: 'UNDER_REVIEW',
            to: 'APPROVED',
          },
          approved_amount: 61.03,
        },
        reason: 'Claim verified against contract terms and flight records',
        ipAddress: '10.0.1.51',
        userAgent: 'Avelo-AI-Claims/1.0',
      },
    }),
    prisma.auditLog.create({
      data: {
        entityType: 'pay_calculation',
        entityId: payCalculations[0].id,
        action: 'UPDATED',
        actorId: 'system',
        actorType: 'SYSTEM',
        changes: {
          validated_at: new Date('2024-01-17'),
          validated_by: 'Payroll System',
        },
        reason: 'Pay calculation validated and approved',
        ipAddress: '10.0.1.10',
        userAgent: 'Avelo-Payroll-System/2.1',
      },
    }),
  ]);

  console.log(`✅ Created ${auditLogs.length} audit log entries\n`);

  console.log('✨ Database seeding completed successfully!\n');
  console.log('Summary:');
  console.log(`  - ${crews.length} crew members`);
  console.log(`  - ${payPeriods.length} pay periods`);
  console.log(`  - ${flights.length} flights`);
  console.log(`  - ${assignments.length} crew assignments`);
  console.log(`  - ${faaRules.length} FAA rules`);
  console.log(`  - ${contractTerms.length} union contract terms`);
  console.log(`  - ${interpretations.length} rule interpretations`);
  console.log(`  - ${payCalculations.length} pay calculations`);
  console.log(`  - ${discrepancies.length} discrepancies`);
  console.log(`  - ${claims.length} claims`);
  console.log(`  - ${notifications.length} notifications`);
  console.log(`  - ${auditLogs.length} audit log entries`);
}

main()
  .catch((e) => {
    console.error('Error seeding database:');
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
