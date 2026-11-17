# Event Poll

Flutter client for event polls with auth, listing, creation, and voting.

## Overview

Event Poll talks to a REST backend (default `http://localhost:5240` in `lib/configs.dart`). Users can sign up, log in, browse events, open details, and create polls. Auth and poll state use Provider.

The UI is localized for French (Material localizations, `fr` locale).

## Features

- Login and signup
- Event / poll list and detail
- Create event poll
- Auth token wired into polls state
- Named routes with shared scaffold
- HTTP client against a local API

## Stack

- Dart / Flutter
- Provider
- http
- flutter_localizations

## Layout

```
event_poll/
├── android/
├── ios/
├── lib/
│   ├── configs.dart
│   ├── main.dart
│   ├── models/
│   ├── states/
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
# start the API on the URL in lib/configs.dart, then:
flutter pub get
flutter run
```
