# APIfilms

ASP.NET Core REST API for users and film ratings on PostgreSQL.

## Overview

APIfilms exposes utilisateur CRUD with lookup by id or email. Entity Framework Core maps to PostgreSQL; data access uses a repository pattern. Swagger documents the HTTP surface.

An xUnit test project covers controller behavior.

## Features

- Utilisateur create, read, update, delete
- Get by id and by email
- EF Core + PostgreSQL
- Repository pattern
- Swagger / OpenAPI
- APIfilmsTests (xUnit)

## Stack

- C# / .NET 8
- ASP.NET Core
- Entity Framework Core
- PostgreSQL
- Swagger
- xUnit

## Layout

```
APIfilms/
├── APIfilms/
├── APIfilmsTests/
├── APIfilms.sln
└── README.md
```

## Run

```bash
# set PostgreSQL connection in APIfilms/appsettings.json
dotnet ef database update --project APIfilms
dotnet run --project APIfilms
# Swagger: /swagger
dotnet test APIfilmsTests
```
