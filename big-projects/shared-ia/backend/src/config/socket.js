import jwt from 'jsonwebtoken';
import { pool } from './database.js';
import { sendMessageToAI, retryAIMessage } from './ai-handler.js';

// Stockage des utilisateurs connectés : userId -> socketId
const connectedUsers = new Map();
let ioInstance = null;

// Middleware d'authentification Socket.io
export function setupSocketIO(io) {
  ioInstance = io;
  // Middleware d'authentification
  io.use(async (socket, next) => {
    try {
      const token = socket.handshake.auth?.token || socket.handshake.headers?.authorization?.replace('Bearer ', '');
      
      if (!token) {
        return next(new Error('Token manquant'));
      }

      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      
      // Vérifier que l'utilisateur existe toujours
      const result = await pool.query('SELECT id, username FROM users WHERE id = $1', [decoded.userId]);
      
      if (result.rows.length === 0) {
        return next(new Error('Utilisateur introuvable'));
      }

      socket.userId = decoded.userId;
      socket.username = result.rows[0].username;
      next();
    } catch (error) {
      next(new Error('Token invalide'));
    }
  });

  io.on('connection', (socket) => {
    console.log(`Utilisateur connecte: ${socket.username} (${socket.userId})`);
    
    // Si l'utilisateur était déjà connecté, remplacer l'ancienne connexion
    const oldSocketId = connectedUsers.get(socket.userId);
    if (oldSocketId && oldSocketId !== socket.id) {
      const oldSocket = io.sockets.sockets.get(oldSocketId);
      if (oldSocket) {
        oldSocket.disconnect();
      }
    }
    
    connectedUsers.set(socket.userId, socket.id);

    // Notifier la présence en ligne
    socket.broadcast.emit('user-presence', {
      userId: socket.userId,
      username: socket.username,
      status: 'online',
    });

    // Émettre la connexion réussie avec synchronisation d'état
    socket.emit('authenticated', { 
      userId: socket.userId, 
      username: socket.username,
      reconnect: !!oldSocketId, // Indique si c'est une reconnexion
    });

    // Gestion des rooms
    socket.on('join-room', async (roomId) => {
      try {
        // Vérifier que l'utilisateur est membre de la room
        const result = await pool.query(
          'SELECT * FROM room_members WHERE user_id = $1 AND room_id = $2',
          [socket.userId, roomId]
        );

        if (result.rows.length === 0) {
          socket.emit('error', { message: 'Vous n\'etes pas membre de cette room' });
          return;
        }

        socket.join(`room:${roomId}`);
        console.log(`${socket.username} a rejoint la room ${roomId}`);

        // Vérifier que la room existe
        const roomCheck = await pool.query('SELECT id FROM rooms WHERE id = $1', [roomId]);
        if (roomCheck.rows.length === 0) {
          socket.emit('room-not-found', { roomId });
          return;
        }

        // Récupérer les infos de la room
        const roomResult = await pool.query(
          `SELECT r.*, 
            json_agg(json_build_object('id', u.id, 'username', u.username, 'role', rm.role)) as members
           FROM rooms r
           LEFT JOIN room_members rm ON r.id = rm.room_id
           LEFT JOIN users u ON rm.user_id = u.id
           WHERE r.id = $1
           GROUP BY r.id`,
          [roomId]
        );

        // Récupérer les messages
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

        // Récupérer les membres avec leur statut de présence
        const membersWithPresence = (roomResult.rows[0]?.members || []).map(member => ({
          ...member,
          isOnline: connectedUsers.has(member.id),
        }));

        socket.emit('room-joined', {
          room: roomResult.rows[0],
          members: membersWithPresence,
          messages: messagesResult.rows,
        });
      } catch (error) {
        console.error('Erreur lors de la jointure à la room:', error);
        socket.emit('error', { message: 'Erreur lors de la jointure à la room' });
      }
    });

    socket.on('leave-room', (roomId) => {
      socket.leave(`room:${roomId}`);
      console.log(`${socket.username} a quitte la room ${roomId}`);
    });

    // Gestion des messages - Phase 4 : Validation Collaborative
    socket.on('send-message', async (data) => {
      const client = await pool.connect();
      try {
        const { roomId, content } = data;

        // Validation
        if (!roomId || !content || typeof content !== 'string' || content.trim().length === 0) {
          socket.emit('error', { message: 'Room ID et contenu requis' });
          return;
        }

        await client.query('BEGIN');

        // Vérifier que l'utilisateur est membre de la room
        const memberCheck = await client.query(
          'SELECT rm.*, u.username FROM room_members rm INNER JOIN users u ON rm.user_id = u.id WHERE rm.user_id = $1 AND rm.room_id = $2',
          [socket.userId, roomId]
        );

        if (memberCheck.rows.length === 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous n\'etes pas membre de cette room' });
          return;
        }

        const member = memberCheck.rows[0];

        // Vérifier que l'utilisateur a défini son rôle
        if (!member.role) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous devez definir votre role avant d\'envoyer un message' });
          return;
        }

        // Récupérer tous les autres membres de la room (sauf l'auteur)
        const otherMembersResult = await client.query(
          'SELECT user_id FROM room_members WHERE room_id = $1 AND user_id != $2',
          [roomId, socket.userId]
        );
        
        // Compter combien d'autres membres sont actuellement connectés dans cette room Socket.io
        const roomSockets = io.sockets.adapter.rooms.get(`room:${roomId}`);
        const connectedOtherMemberIds = new Set();
        
        if (roomSockets) {
          for (const socketId of roomSockets) {
            const roomSocket = io.sockets.sockets.get(socketId);
            if (roomSocket && roomSocket.userId && roomSocket.userId !== socket.userId) {
              connectedOtherMemberIds.add(roomSocket.userId);
            }
          }
        }
        
        const otherMembersCount = otherMembersResult.rows.filter(m => 
          connectedOtherMemberIds.has(m.user_id)
        ).length;

        // Vérifier s'il existe déjà un message en attente de validation (détection de conflit)
        // Ne détecter un conflit que s'il y a d'autres membres dans la room
        const pendingCheck = await client.query(
          'SELECT id FROM messages WHERE room_id = $1 AND status = $2',
          [roomId, 'pending_validation']
        );

        // Si un message est déjà en attente ET qu'il y a d'autres membres, créer un conflit
        // Si l'auteur est seul, on ne crée pas de conflit car il n'y a personne pour voter
        if (pendingCheck.rows.length > 0 && otherMembersCount > 0) {
          // Créer le nouveau message en "pending_validation"
          const messageResult = await client.query(
            `INSERT INTO messages (room_id, user_id, type, content, status, created_at)
             VALUES ($1, $2, 'user', $3, 'pending_validation', NOW())
             RETURNING *`,
            [roomId, socket.userId, content.trim()]
          );

          const newMessage = messageResult.rows[0];

          // Récupérer tous les messages en "pending_validation" de cette room (anciens + nouveau)
          const allPendingMessages = await client.query(
            `SELECT m.*, u.username, rm.role
             FROM messages m
             INNER JOIN users u ON m.user_id = u.id
             INNER JOIN room_members rm ON m.user_id = rm.user_id AND m.room_id = rm.room_id
             WHERE m.room_id = $1 AND m.status = 'pending_validation'
             ORDER BY m.created_at ASC`,
            [roomId]
          );

          // Vérifier s'il existe déjà un conflit actif pour cette room
          const existingConflict = await client.query(
            'SELECT * FROM message_conflicts WHERE room_id = $1 AND status = $2',
            [roomId, 'voting']
          );

          let conflictId;

          if (existingConflict.rows.length > 0) {
            // Utiliser le conflit existant
            conflictId = existingConflict.rows[0].id;

            // Ajouter le nouveau message au conflit existant
            await client.query(
              'INSERT INTO conflict_messages (conflict_id, message_id) VALUES ($1, $2) ON CONFLICT DO NOTHING',
              [conflictId, newMessage.id]
            );
          } else {
            // Créer un nouveau MessageConflict
            const conflictResult = await client.query(
              `INSERT INTO message_conflicts (room_id, status, created_at)
               VALUES ($1, 'voting', NOW())
               RETURNING *`,
              [roomId]
            );

            conflictId = conflictResult.rows[0].id;

            // Créer des entrées ConflictMessage pour tous les messages en conflit
            for (const msg of allPendingMessages.rows) {
              await client.query(
                'INSERT INTO conflict_messages (conflict_id, message_id) VALUES ($1, $2)',
                [conflictId, msg.id]
              );
            }
          }

          await client.query('COMMIT');

          // Broadcast événement "conflict-detected"
          io.to(`room:${roomId}`).emit('conflict-detected', {
            conflictId,
            messages: allPendingMessages.rows.map(msg => ({
              ...msg,
              role: msg.role,
            })),
          });

          console.log(`Conflit detecte dans room ${roomId} avec ${allPendingMessages.rows.length} messages`);
          return;
        }

        // Limiter la taille du message (5000 caractères max)
        if (content.length > 5000) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Le message est trop long (maximum 5000 caracteres)' });
          return;
        }

        // Si l'auteur est seul dans la room, valider automatiquement le message
        const shouldAutoValidate = otherMembersCount === 0;

        // Créer le message en base avec status "pending_validation" ou "validated" selon le cas
        const messageResult = await client.query(
          `INSERT INTO messages (room_id, user_id, type, content, status, created_at)
           VALUES ($1, $2, 'user', $3, $4, NOW())
           RETURNING *`,
          [roomId, socket.userId, content.trim(), shouldAutoValidate ? 'validated' : 'pending_validation']
        );

        const message = messageResult.rows[0];

        await client.query('COMMIT');

        // Récupérer le rôle du membre
        const role = member.role;

        // Préparer le message pour le broadcast
        const messageToBroadcast = {
          ...message,
          username: socket.username,
          role: role,
        };

        if (shouldAutoValidate) {
          // Si validation automatique, émettre d'abord le message validé pour qu'il s'affiche
          const validatedMessageResult = await pool.query(
            `SELECT m.*, u.username, rm.role
             FROM messages m
             INNER JOIN users u ON m.user_id = u.id
             INNER JOIN room_members rm ON m.user_id = rm.user_id AND m.room_id = rm.room_id
             WHERE m.id = $1`,
            [message.id]
          );
          
          // Émettre l'événement que le message est validé (pour l'ajouter à la liste)
          io.to(`room:${roomId}`).emit('message-validated', {
            message: validatedMessageResult.rows[0],
          });
          
          // Ensuite, envoyer directement à l'IA (avec un petit délai pour s'assurer que le message est affiché)
          setTimeout(() => {
            sendMessageToAI(io, roomId, message.id).catch((error) => {
              console.error('Erreur lors de l\'envoi automatique à l\'IA:', error);
            });
          }, 100);
          
          console.log(`Message automatiquement validé et envoyé à l'IA (auteur seul) par ${socket.username} dans room ${roomId}`);
        } else {
          // Broadcast le message en attente à tous les membres de la room
          io.to(`room:${roomId}`).emit('new-pending-message', messageToBroadcast);
          console.log(`Message en attente de validation envoye par ${socket.username} dans room ${roomId}`);
        }
      } catch (error) {
        await client.query('ROLLBACK');
        console.error('Erreur lors de l\'envoi du message:', error);
        socket.emit('error', { message: 'Erreur lors de l\'envoi du message' });
      } finally {
        client.release();
      }
    });

    // Validation de messages - Phase 4
    socket.on('retract-message', async (data) => {
      const client = await pool.connect();
      try {
        const { messageId } = data;

        if (!messageId) {
          socket.emit('error', { message: 'Message ID requis' });
          return;
        }

        await client.query('BEGIN');

        // Récupérer le message
        const messageResult = await client.query(
          'SELECT * FROM messages WHERE id = $1',
          [messageId]
        );

        if (messageResult.rows.length === 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Message introuvable' });
          return;
        }

        const message = messageResult.rows[0];

        // Vérifier que l'utilisateur est l'auteur
        if (message.user_id !== socket.userId) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous n\'etes pas l\'auteur de ce message' });
          return;
        }

        // Vérifier qu'aucune validation n'a été effectuée
        const validationCheck = await client.query(
          'SELECT COUNT(*) as count FROM message_validations WHERE message_id = $1',
          [messageId]
        );

        if (parseInt(validationCheck.rows[0].count) > 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Le message a deja ete valide, vous ne pouvez plus le retirer' });
          return;
        }

        // Supprimer le message
        await client.query('DELETE FROM messages WHERE id = $1', [messageId]);

        await client.query('COMMIT');

        // Broadcast la suppression
        io.to(`room:${message.room_id}`).emit('message-retracted', { messageId });

        console.log(`Message ${messageId} retire par ${socket.username}`);
      } catch (error) {
        await client.query('ROLLBACK');
        console.error('Erreur lors du retrait du message:', error);
        socket.emit('error', { message: 'Erreur lors du retrait du message' });
      } finally {
        client.release();
      }
    });

    socket.on('validate-message', async (data) => {
      const client = await pool.connect();
      try {
        const { messageId, action, addition, comment } = data;

        if (!messageId || !action) {
          socket.emit('error', { message: 'Message ID et action requis' });
          return;
        }

        if (!['validated', 'added', 'rejected'].includes(action)) {
          socket.emit('error', { message: 'Action invalide' });
          return;
        }

        await client.query('BEGIN');

        // Récupérer le message
        const messageResult = await client.query(
          'SELECT * FROM messages WHERE id = $1',
          [messageId]
        );

        if (messageResult.rows.length === 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Message introuvable' });
          return;
        }

        const message = messageResult.rows[0];

        // Vérifier que le message est en attente de validation
        if (message.status !== 'pending_validation') {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Ce message n\'est pas en attente de validation' });
          return;
        }

        // Vérifier que l'utilisateur est membre de la room
        const memberCheck = await client.query(
          'SELECT rm.id, rm.role, u.username FROM room_members rm INNER JOIN users u ON rm.user_id = u.id WHERE rm.user_id = $1 AND rm.room_id = $2',
          [socket.userId, message.room_id]
        );

        if (memberCheck.rows.length === 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous n\'etes pas membre de cette room' });
          return;
        }

        const member = memberCheck.rows[0];

        // Vérifier que l'utilisateur n'est pas l'auteur
        if (message.user_id === socket.userId) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous ne pouvez pas valider votre propre message' });
          return;
        }

        // Vérifier que le membre n'a pas déjà validé ce message
        const existingValidation = await client.query(
          'SELECT * FROM message_validations WHERE message_id = $1 AND member_id = $2',
          [messageId, member.id]
        );

        if (existingValidation.rows.length > 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous avez deja valide ce message' });
          return;
        }

        // Gérer le rejet
        if (action === 'rejected') {
          // Créer la validation avec rejet
          await client.query(
            `INSERT INTO message_validations (message_id, member_id, action, comment, created_at)
             VALUES ($1, $2, 'rejected', $3, NOW())`,
            [messageId, member.id, comment || null]
          );

          // Mettre à jour le message : status = "rejected"
          await client.query(
            'UPDATE messages SET status = $1 WHERE id = $2',
            ['rejected', messageId]
          );

          await client.query('COMMIT');

          // Broadcast le rejet
          io.to(`room:${message.room_id}`).emit('message-rejected', {
            messageId,
            validation: {
              userId: socket.userId,
              username: socket.username,
              role: member.role,
              comment: comment || null,
            },
          });

          console.log(`Message ${messageId} rejete par ${socket.username}`);
          return;
        }

        // Gérer validated ou added
        if (action === 'added' && (!addition || typeof addition !== 'string' || addition.trim().length === 0)) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Le texte a ajouter est requis pour l\'action "added"' });
          return;
        }

        // Créer la validation
        await client.query(
          `INSERT INTO message_validations (message_id, member_id, action, addition, created_at)
           VALUES ($1, $2, $3, $4, NOW())`,
          [messageId, member.id, action, action === 'added' ? addition.trim() : null]
        );

        // Compter les validations (action != "rejected")
        const validationsResult = await client.query(
          `SELECT COUNT(*) as count FROM message_validations mv
           INNER JOIN room_members rm ON mv.member_id = rm.id
           WHERE mv.message_id = $1 AND mv.action != 'rejected'`,
          [messageId]
        );

        const validationsCount = parseInt(validationsResult.rows[0].count);

        // Récupérer tous les autres membres de la room (sauf l'auteur du message)
        const membersResult = await client.query(
          'SELECT user_id FROM room_members WHERE room_id = $1 AND user_id != $2',
          [message.room_id, message.user_id]
        );

        // Compter uniquement les membres actuellement connectés dans la room Socket.io
        const roomSockets = io.sockets.adapter.rooms.get(`room:${message.room_id}`);
        const connectedMemberIds = new Set();
        
        if (roomSockets) {
          for (const socketId of roomSockets) {
            const socket = io.sockets.sockets.get(socketId);
            if (socket && socket.userId) {
              connectedMemberIds.add(socket.userId);
            }
          }
        }
        
        // Compter combien d'autres membres (sauf l'auteur) sont connectés
        const totalMembers = membersResult.rows.filter(m => 
          connectedMemberIds.has(m.user_id)
        ).length;

        // Récupérer toutes les validations pour le broadcast
        const allValidationsResult = await client.query(
          `SELECT mv.*, u.username, rm.role
           FROM message_validations mv
           INNER JOIN room_members rm ON mv.member_id = rm.id
           INNER JOIN users u ON rm.user_id = u.id
           WHERE mv.message_id = $1
           ORDER BY mv.created_at ASC`,
          [messageId]
        );

        // Si toutes les validations sont présentes, mettre à jour le status à "validated"
        if (validationsCount >= totalMembers) {
          await client.query(
            'UPDATE messages SET status = $1 WHERE id = $2',
            ['validated', messageId]
          );
        }

        await client.query('COMMIT');

        // Broadcast la mise à jour de validation
        io.to(`room:${message.room_id}`).emit('validation-update', {
          messageId,
          validation: {
            userId: socket.userId,
            username: socket.username,
            role: member.role,
            action: action,
            addition: action === 'added' ? addition.trim() : null,
          },
          validationsCount,
          totalMembers,
          allValidations: allValidationsResult.rows,
        });

        // Si toutes les validations sont présentes, déclencher l'envoi à l'IA
        if (validationsCount >= totalMembers) {
          // Récupérer le message validé avec username et role
          const validatedMessageResult = await pool.query(
            `SELECT m.*, u.username, rm.role
             FROM messages m
             INNER JOIN users u ON m.user_id = u.id
             INNER JOIN room_members rm ON m.user_id = rm.user_id AND m.room_id = rm.room_id
             WHERE m.id = $1`,
            [messageId]
          );
          
          // Émettre l'événement que le message est validé
          io.to(`room:${message.room_id}`).emit('message-validated', {
            message: validatedMessageResult.rows[0],
          });
          
          // Appeler la fonction d'envoi à l'IA
          sendMessageToAI(io, message.room_id, messageId).catch((error) => {
            console.error('Erreur lors de l\'envoi à l\'IA:', error);
          });
        }

        console.log(`Message ${messageId} valide par ${socket.username} (${action})`);
      } catch (error) {
        await client.query('ROLLBACK');
        console.error('Erreur lors de la validation du message:', error);
        socket.emit('error', { message: 'Erreur lors de la validation du message' });
      } finally {
        client.release();
      }
    });

    // Indicateur "en train d'écrire" - Phase 3
    const typingUsers = new Map(); // roomId -> Set of userIds

    socket.on('typing', async (data) => {
      try {
        const { roomId, isTyping } = data;

        if (!roomId) {
          return;
        }

        // Vérifier que l'utilisateur est membre de la room
        const memberCheck = await pool.query(
          'SELECT * FROM room_members WHERE user_id = $1 AND room_id = $2',
          [socket.userId, roomId]
        );

        if (memberCheck.rows.length === 0) {
          return;
        }

        if (isTyping) {
          if (!typingUsers.has(roomId)) {
            typingUsers.set(roomId, new Set());
          }
          typingUsers.get(roomId).add(socket.userId);
        } else {
          if (typingUsers.has(roomId)) {
            typingUsers.get(roomId).delete(socket.userId);
            if (typingUsers.get(roomId).size === 0) {
              typingUsers.delete(roomId);
            }
          }
        }

        // Broadcast l'état de typing à tous les membres de la room (sauf l'émetteur)
        socket.to(`room:${roomId}`).emit('typing-update', {
          userId: socket.userId,
          username: socket.username,
          isTyping: isTyping,
        });
      } catch (error) {
        console.error('Erreur lors de la gestion du typing:', error);
      }
    });

    // Gestion des conflits - Phase 6
    socket.on('vote-message', async (data) => {
      const client = await pool.connect();
      try {
        const { conflictId, messageId } = data;

        if (!conflictId || !messageId) {
          socket.emit('error', { message: 'Conflict ID et Message ID requis' });
          return;
        }

        await client.query('BEGIN');

        // Vérifier que le conflit existe et est en "voting"
        const conflictResult = await client.query(
          'SELECT * FROM message_conflicts WHERE id = $1 AND status = $2',
          [conflictId, 'voting']
        );

        if (conflictResult.rows.length === 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Conflit introuvable ou deja resolu' });
          return;
        }

        const conflict = conflictResult.rows[0];

        // Vérifier que l'utilisateur est membre de la room
        const memberCheck = await client.query(
          'SELECT * FROM room_members WHERE user_id = $1 AND room_id = $2',
          [socket.userId, conflict.room_id]
        );

        if (memberCheck.rows.length === 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous n\'etes pas membre de cette room' });
          return;
        }

        // Vérifier que le message fait partie du conflit
        const conflictMessageCheck = await client.query(
          'SELECT * FROM conflict_messages WHERE conflict_id = $1 AND message_id = $2',
          [conflictId, messageId]
        );

        if (conflictMessageCheck.rows.length === 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Ce message ne fait pas partie de ce conflit' });
          return;
        }

        // Vérifier que l'utilisateur n'a pas déjà voté pour ce conflit
        const existingVote = await client.query(
          'SELECT * FROM votes WHERE conflict_id = $1 AND user_id = $2',
          [conflictId, socket.userId]
        );

        if (existingVote.rows.length > 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous avez deja vote pour ce conflit' });
          return;
        }

        // Créer le vote
        await client.query(
          'INSERT INTO votes (conflict_id, user_id, message_id, created_at) VALUES ($1, $2, $3, NOW())',
          [conflictId, socket.userId, messageId]
        );

        // Compter les votes
        const votesResult = await client.query(
          'SELECT COUNT(*) as count FROM votes WHERE conflict_id = $1',
          [conflictId]
        );

        const votesCount = parseInt(votesResult.rows[0].count);

        // Compter les membres de la room
        const membersResult = await client.query(
          'SELECT COUNT(*) as count FROM room_members WHERE room_id = $1',
          [conflict.room_id]
        );

        const totalMembers = parseInt(membersResult.rows[0].count);

        // Si tous les membres ont voté, résoudre le conflit
        if (votesCount >= totalMembers) {
          // Compter les votes par message
          const votesByMessage = await client.query(
            `SELECT message_id, COUNT(*) as vote_count
             FROM votes
             WHERE conflict_id = $1
             GROUP BY message_id
             ORDER BY vote_count DESC`,
            [conflictId]
          );

          // Déterminer le gagnant (majorité simple)
          const winner = votesByMessage.rows[0];
          const winnerId = winner.message_id;

          // Récupérer tous les messages du conflit
          const allConflictMessages = await client.query(
            'SELECT message_id FROM conflict_messages WHERE conflict_id = $1',
            [conflictId]
          );

          // Supprimer les messages perdants
          const losingMessageIds = allConflictMessages.rows
            .map(row => row.message_id)
            .filter(id => id !== winnerId);

          if (losingMessageIds.length > 0) {
            await client.query(
              `DELETE FROM messages WHERE id = ANY($1::uuid[])`,
              [losingMessageIds]
            );
          }

          // Mettre à jour le conflit : status = "resolved", winnerId, resolvedAt
          await client.query(
            `UPDATE message_conflicts 
             SET status = 'resolved', winner_id = $1, resolved_at = NOW()
             WHERE id = $2`,
            [winnerId, conflictId]
          );

          await client.query('COMMIT');

          // Récupérer le message gagnant avec ses infos
          const winnerMessage = await pool.query(
            `SELECT m.*, u.username, rm.role
             FROM messages m
             INNER JOIN users u ON m.user_id = u.id
             INNER JOIN room_members rm ON m.user_id = rm.user_id AND m.room_id = rm.room_id
             WHERE m.id = $1`,
            [winnerId]
          );

          // Broadcast événement "conflict-resolved"
          io.to(`room:${conflict.room_id}`).emit('conflict-resolved', {
            conflictId,
            winnerId,
            message: {
              ...winnerMessage.rows[0],
              role: winnerMessage.rows[0].role,
            },
          });

          // Le message gagnant continue le processus de validation normal
          // Il est déjà en "pending_validation", donc il sera affiché normalement
          io.to(`room:${conflict.room_id}`).emit('new-pending-message', {
            ...winnerMessage.rows[0],
            role: winnerMessage.rows[0].role,
          });

          console.log(`Conflit ${conflictId} resolu, message gagnant: ${winnerId}`);
        } else {
          // Sinon, broadcast "vote-update"
          await client.query('COMMIT');

          io.to(`room:${conflict.room_id}`).emit('vote-update', {
            conflictId,
            votesCount,
            totalMembers,
          });

          console.log(`Vote enregistre pour conflit ${conflictId} (${votesCount}/${totalMembers})`);
        }
      } catch (error) {
        await client.query('ROLLBACK');
        console.error('Erreur lors du vote:', error);
        socket.emit('error', { message: 'Erreur lors du vote' });
      } finally {
        client.release();
      }
    });

    // Édition et suppression de messages - Phase 7
    socket.on('edit-message', async (data) => {
      const client = await pool.connect();
      try {
        const { messageId, newContent } = data;

        if (!messageId || !newContent || typeof newContent !== 'string' || newContent.trim().length === 0) {
          socket.emit('error', { message: 'Message ID et nouveau contenu requis' });
          return;
        }

        // Limiter la taille du message (5000 caractères max)
        if (newContent.length > 5000) {
          socket.emit('error', { message: 'Le message est trop long (maximum 5000 caracteres)' });
          return;
        }

        await client.query('BEGIN');

        // Récupérer le message
        const messageResult = await client.query(
          'SELECT * FROM messages WHERE id = $1',
          [messageId]
        );

        if (messageResult.rows.length === 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Message introuvable' });
          return;
        }

        const message = messageResult.rows[0];

        // Vérifier que l'utilisateur est l'auteur
        if (message.user_id !== socket.userId) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous n\'etes pas l\'auteur de ce message' });
          return;
        }

        // Vérifier que le message n'est pas en "pending_validation"
        if (message.status === 'pending_validation') {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous ne pouvez pas editer un message en cours de validation' });
          return;
        }

        // Vérifier que le message est de type "user"
        if (message.type !== 'user') {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous ne pouvez editer que vos propres messages utilisateur' });
          return;
        }

        // Supprimer TOUS les messages de la room créés après ce message
        const deletedMessagesResult = await client.query(
          'DELETE FROM messages WHERE room_id = $1 AND created_at > $2 RETURNING id',
          [message.room_id, message.created_at]
        );

        const deletedMessageIds = deletedMessagesResult.rows.map(row => row.id);
        const deletedAt = new Date();

        // Mettre à jour le message : contenu, editedAt, status = "pending_validation"
        const updatedMessageResult = await client.query(
          `UPDATE messages 
           SET content = $1, edited_at = NOW(), status = 'pending_validation'
           WHERE id = $2
           RETURNING *`,
          [newContent.trim(), messageId]
        );

        await client.query('COMMIT');

        // Récupérer les infos du membre pour le broadcast
        const memberResult = await pool.query(
          `SELECT rm.role, u.username
           FROM room_members rm
           INNER JOIN users u ON rm.user_id = u.id
           WHERE rm.user_id = $1 AND rm.room_id = $2`,
          [socket.userId, message.room_id]
        );

        const role = memberResult.rows[0]?.role || null;
        const username = memberResult.rows[0]?.username || socket.username;

        // Préparer le message mis à jour pour le broadcast
        const updatedMessage = {
          ...updatedMessageResult.rows[0],
          username,
          role,
        };

        // Broadcast événement "message-edited"
        io.to(`room:${message.room_id}`).emit('message-edited', {
          message: updatedMessage,
          deletedAfter: deletedAt,
          deletedMessageIds,
        });

        // Broadcast le message comme nouveau message en attente
        io.to(`room:${message.room_id}`).emit('new-pending-message', updatedMessage);

        console.log(`Message ${messageId} edite par ${socket.username}, ${deletedMessageIds.length} messages supprimes`);
      } catch (error) {
        await client.query('ROLLBACK');
        console.error('Erreur lors de l\'edition du message:', error);
        socket.emit('error', { message: 'Erreur lors de l\'edition du message' });
      } finally {
        client.release();
      }
    });

    socket.on('delete-message', async (data) => {
      const client = await pool.connect();
      try {
        const { messageId } = data;

        if (!messageId) {
          socket.emit('error', { message: 'Message ID requis' });
          return;
        }

        await client.query('BEGIN');

        // Récupérer le message
        const messageResult = await client.query(
          'SELECT * FROM messages WHERE id = $1',
          [messageId]
        );

        if (messageResult.rows.length === 0) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Message introuvable' });
          return;
        }

        const message = messageResult.rows[0];

        // Vérifier que l'utilisateur est l'auteur
        if (message.user_id !== socket.userId) {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous n\'etes pas l\'auteur de ce message' });
          return;
        }

        // Vérifier que le message est de type "user"
        if (message.type !== 'user') {
          await client.query('ROLLBACK');
          socket.emit('error', { message: 'Vous ne pouvez supprimer que vos propres messages utilisateur' });
          return;
        }

        // Supprimer le message + tous ceux qui suivent
        const deletedMessagesResult = await client.query(
          'DELETE FROM messages WHERE room_id = $1 AND created_at >= $2 RETURNING id',
          [message.room_id, message.created_at]
        );

        const deletedMessageIds = deletedMessagesResult.rows.map(row => row.id);
        const deletedAt = new Date();

        await client.query('COMMIT');

        // Broadcast événement "messages-deleted"
        io.to(`room:${message.room_id}`).emit('messages-deleted', {
          deletedFrom: deletedAt,
          deletedMessageIds,
          roomId: message.room_id,
        });

        console.log(`Message ${messageId} et ${deletedMessageIds.length - 1} messages suivants supprimes par ${socket.username}`);
      } catch (error) {
        await client.query('ROLLBACK');
        console.error('Erreur lors de la suppression du message:', error);
        socket.emit('error', { message: 'Erreur lors de la suppression du message' });
      } finally {
        client.release();
      }
    });

    // Retry manuel d'un message en erreur - Phase 5
    socket.on('retry-ai-message', async (data) => {
      try {
        const { messageId, roomId } = data;

        if (!messageId || !roomId) {
          socket.emit('error', { message: 'Message ID et Room ID requis' });
          return;
        }

        // Vérifier que l'utilisateur est membre de la room
        const memberCheck = await pool.query(
          'SELECT * FROM room_members WHERE user_id = $1 AND room_id = $2',
          [socket.userId, roomId]
        );

        if (memberCheck.rows.length === 0) {
          socket.emit('error', { message: 'Vous n\'etes pas membre de cette room' });
          return;
        }

        // Vérifier que le message appartient à cette room
        const messageCheck = await pool.query(
          'SELECT * FROM messages WHERE id = $1 AND room_id = $2',
          [messageId, roomId]
        );

        if (messageCheck.rows.length === 0) {
          socket.emit('error', { message: 'Message introuvable dans cette room' });
          return;
        }

        // Appeler la fonction de retry
        await retryAIMessage(io, roomId, messageId);

        console.log(`Retry manuel pour message ${messageId} par ${socket.username}`);
      } catch (error) {
        console.error('Erreur lors du retry manuel:', error);
        socket.emit('error', { message: error.message || 'Erreur lors du retry' });
      }
    });

    // Synchronisation d'état après reconnexion - Phase 8
    socket.on('sync-state', async (data) => {
      try {
        const { roomIds } = data || {};

        if (!roomIds || !Array.isArray(roomIds)) {
          return;
        }

        // Pour chaque room, récupérer l'état actuel
        const state = {
          rooms: [],
          pendingInvitations: [],
        };

        for (const roomId of roomIds) {
          // Vérifier que l'utilisateur est membre
          const memberCheck = await pool.query(
            'SELECT * FROM room_members WHERE user_id = $1 AND room_id = $2',
            [socket.userId, roomId]
          );

          if (memberCheck.rows.length === 0) {
            continue;
          }

          // Récupérer les messages en attente de validation
          const pendingMessages = await pool.query(
            `SELECT m.*, u.username, rm.role
             FROM messages m
             LEFT JOIN users u ON m.user_id = u.id
             LEFT JOIN room_members rm ON m.user_id = rm.user_id AND m.room_id = rm.room_id
             WHERE m.room_id = $1 AND m.status = 'pending_validation'
             ORDER BY m.created_at DESC
             LIMIT 1`,
            [roomId]
          );

          // Récupérer les conflits actifs
          const activeConflicts = await pool.query(
            `SELECT mc.*, 
               json_agg(json_build_object('id', m.id, 'username', u.username, 'role', rm.role, 'content', m.content)) as messages
             FROM message_conflicts mc
             INNER JOIN conflict_messages cm ON mc.id = cm.conflict_id
             INNER JOIN messages m ON cm.message_id = m.id
             LEFT JOIN users u ON m.user_id = u.id
             LEFT JOIN room_members rm ON m.user_id = rm.user_id AND m.room_id = rm.room_id
             WHERE mc.room_id = $1 AND mc.status = 'voting'
             GROUP BY mc.id`,
            [roomId]
          );

          // Récupérer les validations en cours
          const validations = await pool.query(
            `SELECT mv.*, m.id as message_id, m.room_id
             FROM message_validations mv
             INNER JOIN messages m ON mv.message_id = m.id
             WHERE m.room_id = $1 AND m.status = 'pending_validation'`,
            [roomId]
          );

          state.rooms.push({
            roomId,
            pendingMessage: pendingMessages.rows[0] || null,
            activeConflict: activeConflicts.rows[0] || null,
            validations: validations.rows,
          });
        }

        // Récupérer les invitations en attente
        const invitations = await pool.query(
          `SELECT i.*, r.name as room_name, u.username as sender_username
           FROM invitations i
           INNER JOIN rooms r ON i.room_id = r.id
           INNER JOIN users u ON i.sender_id = u.id
           WHERE i.recipient_id = $1 AND i.status = 'pending' AND i.expires_at > NOW()`,
          [socket.userId]
        );

        state.pendingInvitations = invitations.rows;

        socket.emit('state-synced', state);
      } catch (error) {
        console.error('Erreur lors de la synchronisation d\'etat:', error);
        socket.emit('error', { message: 'Erreur lors de la synchronisation' });
      }
    });

    socket.on('disconnect', () => {
      console.log(`Utilisateur deconnecte: ${socket.username} (${socket.userId})`);
      
      // Vérifier si l'utilisateur a une autre connexion active
      const currentSocketId = connectedUsers.get(socket.userId);
      if (currentSocketId === socket.id) {
        // C'est la dernière connexion, marquer comme offline
        connectedUsers.delete(socket.userId);
        
        // Notifier la présence hors ligne
        socket.broadcast.emit('user-presence', {
          userId: socket.userId,
          username: socket.username,
          status: 'offline',
        });
      }
      
      // Nettoyer les indicateurs de typing
      for (const [roomId, userIds] of typingUsers.entries()) {
        if (userIds.has(socket.userId)) {
          userIds.delete(socket.userId);
          if (userIds.size === 0) {
            typingUsers.delete(roomId);
          } else {
            // Notifier que l'utilisateur a arrêté de taper
            io.to(`room:${roomId}`).emit('typing-update', {
              userId: socket.userId,
              username: socket.username,
              isTyping: false,
            });
          }
        }
      }
    });
  });

  return io;
}

// Helper pour obtenir l'instance io
export function getIOInstance() {
  return ioInstance;
}

// Helper pour obtenir le socket d'un utilisateur
export function getUserSocket(userId) {
  if (!ioInstance) return null;
  const socketId = connectedUsers.get(userId);
  return socketId ? ioInstance.sockets.sockets.get(socketId) : null;
}

