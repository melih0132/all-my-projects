# Todo App

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
todo-app/
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
