"""Ecriture des tags audio (mutagen)."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

try:
    import mutagen
    from mutagen import MutagenError
    from mutagen.easyid3 import EasyID3
    from mutagen.id3 import ID3NoHeaderError
except ImportError:  # pragma: no cover
    mutagen = None
    MutagenError = Exception
    EasyID3 = None
    ID3NoHeaderError = Exception

from music_formatter.exceptions import CoverWriteError, TagWriteError
from music_formatter.models import MediaMetadata, ParsedTitle

if EasyID3 is not None:
    try:
        EasyID3.RegisterTextKey("comment", "COMM")
    except Exception:
        pass


class AudioMetadataWriter:
    """Écriture des tags audio via mutagen."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        if mutagen is None:
            raise ImportError(
                "Le paquet 'mutagen' est requis. Installez-le avec : "
                "py -m pip install -r requirements.txt"
            )

    def read_tags(self, file_path: Path) -> Dict[str, str]:
        """Lit les tags title/artist/album actuels (best effort)."""
        try:
            tags = self._load_easy_tags(file_path)
            if tags is None:
                return {}
            result = {}
            for key in ('title', 'artist', 'album', 'albumartist', 'comment'):
                value = self._get_first(tags, key)
                if value:
                    result[key] = value
            return result
        except Exception as e:
            self.logger.debug(f"Lecture tags impossible pour {file_path}: {e}")
            return {}

    def write(
        self,
        file_path: Path,
        parsed: ParsedTitle,
        cover: Optional[Tuple[bytes, str]] = None,
    ) -> None:
        """Écrit title, artist, comment. Album et genre sont vidés.

        cover: (bytes, mime) optionnel pour embarquer l'image artiste.
        """
        meta = MediaMetadata.from_parsed(parsed)
        if not meta.title and not meta.artist:
            raise TagWriteError("Aucune métadonnée à écrire (titre et artiste vides).")

        try:
            if file_path.suffix.lower() == '.mp3':
                self._write_mp3(file_path, meta, cover=cover)
            else:
                self._write_generic(file_path, meta, cover=cover)

            cover_state = "set" if cover else "removed"
            self.logger.info(
                f"Tags écrits : {file_path.name} "
                f"(title={meta.title!r}, artist={meta.artist!r}, "
                f"album='', genre='', cover={cover_state})"
            )
        except TagWriteError:
            raise
        except PermissionError as e:
            raise TagWriteError(
                f"Permission refusée (fichier ouvert ?) : {e}"
            ) from e
        except (OSError, MutagenError) as e:
            raise TagWriteError(f"Échec écriture tags : {e}") from e
        except Exception as e:
            raise TagWriteError(f"Erreur inattendue tags : {e}") from e

    def set_cover(self, file_path: Path, cover_data: bytes, mime: str) -> None:
        """Embarque une image artiste (remplace toute pochette existante)."""
        if not cover_data:
            raise CoverWriteError("Données image vides.")
        if not mime:
            raise CoverWriteError("MIME image manquant.")

        try:
            suffix = file_path.suffix.lower()
            if suffix == ".mp3":
                self._set_mp3_cover(str(file_path), cover_data, mime)
            else:
                self._set_generic_cover(file_path, cover_data, mime)
            self.logger.info(
                f"Image artiste écrite : {file_path.name} ({mime}, {len(cover_data)} o)"
            )
        except CoverWriteError:
            raise
        except PermissionError as e:
            raise CoverWriteError(
                f"Permission refusée (fichier ouvert ?) : {e}"
            ) from e
        except (OSError, MutagenError) as e:
            raise CoverWriteError(f"Échec écriture image : {e}") from e
        except Exception as e:
            raise CoverWriteError(f"Erreur inattendue image : {e}") from e

    def _load_easy_tags(self, file_path: Path):
        if file_path.suffix.lower() == '.mp3':
            try:
                return EasyID3(str(file_path))
            except ID3NoHeaderError:
                return None
        audio = mutagen.File(str(file_path), easy=True)
        if audio is None:
            return None
        return audio.tags

    def _write_mp3(
        self,
        file_path: Path,
        meta: MediaMetadata,
        cover: Optional[Tuple[bytes, str]] = None,
    ) -> None:
        path_str = str(file_path)
        try:
            tags = EasyID3(path_str)
        except ID3NoHeaderError:
            tags = EasyID3()
        self._apply_meta(tags, meta)
        tags.save(path_str)
        cover_data, cover_mime = cover if cover else (None, None)
        self._strip_mp3_id3_extras(
            path_str,
            meta.description,
            cover_data=cover_data,
            cover_mime=cover_mime,
        )

    def _strip_mp3_id3_extras(
        self,
        path_str: str,
        description: str = "",
        cover_data: Optional[bytes] = None,
        cover_mime: Optional[str] = None,
    ) -> None:
        """Vide album/genre, gère la pochette, réécrit le commentaire."""
        try:
            from mutagen.id3 import COMM, ID3
            try:
                id3 = ID3(path_str)
            except ID3NoHeaderError:
                if not description and not cover_data:
                    return
                id3 = ID3()

            id3.delall("TALB")
            id3.delall("TCON")
            id3.delall("APIC")
            id3.delall("PIC")

            if cover_data and cover_mime:
                id3.add(self._make_apic(cover_data, cover_mime))

            if description:
                id3.delall("COMM")
                id3.add(COMM(encoding=3, lang="eng", desc="desc", text=description))

            # ID3v2.3 : Windows Explorer / Lecteur Windows lisent la pochette
            self._save_id3_windows(id3, path_str)
        except Exception as e:
            self.logger.debug(f"Strip ID3 album/genre/cover : {e}")

    def _set_mp3_cover(self, path_str: str, cover_data: bytes, mime: str) -> None:
        from mutagen.id3 import ID3
        try:
            id3 = ID3(path_str)
        except ID3NoHeaderError:
            id3 = ID3()
        try:
            id3.update_to_v23()
        except Exception:
            pass
        id3.delall("APIC")
        id3.delall("PIC")
        id3.add(self._make_apic(cover_data, mime))
        self._save_id3_windows(id3, path_str)

    @staticmethod
    def _make_apic(cover_data: bytes, mime: str):
        """APIC compatible Windows (encoding latin-1, desc vide, type Cover Front)."""
        from mutagen.id3 import APIC
        mime_norm = "image/jpeg" if mime in ("image/jpeg", "image/jpg") else mime
        return APIC(
            encoding=0,
            mime=mime_norm,
            type=3,
            desc="",
            data=cover_data,
        )

    @staticmethod
    def _save_id3_windows(id3, path_str: str) -> None:
        """Sauvegarde ID3v2.3 (Explorer ne lit pas correctement APIC en v2.4)."""
        try:
            id3.update_to_v23()
        except Exception:
            pass
        id3.save(path_str, v2_version=3)

    def _write_generic(
        self,
        file_path: Path,
        meta: MediaMetadata,
        cover: Optional[Tuple[bytes, str]] = None,
    ) -> None:
        audio = mutagen.File(str(file_path), easy=True)
        if audio is None:
            raise TagWriteError(
                f"Format non supporté ou fichier illisible : {file_path.suffix}"
            )
        if audio.tags is None:
            try:
                audio.add_tags()
            except Exception as e:
                raise TagWriteError(
                    f"Impossible de créer des tags pour {file_path.name}: {e}"
                ) from e
        self._apply_meta(audio.tags, meta)
        self._clear_embedded_pictures(audio)
        if cover:
            self._embed_cover_on_audio(audio, cover[0], cover[1])
        audio.save()

    def _set_generic_cover(
        self, file_path: Path, cover_data: bytes, mime: str
    ) -> None:
        audio = mutagen.File(str(file_path))
        if audio is None:
            raise CoverWriteError(
                f"Format non supporté ou fichier illisible : {file_path.suffix}"
            )
        self._clear_embedded_pictures(audio)
        self._embed_cover_on_audio(audio, cover_data, mime)
        audio.save()

    def _embed_cover_on_audio(
        self, audio: Any, cover_data: bytes, mime: str
    ) -> None:
        """Embarque une image selon le format (FLAC / MP4 / Vorbis)."""
        suffix = ""
        try:
            filename = getattr(audio, "filename", None)
            if filename:
                suffix = Path(filename).suffix.lower()
        except Exception:
            suffix = ""

        if hasattr(audio, "add_picture"):
            from mutagen.flac import Picture
            pic = Picture()
            pic.type = 3
            pic.mime = mime
            pic.desc = "Cover"
            pic.data = cover_data
            audio.add_picture(pic)
            return

        tags = getattr(audio, "tags", None)
        if tags is None:
            raise CoverWriteError("Aucun conteneur de tags pour l'image.")

        if suffix in (".m4a", ".mp4", ".aac"):
            from mutagen.mp4 import MP4Cover
            fmt = (
                MP4Cover.FORMAT_PNG
                if mime == "image/png"
                else MP4Cover.FORMAT_JPEG
            )
            tags["covr"] = [MP4Cover(cover_data, imageformat=fmt)]
            return

        try:
            import base64
            from mutagen.flac import Picture
            pic = Picture()
            pic.type = 3
            pic.mime = mime
            pic.desc = "Cover"
            pic.data = cover_data
            encoded = base64.b64encode(pic.write()).decode("ascii")
            tags["metadata_block_picture"] = [encoded]
            return
        except Exception as e:
            raise CoverWriteError(
                f"Format image non supporté pour ce fichier ({suffix or 'inconnu'}): {e}"
            ) from e

    def _clear_embedded_pictures(self, audio: Any) -> None:
        """Supprime les images embarquées (FLAC / MP4 / Ogg / etc.)."""
        try:
            if hasattr(audio, "clear_pictures"):
                audio.clear_pictures()
                return
        except Exception as e:
            self.logger.debug(f"clear_pictures : {e}")

        try:
            if hasattr(audio, "pictures") and audio.pictures:
                audio.pictures = []
        except Exception as e:
            self.logger.debug(f"pictures=[] : {e}")

        tags = getattr(audio, "tags", None)
        if tags is None:
            return

        # MP4 / M4A
        for key in ("covr", "----:com.apple.iTunes:Artwork"):
            try:
                if key in tags:
                    del tags[key]
            except Exception:
                pass

        # Vorbis / Ogg METADATA_BLOCK_PICTURE
        try:
            if hasattr(tags, "getall"):
                for picture_key in list(tags.keys()):
                    if "METADATA_BLOCK_PICTURE" in str(picture_key).upper():
                        del tags[picture_key]
            elif hasattr(tags, "keys"):
                for picture_key in list(tags.keys()):
                    if "METADATA_BLOCK_PICTURE" in str(picture_key).upper():
                        del tags[picture_key]
        except Exception as e:
            self.logger.debug(f"Clear METADATA_BLOCK_PICTURE : {e}")

    def _apply_meta(self, tags: Any, meta: MediaMetadata) -> None:
        mapping = {
            'title': meta.title,
            'artist': meta.artist,
            'albumartist': meta.albumartist,
            'comment': meta.description,
        }
        for key, value in mapping.items():
            if not value:
                continue
            try:
                self._set_tag(tags, key, value)
            except (KeyError, ValueError, MutagenError, TypeError, AttributeError):
                if key == 'comment':
                    continue
                raise
        # Album et genre: toujours vides (supprime les valeurs existantes).
        for empty_key in ('album', 'genre'):
            self._clear_tag(tags, empty_key)

    @staticmethod
    def _clear_tag(tags: Any, key: str) -> None:
        try:
            if key in tags:
                del tags[key]
        except Exception:
            try:
                tags[key] = []
            except Exception:
                pass

    @staticmethod
    def _get_first(tags: Any, key: str) -> str:
        try:
            values = tags.get(key)
            if not values:
                return ""
            if isinstance(values, list):
                return str(values[0]) if values else ""
            return str(values)
        except Exception:
            return ""

    @staticmethod
    def _set_tag(tags: Any, key: str, value: str) -> None:
        tags[key] = value
