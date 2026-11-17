# FilmRatingsApp.Tests.MSTest

MSTest project for FilmRatingsApp unit and UI-thread tests.

## Overview

FilmRatingsApp.Tests.MSTest validates view models and helpers with MSTest. UI control tests must use `[UITestMethod]` so they run on the WinUI UI thread. Dependency injection in the app allows mock services in constructors.

Run from Visual Studio Test Explorer or `dotnet test`.

## Features

- MSTest unit tests
- UITestMethod support for WinUI thread
- Mockable service interfaces
- Startup Initialize helpers
- Solution-integrated test project

## Stack

- C# / .NET 7 (Windows)
- MSTest
- WinUI test host (for UI tests)

## Layout

```
FilmRatingsApp.Tests.MSTest/
├── TestClass.cs
├── Initialize.cs
├── Usings.cs
├── FilmRatingsApp.Tests.MSTest.csproj
└── README.md
```

## Run

```bash
dotnet test FilmRatingsApp.Tests.MSTest/FilmRatingsApp.Tests.MSTest.csproj
```
