# File Renamer

Reformats music file titles: audio tags, Windows explorer properties, renaming, and duplicate removal. Optional OpenAI correction for artist and title.

## Features

- Normalize filenames to `Artiste - Titre ft. Featuring.ext`
- Read and write audio tags (mutagen)
- Update Windows explorer properties when available
- Detect and remove duplicates
- Optional OpenAI correction (`--ai`)
- Optional local artist cover embedding from `images/`
- Interactive mode or CLI flags (dry-run, apply, recursive, parallel workers)

## Technical Concepts

- Package layout (`music_formatter`) with CLI, parsing, I/O, and processing modules
- Audio metadata handling
- Filename parsing and harmonization
- Optional external API enrichment
- Parallel file processing
- Environment-based configuration (`.env`)

## Installation

1. Ensure Python 3.10+ is installed
2. Navigate to this directory and install dependencies:

```bash
cd python/applications/utilities/file-renamer
pip install -r requirements.txt
copy .env.example .env
```

3. Set `OPENAI_API_KEY` in `.env` only if you use `--ai`

## Usage

```bash
python main.py
# Interactive mode

python main.py --path D:/ --verbose --ai
# Dry-run with OpenAI correction

python main.py --path D:/ --apply --ai --yes
# Apply changes without confirmation

python -m music_formatter --create-config
# Create music_formatter_config.json
```

### Options

| Option | Effect |
|--------|--------|
| `--path` | Target folder (interactive default: `D:\`) |
| `--verbose`, `-v` | Dry-run only |
| `--apply` | Write changes |
| `--yes`, `-y` | Skip confirmation |
| `--recursive`, `-r` | Include subfolders |
| `--ai` | OpenAI artist/title correction |
| `--config` | Custom JSON config |
| `--no-parallel` | Disable parallelism |
| `--workers N` | Worker count (default: 4) |
| `--backup` | Backup names/tags before processing |
| `--create-config` | Generate sample config |

Artist covers: if `images/` contains `Artist_Name.jpg` / `.png`, matching covers are embedded during processing. That folder is not versioned.

## Project Structure

```
file-renamer/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── logs/
├── images/
└── music_formatter/
    ├── cli/
    ├── ai/
    ├── io/
    ├── parsing/
    └── processing/
```

## Requirements

- Python 3.10+
- `mutagen`: audio tags
- `openai`: AI correction
- `python-dotenv`: `.env` loading
- Windows recommended for explorer properties (`pywin32` optional; mutagen alone covers tags)
