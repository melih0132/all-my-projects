"""Nettoyage des noms de fichiers."""
from pathlib import Path

from music_formatter.constants import (
    INVALID_FILENAME_CHARS,
    MAX_FILENAME_LENGTH,
    MAX_PATH_LENGTH,
)


class FilenameSanitizer:
    """Nettoyage et validation des noms de fichiers."""

    @staticmethod
    def sanitize(filename: str) -> str:
        for char in INVALID_FILENAME_CHARS:
            filename = filename.replace(char, '_')
        filename = filename.rstrip('. ')
        if len(filename) > MAX_FILENAME_LENGTH:
            filename = filename[:MAX_FILENAME_LENGTH]
        return filename

    @staticmethod
    def is_path_too_long(file_path: Path) -> bool:
        return len(str(file_path.absolute())) > MAX_PATH_LENGTH

    @staticmethod
    def has_invalid_chars(filename: str) -> bool:
        return any(char in filename for char in INVALID_FILENAME_CHARS)
