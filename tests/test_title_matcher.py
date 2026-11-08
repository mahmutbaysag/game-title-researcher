"""Unit tests for title normalization, variant generation, and matching logic."""
from scripts.models import MatchCategory
from scripts.title_matcher import (
    normalize_title,
    generate_variants,
    classify_match,
)


def test_normalization_basic():
    assert normalize_title("Ironhold") == "ironhold"
    assert normalize_title("  The   Iron   Hold!  ") == "the iron hold"
    assert normalize_title("Pokémon: Red & Blue") == "pokemon red blue"
    assert normalize_title("Dead-End: Chapter 1") == "dead end chapter 1"


def test_variant_generation():
    variants = generate_variants("The Iron Hold")
    assert "The Iron Hold" in variants
    assert "the iron hold" in variants
    assert "iron hold" in variants  # Article stripped
    assert "ironhold" in variants   # Concatenated
    assert "iron-hold" in variants  # Hyphenated


# --- Brief Section 10 Acceptance Tests 1-6 ---

def test_case_1_exact_same_capitalization():
    cat, score = classify_match("Ironhold", "Ironhold")
    assert cat == MatchCategory.EXACT_MATCH
    assert score == 1.0


def test_case_2_exact_different_capitalization():
    cat, score = classify_match("ironhold", "IRONHOLD")
    assert cat == MatchCategory.EXACT_MATCH
    assert score == 1.0


def test_case_3_punctuation_and_spacing_difference():
    cat, score = classify_match("Ironhold", "Iron-Hold")
    # "ironhold" vs "iron hold" (normalized) -> token sort ratio high / near exact
    assert cat in (MatchCategory.NEAR_EXACT, MatchCategory.STRUCTURAL_MATCH)
    assert score >= 0.85


def test_case_4_minor_typo_near_exact():
    cat, score = classify_match("Ironhold", "Ironhould")
    assert cat == MatchCategory.NEAR_EXACT
    assert score >= 0.85


def test_case_5_phonetically_similar_title():
    # "Knight" vs "Night" have identical soundex/metaphone
    cat, score = classify_match("Night Quest", "Knight Quest")
    assert cat in (MatchCategory.PHONETIC_MATCH, MatchCategory.NEAR_EXACT)
    assert score >= 0.70


def test_case_6_shared_generic_word_unrelated():
    # Both have "War" but are completely unrelated titles
    cat, score = classify_match("War of Titans", "Star Wars")
    assert cat == MatchCategory.UNRELATED
