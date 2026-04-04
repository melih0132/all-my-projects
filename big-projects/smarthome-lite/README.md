# SmartHome Lite

This folder is a redirect to the **[SmartHome Lite](https://github.com/oeoecbien/smarthome-lite)** project repository. For architecture, setup, API, hardware (Raspberry Pi / Z-Wave), and deployment details, see the dedicated repository.

## Project Overview

SmartHome Lite is a portfolio showcase project (SAE — domotique distribuée et embarquée): intelligent lighting and device control with presence detection, ambient light adaptation (smart dimming), rule-based automation, and classical ML (classification, regression) on the backend.

## Key Features

- Manual control of lights and sockets (mobile and web)
- Presence detection (Z-Wave, e.g. MultiSensor 7) and history
- IF-THEN rule engine and predefined scenarios
- Smart dimming from ambient light readings
- AI-assisted scenario classification and intensity prediction (scikit-learn)
- Dashboards and charts (presence, luminosity)

## Technologies Used

- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic, JWT, bcrypt
- **Database:** PostgreSQL, TimescaleDB (time-series)
- **Web:** Next.js (App Router), React, TypeScript, Tailwind CSS
- **Mobile:** Kotlin, Jetpack Compose, Material 3, Retrofit
- **Edge:** Raspberry Pi, Flask API, Z-Wave JS UI
- **ML:** scikit-learn, pandas, numpy, joblib

## Access the Project

Explore the code and documentation on GitHub: **[oeoecbien/smarthome-lite](https://github.com/oeoecbien/smarthome-lite)**.
