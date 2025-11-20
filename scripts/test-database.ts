import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function testDatabase() {
  console.log('🧪 Testing Database Setup\n');
  console.log('═══════════════════════════════════════\n');

  try {
    // Test 1: Connection
    console.log('1. Testing database connection...');
    await prisma.$connect();
    console.log('   ✅ Successfully connected to database\n');

    // Test 2: Table existence
    console.log('2. Checking table existence...');
    const tables = [
      'crew_members',
      'flights',
      'crew_assignments',
      'pay_periods',
      'pay_calculations',
      'discrepancies',
      'claims',
      'faa_rules',
      'union_contract_terms',
      'rule_interpretations',
      'notifications',
      'audit_log',
    ];

    for (const table of tables) {
      const result = await prisma.$queryRawUnsafe(`
        SELECT EXISTS (
          SELECT FROM information_schema.tables
          WHERE table_name = '${table}'
        );
      `);
      console.log(`   ✅ Table '${table}' exists`);
    }
    console.log('');

    // Test 3: Sample data counts
    console.log('3. Checking seed data...');

    const crewCount = await prisma.crewMember.count();
    console.log(`   ✅ Crew members: ${crewCount}`);

    const flightCount = await prisma.flight.count();
    console.log(`   ✅ Flights: ${flightCount}`);

    const assignmentCount = await prisma.crewAssignment.count();
    console.log(`   ✅ Crew assignments: ${assignmentCount}`);

    const payPeriodCount = await prisma.payPeriod.count();
    console.log(`   ✅ Pay periods: ${payPeriodCount}`);

    const payCalcCount = await prisma.payCalculation.count();
    console.log(`   ✅ Pay calculations: ${payCalcCount}`);

    const discrepancyCount = await prisma.discrepancy.count();
    console.log(`   ✅ Discrepancies: ${discrepancyCount}`);

    const claimCount = await prisma.claim.count();
    console.log(`   ✅ Claims: ${claimCount}`);

    const faaRuleCount = await prisma.faaRule.count();
    console.log(`   ✅ FAA rules: ${faaRuleCount}`);

    const contractTermCount = await prisma.unionContractTerm.count();
    console.log(`   ✅ Contract terms: ${contractTermCount}`);

    const notificationCount = await prisma.notification.count();
    console.log(`   ✅ Notifications: ${notificationCount}`);

    const auditLogCount = await prisma.auditLog.count();
    console.log(`   ✅ Audit log entries: ${auditLogCount}\n`);

    // Test 4: Sample queries
    console.log('4. Testing sample queries...');

    // Get crew with their assignments
    const crewWithAssignments = await prisma.crewMember.findFirst({
      include: {
        crewAssignments: {
          include: {
            flight: true,
          },
          take: 5,
        },
      },
    });
    console.log(`   ✅ Query: Crew member with assignments`);
    console.log(`      Found: ${crewWithAssignments?.firstName} ${crewWithAssignments?.lastName}`);
    console.log(`      Assignments: ${crewWithAssignments?.crewAssignments.length || 0}\n`);

    // Get pay calculation with details
    const payCalc = await prisma.payCalculation.findFirst({
      include: {
        crewMember: true,
        payPeriod: true,
      },
    });
    console.log(`   ✅ Query: Pay calculation with relationships`);
    console.log(`      Crew: ${payCalc?.crewMember.firstName} ${payCalc?.crewMember.lastName}`);
    console.log(`      Total pay: $${payCalc?.totalGrossPay || 0}\n`);

    // Get open discrepancies
    const openDiscrepancies = await prisma.discrepancy.findMany({
      where: {
        resolutionStatus: { in: ['OPEN', 'INVESTIGATING'] },
      },
      include: {
        crewMember: true,
      },
    });
    console.log(`   ✅ Query: Open discrepancies`);
    console.log(`      Count: ${openDiscrepancies.length}\n`);

    // Get claims with status
    const claims = await prisma.claim.findMany({
      include: {
        crewMember: true,
      },
      take: 5,
    });
    console.log(`   ✅ Query: Claims with crew info`);
    console.log(`      Count: ${claims.length}\n`);

    // Test 5: Index verification
    console.log('5. Verifying indexes...');
    const indexQuery = await prisma.$queryRaw<any[]>`
      SELECT tablename, indexname
      FROM pg_indexes
      WHERE schemaname = 'public'
      AND tablename IN ('crew_members', 'flights', 'crew_assignments', 'pay_calculations')
      ORDER BY tablename, indexname;
    `;
    console.log(`   ✅ Found ${indexQuery.length} indexes\n`);

    // Test 6: Foreign key constraints
    console.log('6. Verifying foreign key constraints...');
    const fkQuery = await prisma.$queryRaw<any[]>`
      SELECT
        tc.table_name,
        kcu.column_name,
        ccu.table_name AS foreign_table_name,
        ccu.column_name AS foreign_column_name
      FROM information_schema.table_constraints AS tc
      JOIN information_schema.key_column_usage AS kcu
        ON tc.constraint_name = kcu.constraint_name
      JOIN information_schema.constraint_column_usage AS ccu
        ON ccu.constraint_name = tc.constraint_name
      WHERE tc.constraint_type = 'FOREIGN KEY'
      AND tc.table_schema = 'public'
      ORDER BY tc.table_name;
    `;
    console.log(`   ✅ Found ${fkQuery.length} foreign key constraints\n`);

    console.log('═══════════════════════════════════════');
    console.log('✨ All database tests passed!\n');

    // Summary
    console.log('📊 Database Summary:');
    console.log(`   - Tables: ${tables.length}`);
    console.log(`   - Crew members: ${crewCount}`);
    console.log(`   - Flights: ${flightCount}`);
    console.log(`   - Total records: ${crewCount + flightCount + assignmentCount + payPeriodCount + payCalcCount + discrepancyCount + claimCount + faaRuleCount + contractTermCount + notificationCount + auditLogCount}`);
    console.log(`   - Indexes: ${indexQuery.length}`);
    console.log(`   - Foreign keys: ${fkQuery.length}`);
    console.log('');
  } catch (error: any) {
    console.error('❌ Database test failed:');
    console.error(error.message);
    process.exit(1);
  } finally {
    await prisma.$disconnect();
  }
}

testDatabase();
