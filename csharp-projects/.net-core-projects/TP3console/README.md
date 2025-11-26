# TP3console

Application console .NET pour manipuler une base de données de films avec Entity Framework Core.

## Description

Application console développée dans le cadre d'un TP (Travaux Pratiques) pour apprendre à utiliser Entity Framework Core avec PostgreSQL. L'application démontre les opérations CRUD de base et les requêtes LINQ sur une base de données de films.

## Fonctionnalités

- **Lecture de données** : Affichage des emails des utilisateurs
- **Recherche de films** : Recherche de films par critères (ex: commençant par "Le")
- **Ajout d'utilisateurs** : Création de nouveaux utilisateurs
- **Modification de films** : Mise à jour des informations de films
- **Suppression de films** : Suppression de films avec gestion des relations (avis)

## Technologies

- **.NET Core** : Framework principal
- **Entity Framework Core** : ORM pour l'accès aux données
- **PostgreSQL** : Base de données
- **LINQ** : Requêtes sur les données
- **C#** : Langage de programmation

## Structure du projet

```
TP3console/
├── TP3console/                  # Projet principal
│   ├── Models/                  # Modèles Entity Framework
│   │   └── EntityFramework/     # DbContext et entités
│   └── Program.cs               # Point d'entrée avec exemples
└── TP3console.sln               # Solution Visual Studio
```

## Exemples d'utilisation

### Exercice 2.2 : Afficher les emails des utilisateurs
```csharp
Exo2Q2(); // Affiche tous les emails de la base de données
```

### Exercice 2.7 : Films commençant par "Le"
```csharp
Exo2Q7(); // Recherche les films dont le nom commence par "Le" (insensible à la casse)
```

### Ajout d'un utilisateur
```csharp
AjouterUtilisateur(); // Crée un nouvel utilisateur dans la base de données
```

### Modification d'un film
```csharp
ModifierFilm(); // Met à jour les informations d'un film
```

### Suppression d'un film
```csharp
SupprimerFilm(); // Supprime un film et ses avis associés
```

## Concepts démontrés

- **DbContext** : Contexte de base de données Entity Framework
- **LINQ** : Requêtes sur les collections
- **Include** : Chargement des relations (eager loading)
- **SaveChanges** : Persistance des modifications
- **ILike** : Recherche insensible à la casse avec PostgreSQL

## Configuration

1. Configurez la chaîne de connexion PostgreSQL dans `appsettings.json` ou dans le code
2. Assurez-vous que la base de données est créée et contient des données
3. Exécutez l'application pour voir les exemples en action

## Base de données

L'application utilise une base de données PostgreSQL avec les entités suivantes :
- **Utilisateurs** : Informations des utilisateurs
- **Films** : Catalogue de films
- **Categories** : Catégories de films
- **Avis** : Avis des utilisateurs sur les films
