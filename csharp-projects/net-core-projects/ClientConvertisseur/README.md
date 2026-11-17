# ClientConvertisseur

WinUI 3 desktop clients that convert amounts between currencies via WSConvertisseur.

## Overview

ClientConvertisseur ships two apps in one solution: V1 with logic in code-behind, and V2 with MVVM (models, views, view models, services). Both call the currency REST service for rates and conversion.

Run WSConvertisseur first and point the client service URL at that host.

## Features

- Amount conversion between devises
- WinUI 3 / XAML UI
- V1 simple code-behind client
- V2 MVVM client with bindings
- HTTP service layer to WSConvertisseur

## Stack

- C# / .NET 8 (Windows)
- WinUI 3
- XAML
- HTTP client services

## Layout

```
ClientConvertisseur/
├── ClientConvertisseurV1/
├── ClientConvertisseurV2/
├── ClientConvertisseur.sln
└── README.md
```

## Run

```bash
# start WSConvertisseur, then:
dotnet build ClientConvertisseur.sln
# open ClientConvertisseur.sln in Visual Studio and Run V1 or V2
```
