# Currency Converter API

ASP.NET Core REST service for currency (devise) CRUD and conversion.

## Overview

Exposes devise endpoints used by the WinUI currency-converter-client. Models use data annotations; Swagger includes XML comments. Tests exercise the controllers.

## Features

- Devise create, read, update, delete
- Amount conversion between devises
- Data annotation validation
- Swagger with XML comments
- xUnit controller tests

## Stack

- ASP.NET Core, C#
- Swagger, xUnit

## Layout

```
currency-converter-api/
├── WSConvertisseur/          → Web API project
├── WSConvertisseurTests/     → xUnit tests
└── WSConvertisseur.sln
```

## Run

```bash
cd currency-converter-api
dotnet restore
dotnet run --project WSConvertisseur
```

Point the WinUI client service URL at this host.
