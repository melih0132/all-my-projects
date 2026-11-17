# TP3console

.NET console sample for film database CRUD with Entity Framework Core.

## Overview

TP3console runs lab-style methods against PostgreSQL: list user emails, find films by name pattern, add users, update films, and delete films including related avis. LINQ and EF Core (`Include`, `SaveChanges`, `ILike`) drive the exercises.

Connection settings belong in configuration or the DbContext setup before running.

## Features

- List utilisateur emails
- Search films (e.g. name starts with "Le")
- Add utilisateurs
- Update and delete films with related avis
- LINQ + EF Core against PostgreSQL

## Stack

- C# / .NET 8
- Entity Framework Core
- PostgreSQL
- LINQ

## Layout

```
TP3console/
├── TP3console/
├── TP3console.sln
└── README.md
```

## Run

```bash
# configure PostgreSQL for the DbContext
dotnet run --project TP3console
```
