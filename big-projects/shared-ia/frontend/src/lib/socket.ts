import { io, Socket } from 'socket.io-client';

const SOCKET_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';

let socket: Socket | null = null;

export function getSocket(): Socket {
  if (!socket) {
    const token = localStorage.getItem('token');
    
    socket = io(SOCKET_URL, {
      auth: {
        token: token || '',
      },
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: Infinity,
      timeout: 20000,
    });

    socket.on('connect', () => {
      console.log('Socket.io connecté');
    });

    socket.on('disconnect', (reason) => {
      console.log('Socket.io déconnecté:', reason);
      if (reason === 'io server disconnect' && socket) {
        // Le serveur a déconnecté le socket, il faut se reconnecter manuellement
        socket.connect();
      }
    });

    socket.on('reconnect', (attemptNumber) => {
      console.log('Socket.io reconnecté après', attemptNumber, 'tentatives');
    });

    socket.on('reconnect_attempt', (attemptNumber) => {
      console.log('Tentative de reconnexion', attemptNumber);
    });

    socket.on('reconnect_error', (error) => {
      console.error('Erreur de reconnexion:', error);
    });

    socket.on('reconnect_failed', () => {
      console.error('Échec de la reconnexion');
    });

    socket.on('error', (error) => {
      console.error('Erreur Socket.io:', error);
    });
  }

  return socket;
}

export function disconnectSocket() {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
}

export function reconnectSocket() {
  disconnectSocket();
  return getSocket();
}

export function updateSocketAuth(token: string) {
  if (socket) {
    socket.auth = { token };
    socket.disconnect();
    socket.connect();
  }
}

