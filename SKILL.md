---
name: game-title-researcher
description: Research video game title availability, find naming conflicts across stores and databases, and generate pre-researched alternative titles for game developers.
license: MIT
compatibility: Python 3.10+, httpx, rapidfuzz, jellyfish
metadata:
  version: "1.1.0"
  authors:
    - "Mahmut Baysağ (@mahmutbaysag)"
    - "Antigravity (Google DeepMind)"
---

# Game Title Researcher

AI agent skill for video game developers to check title conflicts, explore naming variations, and evaluate trademark warning signs before committing to a game title.

## Core Principle
**Research first; never present an unverified title as available or legally safe.**

## When to Use
- Check single title: "Is *Ironhold* already used by a game?"
- Deep investigation: "Investigate *Dead End* thoroughly, including similar titles and trademarks."
- Name generation: "Suggest names for a co-op zombie FPS and verify each candidate."
- Compare titles: "Compare *Ironhold*, *Dead End*, and *Last Stand*."

## Quick Start (Automated Script Mode)
If Python environment is available:
```bash
pip install -r requirements.txt
python -m scripts check "Proposed Title"
python -m scripts compare "Title A" "Title B"
```

## Research Modes

### 1. Check Mode
1. Normalize query title (lowercase, strip diacritics, strip punctuation).
2. Query automated keyless stores:
   - **Steam Store Search** (PC, Steam storefront)
   - **Apple App Store via iTunes Search API** (iOS/iPadOS games)
   - **GOG Catalog** (PC DRM-free games)
3. Compare candidate matches using multi-metric matching:
   - Exact normalized (`EXACT_MATCH`)
   - Levenshtein distance (`NEAR_EXACT`, typo tolerance)
   - Soundex & Metaphone (`PHONETIC_MATCH`)
   - Token set & sort ratio (`STRUCTURAL_MATCH`)
   - Non-generic word overlap (`PARTIAL_MATCH`)
4. Generate manual verification links for storefronts without public open APIs:
   - PlayStation Store, Xbox / Microsoft Store, Nintendo eShop, itch.io, Epic Games Store, Google Play
5. Generate trademark search links (WIPO pre-filled JSON query, USPTO, EUIPO, TMview, TÜRKPATENT).
6. Calculate multi-dimensional risk rating (LOW, MODERATE, HIGH, CRITICAL, INSUFFICIENT_DATA).
7. Format standard Markdown report.

### 2. Generate and Verify Mode
When developer requests title recommendations:
1. Extract concept, genre, theme, mechanics, and tone.
2. Brainstorm diverse title candidates across different styles (short, atmospheric, coined, two-word).
3. Filter out candidates containing common generic single-word tropes.
4. Run automated check pipeline on shortlist candidates.
5. Rank and present only verified candidates with their risk indicators and findings.

## Store and Source Coverage
- **Automated (No API Key Required):**
  - Steam (`store.steampowered.com/api/storesearch/`)
  - Apple App Store (`itunes.apple.com/search`)
  - GOG (`catalog.gog.com/v1/catalog`)
- **Manual Verification Required (Links provided):**
  - PlayStation Store
  - Xbox Store
  - Nintendo eShop
  - itch.io
  - Epic Games Store
  - Google Play Store
  - WIPO Global Brand Database (pre-filled query link)
  - USPTO Trademark Search
  - EUIPO eSearch
  - TMview
  - TÜRKPATENT

## Standard Report Structure
Every report must follow sections A through H:
- **A. Summary:** Proposed title, timestamp, mode, overall risk level.
- **B. Research Coverage:** Status table of checked, partially checked, and manual sources.
- **C. Exact Matches:** Confirmed identical game titles with platforms, status, and source link.
- **D. Similar Matches:** Grouped by match category (Near Exact, Phonetic, Structural, Partial).
- **E. Trademark & Brand Findings:** Pre-filled database links, relevant Nice classes (9, 28, 41, 42), and disclaimer.
- **F. Risk Assessment:** 7-dimension breakdown and concise reasoning.
- **G. Alternatives:** Researched alternatives if requested.
- **H. Recommendation:** Practical next steps and disclaimer.

## Important Limitations & Disclaimers
1. Preliminary research only — **not legal advice**.
2. Does not bypass anti-bot, CAPTCHAs, or terms of service.
3. Unlisted, removed, or obscure cancelled games might not appear in public active store listings.
4. Trademark clearance requires professional legal counsel before commercial launch.

## References
- Matching Methodology: [matching-methodology.md](./references/matching-methodology.md)
- Research Sources: [research-sources.md](./references/research-sources.md)
- Trademark Research: [trademark-research.md](./references/trademark-research.md)
- Naming Guidelines: [naming-guidelines.md](./references/naming-guidelines.md)
- Report Template: [report-template.md](./references/report-template.md)
