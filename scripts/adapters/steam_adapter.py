"""Steam Store Search adapter — no API key required."""
from __future__ import annotations

from ..models import EvidenceRecord, EntityType
from .base import BaseAdapter


class SteamAdapter(BaseAdapter):
    """Query the undocumented Steam storefront search endpoint.

    ``store.steampowered.com/api/storesearch/`` returns JSON, needs no key,
    but is rate-sensitive — keep ≥ 2 s between requests.
    """

    name = "steam"
    base_url = "https://store.steampowered.com/api/storesearch/"
    min_request_interval = 2.0

    def search(self, title: str) -> list[EvidenceRecord]:
        data = self._get(
            self.base_url,
            params={"term": title, "l": "english", "cc": "US"},
        )

        results: list[EvidenceRecord] = []
        for item in data.get("items", []):
            platforms: list[str] = []
            pf = item.get("platforms", {})
            if pf.get("windows"):
                platforms.append("Windows")
            if pf.get("mac"):
                platforms.append("macOS")
            if pf.get("linux"):
                platforms.append("Linux")

            entity = EntityType.RELEASED_GAME
            if item.get("type") == "dlc":
                entity = EntityType.DLC_EXPANSION

            results.append(
                EvidenceRecord(
                    source_name=self.name,
                    raw_title=item.get("name", ""),
                    source_url=f"https://store.steampowered.com/app/{item['id']}",
                    entity_type=entity,
                    platforms=platforms,
                    status="released",
                )
            )
        return results
