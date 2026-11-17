# ApiRestAvecEtat

ASP.NET Core REST API for TV series with CORS and EF Core state tracking.

## Overview

ApiRestAvecEtat provides CRUD endpoints for series stored in PostgreSQL. Entity Framework Core tracks entity state across requests. CORS is configured (AllowAll) so browser clients can call the API.

Swagger is enabled for interactive testing.

## Features

- Series create, read, update, delete
- EF Core change tracking
- PostgreSQL persistence
- CORS AllowAll policy
- Swagger / OpenAPI

## Stack

- C# / .NET 8
- ASP.NET Core
- Entity Framework Core
- PostgreSQL
- Swagger
- CORS

## Layout

```
ApiRestAvecEtat/
├── ApiRestAvecEtat/
├── ApiRestAvecEtat.sln
└── README.md
```

## Run

```bash
# set PostgreSQL connection in ApiRestAvecEtat/appsettings.json
dotnet ef database update --project ApiRestAvecEtat
dotnet run --project ApiRestAvecEtat
# Swagger: /swagger
```
