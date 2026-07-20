"""Operations systeme de fichiers."""
from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import List, Tuple

from music_formatter.exceptions import DeleteError, RenameError
from music_formatter.io.sanitizer import FilenameSanitizer


class FileSystemHandler:
    """Opérations sur le système de fichiers."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.sanitizer = FilenameSanitizer()

    def get_music_files(
        self,
        folder_path: str,
        extensions: frozenset,
        recursive: bool = False
    ) -> List[Tuple[Path, str, str]]:
        folder = Path(folder_path)

        if not folder.exists():
            raise FileNotFoundError(f"Le dossier '{folder_path}' n'existe pas.")
        if not folder.is_dir():
            raise NotADirectoryError(f"'{folder_path}' n'est pas un dossier.")

        pattern = "**/*" if recursive else "*"
        music_files = []

        try:
            for file_path in folder.glob(pattern):
                if file_path.is_file() and file_path.suffix.lower() in extensions:
                    music_files.append((file_path, file_path.stem, file_path.suffix))
        except PermissionError as e:
            self.logger.error(f"Permission refusée pour '{folder_path}': {e}")
            raise
        except Exception as e:
            self.logger.error(f"Erreur lecture dossier : {e}", exc_info=True)
            raise

        return sorted(music_files, key=lambda x: x[0].name.lower())

    def rename_file(self, file_path: Path, new_name: str) -> None:
        """Renomme un fichier. Lève RenameError en cas d'échec."""
        sanitized_name = self.sanitizer.sanitize(new_name)
        new_path = file_path.parent / sanitized_name

        if self.sanitizer.is_path_too_long(new_path):
            raise RenameError(f"Chemin trop long pour '{sanitized_name}'.")

        if self.sanitizer.has_invalid_chars(sanitized_name):
            raise RenameError(f"Nom de fichier invalide : '{sanitized_name}'.")

        try:
            if (
                file_path.name.lower() == sanitized_name.lower()
                and file_path.name != sanitized_name
            ):
                self._fix_case(file_path, sanitized_name, new_path)
                return

            if new_path.exists() and new_path != file_path:
                raise RenameError(
                    f"Collision : '{sanitized_name}' existe déjà."
                )

            file_path.rename(new_path)
            self.logger.info(f"Renommé : {file_path.name} -> {sanitized_name}")
        except RenameError:
            raise
        except PermissionError as e:
            raise RenameError(f"Permission refusée lors du renommage : {e}") from e
        except OSError as e:
            raise RenameError(f"Erreur système lors du renommage : {e}") from e
        except Exception as e:
            raise RenameError(f"Erreur inattendue renommage : {e}") from e

    def _fix_case(self, file_path: Path, sanitized_name: str, new_path: Path) -> None:
        temp_name = f"temp_{uuid.uuid4().hex[:8]}_{sanitized_name}"
        temp_path = file_path.parent / temp_name
        try:
            file_path.rename(temp_path)
            temp_path.rename(new_path)
            self.logger.info(f"Casse corrigée : {file_path.name} -> {sanitized_name}")
        except Exception as e:
            raise RenameError(f"Erreur correction de casse : {e}") from e

    def delete_file(self, file_path: Path) -> None:
        """Supprime un fichier doublon. Lève DeleteError en cas d'échec."""
        try:
            if not file_path.exists():
                raise DeleteError(f"Fichier introuvable : {file_path}")
            file_path.unlink()
            self.logger.info(f"Doublon supprimé : {file_path.name}")
        except DeleteError:
            raise
        except PermissionError as e:
            raise DeleteError(f"Permission refusée lors de la suppression : {e}") from e
        except OSError as e:
            raise DeleteError(f"Erreur système lors de la suppression : {e}") from e
        except Exception as e:
            raise DeleteError(f"Erreur inattendue suppression : {e}") from e
