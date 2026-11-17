# Sass Compilation

Node container that compiles SCSS to CSS.

## Overview

Frontend workflow lab: install npm deps in the image and compile styles from mounted sources.

## Features

- Node Alpine image
- `sass-compile` / watch scripts
- Sample HTML + SCSS structure

## Stack

- Docker
- Node.js
- Sass

## Layout

```
02-sass-compilation/
├── css/
├── scss/
├── index.html
├── package.json
├── Dockerfile
└── README.md
```

## Run

```bash
cd docker/basics/sass-compilation
docker build -t sass-compile .
docker run --rm -v "${PWD}:/app" sass-compile
```
