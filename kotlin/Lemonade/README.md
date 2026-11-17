# Lemonade

Android lemonade-making flow with multi-step Compose state.

## Overview

Lemonade walks through four taps: pick a lemon, squeeze it, drink, then restart. Squeeze count is random (2-4). Images and copy change per step under a Material 3 scaffold and top app bar.

The sample focuses on conditional UI and multi-variable state in Compose.

## Features

- Four-step lemonade sequence
- Random squeeze requirement
- Per-step images and labels
- Scaffold and CenterAlignedTopAppBar
- Clickable image buttons

## Stack

- Kotlin
- Jetpack Compose
- Material Design 3
- Gradle (Kotlin DSL)

## Layout

```
Lemonade/
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
