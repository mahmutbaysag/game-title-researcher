"""Unit tests for HTTP adapters with mocked responses."""
import pytest
import respx
import httpx
from scripts.adapters.steam_adapter import SteamAdapter
from scripts.adapters.itunes_adapter import ITunesAdapter
from scripts.adapters.gog_adapter import GOGAdapter
from scripts.adapters.base import AdapterError, RateLimitError, SourceUnavailableError


@respx.mock
def test_steam_adapter_success():
    respx.get("https://store.steampowered.com/api/storesearch/").respond(
        status_code=200,
        json={
            "total": 1,
            "items": [
                {
                    "id": 12345,
                    "name": "Ironhold",
                    "type": "app",
                    "platforms": {"windows": True, "mac": False, "linux": True},
                }
            ],
        },
    )
    with SteamAdapter() as adapter:
        adapter.min_request_interval = 0.0  # Fast tests
        results = adapter.search("Ironhold")
        assert len(results) == 1
        assert results[0].raw_title == "Ironhold"
        assert "Windows" in results[0].platforms
        assert "Linux" in results[0].platforms


# --- Acceptance Tests 11-13 ---

@respx.mock
def test_case_11_source_unavailable_403():
    respx.get("https://store.steampowered.com/api/storesearch/").respond(
        status_code=403
    )
    with SteamAdapter() as adapter:
        adapter.min_request_interval = 0.0
        with pytest.raises(SourceUnavailableError):
            adapter.search("Ironhold")


@respx.mock
def test_case_12_search_returns_no_results():
    respx.get("https://store.steampowered.com/api/storesearch/").respond(
        status_code=200,
        json={"total": 0, "items": []},
    )
    with SteamAdapter() as adapter:
        adapter.min_request_interval = 0.0
        results = adapter.search("NonExistentUniqueGameTitle12345")
        assert len(results) == 0


@respx.mock
def test_case_13_rate_limit_error_429():
    respx.get("https://store.steampowered.com/api/storesearch/").respond(
        status_code=429
    )
    with SteamAdapter() as adapter:
        adapter.min_request_interval = 0.0
        with pytest.raises(RateLimitError):
            adapter.search("Ironhold")


@respx.mock
def test_itunes_adapter_game_filter():
    respx.get("https://itunes.apple.com/search").respond(
        status_code=200,
        json={
            "resultCount": 2,
            "results": [
                {
                    "trackName": "Ironhold Strategy Game",
                    "primaryGenreName": "Games",
                    "genres": ["Games", "Strategy"],
                    "trackViewUrl": "https://apple.com/app/1",
                    "artistName": "IndieDev",
                    "supportedDevices": ["iPhone", "iPad"],
                },
                {
                    "trackName": "Ironhold Productivity Utility",
                    "primaryGenreName": "Productivity",
                    "genres": ["Productivity"],
                },
            ],
        },
    )
    with ITunesAdapter() as adapter:
        adapter.min_request_interval = 0.0
        results = adapter.search("Ironhold")
        assert len(results) == 1
        assert results[0].raw_title == "Ironhold Strategy Game"
        assert "iOS" in results[0].platforms
        assert "iPadOS" in results[0].platforms


@respx.mock
def test_gog_adapter_success():
    respx.get("https://catalog.gog.com/v1/catalog").respond(
        status_code=200,
        json={
            "products": [
                {
                    "id": 9999,
                    "title": "Ironhold: Chronicles",
                    "slug": "ironhold_chronicles",
                    "developers": ["GOGDev"],
                    "publishers": ["GOGPub"],
                    "releaseDate": "2024-05-10T12:00:00Z",
                    "productType": "game",
                    "operatingSystems": ["windows", "linux", "osx"],
                }
            ]
        },
    )
    with GOGAdapter() as adapter:
        adapter.min_request_interval = 0.0
        results = adapter.search("Ironhold")
        assert len(results) == 1
        assert results[0].raw_title == "Ironhold: Chronicles"
        assert "Windows" in results[0].platforms
        assert "Linux" in results[0].platforms
        assert "macOS" in results[0].platforms
        assert results[0].release_date == "2024-05-10"

