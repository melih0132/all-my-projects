# APIfilms

API REST développée en .NET Core pour la gestion des utilisateurs et des films avec système de notation (ratings).

## Description

Cette API permet de gérer une base de données de films et d'utilisateurs avec un système de notation. Elle utilise Entity Framework Core avec PostgreSQL comme base de données et implémente le pattern Repository pour une meilleure séparation des responsabilités.

## Fonctionnalités

- **Gestion des utilisateurs** : CRUD complet (Create, Read, Update, Delete)
- **Recherche d'utilisateurs** : Par ID ou par email
- **Base de données** : PostgreSQL avec Entity Framework Core
- **Architecture** : Pattern Repository pour l'accès aux données
- **Documentation API** : Swagger/OpenAPI intégré
- **Tests unitaires** : Projet de tests inclus

## Technologies

- **.NET Core** : Framework principal
- **Entity Framework Core** : ORM pour l'accès aux données
- **PostgreSQL** : Base de données
- **Swagger/OpenAPI** : Documentation de l'API
- **xUnit** : Framework de tests

## Structure du projet

```
APIfilms/
├── APIfilms/                    # Projet principal
│   ├── Controllers/             # Contrôleurs API
│   │   └── UtilisateursController.cs
│   ├── Models/
│   │   ├── DataManager/         # Gestionnaires de données
│   │   ├── EntityFramework/     # Modèles EF Core
│   │   └── Repository/          # Interfaces Repository
│   ├── Migrations/              # Migrations de base de données
│   └── Program.cs               # Point d'entrée
├── APIfilmsTests/               # Projet de tests
│   └── UtilisateursControllerTests.cs
└── APIfilms.sln                 # Solution Visual Studio
```

## Endpoints API

### Utilisateurs

- `GET /api/Utilisateurs` - Récupère tous les utilisateurs
- `GET /api/Utilisateurs/GetById/{id}` - Récupère un utilisateur par ID
- `GET /api/Utilisateurs/GetByEmail/{email}` - Récupère un utilisateur par email
- `POST /api/Utilisateurs` - Crée un nouvel utilisateur
- `PUT /api/Utilisateurs/{id}` - Met à jour un utilisateur
- `DELETE /api/Utilisateurs/{id}` - Supprime un utilisateur

## Configuration

1. Configurer la chaîne de connexion PostgreSQL dans `appsettings.json`
2. Exécuter les migrations Entity Framework pour créer la base de données
3. Lancer l'application

## Documentation API

Une fois l'application lancée, accédez à `/swagger` pour voir la documentation interactive de l'API.
