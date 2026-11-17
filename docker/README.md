# Docker

Progressive container labs from a single image to Compose stacks, Kubernetes, and fuller apps.

## Overview

Four stages: image basics, Compose services, a Kubernetes sample app, then multi-service todo applications with CI.

## Stack

- Docker, Docker Compose, Kubernetes
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
├── k8s/
│   └── quote-app/
└── projects/
    ├── todo-app/
    └── todo-production/
```

## Run

```bash
cd docker/projects/todo-app
docker compose up -d
```

```bash
cd docker/k8s/quote-app
docker compose -f compose.yaml up --build
```

Open any lab README for build and access details.
