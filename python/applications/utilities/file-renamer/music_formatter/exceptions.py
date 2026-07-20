"""Exceptions métier."""


class TagWriteError(Exception):
    """Échec d'écriture des tags audio."""


class PropertyWriteError(Exception):
    """Échec d'écriture des propriétés Windows."""


class RenameError(Exception):
    """Échec de renommage du fichier."""


class DeleteError(Exception):
    """Échec de suppression du fichier."""


class CoverWriteError(Exception):
    """Échec d'écriture de la pochette / image artiste."""
