# File Renamer

Normalize music filenames and tags; optional OpenAI artist/title correction.

## Overview

CLI and interactive tool that rewrites titles to `Artist - Title ft. Featuring.ext`, updates tags, and can remove duplicates. Package name is `music_formatter`.

## Features

- Filename and tag normalization
- Windows explorer properties when available
- Duplicate detection
- Optional `--ai` enrichment
- Optional local artist covers from `images/`
- Dry-run and apply modes

## Stack

- Python 3.10+
- mutagen, openai, python-dotenv
- Optional pywin32

## Layout

```
file-renamer/
├── main.py
├── requirements.txt
├── .env.example
└── music_formatter/
```

## Run

```bash
cd python/applications/utilities/file-renamer
pip install -r requirements.txt
copy .env.example .env
python main.py
python main.py --path D:/ --verbose --ai
python main.py --path D:/ --apply --ai --yes
```
