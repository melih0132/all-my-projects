# Multi-Service Stack

PHP web container talking to MariaDB, PostgreSQL, and Redis.

## Overview

Compose orchestration of multiple datastores on one network, with a status page that probes each dependency.

## Features

- PHP Apache app with PDO MySQL / PostgreSQL
- MariaDB, PostgreSQL, Redis services
- Named volumes for data stores
- Dependency `depends_on` wiring

## Stack

- Docker Compose
- PHP, Apache
- MariaDB, PostgreSQL, Redis

## Layout

```
05-multi-service-stack/
├── index.php
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Run

```bash
cd docker/compose/multi-service
docker compose up --build -d
```

App: http://localhost:8083
