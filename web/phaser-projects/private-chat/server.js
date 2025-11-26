const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

app.use(express.static('public'));

const users = new Map();

io.on('connection', (socket) => {
    socket.on('register', (username) => {
        users.set(socket.id, username);
        socket.emit('users', Array.from(users.values()));
        socket.broadcast.emit('userJoined', username);
    });

    socket.on('private message', (data) => {
        const recipientSocket = Array.from(users.entries())
            .find(([, name]) => name === data.to)?.[0];
            
        if (recipientSocket) {
            io.to(recipientSocket).emit('private message', {
                from: users.get(socket.id),
                message: data.message
            });
        }
    });

    socket.on('disconnect', () => {
        const username = users.get(socket.id);
        users.delete(socket.id);
        io.emit('userLeft', username);
    });
});

server.listen(3000, () => {
    console.log('Serveur de chat privé sur le port 3000');
});