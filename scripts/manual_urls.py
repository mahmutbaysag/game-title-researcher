"""Generate manual verification URLs for stores and trademark databases."""
from __future__ import annotations

import urllib.parse

from .models import ManualCheckURL, TrademarkFinding, SourceStatus


def generate_store_urls(title: str) -> list[ManualCheckURL]:
    """Generate clickable search URLs for stores without free API access."""
    enc = urllib.parse.quote_plus(title)
    return [
        ManualCheckURL(
            source_name="PlayStation Store",
            url=f"https://store.playstation.com/en-us/search/{enc}",
            instructions="Search and check for matching game titles",
        ),
        ManualCheckURL(
            source_name="Xbox / Microsoft Store",
            url=f"https://www.xbox.com/en-US/search?q={enc}",
            instructions="Search for matching game titles on Xbox",
        ),
        ManualCheckURL(
            source_name="Nintendo eShop",
            url=f"https://www.nintendo.com/us/search/#q={enc}&cat=games",
            instructions="Search Nintendo's catalog for matching titles",
        ),
        ManualCheckURL(
            source_name="Google Play",
            url=f"https://play.google.com/store/search?q={enc}&c=apps",
            instructions="Search for matching game apps on Google Play",
        ),
        ManualCheckURL(
            source_name="itch.io",
            url=f"https://itch.io/search?q={enc}",
            instructions="Search indie game platform for matching titles",
        ),
        ManualCheckURL(
            source_name="Epic Games Store",
            url=f"https://store.epicgames.com/en-US/browse?q={enc}&sortBy=relevancy",
            instructions="Search Epic Games Store for matching titles",
        ),
    ]


def generate_trademark_urls(title: str) -> list[TrademarkFinding]:
    """Generate trademark database search URLs for manual verification."""
    wipo_q = urllib.parse.quote(
        '{"searches":[{"te":"' + title + '","fi":"BRAND"}]}'
    )
    return [
        TrademarkFinding(
            database="WIPO Global Brand Database",
            search_url=f"https://branddb.wipo.int/en/?q={wipo_q}",
            status=SourceStatus.MANUAL_REQUIRED,
            notes="Filter by Nice Classes 9, 28, 41, 42 for games.",
        ),
        TrademarkFinding(
            database="USPTO Trademark Search",
            search_url="https://tmsearch.uspto.gov/",
            status=SourceStatus.MANUAL_REQUIRED,
            notes=f"Search for '{title}'. Check Nice Classes 009, 028, 041, 042.",
        ),
        TrademarkFinding(
            database="EUIPO eSearch (EU)",
            search_url="https://euipo.europa.eu/eSearch/",
            status=SourceStatus.MANUAL_REQUIRED,
            notes=f"Search for '{title}' in EU trademark database.",
        ),
        TrademarkFinding(
            database="TMview (Global)",
            search_url="https://www.tmdn.org/tmview/",
            status=SourceStatus.MANUAL_REQUIRED,
            notes=f"Search for '{title}' across multiple national offices.",
        ),
        TrademarkFinding(
            database="TÜRKPATENT",
            search_url="https://www.turkpatent.gov.tr",
            status=SourceStatus.MANUAL_REQUIRED,
            notes=f"Search for '{title}'. Also covered in WIPO for international marks.",
        ),
    ]
