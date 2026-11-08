"""Command-line interface for Game Title Researcher."""
from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from datetime import datetime
from enum import Enum

from .adapters import SteamAdapter, ITunesAdapter, GOGAdapter
from .adapters.base import AdapterError
from .evidence_store import EvidenceStore
from .manual_urls import generate_store_urls, generate_trademark_urls
from .models import (
    ResearchReport,
    SourceCoverage,
    SourceStatus,
)
from .report_generator import (
    generate_recommendation,
    generate_report_markdown,
    generate_summary,
)
from .risk_analyzer import assess_risk
from .title_matcher import classify_match, compare_titles, normalize_title


# ────────────────────────────────────────────────────────────────────── #
#  Helpers
# ────────────────────────────────────────────────────────────────────── #

_ADAPTERS = [SteamAdapter, ITunesAdapter, GOGAdapter]


def _serialize(obj):
    """Recursively convert dataclasses / enums / datetimes to JSON-safe dicts."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {
            f.name: _serialize(getattr(obj, f.name))
            for f in dataclasses.fields(obj)
        }
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, list):
        return [_serialize(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj


# ────────────────────────────────────────────────────────────────────── #
#  Core pipeline
# ────────────────────────────────────────────────────────────────────── #


def check_title(title: str, *, verbose: bool = False) -> ResearchReport:
    """Run full research pipeline on a single title."""
    if verbose:
        print(f"\n🔍 Researching: {title}")
        print("=" * 50)

    store = EvidenceStore()
    coverage: list[SourceCoverage] = []

    for cls in _ADAPTERS:
        adapter = cls()
        try:
            if verbose:
                print(f"  → {adapter.name} …", end=" ", flush=True)
            results = adapter.search(title)

            for rec in results:
                rec.normalized_title = normalize_title(rec.raw_title)
                scores = compare_titles(title, rec.raw_title)
                cat, score = classify_match(title, rec.raw_title, scores)
                rec.match_category = cat
                rec.similarity_score = score
                rec.similarity_details = scores
                store.add(rec)

            coverage.append(
                SourceCoverage(adapter.name, SourceStatus.CHECKED_OK, len(results))
            )
            if verbose:
                print(f"{len(results)} result(s)")
        except AdapterError as exc:
            coverage.append(
                SourceCoverage(adapter.name, SourceStatus.ERROR, notes=str(exc))
            )
            if verbose:
                print(f"ERROR: {exc}")
        finally:
            adapter.close()

    # Manual verification sources
    manual_urls = generate_store_urls(title)
    trademark_findings = generate_trademark_urls(title)

    for mu in manual_urls:
        coverage.append(
            SourceCoverage(mu.source_name, SourceStatus.MANUAL_REQUIRED)
        )
    for tf in trademark_findings:
        coverage.append(
            SourceCoverage(
                f"Trademark: {tf.database}", SourceStatus.MANUAL_REQUIRED
            )
        )

    evidence = store.get_all()
    risk = assess_risk(title, evidence, coverage)

    report = ResearchReport(
        proposed_title=title,
        mode="check",
        coverage=coverage,
        exact_matches=store.get_exact_matches(),
        similar_matches=store.get_similar_matches(),
        trademark_findings=trademark_findings,
        risk_assessment=risk,
        manual_check_urls=manual_urls,
    )
    report.summary = generate_summary(report)
    report.recommendation = generate_recommendation(report)
    return report


# ────────────────────────────────────────────────────────────────────── #
#  CLI entry point
# ────────────────────────────────────────────────────────────────────── #


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="game-title-researcher",
        description="Research video game title availability and conflicts",
    )
    sub = parser.add_subparsers(dest="command")

    # -- check --
    p_check = sub.add_parser("check", help="Check a game title")
    p_check.add_argument("title", help="Game title to research")
    p_check.add_argument("-v", "--verbose", action="store_true")
    p_check.add_argument(
        "--json", dest="as_json", action="store_true", help="Output JSON"
    )

    # -- compare --
    p_cmp = sub.add_parser("compare", help="Compare two titles")
    p_cmp.add_argument("title_a")
    p_cmp.add_argument("title_b")

    args = parser.parse_args(argv)

    if args.command == "check":
        if not args.as_json and not args.verbose:
            sys.stderr.write(f"🔍 Checking '{args.title}' across Steam, App Store, and GOG...\n")
        report = check_title(args.title, verbose=args.verbose)
        if args.as_json:
            print(json.dumps(_serialize(report), indent=2, ensure_ascii=False))
        else:
            print(generate_report_markdown(report))

    elif args.command == "compare":
        scores = compare_titles(args.title_a, args.title_b)
        cat, score = classify_match(args.title_a, args.title_b, scores)
        print(f"Comparing: '{args.title_a}' vs '{args.title_b}'")
        print(f"Category:  {cat.value}")
        print(f"Score:     {score:.3f}")
        print("Details:")
        for k, v in scores.items():
            print(f"  {k}: {v:.3f}" if isinstance(v, float) else f"  {k}: {v}")

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
