# Frontend - Application de Chat IA Collaboratif

Frontend React avec Vite pour l'application de chat IA collaboratif.

## Prérequis

- Node.js 18+
- Backend en cours d'exécution sur http://localhost:3001

## Installation

1. Installer les dépendances :
```bash
npm install
```

2. Créer un fichier `.env` à la racine du dossier `frontend` :
```env
VITE_API_URL=http://localhost:3001
VITE_SOCKET_URL=http://localhost:3001
```

3. Lancer le serveur de développement :
```bash
npm run dev
```

L'application démarre sur `http://localhost:5173`

## Structure du projet

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/          # Composants UI de base (shadcn/ui)
│   │   └── ...          # Composants métier
│   ├── pages/           # Pages de l'application
│   ├── lib/             # Utilitaires (API, Socket, etc.)
│   ├── store/           # Stores Zustand
│   └── App.tsx          # Point d'entrée
├── .env                 # Variables d'environnement (à créer)
└── package.json
```

## Technologies utilisées

- **React 19** avec TypeScript
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **React Router v6** - Routing
- **Zustand** - State management
- **React Hook Form + Zod** - Formulaires et validation
- **Socket.io-client** - Temps réel
- **Axios** - Requêtes HTTP

## Pages

- `/login` - Page de connexion
- `/register` - Page d'inscription
- `/dashboard` - Dashboard avec liste des rooms
- `/rooms/:roomId` - Page de chat d'une room (à implémenter)
- `/rooms/new` - Création d'une nouvelle room (à implémenter)
