"""Extraction et normalisation des artistes."""
from __future__ import annotations

import re
from typing import List, Tuple

from music_formatter.parsing.casing import (
    identity_key,
    is_short_acronym,
    is_stylized_allcaps,
    title_case_word,
)
from music_formatter.parsing.patterns import PatternCompiler


class ArtistExtractor:
    """Extraction et capitalisation des artistes (support turc)."""

    def __init__(self, patterns: PatternCompiler):
        self.patterns = patterns

    def extract_featured(self, title: str) -> Tuple[str, List[str]]:
        if not title:
            return "", []
        for pattern in self.patterns.feat_patterns:
            match = pattern.search(title)
            if match:
                main_title = title[:match.start()].strip()
                feat_part = match.group(2).strip()
                if feat_part:
                    return main_title, self.split_artists(feat_part)
                return main_title, []
        return title, []

    def split_artists(self, artist_string: str) -> List[str]:
        if not artist_string:
            return []
        parts = self.patterns.combined_artist_separator.split(artist_string.strip())
        artists = [part.strip() for part in parts if part.strip()]
        if not artists:
            return []
        seen = set()
        unique_artists = []
        for artist in artists:
            normalized = self.normalize_name(artist)
            key = identity_key(normalized)
            if normalized and key not in seen:
                seen.add(key)
                unique_artists.append(normalized)
        return unique_artists

    def normalize_name(self, text: str) -> str:
        """Harmonise la casse (Title Case + locale turque si besoin)."""
        if not text:
            return text
        text = text.strip()
        if not text:
            return text

        aliases = getattr(self.patterns, "artist_aliases", None) or {}
        alias_hit = aliases.get(identity_key(text))
        if alias_hit:
            return str(alias_hit).strip()

        # Acronyme / marque ALL CAPS (DJ, GIMS) — pas les mots turcs
        if (
            (is_short_acronym(text) or is_stylized_allcaps(text))
            and " " not in text
            and "-" not in text
        ):
            return text

        parts = re.split(r"(\s+)", text)
        result = []
        word_index = 0
        exceptions = set(self.patterns.title_case_exceptions)
        for part in parts:
            if not part or part.isspace():
                result.append(part)
                continue
            result.append(self._normalize_token(part, word_index == 0, exceptions))
            word_index += 1
        return "".join(result).strip()

    def _normalize_token(self, token: str, is_first: bool, exceptions: set) -> str:
        if not token:
            return token

        sub_parts = re.split(r"([-'])", token)
        out = []
        for i, sub in enumerate(sub_parts):
            if sub in ("-", "'"):
                out.append(sub)
                continue
            if not sub:
                continue
            out.append(
                title_case_word(
                    sub,
                    is_first=is_first and i == 0,
                    exceptions=exceptions,
                )
            )
        return "".join(out)

    def _capitalize(self, text: str) -> str:
        return self.normalize_name(text)
