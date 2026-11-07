"""Evidence storage and deduplication."""
from __future__ import annotations

from .models import EvidenceRecord, MatchCategory
from .title_matcher import normalize_title


class EvidenceStore:
    """Collects, deduplicates, and retrieves evidence records."""

    def __init__(self) -> None:
        self._records: list[EvidenceRecord] = []
        self._seen: set[str] = set()

    # ------------------------------------------------------------------
    def _dedup_key(self, record: EvidenceRecord) -> str:
        norm = normalize_title(record.raw_title)
        return f"{norm}|{record.source_name}"

    # ------------------------------------------------------------------
    def add(self, record: EvidenceRecord) -> None:
        """Add a record, skipping same-title duplicates from the same source."""
        key = self._dedup_key(record)
        if key in self._seen:
            return
        self._seen.add(key)
        if not record.normalized_title:
            record.normalized_title = normalize_title(record.raw_title)
        self._records.append(record)

    def add_many(self, records: list[EvidenceRecord]) -> None:
        for r in records:
            self.add(r)

    # ------------------------------------------------------------------
    def get_all(self) -> list[EvidenceRecord]:
        return list(self._records)

    def get_by_category(self, category: MatchCategory) -> list[EvidenceRecord]:
        return [r for r in self._records if r.match_category == category]

    def get_exact_matches(self) -> list[EvidenceRecord]:
        return self.get_by_category(MatchCategory.EXACT_MATCH)

    def get_similar_matches(self) -> list[EvidenceRecord]:
        """All non-exact, non-unrelated matches."""
        return [
            r
            for r in self._records
            if r.match_category
            not in (MatchCategory.EXACT_MATCH, MatchCategory.UNRELATED)
        ]

    # ------------------------------------------------------------------
    @property
    def total_count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records.clear()
        self._seen.clear()
