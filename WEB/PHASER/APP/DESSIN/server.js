const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

app.use(express.static('public'));

io.on('connection', (socket) => {
    console.log('Nouvel artiste connecté');

    socket.on('drawing', (data) => {
        socket.broadcast.emit('drawing', data);
    });

    socket.on('clear', () => {
        io.emit('clear');
    });
});

server.listen(3000, () => {
    console.log('Serveur de dessin sur le port 3000');
});