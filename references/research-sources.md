# Research Sources Guide

This document catalogs video game storefronts and trademark databases, documenting their access methods, limitations, and operational characteristics for title research.

---

## 1. Automated Sources (Zero Authentication Required)

### Steam Storefront Search
- **Endpoint:** `GET https://store.steampowered.com/api/storesearch/`
- **Parameters:** `term={title}&l=english&cc=US`
- **Authentication:** None required.
- **Coverage:** Active PC games, software, and DLC listed on Steam.
- **Output:** JSON list (`total`, `items` with `id`, `name`, `type`, `platforms`).
- **Rate Limit & Throttling:** Undocumented public store endpoint. Enforce at least 2.0 seconds between calls to prevent HTTP 429/403 throttling.
- **Limitation:** Does not return delisted, banned, or unlisted historical app IDs.

### Apple App Store (iTunes Search API)
- **Endpoint:** `GET https://itunes.apple.com/search`
- **Parameters:** `term={title}&country=us&entity=software&limit=50`
- **Authentication:** Official, documented public API. No key required.
- **Coverage:** iOS and iPadOS applications. Filtered by game genres (`primaryGenreName == "Games"` or `genreIds` matching game categories).
- **Rate Limit:** ~20 requests per minute recommended.
- **Limitation:** Mobile catalog only. Regional availability depends on country parameter.

### GOG.com Catalog API
- **Endpoint:** `GET https://catalog.gog.com/v1/catalog`
- **Parameters:** `query=like:{title}&limit=20&countryCode=US&locale=en-US&currencyCode=USD`
- **Authentication:** None required.
- **Coverage:** PC DRM-free catalog, classic retro titles, and modern indie releases.
- **Rate Limit:** Moderate. Enforce 1.5 seconds between requests.
- **Limitation:** Curated store catalog; smaller than Steam.

---

## 2. Storefronts Requiring Manual Verification

These platforms do not provide public, open, or unauthenticated search APIs. Automated scraping violates their terms of service and triggers anti-bot mechanisms (Cloudflare, Akamai, CAPTCHAs).

### PlayStation Store
- **Search URL:** `https://store.playstation.com/en-us/search/{title}`
- **Reason:** Requires session tokens (`npsso`) and rotating query hashes.

### Xbox / Microsoft Store
- **Search URL:** `https://www.xbox.com/en-US/search?q={title}`
- **Reason:** Internal APIs change frequently without notice.

### Nintendo eShop
- **Search URL:** `https://www.nintendo.com/us/search/#q={title}&cat=games`
- **Reason:** Regionally fragmented architectures (Algolia in US, Solr in Europe).

### itch.io
- **Search URL:** `https://itch.io/search?q={title}`
- **Reason:** Official API is developer-account only; no public catalog search API.

### Epic Games Store
- **Search URL:** `https://store.epicgames.com/en-US/browse?q={title}&sortBy=relevancy`
- **Reason:** GraphQL backend is unofficial and subject to anti-bot throttling.

### Google Play Store
- **Search URL:** `https://play.google.com/store/search?q={title}&c=apps`
- **Reason:** Google Play Developer API manages owned apps only; web search enforces aggressive anti-bot challenges.

---

## 3. Trademark Databases

| Database | Jurisdiction | Access Method | Notes |
|:---|:---|:---|:---|
| **WIPO Global Brand DB** | International (Madrid System) | Pre-filled JSON query URL | Clickable link directly executes query |
| **USPTO Trademark Search** | United States | Manual entry | SPA architecture prevents pre-filled URLs |
| **EUIPO eSearch** | European Union | Manual entry | Portal search for EUTMs |
| **TMview** | Global aggregation | Manual entry | Multi-office trademark aggregator |
| **TÜRKPATENT** | Turkey | Manual entry | Turkish national trademark search |
