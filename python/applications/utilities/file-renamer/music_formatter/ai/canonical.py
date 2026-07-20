"""Table de noms officiels (artistes / albums) via OpenAI."""
from __future__ import annotations

import json
import re
from typing import Dict, List, Optional, Sequence, Set, Tuple

from music_formatter.ai.settings import AISettings, load_ai_settings
from music_formatter.logging_setup import get_logger
from music_formatter.models import FileUpdateResult, ParsedTitle
from music_formatter.parsing.casing import identity_key

logger = get_logger("ai.canonical")

CANONICAL_SYSTEM_PROMPT = """Tu es un expert des noms d'artistes et d'albums musicaux (rap FR, pop turque, international).
On te donne une liste de variantes observées dans une bibliothèque locale.

Pour chaque variante, renvoie le nom OFFICIEL / canonique (orthographe et casse exactes utilisées par l'artiste / le label).

Règles strictes:
- Conserve les marques en majuscules si c'est officiel: GIMS (pas Gims), MØ, ASAP Rocky / A$AP Rocky selon l'usage officiel.
- Conserve les caractères turcs: İbrahim Tatlıses, Gülşen, Özdemir Erdoğan.
- Unifie les variantes d'un même artiste vers UNE seule forme (ex. Gims / GIMS / gims → GIMS).
- Ne fusionne PAS des artistes différents (Gims ≠ Jul).
- Si inconnu, garde la forme la plus propre observée et confidence basse.
- Réponds UNIQUEMENT en JSON valide.
"""


class CanonicalNameResolver:
    """Construit et applique une table variante → nom officiel."""

    def __init__(self, settings: Optional[AISettings] = None):
        self.settings = settings or load_ai_settings()
        self._client = None
        self.artist_map: Dict[str, str] = {}
        self.album_map: Dict[str, str] = {}

    def ensure_ready(self) -> None:
        if not self.settings.is_configured:
            raise RuntimeError(
                "OPENAI_API_KEY manquante ou invalide. "
                "Renseigne-la dans le fichier .env à la racine du projet."
            )
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError(
                "Paquet openai requis: py -m pip install -r requirements.txt"
            ) from e

        kwargs = {"api_key": self.settings.api_key}
        if self.settings.base_url:
            kwargs["base_url"] = self.settings.base_url
        self._client = OpenAI(**kwargs)

    def build_and_apply(
        self,
        results: List[FileUpdateResult],
    ) -> List[FileUpdateResult]:
        """Extrait les noms, demande la table IA, applique à tous les résultats."""
        if not results:
            return results

        artists, albums = self._collect_names(results)
        if not artists and not albums:
            return results

        self.ensure_ready()
        self.artist_map = self._resolve_kind("artist", sorted(artists))
        self.album_map = self._resolve_kind("album", sorted(albums))

        logger.info(
            f"Table canonique: {len(self.artist_map)} artiste(s), "
            f"{len(self.album_map)} album(s)"
        )
        for key, value in sorted(self.artist_map.items(), key=lambda x: x[1].casefold()):
            if key != identity_key(value):
                logger.info(f"Canon artiste: {key!r} -> {value!r}")
            else:
                # même clé: log seulement si casse différente des variants courants
                pass

        applied = 0
        updated: List[FileUpdateResult] = []
        for result in results:
            new_parsed, changed = self._apply_maps(result.parsed)
            if changed:
                new_result = result.with_parsed(new_parsed)
                new_result.ai_corrected = True
                updated.append(new_result)
                applied += 1
            else:
                updated.append(result)

        logger.info(f"Table canonique appliquée à {applied}/{len(results)} fichier(s)")
        return updated

    def as_aliases(self) -> Dict[str, str]:
        """Aliases pour ArtistHarmonizer (clé identity → forme officielle)."""
        aliases: Dict[str, str] = {}
        for key, value in self.artist_map.items():
            aliases[key] = value
        for key, value in self.album_map.items():
            aliases[key] = value
        return aliases

    @staticmethod
    def _collect_names(
        results: Sequence[FileUpdateResult],
    ) -> Tuple[Set[str], Set[str]]:
        artists: Set[str] = set()
        albums: Set[str] = set()
        for result in results:
            for name in result.parsed.primary_artists:
                if name and name.strip():
                    artists.add(name.strip())
            for name in result.parsed.featured_artists:
                if name and name.strip():
                    artists.add(name.strip())
            if result.parsed.album and result.parsed.album.strip():
                album = result.parsed.album.strip()
                if album.casefold() != "singles":
                    albums.add(album)
        return artists, albums

    def _resolve_kind(self, kind: str, names: List[str]) -> Dict[str, str]:
        """kind = artist|album → map identity_key → forme officielle."""
        if not names:
            return {}

        mapping: Dict[str, str] = {}
        batch_size = max(20, self.settings.batch_size * 2)

        for start in range(0, len(names), batch_size):
            batch = names[start : start + batch_size]
            partial = self._ask_canonical_batch(kind, batch)
            mapping.update(partial)

        # Garantit une entrée pour chaque nom observé
        for name in names:
            key = identity_key(name)
            if key and key not in mapping:
                mapping[key] = name
        return mapping

    def _ask_canonical_batch(self, kind: str, names: List[str]) -> Dict[str, str]:
        label = "artistes" if kind == "artist" else "albums"
        user_content = (
            f"Voici des noms d'{label} observés. "
            "Renvoie un JSON "
            '{"items":[{"variant":"...","canonical":"...","confidence":0.0}]}\n\n'
            + json.dumps({"kind": kind, "names": names}, ensure_ascii=False, indent=2)
        )

        assert self._client is not None
        try:
            response = self._client.chat.completions.create(
                model=self.settings.model,
                temperature=0.0,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": CANONICAL_SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
            )
            raw = response.choices[0].message.content or "{}"
            return self._parse_canonical_response(raw, names)
        except Exception as e:
            logger.error(f"Appel OpenAI (table canonique {kind}) échoué: {e}", exc_info=True)
            return {identity_key(n): n for n in names if n}

    def _parse_canonical_response(
        self,
        raw: str,
        fallback_names: List[str],
    ) -> Dict[str, str]:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", raw)
            if not match:
                logger.error("Réponse table canonique non JSON")
                return {identity_key(n): n for n in fallback_names}
            data = json.loads(match.group(0))

        items = data.get("items") if isinstance(data, dict) else data
        if not isinstance(items, list):
            logger.error("Schéma table canonique invalide")
            return {identity_key(n): n for n in fallback_names}

        mapping: Dict[str, str] = {}
        for item in items:
            if not isinstance(item, dict):
                continue
            variant = str(item.get("variant") or "").strip()
            canonical = str(item.get("canonical") or "").strip()
            if not variant or not canonical:
                continue
            try:
                conf = float(item.get("confidence", 1.0) or 0)
            except (TypeError, ValueError):
                conf = 0.0
            if conf < 0.4:
                continue
            mapping[identity_key(variant)] = canonical
            mapping[identity_key(canonical)] = canonical

        return mapping

    def _apply_maps(self, parsed: ParsedTitle) -> Tuple[ParsedTitle, bool]:
        def map_artist(name: str) -> str:
            key = identity_key(name)
            return self.artist_map.get(key, name)

        primary = tuple(map_artist(a) for a in parsed.primary_artists if a)
        featured = tuple(map_artist(a) for a in parsed.featured_artists if a)
        primary_keys = {identity_key(a) for a in primary}
        featured = tuple(a for a in featured if identity_key(a) not in primary_keys)

        album = parsed.album
        if album:
            album = self.album_map.get(identity_key(album), album)

        changed = (
            primary != parsed.primary_artists
            or featured != parsed.featured_artists
            or album != parsed.album
        )
        if not changed:
            return parsed, False

        return (
            ParsedTitle(
                primary,
                parsed.song_title,
                featured,
                parsed.original_title,
                album,
            ),
            True,
        )
