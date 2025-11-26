const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static('public'));

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
    console.log(`Server is listening on port ${PORT}`);
});

let players = {};
let ball = {
    x: 500,
    y: 300,
    velocityX: 0,
    velocityY: 0
};

io.on('connection', (socket) => {
    console.log('A user has connected:', socket.id);

    players[socket.id] = {
        x: Math.floor(Math.random() * 700) + 50,
        y: Math.floor(Math.random() * 500) + 50,
        playerId: socket.id,
        color: Math.floor(Math.random() * 0xFFFFFF)
    };
 
    socket.emit('currentPlayers', players);
    socket.emit('ballPosition', ball);
    socket.broadcast.emit('newPlayer', players[socket.id]);

    socket.on('disconnect', () => {
        delete players[socket.id];
        io.emit('playerDisconnected', socket.id);
    });

    socket.on('playerMovement', (movementData) => {
        if (players[socket.id]) {
            players[socket.id].x = movementData.x;
            players[socket.id].y = movementData.y;
            socket.broadcast.emit('playerMovement', players[socket.id]);
        }
    });

    socket.on('updateBall', (ballData) => {
        ball.x = ballData.x;
        ball.y = ballData.y;

        io.emit('ballPosition', ball);
    });
});