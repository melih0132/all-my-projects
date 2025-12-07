# Affirmations

A scrollable list application that demonstrates data classes, lists, and lazy loading in Jetpack Compose.

## Overview

The Affirmations app displays a scrollable list of 10 motivational affirmation cards. Each card contains an inspirational message paired with a beautiful image, showcasing how to work with lists and data in Jetpack Compose.

## Features

- Scrollable list of 10 affirmation cards
- Each card displays an image and motivational text
- Smooth scrolling with LazyColumn
- Material Design 3 Card components
- Responsive layout with proper image scaling

## Key Concepts

- **LazyColumn composables**: Efficiently display scrollable lists
- **Card components**: Material Design 3 card layout
- **Data classes**: Model data with Kotlin data classes
- **Lists in Compose**: Working with collections and data sources
- **Image composables**: Displaying drawable resources
- **Resource management**: Using string and drawable resources

## Technologies

- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Design System**: Material Design 3
- **Build System**: Gradle (Kotlin DSL)

## SDK Versions

- **Min SDK**: 24
- **Target SDK**: 33
- **Compile SDK**: 33

## Project Structure

```
Affirmations/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/affirmations/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── data/
│   │   │   │   │   └── Datasource.kt
│   │   │   │   ├── model/
│   │   │   │   │   └── Affirmation.kt
│   │   │   │   └── ui/theme/
│   │   │   ├── res/
│   │   │   │   ├── drawable/ (10 affirmation images)
│   │   │   │   └── values/
│   │   │   │       └── strings.xml
│   │   │   └── AndroidManifest.xml
│   │   ├── test/
│   │   └── androidTest/
│   └── build.gradle.kts
├── build.gradle.kts
└── settings.gradle.kts
```

## Getting Started

### Prerequisites

- Android Studio (latest version recommended)
- JDK 11 or higher
- Android SDK (API level 24+)
- Basic knowledge of Kotlin syntax
- Understanding of Android development fundamentals

### Installation

1. Open the project in Android Studio:
   - File → Open → Select the `Affirmations` folder

2. Sync Gradle dependencies

3. Run the app on an emulator or physical device

## Learning Objectives

This project teaches:
- How to create and use data classes in Kotlin
- Working with lists and collections in Compose
- Implementing scrollable lists with LazyColumn
- Using Card components from Material Design 3
- Managing resources (strings and drawables)
- Creating reusable composable functions

## Credits

All photos by Romain Guy. All photos are licensed under CC0 https://creativecommons.org/share-your-work/public-domain/cc0/

## License

This project is part of the Android Basics with Compose course materials.
