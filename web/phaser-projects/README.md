# Phaser Projects

This folder contains my Phaser.js HTML5 game development projects, covering a wide range of web-based games and interactive applications. These projects demonstrate my proficiency in game development, real-time communication, and the Phaser framework.

## Projects Included

### 1. [App](app)
A collection of web applications built using Phaser.js, exploring various capabilities of the framework.

- **[Draw](app/draw)**: Drawing application with Phaser
  - Real-time collaborative drawing
  - Socket.io integration for multi-user support
  
- **[Notification](app/notification)**: Notification system implementation
  - Real-time notifications
  - Event-based communication
  
- **[Quiz](app/quiz)**: Interactive quiz application
  - Real-time quiz functionality
  - Multi-user quiz participation

**Technologies**: Phaser.js, Node.js, Express.js, Socket.io

### 2. [Chat](chat)
Real-time chat applications powered by Phaser.js and Socket.io.

- **[Private Chat](chat/private-chat)**: Secure private messaging
  - One-on-one private conversations
  - Real-time message delivery
  
- **[Public Chat](chat/public-chat)**: Public chat room functionality
  - Multi-user public chat rooms
  - Real-time message broadcasting

**Technologies**: Phaser.js, Node.js, Socket.io, Express.js

### 3. [Private Chat](private-chat)
A standalone private chat application built with Phaser.js.

- Secure and confidential communication features
- Real-time messaging with Socket.io
- User interface built with Phaser
- Standalone server implementation

**Technologies**: Phaser.js, Node.js, Socket.io, Express.js

### 4. [Public Chat](public-chat)
A public chat application developed using Phaser.js.

- Public chat room functionality
- Real-time message broadcasting
- Multiple user support
- Custom styling with CSS

**Technologies**: Phaser.js, Node.js, Socket.io, Express.js

## Technologies Used

### Languages & Frameworks
- **JavaScript**: Primary programming language
- **Phaser.js**: HTML5 game development framework
- **Node.js**: JavaScript runtime environment

### Frontend Technologies
- **HTML5**: Web markup language
- **CSS**: Styling and layout
- **Canvas API**: 2D graphics rendering

### Backend Technologies
- **Express.js**: Web application framework
- **Socket.io**: Real-time bidirectional communication

### Real-time Communication
- **WebSockets**: Persistent connections for live updates
- **Socket.io**: Real-time event-based communication

### Development Tools
- **npm**: Package manager for Node.js
- **Nodemon**: Development server auto-reload
- **Git / GitHub**: Version control
- **Visual Studio Code**: Primary IDE

## Project Structure

```
phaser-projects/
├── app/                     → Game applications
│   ├── draw/                → Drawing application
│   │   ├── server.js        → Server configuration
│   │   ├── package.json     → Dependencies
│   │   └── public/          → Client-side files
│   │       └── index.html   → Main HTML file
│   ├── notification/        → Notification system
│   │   ├── server.js        → Server configuration
│   │   ├── package.json     → Dependencies
│   │   └── public/          → Client-side files
│   │       └── index.html   → Main HTML file
│   └── quiz/                → Quiz application
│       ├── server.js        → Server configuration
│       ├── package.json     → Dependencies
│       └── public/          → Client-side files
│           └── index.html   → Main HTML file
├── chat/                    → Chat functionality
│   ├── private-chat/        → Private chat feature
│   │   ├── server.js        → Server configuration
│   │   └── package.json     → Dependencies
│   └── public-chat/         → Public chat feature
│       ├── server.js        → Server configuration
│       └── package.json     → Dependencies
├── private-chat/            → Standalone private chat
│   ├── server.js            → Server configuration
│   ├── package.json         → Dependencies
│   └── public/              → Client-side files
│       └── index.html       → Main HTML file
└── public-chat/             → Standalone public chat
    ├── server.js            → Server configuration
    ├── package.json         → Dependencies
    └── public/              → Client-side files
        ├── index.html       → Main HTML file
        └── styleChat.css    → Chat styling
```

## Getting Started

Each project has its own structure and dependencies. To explore a project:

1. Navigate to the project directory
2. Install dependencies using `npm install`
3. Run the server using `node server.js` or `npm start`
4. Open the application in your web browser (typically at `http://localhost:3000` or the port specified in server.js)

**Note**: Make sure Node.js and npm are installed on your system before running these projects.

Feel free to explore the repositories for more detailed information on each project!
