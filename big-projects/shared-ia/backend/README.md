# Backend - Collaborative AI Chat Application

Node.js/Express backend with Socket.io for the collaborative AI chat application. This project demonstrates real-time communication, RESTful API design, and AI integration.

## Overview

The backend provides RESTful APIs and real-time WebSocket communication for the collaborative AI chat application. It handles user authentication, room management, message validation, conflict resolution, and OpenAI integration.

## Technologies Used

### Languages & Frameworks
- **Node.js 18+**: JavaScript runtime environment
- **Express.js**: Web application framework

### Real-time Communication
- **Socket.io**: Real-time bidirectional communication
- **WebSockets**: Persistent connections for live updates

### Database
- **PostgreSQL**: Relational database management (via Supabase)

### AI Integration
- **OpenAI API**: AI response generation with streaming

### Authentication & Security
- **JWT**: Token-based authentication
- **bcrypt**: Password hashing

### Documentation
- **Swagger**: API documentation

### Development Tools
- **Git / GitHub**: Version control
- **npm**: Package manager

## Project Structure

```
backend/
├── src/
│   ├── config/
│   │   ├── database.js      → PostgreSQL configuration
│   │   ├── socket.js         → Socket.io configuration
│   │   └── swagger.js        → Swagger/OpenAPI configuration
│   ├── middleware/
│   │   └── auth.js           → JWT authentication middleware
│   ├── routes/
│   │   ├── auth.js           → Authentication routes
│   │   ├── rooms.js          → Room routes
│   │   └── invitations.js    → Invitation routes
│   ├── services/
│   │   └── openai.js         → OpenAI service
│   ├── schema.sql            → Database schema
│   └── server.js             → Server entry point
├── scripts/
│   ├── generate-secret.js    → Script to generate JWT secret
│   └── test-db.js            → Script to test database connection
├── .env                      → Environment variables (to create)
├── env.example              → Configuration example
└── package.json
```

## Getting Started

### Prerequisites

- Node.js 18+
- PostgreSQL (via Supabase)
- OpenAI API key

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file at the root of the `backend` folder:
```env
DATABASE_URL=postgresql://user:password@host:port/database
JWT_SECRET=your-secret-key-change-in-production
OPENAI_API_KEY=sk-your-openai-api-key
PORT=3001
NODE_ENV=development
CLIENT_URL=http://localhost:5173
USE_HTTPS=false
```

3. Configure Supabase:
   - Create a project on [Supabase](https://supabase.com)
   - Retrieve the PostgreSQL connection URL from project settings
   - The URL looks like: `postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres`
   - Copy this URL into `DATABASE_URL` in the `.env` file

4. Generate a JWT secret key:
```bash
npm run generate-secret
```

5. Start the server:
```bash
npm run dev
```

The server starts on `http://localhost:3001`

## API Documentation

Once the server is started, Swagger documentation is available at:
- http://localhost:3001/docs

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Rooms
- `POST /api/rooms` - Create a room
- `GET /api/rooms` - List user's rooms
- `GET /api/rooms/:roomId` - Get a room
- `DELETE /api/rooms/:roomId` - Delete a room

### Invitations
- `POST /api/invitations` - Create an invitation
- `GET /api/invitations/pending` - List pending invitations
- `POST /api/invitations/:id/accept` - Accept an invitation
- `POST /api/invitations/:id/reject` - Reject an invitation

## Socket.io Events

### Client → Server
- `join-room` - Join a room (roomId)
- `leave-room` - Leave a room (roomId)
- `send-message` - Send a message (roomId, content)
- `validate-message` - Validate a message (messageId, action, addition?, comment?)
- `retract-message` - Retract a message (messageId)
- `edit-message` - Edit a message (messageId, newContent)
- `delete-message` - Delete a message (messageId)
- `vote-message` - Vote for a message in conflict (conflictId, messageId)
- `typing` - Typing indicator (roomId, isTyping)
- `retry-ai-message` - Manual retry of a message in error (messageId, roomId)
- `sync-state` - Synchronize state after reconnection (roomIds[])

### Server → Client
- `authenticated` - Authentication confirmation (userId, username, reconnect)
- `room-joined` - Room join confirmation (room, members, messages)
- `new-pending-message` - New message pending validation
- `validation-update` - Validation update
- `message-rejected` - Message rejected
- `message-retracted` - Message retracted
- `message-edited` - Message edited
- `messages-deleted` - Messages deleted
- `conflict-detected` - Conflict detected
- `vote-update` - Vote update
- `conflict-resolved` - Conflict resolved
- `ai-response-start` - AI response start
- `ai-response-chunk` - AI response chunk
- `ai-response-end` - AI response end
- `ai-response-error` - Error during AI generation
- `ai-response-retry` - Automatic retry notification
- `typing-update` - Typing indicator update
- `user-presence` - User presence (online/offline)
- `state-synced` - State synchronized after reconnection
- `error` - Error occurred

## Database

The SQL schema is automatically created when the server starts. The created tables are:
- `users` - Users
- `rooms` - Conversation rooms
- `room_members` - Room members
- `messages` - Messages
- `message_validations` - Message validations
- `message_conflicts` - Message conflicts
- `conflict_messages` - Message/conflict relationships
- `votes` - Votes for conflict resolution
- `invitations` - Invitations

## Available Scripts

- `npm run dev`: Start the server in development mode (with watch)
- `npm start`: Start the server in production mode
- `npm run test-db`: Test the database connection
- `npm run generate-secret`: Generate a JWT secret key

## Security

- JWT authentication with 7-day token expiration
- Rate limiting: 100 requests/minute per IP
- Password hashing with bcrypt
- Data validation
- CORS protection configured

## Important Notes

- The backend uses JWT for authentication
- Tokens expire after 7 days
- Socket.io requires a JWT token in `auth.token` when connecting
- Swagger documentation is available at `/docs`

Feel free to explore the codebase for more detailed information!
