"""Resolution du titre album."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, Optional


class AlbumResolver:
    """Détermine le titre d'album (dossier parent ou tag existant)."""

    DRIVE_ROOT_NAMES = frozenset(
        {"$recycle.bin", "system volume information", "windows"}
    )
    JUNK_ALBUM_PATTERNS = (
        re.compile(r"\s*\((?:lyrics?|paroles?|official|audio|video)[^)]*\)", re.I),
        re.compile(r"\s*\[(?:lyrics?|paroles?|official|audio|video)[^\]]*\]", re.I),
        re.compile(r"\s*/\s*(?:lyrics?|paroles?)\s*", re.I),
    )

    def __init__(self, normalize_fn: Callable[[str], str]):
        self.normalize_fn = normalize_fn

    def resolve(
        self,
        file_path: Path,
        existing_album: Optional[str] = None,
    ) -> str:
        if existing_album and existing_album.strip():
            cleaned = self._clean_album_text(existing_album.strip())
            if cleaned:
                return cleaned

        parent = file_path.parent
        try:
            resolved = parent.resolve()
            if resolved == Path(resolved.anchor) or len(parent.parts) <= 1:
                return "Singles"
        except Exception:
            pass

        name = parent.name.strip()
        if not name or name.casefold() in self.DRIVE_ROOT_NAMES:
            return "Singles"
        if re.fullmatch(r"[A-Za-z]:\\?", name):
            return "Singles"

        return self._clean_album_text(name) or "Singles"

    def _clean_album_text(self, text: str) -> str:
        cleaned = text.strip()
        for pattern in self.JUNK_ALBUM_PATTERNS:
            cleaned = pattern.sub(" ", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" -_/")
        if not cleaned:
            return ""
        return self.normalize_fn(cleaned) or cleaned
