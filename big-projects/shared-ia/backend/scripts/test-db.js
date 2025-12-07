import dotenv from 'dotenv';
import { pool } from '../src/config/database.js';

dotenv.config();

async function testConnection() {
  try {
    console.log('Test de connexion a la base de donnees...');
    console.log('URL:', process.env.DATABASE_URL?.replace(/:[^:@]+@/, ':****@'));
    
    const result = await pool.query('SELECT NOW() as current_time, version() as postgres_version');
    
    console.log('Connexion reussie !');
    console.log('Heure serveur:', result.rows[0].current_time);
    console.log('Version PostgreSQL:', result.rows[0].postgres_version.split(' ')[0] + ' ' + result.rows[0].postgres_version.split(' ')[1]);
    
    // Tester si les tables existent
    const tablesResult = await pool.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public'
      ORDER BY table_name
    `);
    
    console.log('\nTables existantes:');
    if (tablesResult.rows.length === 0) {
      console.log('   Aucune table trouvee. Le schema sera cree au demarrage du serveur.');
    } else {
      tablesResult.rows.forEach(row => {
        console.log(`   - ${row.table_name}`);
      });
    }
    
    process.exit(0);
  } catch (error) {
    console.error('Erreur de connexion:', error.message);
    console.error('\nVerifiez que:');
    console.error('   1. Le fichier .env existe et contient DATABASE_URL');
    console.error('   2. L\'URL de connexion est correcte');
    console.error('   3. La base de donnees Supabase est accessible');
    process.exit(1);
  }
}

testConnection();

