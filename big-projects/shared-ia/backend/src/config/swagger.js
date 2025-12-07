import swaggerJsdoc from 'swagger-jsdoc';

// Déterminer l'URL de l'API pour Swagger
const getApiUrl = () => {
  // Render fournit RENDER_EXTERNAL_URL en production
  if (process.env.RENDER_EXTERNAL_URL) {
    return process.env.RENDER_EXTERNAL_URL;
  }
  // Sinon, utiliser API_URL si définie
  if (process.env.API_URL) {
    return process.env.API_URL;
  }
  // En développement, utiliser localhost
  return 'http://localhost:3001';
};

const apiUrl = getApiUrl();
const isProduction = process.env.NODE_ENV === 'production';

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Shared IA Backend API',
      version: '1.0.0',
      description: 'API pour l\'application de chat IA collaboratif',
      contact: {
        name: 'API Support',
      },
    },
    servers: [
      {
        url: apiUrl,
        description: isProduction ? 'Serveur de production' : 'Serveur de développement',
      },
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
        },
      },
      schemas: {
        User: {
          type: 'object',
          properties: {
            id: {
              type: 'string',
              format: 'uuid',
              description: 'Identifiant unique de l\'utilisateur',
            },
            username: {
              type: 'string',
              description: 'Nom d\'utilisateur',
            },
            createdAt: {
              type: 'string',
              format: 'date-time',
              description: 'Date de création',
            },
          },
        },
        Room: {
          type: 'object',
          properties: {
            id: {
              type: 'string',
              format: 'uuid',
            },
            name: {
              type: 'string',
            },
            aiContext: {
              type: 'string',
              description: 'Contexte IA de la room',
            },
            creatorId: {
              type: 'string',
              format: 'uuid',
            },
            createdAt: {
              type: 'string',
              format: 'date-time',
            },
          },
        },
        Invitation: {
          type: 'object',
          properties: {
            id: {
              type: 'string',
              format: 'uuid',
            },
            roomId: {
              type: 'string',
              format: 'uuid',
            },
            senderId: {
              type: 'string',
              format: 'uuid',
            },
            recipientId: {
              type: 'string',
              format: 'uuid',
            },
            status: {
              type: 'string',
              enum: ['pending', 'accepted', 'rejected'],
            },
            expiresAt: {
              type: 'string',
              format: 'date-time',
            },
            createdAt: {
              type: 'string',
              format: 'date-time',
            },
          },
        },
        Error: {
          type: 'object',
          properties: {
            error: {
              type: 'string',
              description: 'Message d\'erreur',
            },
          },
        },
      },
    },
    security: [
      {
        bearerAuth: [],
      },
    ],
  },
  apis: ['./src/routes/*.js', './src/server.js'],
};

export const swaggerSpec = swaggerJsdoc(options);

