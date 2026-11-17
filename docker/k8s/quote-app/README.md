# Quote App

Fastify quote app with PostgreSQL, Docker Compose, and Kubernetes manifests.

## Overview

Containerized Node service that serves and stores quotes. Run locally with Compose or deploy the manifests under `k8s/`.

## Features

- Fastify + Handlebars UI
- PostgreSQL persistence
- Compose stack (app + db)
- Sample Kubernetes deployment, service, PVC, ConfigMap

## Stack

- Node.js, Fastify, Handlebars
- PostgreSQL 16
- Docker Compose, Kubernetes

## Layout

```
quote-app/
├── app/
├── db/
├── k8s/
├── tests/
├── Dockerfile
└── compose.yaml
```

## Run

```bash
cd docker/k8s/quote-app
docker compose -f compose.yaml up --build
```

App: `http://localhost:3232`. Apply manifests in `k8s/` against a local cluster when needed.
