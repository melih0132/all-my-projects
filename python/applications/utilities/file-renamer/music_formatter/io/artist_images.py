"""Catalogue images/artiste -> fichier image embarquable."""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from music_formatter.constants import ARTIST_IMAGES_DIR, IMAGE_EXTENSIONS
from music_formatter.parsing.casing import identity_key


@dataclass(frozen=True)
class ArtistImage:
    """Image associée à un artiste."""
    artist_name: str
    path: Path
    mime: str

    @property
    def key(self) -> str:
        return identity_key(self.artist_name)


_MIME_BY_EXT = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


def artist_name_from_image_stem(stem: str) -> str:
    """Ahmet_Kaya / Ahmet-Kaya -> Ahmet Kaya."""
    name = stem.replace("_", " ").replace("-", " ")
    name = re.sub(r"\s+", " ", name).strip()
    return name


def split_artist_field(artist: str) -> List[str]:
    """Découpe un champ artiste (A & B / A, B & C / A feat. B)."""
    if not artist:
        return []
    text = artist.strip()
    if not text:
        return []
    text = re.split(
        r"\s+(?:ft\.?|feat\.?|featuring)\s+",
        text,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]
    parts = re.split(r"\s*&\s*|\s*,\s*|\s*\+\s*|\s+x\s+", text, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p and p.strip()]


class ArtistImageCatalog:
    """Charge images/ et résout une image pour un artiste."""

    def __init__(
        self,
        images_dir: Optional[Path] = None,
        logger: Optional[logging.Logger] = None,
    ):
        self.images_dir = Path(images_dir) if images_dir else ARTIST_IMAGES_DIR
        self.logger = logger or logging.getLogger(__name__)
        self._by_key: Dict[str, ArtistImage] = {}
        self.reload()

    def reload(self) -> None:
        self._by_key.clear()
        if not self.images_dir.exists() or not self.images_dir.is_dir():
            self.logger.warning(f"Dossier images introuvable : {self.images_dir}")
            return

        for path in sorted(self.images_dir.iterdir()):
            if not path.is_file():
                continue
            ext = path.suffix.lower()
            if ext not in IMAGE_EXTENSIONS:
                continue
            mime = _MIME_BY_EXT.get(ext)
            if not mime:
                continue
            artist_name = artist_name_from_image_stem(path.stem)
            if not artist_name:
                continue
            image = ArtistImage(artist_name=artist_name, path=path, mime=mime)
            existing = self._by_key.get(image.key)
            if existing:
                self.logger.warning(
                    f"Image artiste en double pour {image.artist_name!r}: "
                    f"{existing.path.name} écrasée par {path.name}"
                )
            self._by_key[image.key] = image

        self.logger.info(
            f"Images artistes chargées : {len(self._by_key)} "
            f"depuis {self.images_dir}"
        )

    def __len__(self) -> int:
        return len(self._by_key)

    def list_artists(self) -> List[ArtistImage]:
        return sorted(self._by_key.values(), key=lambda i: i.key)

    def resolve(self, artist: str) -> Optional[ArtistImage]:
        if not artist:
            return None
        return self._by_key.get(identity_key(artist.strip()))

    def resolve_from_artists(self, artists: Iterable[str]) -> Optional[ArtistImage]:
        """Première image trouvée parmi les artistes (ordre donné)."""
        for artist in artists:
            hit = self.resolve(artist)
            if hit:
                return hit
        return None

    def resolve_for_file(
        self,
        *,
        tag_artist: str = "",
        filename_stem: str = "",
        primary_artists: Optional[Iterable[str]] = None,
    ) -> Optional[ArtistImage]:
        """Résout via primary_artists, tag artist, puis stem fichier."""
        candidates: List[str] = []
        if primary_artists:
            candidates.extend(a for a in primary_artists if a)
        if tag_artist:
            candidates.extend(split_artist_field(tag_artist))
        if filename_stem and " - " in filename_stem:
            left = filename_stem.split(" - ", 1)[0]
            candidates.extend(split_artist_field(left))

        seen = set()
        unique: List[str] = []
        for name in candidates:
            key = identity_key(name)
            if key and key not in seen:
                seen.add(key)
                unique.append(name)
        return self.resolve_from_artists(unique)

    def read_bytes(self, image: ArtistImage) -> Tuple[bytes, str]:
        data = image.path.read_bytes()
        if not data:
            raise ValueError(f"Image vide : {image.path}")
        return self._normalize_for_tags(data, image.mime)

    @staticmethod
    def _normalize_for_tags(data: bytes, mime: str) -> Tuple[bytes, str]:
        """Réencode en JPEG baseline RGB (compatible Windows Explorer)."""
        try:
            import io
            from PIL import Image

            img = Image.open(io.BytesIO(data))
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            elif img.mode == "L":
                img = img.convert("RGB")
            # Agrandit les miniatures trop petites pour l'aperçu Explorer
            w, h = img.size
            min_side = min(w, h)
            if min_side < 300:
                scale = 300 / min_side
                img = img.resize(
                    (max(1, int(w * scale)), max(1, int(h * scale))),
                    Image.Resampling.LANCZOS,
                )
            out = io.BytesIO()
            img.save(out, format="JPEG", quality=90, optimize=True, progressive=False)
            return out.getvalue(), "image/jpeg"
        except Exception:
            return data, mime
