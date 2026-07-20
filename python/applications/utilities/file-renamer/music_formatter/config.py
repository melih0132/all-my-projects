"""Chargement de la configuration JSON."""
from __future__ import annotations

import json
import logging
import os
from typing import Dict, Optional

from music_formatter.constants import DEFAULT_CONFIG


class ConfigLoader:
    """Chargement de la configuration JSON."""

    @staticmethod
    def load(config_file: Optional[str]) -> Dict:
        config = DEFAULT_CONFIG.copy()

        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    if isinstance(loaded_config, dict):
                        config.update(loaded_config)
                    else:
                        logging.warning(
                            "Format de configuration invalide. Config par défaut."
                        )
            except (json.JSONDecodeError, IOError) as e:
                logging.warning(
                    f"Erreur chargement config : {e}. Config par défaut."
                )

        return config
