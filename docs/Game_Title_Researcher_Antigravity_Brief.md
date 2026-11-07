# Game Title Researcher
## Antigravity Project Brief & Implementation Specification

**Document purpose:** Give this document to Google Antigravity as the project brief. Antigravity should use it to plan, design, implement, and test a portable Agent Skill that researches video game titles and helps developers find distinctive alternatives.

**Working project name:** `game-title-researcher`  
**Primary deliverable:** A reusable Agent Skills-compatible skill folder  
**Secondary deliverable:** Optional research scripts and integrations that make the skill capable of gathering and comparing evidence  
**Primary principle:** Research first; never present an unverified name as available or legally safe.

---

# 1. Project goal

Build an AI agent skill for video game developers who want to:

1. Check whether a proposed game title has already been used.
2. Find exact matches and similar titles, including older, indie, mobile, unreleased, cancelled, and region-specific games where discoverable.
3. Assess the likelihood that players could confuse the proposed title with an existing game, franchise, studio, or brand.
4. Conduct preliminary trademark research in relevant jurisdictions.
5. Generate alternative titles based on a game's concept, genre, setting, themes, mechanics, and tone.
6. Research every generated alternative before recommending it.
7. Produce a clear, source-backed report with research coverage, limitations, and next steps.

This is not merely a game-name generator. Its core value is a repeatable research and verification workflow.

## Main user scenarios

- **Check a name:** “Is *Ironhold* already used by a video game?”
- **Deep research:** “Investigate *Dead End* thoroughly, including similar games and trademarks.”
- **Generate and verify:** “Suggest names for a co-op zombie survival FPS set in a prison, then research each candidate.”
- **Compare names:** “Compare *Ironhold*, *Dead End*, and *Last Stand*.”
- **Explore variations:** “Keep the idea behind *Ironhold*, but suggest more distinctive alternatives.”

The skill should infer the appropriate mode from the request. Ask a question only when an essential detail is missing. For name generation, useful optional context includes genre, setting, story, gameplay, tone, target platforms, languages/markets, and preferred naming style.

---

# 2. Platform and compatibility requirements

The skill must target the open **Agent Skills** format and remain as portable as reasonably possible across compatible agent products.

Use the official Agent Skills specification as the source of truth:
- https://agentskills.io/specification
- https://agentskills.io

Expected structure:

```text
game-title-researcher/
├── SKILL.md
├── references/
│   ├── research-sources.md
│   ├── matching-methodology.md
│   ├── trademark-research.md
│   ├── naming-guidelines.md
│   └── report-template.md
├── scripts/
│   ├── ... optional research and analysis scripts
├── tests/
│   ├── ... test cases and fixtures
├── config/
│   └── sources.yaml
├── .env.example
├── .gitignore
└── README.md
```

Do not assume every Agent Skills host supports the same tools, network access, shell execution, Python packages, or environment-variable handling. The skill instructions must explain how to adapt to the host's available capabilities.

The `SKILL.md` should be concise enough to be usable as an agent instruction file. Put detailed methodology in `references/` and executable logic in `scripts/`.

---

# 3. Research strategy and source hierarchy

Research must use multiple independent source categories. No single database is complete.

## 3.1 Video game databases and storefronts

Investigate the availability, terms, and official access methods of these sources:

- Steam Store / Steam Web API
- IGDB
- MobyGames
- RAWG
- Giant Bomb
- itch.io
- Epic Games Store
- GOG
- Google Play
- Apple App Store
- PlayStation Store
- Xbox Store
- Nintendo eShop

For every source, document:

- What data it can provide.
- Whether an official API exists.
- Whether API access requires an account, approval, or credentials.
- Rate limits and relevant terms of use.
- Whether title search is supported.
- Whether historical, delisted, unreleased, or cancelled games are represented.
- Whether the source can be queried automatically in this project.
- The fallback method when automated access is unavailable.

Do not claim that a source was checked if it was not actually queried.

### Important source-specific caution

- **IGDB:** Investigate its current official API documentation and authentication requirements. Do not assume endpoints, fields, quotas, or access permissions without verifying them.
- **Steam:** Distinguish official Steam APIs from public Store search pages and third-party endpoints. Verify current documentation and permitted use.
- **itch.io:** Check current official API/documentation and terms before implementing automated access.
- **Other storefronts:** Do not assume they provide public APIs or permit scraping.

Prefer official APIs and documented access methods. If a source has no permitted automated method, provide a source link and mark it as requiring manual verification.

## 3.2 General web research

Search the open web for:

- Exact title in quotation marks.
- Title + “game” / “video game”.
- Title + “Steam”.
- Title + “indie game”.
- Title + developer / publisher.
- Title + release date.
- Title + trademark / studio / franchise.
- Common spelling, punctuation, spacing, plural, and word-order variations.
- Relevant translations and transliterations where appropriate.

Useful evidence can include:

- Developer and publisher websites.
- Game announcements and press releases.
- Gaming news and review sites.
- Store pages.
- Crowdfunding pages.
- Historical game catalogues.
- Archived announcements or project pages, when lawfully accessible.

Search engine snippets are discovery evidence, not always sufficient proof. Open and inspect important results whenever possible.

## 3.3 Trademark and brand research

Investigate official databases and document their current search capabilities:

- WIPO Global Brand Database: https://branddb.wipo.int/
- EUIPO: https://euipo.europa.eu/
- TMview: https://www.tmdn.org/tmview/
- USPTO Trademark Search: https://www.uspto.gov/trademarks/search
- TÜRKPATENT: https://www.turkpatent.gov.tr/

For each relevant record, capture only information that is actually available and verified, such as:

- Mark text.
- Owner/applicant.
- Jurisdiction.
- Application or registration number.
- Filing/registration status.
- Relevant goods/services classes.
- Source URL and access date.

Consider relevant goods and services, including software and entertainment-related categories. Do not assume one class alone determines whether a title can be used.

**Legal limitation:** This tool provides preliminary research, not legal advice, a legal opinion, or a guarantee of availability. Trademark rights can depend on jurisdiction, goods/services, use, reputation, and other facts. Encourage professional legal review before commercial launch or substantial investment.

**Access limitation:** Do not bypass CAPTCHAs, authentication, rate limits, anti-bot systems, or terms of service. Do not implement prohibited scraping. If automated access is not clearly permitted, provide a direct search link and mark the result as “manual verification required.”

## 3.4 Domains and social handles (optional)

If the user requests it or it materially helps brand planning, check:

- Relevant domain names.
- Major social media handles.
- Studio/brand name conflicts.

Do not let domain or handle availability determine whether a game title is safe. Keep these findings separate from game-title and trademark findings. Use permitted lookup methods and state the date.

---

# 4. Matching and similarity methodology

The system must detect more than exact string equality.

## 4.1 Normalize titles

Create normalized forms while preserving the original title:

- Case folding.
- Unicode normalization.
- Leading/trailing and repeated whitespace removal.
- Punctuation and separator variants.
- Hyphen/space/concatenation variants.
- Apostrophe and diacritic variants where relevant.
- Singular/plural and common suffix variants where useful.

Do not destroy meaningful word boundaries or discard the original spelling.

## 4.2 Search variant types

For a title such as `Ironhold`, investigate examples such as:

- Exact: `Ironhold`
- Spacing: `Iron Hold`
- Hyphenation: `Iron-Hold`
- Plural/suffix: `Ironholds`
- Typographical: `Ironhould`
- Phonetic: `Ironholt`
- Word order or article: `The Iron Hold`
- Significant partial matches: `Iron ...`
- Semantic/conceptual matches: related phrases such as `Steel Fortress`

Semantic similarity is a discovery aid, not proof of a naming conflict. A shared generic word should not automatically produce a high-risk result.

## 4.3 Comparison techniques

Use a combination of:

- Exact normalized matching.
- Levenshtein or Damerau-Levenshtein distance.
- Jaro-Winkler or another suitable string similarity metric.
- Token overlap and token-order comparison.
- Phonetic comparison where language support is appropriate.
- Optional multilingual semantic similarity.

Document the selected algorithms, thresholds, and known weaknesses. Avoid pretending a numerical similarity score is an objective legal-risk score.

## 4.4 Match categories

Classify each discovered result as one of:

- `EXACT_MATCH` — identical title after safe normalization.
- `NEAR_EXACT` — very small spelling, punctuation, or spacing difference.
- `PHONETIC_MATCH` — similar pronunciation.
- `STRUCTURAL_MATCH` — similar wording or construction.
- `SEMANTIC_MATCH` — similar meaning or concept.
- `PARTIAL_MATCH` — shares a significant title component.
- `UNRELATED` — superficial similarity only.

Also classify the discovered item's relationship to video games:

- Released game.
- Announced / upcoming game.
- Early access / in-development project.
- Cancelled / abandoned project.
- DLC, expansion, mode, or episode.
- Franchise / series.
- Studio, publisher, product, film, book, or other non-game brand.

Do not misrepresent a film, book, product, or company as a video game. Non-game results can still be relevant to brand-confusion research, but must be shown separately.

---

# 5. Risk assessment

Do not collapse every factor into one opaque score. Report separate dimensions and explain the reasoning.

Evaluate:

1. Exact existing game-title conflicts.
2. Near-exact spelling and visual similarity.
3. Phonetic similarity.
4. Franchise, studio, or publisher association.
5. Trademark warning signals.
6. Search-engine discoverability and uniqueness.
7. Language, pronunciation, and geographic considerations.
8. Evidence quality and research coverage.

Use these overall preliminary labels:

- **LOW:** No significant conflicts found in the sources actually checked.
- **MODERATE:** Similar titles or limited potential conflicts found.
- **HIGH:** Significant existing game, franchise, or brand conflicts found.
- **CRITICAL:** Strong exact-title or highly recognizable franchise/brand conflict signals found.
- **INSUFFICIENT DATA:** Coverage is too limited to make a meaningful assessment.

Always explain why the label was assigned. It is a research-priority indicator, not a legal conclusion.

A title can have:
- Low game-title conflict risk but unresolved trademark risk.
- High search-result competition but low legal concern.
- An exact title used by an obscure old game, requiring context rather than an automatic legal conclusion.

Do not say “available”, “clear”, “safe”, or “free to use” as a definitive conclusion.

---

# 6. Name generation and verification

When asked to generate names:

1. Extract the game's genre, setting, premise, mechanics, tone, and distinguishing features.
2. Identify naming themes and useful keywords.
3. Generate diverse naming directions rather than dozens of near-identical variations.
4. Include different styles where appropriate:
   - Short and memorable.
   - Atmospheric.
   - Narrative.
   - Genre-signalling.
   - Invented/coined words.
   - Two-word combinations.
   - Series/franchise-friendly.
5. Avoid generic, hard-to-pronounce, unintentionally humorous, or overly derivative candidates.
6. Run the same research workflow on every shortlisted candidate.
7. Remove or flag candidates with significant conflicts.
8. Rank the remaining candidates by distinctiveness, memorability, pronunciation, discoverability, and research findings.
9. Explain why each recommended candidate fits the game.

Never describe generated names as checked or verified unless the relevant searches were actually completed.

If there are too many candidates, generate a broad pool, shortlist a manageable number, and conduct deeper research on the shortlist. Clearly state which candidates received only preliminary checks.

---

# 7. Standard report format

Every research report should include:

## A. Summary
- Proposed title.
- Research date and time zone if known.
- Mode used.
- Short overall assessment.
- Confidence/coverage note.

## B. Research coverage
A table listing each source/category and one of:
- Checked successfully.
- Checked partially.
- Not checked.
- Manual verification required.
- Unavailable / access blocked.

Include a short explanation for incomplete checks.

## C. Exact matches
For each result:
- Game title.
- Developer/publisher if verified.
- Release/announcement date if verified.
- Platform.
- Status.
- Source link.
- Why it is an exact match.

If none were found, say: “No exact matches were found in the sources checked.” Never say “no exact match exists.”

## D. Similar matches
Group by match category and explain the similarity. Separate games from non-game brands and unrelated results.

## E. Trademark and brand findings
List verified records, jurisdiction, status, relevant class information when available, and source links. Clearly distinguish no results from an unperformed search.

## F. Risk assessment
Show the dimensions separately, then the overall preliminary label and reasoning.

## G. Alternatives
For each candidate:
- Name.
- Naming rationale.
- Preliminary match findings.
- Risk label.
- Research coverage.
- Source links.

## H. Recommendation
Give a practical next step. Identify any manual checks or professional legal review that may be appropriate.

Every factual finding should have a source link. Include the research date. Do not fabricate results, records, dates, developers, API responses, or citations.

---

# 8. Technical architecture

Design the system so that the skill remains useful even when optional API credentials are missing.

Suggested layers:

## Layer 1 — Skill instructions
`SKILL.md` selects the mode, orchestrates research, sets evidence standards, and formats the report.

## Layer 2 — Source adapters
Independent adapters for sources that can be queried through permitted means. A failure in one adapter must not stop the others.

## Layer 3 — Normalization and matching
A reusable module that normalizes titles, generates variants, deduplicates results, and classifies similarity.

## Layer 4 — Evidence store
A structured internal representation of results. At minimum, each result should retain:
- Source name.
- Source URL or record ID.
- Retrieved timestamp.
- Raw title.
- Normalized title.
- Entity type.
- Match category.
- Evidence notes.
- Verification status.

Do not store secrets or unnecessary personal data.

## Layer 5 — Risk and report generation
Combine evidence without overstating certainty. Generate Markdown reports and, if useful, JSON output for other tools.

## Layer 6 — Optional integrations
Add API-based sources incrementally. The system should gracefully fall back to web research/manual verification when credentials or permitted access are unavailable.

### Suggested environment variables

Use an `.env.example` containing placeholder names only, such as:

```env
IGDB_CLIENT_ID=
IGDB_CLIENT_SECRET=
```

Add any future credentials only after verifying the relevant provider's current authentication documentation.

Never hardcode credentials in source code, `SKILL.md`, sample reports, or committed configuration. Add `.env` to `.gitignore`.

### Reliability requirements

- Set request timeouts.
- Respect documented rate limits.
- Use retries with backoff only where appropriate.
- Cache results where permitted and useful.
- Record source failures and timestamps.
- Deduplicate results across sources.
- Make source adapters independently testable.
- Do not silently convert errors into “zero matches”.
- Do not rely on unofficial endpoints without clearly documenting their instability and terms implications.

---

# 9. Development phases

Antigravity should first inspect current official documentation and produce a plan. Do not start by generating a large amount of code.

## Phase 0 — Discovery and architecture

1. Read the current Agent Skills specification.
2. Inspect official API and access documentation for candidate sources.
3. Make a source capability matrix.
4. Identify permitted automated access, authentication, quotas, and restrictions.
5. Propose the smallest useful architecture.
6. List assumptions, risks, and unresolved questions.
7. Present the plan before implementation.

## Phase 1 — Portable skill foundation

Create:
- `SKILL.md`
- Reference methodology files.
- README with installation/use examples.
- `.env.example`
- `.gitignore`
- Example reports.

The skill should be usable with an agent's own web-search tools even before custom scripts exist.

## Phase 2 — Core research and matching

Implement:
- Title normalization.
- Variant generation.
- Similarity comparison.
- Result classification.
- Deduplication.
- Structured evidence records.
- Honest coverage reporting.

Add unit tests before adding many external integrations.

## Phase 3 — Source integrations

Start with the most useful sources that have documented, permitted access. Evaluate Steam and IGDB first, then add other sources only when their access method is reliable and compliant.

Do not implement every source at once. A smaller set of reliable sources is better than a large list of broken or prohibited scrapers.

## Phase 4 — Trademark research workflow

Add official database links and automated access only where explicitly supported and permitted. Where automation is not appropriate, generate a guided manual checklist and mark the category as incomplete.

## Phase 5 — Generate and verify

Add candidate generation prompts/workflows and automatically send shortlisted names through the same research pipeline.

## Phase 6 — Evaluation and hardening

Run acceptance tests, inspect false positives and false negatives, improve documentation, and test the skill in more than one Agent Skills-compatible host if available.

---

# 10. Acceptance tests

Create a test suite with fixtures and expected classifications. Include at least:

1. Exact same title, same capitalization.
2. Exact same title with different capitalization.
3. Same title with punctuation or spacing differences.
4. Minor typo / near-exact spelling.
5. Phonetically similar title.
6. Shared generic word but otherwise unrelated title.
7. Same title used by a film or book, not a game.
8. Old or obscure game result.
9. Upcoming or cancelled game result.
10. Multiple games with the same title.
11. Source API unavailable or credentials missing.
12. Search returns no results.
13. Search fails due to rate limit or network error.
14. Trademark source requires manual verification.
15. Generated alternative that has an exact match.
16. Generated alternative that has only a weak semantic match.

Expected behaviour:
- The system must distinguish “no result found” from “source not checked”.
- It must not invent data when a source fails.
- It must cite evidence for discovered matches.
- It must not label a title legally safe.
- It must research generated candidates before recommending them.
- It must explain uncertainty and coverage.

---

# 11. Instructions to Antigravity

Work in the following order:

1. **Read this entire brief.**
2. **Inspect current official documentation** for Agent Skills and every proposed external data source. Prefer primary documentation over blog posts or outdated tutorials.
3. **Produce a concise architecture and implementation plan** with a source capability matrix. Cite the documentation used and identify which sources can actually be automated.
4. **Identify blockers and assumptions.** Ask the user only for decisions that genuinely block implementation. Do not ask for API credentials before establishing that a source is worth integrating.
5. **Implement incrementally**, beginning with the portable skill foundation and core matching logic.
6. **Write and run tests** after each meaningful implementation stage.
7. **Keep the project portable** and avoid dependencies on Antigravity-specific features inside the core skill.
8. **Do not invent API endpoints, access permissions, search results, or legal conclusions.**
9. **Do not scrape or bypass restrictions** on websites that prohibit automated access.
10. **Report what works, what is partial, what needs credentials, and what still requires manual verification.**

At the end, provide:
- The project tree.
- A summary of implemented features.
- Setup instructions.
- Required optional environment variables.
- Test commands and test results.
- Known limitations.
- A short example of checking a title.
- A short example of generating and verifying alternatives.

**Definition of done:** A developer can install the skill in a compatible agent, submit a game title, receive a structured and source-backed research report, understand which sources were actually checked, and request alternative names that are themselves researched.
