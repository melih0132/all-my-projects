const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

app.use(express.static('public'));

const notifications = new Map(); // Stockage des notifications par utilisateur

io.on('connection', (socket) => {
    // Login utilisateur
    socket.on('login', (userId) => {
        socket.userId = userId;
        socket.join(`user-${userId}`); // Créer une room personnelle
        
        // Envoyer les notifications non lues
        const userNotifs = notifications.get(userId) || [];
        socket.emit('unread-notifications', userNotifs);
    });

    // Créer une notification
    socket.on('create-notification', (data) => {
        const { targetUserId, message, type } = data;
        const notification = {
            id: Date.now(),
            message,
            type,
            timestamp: new Date(),
            read: false
        };

        // Stocker la notification
        if (!notifications.has(targetUserId)) {
            notifications.set(targetUserId, []);
        }
        notifications.get(targetUserId).push(notification);

        // Envoyer en temps réel si l'utilisateur est connecté
        io.to(`user-${targetUserId}`).emit('new-notification', notification);
    });

    // Marquer comme lu
    socket.on('mark-read', (notificationId) => {
        const userNotifs = notifications.get(socket.userId) || [];
        const notification = userNotifs.find(n => n.id === notificationId);
        if (notification) {
            notification.read = true;
            socket.emit('notification-updated', notification);
        }
    });
});

server.listen(3000);