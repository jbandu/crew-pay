import neo4j from 'neo4j-driver';
import * as fs from 'fs';
import * as path from 'path';
import * as dotenv from 'dotenv';

dotenv.config();

const NEO4J_URI = process.env.NEO4J_URI || '';
const NEO4J_USER = process.env.NEO4J_USER || 'neo4j';
const NEO4J_PASSWORD = process.env.NEO4J_PASSWORD || '';

async function loadNeo4jData() {
  console.log('🔌 Connecting to Neo4j...\n');

  const driver = neo4j.driver(
    NEO4J_URI,
    neo4j.auth.basic(NEO4J_USER, NEO4J_PASSWORD)
  );

  const session = driver.session();

  try {
    // Verify connection
    await session.run('RETURN 1');
    console.log('✅ Connected to Neo4j successfully\n');

    // Load schema
    console.log('📋 Loading schema (constraints and indexes)...');
    const schemaPath = path.join(__dirname, '..', 'neo4j', 'schema.cypher');
    const schemaContent = fs.readFileSync(schemaPath, 'utf-8');

    // Split by semicolons and filter out comments
    const schemaStatements = schemaContent
      .split(';')
      .map((s) => s.trim())
      .filter((s) => s && !s.startsWith('//'));

    for (const statement of schemaStatements) {
      if (statement.toLowerCase().startsWith('create constraint') ||
          statement.toLowerCase().startsWith('create index')) {
        try {
          await session.run(statement);
          console.log(`  ✓ ${statement.substring(0, 60)}...`);
        } catch (err: any) {
          if (err.code === 'Neo.ClientError.Schema.EquivalentSchemaRuleAlreadyExists') {
            console.log(`  ⊘ Already exists: ${statement.substring(0, 60)}...`);
          } else {
            console.error(`  ✗ Error: ${err.message}`);
          }
        }
      }
    }

    console.log('\n🌱 Loading seed data...');

    // Load seed data
    const seedPath = path.join(__dirname, '..', 'neo4j', 'seed.cypher');
    const seedContent = fs.readFileSync(seedPath, 'utf-8');

    // Split by CREATE or MATCH statements
    const seedStatements = seedContent
      .split(/(?=CREATE|MATCH)/g)
      .map((s) => s.trim().replace(/;$/, ''))
      .filter((s) => s && !s.startsWith('//'));

    let created = 0;
    for (const statement of seedStatements) {
      try {
        await session.run(statement);
        created++;
        if (created % 10 === 0) {
          console.log(`  Created ${created} nodes/relationships...`);
        }
      } catch (err: any) {
        console.error(`  ✗ Error executing statement: ${err.message}`);
        console.error(`  Statement: ${statement.substring(0, 100)}...`);
      }
    }

    console.log(`\n✅ Loaded ${created} Cypher statements\n`);

    // Verify data
    console.log('🔍 Verifying loaded data...\n');

    const counts = [
      { label: 'FAA Rules', query: 'MATCH (r:Rule) RETURN count(r) as count' },
      { label: 'Contract Terms', query: 'MATCH (c:ContractTerm) RETURN count(c) as count' },
      { label: 'Pay Components', query: 'MATCH (p:PayComponent) RETURN count(p) as count' },
      { label: 'Scenarios', query: 'MATCH (s:Scenario) RETURN count(s) as count' },
      {
        label: 'Relationships',
        query: 'MATCH ()-[r]->() RETURN count(r) as count',
      },
    ];

    for (const { label, query } of counts) {
      const result = await session.run(query);
      const count = result.records[0].get('count').toNumber();
      console.log(`  ${label}: ${count}`);
    }

    console.log('\n✨ Neo4j setup completed successfully!\n');

    // Example queries
    console.log('📊 Sample queries:\n');

    console.log('1. All scenarios with their required pay components:');
    const scenariosResult = await session.run(`
      MATCH (s:Scenario)-[:REQUIRES]->(p:PayComponent)
      RETURN s.id as scenario, collect(p.type) as components
      ORDER BY s.id
    `);

    scenariosResult.records.forEach((record) => {
      const scenario = record.get('scenario');
      const components = record.get('components');
      console.log(`   - ${scenario}: ${components.join(', ')}`);
    });

    console.log('\n2. Rules applying to delayed flights:');
    const rulesResult = await session.run(`
      MATCH (r)-[:APPLIES_TO]->(s:Scenario {id: 'delayed_flight_controllable'})
      RETURN r.code as code, r.title as title
      ORDER BY r.code
    `);

    rulesResult.records.forEach((record) => {
      const code = record.get('code');
      const title = record.get('title');
      console.log(`   - ${code}: ${title}`);
    });

    console.log('');
  } catch (error: any) {
    console.error('❌ Error loading Neo4j data:');
    console.error(error.message);
    process.exit(1);
  } finally {
    await session.close();
    await driver.close();
  }
}

loadNeo4jData();
