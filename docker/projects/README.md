# Docker Projects

Fuller multi-service applications beyond single-lab Compose stacks.

## Overview

Two progressive todo apps: a local multi-DB Compose stack, then a production-oriented variant with a custom PHP image and GitHub Actions publish workflow.

## Stack

- Docker Compose
- PHP-FPM, Nginx
- MariaDB, PostgreSQL, Redis
- GitHub Actions

## Layout

```
projects/
├── todo-app/           → Nginx + PHP-FPM + MariaDB + PostgreSQL + Redis
└── todo-production/    → custom PHP image, Postgres, Redis, CI publish
```

## Run

```bash
cd docker/projects/todo-app
docker compose up -d
```

See each project README for ports and env setup.
