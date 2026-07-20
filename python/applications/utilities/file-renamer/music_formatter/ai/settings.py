"""Chargement de la configuration IA / OpenAI depuis .env."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from music_formatter.constants import PROJECT_ROOT

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

# Valeurs internes (pas exposées dans .env)
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_BATCH_SIZE = 15
DEFAULT_MIN_CONFIDENCE = 0.55


@dataclass(frozen=True)
class AISettings:
    api_key: str
    model: str = DEFAULT_MODEL
    base_url: str = ""
    batch_size: int = DEFAULT_BATCH_SIZE
    min_confidence: float = DEFAULT_MIN_CONFIDENCE

    @property
    def is_configured(self) -> bool:
        return bool(
            self.api_key
            and self.api_key.strip()
            and not self.api_key.startswith("sk-votre")
        )


def load_ai_settings(env_path: Path | None = None) -> AISettings:
    """Charge OPENAI_API_KEY / OPENAI_MODEL depuis .env."""
    path = env_path or (PROJECT_ROOT / ".env")
    if load_dotenv is not None and path.exists():
        load_dotenv(path, override=False)
    elif load_dotenv is not None:
        load_dotenv(override=False)

    return AISettings(
        api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        model=os.getenv("OPENAI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
    )
