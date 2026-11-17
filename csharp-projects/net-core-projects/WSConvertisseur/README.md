# WSConvertisseur

ASP.NET Core REST service for currency (devise) CRUD and conversion.

## Overview

WSConvertisseur exposes devise endpoints used by ClientConvertisseur. Models use data annotations; Swagger includes XML comments. An in-memory or configured store backs rates relative to a reference currency.

WSConvertisseurTests exercises the controllers.

## Features

- Devise create, read, update, delete
- Amount conversion between devises
- Data annotation validation
- Swagger with XML docs
- Controller unit tests

## Stack

- C# / .NET 8
- ASP.NET Core
- Swagger / OpenAPI
- Data annotations
- xUnit (WSConvertisseurTests)

## Layout

```
WSConvertisseur/
├── WSConvertisseur/
├── WSConvertisseurTests/
├── WSConvertisseur.sln
└── README.md
```

## Run

```bash
dotnet run --project WSConvertisseur
# Swagger: /swagger
dotnet test WSConvertisseurTests
```
