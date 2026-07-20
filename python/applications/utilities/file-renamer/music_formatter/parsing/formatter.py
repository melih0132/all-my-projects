"""Orchestrateur de formatage de titres."""
from __future__ import annotations

from typing import Dict, Optional

from music_formatter.cache import LRUCache
from music_formatter.config import ConfigLoader
from music_formatter.constants import DEFAULT_CACHE_SIZE
from music_formatter.logging_setup import get_logger
from music_formatter.models import ParsedTitle, ProcessingStats
from music_formatter.parsing.album import AlbumResolver
from music_formatter.parsing.artists import ArtistExtractor
from music_formatter.parsing.cleaner import TitleCleaner
from music_formatter.parsing.parser import TitleParser
from music_formatter.parsing.patterns import PatternCompiler

logger = get_logger("parsing")


class MusicTitleFormatter:
    """Formatage des titres avec cache LRU."""

    def __init__(self, config_file: Optional[str] = None):
        config = ConfigLoader.load(config_file)
        patterns = PatternCompiler(config)
        self.cleaner = TitleCleaner(patterns)
        self.extractor = ArtistExtractor(patterns)
        self.parser = TitleParser(self.cleaner, self.extractor)
        self.album_resolver = AlbumResolver(self.extractor.normalize_name)
        self.patterns = patterns
        self._format_cache = LRUCache(max_size=DEFAULT_CACHE_SIZE)
        self._parse_cache: Dict[str, ParsedTitle] = {}
        self.stats = ProcessingStats()

    def parse_title(
        self,
        title: str,
        album: Optional[str] = None,
    ) -> ParsedTitle:
        cache_key = f"{title}||{album or ''}"
        if cache_key in self._parse_cache:
            return self._parse_cache[cache_key]
        parsed = self.parser.parse(title, album=album)
        self._parse_cache[cache_key] = parsed
        return parsed

    def format_title(self, title: str) -> str:
        if not title:
            return ""
        try:
            if title in self._format_cache:
                self.stats.increment_cache_hits()
                return self._format_cache[title]
            self.stats.increment_processed()
            parsed = self.parse_title(title)
            result = parsed.format_title()
            self._format_cache[title] = result
            return result
        except (AttributeError, IndexError, KeyError) as e:
            self.stats.increment_errors()
            logger.error(f"Erreur formatage de '{title}': {e}", exc_info=True)
            return title
        except Exception as e:
            self.stats.increment_errors()
            logger.error(f"Erreur inattendue formatage de '{title}': {e}", exc_info=True)
            return title

    def get_stats(self) -> Dict:
        return self.stats.to_dict()
