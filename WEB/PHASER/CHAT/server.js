const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

// Servir les fichiers statiques depuis le dossier public
app.use(express.static('public'));

// Gestionnaire de route pour la page d'accueil
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

// Gestion des connexions Socket.IO
io.on('connection', (socket) => {
    // Annoncer la connexion d'un nouvel utilisateur
    socket.broadcast.emit('user event', 'Un nouvel utilisateur s\'est connecté');
    console.log('Un utilisateur s\'est connecté');

    // Gestion des messages
    socket.on('chat message', (msg) => {
        // Envoyer le message à tous les autres utilisateurs
        socket.broadcast.emit('chat message', msg);
    });

    // Gestion de la déconnexion
    socket.on('disconnect', () => {
        socket.broadcast.emit('user event', 'Un utilisateur s\'est déconnecté');
        console.log('Un utilisateur s\'est déconnecté');
    });
});

// Démarrage du serveur
server.listen(3000, () => {
    console.log('Serveur en écoute sur le port *:3000');
});