"""Harmonisation des noms d artistes / albums."""
from __future__ import annotations

import re
from typing import Dict, List, Optional

from music_formatter.parsing.casing import identity_key


class ArtistHarmonizer:
    """
    Unifie les variantes d'un même artiste dans un lot de fichiers.
    Ex. GENESIO / genesio / GeNeSiO / GENESIOn → une seule forme canonique.
    Support turc : Özdemir / özdemir / ÖZDEMİR.
    """

    def __init__(
        self,
        aliases: Optional[Dict[str, str]] = None,
        fuzzy_distance: int = 1,
        fuzzy_min_length: int = 5,
        normalize_fn=None,
    ):
        self.aliases = {
            identity_key(k.strip()): v.strip()
            for k, v in (aliases or {}).items()
            if k and v
        }
        self.fuzzy_distance = max(0, int(fuzzy_distance))
        self.fuzzy_min_length = max(1, int(fuzzy_min_length))
        self.normalize_fn = normalize_fn or (lambda s: s)
        self._counts: Dict[str, int] = {}
        self._best_form: Dict[str, str] = {}
        self._key_to_canonical: Dict[str, str] = {}

    def register(self, name: Optional[str]) -> None:
        if not name or not str(name).strip():
            return
        normalized = self.normalize_fn(str(name).strip())
        if not normalized or not str(normalized).strip():
            return
        normalized = str(normalized).strip()
        key = identity_key(normalized)
        if key in self.aliases:
            aliased = self.normalize_fn(self.aliases[key])
            if not aliased:
                return
            aliased = str(aliased).strip()
            key = identity_key(aliased)
            normalized = aliased
        self._counts[key] = self._counts.get(key, 0) + 1
        prev = self._best_form.get(key)
        if prev is None or self._score_form(normalized) > self._score_form(prev):
            self._best_form[key] = normalized

    def finalize(self) -> None:
        """Regroupe les clés proches et choisit une forme canonique par cluster."""
        keys = list(self._counts.keys())
        parent = {k: k for k in keys}

        def find(x: str) -> str:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: str, b: str) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                if self._should_merge(a, b):
                    union(a, b)

        clusters: Dict[str, List[str]] = {}
        for k in keys:
            root = find(k)
            clusters.setdefault(root, []).append(k)

        for members in clusters.values():
            canonical = self._pick_canonical(members)
            for m in members:
                self._key_to_canonical[m] = canonical

    def resolve(self, name: Optional[str]) -> Optional[str]:
        if not name or not str(name).strip():
            return name
        normalized = self.normalize_fn(str(name).strip())
        if not normalized:
            return str(name).strip()
        normalized = str(normalized).strip()
        key = identity_key(normalized)
        if key in self.aliases:
            aliased = self.normalize_fn(self.aliases[key])
            if aliased:
                aliased = str(aliased).strip()
                key = identity_key(aliased)
                normalized = aliased
        return self._key_to_canonical.get(key, self._best_form.get(key, normalized))

    def _should_merge(self, a: str, b: str) -> bool:
        if a == b:
            return True
        if self.fuzzy_distance <= 0:
            return False
        if min(len(a), len(b)) < self.fuzzy_min_length:
            return False
        return self._edit_distance(a, b) <= self.fuzzy_distance

    @staticmethod
    def _edit_distance(a: str, b: str) -> int:
        if a == b:
            return 0
        la, lb = len(a), len(b)
        if la < lb:
            a, b = b, a
            la, lb = lb, la
        prev = list(range(lb + 1))
        for i, ca in enumerate(a, 1):
            curr = [i]
            for j, cb in enumerate(b, 1):
                cost = 0 if ca == cb else 1
                curr.append(min(curr[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost))
            prev = curr
        return prev[lb]

    def _pick_canonical(self, members: List[str]) -> str:
        best_key = max(
            members,
            key=lambda k: (
                self._counts.get(k, 0),
                self._score_form(self._best_form.get(k, "")),
                -len(k),
            ),
        )
        return self._best_form[best_key]

    @staticmethod
    def _score_form(form: Optional[str]) -> int:
        """Score d'affichage. ALL CAPS courts (GIMS, MØ) restent valides."""
        if not form:
            return 0
        score = 0
        letters = [c for c in form if c.isalpha()]
        if form != form.upper() and form != form.lower():
            score += 30
        if form and form[0].isupper():
            score += 10
        if form != form.lower():
            score += 5
        # Marque stylisée tout en majuscules (2-8 lettres): bonus
        if (
            letters
            and form == form.upper()
            and 2 <= len(letters) <= 8
            and " " not in form.strip()
        ):
            score += 40
        elif form != form.upper():
            score += 5
        if re.search(r"^[A-Z]{3,}[a-z]{1,2}$", form):
            score -= 40
        return score
