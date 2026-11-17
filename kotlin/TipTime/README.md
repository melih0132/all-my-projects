# TipTime

Android tip calculator built with Jetpack Compose.

## Overview

TipTime takes a bill amount and tip percent, optionally rounds up, and shows the tip in currency format. Inputs update the result as the user types.

The sample covers text fields, switches or round-up controls, and Material 3 form layout.

## Features

- Bill amount text input
- Tip percentage control
- Optional round-up
- Live tip calculation
- Currency formatting
- Material 3 form UI

## Stack

- Kotlin
- Jetpack Compose
- Material Design 3
- Gradle (Kotlin DSL)

## Layout

```
TipTime/
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
