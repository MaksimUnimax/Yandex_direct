from __future__ import annotations

import csv
import hashlib
from collections import Counter
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

SEARCH_REASONS = {
    "AMBIGUOUS_NUMERIC_OR_FRAGMENT_INTENT",
    "ARCHITECTURE_OR_INSPIRATION_INTENT_NEEDS_SEARCH",
    "BALCONY_REGULATORY_OR_NEGATED_INTENT_NEEDS_SEARCH",
    "COMPARISON_INTENT_NEEDS_SEARCH_VALIDATION",
    "DESIGN_OR_INSPIRATION_INTENT_NEEDS_SEARCH",
    "MATERIAL_OR_PRICE_CONTEXT_NEEDS_VALIDATION",
    "NAVIGATIONAL_OR_ENTITY_INTENT_NEEDS_VALIDATION",
    "PANORAMIC_REAL_ESTATE_OR_INSPIRATION_INTENT_NEEDS_SEARCH",
    "PRIVATE_HOUSE_ADJACENT_TASK_NEEDS_VALIDATION",
    "STATE_OR_CONTEXT_FRAGMENT_NEEDS_VALIDATION",
    "TECHNICAL_INFORMATION_INTENT_NEEDS_CONTENT_FIT",
    "VAGUE_INFORMATIONAL_INTENT_NEEDS_VALIDATION",
}

SEARCH_AND_BUSINESS_REASONS = {
    "COMPONENT_OR_ACCESSORY_INTENT_NEEDS_BUSINESS_FIT",
    "DEMOLITION_SERVICE_BOUNDARY_NEEDS_VALIDATION",
    "DIY_OR_PROCEDURAL_INTENT_NEEDS_CONTENT_FIT",
    "HARDWARE_BRAND_INTENT_NEEDS_BUSINESS_FIT",
    "INSTALLATION_ADJACENT_OR_JOB_INTENT_NEEDS_VALIDATION",
    "PVC_DOOR_SUBTYPE_BUSINESS_FIT_NEEDS_VALIDATION",
    "REHAU_REPAIR_OR_DIAGNOSTIC_INTENT_NEEDS_SEARCH",
    "REPAIR_ADJACENT_INFORMATION_INTENT_NEEDS_VALIDATION",
    "REPAIR_FRAGMENT_OR_DIY_INTENT_NEEDS_VALIDATION",
    "REPAIR_NAVIGATIONAL_OR_ENTITY_INTENT_NEEDS_VALIDATION",
    "RETAINED_BUSINESS_BOUNDARY_NEEDS_SEARCH",
}

DEFERRED_REASONS = {
    "RETAINED_ASSOCIATION_ONLY_NEEDS_VALIDATION",
}


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
        return "REVIEW_SEARCH", "ORDINARY_SEARCH_NEEDED_FOR_INTENT_OR_RESULT_TYPE"
    if reason in SEARCH_AND_BUSINESS_REASONS:
        return "REVIEW_SEARCH_AND_BUSINESS", "SEARCH_EVIDENCE_AND_BUSINESS_SCOPE_BOTH_MATTER"
    if reason in DEFERRED_REASONS:
        return "REVIEW_DEFERRED", "ASSOCIATION_ONLY_EVIDENCE_RETAINED_WITHOUT_IMMEDIATE_SEARCH_CALL"
    raise AssertionError(f"Unmapped REVIEW reason: {reason}")


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
    assert all(r["search_stage_disposition"].startswith("REVIEW_") for r in review_rows)

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

    dup_groups = {r["candidate_group"] for r in dup_rows}
    assert len(dup_groups) == EXPECTED["duplicate_groups"]
    assert len(dup_rows) == EXPECTED["duplicate_rows"]
    dup_fields = list(dup_rows[0].keys()) + ["step08_state", "step08_resolution_route"]
    with OUT_DUP.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=dup_fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for row in dup_rows:
            out = dict(row)
            out["step08_state"] = "UNRESOLVED_DUPLICATE_CANDIDATE"
            out["step08_resolution_route"] = "ORDINARY_SEARCH_INTENT_OR_PAGE_BOUNDARY_CHECK"
            w.writerow(out)

    # Verify written artifacts by reading them back.
    frozen = read_tsv(OUT_SET)
    routed = read_tsv(OUT_REVIEW)
    dups = read_tsv(OUT_DUP)
    assert len(frozen) == EXPECTED["phrase_keys"]
    assert len(routed) == EXPECTED["REVIEW"]
    assert len(dups) == EXPECTED["duplicate_rows"]
    assert len({r["candidate_group"] for r in dups}) == EXPECTED["duplicate_groups"]

    route_order = ["CORE_CANDIDATE", "REVIEW_SEARCH", "REVIEW_BUSINESS", "REVIEW_SEARCH_AND_BUSINESS", "REVIEW_DEFERRED", "EXCLUDED_PRESERVED"]
    lines = [
        "# KW-001 / OKNO-MSK — STEP 08 SEARCH-STAGE FREEZE RECONCILIATION",
        "",
        "Date: 2026-08-29",
        "Status: **GENERATED / MACHINE-VERIFIED / REQUIRES STEP ACCEPTANCE**",
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
        "## Freeze semantics",
        "",
        "Step 8 preserves accepted Step-07C semantic decisions and adds only a routing layer for the next evidence stage. It does not perform clustering, page mapping, Search acquisition, business-priority resolution or automatic non-exact duplicate merging.",
        "",
        "```text",
        "STEP08_INPUT_RECONCILIATION = PASS",
        "STEP08_REVIEW_ROUTING = PASS",
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
