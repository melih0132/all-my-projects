"""Compilation des patterns regex."""
from __future__ import annotations

import re
from typing import Dict


class PatternCompiler:
    """Compile et gère les patterns regex."""

    def __init__(self, config: Dict):
        self.config = config
        self._compile_all()

    def _compile_all(self) -> None:
        self.cleanup_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.config['cleanup_patterns']
        ]
        self.feat_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.config['feat_patterns']
        ]
        all_separators = '|'.join(self.config['artist_separators'])
        self.combined_artist_separator = re.compile(all_separators)
        self.track_number_pattern = re.compile(r'^\d{1,3}(?:\s*[-.–]\s*|\s+)')
        self.multiple_spaces_pattern = re.compile(r'\s+')
        self.multiple_separators_pattern = re.compile(r'[_\-]{2,}')
        self.music_extensions = frozenset(self.config['music_extensions'])
        self.title_case_exceptions = frozenset(self.config['title_case_exceptions'])
        self.artist_aliases = dict(self.config.get('artist_aliases') or {})
        self.artist_fuzzy_distance = int(self.config.get('artist_fuzzy_distance', 1))
        self.artist_fuzzy_min_length = int(self.config.get('artist_fuzzy_min_length', 5))
