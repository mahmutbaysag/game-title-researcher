"""Data models for Game Title Researcher."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class MatchCategory(str, Enum):
    """How a discovered title relates to the query."""

    EXACT_MATCH = "exact_match"
    NEAR_EXACT = "near_exact"
    PHONETIC_MATCH = "phonetic_match"
    STRUCTURAL_MATCH = "structural_match"
    SEMANTIC_MATCH = "semantic_match"
    PARTIAL_MATCH = "partial_match"
    UNRELATED = "unrelated"


class EntityType(str, Enum):
    """What kind of entity a discovered result represents."""

    RELEASED_GAME = "released_game"
    ANNOUNCED_GAME = "announced_game"
    EARLY_ACCESS = "early_access"
    CANCELLED_GAME = "cancelled_game"
    DLC_EXPANSION = "dlc_expansion"
    FRANCHISE_SERIES = "franchise_series"
    NON_GAME_BRAND = "non_game_brand"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    """Risk assessment level."""

    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class SourceStatus(str, Enum):
    """Status of a source check."""

    CHECKED_OK = "checked_successfully"
    CHECKED_PARTIAL = "checked_partially"
    NOT_CHECKED = "not_checked"
    MANUAL_REQUIRED = "manual_verification_required"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class EvidenceRecord:
    """A single piece of evidence from a source."""

    source_name: str
    raw_title: str
    normalized_title: str = ""
    source_url: str | None = None
    retrieved_at: datetime = field(default_factory=_utcnow)
    entity_type: EntityType = EntityType.UNKNOWN
    match_category: MatchCategory = MatchCategory.UNRELATED
    similarity_score: float = 0.0
    similarity_details: dict = field(default_factory=dict)
    developer: str | None = None
    publisher: str | None = None
    release_date: str | None = None
    platforms: list[str] = field(default_factory=list)
    status: str | None = None
    notes: str | None = None


@dataclass
class SourceCoverage:
    """Coverage status for a single source."""

    source_name: str
    status: SourceStatus
    result_count: int = 0
    notes: str | None = None


@dataclass
class TrademarkFinding:
    """Trademark database search result placeholder."""

    database: str
    search_url: str
    status: SourceStatus = SourceStatus.MANUAL_REQUIRED
    notes: str | None = None


@dataclass
class ManualCheckURL:
    """A URL the user should check manually."""

    source_name: str
    url: str
    instructions: str | None = None


@dataclass
class RiskAssessment:
    """Multi-dimensional risk assessment."""

    game_title_conflict: RiskLevel = RiskLevel.INSUFFICIENT_DATA
    spelling_visual: RiskLevel = RiskLevel.INSUFFICIENT_DATA
    phonetic: RiskLevel = RiskLevel.INSUFFICIENT_DATA
    franchise_association: RiskLevel = RiskLevel.INSUFFICIENT_DATA
    trademark_signals: RiskLevel = RiskLevel.INSUFFICIENT_DATA
    search_discoverability: RiskLevel = RiskLevel.INSUFFICIENT_DATA
    evidence_coverage: RiskLevel = RiskLevel.INSUFFICIENT_DATA
    overall: RiskLevel = RiskLevel.INSUFFICIENT_DATA
    reasoning: str = ""


@dataclass
class AlternativeCandidate:
    """A generated alternative title candidate."""

    name: str
    rationale: str = ""
    match_findings: list[EvidenceRecord] = field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.INSUFFICIENT_DATA
    coverage: list[SourceCoverage] = field(default_factory=list)


@dataclass
class ResearchReport:
    """Complete research report."""

    proposed_title: str
    research_date: datetime = field(default_factory=_utcnow)
    mode: str = "check"
    summary: str = ""
    coverage: list[SourceCoverage] = field(default_factory=list)
    exact_matches: list[EvidenceRecord] = field(default_factory=list)
    similar_matches: list[EvidenceRecord] = field(default_factory=list)
    trademark_findings: list[TrademarkFinding] = field(default_factory=list)
    risk_assessment: RiskAssessment = field(default_factory=RiskAssessment)
    alternatives: list[AlternativeCandidate] = field(default_factory=list)
    recommendation: str = ""
    manual_check_urls: list[ManualCheckURL] = field(default_factory=list)
