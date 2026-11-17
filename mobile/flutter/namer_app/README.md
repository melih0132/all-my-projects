# Namer App

Flutter app that generates random English word pairs and saves favorites.

## Overview

Namer App is a Material 3 Flutter client that builds two-word names with the `english_words` package. State is driven by Provider; favorites are persisted with SharedPreferences.

The UI switches between a generator screen and a favorites list. Orientation is unlocked for portrait and landscape.

## Features

- Random word-pair generation
- Like / unlike the current pair
- Favorites list with persistence
- Provider-based app state
- Material 3 theming

## Stack

- Dart / Flutter
- Provider
- english_words
- shared_preferences

## Layout

```
namer_app/
├── android/
├── ios/
├── lib/
│   └── main.dart
├── linux/
├── macos/
├── web/
├── windows/
├── pubspec.yaml
└── README.md
```

## Run

```bash
flutter pub get
flutter run
```
