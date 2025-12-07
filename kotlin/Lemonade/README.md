# Lemonade

An interactive lemonade-making simulation application built with Jetpack Compose. This app demonstrates multi-step state management, user interaction flows, and Material Design 3 components.

## Overview

Lemonade is an Android application that simulates the process of making lemonade through an interactive, step-by-step experience. Users tap through different stages: selecting a lemon, squeezing it, drinking the lemonade, and starting over.

## Features

- **Multi-Step Process**: Four distinct stages of lemonade making
- **Interactive Squeezing**: Random squeeze count (2-4 taps) for realistic interaction
- **Visual Feedback**: Different images and text for each stage
- **State Management**: Complex state handling with multiple state variables
- **Material Design 3**: Uses Scaffold, TopAppBar, and Material 3 theming
- **Edge-to-Edge**: Modern edge-to-edge display support

## App Flow

1. **Select Lemon** - Tap the lemon tree to pick a lemon
2. **Squeeze Lemon** - Tap the lemon multiple times (2-4 random taps required)
3. **Drink Lemonade** - Tap the glass to drink the finished lemonade
4. **Restart** - Tap the empty glass to start the process again

## Technologies

- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Design System**: Material Design 3
- **Minimum SDK**: 24
- **Target SDK**: 35
- **Compile SDK**: 35

## Key Concepts Demonstrated

This project teaches the following Jetpack Compose concepts:

1. **Multi-State Management**
   - Managing multiple state variables (`currentStep`, `squeezeCount`)
   - State transitions between different app stages
   - Conditional rendering based on state

2. **Material Design 3 Components**
   - `Scaffold` for app structure
   - `CenterAlignedTopAppBar` for app bar
   - `Button` with custom styling
   - Material 3 color scheme

3. **User Interaction**
   - Clickable buttons with custom shapes
   - State updates on user actions
   - Random number generation for game mechanics

4. **Layout and Composition**
   - `Box` and `Column` layouts
   - Custom button dimensions and padding
   - Responsive spacing with dimension resources

5. **Resources Management**
   - String resources for text labels
   - Drawable resources for images
   - Dimension resources for consistent sizing

## Project Structure

```
Lemonade/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/lemonade/
│   │   │   │   ├── MainActivity.kt          # Main activity and composables
│   │   │   │   └── ui/theme/                # Theme configuration
│   │   │   ├── res/
│   │   │   │   ├── drawable/                # Lemon images (tree, squeeze, drink, restart)
│   │   │   │   ├── values/
│   │   │   │   │   ├── strings.xml           # String resources
│   │   │   │   │   ├── colors.xml            # Color definitions
│   │   │   │   │   └── dimens.xml            # Dimension resources
│   │   │   └── AndroidManifest.xml
│   │   ├── test/                             # Unit tests
│   │   └── androidTest/                      # Instrumented tests
│   └── build.gradle.kts
├── build.gradle.kts
├── settings.gradle.kts
├── LICENSE
└── CONTRIBUTING.md
```

## Getting Started

### Prerequisites

- Android Studio (latest version)
- JDK 1.8 or higher
- Android SDK with API level 24+
- Basic knowledge of Kotlin
- Understanding of Compose basics (from DiceRoller/HappyBirthday projects)

### Installation

1. Open the project in Android Studio
2. Sync Gradle dependencies
3. Run the app on an emulator or physical device

### Building

```bash
./gradlew assembleDebug
```

### Running Tests

```bash
./gradlew test              # Unit tests
./gradlew connectedAndroidTest  # Instrumented tests
```

## Code Highlights

### State Management

The app manages two key state variables:

```kotlin
@Composable
fun LemonadeApp() {
    var currentStep by remember { mutableStateOf(1) }
    var squeezeCount by remember { mutableStateOf(0) }
    
    // State transitions based on user interaction
    when (currentStep) {
        1 -> { /* Select lemon */ }
        2 -> { /* Squeeze lemon */ }
        3 -> { /* Drink lemonade */ }
        4 -> { /* Restart */ }
    }
}
```

### Random Squeeze Count

Each lemon requires a random number of squeezes:

```kotlin
onImageClick = {
    currentStep = 2
    squeezeCount = (2..4).random()  // Random between 2 and 4
}
```

### Scaffold Structure

Uses Material 3 Scaffold for modern app structure:

```kotlin
Scaffold(
    topBar = {
        CenterAlignedTopAppBar(
            title = { Text("Lemonade", fontWeight = FontWeight.Bold) },
            colors = TopAppBarDefaults.largeTopAppBarColors(
                containerColor = MaterialTheme.colorScheme.primaryContainer
            )
        )
    }
) { innerPadding ->
    // Content
}
```

## Dependencies

- `androidx.activity:activity-compose:1.9.3`
- `androidx.compose.material3:material3`
- `androidx.compose.ui:ui`
- `androidx.compose.ui:ui-graphics`
- `androidx.compose.ui:ui-tooling-preview`
- `androidx.core:core-ktx:1.15.0`
- `androidx.lifecycle:lifecycle-runtime-ktx:2.8.7`
- Compose BOM: `2024.12.01`

## Learning Outcomes

After completing or studying this project, you should understand:

- How to manage complex state with multiple variables
- How to implement multi-step user flows
- How to use Material Design 3 components (Scaffold, TopAppBar)
- How to create interactive buttons with custom styling
- How to use dimension resources for consistent sizing
- How to implement conditional rendering based on state

## App States

| Step | Image | Action | Next Step |
|------|-------|--------|-----------|
| 1 | Lemon Tree | Tap to select | Step 2 (random squeeze count) |
| 2 | Lemon | Tap to squeeze | Step 3 (when squeezeCount = 0) |
| 3 | Glass of Lemonade | Tap to drink | Step 4 |
| 4 | Empty Glass | Tap to restart | Step 1 |

## Future Enhancements

Potential improvements:
- Sound effects for each action
- Animation transitions between states
- Statistics tracking (lemonades made)
- Multiple lemon types
- Achievement system
- Settings for difficulty (squeeze count range)

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Contributing

This is a learning project. Feel free to experiment and modify the code to explore different Compose concepts.