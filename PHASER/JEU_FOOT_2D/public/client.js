const config = {
    type: Phaser.AUTO,
    width: 1000,
    height: 600,
    physics: {
        default: 'arcade',
        arcade: {
            debug: false,
            gravity: { y: 0 }
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const game = new Phaser.Game(config);

let players = {};
let ball;
let teams = { red: 0, blue: 0 };
let cursors;
let scoreText, timerText;
let playerCountText;
let timer = 300;
let timerEvent;
let selectedTeam;

const socket = io();

socket.on('joinGame', (data) => {
    selectedTeam = data.team;
});

function preload() {
    this.load.image('player_red', 'assets/player_red.png');
    this.load.image('player_blue', 'assets/player_blue.png');
    this.load.image('ball', 'assets/ball.png');

    this.load.image('background', 'assets/terrain.png'); const config = {
        type: Phaser.AUTO,
        width: 1000,
        height: 600,
        physics: {
            default: 'arcade',
            arcade: {
                debug: false,
                gravity: { y: 0 }
            }
        },
        scene: {
            preload: preload,
            create: create,
            update: update
        }
    };

    const game = new Phaser.Game(config);

    let players = {};
    let ball;
    let teams = { red: 0, blue: 0 };
    let cursors;
    let scoreText, timerText;
    let playerCountText;
    let timer = 300;
    let timerEvent;
    let selectedTeam;

    const socket = io();

    socket.on('joinGame', (data) => {
        selectedTeam = data.team;
    });

    function preload() {
        this.load.image('player_red', 'assets/player_red.png');
        this.load.image('player_blue', 'assets/player_blue.png');
        this.load.image('ball', 'assets/ball.png');

        this.load.image('background', 'assets/terrain.png');
    }

    function create() {
        socket.emit('joinGame', { team: selectedTeam });

        this.add.image(0, 0, 'background').setOrigin(0, 0);

        ball = this.physics.add.image(500, 300, 'ball');
        ball.setScale(0.05);
        ball.setBounce(1);
        ball.setCollideWorldBounds(true);

        socket.on('currentPlayers', (serverPlayers) => {
            players = serverPlayers;
            updatePlayerCount();
            Object.keys(players).forEach((id) => {
                createPlayer(this, id, players[id].x, players[id].y, players[id].team);
            });
        });

        socket.on('newPlayer', (playerInfo) => {
            createPlayer(this, playerInfo.playerId, playerInfo.x, playerInfo.y, playerInfo.team);
            updatePlayerCount();
        });

        socket.on('playerDisconnected', (playerId) => {
            if (players[playerId] && players[playerId].sprite) {
                players[playerId].sprite.destroy();
            }
            delete players[playerId];
            updatePlayerCount();
        });

        socket.on('playerMovement', (playerData) => {
            if (players[playerData.playerId]) {
                players[playerData.playerId].sprite.setPosition(playerData.x, playerData.y);
            }
        });

        socket.on('ballPosition', (ballData) => {
            if (ball) {
                ball.setPosition(ballData.x, ballData.y);
            }
        });

        scoreText = this.add.text(16, 16, 'Score : Red 0 - 0 Blue', { fontSize: '32px', fill: '#FFF' });
        timerText = this.add.text(775, 16, `Time: ${timer}`, { fontSize: '32px', fill: '#FFF' });
        playerCountText = this.add.text(800, 48, 'Joueurs: 0', { fontSize: '24px', fill: '#FFF' });

        cursors = this.input.keyboard.createCursorKeys();

        timerEvent = this.time.addEvent({
            delay: 1000,
            callback: updateTimer,
            callbackScope: this,
            loop: true
        });

        this.physics.add.collider(ball, Object.values(players).map(player => player.sprite), handleBallCollision, null, this);
    }

    function handleBallCollision(ball, playerSprite) {
        const playerPosition = playerSprite.getCenter();
        const ballPosition = ball.getCenter();

        const direction = new Phaser.Math.Vector2(ballPosition.x - playerPosition.x, ballPosition.y - playerPosition.y);
        direction.normalize();

        const force = 300;
        ball.setVelocity(direction.x * force, direction.y * force);
    }

    function update() {
        if (!socket || !players[socket.id]) return;

        const movement = { x: 0, y: 0 };

        if (cursors.left.isDown) {
            movement.x = -5;
        } else if (cursors.right.isDown) {
            movement.x = 5;
        }

        if (cursors.up.isDown) {
            movement.y = -5;
        } else if (cursors.down.isDown) {
            movement.y = 5;
        }

        if (movement.x !== 0 || movement.y !== 0) {
            const newX = players[socket.id].x + movement.x;
            const newY = players[socket.id].y + movement.y;

            const playerSprite = players[socket.id].sprite;
            if (newX > 0 && newX < config.width) {
                players[socket.id].x = newX;
                playerSprite.x = newX;
            }

            if (newY > 0 && newY < config.height) {
                players[socket.id].y = newY;
                playerSprite.y = newY;
            }

            socket.emit('playerMovement', {
                playerId: socket.id,
                x: players[socket.id].x,
                y: players[socket.id].y
            });
        }
    }

    function createPlayer(scene, id, x, y, team) {
        const playerSprite = scene.physics.add.image(x, y, team === 'red' ? 'player_red' : 'player_blue');
        playerSprite.setScale(0.02);
        players[id] = { sprite: playerSprite, x, y, team };

        // Ensure the player sprite is part of the physics world for collision detection
        scene.physics.add.existing(playerSprite);
    }

    function updatePlayerCount() {
        playerCountText.setText(`Joueurs: ${Object.keys(players).length}`);
    }

    function updateTimer() {
        if (timer > 0) {
            timer--;
            timerText.setText(`Time: ${timer}`);
        } else {
            console.log("Le temps est écoulé !");
            timerEvent.remove();
        }
    }
}

function create() {
    socket.emit('joinGame', { team: selectedTeam });

    this.add.image(0, 0, 'background').setOrigin(0, 0);

    ball = this.physics.add.image(500, 300, 'ball');
    ball.setScale(0.05);
    ball.setBounce(1);
    ball.setCollideWorldBounds(true);

    socket.on('currentPlayers', (serverPlayers) => {
        players = serverPlayers;
        updatePlayerCount();
        Object.keys(players).forEach((id) => {
            createPlayer(this, id, players[id].x, players[id].y, players[id].team);
        });
    });

    socket.on('newPlayer', (playerInfo) => {
        createPlayer(this, playerInfo.playerId, playerInfo.x, playerInfo.y, playerInfo.team);
        updatePlayerCount();
    });

    socket.on('playerDisconnected', (playerId) => {
        if (players[playerId] && players[playerId].sprite) {
            players[playerId].sprite.destroy();
        }
        delete players[playerId];
        updatePlayerCount();
    });

    socket.on('playerMovement', (playerData) => {
        if (players[playerData.playerId]) {
            players[playerData.playerId].sprite.setPosition(playerData.x, playerData.y);
        }
    });

    socket.on('ballPosition', (ballData) => {
        if (ball) {
            ball.setPosition(ballData.x, ballData.y);
        }
    });

    scoreText = this.add.text(16, 16, 'Score : Red 0 - 0 Blue', { fontSize: '32px', fill: '#FFF' });
    timerText = this.add.text(775, 16, `Time: ${timer}`, { fontSize: '32px', fill: '#FFF' });
    playerCountText = this.add.text(800, 48, 'Joueurs: 0', { fontSize: '24px', fill: '#FFF' });

    cursors = this.input.keyboard.createCursorKeys();

    timerEvent = this.time.addEvent({
        delay: 1000,
        callback: updateTimer,
        callbackScope: this,
        loop: true
    });

    this.physics.add.collider(ball, Object.values(players).map(player => player.sprite), handleBallCollision, null, this);
}

function handleBallCollision(ball, playerSprite) {
    const playerPosition = playerSprite.getCenter();
    const ballPosition = ball.getCenter();

    const direction = new Phaser.Math.Vector2(ballPosition.x - playerPosition.x, ballPosition.y - playerPosition.y);
    direction.normalize();

    const force = 300;
    ball.setVelocity(direction.x * force, direction.y * force);
}

function update() {
    if (!socket || !players[socket.id]) return;

    const movement = { x: 0, y: 0 };

    if (cursors.left.isDown) {
        movement.x = -5;
    } else if (cursors.right.isDown) {
        movement.x = 5;
    }

    if (cursors.up.isDown) {
        movement.y = -5;
    } else if (cursors.down.isDown) {
        movement.y = 5;
    }

    if (movement.x !== 0 || movement.y !== 0) {
        const newX = players[socket.id].x + movement.x;
        const newY = players[socket.id].y + movement.y;

        const playerSprite = players[socket.id].sprite;
        if (newX > 0 && newX < config.width) {
            players[socket.id].x = newX;
            playerSprite.x = newX;
        }

        if (newY > 0 && newY < config.height) {
            players[socket.id].y = newY;
            playerSprite.y = newY;
        }

        socket.emit('playerMovement', {
            playerId: socket.id,
            x: players[socket.id].x,
            y: players[socket.id].y
        });
    }
}

function createPlayer(scene, id, x, y, team) {
    const playerSprite = scene.physics.add.image(x, y, team === 'red' ? 'player_red' : 'player_blue');
    playerSprite.setScale(0.02);
    players[id] = { sprite: playerSprite, x, y, team };

    // Ensure the player sprite is part of the physics world for collision detection
    scene.physics.add.existing(playerSprite);
}

function updatePlayerCount() {
    playerCountText.setText(`Joueurs: ${Object.keys(players).length}`);
}

function updateTimer() {
    if (timer > 0) {
        timer--;
        timerText.setText(`Time: ${timer}`);
    } else {
        console.log("Le temps est écoulé !");
        timerEvent.remove();
    }
}