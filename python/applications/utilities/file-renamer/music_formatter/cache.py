"""Cache LRU simple."""
from collections import OrderedDict

from music_formatter.constants import DEFAULT_CACHE_SIZE


class LRUCache:
    """Cache LRU pour les titres formatés."""

    def __init__(self, max_size: int = DEFAULT_CACHE_SIZE):
        self.max_size = max_size
        self._cache: OrderedDict = OrderedDict()

    def __contains__(self, key: str) -> bool:
        return key in self._cache

    def __getitem__(self, key: str) -> str:
        value = self._cache.pop(key)
        self._cache[key] = value
        return value

    def __setitem__(self, key: str, value: str) -> None:
        if key in self._cache:
            self._cache.pop(key)
        elif len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)
        self._cache[key] = value
