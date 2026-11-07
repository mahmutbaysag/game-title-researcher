"""Multi-dimensional risk assessment."""
from __future__ import annotations

from .models import (
    EvidenceRecord,
    EntityType,
    MatchCategory,
    RiskAssessment,
    RiskLevel,
    SourceCoverage,
    SourceStatus,
)


def assess_risk(
    title: str,
    evidence: list[EvidenceRecord],
    coverage: list[SourceCoverage],
) -> RiskAssessment:
    """Assess naming risk across multiple dimensions.

    Returns a populated :class:`RiskAssessment`.
    """

    exact = [e for e in evidence if e.match_category == MatchCategory.EXACT_MATCH]
    near = [e for e in evidence if e.match_category == MatchCategory.NEAR_EXACT]
    phonetic = [e for e in evidence if e.match_category == MatchCategory.PHONETIC_MATCH]
    structural = [e for e in evidence if e.match_category == MatchCategory.STRUCTURAL_MATCH]

    # --- 1. Game-title conflict -----------------------------------------
    if len(exact) >= 2:
        game_conflict = RiskLevel.CRITICAL
    elif len(exact) == 1:
        game_conflict = RiskLevel.HIGH
    elif near:
        game_conflict = RiskLevel.MODERATE
    else:
        game_conflict = RiskLevel.LOW

    # --- 2. Spelling / visual similarity --------------------------------
    if near:
        spelling = (
            RiskLevel.HIGH
            if any(e.similarity_score >= 0.90 for e in near)
            else RiskLevel.MODERATE
        )
    elif structural:
        spelling = RiskLevel.MODERATE
    else:
        spelling = RiskLevel.LOW

    # --- 3. Phonetic similarity -----------------------------------------
    phonetic_risk = RiskLevel.MODERATE if phonetic else RiskLevel.LOW

    # --- 4. Franchise / studio association ------------------------------
    franchise_entries = [
        e for e in evidence if e.entity_type == EntityType.FRANCHISE_SERIES
    ]
    franchise_risk = RiskLevel.HIGH if franchise_entries else RiskLevel.LOW

    # --- 5. Trademark signals (always manual) ---------------------------
    trademark_risk = RiskLevel.INSUFFICIENT_DATA

    # --- 6. Search-engine discoverability --------------------------------
    relevant = [
        e for e in evidence if e.match_category != MatchCategory.UNRELATED
    ]
    if len(relevant) >= 5:
        discoverability = RiskLevel.HIGH
    elif len(relevant) >= 2:
        discoverability = RiskLevel.MODERATE
    else:
        discoverability = RiskLevel.LOW

    # --- 7. Evidence coverage -------------------------------------------
    checked = [
        c
        for c in coverage
        if c.status in (SourceStatus.CHECKED_OK, SourceStatus.CHECKED_PARTIAL)
    ]
    if len(checked) >= 3:
        evidence_cov = RiskLevel.LOW  # good coverage
    elif len(checked) >= 1:
        evidence_cov = RiskLevel.MODERATE
    else:
        evidence_cov = RiskLevel.INSUFFICIENT_DATA

    # --- Overall --------------------------------------------------------
    dims = [game_conflict, spelling, phonetic_risk, franchise_risk, discoverability]
    if RiskLevel.CRITICAL in dims:
        overall = RiskLevel.CRITICAL
    elif dims.count(RiskLevel.HIGH) >= 2:
        overall = RiskLevel.CRITICAL
    elif RiskLevel.HIGH in dims:
        overall = RiskLevel.HIGH
    elif dims.count(RiskLevel.MODERATE) >= 2:
        overall = RiskLevel.MODERATE
    elif RiskLevel.MODERATE in dims:
        overall = RiskLevel.MODERATE
    elif evidence_cov == RiskLevel.INSUFFICIENT_DATA:
        overall = RiskLevel.INSUFFICIENT_DATA
    else:
        overall = RiskLevel.LOW

    # --- Reasoning text --------------------------------------------------
    reasons: list[str] = []
    if exact:
        names = ", ".join(f"'{e.raw_title}' ({e.source_name})" for e in exact[:3])
        reasons.append(f"Exact title match found: {names}")
    if near:
        names = ", ".join(f"'{e.raw_title}'" for e in near[:3])
        reasons.append(f"Near-exact matches: {names}")
    if phonetic:
        names = ", ".join(f"'{e.raw_title}'" for e in phonetic[:3])
        reasons.append(f"Phonetically similar: {names}")
    if franchise_entries:
        reasons.append("Title matches an existing franchise/series")
    if not exact and not near:
        reasons.append(
            "No exact or near-exact game title conflicts found in checked sources"
        )
    reasons.append(f"Sources checked: {len(checked)}/{len(coverage)}")
    reasons.append("Trademark databases require manual verification")

    return RiskAssessment(
        game_title_conflict=game_conflict,
        spelling_visual=spelling,
        phonetic=phonetic_risk,
        franchise_association=franchise_risk,
        trademark_signals=trademark_risk,
        search_discoverability=discoverability,
        evidence_coverage=evidence_cov,
        overall=overall,
        reasoning=". ".join(reasons) + ".",
    )
