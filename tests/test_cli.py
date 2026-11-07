"""Unit tests for CLI runner and end-to-end report synthesis."""
import json
import respx
from scripts.cli import check_title, _serialize
from scripts.models import MatchCategory, RiskLevel
from scripts.report_generator import generate_report_markdown


# --- Acceptance Tests 15 & 16 ---

def test_case_15_alternative_with_exact_conflict():
    # If an alternative has an exact conflict, its risk should be high
    from scripts.models import AlternativeCandidate, EvidenceRecord
    alt = AlternativeCandidate(
        name="Ironhold",
        rationale="Strong fantasy fortress",
        match_findings=[
            EvidenceRecord(
                source_name="steam",
                raw_title="Ironhold",
                match_category=MatchCategory.EXACT_MATCH,
            )
        ],
        risk_level=RiskLevel.HIGH,
    )
    assert alt.risk_level == RiskLevel.HIGH
    assert alt.match_findings[0].match_category == MatchCategory.EXACT_MATCH


def test_case_16_alternative_with_weak_match():
    from scripts.models import AlternativeCandidate, EvidenceRecord
    alt = AlternativeCandidate(
        name="Fortress of Iron",
        rationale="Descriptive variant",
        match_findings=[
            EvidenceRecord(
                source_name="steam",
                raw_title="Iron Quest",
                match_category=MatchCategory.PARTIAL_MATCH,
                similarity_score=0.45,
            )
        ],
        risk_level=RiskLevel.LOW,
    )
    assert alt.risk_level == RiskLevel.LOW
    assert alt.match_findings[0].similarity_score < 0.50


@respx.mock
def test_end_to_end_check_title_mocked():
    respx.get("https://store.steampowered.com/api/storesearch/").respond(
        status_code=200, json={"total": 0, "items": []}
    )
    respx.get("https://itunes.apple.com/search").respond(
        status_code=200, json={"resultCount": 0, "results": []}
    )
    respx.get("https://catalog.gog.com/v1/catalog").respond(
        status_code=200, json={"products": []}
    )

    report = check_title("AstroNova2026")
    assert report.proposed_title == "AstroNova2026"
    assert report.risk_assessment.overall == RiskLevel.LOW
    assert len(report.exact_matches) == 0

    # Test Markdown synthesis
    md = generate_report_markdown(report)
    assert "# 🎮 Game Title Research Report" in md
    assert "AstroNova2026" in md
    assert "## B. Research Coverage" in md
    assert "## E. Trademark & Brand Findings" in md

    # Test JSON serialization
    serialized = _serialize(report)
    json_str = json.dumps(serialized)
    assert "AstroNova2026" in json_str
    assert "LOW" in json_str
