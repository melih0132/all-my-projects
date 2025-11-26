# ApiRestAvecEtat

API REST développée en .NET Core pour la gestion de séries télévisées avec support CORS.

## Description

Cette API permet de gérer une collection de séries télévisées. Elle utilise Entity Framework Core avec PostgreSQL et inclut la configuration CORS pour permettre les requêtes cross-origin depuis des applications frontend.

## Fonctionnalités

- **Gestion des séries** : CRUD complet (Create, Read, Update, Delete)
- **Base de données** : PostgreSQL avec Entity Framework Core
- **CORS** : Configuration pour permettre les requêtes cross-origin
- **Documentation API** : Swagger/OpenAPI intégré
- **Gestion d'état** : Suivi des modifications avec Entity Framework

## Technologies

- **.NET Core** : Framework principal
- **Entity Framework Core** : ORM pour l'accès aux données
- **PostgreSQL** : Base de données
- **Swagger/OpenAPI** : Documentation de l'API
- **CORS** : Support des requêtes cross-origin

## Structure du projet

```
ApiRestAvecEtat/
├── ApiRestAvecEtat/             # Projet principal
│   ├── Controllers/             # Contrôleurs API
│   │   └── SeriesController.cs
│   ├── Models/
│   │   └── EntityFramework/     # Modèles EF Core
│   └── Program.cs               # Point d'entrée
└── ApiRestAvecEtat.sln          # Solution Visual Studio
```

## Endpoints API

### Séries

- `GET /api/Series` - Récupère toutes les séries
- `GET /api/Series/{id}` - Récupère une série par ID
- `POST /api/Series` - Crée une nouvelle série
- `PUT /api/Series/{id}` - Met à jour une série
- `DELETE /api/Series/{id}` - Supprime une série

## Configuration

1. Configurer la chaîne de connexion PostgreSQL dans `appsettings.json`
2. Exécuter les migrations Entity Framework pour créer la base de données
3. La configuration CORS "AllowAll" est déjà configurée dans `Program.cs`
4. Lancer l'application

## Documentation API

Une fois l'application lancée, accédez à `/swagger` pour voir la documentation interactive de l'API.
