"""GOG.com catalog adapter — no API key required."""
from __future__ import annotations

from ..models import EvidenceRecord, EntityType
from .base import BaseAdapter


class GOGAdapter(BaseAdapter):
    """Query the public GOG catalog endpoint.

    ``catalog.gog.com/v1/catalog`` is unauthenticated.  Primarily
    DRM-free PC games (Windows, macOS, Linux).
    """

    name = "gog"
    base_url = "https://catalog.gog.com/v1/catalog"
    min_request_interval = 1.5

    def search(self, title: str) -> list[EvidenceRecord]:
        data = self._get(
            self.base_url,
            params={
                "query": title,
                "limit": 20,
                "countryCode": "US",
                "locale": "en-US",
                "currencyCode": "USD",
                "order": "desc:score",
            },
        )

        results: list[EvidenceRecord] = []
        for prod in data.get("products", []):
            slug = prod.get("slug", "")
            url = f"https://www.gog.com/en/game/{slug}" if slug else None
            devs = ", ".join(prod.get("developers", []))
            pubs = ", ".join(prod.get("publishers", []))
            rd = prod.get("releaseDate")
            if rd:
                rd = rd[:10]

            ptype = prod.get("productType", "game")
            entity = EntityType.RELEASED_GAME
            if ptype in ("dlc", "pack"):
                entity = EntityType.DLC_EXPANSION

            # Detect actual platforms from API response
            pf = prod.get("operatingSystems", [])
            platforms: list[str] = []
            if "windows" in pf:
                platforms.append("Windows")
            if "osx" in pf or "mac" in pf:
                platforms.append("macOS")
            if "linux" in pf:
                platforms.append("Linux")
            if not platforms:
                platforms = ["Windows"]  # fallback for older catalog entries

            results.append(
                EvidenceRecord(
                    source_name=self.name,
                    raw_title=prod.get("title", ""),
                    source_url=url,
                    entity_type=entity,
                    developer=devs or None,
                    publisher=pubs or None,
                    release_date=rd,
                    platforms=platforms,
                    status="released",
                )
            )
        return results
