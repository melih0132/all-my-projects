import jwt from 'jsonwebtoken';
import { pool } from '../config/database.js';

// Middleware d'authentification pour les routes Express
export async function authenticate(req, res, next) {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Token manquant' });
    }

    const token = authHeader.replace('Bearer ', '');
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Vérifier que l'utilisateur existe toujours
    const result = await pool.query('SELECT id, username FROM users WHERE id = $1', [decoded.userId]);
    
    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'Utilisateur introuvable' });
    }

    req.user = {
      id: result.rows[0].id,
      username: result.rows[0].username,
    };

    next();
  } catch (error) {
    if (error.name === 'JsonWebTokenError' || error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token invalide ou expiré' });
    }
    return res.status(500).json({ error: 'Erreur d\'authentification' });
  }
}

