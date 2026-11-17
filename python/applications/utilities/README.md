# Python Utilities

Small scripts and the file-renamer package.

## Overview

Standalone helpers for wallpaper, tasks, a CLI game, and music filename/tag formatting.

## Stack

- Python 3
- Tkinter (task GUI)
- mutagen / openai (file-renamer)

## Layout

```
utilities/
├── app_wallpaper.py
├── gestionnaire_taches.py
├── gestionnaire_taches_app.py
├── pierre_papier_ciseaux.py
└── file-renamer/          → music_formatter package
```

## Run

```bash
python app_wallpaper.py
python gestionnaire_taches.py
python gestionnaire_taches_app.py
python pierre_papier_ciseaux.py
```

For file renaming, see `file-renamer/README.md`.
