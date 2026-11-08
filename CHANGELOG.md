# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-11-08

### Added
- Complete compatibility with open [Agent Skills Specification](https://agentskills.io).
- `CONTRIBUTING.md` and `SECURITY.md` for open-source community standards.
- `requirements-dev.txt` separating testing/dev dependencies from production runtime.
- Multi-OS platform detection for GOG catalog (Windows, macOS, Linux).
- Automated test coverage for GOG catalog adapter.

### Changed
- Replaced absolute Windows paths in `SKILL.md` with standard relative links.
- Optimized GOG catalog query parameters (`order: desc:score`, direct search query).
- Cleaned and streamlined `requirements.txt` to strictly runtime packages.

## [1.0.0] - 2026-11-07

### Added
- Initial release of **Game Title Researcher** agent skill and CLI tool.
- Zero-API-key storefront adapters: Steam Store Search, Apple App Store (iTunes API), GOG Catalog.
- Multi-algorithm title matcher (Levenshtein, Jaro-Winkler, Token Sort/Set, Soundex, Metaphone).
- 50+ generic game trope word filter list.
- Multi-dimensional risk matrix (7 dimensions + overall rating).
- Automated generation of pre-formatted trademark search URLs (WIPO, USPTO, EUIPO, TMview, TÜRKPATENT).
- Manual verification search link generation for PlayStation, Xbox, Nintendo, itch.io, Epic Games, Google Play.
- Markdown report generator and machine-readable JSON output mode.
- Full test suite with 24 mocked and unit test cases.
