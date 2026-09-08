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
SEED_DECISIONS = OUT / "STEP_05A_SEED_DECISIONS.json"
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

PAGE_FIELDS = [
    "inspection_id",
    "competitor_domain",
    "requested_url",
    "final_url",
    "source_step09_query_index",
    "source_step09_query_text",
    "source_step09_rank",
    "http_or_browser_access_state",
    "observation_date",
    "page_type",
    "page_title",
    "h1",
    "material_h2_h3_topics",
    "material_commercial_axes",
    "material_product_service_axes",
    "material_use_case_axes",
    "material_problem_solution_axes",
    "price_or_calculator_presence",
    "portfolio_or_examples_presence",
    "installation_process_presence",
    "faq_presence",
    "trust_or_proof_elements_presence",
    "relevant_internal_navigation_labels",
    "page_evidence_notes",
    "claim_boundary",
]

SEED_FIELDS = [
    "seed_id",
    "normalized_candidate_seed",
    "semantic_axis",
    "competitor_domain",
    "source_requested_url",
    "source_final_url",
    "source_step09_query_index",
    "source_step09_query_text",
    "source_step09_rank",
    "source_page_element_type",
    "source_page_element_text",
    "source_page_evidence_summary",
    "existing_semantic_match_state",
    "existing_semantic_match_examples",
    "business_scope_state",
    "seed_decision",
    "wordstat_required",
    "wordstat_priority",
    "rationale",
    "claim_boundary",
]

WORDSTAT_FIELDS = [
    "wordstat_seed_order",
    "normalized_candidate_seed",
    "semantic_axis",
    "supporting_competitor_count",
    "supporting_page_count",
    "supporting_source_ids",
    "why_existing_core_is_insufficient",
    "business_scope_state",
    "recommended_wordstat_region",
    "recommended_device_scope",
    "provider_call_authorization_state",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


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


def build_page_evidence() -> None:
    targets = authorized_targets()
    observations = json.loads(OBSERVATIONS.read_text(encoding="utf-8"))
    if not isinstance(observations, list):
        raise ValueError("Observation input must be a JSON array")
    by_id = {row["inspection_id"]: row for row in observations}
    if len(by_id) != len(observations):
        raise ValueError("Duplicate inspection_id in observation input")
    authorized_ids = {row["inspection_id"] for row in targets}
    if not set(by_id).issubset(authorized_ids):
        raise ValueError(f"Out-of-scope observation IDs: {sorted(set(by_id) - authorized_ids)}")

    rows: list[dict[str, object]] = []
    for target in targets:
        observation = by_id.get(target["inspection_id"])
        if observation is None:
            continue
        requested = str(target["requested_url"])
        if observation.get("requested_url") != requested:
            raise ValueError(f"Requested URL mismatch for {target['inspection_id']}")
        merged = {**target, **observation}
        missing = [field for field in PAGE_FIELDS if field not in merged]
        if missing:
            raise ValueError(f"Missing fields for {target['inspection_id']}: {missing}")
        rows.append(merged)
    write_tsv(PAGE_EVIDENCE, PAGE_FIELDS, rows)


def build_seed_candidates() -> None:
    pages = {row["inspection_id"]: row for row in read_tsv(PAGE_EVIDENCE)}
    specs = json.loads(SEED_DECISIONS.read_text(encoding="utf-8"))
    if not isinstance(specs, list):
        raise ValueError("Seed decisions must be a JSON array")
    normalized = [row["normalized_candidate_seed"] for row in specs]
    if len(normalized) != len(set(normalized)):
        raise ValueError("Seed decisions must be semantically deduplicated by normalized seed")

    rows: list[dict[str, object]] = []
    for spec_index, spec in enumerate(specs, 1):
        sources = spec.get("sources", [])
        if not sources:
            raise ValueError(f"Seed has no page lineage: {spec['normalized_candidate_seed']}")
        for source_index, source in enumerate(sources, 1):
            page = pages.get(source["inspection_id"])
            if page is None:
                raise ValueError(f"Unknown page source: {source['inspection_id']}")
            decision = spec["seed_decision"] if source_index == 1 else "DUPLICATE_OF_ANOTHER_COMPETITOR_SEED"
            row = {
                "seed_id": f"CS{spec_index:03d}-{source_index:02d}",
                "normalized_candidate_seed": spec["normalized_candidate_seed"],
                "semantic_axis": spec["semantic_axis"],
                "competitor_domain": page["competitor_domain"],
                "source_requested_url": page["requested_url"],
                "source_final_url": page["final_url"],
                "source_step09_query_index": page["source_step09_query_index"],
                "source_step09_query_text": page["source_step09_query_text"],
                "source_step09_rank": page["source_step09_rank"],
                "source_page_element_type": source["element_type"],
                "source_page_element_text": source["element_text"],
                "source_page_evidence_summary": page["page_evidence_notes"],
                "existing_semantic_match_state": spec["existing_semantic_match_state"],
                "existing_semantic_match_examples": " | ".join(spec["existing_semantic_match_examples"]),
                "business_scope_state": spec["business_scope_state"],
                "seed_decision": decision,
                "wordstat_required": str(spec["wordstat_required"]).lower() if source_index == 1 else "false",
                "wordstat_priority": spec["wordstat_priority"] if source_index == 1 else "NOT_APPLICABLE_DUPLICATE",
                "rationale": spec["rationale"] if source_index == 1 else f"Duplicate page support for {spec['normalized_candidate_seed']}; retained as lineage, not a second seed.",
                "claim_boundary": spec["claim_boundary"],
            }
            rows.append(row)
    write_tsv(SEED_CANDIDATES, SEED_FIELDS, rows)


def build_wordstat_package() -> None:
    specs = json.loads(SEED_DECISIONS.read_text(encoding="utf-8"))
    pages = {row["inspection_id"]: row for row in read_tsv(PAGE_EVIDENCE)}
    surviving = sorted(
        (row for row in specs if row["seed_decision"] == "POTENTIALLY_NEW_WORDSTAT_SEED"),
        key=lambda row: int(row["wordstat_priority"]),
    )
    rows: list[dict[str, object]] = []
    for order, spec in enumerate(surviving, 1):
        source_ids = [source["inspection_id"] for source in spec["sources"]]
        rows.append(
            {
                "wordstat_seed_order": order,
                "normalized_candidate_seed": spec["normalized_candidate_seed"],
                "semantic_axis": spec["semantic_axis"],
                "supporting_competitor_count": len({pages[source_id]["competitor_domain"] for source_id in source_ids}),
                "supporting_page_count": len(set(source_ids)),
                "supporting_source_ids": " | ".join(source_ids),
                "why_existing_core_is_insufficient": spec["rationale"],
                "business_scope_state": spec["business_scope_state"],
                "recommended_wordstat_region": "213",
                "recommended_device_scope": "ALL",
                "provider_call_authorization_state": "RETURN_TO_MAIN_CHATGPT_FOR_BRIDGE_EXECUTION",
            }
        )
    write_tsv(WORDSTAT_PACKAGE, WORDSTAT_FIELDS, rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase",
        choices=["baseline", "page-evidence", "seed-candidates", "wordstat-package"],
        required=True,
    )
    args = parser.parse_args()
    if args.phase == "baseline":
        build_checkpoint()
    elif args.phase == "page-evidence":
        build_page_evidence()
    elif args.phase == "seed-candidates":
        build_seed_candidates()
    elif args.phase == "wordstat-package":
        build_wordstat_package()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
