# FilmRatingsApp

Application WinUI 3 complète pour la gestion et la notation de films, développée avec une architecture modulaire.

## Description

Application de bureau moderne développée avec WinUI 3 permettant aux utilisateurs de gérer leur collection de films, d'ajouter des notes et des avis. L'application suit les meilleures pratiques de développement avec une architecture en couches et des tests unitaires.

## Fonctionnalités

- **Gestion de films** : Ajout, modification et suppression de films
- **Système de notation** : Attribution de notes aux films
- **Avis utilisateurs** : Ajout et consultation d'avis
- **Interface moderne** : UI/UX avec WinUI 3
- **Architecture modulaire** : Séparation en plusieurs projets (Core, Tests)
- **Navigation** : Navigation entre différentes pages
- **Thèmes** : Support des thèmes clair/sombre du système

## Technologies

- **.NET** : Framework principal
- **WinUI 3** : Framework d'interface utilisateur moderne
- **C#** : Langage de programmation
- **XAML** : Définition de l'interface utilisateur
- **MSTest** : Framework de tests unitaires
- **Template Studio** : Généré avec Windows Template Studio

## Structure du projet

```
FilmRatingsApp/
├── FilmRatingsApp/              # Projet principal (UI)
│   ├── Views/                   # Pages de l'application
│   ├── ViewModels/              # ViewModels (MVVM)
│   ├── Models/                  # Modèles de données
│   ├── Services/                # Services métier
│   ├── Contracts/               # Interfaces
│   ├── Helpers/                 # Classes utilitaires
│   ├── Behaviors/               # Behaviors XAML
│   └── Styles/                  # Styles et thèmes
├── FilmRatingsApp.Core/         # Bibliothèque partagée
│   ├── Contracts/               # Interfaces partagées
│   ├── Services/                # Services partagés
│   └── Helpers/                 # Helpers partagés
├── FilmRatingsApp.Tests.MSTest/ # Projet de tests
│   └── TestClass.cs             # Tests unitaires
└── FilmRatingsApp.sln           # Solution Visual Studio
```

## Architecture

L'application suit une architecture MVVM (Model-View-ViewModel) avec :
- **Models** : Représentation des données
- **Views** : Interface utilisateur (XAML)
- **ViewModels** : Logique de présentation
- **Services** : Logique métier et accès aux données
- **Contracts** : Interfaces pour l'injection de dépendances

## Fonctionnalités principales

### Gestion des films
- Liste des films
- Détails d'un film
- Ajout/Modification de films
- Suppression de films

### Système de notation
- Attribution de notes (étoiles ou note numérique)
- Consultation des notes moyennes
- Historique des notes par utilisateur

### Avis utilisateurs
- Ajout d'avis textuels
- Consultation des avis
- Filtrage et recherche

## Tests

Le projet inclut un projet de tests unitaires utilisant MSTest. Exécutez les tests pour vérifier le bon fonctionnement de l'application.

## Configuration

1. Configurez les paramètres de l'application dans `appsettings.json`
2. Compilez et lancez l'application
3. L'application s'adapte automatiquement au thème système

## Packaging

L'application peut être packagée en MSIX pour la distribution via le Microsoft Store ou le déploiement en entreprise.
