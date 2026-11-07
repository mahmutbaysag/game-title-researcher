# Title Matching & Similarity Methodology

This document details title normalization, variant generation, similarity metrics, and categorization logic used in Game Title Researcher.

---

## 1. Normalization Pipeline

Raw titles undergo deterministic multi-step normalization:
1. **Unicode NFKD Normalization:** Decomposes accented characters (e.g., `é` → `e` + accent mark).
2. **Diacritic Stripping:** Combines characters and strips marks.
3. **Case Folding:** Converts characters to lowercase.
4. **Alphanumeric Isolation:** Replaces non-alphanumeric symbols, punctuation, and dashes with standard ASCII spaces.
5. **Whitespace Collapsing:** Strips leading/trailing spaces and collapses repeated spaces to single spaces.

Example:
`"Pokémon: Iron-Hold 2026!"` → `"pokemon iron hold 2026"`

---

## 2. Variant Generation

To capture related search patterns, the engine generates:
- **Exact & Normalized:** `Ironhold`, `ironhold`
- **Article Stripping:** Removes leading `the`, `a`, `an` (`"The Iron Hold"` → `"iron hold"`)
- **Spacing Variants:** Concatenated (`"ironhold"`) and spaced (`"iron hold"`)
- **Hyphenation:** Spaced converted to dashes (`"iron-hold"`)
- **Plural / Singular:** Inflection variants (`"ironholds"` / `"ironhold"`)

---

## 3. Comparison Metrics & Algorithms

Comparison uses multiple complementary algorithms from `rapidfuzz` and `jellyfish`:

| Metric | Algorithm | Strength |
|:---|:---|:---|
| **Exact Normalized** | Equality check | Instant 100% equivalence match |
| **Levenshtein Ratio** | `rapidfuzz.fuzz.ratio` | Character edit distance; catches typos and misspellings |
| **Jaro-Winkler** | `jellyfish.jaro_winkler_similarity` | Weights prefix agreement; good for shared name roots |
| **Token Set Ratio** | `rapidfuzz.fuzz.token_set_ratio` | Set overlap; robust against extra descriptive words |
| **Token Sort Ratio** | `rapidfuzz.fuzz.token_sort_ratio` | Word anagramming; catches inverted word order |
| **Partial Ratio** | `rapidfuzz.fuzz.partial_ratio` | Substring inclusion |
| **Phonetic Encoding** | Soundex & Metaphone | Catches identical pronunciation with different spelling |

---

## 4. Match Classification Rules

Every candidate is evaluated against hierarchical decision rules:

1. **`EXACT_MATCH` (Score = 1.0):**
   - Normalized query equals normalized candidate.

2. **`NEAR_EXACT` (Levenshtein ≥ 0.85):**
   - Minor typos, single letter substitutions, or small punctuation variances.
   - Example: `"Ironhold"` vs `"Ironhould"`.

3. **`PHONETIC_MATCH` (Soundex or Metaphone match AND Levenshtein ≥ 0.50):**
   - Pronunciation matches while string distance is close enough to avoid spurious homophone traps.
   - Example: `"Night"` vs `"Knight"`.

4. **`STRUCTURAL_MATCH` (Token Set ≥ 0.80 OR Token Sort ≥ 0.85):**
   - Reordered words or common modifier additions.
   - Example: `"Iron Hold"` vs `"Hold of Iron"`.

5. **`PARTIAL_MATCH` (Non-generic word overlap AND Partial Ratio ≥ 0.70):**
   - Shares a distinctive, non-generic keyword.
   - Example: `"Ironhold Quest"` shares `"ironhold"`.

6. **`UNRELATED`:**
   - Fails all above criteria. Shared generic words alone do not trigger a match.

---

## 5. Generic Word Filter

Common game title keywords are ignored when evaluating partial matches to prevent false positives:
- Articles: `the`, `a`, `an`, `of`, `and`, `or`, `in`, `on`, `for`
- Tropes: `war`, `wars`, `dark`, `dead`, `last`, `rise`, `fall`, `world`, `star`, `battle`, `quest`, `legend`, `shadow`, `blood`, `iron`, `steel`, `fire`, `ice`, `storm`, `night`, `day`, `king`, `lord`, `dragon`, `sword`, `tower`, `gate`, `city`, `hero`, `super`, `final`

Example:
`"War of Heroes"` vs `"Dark War"` will **not** trigger a partial match despite sharing `"war"`.
