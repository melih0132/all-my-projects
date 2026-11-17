# Node.js + MongoDB

Express API with MongoDB via Docker Compose.

## Overview

Two-service stack: Node backend and MongoDB on a shared bridge network with a named volume.

## Features

- Express `/` and `/health` endpoints
- MongoDB service and volume
- Healthcheck on the app container

## Stack

- Docker Compose
- Node.js, Express
- MongoDB

## Layout

```
03-nodejs-mongodb/
├── server.js
├── package.json
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Run

```bash
cd docker-exercices/03-nodejs-mongodb
docker compose up --build -d
```

App: http://localhost:3000
