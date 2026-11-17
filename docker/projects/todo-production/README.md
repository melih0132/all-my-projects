# Todo Production

Production-oriented todo stack with custom PHP image and GitHub Actions publish workflow.

## Overview

Compose app with Postgres and Redis, env-driven config, and a sample CI pipeline under `.github/workflows`.

## Features

- Custom `docker/php` image
- Nginx + PHP services
- PostgreSQL and Redis
- `env.example` for secrets
- GitHub Actions Docker publish workflow

## Stack

- Docker Compose
- PHP, Nginx
- PostgreSQL, Redis
- GitHub Actions

## Layout

```
todo-production/
├── docker/
│   ├── nginx/
│   └── php/
├── src/
├── .github/workflows/
├── docker-compose.yml
├── docker-compose.override.yml
├── env.example
└── README.md
```

## Run

```bash
cd docker/projects/todo-production
cp env.example .env
docker compose up --build -d
```

App: `http://localhost:8080`
