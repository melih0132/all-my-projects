# Kotlin Apps

Welcome to my Kotlin projects repository! This directory contains a collection of Android applications developed using Kotlin and Jetpack Compose. Each project demonstrates different concepts and features of modern Android development with Material Design 3.

## Overview

This repository includes six Android applications, each focusing on different aspects of Jetpack Compose development:
- State management
- User interaction
- UI layout and design
- Material Design 3 components
- Lists and data display

## Included Projects

### 1. **DiceRoller**

A simple and interactive dice rolling application that demonstrates basic state management in Jetpack Compose.

- **Features**: Roll a 6-sided die with visual feedback, random number generation
- **Key Concepts**: State management with `remember` and `mutableStateOf`, Image composables, Button interactions
- **Technologies**: Kotlin, Jetpack Compose, Material Design 3
- **Min SDK**: 24 | **Target SDK**: 36 | **Compile SDK**: 36

### 2. **HappyBirthday**

A personalized birthday card application showcasing image composition and text layout in Compose.

- **Features**: Customizable birthday message, background image with overlay, text styling
- **Key Concepts**: Image composables, Text styling, Layout composition (Box, Column), Content scaling
- **Technologies**: Kotlin, Jetpack Compose, Material Design 3
- **Min SDK**: 24 | **Target SDK**: 36 | **Compile SDK**: 36

### 3. **Lemonade**

An interactive lemonade-making simulation app that demonstrates multi-step state management and user interaction flows.

- **Features**: Step-by-step lemonade making process (select, squeeze, drink, restart), random squeeze count, visual feedback
- **Key Concepts**: Multi-state management, Clickable composables, State transitions, Scaffold and TopAppBar
- **Technologies**: Kotlin, Jetpack Compose, Material Design 3
- **Min SDK**: 24 | **Target SDK**: 35 | **Compile SDK**: 35

### 4. **TipTime**

A tip calculator application that teaches user input handling and real-time calculations in Compose.

- **Features**: Bill amount input, customizable tip percentage, round-up option, real-time tip calculation, currency formatting
- **Key Concepts**: TextField input handling, State management, Calculations, Number formatting, Switch component
- **Technologies**: Kotlin, Jetpack Compose, Material Design 3
- **Min SDK**: 24 | **Target SDK**: 35 | **Compile SDK**: 35

### 5. **Affirmations**

A scrollable list application that demonstrates data classes, lists, and lazy loading in Jetpack Compose.

- **Features**: Scrollable list of 10 affirmation cards, each with an image and motivational text, smooth scrolling with LazyColumn
- **Key Concepts**: LazyColumn composables, Card components, Data classes, Lists in Compose, Image composables, Resource management
- **Technologies**: Kotlin, Jetpack Compose, Material Design 3
- **Min SDK**: 24 | **Target SDK**: 33 | **Compile SDK**: 33

### 6. **Woof**

A beautiful dog gallery application showcasing Material Design 3 components with expandable cards and animations.

- **Features**: Scrollable list of dog cards with photos, names, ages, and favorite activities, expandable cards with smooth animations, Material 3 TopAppBar
- **Key Concepts**: LazyColumn composables, Card components with expand/collapse functionality, Scaffold and CenterAlignedTopAppBar, Animations (animateContentSize), Data classes, Row and Column layouts, Material Icons
- **Technologies**: Kotlin, Jetpack Compose, Material Design 3
- **Min SDK**: 24 | **Target SDK**: 35 | **Compile SDK**: 35

## Technologies Used

### Core Technologies
- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Design System**: Material Design 3
- **Build System**: Gradle (Kotlin DSL)

### Libraries & Dependencies
- AndroidX Core KTX
- AndroidX Lifecycle Runtime KTX
- AndroidX Activity Compose
- Jetpack Compose BOM
- Compose UI, UI Graphics, UI Tooling
- Material 3 Components

### Development Tools
- Android Studio
- Gradle
- Git

## Getting Started

### Prerequisites
- Android Studio (latest version recommended)
- JDK 11 or higher
- Android SDK (API level 24+)
- Basic knowledge of Kotlin syntax
- Understanding of Android development fundamentals

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd kotlin-apps
```

2. Open any project in Android Studio:
   - File → Open → Select the project folder (e.g., `DiceRoller`, `HappyBirthday`, etc.)

3. Sync Gradle dependencies

4. Run the app on an emulator or physical device

## Project Structure

Each project follows a standard Android project structure:
```
ProjectName/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/projectname/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   └── ui/theme/
│   │   │   ├── res/
│   │   │   └── AndroidManifest.xml
│   │   ├── test/
│   │   └── androidTest/
│   └── build.gradle.kts
├── gradle/
├── build.gradle.kts
└── settings.gradle.kts
```

## Learning Path

These projects are designed to progressively teach Jetpack Compose concepts:

1. **DiceRoller** - Start here for basic state and UI
2. **HappyBirthday** - Learn layout and image composition
3. **Lemonade** - Understand multi-step state management
4. **TipTime** - Master user input and calculations
5. **Affirmations** - Learn lists, data classes, and lazy loading
6. **Woof** - Explore Material Design 3 components, expandable cards, and animations

## License

Each project may have its own license. Please refer to individual project README files for license information.

## Contributing

Feel free to explore, learn, and experiment with these projects. Each project is self-contained and can be run independently.
