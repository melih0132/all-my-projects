"""Reformateur de titres musicaux (package)."""

from music_formatter.processing.processor import MusicFileProcessor
from music_formatter.parsing.formatter import MusicTitleFormatter

__version__ = "2.0.0"
__all__ = ["MusicFileProcessor", "MusicTitleFormatter", "__version__"]
