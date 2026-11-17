# FilmRatingsApp

WinUI 3 desktop app for browsing and rating films (MVVM solution).

## Overview

FilmRatingsApp is a multi-project WinUI solution: UI app, shared Core library, and MSTest project. Views and view models manage film lists, details, and settings with Template Studio-style services and DI.

The UI follows system light/dark theme. Package as MSIX from Visual Studio when needed.

## Features

- Film list and detail navigation
- Ratings and user avis flows
- MVVM with services and contracts
- Shared Core class library
- MSTest project
- System theme support

## Stack

- C# / .NET 7 (Windows)
- WinUI 3
- XAML
- MVVM / DI
- MSTest

## Layout

```
FilmRatingsApp/
├── FilmRatingsApp/
├── FilmRatingsApp.Core/
├── FilmRatingsApp.Tests.MSTest/
├── FilmRatingsApp.sln
└── README.md
```

## Run

```bash
dotnet build FilmRatingsApp.sln
# open FilmRatingsApp.sln in Visual Studio and Run FilmRatingsApp
dotnet test FilmRatingsApp.Tests.MSTest
```
