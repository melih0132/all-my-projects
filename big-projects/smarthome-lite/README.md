# SmartHome Lite - Distributed Smart Home (domotique)

This repository is a redirect to the **[SmartHome Lite](https://github.com/melih0132/smarthome-lite)** project repository. For detailed information about the SmartHome Lite project, including its architecture, setup, API, hardware (Raspberry Pi / Z-Wave), and deployment, please visit the dedicated repository.

## Project Overview

The SmartHome Lite project is a portfolio showcase (SAE — domotique distribuée et embarquée): intelligent lighting and device control with presence detection, ambient light adaptation (smart dimming), rule-based automation, and classical ML (classification, regression) on the backend.

## Key Features

- Manual control of lights and sockets (mobile and web)
- Presence detection (Z-Wave, e.g. MultiSensor 7) and history
- IF-THEN rule engine and predefined scenarios
- Smart dimming from ambient light readings
- AI-assisted scenario classification and intensity prediction (scikit-learn)
- Dashboards and charts (presence, luminosity)

## Technologies Used

- **Database:** PostgreSQL, TimescaleDB (time-series)
- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic, JWT, bcrypt
- **Web:** Next.js (App Router), React, TypeScript, Tailwind CSS
- **Mobile:** Kotlin, Jetpack Compose, Material 3, Retrofit
- **Edge:** Raspberry Pi, Flask API, Z-Wave JS UI
- **ML:** scikit-learn, pandas, NumPy, joblib

## Access the Project

To explore the project in detail, please visit the **[SmartHome Lite repository](https://github.com/melih0132/smarthome-lite)**.
