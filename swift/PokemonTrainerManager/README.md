# Pokémon Trainer Manager 🎯

**Sujet UIKit — Projet iOS**

---

## Pitch

Vous incarnez le **Professeur Chen** et devez développer une application pour gérer les **dresseurs Pokémon**, suivre leurs **Pokémon**, leurs **badges** et leur progression dans la **Ligue Pokémon**.

---

## Fonctionnalités

- **Liste des dresseurs**  
  Affichage dans un `UITableView` avec le nom et la photo de chaque dresseur.

- **Fiche dresseur détaillée**  
  - Nom et photo du dresseur  
  - Nombre total de Pokémon  
  - Liste des badges obtenus  
  - Tableau des Pokémon possédés avec image et type

- **Navigation et délégation**  
  - Sélection d’un dresseur → ouverture de sa fiche  
  - Sélection d’un Pokémon dans la fiche dresseur → ouverture de la **fiche Pokémon détaillée** via délégation

- **Chargement des données**  
  - Dresseurs et Pokémon chargés depuis un **JSON local** via `Bundle`

- **Prévisualisation HD**  
  - Visualisation des **badges** ou des **cartes dresseur** en haute résolution grâce à `QLPreviewController`

---

## Technologies

- Swift / UIKit  
- UITableView / UICollectionView  
- Navigation Controller  
- Délégation (Delegate Pattern)  
- Bundle & JSON Parsing  
- QLPreviewController  

---

## Organisation du projet

```

PokémonTrainerManager/
│
├─ Controllers/     # UIViewController pour liste et détails
├─ Resources/       # JSON locaux et images
└─ README.md

````

