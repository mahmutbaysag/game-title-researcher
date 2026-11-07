"""Title normalization, variant generation, and similarity comparison."""
from __future__ import annotations

import re
import unicodedata

from rapidfuzz import fuzz
from jellyfish import soundex, metaphone, jaro_winkler_similarity

from .models import MatchCategory


# Words too common in game titles to signal a meaningful match alone
GENERIC_TITLE_WORDS = frozenset({
    # Articles and prepositions
    "the", "a", "an", "of", "and", "or", "in", "on", "at", "to", "for",
    "is", "it", "my", "no", "do", "go", "up", "so", "by", "as",
    # Very common single-word game-title components
    "game", "games", "war", "wars", "dark", "dead", "last", "rise", "fall",
    "world", "worlds", "star", "stars", "battle", "quest", "legend", "legends",
    "shadow", "shadows", "blood", "iron", "steel", "fire", "ice", "storm",
    "night", "day", "king", "lord", "dragon", "dragons", "sword", "swords",
    "stone", "tower", "gate", "city", "land", "lands", "lost", "new", "old",
    "red", "black", "white", "blue", "death", "life", "age", "end", "hero",
    "heroes", "super", "ultra", "mega", "final", "eternal", "infinite",
})


def normalize_title(title: str) -> str:
    """Normalize a game title for comparison.

    1. Unicode NFKD normalization + remove combining marks
    2. Lowercase
    3. Replace non-alphanumeric with spaces
    4. Collapse whitespace
    """
    text = unicodedata.normalize("NFKD", title)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def generate_variants(title: str) -> list[str]:
    """Generate search query variants from a title."""
    normalized = normalize_title(title)
    words = normalized.split()
    variants: list[str] = []
    seen: set[str] = set()

    def _add(v: str) -> None:
        v = v.strip()
        if v and v not in seen:
            seen.add(v)
            variants.append(v)

    _add(title)
    _add(normalized)

    # Without leading article
    stripped_words = (
        words[1:]
        if (words and words[0] in {"the", "a", "an"} and len(words) > 1)
        else words
    )
    if stripped_words != words:
        _add(" ".join(stripped_words))
        if len(stripped_words) > 1:
            _add("".join(stripped_words))
            _add("-".join(stripped_words))

    # Concatenated
    if len(words) > 1:
        _add("".join(words))

    # Hyphenated
    if len(words) > 1:
        _add("-".join(words))

    # Simple plural / singular
    if normalized.endswith("s") and len(normalized) > 3:
        _add(normalized[:-1])
    elif not normalized.endswith("s"):
        _add(normalized + "s")

    return variants


def compare_titles(query: str, candidate: str) -> dict[str, float | bool]:
    """Compare two titles using multiple similarity algorithms."""
    norm_q = normalize_title(query)
    norm_c = normalize_title(candidate)

    empty: dict[str, float | bool] = {
        "exact_normalized": 0.0,
        "levenshtein_ratio": 0.0,
        "jaro_winkler": 0.0,
        "token_sort_ratio": 0.0,
        "token_set_ratio": 0.0,
        "partial_ratio": 0.0,
        "soundex_match": False,
        "metaphone_match": False,
    }
    if not norm_q or not norm_c:
        return empty

    try:
        soundex_match = soundex(norm_q) == soundex(norm_c)
    except Exception:
        soundex_match = False

    try:
        metaphone_match = metaphone(norm_q) == metaphone(norm_c)
    except Exception:
        metaphone_match = False

    return {
        "exact_normalized": 1.0 if norm_q == norm_c else 0.0,
        "levenshtein_ratio": fuzz.ratio(norm_q, norm_c) / 100.0,
        "jaro_winkler": jaro_winkler_similarity(norm_q, norm_c),
        "token_sort_ratio": fuzz.token_sort_ratio(norm_q, norm_c) / 100.0,
        "token_set_ratio": fuzz.token_set_ratio(norm_q, norm_c) / 100.0,
        "partial_ratio": fuzz.partial_ratio(norm_q, norm_c) / 100.0,
        "soundex_match": soundex_match,
        "metaphone_match": metaphone_match,
    }


def classify_match(
    query: str,
    candidate: str,
    scores: dict[str, float | bool] | None = None,
) -> tuple[MatchCategory, float]:
    """Classify the similarity between two titles.

    Returns ``(category, representative_score)``.
    """
    if scores is None:
        scores = compare_titles(query, candidate)

    # 1. Exact normalized match
    if scores["exact_normalized"] == 1.0:
        return MatchCategory.EXACT_MATCH, 1.0

    lev: float = float(scores["levenshtein_ratio"])
    tset: float = float(scores["token_set_ratio"])
    tsort: float = float(scores["token_sort_ratio"])
    partial: float = float(scores["partial_ratio"])

    # 2. Near exact (typos, minor spelling differences)
    if lev >= 0.85:
        return MatchCategory.NEAR_EXACT, lev

    # 3. Phonetic match (sounds alike + some string similarity)
    if (scores["soundex_match"] or scores["metaphone_match"]) and lev >= 0.50:
        return MatchCategory.PHONETIC_MATCH, max(lev, 0.70)

    # 4. Structural match (same words, different order / extras)
    if tset >= 0.80 or tsort >= 0.85:
        return MatchCategory.STRUCTURAL_MATCH, max(tset, tsort)

    # 5. Partial match (shares significant non-generic words)
    norm_q = normalize_title(query)
    norm_c = normalize_title(candidate)
    words_q = set(norm_q.split()) - GENERIC_TITLE_WORDS
    words_c = set(norm_c.split()) - GENERIC_TITLE_WORDS

    if words_q and words_c:
        overlap = words_q & words_c
        if overlap and partial >= 0.70:
            return MatchCategory.PARTIAL_MATCH, partial

    # 6. Unrelated
    return MatchCategory.UNRELATED, max(lev, tset, tsort)
