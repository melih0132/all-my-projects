# Big Projects

This folder contains my personal and academic large-scale projects that I have been working on or have completed in the past. These projects cover a wide range of topics and technologies, showcasing my versatility and commitment to continuous learning and improvement.

## Projects Included

### 1. [Bird Counting Management LPO](lpo)
This project helps manage bird counting data for the Ligue de Protection des Oiseaux (LPO). It includes:
- A database model (MCD and MLD)
- SQL queries and insertions in PostgreSQL
- Statistics generated in Excel
- An interactive dashboard built with Power BI

**Technologies**: PostgreSQL, SQL, Excel, Power BI, pgAdmin4

### 2. [Uber-like Application (.NET & Vue.js)](uber-dotnet-vue)
A full-stack application inspired by Uber, featuring:
- Backend API built with .NET Core
- Frontend application using Vue.js
- User authentication with JWT
- Ride booking and meal delivery features
- Interactive maps with Leaflet
- Responsive UI design

**Technologies**: .NET 8, Vue.js 3, PostgreSQL, Entity Framework Core, JWT, Leaflet, Vuetify

### 3. [Uber-like Application (Laravel)](uber-laravel)
A comprehensive data management system for an Uber-like application, including:
- User and trip management
- Payment handling
- Ride reservations
- Ratings and feedback system
- Geographical data analysis
- Security and data protection measures

**Technologies**: Laravel, PostgreSQL, Power BI, RESTful API

### 4. [Collaborative AI Chat Application](shared-ia)
A full-stack collaborative AI chat application where multiple users (max 4) can converse with an AI through a collective message validation system. Features include:
- Real-time chat with Socket.io
- Collective message validation system
- Conflict resolution with voting mechanism
- OpenAI integration for AI responses
- User authentication with JWT
- Room management and invitations
- Message editing, deletion, and retraction
- Typing indicators and user presence

**Technologies**: Node.js, Express.js, React, TypeScript, Socket.io, PostgreSQL, OpenAI API, JWT, TailwindCSS, Zustand, Vite

### 5. [SmartHome Lite (domotique)](smarthome-lite)
A distributed smart-home showcase: backend API, Next.js dashboard, Android app, and Raspberry Pi / Z-Wave integration. Includes presence, rules, smart dimming from ambient light, and ML-based scenario assistance.

**Technologies**: FastAPI, PostgreSQL, TimescaleDB, Next.js, Kotlin/Jetpack Compose, Raspberry Pi, Z-Wave JS, scikit-learn

## Technologies Used

### Backend
- **.NET Core**: Full-stack application development
- **Laravel**: PHP framework for data management systems
- **Node.js/Express.js**: RESTful APIs and real-time communication
- **FastAPI**: Python ASGI API (SmartHome Lite)
- **PostgreSQL**: Relational database management
- **TimescaleDB**: Time-series extension for sensor history (SmartHome Lite)

### Frontend
- **Vue.js**: Progressive JavaScript framework
- **React**: Modern UI library with TypeScript
- **Next.js**: React framework (App Router) for SmartHome Lite web UI
- **HTML/CSS/JavaScript**: Core web technologies

### Database & Tools
- **PostgreSQL**: Primary database system
- **Power BI**: Data visualization and business intelligence
- **Excel**: Statistical analysis and data processing
- **pgAdmin4**: PostgreSQL administration tool

### Real-time Communication
- **Socket.io**: Real-time bidirectional communication
- **WebSockets**: Persistent connections for live updates

### Security
- **JWT Authentication**: Secure token-based authentication
- **Data Encryption**: Protection of sensitive information
- **XSS Prevention**: Web application security

### Embedded & Mobile (SmartHome Lite)
- **Raspberry Pi**: Edge controller, Flask API, Z-Wave devices
- **Kotlin / Jetpack Compose**: Android client
- **scikit-learn**: Scenario classification and regression models

## Project Structure

```
big-projects/
├── lpo/                    → Bird Counting Management System
│   ├── 1_Modelisation/     → Database modeling (MCD, MLD)
│   ├── 2_Insert_Query/      → SQL scripts and data insertion
│   ├── 3_View_Stat/        → Statistics and views
│   └── 4_PowerBI/          → Power BI dashboard
├── uber-dotnet-vue/         → Full-stack Uber clone
│   ├── UberApi/            → .NET Core backend
│   └── UberVueJS/          → Vue.js frontend
├── uber-laravel/           → Laravel data management system
├── shared-ia/              → Collaborative AI Chat Application
│   ├── backend/            → Node.js/Express backend
│   └── frontend/           → React/TypeScript frontend
└── smarthome-lite/         → Redirect README → GitHub (domotique, FastAPI, Next.js, Android, RPi)
```

## Getting Started

Each project has its own README with detailed instructions. To explore a project:

1. Navigate to the project directory
2. Read the project's README.md for specific setup instructions
3. Follow the installation and configuration steps
4. Run the project according to its documentation

Feel free to explore the repositories for more detailed information on each project!
