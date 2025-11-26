# WSConvertisseur

Service web REST développé en .NET Core pour la conversion de devises.

## Description

API REST permettant de gérer des devises et de convertir des montants entre différentes devises. Le service expose des endpoints pour récupérer les devises disponibles et effectuer des conversions.

## Fonctionnalités

- **Gestion des devises** : CRUD complet pour les devises
- **Conversion de devises** : Conversion de montants entre devises
- **Documentation API** : Swagger/OpenAPI avec documentation XML
- **Validation** : Validation des données avec Data Annotations

## Technologies

- **.NET Core** : Framework principal
- **Swagger/OpenAPI** : Documentation de l'API avec support XML
- **Data Annotations** : Validation des modèles
- **REST** : Architecture RESTful

## Structure du projet

```
WSConvertisseur/
├── WSConvertisseur/             # Projet principal
│   ├── Controllers/             # Contrôleurs API
│   │   └── DevisesController.cs
│   ├── Models/                  # Modèles de données
│   │   └── Devise.cs            # Modèle de devise
│   └── Program.cs               # Point d'entrée
├── WSConvertisseurTests/        # Projet de tests
│   └── Controllers/             # Tests des contrôleurs
└── WSConvertisseur.sln          # Solution Visual Studio
```

## Modèle de données

### Devise
- **Id** : Identifiant unique de la devise
- **NomDevise** : Nom de la devise (ex: EUR, USD, GBP)
- **Taux** : Taux de conversion par rapport à une devise de référence

## Endpoints API

### Devises

- `GET /api/Devises` - Récupère toutes les devises disponibles
- `GET /api/Devises/{id}` - Récupère une devise par ID
- `POST /api/Devises` - Crée une nouvelle devise
- `PUT /api/Devises/{id}` - Met à jour une devise
- `DELETE /api/Devises/{id}` - Supprime une devise

## Documentation API

La documentation Swagger est générée automatiquement avec support des commentaires XML. Une fois l'application lancée, accédez à `/swagger` pour voir la documentation interactive.

## Tests

Le projet inclut un projet de tests pour valider le fonctionnement des contrôleurs et des endpoints.

## Configuration

1. Configurez les paramètres de l'application dans `appsettings.json`
2. Lancez l'application
3. Accédez à `/swagger` pour tester l'API

## Utilisation avec ClientConvertisseur

Ce service est conçu pour être utilisé avec l'application **ClientConvertisseur** (WinUI 3) qui fournit une interface utilisateur pour la conversion de devises.
