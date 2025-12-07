import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import dotenv from 'dotenv';
import rateLimit from 'express-rate-limit';
import swaggerUi from 'swagger-ui-express';

import { initDatabase } from './config/database.js';
import { setupSocketIO } from './config/socket.js';
import { swaggerSpec } from './config/swagger.js';
import authRoutes from './routes/auth.js';
import roomRoutes from './routes/rooms.js';
import invitationRoutes from './routes/invitations.js';

dotenv.config();

const app = express();

// Configuration HTTP (par défaut, toujours fonctionnel)
const server = createServer(app);
const io = new Server(server, {
  cors: {
    origin: process.env.CLIENT_URL || 'http://localhost:5173',
    methods: ['GET', 'POST'],
    credentials: true,
  },
});

const PORT = process.env.PORT || 3001;
const PROTOCOL = 'http';

// Middleware
app.use(cors({
  origin: process.env.CLIENT_URL || 'http://localhost:5173',
  credentials: true,
}));
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 100, // 100 requêtes par minute
  message: 'Trop de requêtes, veuillez réessayer plus tard.',
});
app.use('/api/', limiter);

// Documentation Swagger
app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, {
  customCss: '.swagger-ui .topbar { display: none }',
  customSiteTitle: 'Shared IA API Documentation',
}));

/**
 * @swagger
 * /:
 *   get:
 *     summary: Informations sur l'API
 *     tags: [General]
 *     responses:
 *       200:
 *         description: Informations sur l'API
 */
app.get('/', (req, res) => {
  res.json({
    name: 'Shared IA Backend API',
    version: '1.0.0',
    status: 'running',
    documentation: `${PROTOCOL}://localhost:${PORT}/docs`,
    endpoints: {
      health: '/health',
      docs: '/docs',
      auth: '/api/auth',
      rooms: '/api/rooms',
      invitations: '/api/invitations',
    },
    socket: {
      enabled: true,
      events: 'See documentation',
    },
  });
});

/**
 * @swagger
 * /health:
 *   get:
 *     summary: Vérifier l'état du serveur
 *     tags: [General]
 *     responses:
 *       200:
 *         description: Serveur opérationnel
 */
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Backend is running' });
});

app.use('/api/auth', authRoutes);
app.use('/api/rooms', roomRoutes);
app.use('/api/invitations', invitationRoutes);

// Handler pour les routes non trouvées
app.use((req, res) => {
  res.status(404).json({
    error: 'Route non trouvée',
    path: req.path,
    method: req.method,
    availableEndpoints: {
      root: 'GET /',
      health: 'GET /health',
      auth: 'POST /api/auth/register, POST /api/auth/login',
      rooms: 'GET /api/rooms, POST /api/rooms, GET /api/rooms/:id, DELETE /api/rooms/:id',
      invitations: 'POST /api/invitations, GET /api/invitations/pending, POST /api/invitations/:id/accept, POST /api/invitations/:id/reject',
    },
  });
});

// Configuration Socket.io
setupSocketIO(io);

// Initialisation de la base de données et démarrage du serveur
initDatabase()
  .then(() => {
    server.listen(PORT, () => {
      console.log(`Serveur demarre sur ${PROTOCOL}://localhost:${PORT}`);
      console.log(`Documentation disponible sur ${PROTOCOL}://localhost:${PORT}/docs`);
      console.log(`Socket.io pret a recevoir des connexions`);
    });
  })
  .catch((error) => {
    console.error('Erreur lors de l\'initialisation:', error);
    process.exit(1);
  });

