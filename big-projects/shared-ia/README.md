# Shared IA

A full-stack collaborative AI chat application where multiple users (max 4) can converse with an AI through a collective message validation system. This project demonstrates real-time communication, collaborative workflows, and AI integration in modern web applications.

## Overview

This application allows a group of users (maximum 4) to collaborate in a conversation with an AI. Each message sent by a user must be validated by all other room members before being sent to the AI. The system also includes a conflict resolution mechanism when multiple messages are proposed simultaneously.

## Projects Included

### 1. [Backend](backend)
Node.js/Express backend with Socket.io for real-time communication and OpenAI integration.

- Real-time chat with Socket.io
- Collective message validation system
- Conflict resolution with voting mechanism
- OpenAI integration for AI responses
- User authentication with JWT
- Room management and invitations
- Message editing, deletion, and retraction
- Typing indicators and user presence

**Technologies**: Node.js, Express.js, Socket.io, PostgreSQL, OpenAI API, JWT, bcrypt, Swagger

### 2. [Frontend](frontend)
React 19 frontend with TypeScript and Vite for the collaborative AI chat interface.

- Modern React 19 with TypeScript
- Real-time UI updates with Socket.io client
- State management with Zustand
- Form handling with React Hook Form and Zod
- Material Design with shadcn/ui components
- Responsive design with TailwindCSS

**Technologies**: React 19, TypeScript, Vite, TailwindCSS, React Router v6, Zustand, Socket.io-client, Axios, shadcn/ui

## Technologies Used

### Languages & Frameworks
- **Node.js 18+**: JavaScript runtime environment
- **Express.js**: Web application framework
- **React 19**: Modern UI library
- **TypeScript**: Static type checking

### Real-time Communication
- **Socket.io**: Real-time bidirectional communication
- **WebSockets**: Persistent connections for live updates

### Backend Services
- **PostgreSQL**: Relational database management (via Supabase)
- **OpenAI API**: AI response generation with streaming
- **JWT**: Token-based authentication
- **bcrypt**: Password hashing

### Frontend Libraries
- **Vite**: Build tool and development server
- **TailwindCSS**: Utility-first CSS framework
- **React Router v6**: Client-side routing
- **Zustand**: Lightweight state management
- **React Hook Form + Zod**: Form handling and validation
- **Axios**: HTTP client
- **shadcn/ui**: UI component library

### Development Tools
- **Swagger**: API documentation
- **Git / GitHub**: Version control
- **npm**: Package manager

## Project Structure

```
shared-ia/
├── backend/                 → Backend Node.js/Express
│   ├── src/
│   │   ├── config/         → Configuration (database, socket, swagger, ai-handler)
│   │   ├── middleware/     → Authentication middleware
│   │   ├── routes/         → API routes (auth, rooms, invitations)
│   │   ├── services/       → Services (OpenAI)
│   │   ├── schema.sql      → Database schema
│   │   └── server.js       → Server entry point
│   ├── scripts/            → Utility scripts (generate-secret, test-db)
│   ├── env.example         → Configuration example
│   ├── README.md           → Backend documentation
│   └── package.json
├── frontend/                → Frontend React/TypeScript
│   ├── src/
│   │   ├── components/     → React components
│   │   │   ├── ui/         → UI components (shadcn/ui)
│   │   │   └── ...         → Business components
│   │   ├── pages/          → Application pages
│   │   ├── lib/            → Utilities (API, Socket, utils)
│   │   ├── store/          → State management (Zustand)
│   │   ├── hooks/          → Custom React hooks
│   │   ├── assets/         → Static resources
│   │   ├── App.tsx         → Main component
│   │   └── main.tsx        → Entry point
│   ├── public/             → Public files
│   ├── env.example         → Configuration example
│   ├── README.md           → Frontend documentation
│   ├── vite.config.ts      → Vite configuration
│   ├── tailwind.config.js  → TailwindCSS configuration
│   └── package.json
└── README.md                → Main documentation
```

## Getting Started

Each project has its own README with detailed instructions. To explore a project:

1. Navigate to the project directory (backend or frontend)
2. Read the project's README.md for specific setup instructions
3. Follow the installation and configuration steps
4. Run the project according to its documentation

### Prerequisites

- Node.js 18+
- PostgreSQL (via Supabase recommended)
- OpenAI API key

### Quick Start

#### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file:
```env
DATABASE_URL=postgresql://user:password@host:port/database
JWT_SECRET=your-secret-key-change-in-production
OPENAI_API_KEY=sk-your-openai-api-key
PORT=3001
NODE_ENV=development
CLIENT_URL=http://localhost:5173
USE_HTTPS=false
```

4. Generate a JWT secret key:
```bash
npm run generate-secret
```

5. Start the server:
```bash
npm run dev
```

The server starts on `http://localhost:3001`

#### Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file:
```env
VITE_API_URL=http://localhost:3001
VITE_SOCKET_URL=http://localhost:3001
```

4. Start the development server:
```bash
npm run dev
```

The application starts on `http://localhost:5173`

## Key Features

### Collective Message Validation
- Each message sent by a user is first pending validation
- All room members (except the author) must validate the message
- Once validated by all, the message is sent to the AI
- Messages can be rejected, modified, or retracted before validation

### Conflict Resolution
- When multiple messages are proposed simultaneously, a conflict is detected
- Members vote to choose which message to send to the AI
- The message with the most votes is selected
- Other messages can be kept for later

### Real-time Communication
- All interactions use Socket.io for instant communication
- Updates are propagated in real-time to all members
- Automatic reconnection with state synchronization

## API Documentation

Once the backend is started, Swagger documentation is available at:
- http://localhost:3001/docs

## Database

The SQL schema is automatically created when the server starts. Main tables include:
- `users`: Users
- `rooms`: Conversation rooms
- `room_members`: Room members
- `messages`: Messages
- `message_validations`: Message validations
- `message_conflicts`: Message conflicts
- `conflict_messages`: Message/conflict relationships
- `votes`: Votes for conflict resolution
- `invitations`: Invitations

## Security

- JWT authentication with 7-day expiration
- Rate limiting: 100 requests/minute per IP
- Password hashing with bcrypt
- Data validation with Zod
- CORS protection configured

## Important Notes

- The backend requires a JWT token in `auth.token` when connecting to Socket.io
- Swagger documentation is available at `/docs` once the server is started
- The system supports a maximum of 4 users per room
- Messages in error can be retried manually or automatically

Feel free to explore the repositories for more detailed information on each project!
