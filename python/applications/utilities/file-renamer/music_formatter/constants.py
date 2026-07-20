"""Constantes globales de l'application."""
from pathlib import Path

INVALID_FILENAME_CHARS = '<>:"/\\|?*'
MAX_FILENAME_LENGTH = 255
MAX_PATH_LENGTH = 260
DEFAULT_CACHE_SIZE = 1000
DEFAULT_WORKERS = 4
PROCESSING_TIMEOUT = 30
DEFAULT_MUSIC_PATH = r"D:\\"
PREVIEW_SAMPLE_SIZE = 15

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGS_ROOT = PROJECT_ROOT / "logs"
ARTIST_IMAGES_DIR = PROJECT_ROOT / "images"
IMAGE_EXTENSIONS = frozenset({".jpg", ".jpeg", ".png", ".webp"})

DEFAULT_CONFIG = {
    "cleanup_patterns": [
        r'\s*\(Official Audio\)',
        r'\s*\(Official Video\)',
        r'\s*\[Official Audio\]',
        r'\s*\[Official Video\]',
        r'\s*\(Official Lyrics Video\)',
        r'\s*\[Official Lyrics Video\]',
        r'\s*\(Clip Officiel\)',
        r'\s*\(Audio Officiel\)',
        r'\s*\(Lyrics?\)',
        r'\s*\[Lyrics?\]',
        r'\s*\(Paroles?\)',
        r'\s*\[Paroles?\]',
        r'\s*\(HD\)',
        r'\s*\[HD\]',
        r'\s*\(Music Video\)',
        r'\s*\[Music Video\]',
        r'\s*\(4K\)',
        r'\s*\[4K\]',
        r'\s*\(1080p?\)',
        r'\s*\[1080p?\]',
        r'\s*\(Visualizer\)',
        r'\s*\[Visualizer\]',
        r'\s*\(Remastered\)',
        r'\s*\[Remastered\]',
    ],
    "feat_patterns": [
        r'\s*\(\s*(feat\.?|featuring|ft\.?)\s+([^)]+)\)',
        r'\s*\[\s*(feat\.?|featuring|ft\.?)\s+([^\]]+)\]',
        r'\s+(feat\.?|featuring|ft\.?)\s+(.+)',
    ],
    "artist_separators": [r'\s*&\s*', r'\s*x\s*', r'\s*,\s*', r'\s*\+\s*'],
    "music_extensions": ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.opus'],
    "title_case_exceptions": [
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at',
        'to', 'for', 'of', 'with', 'by',
    ],
    "artist_aliases": {
        "gims": "GIMS",
        "maitre gims": "GIMS",
        "maître gims": "GIMS",
        "booba": "BOOBA",
        "jul": "JUL",
        "jay z": "JAY-Z",
        "jay-z": "JAY-Z",
        "sezer sargoz": "Sezer Sarıgöz",
        "sezer sarıgoz": "Sezer Sarıgöz",
        "sezer sarigoz": "Sezer Sarıgöz",
        "sezer sarıgöz": "Sezer Sarıgöz",
    },
    "artist_fuzzy_distance": 1,
    "artist_fuzzy_min_length": 5,
}
