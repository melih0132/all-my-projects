"""Configuration des logs (error / warning / execution)."""
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from music_formatter.constants import LOGS_ROOT


class LevelFilter(logging.Filter):
    """Ne laisse passer qu'un niveau exact."""

    def __init__(self, level: int):
        super().__init__()
        self.level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == self.level


def setup_logging(logs_root: Optional[Path] = None) -> logging.Logger:
    """Configure loggers fichiers séparés + console."""
    root_dir = Path(logs_root) if logs_root else LOGS_ROOT
    for name in ("error", "warning", "execution"):
        (root_dir / name).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("music_formatter")
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)
    logger.addHandler(console)

    error_h = RotatingFileHandler(
        root_dir / "error" / "error.log",
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    error_h.setLevel(logging.ERROR)
    error_h.setFormatter(fmt)
    logger.addHandler(error_h)

    warning_h = RotatingFileHandler(
        root_dir / "warning" / "warning.log",
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    warning_h.setLevel(logging.WARNING)
    warning_h.setFormatter(fmt)
    warning_h.addFilter(LevelFilter(logging.WARNING))
    logger.addHandler(warning_h)

    execution_h = RotatingFileHandler(
        root_dir / "execution" / "execution.log",
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    execution_h.setLevel(logging.INFO)
    execution_h.setFormatter(fmt)
    execution_h.addFilter(LevelFilter(logging.INFO))
    logger.addHandler(execution_h)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    base = logging.getLogger("music_formatter")
    if not base.handlers:
        setup_logging()
    if name:
        return base.getChild(name)
    return base
