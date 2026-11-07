"""Base adapter for source queries."""
from __future__ import annotations

import time
from abc import ABC, abstractmethod

import httpx

from ..models import EvidenceRecord


class AdapterError(Exception):
    """Base error for adapter failures."""


class SourceUnavailableError(AdapterError):
    """Source cannot be reached or credentials missing."""


class RateLimitError(AdapterError):
    """Source rate limit exceeded."""


class BaseAdapter(ABC):
    """Abstract base for all source adapters.

    Subclasses set ``name``, ``base_url``, and optionally override
    ``timeout`` / ``min_request_interval``.
    """

    name: str = "unknown"
    base_url: str = ""
    timeout: float = 15.0
    min_request_interval: float = 1.0  # seconds between requests

    def __init__(self) -> None:
        self._last_request_time: float = 0.0
        self._client = httpx.Client(
            timeout=httpx.Timeout(self.timeout),
            follow_redirects=True,
            headers={"User-Agent": "GameTitleResearcher/1.0 (research tool)"},
        )

    # ------------------------------------------------------------------ #

    def _throttle(self) -> None:
        elapsed = time.time() - self._last_request_time
        wait = self.min_request_interval - elapsed
        if wait > 0:
            time.sleep(wait)
        self._last_request_time = time.time()

    def _get(self, url: str, params: dict | None = None) -> dict:
        """Make a throttled GET request and return parsed JSON."""
        self._throttle()

        try:
            resp = self._client.get(url, params=params)
        except httpx.TimeoutException:
            raise AdapterError(f"{self.name}: request timed out")
        except httpx.RequestError as exc:
            raise AdapterError(f"{self.name}: connection error: {exc}")

        if resp.status_code == 429:
            raise RateLimitError(f"{self.name}: rate limit exceeded (429)")
        if resp.status_code == 403:
            raise SourceUnavailableError(f"{self.name}: access forbidden (403)")

        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise AdapterError(
                f"{self.name}: HTTP {exc.response.status_code}"
            )

        try:
            return resp.json()
        except Exception:
            raise AdapterError(f"{self.name}: invalid JSON response")

    # ------------------------------------------------------------------ #

    @abstractmethod
    def search(self, title: str) -> list[EvidenceRecord]:
        """Search for a game title. Returns evidence records."""
        ...

    # ------------------------------------------------------------------ #

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
