"""Casse de texte avec support du turc (ı/İ, ğ, ş, ç, ö, ü)."""
from __future__ import annotations

import re
import unicodedata

# Caractères typiquement turcs (hors latin de base)
_TURKISH_CHARS = set("ğĞıİşŞöÖüÜçÇ")

# Minuscules / majuscules spécifiques au turc
_TR_TO_LOWER = str.maketrans({
    "İ": "i",
    "I": "ı",
    "Ğ": "ğ",
    "Ş": "ş",
    "Ü": "ü",
    "Ö": "ö",
    "Ç": "ç",
})

_TR_TO_UPPER = str.maketrans({
    "i": "İ",
    "ı": "I",
    "ğ": "Ğ",
    "ş": "Ş",
    "ü": "Ü",
    "ö": "Ö",
    "ç": "Ç",
})


def has_turkish_chars(text: str) -> bool:
    return any(ch in _TURKISH_CHARS for ch in text)


def looks_turkish(text: str) -> bool:
    """Heuristique : présence de lettres turques dans le texte."""
    return has_turkish_chars(text)


def turkish_lower(text: str) -> str:
    """Minuscules selon la locale turque (I→ı, İ→i)."""
    if not text:
        return text
    # Traduire d'abord I/İ puis lower Unicode pour le reste
    out = []
    for ch in text:
        if ch == "İ":
            out.append("i")
        elif ch == "I":
            out.append("ı")
        elif ch in "ĞŞÜÖÇ":
            out.append(ch.translate(_TR_TO_LOWER))
        else:
            out.append(ch.lower())
    return "".join(out)


def turkish_upper_char(ch: str) -> str:
    """Majuscule d'un caractère selon la locale turque (i→İ, ı→I)."""
    if ch == "i":
        return "İ"
    if ch == "ı":
        return "I"
    if ch in "ğşüöç":
        return ch.translate(_TR_TO_UPPER)
    return ch.upper()


def ascii_upper_char(ch: str) -> str:
    return ch.upper()


def to_lower(text: str, turkish: bool = False) -> str:
    if turkish or looks_turkish(text):
        return turkish_lower(text)
    return text.lower()


def identity_key(text: str) -> str:
    """Clé de comparaison insensible à la casse (turc-aware)."""
    if not text:
        return ""
    # NFKC + minuscules turques pour unifier İ/i et I/ı
    folded = unicodedata.normalize("NFKC", text)
    return turkish_lower(folded)


def is_short_acronym(word: str) -> bool:
    """
    Acronyme court ASCII uniquement (DJ, OK, USA).
    Les mots turcs (ŞARKI, IŞIN) et noms longs (SEZEN, DRAKE) sont title-casés.
    """
    if not word or len(word) > 3:
        return False
    if not word.isupper():
        return False
    if not re.fullmatch(r"[A-Z0-9]+", word):
        return False
    return True


def is_stylized_allcaps(word: str) -> bool:
    """Marque stylisée ALL CAPS (GIMS, BOOBA, PLK), 2-8 caractères ASCII."""
    if not word or " " in word:
        return False
    if not word.isupper():
        return False
    if not re.fullmatch(r"[A-Z0-9]{2,8}", word):
        return False
    return True


def title_case_word(word: str, *, is_first: bool, exceptions: set[str]) -> str:
    """Title-case d'un mot, avec règles turques si nécessaire."""
    if not word:
        return word

    turkish = looks_turkish(word)

    if (is_short_acronym(word) or is_stylized_allcaps(word)) and not turkish:
        return word

    lower = to_lower(word, turkish=turkish)

    if (not is_first) and lower in exceptions and len(word) > 1:
        return lower

    # Mc / Mac (anglais) : uniquement ASCII
    if not turkish:
        if lower.startswith("mc") and len(lower) > 2 and lower[2:].isalpha():
            rest = lower[2:]
            return "Mc" + rest[0].upper() + rest[1:]
        if lower.startswith("mac") and len(lower) > 3 and lower[3:].isalpha():
            rest = lower[3:]
            return "Mac" + rest[0].upper() + rest[1:]

    upper_fn = turkish_upper_char if turkish else ascii_upper_char
    chars = list(lower)
    for i, ch in enumerate(chars):
        if ch.isalpha():
            chars[i] = upper_fn(ch)
            break
    return "".join(chars)
