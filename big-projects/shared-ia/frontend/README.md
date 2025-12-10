# Frontend - Collaborative AI Chat Application

React frontend with Vite for the collaborative AI chat application. This project demonstrates modern React development with TypeScript, real-time communication, and state management.

## Overview

The frontend is built with React 19 and TypeScript, providing a modern user interface for the collaborative AI chat application. It features real-time updates, form validation, and a responsive design using Material Design components.

## Technologies Used

### Languages & Frameworks
- **React 19**: Modern UI library
- **TypeScript**: Static type checking
- **Vite**: Build tool and development server

### UI & Styling
- **TailwindCSS**: Utility-first CSS framework
- **shadcn/ui**: UI component library
- **Material Design**: Design system

### State Management & Routing
- **Zustand**: Lightweight state management
- **React Router v6**: Client-side routing

### Forms & Validation
- **React Hook Form**: Form handling
- **Zod**: Schema validation

### Real-time Communication
- **Socket.io-client**: WebSocket client for real-time updates

### HTTP Client
- **Axios**: HTTP requests

### Development Tools
- **Git / GitHub**: Version control
- **npm**: Package manager

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/          → Base UI components (shadcn/ui)
│   │   └── ...          → Business components
│   ├── pages/           → Application pages
│   ├── lib/             → Utilities (API, Socket, etc.)
│   ├── store/           → Zustand stores
│   ├── hooks/           → Custom React hooks
│   ├── assets/          → Static resources
│   ├── App.tsx          → Main component
│   └── main.tsx         → Entry point
├── public/              → Public files
├── .env                 → Environment variables (to create)
├── vite.config.ts       → Vite configuration
├── tailwind.config.js   → TailwindCSS configuration
└── package.json
```

## Getting Started

### Prerequisites

- Node.js 18+
- Backend running on http://localhost:3001

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file at the root of the `frontend` folder:
```env
VITE_API_URL=http://localhost:3001
VITE_SOCKET_URL=http://localhost:3001
```

3. Start the development server:
```bash
npm run dev
```

The application starts on `http://localhost:5173`

## Available Scripts

- `npm run dev`: Start the development server
- `npm run build`: Build for production
- `npm run preview`: Preview the production build
- `npm run lint`: Lint the code

## Pages

- `/login` - Login page
- `/register` - Registration page
- `/dashboard` - Dashboard with room list
- `/rooms/:roomId` - Chat page for a room
- `/rooms/new` - Create a new room

## Features

- Real-time chat interface
- Collective message validation UI
- Conflict resolution with voting
- User presence indicators
- Typing indicators
- Message editing and deletion
- Room management
- User authentication

Feel free to explore the codebase for more detailed information!
