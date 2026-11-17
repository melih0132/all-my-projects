# PHP Apache MariaDB

PHP app behind Apache with MariaDB and phpMyAdmin.

## Overview

Compose lab for a classic LAMP-style trio, plus sample GitLab CI pipeline files.

## Features

- PHP Apache image with PDO MySQL
- MariaDB named volume
- phpMyAdmin UI
- GitLab CI samples (`partie-1`, `partie-2`)

## Stack

- Docker Compose
- PHP, Apache
- MariaDB, phpMyAdmin
- GitLab CI

## Layout

```
04-php-apache-mariadb/
├── index.php
├── Dockerfile
├── docker-compose.yml
├── partie-1-gitlab-ci.yml
├── partie-2-gitlab-ci.yml
└── README.md
```

## Run

```bash
cd docker/compose/php-apache-mariadb
docker compose up --build -d
```

App: http://localhost:8081  
phpMyAdmin: http://localhost:8082
