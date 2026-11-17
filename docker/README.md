# Docker

Progressive container labs from a single image to production-oriented stacks.

## Overview

Three stages: image basics, Compose services, then fuller todo applications with CI.

## Stack

- Docker, Docker Compose
- Node.js, PHP, Apache, Nginx
- MongoDB, MariaDB, PostgreSQL, Redis
- GitLab CI, GitHub Actions

## Layout

```
docker/
├── basics/
│   ├── alpine-container/
│   └── sass-compilation/
├── compose/
│   ├── nodejs-mongodb/
│   ├── php-apache-mariadb/
│   └── multi-service/
└── projects/
    ├── todo-app/
    └── todo-production/
```

## Run

```bash
cd docker/projects/todo-app
docker compose up -d
```

Open any lab README for build and access details.
