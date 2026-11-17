# Woof

Android dog gallery with expandable Compose cards.

## Overview

Woof lists dogs with photo, name, age, and hobby. Tapping a card expands details with `animateContentSize`. The screen uses a Scaffold and Material 3 top app bar.

Dog data lives in a Kotlin model under the app package.

## Features

- Scrollable dog list
- Expandable cards
- Content-size expand animation
- Scaffold with CenterAlignedTopAppBar
- Material icons for expand / collapse
- Dog photo, name, age, and hobby

## Stack

- Kotlin
- Jetpack Compose
- Material Design 3
- Gradle (Kotlin DSL)

## Layout

```
Woof/
├── app/
│   ├── src/main/
│   └── build.gradle.kts
├── build.gradle.kts
├── settings.gradle.kts
├── LICENSE
├── ASSETS_LICENSE.txt
└── README.md
```

## Run

```bash
./gradlew assembleDebug
# or open in Android Studio and Run
```

On Windows: `gradlew.bat assembleDebug`
