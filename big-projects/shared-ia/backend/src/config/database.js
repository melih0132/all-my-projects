import pg from 'pg';
import dotenv from 'dotenv';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

dotenv.config();

const { Pool } = pg;

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Pool de connexions PostgreSQL
export const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
});

// Test de connexion
pool.on('connect', () => {
  console.log('Connexion a la base de donnees etablie');
});

pool.on('error', (err) => {
  console.error('Erreur de connexion a la base de donnees:', err);
});

// Initialisation de la base de données (création des tables)
export async function initDatabase() {
  try {
    // Lire et exécuter le schéma SQL
    const schemaPath = join(__dirname, '../schema.sql');
    const schema = readFileSync(schemaPath, 'utf-8');
    
    await pool.query(schema);
    console.log('Schema de base de donnees initialise');
    
    return true;
  } catch (error) {
    // Si les tables existent déjà, ce n'est pas grave
    if (error.code === '42P07') {
      console.log('Les tables existent deja');
      return true;
    }
    throw error;
  }
}

// Helper pour les transactions
export async function withTransaction(callback) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const result = await callback(client);
    await client.query('COMMIT');
    return result;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}

