# TipTime

A tip calculator application built with Jetpack Compose that teaches user input handling and real-time calculations. This app demonstrates form inputs, state management, and Material Design 3 components in modern Android development.

## Overview

TipTime is an Android application that calculates tips based on bill amount and tip percentage. Users can input the bill amount, select or customize the tip percentage, and optionally round up the tip. The app provides real-time calculations and currency formatting.

## Features

- Bill amount input with number formatting
- Customizable tip percentage selection
- Round-up option for tips
- Real-time tip calculation
- Currency formatting
- Material Design 3 components

## Technologies Used

### Languages & Frameworks
- **Kotlin**: Primary programming language
- **Jetpack Compose**: Modern Android UI toolkit
- **Material Design 3**: Design system and components

### Android Development
- **Android Studio**: Primary IDE
- **Gradle (Kotlin DSL)**: Build system
- **Android SDK**: Development toolkit

### Libraries & Dependencies
- **AndroidX Core KTX**: Kotlin extensions
- **AndroidX Lifecycle Runtime KTX**: Lifecycle management
- **AndroidX Activity Compose**: Compose integration
- **Jetpack Compose BOM**: Compose version management
- **Compose UI, UI Graphics, UI Tooling**: Compose components
- **Material 3 Components**: Material Design components

### Development Tools
- **Git / GitHub**: Version control
- **Android Emulator**: Testing environment

## Project Structure

```
TipTime/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/tiptime/
│   │   │   │   ├── MainActivity.kt
│   │   │   │   └── ui/theme/
│   │   │   ├── res/
│   │   │   │   └── values/
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
- Understanding of Jetpack Compose fundamentals

### Installation

1. Install Android Studio, if you don't already have it
2. Download the sample
3. Import the sample into Android Studio
4. Build and run the sample

## Key Concepts

This project demonstrates:

- **User Input Handling**: Text fields and input validation
- **State Management**: Managing form state with `remember` and `mutableStateOf`
- **Real-time Calculations**: Updating calculations as user inputs change
- **Material Design 3**: Using Material 3 components and theming
- **Number Formatting**: Currency and percentage formatting
- **Layout Composition**: Arranging UI elements with Column and Row

## Learning Objectives

After completing this project, you should understand:

- How to handle user input in Compose
- How to perform real-time calculations
- How to format numbers and currency
- How to use Material Design 3 components
- How to manage form state
- How to create interactive UI components

Feel free to explore the repositories for more detailed information on each project!
