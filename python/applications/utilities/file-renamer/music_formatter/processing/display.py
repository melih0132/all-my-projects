"""Affichage console des resultats."""
from __future__ import annotations

import sys
from typing import Dict, List

from music_formatter.constants import PREVIEW_SAMPLE_SIZE
from music_formatter.models import FileUpdateResult


def _safe_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        payload = (text + "\n").encode(encoding, errors="replace")
        sys.stdout.buffer.write(payload)


class ResultDisplay:
    """Affichage des résultats et rapports."""

    @staticmethod
    def display_file_result(result: FileUpdateResult, dry_run: bool) -> None:
        _safe_print(f"\nAnalyse : {result.original_name}")
        _safe_print(f"   Titre formaté : '{result.parsed.format_title()}'")
        _safe_print(f"   Tag title     : '{result.tag_title}'")
        _safe_print(f"   Tag artist    : '{result.tag_artist}'")
        _safe_print(f"   Tag album     : '{result.tag_album}'")
        _safe_print(f"   Description   : '{result.tag_description}'")
        if result.ai_corrected:
            _safe_print(
                f"   IA            : oui (confidence={result.ai_confidence:.2f})"
            )
            if result.ai_notes:
                _safe_print(f"   IA notes      : {result.ai_notes}")

        if result.is_duplicate:
            if dry_run:
                _safe_print(
                    f"   DOUBLON       : à supprimer "
                    f"(même son que '{result.duplicate_of}')"
                )
            elif result.deleted:
                _safe_print(
                    f"   DOUBLON       : supprimé "
                    f"(même son que '{result.duplicate_of}')"
                )
            else:
                _safe_print(
                    f"   DOUBLON       : suppression échouée "
                    f"(même son que '{result.duplicate_of}')"
                )
                for err in result.errors:
                    _safe_print(f"   ERREUR [{err.stage}] : {err.message}")
            return

        if result.needs_rename:
            _safe_print("   CHANGEMENT DE NOM")
            _safe_print(f"   Original : {result.original_name}")
            _safe_print(f"   Nouveau  : {result.new_filename}")
        else:
            _safe_print("   Nom inchangé")

        if not dry_run:
            _safe_print(
                f"   Tags : {'OK' if result.tags_written else 'NON'} | "
                f"Cover : {'OK' if result.cover_written else 'NON'} | "
                f"Props : {'OK' if result.props_written else 'NON'} | "
                f"Rename : {'OK' if result.renamed else ('N/A' if not result.needs_rename else 'NON')}"
            )
            for err in result.errors:
                _safe_print(f"   ERREUR [{err.stage}] : {err.message}")

    @staticmethod
    def display_preview(
        results: List[FileUpdateResult],
        sample_size: int = PREVIEW_SAMPLE_SIZE,
    ) -> None:
        _safe_print(
            f"\n=== APERÇU ({min(sample_size, len(results))} / {len(results)}) ==="
        )
        for result in results[:sample_size]:
            ResultDisplay.display_file_result(result, dry_run=True)
        if len(results) > sample_size:
            _safe_print(f"\n... et {len(results) - sample_size} autre(s) fichier(s).")

    @staticmethod
    def display_stats(stats: Dict, dry_run: bool) -> None:
        _safe_print("\n=== STATISTIQUES ===")
        _safe_print(f"Fichiers trouvés : {stats['total']}")
        _safe_print(f"Fichiers traités : {stats['processed']}")
        mode = "à écrire" if dry_run else "écrits"
        _safe_print(f"Tags {mode} : {stats.get('tags_written', 0)}")
        _safe_print(f"Propriétés Windows {mode} : {stats.get('props_written', 0)}")
        if stats.get("covers_written") is not None:
            _safe_print(f"Images artistes {mode} : {stats.get('covers_written', 0)}")
        if stats.get("ai_corrected") is not None:
            _safe_print(f"Corrections IA : {stats.get('ai_corrected', 0)}")
        if stats.get("duplicates"):
            label = "à supprimer" if dry_run else "supprimés"
            count = stats.get("duplicates_deleted", stats.get("duplicates", 0))
            _safe_print(f"Doublons {label} : {count}")
        _safe_print(
            f"Fichiers {'à renommer' if dry_run else 'renommés'} : "
            f"{stats.get('renamed', 0)}"
        )
        _safe_print(f"Erreurs : {stats.get('errors', 0)}")
        if dry_run:
            _safe_print(
                "SIMULATION : fichiers, tags et doublons inchangés sur le disque."
            )

        if "formatter_stats" in stats:
            fmt_stats = stats["formatter_stats"]
            _safe_print(f"Cache hits : {fmt_stats['cache_hits']}")
            _safe_print(f"Erreurs de formatage : {fmt_stats['errors']}")

        error_list = stats.get("error_details") or []
        if error_list:
            _safe_print("\n=== DÉTAIL DES ERREURS ===")
            for err in error_list:
                _safe_print(
                    f"  [{err['stage']}] {err['file']} : {err['message']}"
                )
