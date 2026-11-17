# FilmRatingsApp

WinUI 3 UI project for the film ratings desktop client.

## Overview

This project hosts App.xaml, views, view models, services, styles, and assets for FilmRatingsApp. It depends on FilmRatingsApp.Core for shared contracts and helpers and uses Windows App SDK packaging for local run and MSIX publish.

Generated from Windows Template Studio patterns (activation, theme, navigation).

## Features

- XAML views and view models
- Navigation and activation services
- Theme and settings helpers
- Styles and string resources
- WinUI packaging entry point

## Stack

- C# / .NET 7 (Windows)
- WinUI 3
- XAML
- Windows App SDK

## Layout

```
FilmRatingsApp/
├── Views/
├── ViewModels/
├── Services/
├── Models/
├── Styles/
├── App.xaml
└── README.md
```

## Run

```bash
# from solution root FilmRatingsApp/
dotnet build FilmRatingsApp/FilmRatingsApp.csproj
# prefer Visual Studio: set FilmRatingsApp as startup project and Run
```
