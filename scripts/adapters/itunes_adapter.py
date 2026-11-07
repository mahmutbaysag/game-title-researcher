"""Apple App Store (iTunes Search API) adapter — official, no key required."""
from __future__ import annotations

from ..models import EvidenceRecord, EntityType
from .base import BaseAdapter


class ITunesAdapter(BaseAdapter):
    """Query the official iTunes Search API for iOS / iPadOS games.

    Documented at developer.apple.com.  No API key needed; ~20 req/min
    recommended.
    """

    name = "itunes_appstore"
    base_url = "https://itunes.apple.com/search"
    min_request_interval = 3.0

    def search(self, title: str) -> list[EvidenceRecord]:
        data = self._get(
            self.base_url,
            params={
                "term": title,
                "country": "us",
                "entity": "software",
                "limit": 50,
            },
        )

        results: list[EvidenceRecord] = []
        for item in data.get("results", []):
            # Keep only items with a game-related genre
            genres = [g.lower() for g in item.get("genres", [])]
            primary = (item.get("primaryGenreName") or "").lower()
            if not (any("game" in g for g in genres) or "game" in primary):
                continue

            platforms: list[str] = ["iOS"]
            devices = item.get("supportedDevices", [])
            if any("iPad" in d for d in devices):
                platforms.append("iPadOS")

            results.append(
                EvidenceRecord(
                    source_name=self.name,
                    raw_title=item.get("trackName", ""),
                    source_url=item.get("trackViewUrl"),
                    entity_type=EntityType.RELEASED_GAME,
                    developer=item.get("artistName"),
                    release_date=(item.get("releaseDate") or "")[:10],
                    platforms=platforms,
                    status="released",
                )
            )
        return results
