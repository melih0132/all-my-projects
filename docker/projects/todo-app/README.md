# Todo Application

PHP-FPM todo app with Nginx, MariaDB, PostgreSQL, and Redis.

## Overview

Multi-service Compose stack for a simple todo UI and API under `src/`.

## Features

- Nginx reverse proxy to PHP-FPM
- MariaDB and PostgreSQL services
- Redis cache service
- Composer install on container start

## Stack

- Docker Compose
- PHP-FPM, Nginx
- MariaDB, PostgreSQL, Redis
- Composer

## Layout

```
06-todo-application/
├── src/
├── nginx.conf
├── composer.json
├── docker-compose.yml
└── README.md
```

## Run

```bash
cd docker/projects/todo-app
docker compose up -d
```

App: http://localhost:8080
