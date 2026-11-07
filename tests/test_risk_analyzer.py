"""Unit tests for RiskAnalyzer."""
from scripts.models import (
    EvidenceRecord,
    MatchCategory,
    RiskLevel,
    SourceCoverage,
    SourceStatus,
)
from scripts.risk_analyzer import assess_risk
from scripts.manual_urls import generate_trademark_urls


def test_risk_critical_on_multiple_exact():
    evidence = [
        EvidenceRecord(
            source_name="steam",
            raw_title="Ironhold",
            match_category=MatchCategory.EXACT_MATCH,
        ),
        EvidenceRecord(
            source_name="itunes_appstore",
            raw_title="Ironhold",
            match_category=MatchCategory.EXACT_MATCH,
        ),
    ]
    cov = [
        SourceCoverage("steam", SourceStatus.CHECKED_OK, 1),
        SourceCoverage("itunes_appstore", SourceStatus.CHECKED_OK, 1),
        SourceCoverage("gog", SourceStatus.CHECKED_OK, 0),
    ]
    risk = assess_risk("Ironhold", evidence, cov)
    assert risk.overall == RiskLevel.CRITICAL
    assert risk.game_title_conflict == RiskLevel.CRITICAL


def test_risk_low_on_no_matches():
    evidence = []
    cov = [
        SourceCoverage("steam", SourceStatus.CHECKED_OK, 0),
        SourceCoverage("itunes_appstore", SourceStatus.CHECKED_OK, 0),
        SourceCoverage("gog", SourceStatus.CHECKED_OK, 0),
    ]
    risk = assess_risk("UniqueTitleXyZ", evidence, cov)
    assert risk.overall == RiskLevel.LOW
    assert risk.game_title_conflict == RiskLevel.LOW


# --- Acceptance Test 14 ---

def test_case_14_trademark_manual_verification_required():
    trademark_findings = generate_trademark_urls("Ironhold")
    assert len(trademark_findings) >= 4
    for tf in trademark_findings:
        assert tf.status == SourceStatus.MANUAL_REQUIRED
        assert tf.search_url.startswith("http")

    wipo = next(tf for tf in trademark_findings if "WIPO" in tf.database)
    assert "branddb.wipo.int" in wipo.search_url
    assert "Ironhold" in wipo.search_url
