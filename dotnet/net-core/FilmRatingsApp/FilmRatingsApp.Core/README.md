# FilmRatingsApp.Core

Shared .NET library for FilmRatingsApp contracts, services, and helpers.

## Overview

FilmRatingsApp.Core holds reusable code consumed by the WinUI app and tests: interfaces, helper types, and service implementations that do not depend on WinUI. Targeting net7.0 keeps the library usable outside the Windows UI project.

Keep UI-specific types in the FilmRatingsApp app project.

## Features

- Shared contracts / interfaces
- Core service implementations
- Cross-project helpers
- net7.0 class library
- Referenced by app and tests

## Stack

- C# / .NET 7
- Class library (no WinUI dependency)

## Layout

```
FilmRatingsApp.Core/
├── Contracts/
├── Helpers/
├── Services/
├── FilmRatingsApp.Core.csproj
└── README.md
```

## Run

```bash
dotnet build FilmRatingsApp.Core/FilmRatingsApp.Core.csproj
```
