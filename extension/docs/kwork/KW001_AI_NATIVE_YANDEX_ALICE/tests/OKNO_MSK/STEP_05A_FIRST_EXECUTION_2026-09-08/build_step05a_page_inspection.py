#!/usr/bin/env python3
"""Build Step 5A.2/5A.3 artifacts from the authorized URL universe.

The script never performs network or provider calls. Public-page observations
are supplied separately as explicit, auditable inputs and all reconciliation is
performed against preserved repository authorities.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


OUT = Path(__file__).resolve().parent
JOB = OUT.parent
SELECTION = OUT / "STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv"
SERP = OUT / "STEP_05A_SERP_COMBINED_750.tsv"
CHECKPOINT = OUT / "CHECKPOINT_01_COMPETITOR_PAGE_INSPECTION_BASELINE.md"
OBSERVATIONS = OUT / "STEP_05A_COMPETITOR_PAGE_OBSERVATIONS.json"
PAGE_EVIDENCE = OUT / "STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv"
SEED_CANDIDATES = OUT / "STEP_05A_DERIVED_SEED_CANDIDATES.tsv"
WORDSTAT_PACKAGE = OUT / "STEP_05A_WORDSTAT_REQUIREMENT_PACKAGE.tsv"
QA = OUT / "STEP_05A_PAGE_INSPECTION_QA.json"
REPORT = OUT / "STEP_05A_PAGE_INSPECTION_REPORT.md"
LOG = OUT / "STEP_05A_PAGE_INSPECTION_EXECUTION_LOG.md"

STARTING_HEAD = "09486a6fd2cf09fd2ef362e1e13456441a75717c"
EXPECTED_DOMAINS = [
    "mosokna.ru",
    "i-okna.ru",
    "msk.okna-servise.com",
    "okna-moskva.ru",
    "oknafactoria.ru",
    "okna-germany.ru",
    "fabrikaokon.ru",
    "aluminarium.ru",
    "elit-balkon.ru",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def authorized_targets() -> list[dict[str, object]]:
    selected = [
        row
        for row in read_tsv(SELECTION)
        if row["selection_state"] == "SELECTED_FOR_NEXT_STEP5A_PAGE_INSPECTION"
    ]
    query_lookup: dict[tuple[int, int, str], str] = {}
    for row in read_tsv(SERP):
        query_lookup[(int(row["query_index"]), int(row["rank"]), row["url"])] = row[
            "query_text"
        ]

    targets: list[dict[str, object]] = []
    for row in selected:
        for item in row["exact_ranking_urls_to_inspect_next"].split(" | "):
            match = re.fullmatch(r"Q(\d+)/R(\d+) (https?://\S+)", item)
            if not match:
                raise ValueError(f"Malformed authorized target: {item}")
            query_index, rank, url = int(match.group(1)), int(match.group(2)), match.group(3)
            query_text = query_lookup.get((query_index, rank, url))
            if query_text is None:
                raise ValueError(f"Target absent from preserved SERP: {item}")
            targets.append(
                {
                    "inspection_id": f"I{len(targets) + 1:03d}",
                    "competitor_domain": row["normalized_domain"],
                    "requested_url": url,
                    "source_step09_query_index": query_index,
                    "source_step09_query_text": query_text,
                    "source_step09_rank": rank,
                }
            )
    return targets


def build_checkpoint() -> None:
    targets = authorized_targets()
    domains = list(dict.fromkeys(str(row["competitor_domain"]) for row in targets))
    if domains != EXPECTED_DOMAINS or len(targets) != 44:
        raise ValueError(f"Unexpected universe: domains={domains!r}, targets={len(targets)}")

    lines = [
        "# CHECKPOINT 01 — competitor-page inspection baseline",
        "",
        "Date: 2026-09-08  ",
        "Status: **BASELINE FROZEN / READY FOR AUTHORIZED PAGE OPENING**",
        "",
        "## Scope boundary",
        "",
        f"- Starting remote HEAD: `{STARTING_HEAD}`",
        "- Selected domains: `9`",
        "- Authorized preserved ranking URLs: `44`",
        "- Authorized evidence targets are exactly the rows below.",
        "- Extra URL discovery, site crawling and seed inference from domains or URL slugs are forbidden.",
        "- New Yandex Search, Wordstat, Alice, GenSearch, Webmaster, Metrika and Direct calls: `0`.",
        "",
        "## Authorized inspection universe",
        "",
        "| ID | Domain | Step 9 evidence | Query | Exact URL |",
        "|---|---|---:|---|---|",
    ]
    for row in targets:
        lines.append(
            f"| {row['inspection_id']} | {row['competitor_domain']} | "
            f"Q{row['source_step09_query_index']}/R{row['source_step09_rank']} | "
            f"{row['source_step09_query_text']} | {row['requested_url']} |"
        )
    lines += [
        "",
        "## Protected baseline",
        "",
        "- Corrected client release Git tree: `a011ea5b5afa00a21031a254eb86ca6bd7b7a89f`",
        "- Document 01 SHA-256: `79450c2f0dc58ea064b72b7c400f6db7b908cb455c72003584c5e59c9b9fad08`",
        "- Document 02 SHA-256: `b1a2848f781fe12dfe8293cfe2f88e796c967ce9eee7f9b251b171ac73060056`",
        "- Document 03 SHA-256: `d5c90cf187041e975f17d03a2be138eff0b6a06bfe1b7d395a3b24547edc62b0`",
        "- Semantic core 04 SHA-256: `cee26a8d7d4a8381d4706c7940b739c3afca652034e9e3630053e35bd0184e3a`",
        "- Level-1 method promotion remains false/pending.",
        "",
        "## Next block",
        "",
        "Open only the exact targets above and persist one observation for every target, including explicit failures.",
    ]
    CHECKPOINT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["baseline"], required=True)
    args = parser.parse_args()
    if args.phase == "baseline":
        build_checkpoint()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
