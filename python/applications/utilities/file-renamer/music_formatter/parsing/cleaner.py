"""Nettoyage des titres."""
from music_formatter.parsing.patterns import PatternCompiler


class TitleCleaner:
    """Nettoyage des titres."""

    def __init__(self, patterns: PatternCompiler):
        self.patterns = patterns

    def clean(self, title: str) -> str:
        if not title:
            return ""
        cleaned = title.strip()
        if not cleaned:
            return ""
        cleaned = self.patterns.track_number_pattern.sub('', cleaned).strip()
        if not cleaned:
            return ""
        for pattern in self.patterns.cleanup_patterns:
            cleaned = pattern.sub('', cleaned)
            if not cleaned:
                return ""
        cleaned = self.patterns.multiple_spaces_pattern.sub(' ', cleaned).strip()
        cleaned = self.patterns.multiple_separators_pattern.sub(' ', cleaned)
        return cleaned
