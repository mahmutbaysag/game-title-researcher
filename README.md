# 🎮 Game Title Researcher

A portable Agent Skill and CLI tool for video game developers to research title availability, detect naming conflicts, assess trademark risks, and discover distinctive alternatives.

**Zero API keys required out of the box.** Query public storefronts instantly, generate pre-formatted manual verification links for restricted databases, and get clear, structured risk reports.

---

## 🚀 Features

- **Keyless Automated Research:** Queries Steam, Apple App Store, and GOG out of the box without registration or credentials.
- **Intelligent Title Matching:** Combines exact normalized matching, Levenshtein distance, Jaro-Winkler, Token Set/Sort ratios, and Soundex/Metaphone phonetic algorithms.
- **Generic Word Filtering:** Filters 50+ common game tropes ("War", "Legend", "Dark", "Dead", etc.) to minimize false positives.
- **Trademark Link Generator:** Produces pre-filled query links for WIPO Global Brand Database and direct portals for USPTO, EUIPO, TMview, and TÜRKPATENT (Nice Classes 9, 28, 41, 42).
- **Storefront Manual Checklists:** Generates deep search links for PlayStation, Xbox, Nintendo eShop, itch.io, Epic Games Store, and Google Play.
- **Multi-Dimensional Risk Matrix:** Evaluates 7 distinct risk dimensions and computes clear preliminary ratings (`LOW`, `MODERATE`, `HIGH`, `CRITICAL`, `INSUFFICIENT_DATA`).
- **Markdown & JSON Output:** Generates clean Markdown reports and machine-readable JSON for CI/CD or agent pipelines.

---

## 📦 Installation & AI Agent Setup

### 🤖 Using with AI Agents (Claude Code, Cursor, Codex, Antigravity, Roo Code, OpenCode)

This skill follows the open [Agent Skills Specification](https://agentskills.io/specification). AI agents discover and execute it automatically.

#### 1. Claude Code
Clone directly into Claude Code's skill directory:
```bash
# Global installation (available across all projects)
git clone https://github.com/mahmutbaysag/game-title-researcher.git ~/.claude/skills/game-title-researcher

# Or project-level installation
git clone https://github.com/mahmutbaysag/game-title-researcher.git .claude/skills/game-title-researcher
```

#### 2. Antigravity (Google)
Clone into Antigravity user or project skills folder:
```bash
# Windows
git clone https://github.com/mahmutbaysag/game-title-researcher.git "%USERPROFILE%\.gemini\antigravity-cli\skills\game-title-researcher"
```

#### 3. Cursor, Codex CLI, OpenCode, Goose, Roo Code
Clone into your project's `.skills/` directory:
```bash
git clone https://github.com/mahmutbaysag/game-title-researcher.git .skills/game-title-researcher
```
Any compatible agent will parse `SKILL.md` metadata, dynamically activate it when you ask to check a game title, and run research workflows.

---

### 💻 Standalone CLI Usage (Without AI Agent)

```bash
git clone https://github.com/mahmutbaysag/game-title-researcher.git
cd game-title-researcher

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 💻 CLI Usage

### Check a Single Title
```bash
python -m scripts check "Ironhold"
```

Verbose progress tracking:
```bash
python -m scripts check "Ironhold" -v
```

Machine-readable JSON output:
```bash
python -m scripts check "Ironhold" --json
```

### Compare Two Titles
```bash
python -m scripts compare "Ironhold" "Iron Hold"
```

---

## 📁 Project Structure

```text
game-title-researcher/
├── SKILL.md                          # Agent Skills standard specification
├── README.md                         # Documentation and usage guide
├── requirements.txt                  # Python runtime dependencies
├── .env.example                      # Optional credentials template
├── .gitignore                        # Git exclusion rules
├── config/
│   └── sources.yaml                  # Store and source definitions
├── references/
│   ├── research-sources.md           # Source capabilities and access tiers
│   ├── matching-methodology.md       # Similarity algorithms & thresholds
│   ├── trademark-research.md         # Trademark manual guide & Nice classes
│   ├── naming-guidelines.md          # Naming strategies and style advice
│   └── report-template.md            # Standard Markdown report layout
├── scripts/
│   ├── __init__.py
│   ├── __main__.py                   # Module entry point
│   ├── models.py                     # Dataclasses & Enums
│   ├── title_matcher.py              # Normalization, variants & similarity
│   ├── evidence_store.py             # Deduplicated evidence storage
│   ├── manual_urls.py                # Store & trademark link builders
│   ├── risk_analyzer.py              # 7-dimension risk assessment
│   ├── report_generator.py           # Markdown report synthesis
│   ├── cli.py                        # Terminal interface
│   └── adapters/
│       ├── __init__.py
│       ├── base.py                   # Base adapter with throttling & error handling
│       ├── steam_adapter.py          # Steam storefront search (keyless)
│       ├── itunes_adapter.py         # Apple App Store / iTunes API (keyless)
│       └── gog_adapter.py            # GOG catalog API (keyless)
└── tests/
    ├── __init__.py
    ├── test_title_matcher.py         # Normalization & matching unit tests
    ├── test_evidence_store.py        # Storage & deduplication tests
    ├── test_adapters.py              # Mocked HTTP adapter tests
    ├── test_risk_analyzer.py         # Risk level logic tests
    └── test_cli.py                   # End-to-end CLI & JSON tests
```

---

## ⚖️ Legal Disclaimer

This tool performs preliminary factual research and is **not legal advice**. Trademark and intellectual property rights depend on jurisdiction, goods and services classification, prior commercial use, and legal precedent. Always consult a qualified trademark attorney before commercial release or major financial investment.

---

## 📄 License

MIT License. See LICENSE file for details.
