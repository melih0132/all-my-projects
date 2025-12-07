# DiceRoller

A simple and interactive dice rolling application built with Jetpack Compose. This app demonstrates basic state management and user interaction in modern Android development.

## Overview

DiceRoller is a beginner-friendly Android application that allows users to roll a virtual 6-sided die. Each roll generates a random number between 1 and 6, displayed with a corresponding visual representation.

## Features

- **Interactive Dice Rolling**: Tap the "Roll" button to generate a random dice result
- **Visual Feedback**: Each dice face (1-6) is displayed with a corresponding image
- **Simple UI**: Clean, centered interface with Material Design 3 components
- **State Management**: Demonstrates reactive state updates in Compose

## Screenshots

The app displays:
- A dice image showing the current result (1-6)
- A "Roll" button to generate a new random result

## Technologies

- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Design System**: Material Design 3
- **Minimum SDK**: 24
- **Target SDK**: 36
- **Compile SDK**: 36

## Key Concepts Demonstrated

This project teaches the following Jetpack Compose concepts:

1. **State Management**
   - Using `remember` and `mutableStateOf` to manage component state
   - Reactive UI updates based on state changes

2. **Composables**
   - `Image` composable for displaying dice faces
   - `Button` composable for user interaction
   - `Column` composable for vertical layout
   - `Text` composable for button labels

3. **Layout**
   - Centering content with `wrapContentSize` and `Alignment.Center`
   - Spacing with `Spacer` composable

4. **Resources**
   - Using `stringResource` for internationalization
   - Using `painterResource` for drawable images

## Project Structure

```
DiceRoller/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/diceroller/
│   │   │   │   ├── MainActivity.kt          # Main activity and composables
│   │   │   │   └── ui/theme/                # Theme configuration
│   │   │   ├── res/
│   │   │   │   ├── drawable/                # Dice face images (dice_1 to dice_6)
│   │   │   │   └── values/
│   │   │   │       └── strings.xml           # String resources
│   │   │   └── AndroidManifest.xml
│   │   ├── test/                             # Unit tests
│   │   └── androidTest/                      # Instrumented tests
│   └── build.gradle.kts
├── build.gradle.kts
└── settings.gradle.kts
```

## Getting Started

### Prerequisites

- Android Studio (latest version)
- JDK 11 or higher
- Android SDK with API level 24+
- Basic knowledge of Kotlin

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

### Main Composable

The app uses a simple state-based architecture:

```kotlin
@Composable
fun DiceWithButtonAndImage(modifier: Modifier = Modifier) {
    var result by remember { mutableStateOf(1) }
    
    val imageResource = when (result) {
        1 -> R.drawable.dice_1
        2 -> R.drawable.dice_2
        // ... other cases
        else -> R.drawable.dice_6
    }
    
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Image(
            painter = painterResource(imageResource),
            contentDescription = result.toString()
        )
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = { result = (1..6).random() }) {
            Text(stringResource(R.string.roll))
        }
    }
}
```

## Dependencies

- `androidx.core:core-ktx`
- `androidx.lifecycle:lifecycle-runtime-ktx`
- `androidx.activity:activity-compose`
- `androidx.compose.ui:ui`
- `androidx.compose.material3:material3`
- `androidx.compose.ui:ui-tooling-preview`

## Learning Outcomes

After completing or studying this project, you should understand:

- How to create a basic Compose UI
- How to manage state in Compose
- How to handle user interactions (button clicks)
- How to use resources (strings, drawables) in Compose
- Basic layout principles in Compose

## Future Enhancements

Potential improvements:
- Multiple dice support
- Dice history/log
- Different dice types (4-sided, 8-sided, etc.)
- Animation effects
- Sound effects

## License

This project is part of a learning collection. Please refer to the main repository for license information.

