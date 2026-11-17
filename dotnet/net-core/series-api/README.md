# Series API

ASP.NET Core REST API for TV series with CORS and EF Core state tracking.

## Overview

CRUD endpoints for series stored in PostgreSQL. Entity Framework Core tracks entity state. CORS is configured so browser clients can call the API. Swagger is enabled for interactive testing.

## Features

- Series create, read, update, delete
- EF Core change tracking
- PostgreSQL persistence
- CORS AllowAll for local clients
- Swagger UI

## Stack

- ASP.NET Core, C#
- Entity Framework Core, PostgreSQL
- Swagger

## Layout

```
series-api/
├── ApiRestAvecEtat/     → Web API project
└── ApiRestAvecEtat.sln
```

## Run

```bash
cd series-api
dotnet restore
dotnet run --project ApiRestAvecEtat
```

Configure the connection string in `appsettings.json` before running.
