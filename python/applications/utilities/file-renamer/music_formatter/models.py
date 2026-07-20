"""Modeles de donnees."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from music_formatter.io.sanitizer import FilenameSanitizer


@dataclass(frozen=True)
class ParsedTitle:
    """
    Structure immuable d'un titre parsé.

    Syntaxe canonique du stem (nom sans extension)
    ----------------------------------------------
    join(artistes):
      0  →  ""
      1  →  "A"
      2  →  "A & B"
      3+ →  "A, B & C"

    title_clause = titre
      + optionnel " ft. " + join(featuring)

    si primary non vide :
      stem = join(primary) + " - " + title_clause
    sinon :
      stem = title_clause

    Exemples :
      Song
      Artist - Song
      A & B - Song
      A, B & C - Song
      Artist - Song ft. Guest
      A & B - Song ft. C & D
    """
    primary_artists: Tuple[str, ...]
    song_title: str
    featured_artists: Tuple[str, ...]
    original_title: str
    album: Optional[str] = None

    @staticmethod
    def join_artists(artists: Tuple[str, ...]) -> str:
        """Jointure algorithmique 0/1/2/3+ artistes."""
        artists = tuple(a for a in artists if a and a.strip())
        n = len(artists)
        if n == 0:
            return ""
        if n == 1:
            return artists[0]
        if n == 2:
            return f"{artists[0]} & {artists[1]}"
        return ", ".join(artists[:-1]) + f" & {artists[-1]}"

    def format_artists_clause(self) -> str:
        return self.join_artists(self.primary_artists)

    def format_featured_clause(self) -> str:
        return self.join_artists(self.featured_artists)

    def format_song_title(self) -> str:
        """Titre média (avec ft. si featuring)."""
        featured = self.format_featured_clause()
        if featured:
            return f"{self.song_title} ft. {featured}"
        return self.song_title

    def format_artist(self) -> str:
        """Champ artiste (tous les primary joints)."""
        return self.format_artists_clause()

    def format_album(self) -> str:
        """Album volontairement non utilisé pour les tags (toujours vide)."""
        return ""

    def format_albumartist(self) -> str:
        return self.format_artists_clause()

    def format_description(self) -> str:
        """Description / commentaire fichier (sans album)."""
        artists = self.format_artists_clause()
        title = self.format_song_title()
        if artists:
            return f"{artists} - {title}"
        return title

    def format_title(self) -> str:
        """Nom de fichier formaté (sans extension)."""
        title_clause = self.format_song_title()
        artists = self.format_artists_clause()
        if artists:
            return f"{artists} - {title_clause}"
        return title_clause

    def with_album(self, album: Optional[str]) -> "ParsedTitle":
        return ParsedTitle(
            self.primary_artists,
            self.song_title,
            self.featured_artists,
            self.original_title,
            album,
        )

    def with_artists(
        self,
        primary: Tuple[str, ...],
        featured: Tuple[str, ...],
    ) -> "ParsedTitle":
        return ParsedTitle(
            primary,
            self.song_title,
            featured,
            self.original_title,
            self.album,
        )


@dataclass
class MediaMetadata:
    """Payload unifié tags audio + propriétés Windows."""
    title: str
    artist: str
    album: str
    albumartist: str
    description: str

    @classmethod
    def from_parsed(cls, parsed: ParsedTitle) -> "MediaMetadata":
        return cls(
            title=parsed.format_song_title(),
            artist=parsed.format_artist(),
            album="",
            albumartist=parsed.format_albumartist(),
            description=parsed.format_description(),
        )

@dataclass
class ProcessingStats:
    """Statistiques de formatage (cache)."""
    processed: int = 0
    cache_hits: int = 0
    errors: int = 0

    def increment_processed(self) -> None:
        self.processed += 1

    def increment_cache_hits(self) -> None:
        self.cache_hits += 1

    def increment_errors(self) -> None:
        self.errors += 1

    def to_dict(self) -> Dict:
        return {
            'processed': self.processed,
            'cache_hits': self.cache_hits,
            'errors': self.errors
        }


@dataclass
class StageError:
    """Erreur sur une étape d'un fichier."""
    file: str
    stage: str
    message: str

    def to_dict(self) -> Dict[str, str]:
        return {'file': self.file, 'stage': self.stage, 'message': self.message}


@dataclass
class FileUpdateResult:
    """Résultat du traitement d'un fichier."""
    file_path: Path
    original_name: str
    new_filename: str
    parsed: ParsedTitle
    needs_rename: bool
    tag_title: str
    tag_artist: str
    tag_album: str = ""
    tag_description: str = ""
    tags_written: bool = False
    props_written: bool = False
    cover_written: bool = False
    renamed: bool = False
    errors: List[StageError] = field(default_factory=list)
    ai_corrected: bool = False
    ai_confidence: float = 0.0
    ai_notes: str = ""
    is_duplicate: bool = False
    duplicate_of: str = ""
    deleted: bool = False

    @property
    def has_changes(self) -> bool:
        return (
            self.needs_rename
            or bool(self.tag_title)
            or bool(self.tag_artist)
            or bool(self.tag_album)
        )

    def with_parsed(self, parsed: ParsedTitle) -> "FileUpdateResult":
        """Recalcule nom / tags après harmonisation / IA."""
        formatted_name = parsed.format_title()
        extension = Path(self.original_name).suffix
        new_filename = FilenameSanitizer.sanitize(formatted_name) + extension
        return FileUpdateResult(
            file_path=self.file_path,
            original_name=self.original_name,
            new_filename=new_filename,
            parsed=parsed,
            needs_rename=self.file_path.name != new_filename,
            tag_title=parsed.format_song_title(),
            tag_artist=parsed.format_artist(),
            tag_album=parsed.format_album(),
            tag_description=parsed.format_description(),
            tags_written=self.tags_written,
            props_written=self.props_written,
            cover_written=self.cover_written,
            renamed=self.renamed,
            errors=list(self.errors),
            ai_corrected=self.ai_corrected,
            ai_confidence=self.ai_confidence,
            ai_notes=self.ai_notes,
            is_duplicate=self.is_duplicate,
            duplicate_of=self.duplicate_of,
            deleted=self.deleted,
        )
