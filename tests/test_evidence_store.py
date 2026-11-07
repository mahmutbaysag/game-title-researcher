"""Unit tests for EvidenceStore storage and deduplication."""
from scripts.models import EvidenceRecord, EntityType, MatchCategory
from scripts.evidence_store import EvidenceStore


def test_evidence_deduplication():
    store = EvidenceStore()
    rec1 = EvidenceRecord(
        source_name="steam",
        raw_title="Ironhold",
        entity_type=EntityType.RELEASED_GAME,
    )
    rec2 = EvidenceRecord(
        source_name="steam",
        raw_title="ironhold",  # Same title normalized
        entity_type=EntityType.RELEASED_GAME,
    )
    store.add(rec1)
    store.add(rec2)
    assert store.total_count == 1


# --- Acceptance Tests 7-10 ---

def test_case_7_non_game_brand_representation():
    store = EvidenceStore()
    rec = EvidenceRecord(
        source_name="web",
        raw_title="Ironhold (Novel)",
        entity_type=EntityType.NON_GAME_BRAND,
        match_category=MatchCategory.PARTIAL_MATCH,
    )
    store.add(rec)
    records = store.get_all()
    assert records[0].entity_type == EntityType.NON_GAME_BRAND


def test_case_8_old_obscure_game():
    store = EvidenceStore()
    rec = EvidenceRecord(
        source_name="gog",
        raw_title="Ironhold 1994",
        entity_type=EntityType.RELEASED_GAME,
        release_date="1994-05-12",
        status="released",
    )
    store.add(rec)
    assert len(store.get_all()) == 1
    assert store.get_all()[0].release_date == "1994-05-12"


def test_case_9_upcoming_or_cancelled_game():
    store = EvidenceStore()
    rec_cancelled = EvidenceRecord(
        source_name="web",
        raw_title="Ironhold Online",
        entity_type=EntityType.CANCELLED_GAME,
        status="cancelled",
    )
    rec_announced = EvidenceRecord(
        source_name="steam",
        raw_title="Ironhold Reborn",
        entity_type=EntityType.ANNOUNCED_GAME,
        status="announced",
    )
    store.add(rec_cancelled)
    store.add(rec_announced)
    assert store.total_count == 2
    types = [r.entity_type for r in store.get_all()]
    assert EntityType.CANCELLED_GAME in types
    assert EntityType.ANNOUNCED_GAME in types


def test_case_10_multiple_games_same_title():
    store = EvidenceStore()
    rec_pc = EvidenceRecord(
        source_name="steam",
        raw_title="Prey",
        match_category=MatchCategory.EXACT_MATCH,
        developer="Arkane Studios",
        release_date="2017",
    )
    rec_mobile = EvidenceRecord(
        source_name="itunes_appstore",
        raw_title="Prey",
        match_category=MatchCategory.EXACT_MATCH,
        developer="Other Studio",
        release_date="2021",
    )
    # Different sources with same title should both be recorded
    store.add(rec_pc)
    store.add(rec_mobile)
    exacts = store.get_exact_matches()
    assert len(exacts) == 2
