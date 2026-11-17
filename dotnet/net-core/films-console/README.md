# Films Console

.NET console sample for film database CRUD with Entity Framework Core.

## Overview

Lab-style methods against PostgreSQL: list user emails, find films by name pattern, add users, update films, and delete films including related avis. LINQ and EF Core (`Include`, `SaveChanges`, `ILike`) drive the exercises.

## Features

- List utilisateur emails
- Search films (e.g. name starts with "Le")
- Add utilisateurs
- Update and delete films with related avis

## Stack

- .NET console, C#
- Entity Framework Core, PostgreSQL

## Layout

```
films-console/
├── TP3console/       → console project
└── TP3console.sln
```

## Run

```bash
cd films-console
dotnet restore
dotnet run --project TP3console
```

Set the PostgreSQL connection string before running (`Password=CHANGE_ME` placeholders).
