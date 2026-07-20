"""Parseur de titres (syntaxe canonique)."""
from __future__ import annotations

from typing import List, Optional, Tuple

from music_formatter.models import ParsedTitle
from music_formatter.parsing.artists import ArtistExtractor
from music_formatter.parsing.cleaner import TitleCleaner


class TitleParser:
    """Parse la structure complète d'un titre selon la syntaxe canonique."""

    def __init__(self, cleaner: TitleCleaner, extractor: ArtistExtractor):
        self.cleaner = cleaner
        self.extractor = extractor

    def parse(self, title: str, album: Optional[str] = None) -> ParsedTitle:
        if not title:
            return ParsedTitle((), "", (), "", album)
        original_title = title
        cleaned = self.cleaner.clean(title)
        if not cleaned:
            return ParsedTitle((), original_title, (), original_title, album)
        if ' - ' in cleaned:
            return self._parse_with_separator(cleaned, original_title, album)
        return self._parse_simple(cleaned, original_title, album)

    def _parse_with_separator(
        self,
        cleaned: str,
        original_title: str,
        album: Optional[str],
    ) -> ParsedTitle:
        parts = cleaned.split(' - ', 1)
        artist_part = parts[0].strip()
        song_part = parts[1].strip()
        if not artist_part or not song_part:
            return self._parse_simple(cleaned, original_title, album)

        song_title, song_featured = self.extractor.extract_featured(song_part)
        primary, artist_featured = self._parse_artist_part(artist_part)
        all_featured = tuple(artist_featured + song_featured)
        # Retire des featuring les artistes déjà primary
        primary_keys = {a.casefold() for a in primary}
        all_featured = tuple(
            a for a in all_featured if a.casefold() not in primary_keys
        )

        return ParsedTitle(
            tuple(primary),
            self.extractor.normalize_name(song_title) if song_title else original_title,
            all_featured,
            original_title,
            album,
        )

    def _parse_simple(
        self,
        cleaned: str,
        original_title: str,
        album: Optional[str],
    ) -> ParsedTitle:
        song_title, featured = self.extractor.extract_featured(cleaned)
        return ParsedTitle(
            (),
            self.extractor.normalize_name(song_title) if song_title else original_title,
            tuple(featured),
            original_title,
            album,
        )

    def _parse_artist_part(self, artist_string: str) -> Tuple[List[str], List[str]]:
        """Tous les artistes avant ' - ' sont co-primaires ; feat. reste featuring."""
        if not artist_string:
            return [], []
        main_part, featured = self.extractor.extract_featured(artist_string)
        primary = self.extractor.split_artists(main_part)
        return primary, featured
