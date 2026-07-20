"""Enrichissement métadonnées via OpenAI."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence

from music_formatter.ai.settings import AISettings, load_ai_settings
from music_formatter.logging_setup import get_logger
from music_formatter.models import FileUpdateResult, ParsedTitle

logger = get_logger("ai")

SYSTEM_PROMPT = """Tu es un expert musical. On te donne des noms de fichiers audio (souvent sales, YouTube, fautes, mauvaises casses, turc/français/anglais).
Pour chaque entrée, restitue les métadonnées correctes et canoniques.

Règles:
- primary_artists: artistes principaux (liste ordonnée). Vide si inconnu.
- featured_artists: featuring uniquement (feat./ft.), pas les co-artistes principaux.
- song_title: titre du morceau SANS artiste ni feat. ni (Official Video) etc.
- album: album connu si fiable, sinon null (ne pas inventer).
- confidence: 0.0 à 1.0 (fiabilité de ton identification).
- notes: courte justification optionnelle.
- Conserve l'orthographe et la casse officielles (ex. GIMS pas Gims, Özdemir Erdoğan, caractères turcs).
- Ne renomme pas au hasard: si tu ne reconnais pas, garde une version nettoyée et baisse confidence.
- Réponds UNIQUEMENT en JSON valide selon le schéma demandé.
"""


@dataclass
class AISuggestion:
    id: str
    primary_artists: List[str]
    featured_artists: List[str]
    song_title: str
    album: Optional[str]
    confidence: float
    notes: str = ""


class OpenAIMetadataEnricher:
    """Corrige artiste / titre / album via l'API OpenAI."""

    def __init__(self, settings: Optional[AISettings] = None):
        self.settings = settings or load_ai_settings()
        self._client = None

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

        kwargs: Dict[str, Any] = {"api_key": self.settings.api_key}
        if self.settings.base_url:
            kwargs["base_url"] = self.settings.base_url
        self._client = OpenAI(**kwargs)

    def enrich_results(
        self,
        results: List[FileUpdateResult],
        normalize_fn,
        min_confidence: Optional[float] = None,
    ) -> List[FileUpdateResult]:
        """Applique les suggestions IA aux résultats planifiés."""
        if not results:
            return results

        self.ensure_ready()
        threshold = (
            self.settings.min_confidence
            if min_confidence is None
            else min_confidence
        )
        batch_size = self.settings.batch_size
        updated: List[FileUpdateResult] = []
        corrected = 0

        for start in range(0, len(results), batch_size):
            batch = results[start : start + batch_size]
            suggestions = self._suggest_batch(batch)
            by_id = {s.id: s for s in suggestions}

            for result in batch:
                suggestion = by_id.get(result.original_name) or by_id.get(
                    str(result.file_path)
                )
                if not suggestion or suggestion.confidence < threshold:
                    updated.append(result)
                    continue

                new_parsed = self._apply_suggestion(
                    result.parsed, suggestion, normalize_fn
                )
                new_result = result.with_parsed(new_parsed)
                new_result.ai_corrected = True
                new_result.ai_confidence = suggestion.confidence
                new_result.ai_notes = suggestion.notes
                updated.append(new_result)
                corrected += 1
                logger.info(
                    f"IA corrigé: {result.original_name} -> "
                    f"{new_parsed.format_title()} "
                    f"(confidence={suggestion.confidence:.2f})"
                )

        logger.info(f"IA: {corrected}/{len(results)} fichier(s) corrigé(s)")
        return updated

    def _apply_suggestion(
        self,
        parsed: ParsedTitle,
        suggestion: AISuggestion,
        normalize_fn,
    ) -> ParsedTitle:
        # Artistes / albums: casse officielle IA préservée (pas de title-case).
        primary = tuple(
            str(a).strip() for a in suggestion.primary_artists if a and str(a).strip()
        )
        featured = tuple(
            str(a).strip() for a in suggestion.featured_artists if a and str(a).strip()
        )
        primary_keys = {a.casefold() for a in primary}
        featured = tuple(a for a in featured if a.casefold() not in primary_keys)

        title = normalize_fn(suggestion.song_title) if suggestion.song_title else parsed.song_title
        album = parsed.album
        if suggestion.album and str(suggestion.album).strip():
            album = str(suggestion.album).strip()

        return ParsedTitle(
            primary,
            title or parsed.song_title,
            featured,
            parsed.original_title,
            album,
        )

    def _suggest_batch(self, batch: Sequence[FileUpdateResult]) -> List[AISuggestion]:
        payload = []
        for item in batch:
            payload.append(
                {
                    "id": item.original_name,
                    "filename": item.original_name,
                    "stem": item.file_path.stem,
                    "parsed_artist": item.tag_artist,
                    "parsed_title": item.tag_title,
                    "parsed_album": item.tag_album,
                }
            )

        user_content = (
            "Corrige ces fichiers audio. Renvoie un JSON "
            '{"items":[{"id":"...","primary_artists":[],"featured_artists":[],'
            '"song_title":"...","album":null,"confidence":0.0,"notes":""}]}\n\n'
            + json.dumps(payload, ensure_ascii=False, indent=2)
        )

        assert self._client is not None
        try:
            response = self._client.chat.completions.create(
                model=self.settings.model,
                temperature=0.1,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
            )
            raw = response.choices[0].message.content or "{}"
            return self._parse_response(raw)
        except Exception as e:
            logger.error(f"Appel OpenAI échoué: {e}", exc_info=True)
            return []

    def _parse_response(self, raw: str) -> List[AISuggestion]:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", raw)
            if not match:
                logger.error("Réponse IA non JSON")
                return []
            data = json.loads(match.group(0))

        items = data.get("items") if isinstance(data, dict) else data
        if not isinstance(items, list):
            logger.error("Schéma IA invalide: pas de liste items")
            return []

        suggestions: List[AISuggestion] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            try:
                conf = float(item.get("confidence", 0) or 0)
            except (TypeError, ValueError):
                conf = 0.0
            primary = item.get("primary_artists") or []
            featured = item.get("featured_artists") or []
            if isinstance(primary, str):
                primary = [primary]
            if isinstance(featured, str):
                featured = [featured]
            suggestions.append(
                AISuggestion(
                    id=str(item.get("id") or ""),
                    primary_artists=[str(x).strip() for x in primary if str(x).strip()],
                    featured_artists=[str(x).strip() for x in featured if str(x).strip()],
                    song_title=str(item.get("song_title") or "").strip(),
                    album=(
                        str(item.get("album")).strip()
                        if item.get("album") not in (None, "", "null")
                        else None
                    ),
                    confidence=max(0.0, min(1.0, conf)),
                    notes=str(item.get("notes") or "").strip(),
                )
            )
        return suggestions
