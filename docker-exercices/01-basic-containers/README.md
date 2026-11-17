# Basic Containers

Minimal Alpine image with labels and a custom command.

## Overview

First lab: build and run a labeled container that prints a greeting.

## Features

- Alpine base image
- Maintainer / description / version labels
- Custom `CMD` output

## Stack

- Docker
- Alpine Linux

## Layout

```
01-basic-containers/
├── Dockerfile
└── README.md
```

## Run

```bash
cd docker-exercices/01-basic-containers
docker build -t basic-containers .
docker run --rm basic-containers
```
