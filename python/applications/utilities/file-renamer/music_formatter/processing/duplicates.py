"""Détection et résolution des doublons (même artiste + même titre)."""
from __future__ import annotations

import re
from typing import Dict, List, Tuple

from music_formatter.logging_setup import get_logger
from music_formatter.models import FileUpdateResult, ParsedTitle
from music_formatter.parsing.casing import identity_key

logger = get_logger("duplicates")

_FEAT_SPLIT = re.compile(
    r"\s+(?:ft\.?|feat\.?|featuring)\s+",
    re.IGNORECASE,
)


def core_song_key(title: str) -> str:
    """Titre sans featuring, pour comparer les doublons."""
    if not title:
        return ""
    base = _FEAT_SPLIT.split(title, maxsplit=1)[0].strip()
    # ignore ponctuation légère
    base = re.sub(r"[^\w\s]", " ", base, flags=re.UNICODE)
    base = re.sub(r"\s+", " ", base).strip()
    return identity_key(base)


def track_fingerprint(parsed: ParsedTitle) -> str:
    """Empreinte artiste + titre de base (feat. ignoré)."""
    artist = identity_key(parsed.format_artists_clause() or "")
    title = core_song_key(parsed.song_title or parsed.format_song_title())
    if not artist and not title:
        return ""
    return f"{artist}::{title}"


def _score_result(result: FileUpdateResult) -> Tuple:
    """Préfère la version la plus complète / fiable."""
    parsed = result.parsed
    return (
        1 if result.ai_corrected else 0,
        float(result.ai_confidence or 0.0),
        len(parsed.featured_artists),
        len(parsed.primary_artists),
        len(parsed.song_title or ""),
        # préfère un nom déjà proche de la forme canonique
        0 if result.needs_rename else 1,
        -len(result.original_name),
    )


def resolve_duplicates(results: List[FileUpdateResult]) -> List[FileUpdateResult]:
    """
    Marque les doublons : un seul fichier gardé par empreinte.
    Les autres sont skippés à l'écriture (is_duplicate=True).
    """
    groups: Dict[str, List[int]] = {}
    for idx, result in enumerate(results):
        fp = track_fingerprint(result.parsed)
        if not fp:
            continue
        groups.setdefault(fp, []).append(idx)

    resolved = list(results)
    duplicate_count = 0

    for fp, indices in groups.items():
        if len(indices) < 2:
            continue

        ranked = sorted(indices, key=lambda i: _score_result(resolved[i]), reverse=True)
        winner_idx = ranked[0]
        winner = resolved[winner_idx]

        # Fusionne les featuring manquants depuis les doublons vers le gagnant
        featured = list(winner.parsed.featured_artists)
        featured_keys = {identity_key(a) for a in featured}
        for idx in ranked[1:]:
            for feat in resolved[idx].parsed.featured_artists:
                key = identity_key(feat)
                if key and key not in featured_keys:
                    featured.append(feat)
                    featured_keys.add(key)

        if tuple(featured) != winner.parsed.featured_artists:
            merged = winner.parsed.with_artists(
                winner.parsed.primary_artists,
                tuple(featured),
            )
            winner = winner.with_parsed(merged)
            resolved[winner_idx] = winner

        winner_name = winner.original_name
        for idx in ranked[1:]:
            dup = resolved[idx]
            dup.is_duplicate = True
            dup.duplicate_of = winner_name
            dup.needs_rename = False
            resolved[idx] = dup
            duplicate_count += 1
            logger.info(
                f"Doublon détecté: '{dup.original_name}' "
                f"(= même son que '{winner_name}', sera supprimé)"
            )

        logger.info(
            f"Doublon groupé [{fp}]: garde '{winner_name}', "
            f"ignore/supprime {len(ranked) - 1} copie(s)"
        )

    if duplicate_count:
        logger.info(f"Doublons: {duplicate_count} fichier(s) à supprimer")
    return resolved
