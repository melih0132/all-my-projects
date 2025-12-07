# shared-ia

Application full-stack de chat IA collaborative où plusieurs utilisateurs (max 4) conversent avec une IA via un système de validation collective des messages.

## Vue d'ensemble

Cette application permet à un groupe d'utilisateurs (maximum 4) de collaborer dans une conversation avec une IA. Chaque message envoyé par un utilisateur doit être validé par les autres membres de la room avant d'être envoyé à l'IA. Le système inclut également un mécanisme de résolution de conflits lorsque plusieurs messages sont proposés simultanément.

## Fonctionnalités principales

- **Chat collaboratif en temps réel** : Communication instantanée via Socket.io
- **Système de validation collective** : Chaque message nécessite l'approbation de tous les membres
- **Résolution de conflits** : Mécanisme de vote lorsque plusieurs messages sont proposés en même temps
- **Intégration OpenAI** : Réponses générées par l'IA avec streaming en temps réel
- **Gestion des rooms** : Création, suppression et gestion de salles de conversation
- **Système d'invitations** : Invitation de membres à rejoindre une room
- **Édition et suppression de messages** : Modification ou retrait de messages en attente
- **Indicateurs de présence** : Affichage du statut en ligne/hors ligne des utilisateurs
- **Indicateurs de frappe** : Visualisation en temps réel de qui est en train d'écrire

## Architecture

L'application suit une architecture full-stack moderne :

- **Backend** : Node.js avec Express.js et Socket.io pour la communication en temps réel
- **Frontend** : React 19 avec TypeScript et Vite
- **Base de données** : PostgreSQL (via Supabase)
- **Authentification** : JWT (JSON Web Tokens)
- **IA** : OpenAI API pour la génération de réponses

## Structure du projet

```
shared-ia/
├── backend/                 → Backend Node.js/Express
│   ├── src/
│   │   ├── config/         → Configuration (database, socket, swagger, ai-handler)
│   │   ├── middleware/     → Middleware d'authentification
│   │   ├── routes/         → Routes API (auth, rooms, invitations)
│   │   ├── services/       → Services (OpenAI)
│   │   ├── schema.sql      → Schéma de base de données
│   │   └── server.js       → Point d'entrée du serveur
│   ├── scripts/            → Scripts utilitaires (generate-secret, test-db)
│   ├── env.example         → Exemple de configuration
│   ├── README.md           → Documentation backend
│   └── package.json
├── frontend/                → Frontend React/TypeScript
│   ├── src/
│   │   ├── components/     → Composants React
│   │   │   ├── ui/         → Composants UI (shadcn/ui)
│   │   │   └── ...         → Composants métier
│   │   ├── pages/          → Pages de l'application
│   │   ├── lib/            → Utilitaires (API, Socket, utils)
│   │   ├── store/          → State management (Zustand)
│   │   ├── hooks/          → Hooks React personnalisés
│   │   ├── assets/         → Ressources statiques
│   │   ├── App.tsx         → Composant principal
│   │   └── main.tsx        → Point d'entrée
│   ├── public/             → Fichiers publics
│   ├── env.example         → Exemple de configuration
│   ├── README.md           → Documentation frontend
│   ├── vite.config.ts      → Configuration Vite
│   ├── tailwind.config.js  → Configuration TailwindCSS
│   └── package.json
└── README.md                → Documentation principale
```

## Technologies utilisées

### Backend
- **Node.js 18+** : Runtime JavaScript
- **Express.js** : Framework web
- **Socket.io** : Communication en temps réel
- **PostgreSQL** : Base de données relationnelle
- **OpenAI API** : Intégration IA
- **JWT** : Authentification
- **bcrypt** : Hashage de mots de passe
- **Swagger** : Documentation API

### Frontend
- **React 19** : Bibliothèque UI
- **TypeScript** : Typage statique
- **Vite** : Build tool et dev server
- **TailwindCSS** : Framework CSS
- **React Router v6** : Routing
- **Zustand** : State management
- **React Hook Form + Zod** : Formulaires et validation
- **Socket.io-client** : Client WebSocket
- **Axios** : Requêtes HTTP
- **shadcn/ui** : Composants UI

## Installation

### Prérequis
- Node.js 18+
- PostgreSQL (via Supabase recommandé)
- Clé API OpenAI

### Backend

1. Naviguer vers le dossier backend :
```bash
cd backend
```

2. Installer les dépendances :
```bash
npm install
```

3. Créer un fichier `.env` :
```env
DATABASE_URL=postgresql://user:password@host:port/database
JWT_SECRET=your-secret-key-change-in-production
OPENAI_API_KEY=sk-your-openai-api-key
PORT=3001
NODE_ENV=development
CLIENT_URL=http://localhost:5173
USE_HTTPS=false
```

4. Générer une clé JWT secrète :
```bash
npm run generate-secret
```

5. Démarrer le serveur :
```bash
npm run dev
```

Le serveur démarre sur `http://localhost:3001`

### Frontend

1. Naviguer vers le dossier frontend :
```bash
cd frontend
```

2. Installer les dépendances :
```bash
npm install
```

3. Créer un fichier `.env` :
```env
VITE_API_URL=http://localhost:3001
VITE_SOCKET_URL=http://localhost:3001
```

4. Démarrer le serveur de développement :
```bash
npm run dev
```

L'application démarre sur `http://localhost:5173`

## Documentation API

Une fois le backend démarré, la documentation Swagger est disponible sur :
- http://localhost:3001/docs

## Fonctionnalités détaillées

### Système de validation
- Chaque message envoyé par un utilisateur est d'abord en attente de validation
- Tous les membres de la room (sauf l'auteur) doivent valider le message
- Une fois validé par tous, le message est envoyé à l'IA
- Les messages peuvent être rejetés, modifiés ou retirés avant validation

### Résolution de conflits
- Lorsque plusieurs messages sont proposés simultanément, un conflit est détecté
- Les membres votent pour choisir quel message envoyer à l'IA
- Le message avec le plus de votes est sélectionné
- Les autres messages peuvent être conservés pour plus tard

### Communication en temps réel
- Toutes les interactions utilisent Socket.io pour la communication instantanée
- Les mises à jour sont propagées en temps réel à tous les membres
- Reconnexion automatique avec synchronisation de l'état

## Base de données

Le schéma SQL est automatiquement créé au démarrage du serveur. Les tables principales sont :
- `users` : Utilisateurs
- `rooms` : Salles de conversation
- `room_members` : Membres des rooms
- `messages` : Messages
- `message_validations` : Validations de messages
- `message_conflicts` : Conflits de messages
- `conflict_messages` : Liaison messages/conflits
- `votes` : Votes pour résoudre les conflits
- `invitations` : Invitations

## Scripts disponibles

### Backend
- `npm run dev` : Démarrer en mode développement (avec watch)
- `npm start` : Démarrer en mode production
- `npm run test-db` : Tester la connexion à la base de données
- `npm run generate-secret` : Générer une clé JWT secrète

### Frontend
- `npm run dev` : Démarrer le serveur de développement
- `npm run build` : Build de production
- `npm run preview` : Prévisualiser le build de production
- `npm run lint` : Linter le code

## Sécurité

- Authentification JWT avec expiration après 7 jours
- Rate limiting : 100 requêtes/minute par IP
- Hashage des mots de passe avec bcrypt
- Validation des données avec Zod
- Protection CORS configurée

## Notes importantes

- Le backend nécessite un token JWT dans `auth.token` lors de la connexion Socket.io
- La documentation Swagger est disponible sur `/docs` une fois le serveur démarré
- Le système supporte un maximum de 4 utilisateurs par room
- Les messages en erreur peuvent être retentés manuellement ou automatiquement

## Contribution

Ce projet est en développement actif. N'hésitez pas à explorer le code et à proposer des améliorations !
