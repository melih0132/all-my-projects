# Pokemon Trainer Manager

UIKit iOS app to browse Pokemon trainers, badges, and party members.

## Overview

Pokemon Trainer Manager loads trainers and Pokemon from local JSON in the app bundle. A table lists trainers; detail screens show badges and owned Pokemon. Selecting a Pokemon opens a detail controller via delegation.

Quick Look can preview high-resolution badge or trainer assets.

## Features

- Trainer list in UITableView
- Trainer detail with badges and Pokemon
- Pokemon detail via delegate navigation
- Local JSON loading from Bundle
- QLPreviewController for HD assets
- Storyboard-based UIKit flow

## Stack

- Swift
- UIKit
- UITableView / navigation
- Bundle JSON parsing
- QLPreviewController
- Xcode

## Layout

```
PokemonTrainerManager/
├── Pokémon Trainer Manager/
│   ├── Pokémon Trainer Manager/
│   │   ├── Controller/
│   │   ├── Ressources/
│   │   ├── AppDelegate.swift
│   │   └── SceneDelegate.swift
│   └── Pokémon Trainer Manager.xcodeproj/
└── README.md
```

## Run

```bash
open "Pokémon Trainer Manager/Pokémon Trainer Manager.xcodeproj"
# select a simulator or device, then Run in Xcode
```
