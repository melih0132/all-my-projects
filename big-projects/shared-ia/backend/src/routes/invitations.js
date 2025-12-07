import express from 'express';
import { z } from 'zod';
import { pool } from '../config/database.js';
import { authenticate } from '../middleware/auth.js';

const router = express.Router();

router.use(authenticate);

// Schéma de validation pour l'envoi d'invitation
const createInvitationSchema = z.object({
  roomId: z.string().uuid('Room ID invalide'),
  recipientUsername: z.string().min(1, 'Le username du destinataire est requis'),
});

/**
 * @swagger
 * /api/invitations:
 *   post:
 *     summary: Créer une invitation
 *     tags: [Invitations]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - roomId
 *               - recipientUsername
 *             properties:
 *               roomId:
 *                 type: string
 *                 format: uuid
 *               recipientUsername:
 *                 type: string
 *                 example: john_doe
 *     responses:
 *       201:
 *         description: Invitation créée avec succès
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 invitation:
 *                   $ref: '#/components/schemas/Invitation'
 *       400:
 *         description: Erreur de validation ou conditions non remplies
 *       403:
 *         description: Vous n'êtes pas membre de cette room
 *       404:
 *         description: Utilisateur introuvable
 */
router.post('/', async (req, res) => {
  try {
    const { roomId, recipientUsername } = createInvitationSchema.parse(req.body);

    const client = await pool.connect();
    try {
      await client.query('BEGIN');

      // Vérifier que l'expéditeur est membre de la room
      const senderCheck = await client.query(
        'SELECT * FROM room_members WHERE user_id = $1 AND room_id = $2',
        [req.user.id, roomId]
      );

      if (senderCheck.rows.length === 0) {
        await client.query('ROLLBACK');
        return res.status(403).json({ error: 'Vous n\'êtes pas membre de cette room' });
      }

      // Vérifier que le destinataire existe
      const recipientResult = await client.query('SELECT id FROM users WHERE username = $1', [recipientUsername]);
      
      if (recipientResult.rows.length === 0) {
        await client.query('ROLLBACK');
        return res.status(404).json({ error: 'Utilisateur introuvable' });
      }

      const recipientId = recipientResult.rows[0].id;

      // Vérifier que le destinataire n'est pas déjà membre
      const memberCheck = await client.query(
        'SELECT * FROM room_members WHERE user_id = $1 AND room_id = $2',
        [recipientId, roomId]
      );

      if (memberCheck.rows.length > 0) {
        await client.query('ROLLBACK');
        return res.status(400).json({ error: 'Cet utilisateur est déjà membre de la room' });
      }

      // Vérifier que la room n'a pas atteint 4 membres
      const memberCount = await client.query(
        'SELECT COUNT(*) as count FROM room_members WHERE room_id = $1',
        [roomId]
      );

      if (parseInt(memberCount.rows[0].count) >= 4) {
        await client.query('ROLLBACK');
        return res.status(400).json({ error: 'La room a atteint le maximum de 4 membres' });
      }

      // Vérifier qu'il n'existe pas déjà une invitation en "pending" pour ce destinataire dans cette room
      const existingInvitation = await client.query(
        `SELECT * FROM invitations 
         WHERE room_id = $1 AND recipient_id = $2 AND status = 'pending' AND expires_at > NOW()`,
        [roomId, recipientId]
      );

      if (existingInvitation.rows.length > 0) {
        await client.query('ROLLBACK');
        return res.status(400).json({ error: 'Une invitation est déjà en attente pour cet utilisateur' });
      }

      // Créer l'invitation
      const expiresAt = new Date();
      expiresAt.setDate(expiresAt.getDate() + 7); // 7 jours

      const invitationResult = await client.query(
        `INSERT INTO invitations (room_id, sender_id, recipient_id, status, expires_at, created_at)
         VALUES ($1, $2, $3, 'pending', $4, NOW())
         RETURNING *`,
        [roomId, req.user.id, recipientId, expiresAt]
      );

      await client.query('COMMIT');

      res.status(201).json({ invitation: invitationResult.rows[0] });
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
    console.error('Erreur lors de la création de l\'invitation:', error);
    res.status(500).json({ error: 'Erreur lors de la création de l\'invitation' });
  }
});

/**
 * @swagger
 * /api/invitations/pending:
 *   get:
 *     summary: Lister les invitations reçues en attente
 *     tags: [Invitations]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Liste des invitations en attente
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 invitations:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/Invitation'
 */
router.get('/pending', async (req, res) => {
  try {
    const result = await pool.query(
      `SELECT i.*, 
        r.name as room_name, r.ai_context as room_context,
        u.username as sender_username
       FROM invitations i
       INNER JOIN rooms r ON i.room_id = r.id
       INNER JOIN users u ON i.sender_id = u.id
       WHERE i.recipient_id = $1 AND i.status = 'pending'
       ORDER BY i.created_at DESC`,
      [req.user.id]
    );

    // Vérifier l'expiration
    const now = new Date();
    const invitations = result.rows.map(inv => ({
      ...inv,
      isExpired: new Date(inv.expires_at) < now,
    }));

    res.json({ invitations });
  } catch (error) {
    console.error('Erreur lors de la récupération des invitations:', error);
    res.status(500).json({ error: 'Erreur lors de la récupération des invitations' });
  }
});

/**
 * @swagger
 * /api/invitations/{id}/accept:
 *   post:
 *     summary: Accepter une invitation
 *     tags: [Invitations]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *     responses:
 *       200:
 *         description: Invitation acceptée
 *       400:
 *         description: La room a atteint le maximum de membres
 *       404:
 *         description: Invitation introuvable
 *       410:
 *         description: Invitation expirée
 */
router.post('/:id/accept', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Valider le format UUID
    if (!z.string().uuid().safeParse(id).success) {
      return res.status(400).json({ error: 'ID d\'invitation invalide' });
    }

    const client = await pool.connect();
    try {
      await client.query('BEGIN');

      // Récupérer l'invitation
      const invitationResult = await client.query(
        'SELECT * FROM invitations WHERE id = $1 AND recipient_id = $2',
        [id, req.user.id]
      );

      if (invitationResult.rows.length === 0) {
        await client.query('ROLLBACK');
        return res.status(404).json({ error: 'Invitation introuvable' });
      }

      const invitation = invitationResult.rows[0];

      // Vérifier l'expiration
      if (new Date(invitation.expires_at) < new Date()) {
        await client.query('ROLLBACK');
        return res.status(410).json({ error: 'Cette invitation a expiré' });
      }

      // Vérifier que l'invitation est en pending
      if (invitation.status !== 'pending') {
        await client.query('ROLLBACK');
        return res.status(400).json({ error: 'Cette invitation a déjà été traitée' });
      }

      // Vérifier que la room n'a pas atteint 4 membres
      const memberCount = await client.query(
        'SELECT COUNT(*) as count FROM room_members WHERE room_id = $1',
        [invitation.room_id]
      );

      if (parseInt(memberCount.rows[0].count) >= 4) {
        await client.query('ROLLBACK');
        return res.status(400).json({ error: 'La room a atteint le maximum de 4 membres' });
      }

      // Créer le membre avec role: null
      await client.query(
        'INSERT INTO room_members (room_id, user_id, role, joined_at) VALUES ($1, $2, NULL, NOW())',
        [invitation.room_id, req.user.id]
      );

      // Mettre à jour l'invitation
      await client.query(
        'UPDATE invitations SET status = $1 WHERE id = $2',
        ['accepted', id]
      );

      // Créer un message IA demandant le rôle
      const welcomeMessageContent = `Bonjour ${req.user.username} ! Veuillez définir votre rôle dans l'équipe.`;
      const welcomeMessage = await client.query(
        `INSERT INTO messages (room_id, user_id, type, content, status, created_at)
         VALUES ($1, NULL, 'ai', $2, 'sent', NOW())
         RETURNING *`,
        [invitation.room_id, welcomeMessageContent]
      );

      await client.query('COMMIT');

      res.json({
        message: 'Invitation acceptée',
        roomId: invitation.room_id,
        welcomeMessage: welcomeMessage.rows[0],
      });
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  } catch (error) {
    console.error('Erreur lors de l\'acceptation de l\'invitation:', error);
    res.status(500).json({ error: 'Erreur lors de l\'acceptation de l\'invitation' });
  }
});

/**
 * @swagger
 * /api/invitations/{id}/reject:
 *   post:
 *     summary: Refuser une invitation
 *     tags: [Invitations]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *     responses:
 *       200:
 *         description: Invitation refusée
 *       404:
 *         description: Invitation introuvable
 */
router.post('/:id/reject', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Valider le format UUID
    if (!z.string().uuid().safeParse(id).success) {
      return res.status(400).json({ error: 'ID d\'invitation invalide' });
    }

    const result = await pool.query(
      'UPDATE invitations SET status = $1 WHERE id = $2 AND recipient_id = $3 RETURNING *',
      ['rejected', id, req.user.id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Invitation introuvable' });
    }

    res.json({ message: 'Invitation refusée' });
  } catch (error) {
    console.error('Erreur lors du refus de l\'invitation:', error);
    res.status(500).json({ error: 'Erreur lors du refus de l\'invitation' });
  }
});

export default router;

