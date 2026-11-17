# Film Ratings App

WinUI 3 desktop app for browsing and rating films (MVVM solution).

## Overview

Multi-project WinUI solution: UI app, shared Core library, and MSTest project. Views and view models manage film lists, details, and settings with services and DI. Follows system light/dark theme.

## Features

- Film list and detail navigation
- Ratings and user avis flows
- MVVM with services and contracts
- MSTest coverage

## Stack

- WinUI 3, XAML, C#
- MSTest

## Layout

```
film-ratings-app/
├── FilmRatingsApp/            → WinUI UI
├── FilmRatingsApp.Core/       → shared library
├── FilmRatingsApp.Tests.MSTest/
└── FilmRatingsApp.sln
```

## Run

Open `FilmRatingsApp.sln` in Visual Studio and run the WinUI project. Package as MSIX when needed.
