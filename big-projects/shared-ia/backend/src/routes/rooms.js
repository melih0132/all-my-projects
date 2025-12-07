import express from 'express';
import { z } from 'zod';
import { pool } from '../config/database.js';
import { authenticate } from '../middleware/auth.js';

const router = express.Router();

// Toutes les routes nécessitent une authentification
router.use(authenticate);

// Schéma de validation pour la création de room
const createRoomSchema = z.object({
  name: z.string().max(100).optional(),
  aiContext: z.string().min(1, 'Le contexte IA est requis'),
});

/**
 * @swagger
 * /api/rooms:
 *   post:
 *     summary: Créer une nouvelle room
 *     tags: [Rooms]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - aiContext
 *             properties:
 *               name:
 *                 type: string
 *                 maxLength: 100
 *                 example: Ma conversation
 *               aiContext:
 *                 type: string
 *                 description: Contexte et rôle de l'IA
 *                 example: Tu es un assistant développeur spécialisé en React
 *     responses:
 *       201:
 *         description: Room créée avec succès
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 room:
 *                   $ref: '#/components/schemas/Room'
 *                 welcomeMessage:
 *                   type: object
 *       400:
 *         description: Erreur de validation
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Error'
 */
router.post('/', async (req, res) => {
  try {
    const { name, aiContext } = createRoomSchema.parse(req.body);

    // Générer un nom par défaut si non fourni
    const roomName = name || `Conversation du ${new Date().toLocaleDateString('fr-FR')}`;

    // Créer la room et ajouter le créateur comme membre dans une transaction
    const client = await pool.connect();
    try {
      await client.query('BEGIN');

      // Créer la room
      const roomResult = await client.query(
        'INSERT INTO rooms (name, ai_context, creator_id) VALUES ($1, $2, $3) RETURNING *',
        [roomName, aiContext, req.user.id]
      );

      const room = roomResult.rows[0];

      // Ajouter le créateur comme membre
      await client.query(
        'INSERT INTO room_members (room_id, user_id, role, joined_at) VALUES ($1, $2, NULL, NOW())',
        [room.id, req.user.id]
      );

      // Créer un message de bienvenue de l'IA
      const welcomeMessageContent = 'Bonjour ! Je suis votre assistant IA. Pour commencer, veuillez définir votre rôle dans l\'équipe.';
      const welcomeMessage = await client.query(
        `INSERT INTO messages (room_id, user_id, type, content, status, created_at)
         VALUES ($1, NULL, 'ai', $2, 'sent', NOW())
         RETURNING *`,
        [room.id, welcomeMessageContent]
      );

      await client.query('COMMIT');

      res.status(201).json({
        room: {
          id: room.id,
          name: room.name,
          aiContext: room.ai_context,
          creatorId: room.creator_id,
          createdAt: room.created_at,
        },
        welcomeMessage: welcomeMessage.rows[0],
      });
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: error.errors[0].message });
    }
    console.error('Erreur lors de la création de la room:', error);
    res.status(500).json({ error: 'Erreur lors de la création de la room' });
  }
});

/**
 * @swagger
 * /api/rooms:
 *   get:
 *     summary: Lister toutes les rooms de l'utilisateur
 *     tags: [Rooms]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Liste des rooms
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 rooms:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/Room'
 */
router.get('/', async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT r.*, 
        COUNT(DISTINCT rm.user_id) as member_count,
        MAX(m.created_at) as last_message_at
       FROM rooms r
       INNER JOIN room_members rm ON r.id = rm.room_id
       LEFT JOIN messages m ON r.id = m.room_id
       WHERE rm.user_id = $1
       GROUP BY r.id
       ORDER BY last_message_at DESC NULLS LAST, r.created_at DESC`,
      [req.user.id]
    );

    res.json({ rooms: result.rows });
  } catch (error) {
    console.error('Erreur lors de la récupération des rooms:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des rooms' });
  }
});

/**
 * @swagger
 * /api/rooms/{roomId}:
 *   get:
 *     summary: Récupérer une room avec ses membres et messages
 *     tags: [Rooms]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: roomId
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *     responses:
 *       200:
 *         description: Détails de la room
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 room:
 *                   $ref: '#/components/schemas/Room'
 *                 members:
 *                   type: array
 *                 messages:
 *                   type: array
 *       403:
 *         description: Vous n'êtes pas membre de cette room
 *       404:
 *         description: Room introuvable
 */
router.get('/:roomId', async (req, res) => {
  try {
    const { roomId } = req.params;
    
    // Valider le format UUID
    if (!z.string().uuid().safeParse(roomId).success) {
      return res.status(400).json({ error: 'ID de room invalide' });
    }

    // Vérifier que l'utilisateur est membre de la room
    const memberCheck = await pool.query(
      'SELECT * FROM room_members WHERE user_id = $1 AND room_id = $2',
      [req.user.id, roomId]
    );

    if (memberCheck.rows.length === 0) {
      return res.status(403).json({ error: 'Vous n\'êtes pas membre de cette room' });
    }

    // Récupérer la room
    const roomResult = await pool.query('SELECT * FROM rooms WHERE id = $1', [roomId]);
    
    if (roomResult.rows.length === 0) {
      return res.status(404).json({ error: 'Room introuvable' });
    }

    const room = roomResult.rows[0];

    // Récupérer les membres
    const membersResult = await pool.query(
      `SELECT u.id, u.username, rm.role, rm.joined_at
       FROM room_members rm
       INNER JOIN users u ON rm.user_id = u.id
       WHERE rm.room_id = $1
       ORDER BY rm.joined_at ASC`,
      [roomId]
    );

    // Récupérer les messages (50 derniers)
    const messagesResult = await pool.query(
      `SELECT m.*, u.username, rm.role
       FROM messages m
       LEFT JOIN users u ON m.user_id = u.id
       LEFT JOIN room_members rm ON m.user_id = rm.user_id AND m.room_id = rm.room_id
       WHERE m.room_id = $1
       ORDER BY m.created_at ASC
       LIMIT 50`,
      [roomId]
    );

    res.json({
      room: {
        id: room.id,
        name: room.name,
        aiContext: room.ai_context,
        creatorId: room.creator_id,
        createdAt: room.created_at,
      },
      members: membersResult.rows,
      messages: messagesResult.rows,
    });
  } catch (error) {
    console.error('Erreur lors de la récupération de la room:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération de la room' });
  }
});

/**
 * @swagger
 * /api/rooms/{roomId}:
 *   delete:
 *     summary: Supprimer une room (seul le créateur peut)
 *     tags: [Rooms]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: roomId
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *     responses:
 *       200:
 *         description: Room supprimée avec succès
 *       403:
 *         description: Seul le créateur peut supprimer la room
 *       404:
 *         description: Room introuvable
 */
/**
 * @swagger
 * /api/rooms/{roomId}/role:
 *   put:
 *     summary: Mettre à jour le rôle d'un membre dans une room
 *     tags: [Rooms]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: roomId
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - role
 *             properties:
 *               role:
 *                 type: string
 *                 maxLength: 100
 *                 example: Développeur Frontend
 *     responses:
 *       200:
 *         description: Rôle mis à jour avec succès
 *       400:
 *         description: Erreur de validation
 *       403:
 *         description: Vous n'êtes pas membre de cette room
 *       404:
 *         description: Room introuvable
 */
router.put('/:roomId/role', async (req, res) => {
  try {
    const { roomId } = req.params;
    const { role } = req.body;

    // Valider le format UUID
    if (!z.string().uuid().safeParse(roomId).success) {
      return res.status(400).json({ error: 'ID de room invalide' });
    }

    // Valider le rôle
    if (!role || typeof role !== 'string' || role.trim().length === 0) {
      return res.status(400).json({ error: 'Le role est requis' });
    }

    if (role.length > 100) {
      return res.status(400).json({ error: 'Le role ne peut pas depasser 100 caracteres' });
    }

    // Vérifier que l'utilisateur est membre de la room
    const memberCheck = await pool.query(
      'SELECT * FROM room_members WHERE user_id = $1 AND room_id = $2',
      [req.user.id, roomId]
    );

    if (memberCheck.rows.length === 0) {
      return res.status(403).json({ error: 'Vous n\'etes pas membre de cette room' });
    }

    // Vérifier que la room existe
    const roomCheck = await pool.query('SELECT id FROM rooms WHERE id = $1', [roomId]);
    if (roomCheck.rows.length === 0) {
      return res.status(404).json({ error: 'Room introuvable' });
    }

    // Mettre à jour le rôle
    await pool.query(
      'UPDATE room_members SET role = $1 WHERE user_id = $2 AND room_id = $3',
      [role.trim(), req.user.id, roomId]
    );

    res.json({ message: 'Role mis a jour avec succes', role: role.trim() });
  } catch (error) {
    console.error('Erreur lors de la mise a jour du role:', error);
    res.status(500).json({ error: 'Erreur lors de la mise a jour du role' });
  }
});

/**
 * @swagger
 * /api/rooms/{roomId}:
 *   delete:
 *     summary: Supprimer une room (seul le créateur peut)
 *     tags: [Rooms]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: roomId
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *     responses:
 *       200:
 *         description: Room supprimée avec succès
 *       403:
 *         description: Seul le créateur peut supprimer la room
 *       404:
 *         description: Room introuvable
 */
router.delete('/:roomId', async (req, res) => {
  try {
    const { roomId } = req.params;
    
    // Valider le format UUID
    if (!z.string().uuid().safeParse(roomId).success) {
      return res.status(400).json({ error: 'ID de room invalide' });
    }

    // Vérifier que l'utilisateur est le créateur
    const roomResult = await pool.query('SELECT creator_id FROM rooms WHERE id = $1', [roomId]);
    
    if (roomResult.rows.length === 0) {
      return res.status(404).json({ error: 'Room introuvable' });
    }

    if (roomResult.rows[0].creator_id !== req.user.id) {
      return res.status(403).json({ error: 'Seul le créateur peut supprimer la room' });
    }

    // Notifier tous les membres de la room via Socket.io que la room a été supprimée
    // Note: Cette notification doit être faite avant la suppression pour que les sockets soient encore connectés
    const { getIOInstance } = await import('../config/socket.js');
    const io = getIOInstance();
    if (io) {
      io.to(`room:${roomId}`).emit('room-deleted', { roomId });
    }

    // Supprimer la room (les contraintes CASCADE supprimeront les données liées)
    await pool.query('DELETE FROM rooms WHERE id = $1', [roomId]);

    res.json({ message: 'Room supprimée avec succès' });
  } catch (error) {
    console.error('Erreur lors de la suppression de la room:', error);
    res.status(500).json({ error: 'Erreur lors de la suppression de la room' });
  }
});

export default router;

