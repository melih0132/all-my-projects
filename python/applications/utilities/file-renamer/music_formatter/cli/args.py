"""Parser argparse et config exemple."""
from __future__ import annotations

import argparse
import json

from music_formatter.constants import DEFAULT_MUSIC_PATH, DEFAULT_WORKERS


def create_sample_config() -> None:
    config = {
        "cleanup_patterns": [
            "\\s*\\(Official Audio\\)",
            "\\s*\\(Official Video\\)",
            "\\s*\\[Official Audio\\]",
            "\\s*\\[Official Video\\]"
        ],
        "feat_patterns": [
            "\\s*\\(\\s*(feat\\.?|featuring|ft\\.?)\\s+([^)]+)\\)",
            "\\s*\\[\\s*(feat\\.?|featuring|ft\\.?)\\s+([^\\]]+)\\]"
        ],
        "artist_separators": ["\\s*&\\s*", "\\s*x\\s*", "\\s*,\\s*"],
        "music_extensions": [".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg", ".wma"],
        "title_case_exceptions": [
            "a", "an", "the", "and", "or", "but", "in", "on", "at",
            "to", "for", "of", "with", "by"
        ],
        "artist_aliases": {},
        "artist_fuzzy_distance": 1,
        "artist_fuzzy_min_length": 5
    }
    try:
        with open("music_formatter_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print("Fichier de configuration créé : music_formatter_config.json")
    except IOError as e:
        print(f"Erreur création config : {e}")


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reformateur de titres musicaux (tags + propriétés Windows + renommage)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python main.py
      Mode interactif (chemin par defaut D:\\)
  python main.py --path D:/ --verbose --ai
      Simulation + correction OpenAI
  python main.py --path D:/ --apply --ai
      Applique tags/props/rename apres correction IA
  python -m music_formatter --create-config
        """
    )
    parser.add_argument(
        '--path',
        default=None,
        help=f'Dossier à traiter (défaut interactif: {DEFAULT_MUSIC_PATH})'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mode simulation uniquement (aucune écriture ni suppression)'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Force le mode application (défaut hors --verbose)'
    )
    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Sans confirmation avant écriture'
    )
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Traitement récursif des sous-dossiers'
    )
    parser.add_argument('--config', help='Fichier de configuration JSON')
    parser.add_argument(
        '--parallel',
        action='store_true',
        default=True,
        help='Analyse parallèle (par défaut)'
    )
    parser.add_argument(
        '--no-parallel',
        dest='parallel',
        action='store_false',
        help='Désactiver le traitement parallèle'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=DEFAULT_WORKERS,
        help=f'Nombre de workers (défaut: {DEFAULT_WORKERS})'
    )
    parser.add_argument(
        '--create-config',
        action='store_true',
        help="Créer un fichier de configuration d'exemple"
    )
    parser.add_argument(
        '--backup',
        action='store_true',
        help='Créer une sauvegarde des noms et tags'
    )
    parser.add_argument(
        '--ai',
        action='store_true',
        help='Active la correction artiste/titre via OpenAI (.env OPENAI_API_KEY)'
    )
    return parser
