# Currency Converter Client

WinUI 3 desktop clients that convert amounts between currencies via the currency-converter-api.

## Overview

Two apps in one solution: V1 with logic in code-behind, and V2 with MVVM (models, views, view models, services). Both call the currency REST service for rates and conversion.

Run the API first and point the client service URL at that host.

## Features

- Amount conversion between devises
- WinUI 3 / XAML UI
- V1 code-behind client
- V2 MVVM client

## Stack

- WinUI 3, XAML, C#
- HTTP client against the currency API

## Layout

```
currency-converter-client/
├── ClientConvertisseurV1/
├── ClientConvertisseurV2/
└── ClientConvertisseur.sln
```

## Run

Open `ClientConvertisseur.sln` in Visual Studio. Start `currency-converter-api`, then run V1 or V2.
