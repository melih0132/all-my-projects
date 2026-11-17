# Weather App

Flutter client for current weather via OpenWeatherMap and device location.

## Overview

Weather App loads the user's position, then fetches and displays weather for that place. Search is available for other locations. Provider injects the API and geolocation services.

An OpenWeatherMap API key is required. Copy `lib/config.example.dart` to `lib/config.dart` and set the key before running.

## Features

- Geolocation-based weather on launch
- City / location search
- OpenWeatherMap HTTP integration
- Loading screen and weather detail UI
- Dark Material theme
- French locale formatting via intl

## Stack

- Dart / Flutter
- Provider
- http
- geolocator
- intl

## Layout

```
weather_app/
├── android/
├── ios/
├── lib/
│   ├── config.example.dart
│   ├── main.dart
│   ├── models/
│   ├── services/
│   └── ui/
├── linux/
├── macos/
├── web/
├── windows/
├── pubspec.yaml
└── README.md
```

## Run

```bash
cp lib/config.example.dart lib/config.dart
# set openWeatherMapApiKey in lib/config.dart
flutter pub get
flutter run
```
