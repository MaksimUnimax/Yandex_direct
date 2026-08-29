from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT_WORKING = ROOT / "STEP_07C_SEMANTIC_CORRECTION_WORKING.tsv"
INPUT_DUPLICATES = ROOT / "STEP_07C_NONEXACT_DUPLICATE_CANDIDATES.tsv"
OUT_SET = ROOT / "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv"
OUT_REVIEW = ROOT / "STEP_08_REVIEW_RESOLUTION_ROUTES.tsv"
OUT_DUP = ROOT / "STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv"
OUT_RECON = ROOT / "STEP_08_SEARCH_STAGE_FREEZE_RECONCILIATION.md"

EXPECTED = {
    "phrase_keys": 2840,
    "KEEP": 1388,
    "REVIEW": 1118,
    "EXCLUDE_SCOPE": 180,
    "EXCLUDE_IRRELEVANT": 120,
    "EXCLUDE_MECHANICAL": 34,
    "duplicate_groups": 9,
    "duplicate_rows": 18,
}

# Step 8 only routes to evidence that this workflow can actually obtain.
# Business relevance is not a separate evidence channel here. It is evaluated from
# known public offer/scope together with Search intent; unknown internal commercial
# priorities belong to later prioritization/client constraints, not to Search routing.
SEARCH_REASONS = {
    "AMBIGUOUS_NUMERIC_OR_FRAGMENT_INTENT",
    "ARCHITECTURE_OR_INSPIRATION_INTENT_NEEDS_SEARCH",
    "BALCONY_REGULATORY_OR_NEGATED_INTENT_NEEDS_SEARCH",
    "COMPARISON_INTENT_NEEDS_SEARCH_VALIDATION",
    "COMPONENT_OR_ACCESSORY_INTENT_NEEDS_BUSINESS_FIT",
    "DEMOLITION_SERVICE_BOUNDARY_NEEDS_VALIDATION",
    "DESIGN_OR_INSPIRATION_INTENT_NEEDS_SEARCH",
    "DIY_OR_PROCEDURAL_INTENT_NEEDS_CONTENT_FIT",
    "HARDWARE_BRAND_INTENT_NEEDS_BUSINESS_FIT",
    "INSTALLATION_ADJACENT_OR_JOB_INTENT_NEEDS_VALIDATION",
    "MATERIAL_OR_PRICE_CONTEXT_NEEDS_VALIDATION",
    "NAVIGATIONAL_OR_ENTITY_INTENT_NEEDS_VALIDATION",
    "PANORAMIC_REAL_ESTATE_OR_INSPIRATION_INTENT_NEEDS_SEARCH",
    "PRIVATE_HOUSE_ADJACENT_TASK_NEEDS_VALIDATION",
    "PVC_DOOR_SUBTYPE_BUSINESS_FIT_NEEDS_VALIDATION",
    "REHAU_REPAIR_OR_DIAGNOSTIC_INTENT_NEEDS_SEARCH",
    "REPAIR_ADJACENT_INFORMATION_INTENT_NEEDS_VALIDATION",
    "REPAIR_FRAGMENT_OR_DIY_INTENT_NEEDS_VALIDATION",
    "REPAIR_NAVIGATIONAL_OR_ENTITY_INTENT_NEEDS_VALIDATION",
    "RETAINED_BUSINESS_BOUNDARY_NEEDS_SEARCH",
    "STATE_OR_CONTEXT_FRAGMENT_NEEDS_VALIDATION",
    "TECHNICAL_INFORMATION_INTENT_NEEDS_CONTENT_FIT",
    "VAGUE_INFORMATIONAL_INTENT_NEEDS_VALIDATION",
}

DEFERRED_REASONS = {
    "RETAINED_ASSOCIATION_ONLY_NEEDS_VALIDATION",
}

FORBIDDEN_DISPOSITIONS = {"REVIEW_BUSINESS", "REVIEW_SEARCH_AND_BUSINESS"}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def route_review(reason: str) -> tuple[str, str]:
    if reason in SEARCH_REASONS:
        return "REVIEW_SEARCH", "ORDINARY_SEARCH_NEEDED_TO_RESOLVE_INTENT_RELEVANCE_OR_BOUNDARY"
    if reason in DEFERRED_REASONS:
        return "REVIEW_DEFERRED", "ASSOCIATION_ONLY_EVIDENCE_RETAINED_WITHOUT_IMMEDIATE_SEARCH_CALL"
    raise AssertionError(f"Unmapped REVIEW reason: {reason}")


def duplicate_group_route(dispositions: set[str]) -> str:
    assert not (dispositions & FORBIDDEN_DISPOSITIONS), dispositions
    if "CORE_CANDIDATE" in dispositions or "REVIEW_SEARCH" in dispositions:
        return "ORDINARY_SEARCH_BEFORE_ANY_NONEXACT_MERGE"
    if dispositions == {"REVIEW_DEFERRED"}:
        return "DEFER_UNLESS_GROUP_SELECTED_FOR_SEARCH"
    if dispositions == {"EXCLUDED_PRESERVED"}:
        return "NO_ACTIVE_NONEXACT_MERGE_ROUTE"
    return "PRESERVE_UNRESOLVED_MIXED_ROUTE"


def main() -> None:
    rows = read_tsv(INPUT_WORKING)
    dup_rows = read_tsv(INPUT_DUPLICATES)

    assert len(rows) == EXPECTED["phrase_keys"], (len(rows), EXPECTED["phrase_keys"])
    status_counts = Counter(r["corrected_status"] for r in rows)
    for status in ["KEEP", "REVIEW", "EXCLUDE_SCOPE", "EXCLUDE_IRRELEVANT", "EXCLUDE_MECHANICAL"]:
        assert status_counts[status] == EXPECTED[status], (status, status_counts[status], EXPECTED[status])

    out_fields = list(rows[0].keys()) + ["search_stage_disposition", "next_resolution_route", "route_reason"]
    route_counts: Counter[str] = Counter()
    review_reason_counts: Counter[str] = Counter()
    review_rows: list[dict[str, str]] = []
    out_rows: list[dict[str, str]] = []

    for row in rows:
        status = row["corrected_status"]
        reason = row["corrected_reason"]
        if status == "KEEP":
            disposition = "CORE_CANDIDATE"
            next_route = "ORDINARY_SEARCH_ELIGIBLE"
            route_reason = "ACCEPTED_STEP07C_KEEP_WITH_POSITIVE_EVIDENCE"
        elif status == "REVIEW":
            disposition, route_reason = route_review(reason)
            next_route = disposition
            review_reason_counts[reason] += 1
        elif status.startswith("EXCLUDE_"):
            disposition = "EXCLUDED_PRESERVED"
            next_route = "NO_ACTIVE_SEARCH_ROUTE"
            route_reason = "ACCEPTED_STEP07C_EXCLUSION_PRESERVED_FOR_AUDIT"
        else:
            raise AssertionError(f"Unexpected status: {status}")

        assert disposition not in FORBIDDEN_DISPOSITIONS
        out = dict(row)
        out["search_stage_disposition"] = disposition
        out["next_resolution_route"] = next_route
        out["route_reason"] = route_reason
        out_rows.append(out)
        route_counts[disposition] += 1
        if status == "REVIEW":
            review_rows.append(out)

    assert len(out_rows) == EXPECTED["phrase_keys"]
    assert route_counts["CORE_CANDIDATE"] == EXPECTED["KEEP"]
    assert len(review_rows) == EXPECTED["REVIEW"]
    assert route_counts["EXCLUDED_PRESERVED"] == (
        EXPECTED["EXCLUDE_SCOPE"] + EXPECTED["EXCLUDE_IRRELEVANT"] + EXPECTED["EXCLUDE_MECHANICAL"]
    )
    assert sum(route_counts.values()) == EXPECTED["phrase_keys"]
    assert all(r["corrected_status"] == "REVIEW" for r in review_rows)
    assert all(r["search_stage_disposition"] in {"REVIEW_SEARCH", "REVIEW_DEFERRED"} for r in review_rows)
    assert not any(r["search_stage_disposition"] in FORBIDDEN_DISPOSITIONS for r in out_rows)

    # Step 8 is a routing/freeze layer. It must never rewrite accepted Step-07C semantics.
    for src, out in zip(rows, out_rows):
        assert src["phrase"] == out["phrase"]
        assert src["corrected_status"] == out["corrected_status"]
        assert src["corrected_reason"] == out["corrected_reason"]
        assert src["provenance"] == out["provenance"]

    with OUT_SET.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(out_rows)

    review_fields = [
        "phrase", "corrected_reason", "semantic_confidence", "source_occurrences",
        "result_occurrences", "association_occurrences", "max_result_count",
        "max_association_count", "source_ids", "provenance", "search_stage_disposition",
        "next_resolution_route", "route_reason"
    ]
    with OUT_REVIEW.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=review_fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for row in review_rows:
            w.writerow({k: row[k] for k in review_fields})

    out_by_phrase = {r["phrase"]: r for r in out_rows}
    dup_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in dup_rows:
        assert row["phrase"] in out_by_phrase, row["phrase"]
        dup_groups[row["candidate_group"]].append(row)
    assert len(dup_groups) == EXPECTED["duplicate_groups"]
    assert len(dup_rows) == EXPECTED["duplicate_rows"]

    group_route = {}
    for group_id, members in dup_groups.items():
        dispositions = {out_by_phrase[m["phrase"]]["search_stage_disposition"] for m in members}
        group_route[group_id] = duplicate_group_route(dispositions)

    dup_fields = list(dup_rows[0].keys()) + [
        "step08_state", "step08_member_disposition", "step08_member_next_route", "step08_duplicate_resolution_route"
    ]
    with OUT_DUP.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=dup_fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for row in dup_rows:
            member = out_by_phrase[row["phrase"]]
            out = dict(row)
            out["step08_state"] = "UNRESOLVED_DUPLICATE_CANDIDATE"
            out["step08_member_disposition"] = member["search_stage_disposition"]
            out["step08_member_next_route"] = member["next_resolution_route"]
            out["step08_duplicate_resolution_route"] = group_route[row["candidate_group"]]
            w.writerow(out)

    frozen = read_tsv(OUT_SET)
    routed = read_tsv(OUT_REVIEW)
    dups = read_tsv(OUT_DUP)
    assert len(frozen) == EXPECTED["phrase_keys"]
    assert len(routed) == EXPECTED["REVIEW"]
    assert len(dups) == EXPECTED["duplicate_rows"]
    assert len({r["candidate_group"] for r in dups}) == EXPECTED["duplicate_groups"]
    assert all(r["step08_state"] == "UNRESOLVED_DUPLICATE_CANDIDATE" for r in dups)
    assert not any(r["step08_member_disposition"] in FORBIDDEN_DISPOSITIONS for r in dups)

    route_order = ["CORE_CANDIDATE", "REVIEW_SEARCH", "REVIEW_DEFERRED", "EXCLUDED_PRESERVED"]
    duplicate_route_counts = Counter(group_route.values())
    lines = [
        "# KW-001 / OKNO-MSK — STEP 08 SEARCH-STAGE FREEZE RECONCILIATION",
        "",
        "Date: 2026-08-29",
        "Status: **CORRECTED / MACHINE-VERIFIED / SOURCE-METHOD TRACEABILITY FIX APPLIED**",
        "",
        "## Source reconciliation",
        "",
        "```text",
        f"Step-07C phrase keys expected = {EXPECTED['phrase_keys']}",
        f"Step-08 phrase keys written = {len(frozen)}",
        f"Step-07C KEEP / CORE expected = {EXPECTED['KEEP']}",
        f"Step-08 CORE_CANDIDATE = {route_counts['CORE_CANDIDATE']}",
        f"Step-07C REVIEW expected = {EXPECTED['REVIEW']}",
        f"Step-08 REVIEW rows routed = {len(routed)}",
        f"Step-07C EXCLUDE rows expected = {EXPECTED['EXCLUDE_SCOPE'] + EXPECTED['EXCLUDE_IRRELEVANT'] + EXPECTED['EXCLUDE_MECHANICAL']}",
        f"Step-08 EXCLUDED_PRESERVED = {route_counts['EXCLUDED_PRESERVED']}",
        f"non-exact duplicate groups preserved = {len(dup_groups)}",
        f"non-exact duplicate rows preserved = {len(dups)}",
        "Step-07C semantic status rewrites = 0",
        "unrouted REVIEW = 0",
        "silent drops = 0",
        "forbidden business-route dispositions = 0",
        "provider/Search requests executed = 0",
        "provider cost = 0 RUB",
        "```",
        "",
        "## Search-stage disposition counts",
        "",
        "```text",
    ]
    for key in route_order:
        lines.append(f"{key} = {route_counts[key]}")
    lines += ["```", "", "## REVIEW routing by Step-07C reason", "", "```text"]
    for key in sorted(review_reason_counts):
        lines.append(f"{key} = {review_reason_counts[key]}")
    lines += ["```", "", "## Non-exact duplicate group routes", "", "```text"]
    for key in sorted(duplicate_route_counts):
        lines.append(f"{key} = {duplicate_route_counts[key]}")
    lines += [
        "```",
        "",
        "## Artifact hashes",
        "",
        "```text",
        f"STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv SHA-256 = {sha256(OUT_SET)}",
        f"STEP_08_REVIEW_RESOLUTION_ROUTES.tsv SHA-256 = {sha256(OUT_REVIEW)}",
        f"STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv SHA-256 = {sha256(OUT_DUP)}",
        "```",
        "",
        "## Corrected freeze semantics",
        "",
        "Step 8 routes only to evidence paths that actually exist in the workflow. Internal business priority is not a Search-stage resolution route. Public business relevance is evaluated from the known offer/scope together with Search intent; unknown margin/capacity/strategic priority belongs to later recommendation prioritization or explicit client constraints.",
        "",
        "```text",
        "STEP08_INPUT_RECONCILIATION = PASS",
        "STEP08_REVIEW_ROUTING = PASS_AFTER_METHOD_CORRECTION",
        "STEP08_FORBIDDEN_BUSINESS_ROUTE_STATES = 0",
        "STEP08_STATUS_REWRITE_COUNT = 0",
        "STEP08_NONEXACT_DUPLICATES_AUTO_MERGED = 0",
        "STEP08_PROVIDER_REQUESTS = 0",
        "STEP08_FREEZE_ARTIFACTS_READY = true",
        "```",
        "",
    ]
    OUT_RECON.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
