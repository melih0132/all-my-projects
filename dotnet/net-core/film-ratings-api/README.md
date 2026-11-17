# Film Ratings API

ASP.NET Core REST API for users and film ratings on PostgreSQL.

## Overview

CRUD for utilisateurs with lookup by id or email. Entity Framework Core maps to PostgreSQL; data access uses a repository pattern. Swagger documents the HTTP surface. An xUnit test project covers controller behavior.

## Features

- Utilisateur create, read, update, delete
- Get by id and by email
- EF Core + PostgreSQL
- Swagger / OpenAPI
- xUnit controller tests

## Stack

- ASP.NET Core, C#
- Entity Framework Core, PostgreSQL
- Swagger, xUnit

## Layout

```
film-ratings-api/
├── APIfilms/          → Web API project
├── APIfilmsTests/     → xUnit tests
└── APIfilms.sln
```

## Run

```bash
cd film-ratings-api
dotnet restore
dotnet run --project APIfilms
```

Set the PostgreSQL connection string before running (`Password=CHANGE_ME` placeholders).
