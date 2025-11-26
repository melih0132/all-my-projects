# **.NET CORE PROJECTS**

Welcome to my **PROJECTS** repository! This repository serves as a curated collection of my development projects, each housed in its own directory. These projects cover a wide range of domains, technologies, and complexity levels, showcasing my skills and interests in software development.

## **Projects**

1. **[APIfilms](APIfilms)** : REST API for managing users and films with a rating system, using Entity Framework Core and PostgreSQL

2. **[ApiRestAvecEtat](ApiRestAvecEtat)** : REST API for managing TV series with CORS support and Entity Framework Core

3. **[ClientConvertisseur](ClientConvertisseur)** : WinUI 3 application for currency conversion (V1 simple version and V2 with MVVM)

4. **[FilmRatingsApp](FilmRatingsApp)** : Complete WinUI 3 application for film management and rating with modular architecture

5. **[TP3console](TP3console)** : Console application for manipulating a film database with Entity Framework Core

6. **[WSConvertisseur](WSConvertisseur)** : REST web service for currency conversion with Swagger documentation

## **Technologies & Tools**

Throughout these projects, I have utilized a diverse set of technologies and tools, including:

### Languages

- **Backend** : C#
- **Frontend** : XAML, C#
- **Database** : SQL (PostgreSQL)

### Frameworks & Libraries

- **Web** : ASP.NET Core, REST API
- **Desktop** : .NET (WinUI 3)
- **ORM** : Entity Framework Core
- **API Documentation** : Swagger/OpenAPI

### Databases & Tools

- **Databases** : PostgreSQL
- **Version Control** : Git, GitHub
- **Testing** : xUnit, MSTest

### Development Environments

- **IDE** : Visual Studio

## Project Structure

```
.net-core-projects/
├── APIfilms/                    → REST API for films and users
│   ├── APIfilms/                → Main project
│   └── APIfilmsTests/           → Unit tests
├── ApiRestAvecEtat/             → REST API for series with CORS
│   └── ApiRestAvecEtat/         → Main project
├── ClientConvertisseur/         → WinUI 3 converter application
│   ├── ClientConvertisseurV1/   → Simple version (without MVVM)
│   └── ClientConvertisseurV2/   → Version with MVVM
├── FilmRatingsApp/              → WinUI 3 film management application
│   ├── FilmRatingsApp/          → Main project (UI)
│   ├── FilmRatingsApp.Core/     → Shared library
│   └── FilmRatingsApp.Tests.MSTest/ → Unit tests
├── TP3console/                  → Entity Framework console application
│   └── TP3console/              → Main project
├── WSConvertisseur/             → Currency conversion web service
│   ├── WSConvertisseur/         → Main project
│   └── WSConvertisseurTests/    → Unit tests
└── README.md                    → Project documentation
```

## Getting Started

To explore a project:

1. Navigate to the desired project directory
2. Read the project's README.md for specific instructions
3. Follow the setup and installation steps
4. Run the project according to its documentation

## Project Details

### APIfilms
Complete REST API with Repository pattern, Entity Framework Core and PostgreSQL. CRUD management of users with search by ID or email.

### ApiRestAvecEtat
REST API for managing series with CORS configuration to allow cross-origin requests from frontend applications.

### ClientConvertisseur
WinUI 3 application demonstrating two approaches: a simple version and a version with MVVM architecture for currency conversion.

### FilmRatingsApp
Complete WinUI 3 application with modular architecture, separation into multiple projects (Core, Tests) and system theme support.

### TP3console
Educational console application demonstrating the use of Entity Framework Core with PostgreSQL, including LINQ query examples and CRUD operations.

### WSConvertisseur
REST web service for currency management with complete Swagger documentation and data validation.

Feel free to explore the repositories, and don't hesitate to reach out if you have any questions or need further information!
