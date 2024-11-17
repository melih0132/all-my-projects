const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

app.use(express.static('public'));

const quizQuestions = [
    {
        question: "Quelle est la fonction d'un routeur dans un réseau?",
        options: ["Connecter des ordinateurs à Internet", "Acheminer des paquets entre réseaux", "Fournir de l'électricité", "Stocker des fichiers"],
        correct: 1
    },
    {
        question: "Quel est le protocole utilisé pour l'envoi d'emails?",
        options: ["HTTP", "SMTP", "FTP", "IMAP"],
        correct: 1
    },
    {
        question: "Qu'est-ce qu'un VPN?",
        options: ["Un réseau privé virtuel", "Un protocole de transfert de fichiers", "Un type de serveur", "Un type de câble réseau"],
        correct: 0
    },
    {
        question: "Que signifie l'acronyme DHCP?",
        options: ["Dynamic Host Configuration Protocol", "Domain Host Configuration Protocol", "Data Host Control Protocol", "Dynamic Hyperlink Control Protocol"],
        correct: 0
    },
    {
        question: "Quel est le rôle de DNS dans un réseau?",
        options: ["Chiffrer les communications", "Réduire le trafic réseau", "Résoudre les noms de domaine en adresses IP", "Augmenter la bande passante"],
        correct: 2
    },
    {
        question: "Quel protocole est utilisé pour accéder à un site web?",
        options: ["FTP", "SMTP", "HTTP", "IMAP"],
        correct: 2
    },
    {
        question: "Quelle est la principale différence entre un switch et un hub?",
        options: ["Le switch envoie les données à tous les appareils", "Le hub est plus rapide que le switch", "Le switch envoie les données uniquement à l'appareil cible", "Le hub est plus sûr que le switch"],
        correct: 2
    },
    {
        question: "Que signifie l'acronyme LAN?",
        options: ["Large Area Network", "Local Area Network", "Long Area Network", "Low Area Network"],
        correct: 1
    },
    {
        question: "Quelle est la principale fonction d'un pare-feu?",
        options: ["Accélérer la connexion Internet", "Filtrer le trafic réseau entrant et sortant", "Gérer l'attribution des adresses IP", "Améliorer la vitesse du réseau"],
        correct: 1
    },
    {
        question: "Qu'est-ce qu'une adresse IP?",
        options: ["Une adresse email", "Une adresse pour se connecter à Internet", "Une clé de sécurité pour les réseaux sans fil", "Une adresse physique d'un appareil"],
        correct: 1
    }
];

let currentQuestion = 0;
let scores = {};
let playersAnswered = {}; // Suivi des joueurs qui ont répondu correctement
let totalPlayers = 0;     // Nombre total de joueurs

io.on('connection', (socket) => {
    console.log('Nouveau participant au quiz');
    
    socket.on('join', (username) => {
        scores[socket.id] = {
            username: username,
            score: 0
        };
        playersAnswered[socket.id] = false;  // Indiquer que ce joueur n'a pas encore répondu correctement
        totalPlayers++;
        io.emit('updateScores', scores);
        
        if (Object.keys(scores).length === 1) {
            // Premier joueur = hôte
            socket.emit('makeHost');
        }
    });

    socket.on('startQuiz', () => {
        io.emit('question', {
            ...quizQuestions[currentQuestion],
            number: currentQuestion + 1,
            total: quizQuestions.length
        });
    });

    socket.on('answer', (answer) => {
        if (answer === quizQuestions[currentQuestion].correct && !playersAnswered[socket.id]) {
            // Si la réponse est correcte et que le joueur n'a pas encore répondu correctement
            scores[socket.id].score += 1;  // Ajouter un point pour la réponse correcte
            playersAnswered[socket.id] = true; // Marquer ce joueur comme ayant répondu correctement
            socket.emit('result', true);
        } else if (!playersAnswered[socket.id]) {
            // Si la réponse est incorrecte, il n'y a pas de point
            socket.emit('result', false);
        }

        // Vérifier si tous les joueurs ont répondu, ou si quelqu'un a répondu correctement
        if (Object.values(playersAnswered).every(answered => answered) || Object.values(playersAnswered).includes(true)) {
            // Si tous les joueurs ont répondu ou si au moins un joueur a répondu correctement
            // Passer à la question suivante
            currentQuestion++;
            if (currentQuestion < quizQuestions.length) {
                // Si d'autres questions existent, afficher la prochaine question
                io.emit('question', {
                    ...quizQuestions[currentQuestion],
                    number: currentQuestion + 1,
                    total: quizQuestions.length
                });
                // Réinitialiser l'état des réponses pour la prochaine question
                playersAnswered = {};
                for (let playerId in scores) {
                    playersAnswered[playerId] = false;
                }
            } else {
                // Si toutes les questions sont terminées, annoncer la fin du quiz
                let winner = null;
                let maxScore = -1;
                for (let playerId in scores) {
                    if (scores[playerId].score > maxScore) {
                        maxScore = scores[playerId].score;
                        winner = scores[playerId];
                    }
                }
                io.emit('quizFinished', {
                    winner: winner.username,
                    score: winner.score
                });
            }
        }

        io.emit('updateScores', scores);
    });

    socket.on('disconnect', () => {
        delete scores[socket.id];
        delete playersAnswered[socket.id];
        totalPlayers--;
        io.emit('updateScores', scores);
    });
});

server.listen(3000, () => {
    console.log('Serveur de quiz sur le port 3000');
});