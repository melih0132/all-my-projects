# Woof

A beautiful dog gallery application showcasing Material Design 3 components with expandable cards and animations.

## Overview

The Woof app displays a scrollable list of dog cards, each containing a photo, name, age, and favorite activity. Users can expand each card to see more information with smooth animations. This app demonstrates advanced Material Design 3 components and animation techniques in Jetpack Compose.

## Features

- **Scrollable Dog Gallery**: Browse through a collection of 9 different dogs
- **Expandable Cards**: Tap any card to expand and see detailed information about each dog
- **Smooth Animations**: Beautiful expand/collapse animations using `animateContentSize`
- **Material Design 3**: Modern UI with Material 3 components including CenterAlignedTopAppBar
- **Dog Information**: Each card displays:
  - Dog photo
  - Name
  - Age
  - Favorite activity/hobby

## Key Concepts

This project demonstrates:

- **LazyColumn**: Efficiently displaying scrollable lists
- **Card Components**: Material 3 cards with expandable functionality
- **Scaffold**: App structure with TopAppBar
- **CenterAlignedTopAppBar**: Material 3 app bar component
- **Animations**: Using `animateContentSize` for smooth expand/collapse transitions
- **State Management**: Managing expanded state with `remember` and `mutableStateOf`
- **Data Classes**: Organizing dog data with Kotlin data classes
- **Row and Column Layouts**: Arranging UI elements horizontally and vertically
- **Material Icons**: Using Material Icons (ExpandMore, ExpandLess)
- **Modifiers**: Applying padding, sizing, and styling with modifiers

## Technologies

- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Design System**: Material Design 3
- **Build System**: Gradle (Kotlin DSL)

## Project Configuration

- **Min SDK**: 24
- **Target SDK**: 35
- **Compile SDK**: 35

## Getting Started

### Prerequisites

- Android Studio (latest version recommended)
- JDK 11 or higher
- Android SDK (API level 24+)
- Basic knowledge of Kotlin syntax
- Understanding of Jetpack Compose fundamentals

### Installation

1. Open the project in Android Studio:
   - File → Open → Select the `Woof` folder

2. Sync Gradle dependencies

3. Run the app on an emulator or physical device

## Project Structure

```
Woof/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/woof/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   ├── data/
│   │   │   │   │   └── Dog.kt
│   │   │   │   └── ui/theme/
│   │   │   ├── res/
│   │   │   │   ├── drawable/ (dog images)
│   │   │   │   └── values/
│   │   │   └── AndroidManifest.xml
│   │   ├── test/
│   │   └── androidTest/
│   └── build.gradle.kts
├── gradle/
├── build.gradle.kts
└── settings.gradle.kts
```

## Learning Objectives

After completing this project, you should understand:

- How to create expandable/collapsible UI components
- How to implement smooth animations in Compose
- How to use Material 3 components effectively
- How to structure data with data classes
- How to create beautiful, modern Android UIs with Material Design 3

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.
