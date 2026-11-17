# Affirmations

Android scrollable list of affirmation cards in Jetpack Compose.

## Overview

Affirmations shows ten motivational cards in a `LazyColumn`. Each item pairs a drawable with a string via a data model and a local data source.

The sample introduces lists, cards, and resource-backed content in Compose.

## Features

- LazyColumn of affirmation cards
- Image plus text per card
- Affirmation data class and Datasource
- Material 3 Card layout
- String and drawable resources

## Stack

- Kotlin
- Jetpack Compose
- Material Design 3
- Gradle (Kotlin DSL)

## Layout

```
Affirmations/
├── app/
│   ├── src/main/
│   └── build.gradle.kts
├── build.gradle.kts
├── settings.gradle.kts
├── LICENSE
└── README.md
```

## Run

```bash
./gradlew assembleDebug
# or open in Android Studio and Run
```

On Windows: `gradlew.bat assembleDebug`
