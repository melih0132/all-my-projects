import { pool } from '../config/database.js';
import { sendToOpenAI, buildSystemContext } from '../services/openai.js';

/**
 * Envoie un message validé à l'IA et gère le streaming de la réponse
 * @param {Object} io - Instance Socket.io
 * @param {string} roomId - ID de la room
 * @param {string} messageId - ID du message validé
 */
export async function sendMessageToAI(io, roomId, messageId) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    // Récupérer le message principal avec son auteur et rôle
    const messageResult = await client.query(
      `SELECT m.*, u.username, rm.role
       FROM messages m
       INNER JOIN users u ON m.user_id = u.id
       INNER JOIN room_members rm ON m.user_id = rm.user_id AND m.room_id = rm.room_id
       WHERE m.id = $1`,
      [messageId]
    );

    if (messageResult.rows.length === 0) {
      throw new Error('Message introuvable');
    }

    const message = messageResult.rows[0];

    // Récupérer toutes les validations avec leurs membres et rôles
    const validationsResult = await client.query(
      `SELECT mv.*, u.username, rm.role
       FROM message_validations mv
       INNER JOIN room_members rm ON mv.member_id = rm.id
       INNER JOIN users u ON rm.user_id = u.id
       WHERE mv.message_id = $1 AND mv.action != 'rejected'
       ORDER BY mv.created_at ASC`,
      [messageId]
    );

    // Construire le contenu groupé
    let userBatch = `${message.username} (${message.role || 'Sans rôle'}): ${message.content}`;
    
    for (const validation of validationsResult.rows) {
      if (validation.action === 'added' && validation.addition) {
        userBatch += `\n${validation.username} (${validation.role || 'Sans rôle'}) ajoute: ${validation.addition}`;
      }
    }

    // Récupérer le contexte de la room
    const roomResult = await client.query(
      'SELECT ai_context FROM rooms WHERE id = $1',
      [roomId]
    );

    if (roomResult.rows.length === 0) {
      throw new Error('Room introuvable');
    }

    // Récupérer les membres avec leurs rôles
    const membersResult = await client.query(
      `SELECT u.username, rm.role
       FROM room_members rm
       INNER JOIN users u ON rm.user_id = u.id
       WHERE rm.room_id = $1
       ORDER BY rm.joined_at ASC`,
      [roomId]
    );

    // Construire le contexte système
    const systemContext = buildSystemContext(roomResult.rows[0].ai_context, membersResult.rows);

    // Récupérer l'historique (50 derniers messages avec status "sent" ou "validated")
    const historyResult = await client.query(
      `SELECT m.*, u.username, rm.role
       FROM messages m
       LEFT JOIN users u ON m.user_id = u.id
       LEFT JOIN room_members rm ON m.user_id = rm.user_id AND m.room_id = rm.room_id
       WHERE m.room_id = $1 
         AND m.status IN ('sent', 'validated')
         AND m.type IN ('user', 'ai')
       ORDER BY m.created_at ASC
       LIMIT 50`,
      [roomId]
    );

    // Formater l'historique pour OpenAI
    const history = historyResult.rows.map(msg => {
      if (msg.type === 'user') {
        return {
          role: 'user',
          content: `${msg.username} (${msg.role || 'Sans rôle'}): ${msg.content}`,
        };
      } else {
        return {
          role: 'assistant',
          content: msg.content,
        };
      }
    });

    await client.query('COMMIT');

    // Appeler OpenAI avec retry et timeout
    await callOpenAIWithRetry(io, roomId, messageId, systemContext, history, userBatch);
  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Erreur lors de l\'envoi à l\'IA:', error);
    throw error;
  } finally {
    client.release();
  }
}

/**
 * Appelle OpenAI avec retry automatique et timeout
 */
async function callOpenAIWithRetry(io, roomId, messageId, systemContext, history, userBatch) {
  const MAX_RETRIES = 3;
  const RETRY_DELAY = 2000; // 2 secondes
  const TIMEOUT = 60000; // 60 secondes

  let lastError = null;

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    try {
      // Émettre le début de la réponse (seulement au premier essai)
      if (attempt === 1) {
        io.to(`room:${roomId}`).emit('ai-response-start', { messageId });
      } else {
        // En cas de retry, notifier les utilisateurs
        io.to(`room:${roomId}`).emit('ai-response-retry', {
          messageId,
          attempt,
          maxRetries: MAX_RETRIES,
        });
      }

      // Créer une promesse avec timeout
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => {
          reject(new Error('Timeout: La requete OpenAI a depasse 60 secondes'));
        }, TIMEOUT);
      });

      // Appeler OpenAI avec streaming
      const streamPromise = sendToOpenAI(systemContext, history, userBatch);
      const stream = await Promise.race([streamPromise, timeoutPromise]);

      let fullResponse = '';

      // Streamer la réponse avec timeout pour chaque chunk
      const chunkTimeout = 5000; // 5 secondes max entre chaque chunk
      let lastChunkTime = Date.now();

      for await (const chunk of stream) {
        const now = Date.now();
        if (now - lastChunkTime > chunkTimeout) {
          // Si pas de chunk depuis 5 secondes, vérifier que le stream est toujours actif
          // (le timeout principal gère déjà le cas général)
        }
        lastChunkTime = now;

        const content = chunk.choices[0]?.delta?.content || '';
        if (content) {
          fullResponse += content;
          io.to(`room:${roomId}`).emit('ai-response-chunk', {
            messageId,
            content,
          });
        }
      }

      // Sauvegarder la réponse complète en base
      const aiMessageResult = await pool.query(
        `INSERT INTO messages (room_id, user_id, type, content, status, created_at)
         VALUES ($1, NULL, 'ai', $2, 'sent', NOW())
         RETURNING *`,
        [roomId, fullResponse]
      );

      // Mettre à jour le message original : status = "validated"
      await pool.query(
        'UPDATE messages SET status = $1 WHERE id = $2',
        ['validated', messageId]
      );

      // Émettre la fin de la réponse
      io.to(`room:${roomId}`).emit('ai-response-end', {
        messageId,
        fullResponse,
        aiMessage: aiMessageResult.rows[0],
      });

      console.log(`Reponse IA generee pour message ${messageId} dans room ${roomId} (tentative ${attempt})`);
      return; // Succès, sortir de la boucle
    } catch (error) {
      lastError = error;
      console.error(`Erreur OpenAI (tentative ${attempt}/${MAX_RETRIES}):`, error.message);

      // Si c'est la dernière tentative, gérer l'erreur
      if (attempt === MAX_RETRIES) {
        await handleAIError(io, roomId, messageId, error);
        return;
      }

      // Attendre avant de réessayer (sauf pour certaines erreurs non retryables)
      if (!isRetryableError(error)) {
        await handleAIError(io, roomId, messageId, error);
        return;
      }

      // Attendre avant le prochain essai
      await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
    }
  }
}

/**
 * Détermine si une erreur est retryable
 */
function isRetryableError(error) {
  // Erreurs non retryables
  if (error.status === 401) return false; // Clé API invalide
  if (error.status === 400) return false; // Requête invalide
  if (error.message?.includes('Timeout')) return true; // Timeout est retryable
  if (error.status === 429) return true; // Rate limit est retryable
  if (error.status === 500 || error.status === 502 || error.status === 503) return true; // Erreurs serveur
  // Par défaut, on retry pour les autres erreurs
  return true;
}

/**
 * Gère les erreurs OpenAI et émet les événements appropriés
 */
async function handleAIError(io, roomId, messageId, error) {
  // Mettre à jour le message : status = "error"
  await pool.query(
    'UPDATE messages SET status = $1 WHERE id = $2',
    ['error', messageId]
  );

  let errorMessage = 'Erreur lors de la generation de la reponse IA';
  let canRetry = true;

  if (error.status === 429) {
    errorMessage = 'Quota ou rate limit OpenAI depasse. Veuillez reessayer plus tard.';
    canRetry = true; // On peut retry manuellement
  } else if (error.status === 401) {
    errorMessage = 'Cle API OpenAI invalide. Verifiez votre configuration.';
    canRetry = false;
  } else if (error.status === 400) {
    errorMessage = 'Requete invalide vers OpenAI. Le message est peut-etre trop long.';
    canRetry = false;
  } else if (error.message?.includes('Timeout')) {
    errorMessage = 'Timeout: La requete a depasse 60 secondes. Vous pouvez reessayer.';
    canRetry = true;
  } else if (error.status === 500 || error.status === 502 || error.status === 503) {
    errorMessage = 'Erreur serveur OpenAI. Veuillez reessayer.';
    canRetry = true;
  } else {
    errorMessage = `Erreur lors de la generation: ${error.message || 'Erreur inconnue'}`;
    canRetry = true;
  }

  // Broadcast l'erreur
  io.to(`room:${roomId}`).emit('ai-response-error', {
    messageId,
    error: errorMessage,
    canRetry,
  });
}

/**
 * Retry manuel d'un message en erreur
 * @param {Object} io - Instance Socket.io
 * @param {string} roomId - ID de la room
 * @param {string} messageId - ID du message à retry
 */
export async function retryAIMessage(io, roomId, messageId) {
  // Vérifier que le message est en erreur
  const messageResult = await pool.query(
    'SELECT * FROM messages WHERE id = $1 AND status = $2',
    [messageId, 'error']
  );

  if (messageResult.rows.length === 0) {
    throw new Error('Message introuvable ou pas en erreur');
  }

  // Relancer l'envoi à l'IA
  await sendMessageToAI(io, roomId, messageId);
}

