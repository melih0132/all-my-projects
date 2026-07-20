"""Point d entree CLI."""
from __future__ import annotations

import argparse
import sys
from typing import List

from music_formatter.cli.args import create_argument_parser, create_sample_config
from music_formatter.cli.interactive import run_interactive
from music_formatter.constants import DEFAULT_MUSIC_PATH
from music_formatter.logging_setup import get_logger, setup_logging
from music_formatter.processing.processor import MusicFileProcessor


def display_startup_info(args: argparse.Namespace, dry_run: bool, folder_path: str) -> None:
    print("=== REFORMATEUR DE TITRES MUSICAUX ===")
    print(f"Dossier : {folder_path}")
    if dry_run:
        print("Mode : SIMULATION (aucune écriture, aucun renommage, aucune suppression)")
    else:
        print("Mode : APPLICATION (tags + propriétés + renommage + suppression doublons)")
    print(f"Recursif : {'OUI' if args.recursive else 'NON'}")
    print(f"Parallele : {'OUI' if args.parallel else 'NON'}")
    print(f"IA : {'OUI' if getattr(args, 'ai', False) else 'NON'}")
    if args.parallel:
        print(f"Workers : {args.workers}")
    if args.config:
        print(f"Config : {args.config}")
    print()


def _confirm_apply(folder_path: str, yes: bool) -> bool:
    if yes:
        return True
    print(f"Écriture réelle sur : {folder_path}")
    print("Cela modifie les tags, renomme les fichiers et SUPPRIME les doublons.")
    raw = input("Confirmer ? [o/N] ").strip().lower()
    return raw in ("o", "oui", "y", "yes")


def should_run_interactive(argv: List[str]) -> bool:
    """Interactif si aucun argument CLI."""
    return len(argv) <= 1


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    setup_logging()
    logger = get_logger("cli")
    parser = create_argument_parser()

    if should_run_interactive(sys.argv):
        args = parser.parse_args([])
        try:
            run_interactive(args)
        except KeyboardInterrupt:
            print("\nInterruption par l'utilisateur.")
            sys.exit(130)
        except (FileNotFoundError, NotADirectoryError) as e:
            print(f"Erreur : {e}")
            sys.exit(1)
        except ImportError as e:
            print(f"Erreur : {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Erreur inattendue : {e}")
            logger.exception("Erreur detaillee")
            sys.exit(1)
        return

    args = parser.parse_args()

    if args.create_config:
        create_sample_config()
        return

    folder_path = args.path if args.path else DEFAULT_MUSIC_PATH
    if args.apply and args.verbose:
        print("Erreur : --apply et --verbose sont incompatibles.")
        sys.exit(2)
    # Défaut = application. --verbose seul = simulation (rien n'est écrit).
    dry_run = bool(args.verbose) and not bool(args.apply)

    display_startup_info(args, dry_run, folder_path)

    try:
        from music_formatter.ai.settings import load_ai_settings
        ai_settings = load_ai_settings()
        use_ai = bool(args.ai)
        if use_ai and not ai_settings.is_configured:
            print("Erreur : --ai demandé mais OPENAI_API_KEY absente dans .env")
            sys.exit(2)

        if not dry_run and not _confirm_apply(folder_path, bool(args.yes)):
            print("Annulé.")
            sys.exit(0)

        processor = MusicFileProcessor(args.config, args.workers, use_ai=use_ai)

        if args.backup:
            processor.create_backup_list(
                folder_path, recursive=args.recursive
            )

        stats = processor.process_folder(
            folder_path,
            dry_run=dry_run,
            recursive=args.recursive,
            parallel=args.parallel,
            show_preview=dry_run,
        )
        processor.display.display_stats(stats, dry_run)
        if dry_run:
            print(
                "\nAucune modification effectuée (simulation). "
                "Relance sans --verbose pour écrire réellement, "
                "ou avec --yes pour sauter la confirmation."
            )

    except KeyboardInterrupt:
        print("\nInterruption par l'utilisateur.")
        sys.exit(130)
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Erreur : {e}")
        sys.exit(1)
    except ImportError as e:
        print(f"Erreur : {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        logger.exception("Erreur detaillee")
        sys.exit(1)
