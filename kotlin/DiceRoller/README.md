# DiceRoller

Android app that rolls a six-sided die with Jetpack Compose.

## Overview

DiceRoller shows a die face and a Roll button. Each tap picks a random value from 1 to 6 and updates the matching drawable. State is held with `remember` and `mutableStateOf`.

The project is a Compose starter for button interaction and simple reactive UI.

## Features

- Tap to roll a 1-6 result
- Die face images for each value
- Centered Material 3 layout
- Compose state updates on click
- String and drawable resources

## Stack

- Kotlin
- Jetpack Compose
- Material Design 3
- Gradle (Kotlin DSL)

## Layout

```
DiceRoller/
├── app/
│   ├── src/main/
│   └── build.gradle.kts
├── build.gradle.kts
├── settings.gradle.kts
└── README.md
```

## Run

```bash
./gradlew assembleDebug
# or open in Android Studio and Run
```

On Windows: `gradlew.bat assembleDebug`
