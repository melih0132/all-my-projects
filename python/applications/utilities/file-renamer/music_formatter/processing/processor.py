"""Processeur principal des fichiers musicaux."""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from music_formatter.constants import DEFAULT_WORKERS, PROCESSING_TIMEOUT
from music_formatter.exceptions import (
    DeleteError,
    PropertyWriteError,
    RenameError,
    TagWriteError,
)
from music_formatter.io.artist_images import ArtistImageCatalog
from music_formatter.io.filesystem import FileSystemHandler
from music_formatter.io.metadata import AudioMetadataWriter
from music_formatter.io.sanitizer import FilenameSanitizer
from music_formatter.io.windows_props import WindowsPropertyWriter
from music_formatter.models import (
    FileUpdateResult,
    MediaMetadata,
    ParsedTitle,
    StageError,
)
from music_formatter.parsing.formatter import MusicTitleFormatter
from music_formatter.parsing.harmonizer import ArtistHarmonizer
from music_formatter.processing.display import ResultDisplay
from music_formatter.processing.duplicates import resolve_duplicates


class MusicFileProcessor:
    """Traite les fichiers musicaux : tags, propriétés Windows, renommage."""

    def __init__(
        self,
        config_file: Optional[str] = None,
        max_workers: int = DEFAULT_WORKERS,
        use_ai: bool = False,
    ):
        self.formatter = MusicTitleFormatter(config_file)
        self.max_workers = max_workers
        self.use_ai = use_ai
        from music_formatter.logging_setup import get_logger, setup_logging
        setup_logging()
        self.logger = get_logger("processor")
        self.fs_handler = FileSystemHandler(self.logger)
        self.display = ResultDisplay()
        self.metadata_writer = AudioMetadataWriter(self.logger)
        self.property_writer = WindowsPropertyWriter(self.logger)
        self.artist_images = ArtistImageCatalog(logger=self.logger)
        self.ai_enricher = None
        self.canonical_resolver = None
        if use_ai:
            from music_formatter.ai.canonical import CanonicalNameResolver
            from music_formatter.ai.enricher import OpenAIMetadataEnricher
            self.ai_enricher = OpenAIMetadataEnricher()
            self.canonical_resolver = CanonicalNameResolver()


    def plan_single_file(
        self,
        file_info: Tuple[Path, str, str]
    ) -> Optional[FileUpdateResult]:
        """Analyse un fichier sans écrire."""
        file_path, name_without_ext, extension = file_info
        try:
            existing = self.metadata_writer.read_tags(file_path)
            album = self.formatter.album_resolver.resolve(
                file_path,
                existing.get('album'),
            )
            parsed = self.formatter.parse_title(name_without_ext, album=album)
            formatted_name = parsed.format_title()
            new_filename = FilenameSanitizer.sanitize(formatted_name) + extension
            needs_rename = file_path.name != new_filename
            return FileUpdateResult(
                file_path=file_path,
                original_name=file_path.name,
                new_filename=new_filename,
                parsed=parsed,
                needs_rename=needs_rename,
                tag_title=parsed.format_song_title(),
                tag_artist=parsed.format_artist(),
                tag_album=parsed.format_album(),
                tag_description=parsed.format_description(),
            )
        except Exception as e:
            self.logger.error(
                f"Erreur analyse de {file_path}: {e}", exc_info=True
            )
            return None

    def apply_file_updates(self, result: FileUpdateResult) -> FileUpdateResult:
        """Écrit tags, propriétés Windows, puis renomme."""
        path = result.file_path
        meta = MediaMetadata.from_parsed(result.parsed)
        cover_payload = self._cover_for_parsed(result.parsed)

        try:
            self.metadata_writer.write(path, result.parsed, cover=cover_payload)
            result.tags_written = True
            if cover_payload:
                result.cover_written = True
        except TagWriteError as e:
            err = StageError(str(path), "tags", str(e))
            result.errors.append(err)
            self.logger.error(f"[tags] {path.name}: {e}")
        except Exception as e:
            err = StageError(str(path), "tags", f"Erreur inattendue : {e}")
            result.errors.append(err)
            self.logger.error(f"[tags] {path.name}: {e}", exc_info=True)

        try:
            if getattr(self.property_writer, "_enabled", False):
                self.property_writer.write(path, meta)
                result.props_written = True
        except PropertyWriteError as e:
            if result.tags_written:
                self.logger.warning(
                    f"[props] {path.name}: {e} (tags déjà écrits, ignoré comme erreur bloquante)"
                )
            else:
                err = StageError(str(path), "props", str(e))
                result.errors.append(err)
                self.logger.error(f"[props] {path.name}: {e}")
        except Exception as e:
            if result.tags_written:
                self.logger.warning(
                    f"[props] {path.name}: erreur inattendue : {e} (tags OK)"
                )
            else:
                err = StageError(str(path), "props", f"Erreur inattendue : {e}")
                result.errors.append(err)
                self.logger.error(f"[props] {path.name}: {e}", exc_info=True)

        if result.needs_rename:
            try:
                self.fs_handler.rename_file(path, result.new_filename)
                result.renamed = True
            except RenameError as e:
                err = StageError(str(path), "rename", str(e))
                result.errors.append(err)
                self.logger.error(f"[rename] {path.name}: {e}")
            except Exception as e:
                err = StageError(str(path), "rename", f"Erreur inattendue : {e}")
                result.errors.append(err)
                self.logger.error(f"[rename] {path.name}: {e}", exc_info=True)

        return result

    def _cover_for_parsed(self, parsed: ParsedTitle):
        image = self.artist_images.resolve_from_artists(parsed.primary_artists)
        if image is None:
            return None
        try:
            return self.artist_images.read_bytes(image)
        except Exception as e:
            self.logger.warning(f"Lecture image artiste {image.path.name}: {e}")
            return None

    def _plan_files_parallel(
        self,
        music_files: List[Tuple[Path, str, str]]
    ) -> Tuple[List[FileUpdateResult], int]:
        results: List[FileUpdateResult] = []
        errors = 0
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.plan_single_file, info): info
                for info in music_files
            }
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=PROCESSING_TIMEOUT)
                    if result:
                        results.append(result)
                    else:
                        errors += 1
                except Exception as e:
                    file_info = futures[future]
                    self.logger.error(
                        f"Erreur parallèle pour {file_info[0]}: {e}",
                        exc_info=True
                    )
                    errors += 1
        results.sort(key=lambda r: r.original_name.lower())
        return results, errors

    def _plan_files_sequential(
        self,
        music_files: List[Tuple[Path, str, str]]
    ) -> Tuple[List[FileUpdateResult], int]:
        results: List[FileUpdateResult] = []
        errors = 0
        for file_info in music_files:
            result = self.plan_single_file(file_info)
            if result:
                results.append(result)
            else:
                errors += 1
        return results, errors

    def _harmonize_results(
        self,
        results: List[FileUpdateResult],
        extra_aliases: Optional[Dict[str, str]] = None,
    ) -> List[FileUpdateResult]:
        """Unifie les variantes d'artistes et d'albums sur tout le lot."""
        patterns = self.formatter.patterns
        aliases = dict(patterns.artist_aliases or {})
        if extra_aliases:
            aliases.update(extra_aliases)

        # Après table IA: ne pas retitle-caser (préserve GIMS, etc.)
        if extra_aliases:
            normalize_fn = lambda s: str(s).strip() if s else s
        else:
            normalize_fn = self.formatter.extractor.normalize_name

        artist_harm = ArtistHarmonizer(
            aliases=aliases,
            fuzzy_distance=patterns.artist_fuzzy_distance,
            fuzzy_min_length=patterns.artist_fuzzy_min_length,
            normalize_fn=normalize_fn,
        )
        album_harm = ArtistHarmonizer(
            aliases={k: v for k, v in aliases.items()},
            fuzzy_distance=patterns.artist_fuzzy_distance,
            fuzzy_min_length=patterns.artist_fuzzy_min_length,
            normalize_fn=normalize_fn,
        )

        for result in results:
            for artist in result.parsed.primary_artists:
                artist_harm.register(artist)
            for feat in result.parsed.featured_artists:
                artist_harm.register(feat)
            if result.parsed.album:
                album_harm.register(result.parsed.album)

        artist_harm.finalize()
        album_harm.finalize()

        harmonized: List[FileUpdateResult] = []
        for result in results:
            parsed = result.parsed
            primary = tuple(
                artist_harm.resolve(a) or a for a in parsed.primary_artists
            )
            featured = tuple(
                artist_harm.resolve(a) or a for a in parsed.featured_artists
            )
            primary_keys = {a.casefold() for a in primary}
            featured = tuple(a for a in featured if a.casefold() not in primary_keys)
            album = album_harm.resolve(parsed.album) if parsed.album else parsed.album
            new_parsed = ParsedTitle(
                primary,
                parsed.song_title,
                featured,
                parsed.original_title,
                album,
            )
            harmonized.append(result.with_parsed(new_parsed))
        return harmonized

    def process_folder(
        self,
        folder_path: str,
        dry_run: bool = True,
        recursive: bool = False,
        parallel: bool = True,
        show_preview: bool = True
    ) -> Dict:
        music_files = self.fs_handler.get_music_files(
            folder_path,
            self.formatter.patterns.music_extensions,
            recursive
        )

        if not music_files:
            self.logger.info("Aucun fichier musical trouvé dans le dossier.")
            return {
                'total': 0,
                'processed': 0,
                'renamed': 0,
                'tags_written': 0,
                'props_written': 0,
                'errors': 0,
                'error_details': [],
            }

        self.logger.info(f"Fichiers musicaux trouvés : {len(music_files)}")

        if parallel and len(music_files) > 1:
            results, plan_errors = self._plan_files_parallel(music_files)
        else:
            results, plan_errors = self._plan_files_sequential(music_files)

        ai_corrected = 0
        extra_aliases: Dict[str, str] = {}
        if self.use_ai and self.ai_enricher is not None:
            self.logger.info("Enrichissement IA OpenAI en cours...")
            results = self.ai_enricher.enrich_results(
                results,
                normalize_fn=self.formatter.extractor.normalize_name,
            )
            ai_corrected = sum(1 for r in results if r.ai_corrected)

        if self.use_ai and self.canonical_resolver is not None:
            self.logger.info("Construction table noms officiels IA...")
            results = self.canonical_resolver.build_and_apply(results)
            extra_aliases = self.canonical_resolver.as_aliases()
            ai_corrected = sum(1 for r in results if r.ai_corrected)

        results = self._harmonize_results(results, extra_aliases=extra_aliases or None)
        results = resolve_duplicates(results)
        duplicates = sum(1 for r in results if r.is_duplicate)

        if show_preview and dry_run:
            self.display.display_preview(results)

        all_errors: List[StageError] = []
        tags_written = 0
        props_written = 0
        covers_written = 0
        renamed_count = 0
        deleted_duplicates = 0

        for result in results:
            if result.is_duplicate:
                if dry_run:
                    if not show_preview:
                        self.display.display_file_result(result, dry_run=True)
                    deleted_duplicates += 1
                else:
                    try:
                        self.fs_handler.delete_file(result.file_path)
                        result.deleted = True
                        deleted_duplicates += 1
                    except DeleteError as e:
                        err = StageError(str(result.file_path), "delete", str(e))
                        result.errors.append(err)
                        all_errors.append(err)
                        self.logger.error(f"[delete] {result.original_name}: {e}")
                    self.display.display_file_result(result, dry_run=False)
                continue

            if dry_run:
                if not show_preview:
                    self.display.display_file_result(result, dry_run=True)
                if result.needs_rename:
                    renamed_count += 1
                if result.tag_title or result.tag_artist:
                    tags_written += 1
                    props_written += 1
                if self.artist_images.resolve_from_artists(result.parsed.primary_artists):
                    covers_written += 1
            else:
                updated = self.apply_file_updates(result)
                self.display.display_file_result(updated, dry_run=False)
                if updated.tags_written:
                    tags_written += 1
                if updated.props_written:
                    props_written += 1
                if updated.cover_written:
                    covers_written += 1
                if updated.renamed:
                    renamed_count += 1
                all_errors.extend(updated.errors)

        return {
            'total': len(music_files),
            'processed': len(results) - sum(1 for r in results if r.is_duplicate),
            'renamed': renamed_count,
            'tags_written': tags_written,
            'props_written': props_written,
            'covers_written': covers_written,
            'ai_corrected': ai_corrected,
            'duplicates': duplicates,
            'duplicates_deleted': deleted_duplicates,
            'errors': plan_errors + len(all_errors),
            'error_details': [e.to_dict() for e in all_errors],
            'formatter_stats': self.formatter.get_stats(),
            'results': results,
        }

    def create_backup_list(
        self,
        folder_path: str,
        output_file: str = "backup_list.json",
        recursive: bool = False
    ) -> None:
        try:
            music_files = self.fs_handler.get_music_files(
                folder_path,
                self.formatter.patterns.music_extensions,
                recursive
            )
            files_data = []
            for file_path, name, ext in music_files:
                entry: Dict[str, Any] = {
                    'original': str(file_path),
                    'name': name,
                    'ext': ext,
                }
                try:
                    entry['tags'] = self.metadata_writer.read_tags(file_path)
                except Exception:
                    entry['tags'] = {}
                files_data.append(entry)

            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'folder': folder_path,
                'files': files_data,
            }
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Liste de sauvegarde créée : {output_file}")
        except (IOError, PermissionError) as e:
            self.logger.error(f"Erreur création sauvegarde : {e}")
        except Exception as e:
            self.logger.error(
                f"Erreur inattendue sauvegarde : {e}", exc_info=True
            )


# ============================================================================
# CLI / INTERACTIF
