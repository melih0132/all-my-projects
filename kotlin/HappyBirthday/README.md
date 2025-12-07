# HappyBirthday

A personalized birthday card application built with Jetpack Compose. This app demonstrates image composition, text styling, and layout techniques in modern Android development.

## Overview

HappyBirthday is an Android application that displays a customizable birthday card with a message and background image. It showcases how to combine images and text in Compose to create visually appealing layouts.

## Features

- **Customizable Birthday Message**: Display personalized birthday greetings
- **Background Image**: Beautiful background image with overlay effect
- **Text Styling**: Large, styled text with custom fonts and sizes
- **Image Composition**: Demonstrates Box layout with image and text overlay
- **Content Scaling**: Image scaling and alpha transparency effects

## Screenshots

The app displays:
- A background party image with 50% opacity
- A large birthday message (e.g., "Happy Birthday Sam!")
- A sender name (e.g., "From Emma")

## Technologies

- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Design System**: Material Design 3
- **Minimum SDK**: 24
- **Target SDK**: 36
- **Compile SDK**: 36

## Key Concepts Demonstrated

This project teaches the following Jetpack Compose concepts:

1. **Layout Composition**
   - `Box` composable for overlaying elements
   - `Column` composable for vertical text arrangement
   - `Surface` composable for theming

2. **Image Handling**
   - `Image` composable with `painterResource`
   - `ContentScale.Crop` for image scaling
   - Alpha transparency for overlay effects

3. **Text Styling**
   - Custom font sizes (100sp for message, 36sp for sender)
   - Text alignment and positioning
   - Line height adjustments

4. **Layout Modifiers**
   - `fillMaxSize()` for full-screen layout
   - `padding()` for spacing
   - `align()` for positioning within layouts

## Project Structure

```
HappyBirthday/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/happybirthday/
│   │   │   │   ├── MainActivity.kt          # Main activity and composables
│   │   │   │   └── ui/theme/                # Theme configuration
│   │   │   ├── res/
│   │   │   │   ├── drawable/                # Background images
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

### Main Composable Structure

The app uses a Box layout to overlay text on an image:

```kotlin
@Composable
fun GreetingImage(message: String, from: String, modifier: Modifier = Modifier) {
    val image = painterResource(R.drawable.androidparty)
    Box(modifier) {
        Image(
            painter = image,
            contentDescription = null,
            contentScale = ContentScale.Crop,
            alpha = 0.5F
        )
        GreetingText(
            message = message,
            from = from,
            modifier = Modifier
                .fillMaxSize()
                .padding(8.dp)
        )
    }
}
```

### Text Styling

The birthday message uses large, centered text:

```kotlin
@Composable
fun GreetingText(message: String, from: String, modifier: Modifier = Modifier) {
    Column(
        verticalArrangement = Arrangement.Center,
        modifier = modifier
    ) {
        Text(
            text = message,
            fontSize = 100.sp,
            lineHeight = 116.sp,
            textAlign = TextAlign.Center
        )
        Text(
            text = from,
            fontSize = 36.sp,
            modifier = Modifier
                .padding(16.dp)
                .align(alignment = Alignment.CenterHorizontally)
        )
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

- How to compose images and text in Compose
- How to use Box layout for overlaying elements
- How to style text with custom sizes and alignments
- How to apply transparency and scaling to images
- Layout arrangement and spacing techniques

## Customization

To customize the birthday card:

1. Edit the message in `MainActivity.kt`:
   ```kotlin
   GreetingImage(message = "Happy Birthday Sam!", from = "From Emma")
   ```

2. Replace the background image in `res/drawable/`

3. Adjust text sizes and colors in the composable functions

## Future Enhancements

Potential improvements:
- User input fields for customizing message
- Multiple card templates
- Animation effects
- Save/share functionality
- Multiple background options

## License

This project is part of a learning collection. Please refer to the main repository for license information.

