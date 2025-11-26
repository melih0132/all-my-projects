# C# Projects

This folder contains my C# and .NET development projects, covering a wide range of applications from desktop applications to web APIs and game development. These projects demonstrate my proficiency in C# programming, .NET frameworks, and various technologies.

## Projects Included

### 1. [C# with Database](csharp-with-db)
Projects developed in C# that utilize database integration, primarily with PostgreSQL.

**Projects:**
- **[DortanApp](csharp-with-db/DORTANAPP)**: WPF application for managing activity reservations in a town hall, integrated with PostgreSQL database

**Technologies**: C#, WPF, PostgreSQL, Entity Framework

### 2. [C# without Database](csharp-without-db)
C# projects that focus on programming concepts, algorithms, and applications without database integration.

**Projects:**
- **[csharp](csharp-without-db/csharp)**: Console-based applications demonstrating fundamental C# concepts
  - Bank Account: Object-oriented programming example
  - Minesweeper Console: Game logic implementation
- **[WPF](csharp-without-db/WPF)**: Desktop applications built with Windows Presentation Foundation
  - **EVIT_SHURIKEN**: WPF game application

**Technologies**: C#, WPF, Console Applications

### 3. [.NET Core Projects](.net-core-projects)
Modern .NET Core applications including REST APIs, WinUI 3 desktop applications, and web services.

**Projects:**
- **[APIfilms](.net-core-projects/APIfilms)**: REST API for managing users and films with rating system
- **[ApiRestAvecEtat](.net-core-projects/ApiRestAvecEtat)**: REST API for managing TV series with CORS support
- **[ClientConvertisseur](.net-core-projects/ClientConvertisseur)**: WinUI 3 currency conversion application (V1 simple, V2 with MVVM)
- **[FilmRatingsApp](.net-core-projects/FilmRatingsApp)**: Complete WinUI 3 film management application with modular architecture
- **[TP3console](.net-core-projects/TP3console)**: Console application for manipulating film database with Entity Framework Core
- **[WSConvertisseur](.net-core-projects/WSConvertisseur)**: REST web service for currency conversion with Swagger documentation

**Technologies**: .NET Core, ASP.NET Core, WinUI 3, Entity Framework Core, PostgreSQL, Swagger/OpenAPI

### 4. [Unity](unity)
Games and interactive applications built with Unity game engine using C# scripting.

**Projects:**
- **[KUBE](unity/KUBE)**: 3D platformer game with physics and animations

**Technologies**: Unity, C#, Blender

## Technologies Used

### Languages & Frameworks
- **C#**: Primary programming language
- **.NET Core / .NET**: Modern cross-platform framework
- **ASP.NET Core**: Web API development
- **WPF**: Windows Presentation Foundation for desktop applications
- **WinUI 3**: Modern Windows UI framework
- **Unity**: Game development engine

### Databases & ORM
- **PostgreSQL**: Relational database management
- **Entity Framework Core**: Object-relational mapping
- **SQL**: Database queries and operations

### Development Tools
- **Visual Studio**: Primary IDE
- **Unity Hub / Unity Editor**: Game development environment
- **Git / GitHub**: Version control
- **Swagger / OpenAPI**: API documentation
- **xUnit / MSTest**: Unit testing frameworks

### Design Patterns & Architecture
- **MVVM**: Model-View-ViewModel pattern (WinUI 3)
- **Repository Pattern**: Data access abstraction
- **RESTful API**: Web service architecture
- **Object-Oriented Programming**: Core programming paradigm

## Project Structure

```
csharp-projects/
├── csharp-with-db/          → C# projects with database
│   └── DORTANAPP/           → WPF reservation management app
├── csharp-without-db/       → C# projects without database
│   ├── csharp/              → Console applications
│   │   ├── bank-account/    → OOP bank account example
│   │   └── Demineur Console/ → Minesweeper game
│   └── WPF/                 → WPF desktop applications
│       └── EVIT_SHURIKEN/   → WPF game
├── .net-core-projects/       → Modern .NET Core applications
│   ├── APIfilms/            → REST API for films
│   ├── ApiRestAvecEtat/    → REST API for series
│   ├── ClientConvertisseur/ → WinUI 3 converter app
│   ├── FilmRatingsApp/      → WinUI 3 film management
│   ├── TP3console/          → EF Core console app
│   └── WSConvertisseur/     → Currency conversion web service
└── unity/                   → Unity game development
    └── KUBE/                → 3D platformer game
```

## Getting Started

Each project has its own README with detailed instructions. To explore a project:

1. Navigate to the project directory
2. Read the project's README.md for specific setup instructions
3. Follow the installation and configuration steps
4. Run the project according to its documentation

### Prerequisites

- **.NET SDK**: For .NET Core projects (version 6.0 or higher recommended)
- **Visual Studio**: For WPF and .NET Core development
- **Unity Hub**: For Unity game projects (version 2022.3 LTS recommended)
- **PostgreSQL**: For projects with database integration
- **Node.js**: For some frontend dependencies (if applicable)

### Common Setup Steps

1. **For .NET Core Projects:**
   ```bash
   cd project-directory
   dotnet restore
   dotnet build
   dotnet run
   ```

2. **For WPF Projects:**
   - Open the `.sln` file in Visual Studio
   - Restore NuGet packages
   - Build and run the project

3. **For Unity Projects:**
   - Open Unity Hub
   - Add the project folder
   - Open the project in Unity Editor
   - Press Play to run

Feel free to explore the repositories for more detailed information on each project!

