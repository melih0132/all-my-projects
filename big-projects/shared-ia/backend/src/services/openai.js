import OpenAI from 'openai';
import dotenv from 'dotenv';

dotenv.config();

// Configuration OpenAI
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

/**
 * Envoie un message à OpenAI avec streaming
 * @param {string} systemContext - Contexte système (rôle de l'IA)
 * @param {Array} history - Historique des messages formatés
 * @param {string} userBatch - Batch de messages utilisateur à envoyer
 * @returns {Promise<AsyncIterable>} Stream de la réponse OpenAI
 */
export async function sendToOpenAI(systemContext, history, userBatch) {
  const messages = [
    {
      role: 'system',
      content: systemContext,
    },
    ...history,
    {
      role: 'user',
      content: userBatch,
    },
  ];

  const stream = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: messages,
    temperature: 0.7,
    stream: true,
  });

  return stream;
}

/**
 * Construit le contexte système avec les rôles
 * @param {string} aiContext - Contexte IA de la room
 * @param {Array} members - Liste des membres avec leurs rôles
 * @returns {string} Contexte système formaté
 */
export function buildSystemContext(aiContext, members) {
  const rolesList = members
    .filter(m => m.role)
    .map(m => `- ${m.username} : ${m.role}`)
    .join('\n');

  return `${aiContext}

Les membres de l'équipe et leurs rôles :
${rolesList || 'Aucun rôle défini pour le moment.'}

Adapte tes réponses en fonction des rôles de chaque membre de l'équipe.`;
}

