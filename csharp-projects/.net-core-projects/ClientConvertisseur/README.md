# ClientConvertisseur

Application WinUI 3 pour convertir des devises, développée en deux versions : une version simple et une version avec architecture MVVM.

## Description

Cette application cliente permet de convertir des montants entre différentes devises en utilisant un service web. Le projet contient deux versions :
- **V1** : Version simple sans pattern MVVM
- **V2** : Version avec architecture MVVM (Model-View-ViewModel)

## Fonctionnalités

- **Conversion de devises** : Conversion de montants entre différentes devises
- **Interface WinUI 3** : Interface utilisateur moderne avec WinUI 3
- **Architecture MVVM** : Version V2 implémente le pattern MVVM
- **Services** : Communication avec un service web pour les taux de change

## Technologies

- **.NET** : Framework principal
- **WinUI 3** : Framework d'interface utilisateur
- **C#** : Langage de programmation
- **XAML** : Définition de l'interface utilisateur

## Structure du projet

```
ClientConvertisseur/
├── ClientConvertisseurV1/       # Version simple (sans MVVM)
│   ├── Models/                  # Modèles de données
│   ├── Services/                # Services de communication
│   ├── Views/                   # Vues XAML
│   └── MainWindow.xaml          # Fenêtre principale
├── ClientConvertisseurV2/       # Version avec MVVM
│   ├── Models/                  # Modèles de données
│   ├── Services/                # Services de communication
│   ├── ViewModels/              # ViewModels (MVVM)
│   ├── Views/                   # Vues XAML
│   └── MainWindow.xaml          # Fenêtre principale
└── ClientConvertisseur.sln      # Solution Visual Studio
```

## Versions

### V1 - Version Simple
- Architecture simple sans séparation des responsabilités
- Logique métier directement dans le code-behind
- Idéal pour comprendre les bases de WinUI 3

### V2 - Version MVVM
- Architecture MVVM complète
- Séparation claire entre la vue, le ViewModel et le modèle
- Meilleure testabilité et maintenabilité
- Binding de données avec INotifyPropertyChanged

## Configuration

1. Assurez-vous que le service web de conversion (WSConvertisseur) est en cours d'exécution
2. Configurez l'URL du service dans les fichiers de configuration
3. Compilez et lancez l'application

## Utilisation

1. Sélectionnez la devise source
2. Entrez le montant à convertir
3. Sélectionnez la devise cible
4. Cliquez sur convertir pour obtenir le résultat
