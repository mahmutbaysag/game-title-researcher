"""Source adapters for querying game databases and storefronts."""
from .steam_adapter import SteamAdapter
from .itunes_adapter import ITunesAdapter
from .gog_adapter import GOGAdapter

__all__ = ["SteamAdapter", "ITunesAdapter", "GOGAdapter"]
