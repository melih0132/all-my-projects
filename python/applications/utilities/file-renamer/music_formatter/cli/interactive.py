"""Mode interactif."""
from __future__ import annotations

import argparse
from pathlib import Path

from music_formatter.ai.settings import load_ai_settings
from music_formatter.constants import DEFAULT_MUSIC_PATH
from music_formatter.processing.processor import MusicFileProcessor


def _prompt_yes_no(message: str, default_yes: bool) -> bool:
    suffix = " [O/n] " if default_yes else " [o/N] "
    raw = input(message + suffix).strip().lower()
    if not raw:
        return default_yes
    return raw in ('o', 'oui', 'y', 'yes')


def _normalize_path(raw: str) -> str:
    path = raw.strip().strip('"').strip("'")
    if not path:
        return DEFAULT_MUSIC_PATH
    return str(Path(path))


def run_interactive(args: argparse.Namespace) -> None:
    """Mode interactif : chemin, simulation, récursif, IA, confirmation."""
    print("=== REFORMATEUR DE TITRES MUSICAUX ===")
    print("Tags audio + propriétés Windows + renommage\n")

    raw_path = input(f"Chemin du dossier [{DEFAULT_MUSIC_PATH}] : ")
    folder_path = _normalize_path(raw_path)

    dry_run = _prompt_yes_no("Mode simulation (recommandé)", default_yes=True)

    default_recursive = Path(folder_path).resolve() == Path(DEFAULT_MUSIC_PATH).resolve()
    recursive = _prompt_yes_no(
        "Parcourir les sous-dossiers",
        default_yes=default_recursive
    )

    ai_settings = load_ai_settings()
    use_ai = bool(getattr(args, "ai", False))
    if ai_settings.is_configured:
        use_ai = _prompt_yes_no(
            "Correction IA OpenAI (artiste/titre)",
            default_yes=use_ai,
        )
    else:
        print("IA désactivée: renseigne OPENAI_API_KEY dans .env pour l'activer.")
        use_ai = False

    print(f"\nDossier : {folder_path}")
    print(f"Mode : {'SIMULATION' if dry_run else 'APPLICATION'}")
    print(f"Récursif : {'OUI' if recursive else 'NON'}")
    print(f"IA : {'OUI' if use_ai else 'NON'}\n")

    processor = MusicFileProcessor(args.config, args.workers, use_ai=use_ai)

    if args.backup:
        processor.create_backup_list(folder_path, recursive=recursive)

    if dry_run:
        stats = processor.process_folder(
            folder_path,
            dry_run=True,
            recursive=recursive,
            parallel=args.parallel,
            show_preview=True,
        )
        processor.display.display_stats(stats, dry_run=True)

        if stats['total'] == 0:
            return

        if _prompt_yes_no(
            "\nÉcrire réellement (tags + props + rename + suppression doublons)",
            default_yes=False,
        ):
            apply_stats = processor.process_folder(
                folder_path,
                dry_run=False,
                recursive=recursive,
                parallel=args.parallel,
                show_preview=False,
            )
            processor.display.display_stats(apply_stats, dry_run=False)
    else:
        if not _prompt_yes_no(
            "Confirmer l'écriture immédiate (tags + props + rename)",
            default_yes=False
        ):
            print("Annulé.")
            return
        stats = processor.process_folder(
            folder_path,
            dry_run=False,
            recursive=recursive,
            parallel=args.parallel,
            show_preview=False,
        )
        processor.display.display_stats(stats, dry_run=False)
