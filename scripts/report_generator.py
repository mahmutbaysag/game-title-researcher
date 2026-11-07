"""Generate Markdown research reports."""
from __future__ import annotations

from .models import (
    MatchCategory,
    ResearchReport,
    RiskLevel,
    SourceStatus,
)


def _risk_emoji(level: RiskLevel) -> str:
    return {
        RiskLevel.LOW: "🟢",
        RiskLevel.MODERATE: "🟡",
        RiskLevel.HIGH: "🟠",
        RiskLevel.CRITICAL: "🔴",
        RiskLevel.INSUFFICIENT_DATA: "⚪",
    }.get(level, "⚪")


def _status_emoji(status: SourceStatus) -> str:
    return {
        SourceStatus.CHECKED_OK: "✅",
        SourceStatus.CHECKED_PARTIAL: "⚠️",
        SourceStatus.NOT_CHECKED: "⬜",
        SourceStatus.MANUAL_REQUIRED: "🔗",
        SourceStatus.UNAVAILABLE: "❌",
        SourceStatus.ERROR: "❌",
    }.get(status, "⬜")


# ---------------------------------------------------------------------- #


def generate_report_markdown(report: ResearchReport) -> str:
    """Produce a complete Markdown report from a *ResearchReport*."""
    out: list[str] = []

    # ── A. Header / Summary ──────────────────────────────────────────
    out.append(f"# 🎮 Game Title Research Report: *{report.proposed_title}*\n")
    out.append("## A. Summary\n")
    out.append(f"- **Proposed Title:** {report.proposed_title}")
    out.append(
        f"- **Research Date:** {report.research_date.strftime('%Y-%m-%d %H:%M UTC')}"
    )
    out.append(f"- **Mode:** {report.mode}")
    out.append(
        f"- **Overall Risk:** {_risk_emoji(report.risk_assessment.overall)}"
        f" **{report.risk_assessment.overall.value}**"
    )
    if report.summary:
        out.append(f"\n{report.summary}")
    out.append("")

    # ── B. Research Coverage ─────────────────────────────────────────
    out.append("## B. Research Coverage\n")
    out.append("| Source | Status | Results | Notes |")
    out.append("|--------|--------|---------|-------|")
    for cov in report.coverage:
        e = _status_emoji(cov.status)
        n = cov.notes or "—"
        out.append(f"| {cov.source_name} | {e} {cov.status.value} | {cov.result_count} | {n} |")
    out.append("")

    # ── C. Exact Matches ─────────────────────────────────────────────
    out.append("## C. Exact Matches\n")
    if report.exact_matches:
        for ev in report.exact_matches:
            out.append(f"### {ev.raw_title}")
            if ev.developer:
                out.append(f"- **Developer:** {ev.developer}")
            if ev.publisher:
                out.append(f"- **Publisher:** {ev.publisher}")
            if ev.release_date:
                out.append(f"- **Release Date:** {ev.release_date}")
            if ev.platforms:
                out.append(f"- **Platforms:** {', '.join(ev.platforms)}")
            out.append(f"- **Status:** {ev.status or 'unknown'}")
            if ev.source_url:
                out.append(f"- **Source:** [{ev.source_name}]({ev.source_url})")
            else:
                out.append(f"- **Source:** {ev.source_name}")
            out.append(
                f"- **Match:** {ev.match_category.value} "
                f"(score: {ev.similarity_score:.2f})"
            )
            out.append("")
    else:
        out.append(
            "No exact matches were found in the sources checked.\n"
        )

    # ── D. Similar Matches ───────────────────────────────────────────
    out.append("## D. Similar Matches\n")
    if report.similar_matches:
        by_cat: dict[MatchCategory, list] = {}
        for ev in report.similar_matches:
            by_cat.setdefault(ev.match_category, []).append(ev)
        for cat, items in by_cat.items():
            out.append(f"### {cat.value.replace('_', ' ').title()}\n")
            for ev in items:
                link = (
                    f"[{ev.source_name}]({ev.source_url})"
                    if ev.source_url
                    else ev.source_name
                )
                out.append(
                    f"- **{ev.raw_title}** — {link} "
                    f"(score: {ev.similarity_score:.2f})"
                )
                if ev.developer:
                    out.append(f"  - Developer: {ev.developer}")
                if ev.notes:
                    out.append(f"  - Note: {ev.notes}")
            out.append("")
    else:
        out.append("No similar matches were found in the sources checked.\n")

    # ── E. Trademark & Brand Findings ────────────────────────────────
    out.append("## E. Trademark & Brand Findings\n")
    if report.trademark_findings:
        for tf in report.trademark_findings:
            e = _status_emoji(tf.status)
            out.append(f"- {e} **{tf.database}**: [{tf.search_url}]({tf.search_url})")
            if tf.notes:
                out.append(f"  - {tf.notes}")
    out.append(
        "\n> ⚠️ **Legal Disclaimer:** This is preliminary research, not legal "
        "advice. Trademark rights depend on jurisdiction, goods/services, use, "
        "and other factors. Professional legal review is recommended before "
        "commercial launch.\n"
    )

    # ── F. Risk Assessment ───────────────────────────────────────────
    out.append("## F. Risk Assessment\n")
    ra = report.risk_assessment
    out.append("| Dimension | Level |")
    out.append("|-----------|-------|")
    for label, val in [
        ("Game Title Conflict", ra.game_title_conflict),
        ("Spelling / Visual Similarity", ra.spelling_visual),
        ("Phonetic Similarity", ra.phonetic),
        ("Franchise Association", ra.franchise_association),
        ("Trademark Signals", ra.trademark_signals),
        ("Search Discoverability", ra.search_discoverability),
        ("Evidence Coverage", ra.evidence_coverage),
        ("**Overall**", ra.overall),
    ]:
        out.append(f"| {label} | {_risk_emoji(val)} {val.value} |")
    out.append(f"\n**Reasoning:** {ra.reasoning}\n")

    # ── G. Alternatives ──────────────────────────────────────────────
    if report.alternatives:
        out.append("## G. Alternative Suggestions\n")
        for alt in report.alternatives:
            out.append(f"### {alt.name}")
            out.append(f"- **Rationale:** {alt.rationale}")
            out.append(f"- **Risk:** {_risk_emoji(alt.risk_level)} {alt.risk_level.value}")
            if alt.match_findings:
                out.append(f"- **Findings:** {len(alt.match_findings)} result(s)")
                for mf in alt.match_findings[:3]:
                    out.append(
                        f"  - {mf.raw_title} ({mf.source_name}, "
                        f"{mf.match_category.value})"
                    )
            out.append("")

    # ── H. Recommendation ────────────────────────────────────────────
    out.append("## H. Recommendation\n")
    out.append(report.recommendation or "No specific recommendation generated.")
    out.append("")

    # ── Manual Verification Links ────────────────────────────────────
    if report.manual_check_urls:
        out.append("## 🔗 Manual Verification Links\n")
        for mu in report.manual_check_urls:
            out.append(f"- **{mu.source_name}:** [{mu.url}]({mu.url})")
            if mu.instructions:
                out.append(f"  - {mu.instructions}")
        out.append("")

    return "\n".join(out)


# ---------------------------------------------------------------------- #


def generate_summary(report: ResearchReport) -> str:
    """One-paragraph summary for section A."""
    exact_n = len(report.exact_matches)
    similar_n = len(report.similar_matches)
    checked_n = len(
        [
            c
            for c in report.coverage
            if c.status in (SourceStatus.CHECKED_OK, SourceStatus.CHECKED_PARTIAL)
        ]
    )

    parts: list[str] = []
    if exact_n:
        parts.append(f"**{exact_n} exact match(es) found** across checked sources")
    else:
        parts.append("No exact matches found in checked sources")
    if similar_n:
        parts.append(f"{similar_n} similar title(s) detected")
    parts.append(f"{checked_n} source(s) successfully queried")
    parts.append("Trademark databases require manual verification")
    return ". ".join(parts) + "."


def generate_recommendation(report: ResearchReport) -> str:
    """Practical next-step recommendation based on overall risk."""
    risk = report.risk_assessment.overall

    if risk == RiskLevel.CRITICAL:
        return (
            "**Strong conflicts detected.** This title is already in use by one or "
            "more existing games or well-known brands. Consider choosing a different "
            "title or consulting a trademark attorney before proceeding. Check the "
            "trademark databases linked above for registered marks."
        )
    if risk == RiskLevel.HIGH:
        return (
            "**Significant conflicts found.** Existing games or brands with similar "
            "names could cause confusion. Verify the trademark databases linked "
            "above. Consider alternative titles or consult a trademark attorney. "
            "If proceeding, ensure strong visual branding differentiation."
        )
    if risk == RiskLevel.MODERATE:
        return (
            "**Some similar titles exist** but may not pose a direct conflict "
            "depending on context. Manually verify the trademark databases linked "
            "above. Consider whether the similarities could cause player confusion "
            "in your target markets."
        )
    if risk == RiskLevel.INSUFFICIENT_DATA:
        return (
            "**Research coverage is limited.** Not enough sources were successfully "
            "checked to make a confident assessment. Try again later or manually "
            "check the verification links above. Do not assume the title is "
            "available based on incomplete research."
        )
    # LOW
    return (
        "**No significant conflicts found** in the sources checked. This is a "
        "promising sign but not a guarantee of availability. Verify the trademark "
        "databases linked above before committing. Professional legal review is "
        "recommended before commercial launch or significant investment."
    )
