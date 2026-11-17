# HappyBirthday

Android birthday card screen built with Jetpack Compose.

## Overview

HappyBirthday overlays a large greeting and a sender line on a background image. A `Box` stacks the image and text; alpha and content scale control the photo look.

Message and sender strings are set in the main composable and can be edited for a custom card.

## Features

- Full-screen birthday message
- Sender attribution text
- Background image with crop and alpha
- Box + Column composition
- Material 3 surface theming

## Stack

- Kotlin
- Jetpack Compose
- Material Design 3
- Gradle (Kotlin DSL)

## Layout

```
HappyBirthday/
├── app/
│   ├── src/main/
│   └── build.gradle.kts
├── build.gradle.kts
├── settings.gradle.kts
└── README.md
```

## Run

```bash
./gradlew assembleDebug
# or open in Android Studio and Run
```

On Windows: `gradlew.bat assembleDebug`
