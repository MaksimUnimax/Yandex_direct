#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


OUT = Path(__file__).resolve().parent
JOB = OUT.parent
LEVEL1 = JOB.parent.parent
STEP5A = JOB / "STEP_05A_FIRST_EXECUTION_2026-09-08"

BASE_STEP8 = JOB / "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv"
BASE_STEP7 = JOB / "STEP_07C_SEMANTIC_CORRECTION_WORKING.tsv"
BASE_STAGE5 = JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"
BASE_UNITS = JOB / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"
DELTA = STEP5A / "STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv"
MERGE = STEP5A / "STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv"
GAPS = STEP5A / "STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv"

HOLD_PHRASES = {"окна для старого фонда", "кладовая на балконе"}
FORBIDDEN_ROUTES = {"REVIEW_BUSINESS", "REVIEW_SEARCH_AND_BUSINESS"}

# These decisions deliberately apply the corrected Step-7 rule row by row.
# KEEP requires named positive evidence. REVIEW is retained where a modifier
# introduces an untested building/material/procedure boundary.
DECISIONS = {
    "S5A-DELTA-001": (
        "KEEP", "POSITIVE_OPEN_BALCONY_WATERPROOFING_NEED_WITH_IN_SCOPE_FINISHING_PARENT_AND_EXACT_SEARCH", "HIGH",
        "The exact query has real direct Wordstat demand, a successful exact-query Search observation and an accepted in-scope open-balcony-finishing parent.",
        "NONE", "CORE_CANDIDATE", "ORDINARY_SEARCH_ELIGIBLE",
    ),
    "S5A-DELTA-002": (
        "REVIEW", "PRIVATE_HOUSE_CONTEXT_NEEDS_EXACT_SEARCH_BOUNDARY", "MEDIUM",
        "The direction is relevant, but the private-house modifier may change the user task and was not the tested exact representative query.",
        "Exact Search is required for the private-house variant before downstream grouping or page decisions.", "REVIEW_SEARCH", "REVIEW_SEARCH",
    ),
    "S5A-DELTA-003": (
        "REVIEW", "BEST_MATERIAL_SELECTION_INTENT_NEEDS_EXACT_SEARCH_BOUNDARY", "MEDIUM",
        "The waterproofing direction is relevant, but the superlative wording can indicate product comparison rather than a service task.",
        "Exact Search is required to distinguish product-selection, advice and service intent.", "REVIEW_SEARCH", "REVIEW_SEARCH",
    ),
    "S5A-DELTA-004": (
        "REVIEW", "DIY_OR_PROCEDURAL_INTENT_NEEDS_CONTENT_FIT", "LOW",
        "The phrase is real demand inside the accepted direction, but 'как сделать' explicitly introduces a do-it-yourself procedural task.",
        "Exact Search is required before deciding whether the site can answer the procedural task.", "REVIEW_SEARCH", "REVIEW_SEARCH",
    ),
    "S5A-DELTA-005": (
        "REVIEW", "WOODEN_BALCONY_MATERIAL_BOUNDARY_NEEDS_EXACT_SEARCH", "MEDIUM",
        "The accepted parent covers open-balcony finishing, but the wooden-construction modifier is not independently confirmed by the frozen offer.",
        "Exact Search and later business-fit review are required; no wooden-balcony service claim is made.", "REVIEW_SEARCH", "REVIEW_SEARCH",
    ),
    "S5A-DELTA-006": (
        "REVIEW", "BALCONY_SLAB_REPAIR_BOUNDARY_NEEDS_EXACT_SEARCH", "MEDIUM",
        "The phrase is related to waterproofing, but the slab modifier may indicate construction repair outside the general finishing task.",
        "Exact Search is required to resolve the slab-repair versus finishing boundary.", "REVIEW_SEARCH", "REVIEW_SEARCH",
    ),
    "S5A-DELTA-007": (
        "KEEP", "POSITIVE_SUN_PROTECTION_GLASS_UNIT_PRODUCT_NEED_WITH_EXACT_SEARCH", "HIGH",
        "Direct Wordstat demand, a successful exact-query commercial Search result mix and the in-scope glass-unit-selection parent jointly establish relevance.",
        "NONE", "CORE_CANDIDATE", "ORDINARY_SEARCH_ELIGIBLE",
    ),
    "S5A-DELTA-008": (
        "KEEP", "POSITIVE_SUN_PROTECTION_GLASS_VARIANT_WITH_CONFIRMED_DIRECTION", "MEDIUM",
        "This is a direct Wordstat close wording of the confirmed sun-protection glass-unit product need and does not add a new business boundary.",
        "NONE", "CORE_CANDIDATE", "ORDINARY_SEARCH_ELIGIBLE",
    ),
    "S5A-DELTA-009": (
        "KEEP", "POSITIVE_REHAU_SUN_PROTECTION_GLASS_UNIT_VARIANT_WITH_CONFIRMED_OFFER", "MEDIUM",
        "The direct Wordstat phrase combines the confirmed glass-unit need with REHAU, a frozen in-scope product brand, without creating a new service claim.",
        "NONE", "CORE_CANDIDATE", "ORDINARY_SEARCH_ELIGIBLE",
    ),
    "S5A-DELTA-010": (
        "KEEP", "POSITIVE_MULTIFUNCTIONAL_GLASS_UNIT_INFORMATION_NEED_WITH_EXACT_SEARCH", "HIGH",
        "The exact informational wording has direct Wordstat demand, a successful exact-query article-dominant Search observation and an existing glass-unit-selection information parent.",
        "NONE", "CORE_CANDIDATE", "ORDINARY_SEARCH_ELIGIBLE",
    ),
    "S5A-DELTA-011": (
        "KEEP", "POSITIVE_IMPACT_RESISTANT_GLASS_UNIT_SELECTION_NEED_WITH_EXACT_SEARCH", "HIGH",
        "Direct Wordstat demand, successful exact-query product/guide Search evidence and the in-scope glass-unit-selection parent establish relevance.",
        "NONE", "CORE_CANDIDATE", "ORDINARY_SEARCH_ELIGIBLE",
    ),
    "S5A-DELTA-012": (
        "KEEP", "POSITIVE_BALCONY_OFFICE_USE_CASE_WITH_SERVICE_DISCOVERY_SEARCH", "HIGH",
        "The exact query has direct Wordstat demand, successful use-case/service-discovery Search evidence and an in-scope balcony-renovation parent.",
        "NONE", "CORE_CANDIDATE", "ORDINARY_SEARCH_ELIGIBLE",
    ),
    "S5A-DELTA-013": (
        "KEEP", "POSITIVE_BALCONY_ROOF_SOUNDPROOFING_NEED_WITH_EXACT_SEARCH", "HIGH",
        "The exact query has direct Wordstat demand, successful Search evidence including a relevant service result and an in-scope balcony-roof service parent.",
        "NONE", "CORE_CANDIDATE", "ORDINARY_SEARCH_ELIGIBLE",
    ),
    "S5A-DELTA-014": (
        "KEEP", "POSITIVE_BALCONY_ROOF_RAIN_SOUNDPROOFING_VARIANT_WITH_CONFIRMED_DIRECTION", "MEDIUM",
        "This direct Wordstat wording remains inside the confirmed balcony-roof soundproofing problem and adds no separate construction method claim.",
        "NONE", "CORE_CANDIDATE", "ORDINARY_SEARCH_ELIGIBLE",
    ),
    "S5A-DELTA-015": (
        "REVIEW", "INSIDE_INSTALLATION_METHOD_BOUNDARY_NEEDS_EXACT_SEARCH", "MEDIUM",
        "The 'изнутри' modifier introduces a specific implementation method that the representative Search observation did not test.",
        "Exact Search is required before downstream content or service-fit decisions about an inside installation method.", "REVIEW_SEARCH", "REVIEW_SEARCH",
    ),
    "S5A-DELTA-016": (
        "KEEP", "POSITIVE_WINDOW_PROFILE_REINFORCEMENT_INFORMATION_NEED_WITH_EXACT_SEARCH", "HIGH",
        "Direct Wordstat demand, successful exact-query technical-learning Search evidence and the existing profile-selection information parent establish relevance.",
        "NONE", "CORE_CANDIDATE", "ORDINARY_SEARCH_ELIGIBLE",
    ),
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    if not root.exists():
        return "ABSENT"
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def normalize(phrase: str) -> str:
    return " ".join(re.findall(r"[а-яa-z0-9]+", phrase.lower().replace("ё", "е").replace("рехау", "rehau")))


def display_path(path: Path) -> str:
    try:
        return path.relative_to(JOB).as_posix()
    except ValueError:
        return path.relative_to(LEVEL1).as_posix()


def demand_count(row: dict[str, str]) -> str:
    return row["max_result_count"] if int(row["max_result_count"] or 0) > 0 else row["max_association_count"]


def baseline_raw_locators(source_ids: str) -> str:
    locators: list[str] = []
    for source_id in source_ids.split("|"):
        source_id = source_id.strip()
        if not source_id:
            continue
        if source_id.startswith("P2-"):
            suffix = source_id.split("-")[1]
            locators.append(f"../STEP_05_P2_{suffix}_RAW_NORMALIZED.tsv")
        else:
            locators.append(f"../STEP_03R_{source_id}_RAW_NORMALIZED.tsv")
    return " | ".join(locators)


def protected_identities() -> dict[str, object]:
    files = {
        "level1_step5a_method": LEVEL1 / "STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md",
        "level1_step_rules_index": LEVEL1 / "STEP_RULES_INDEX.md",
        "level1_lessons_ledger": LEVEL1 / "STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md",
        "level1_step8_method": LEVEL1 / "STEP_08_SEARCH_STAGE_FREEZE_METHOD.md",
        "historical_stage5_master": BASE_STAGE5,
        "historical_stage5_units": BASE_UNITS,
        "historical_step7": BASE_STEP7,
        "historical_step8": BASE_STEP8,
        "historical_step8_review_routes": JOB / "STEP_08_REVIEW_RESOLUTION_ROUTES.tsv",
        "historical_step8_duplicate_handoff": JOB / "STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv",
    }
    return {
        "files": {name: {"path": display_path(path), "sha256": sha256(path)} for name, path in files.items()},
        "trees": {
            "corrected_release": {
                "path": "../OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05",
                "sha256": tree_sha256(JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"),
            },
            "kw002": {
                "path": "../../../KW002_SEMANTIC_CORE_FROM_SCRATCH",
                "sha256": tree_sha256(LEVEL1.parent / "KW002_SEMANTIC_CORE_FROM_SCRATCH"),
            },
        },
    }


def build() -> None:
    baseline8 = read_tsv(BASE_STEP8)
    baseline7 = read_tsv(BASE_STEP7)
    stage5 = read_tsv(BASE_STAGE5)
    units = {row["structural_unit_id"]: row for row in read_tsv(BASE_UNITS)}
    delta = read_tsv(DELTA)
    merge = read_tsv(MERGE)
    gaps = {row["deduplicated_direction_id"]: row for row in read_tsv(GAPS)}

    if len(baseline8) != 2840 or len(baseline7) != 2840 or len(stage5) != 2840:
        raise AssertionError("Historical 2,840-row authorities do not reconcile")
    if len(delta) != 16 or set(DECISIONS) != {row["delta_id"] for row in delta}:
        raise AssertionError("The accepted 16-row delta does not match the row-level decision authority")

    base_by_phrase = {row["phrase"]: row for row in baseline8}
    stage5_by_phrase = {row["phrase"]: row for row in stage5}
    if len(base_by_phrase) != 2840 or len(stage5_by_phrase) != 2840:
        raise AssertionError("Historical phrase keys are not unique")
    if any(normalize(row["phrase"]) in {normalize(p) for p in base_by_phrase} for row in delta):
        raise AssertionError("Live normalization contradicts the accepted zero-overlap claim")
    if HOLD_PHRASES & {row["phrase"] for row in delta}:
        raise AssertionError("HOLD phrase entered accepted delta")

    accepted_merge = [row for row in merge if row["phrase_merge_state"] == "MERGE_ACCEPTED"]
    if {row["returned_phrase"] for row in accepted_merge} != {row["phrase"] for row in delta}:
        raise AssertionError("Merge reconciliation and accepted delta disagree")

    unit_fields = list(next(iter(units.values())).keys())
    unit_ids = set(units)
    if len(unit_ids) != 168 or len(unit_fields) < 10:
        raise AssertionError("Historical canonical-unit authority is not the expected 168-unit authority")

    union_rows: list[dict[str, object]] = []
    provenance_rows: list[dict[str, object]] = []
    freeze_rows: list[dict[str, object]] = []
    semantic_rows: list[dict[str, object]] = []

    union_fields = [
        "phrase", "normalized_phrase", "input_origin", "source_record_id", "historical_step7_status",
        "historical_step8_disposition", "source_occurrences", "result_occurrences", "association_occurrences",
        "max_result_count", "max_association_count", "source_ids", "provenance", "frequency_count",
        "frequency_evidence_state", "region", "device_scope", "operator_context", "acquisition_date",
        "acquisition_request_id", "raw_evidence_locator", "search_representative_query",
        "search_evidence_state", "step5a_direction_id", "input_state", "claim_boundary",
    ]

    provenance_fields = [
        "phrase", "demand_provenance_join_key", "input_origin", "source_record_id", "frequency_count",
        "frequency_evidence_state", "result_occurrences", "association_occurrences", "region", "device_scope",
        "operator_context", "acquisition_date", "request_or_source_ids", "raw_evidence_locator",
        "competitor_page_lineage", "search_evidence_locator", "step5a_direction_id", "join_state",
        "silent_field_loss", "claim_boundary",
    ]

    freeze_base_fields = list(baseline8[0].keys())
    freeze_extra_fields = [
        "input_origin", "source_record_id", "step5a_direction_id", "demand_provenance_join_key",
        "post_step8_authority_state",
    ]
    freeze_fields = freeze_base_fields + freeze_extra_fields

    semantic_base_fields = list(stage5[0].keys())
    semantic_extra_fields = [
        "authority_revision", "input_origin", "step5a_delta_id", "step5a_direction_id",
        "post_step8_state", "downstream_refresh_state", "demand_provenance_join_key",
    ]
    semantic_fields = semantic_base_fields + semantic_extra_fields

    for row in baseline8:
        phrase = row["phrase"]
        join_key = f"BASELINE::{phrase}"
        raw_locators = baseline_raw_locators(row["source_ids"])
        union_rows.append({
            "phrase": phrase,
            "normalized_phrase": normalize(phrase),
            "input_origin": "HISTORICAL_BASELINE_2026-09-05",
            "source_record_id": phrase,
            "historical_step7_status": row["corrected_status"],
            "historical_step8_disposition": row["search_stage_disposition"],
            "source_occurrences": row["source_occurrences"],
            "result_occurrences": row["result_occurrences"],
            "association_occurrences": row["association_occurrences"],
            "max_result_count": row["max_result_count"],
            "max_association_count": row["max_association_count"],
            "source_ids": row["source_ids"],
            "provenance": row["provenance"],
            "frequency_count": demand_count(row),
            "frequency_evidence_state": "HISTORICAL_ACCEPTED_STEP8_AGGREGATED_OCCURRENCE_COUNTS",
            "region": "213",
            "device_scope": "DEVICE_ALL",
            "operator_context": "WORDSTAT_GETTOP",
            "acquisition_date": "2026-08-29",
            "acquisition_request_id": row["source_ids"],
            "raw_evidence_locator": raw_locators,
            "search_representative_query": "",
            "search_evidence_state": "HISTORICAL_DOWNSTREAM_AUTHORITY_PRESERVED",
            "step5a_direction_id": "",
            "input_state": "BASELINE_CARRIED_UNCHANGED",
            "claim_boundary": "Historical accepted Step8 row; downstream Stage5 truth is reused without mutation.",
        })
        provenance_rows.append({
            "phrase": phrase,
            "demand_provenance_join_key": join_key,
            "input_origin": "HISTORICAL_BASELINE_2026-09-05",
            "source_record_id": phrase,
            "frequency_count": demand_count(row),
            "frequency_evidence_state": "HISTORICAL_ACCEPTED_STEP8_AGGREGATED_OCCURRENCE_COUNTS",
            "result_occurrences": row["result_occurrences"],
            "association_occurrences": row["association_occurrences"],
            "region": "213",
            "device_scope": "DEVICE_ALL",
            "operator_context": "WORDSTAT_GETTOP",
            "acquisition_date": "2026-08-29",
            "request_or_source_ids": row["source_ids"],
            "raw_evidence_locator": raw_locators,
            "competitor_page_lineage": "NOT_APPLICABLE_HISTORICAL_BASELINE",
            "search_evidence_locator": "Historical downstream authorities; no new Search performed in propagation.",
            "step5a_direction_id": "",
            "join_state": "COMPLETE_DETERMINISTIC_PHRASE_AND_SOURCE_ID_JOIN",
            "silent_field_loss": "0",
            "claim_boundary": "Reuses the accepted historical demand/provenance route; does not claim new provider evidence.",
        })
        frozen = dict(row)
        frozen.update({
            "input_origin": "HISTORICAL_BASELINE_2026-09-05",
            "source_record_id": phrase,
            "step5a_direction_id": "",
            "demand_provenance_join_key": join_key,
            "post_step8_authority_state": "HISTORICAL_STEP8_ROW_CARRIED_UNCHANGED",
        })
        freeze_rows.append(frozen)
        semantic = dict(stage5_by_phrase[phrase])
        semantic.update({
            "authority_revision": "POST_STEP5A_STEP8_2026-09-08",
            "input_origin": "HISTORICAL_BASELINE_2026-09-05",
            "step5a_delta_id": "",
            "step5a_direction_id": "",
            "post_step8_state": row["search_stage_disposition"],
            "downstream_refresh_state": "HISTORICAL_FINAL_FIELDS_PRESERVED_UNCHANGED",
            "demand_provenance_join_key": join_key,
        })
        semantic_rows.append(semantic)

    cleanup_rows: list[dict[str, object]] = []
    impact_rows: list[dict[str, object]] = []
    cleanup_fields = [
        "delta_id", "phrase", "normalized_phrase", "frequency_count", "step5a_direction_id",
        "step7_status", "step7_reason", "semantic_confidence", "positive_evidence_or_review_basis",
        "business_scope_fit", "semantic_relevance", "duplicate_decision", "uncertainty_state",
        "search_required_reason", "source_provenance", "historical_row_interactions", "step8_disposition",
        "next_resolution_route", "claim_boundary",
    ]
    impact_fields = [
        "delta_id", "phrase", "step5a_direction_id", "step7_status", "step8_disposition",
        "step9_existing_evidence_use", "step9_additional_search_requirement", "step10_refresh",
        "candidate_existing_unit_for_recheck", "candidate_historical_primary_page_for_recheck",
        "step11_refresh", "step12_refresh", "step13_trigger", "step14_refresh", "step15_refresh",
        "step16_provider_call_state", "step17_refresh", "step18_refresh", "step19_refresh",
        "step20_refresh", "final_ownership_state", "final_physical_action_state", "claim_boundary",
    ]

    for row in delta:
        delta_id = row["delta_id"]
        phrase = row["phrase"]
        status, reason, confidence, basis, search_reason, disposition, next_route = DECISIONS[delta_id]
        join_key = f"STEP5A::{delta_id}"
        direction = row["step5a_direction_id"]
        gap = gaps[direction]
        authority = gap["frozen_business_scope_authority"]
        unit_id = authority.split("unit:", 1)[1] if authority.startswith("unit:") else ""
        if unit_id and unit_id not in units:
            raise AssertionError(f"Unknown historical unit reference: {unit_id}")
        historical_page = units[unit_id]["final_primary_page"] if unit_id else ""
        raw_locator = f"../STEP_05A_FIRST_EXECUTION_2026-09-08/{row['wordstat_raw_item_file']}"
        search_locator = f"../STEP_05A_FIRST_EXECUTION_2026-09-08/{row['search_raw_item_file']}"
        source_provenance = f"{row['wordstat_row_id']} | {row['wordstat_request_id']} | {raw_locator}"

        union_rows.append({
            "phrase": phrase,
            "normalized_phrase": normalize(phrase),
            "input_origin": "COMPETITOR_DERIVED_STEP5A",
            "source_record_id": delta_id,
            "historical_step7_status": "NOT_APPLICABLE_NEW_ROW",
            "historical_step8_disposition": "NOT_APPLICABLE_NEW_ROW",
            "source_occurrences": "1",
            "result_occurrences": "1",
            "association_occurrences": "0",
            "max_result_count": row["frequency_count"],
            "max_association_count": "0",
            "source_ids": delta_id,
            "provenance": source_provenance,
            "frequency_count": row["frequency_count"],
            "frequency_evidence_state": row["frequency_evidence_state"],
            "region": row["region"],
            "device_scope": row["device_scope"],
            "operator_context": row["operator_context"],
            "acquisition_date": "2026-09-08",
            "acquisition_request_id": row["wordstat_request_id"],
            "raw_evidence_locator": raw_locator,
            "search_representative_query": row["search_representative_query"],
            "search_evidence_state": row["search_evidence_state"],
            "step5a_direction_id": direction,
            "input_state": "OWNER_ACCEPTED_ADD_TO_PIPELINE__PENDING_STEP7",
            "claim_boundary": row["claim_boundary"],
        })
        cleanup_rows.append({
            "delta_id": delta_id,
            "phrase": phrase,
            "normalized_phrase": normalize(phrase),
            "frequency_count": row["frequency_count"],
            "step5a_direction_id": direction,
            "step7_status": status,
            "step7_reason": reason,
            "semantic_confidence": confidence,
            "positive_evidence_or_review_basis": basis,
            "business_scope_fit": gap["frozen_business_scope_state"],
            "semantic_relevance": "POSITIVE_EVIDENCE_ESTABLISHED" if status == "KEEP" else "RELEVANT_DIRECTION_WITH_UNRESOLVED_EXACT_BOUNDARY",
            "duplicate_decision": "NO_EXACT_OR_NORMALIZED_BASELINE_COLLISION__NO_NONEXACT_AUTO_MERGE",
            "uncertainty_state": "NONE" if status == "KEEP" else "SEARCH_REQUIRED",
            "search_required_reason": search_reason,
            "source_provenance": source_provenance,
            "historical_row_interactions": "0",
            "step8_disposition": disposition,
            "next_resolution_route": next_route,
            "claim_boundary": "Step7 semantic admission/routing only; no cluster, page owner, page creation or implementation decision.",
        })
        provenance_rows.append({
            "phrase": phrase,
            "demand_provenance_join_key": join_key,
            "input_origin": "COMPETITOR_DERIVED_STEP5A",
            "source_record_id": delta_id,
            "frequency_count": row["frequency_count"],
            "frequency_evidence_state": row["frequency_evidence_state"],
            "result_occurrences": "1",
            "association_occurrences": "0",
            "region": row["region"],
            "device_scope": row["device_scope"],
            "operator_context": row["operator_context"],
            "acquisition_date": "2026-09-08",
            "request_or_source_ids": f"{delta_id} | {row['wordstat_row_id']} | {row['wordstat_request_id']}",
            "raw_evidence_locator": raw_locator,
            "competitor_page_lineage": f"{row['competitor_page_evidence_ids']} | {row['competitor_page_urls']}",
            "search_evidence_locator": f"{row['search_representative_query']} | {search_locator} | {row['search_request_id']}",
            "step5a_direction_id": direction,
            "join_state": "COMPLETE_DETERMINISTIC_DELTA_ID_AND_WORDSTAT_ROW_JOIN",
            "silent_field_loss": "0",
            "claim_boundary": "Actual persisted Step5A Wordstat occurrence and representative Search lineage; no new provider observation.",
        })
        frozen = {key: "" for key in freeze_base_fields}
        frozen.update({
            "phrase": phrase,
            "historical_status": "ADD_TO_PIPELINE",
            "historical_reason": "OWNER_ACCEPTED_STEP5A_ACQUISITION_DELTA",
            "corrected_status": status,
            "corrected_reason": reason,
            "semantic_confidence": confidence,
            "source_occurrences": "1",
            "result_occurrences": "1",
            "association_occurrences": "0",
            "max_result_count": row["frequency_count"],
            "max_association_count": "0",
            "source_ids": delta_id,
            "provenance": source_provenance,
            "search_stage_disposition": disposition,
            "next_resolution_route": next_route,
            "route_reason": "ACCEPTED_POST_STEP5A_STEP7_KEEP_WITH_POSITIVE_EVIDENCE" if status == "KEEP" else "POST_STEP5A_EXACT_SEARCH_NEEDED_TO_RESOLVE_VARIANT_BOUNDARY",
            "input_origin": "COMPETITOR_DERIVED_STEP5A",
            "source_record_id": delta_id,
            "step5a_direction_id": direction,
            "demand_provenance_join_key": join_key,
            "post_step8_authority_state": "VERSIONED_POST_STEP5A_FREEZE__DOWNSTREAM_NOT_YET_FINAL",
        })
        freeze_rows.append(frozen)
        semantic = {key: "" for key in semantic_base_fields}
        semantic.update({
            "phrase": phrase,
            "final_semantic_state": "NOT_YET_FINAL__POST_STEP8",
            "uncertainty_state": "SEARCH_REQUIRED" if status == "REVIEW" else "PENDING_STEP10_ASSIGNMENT",
            "search_stage_disposition": disposition,
            "next_resolution_route": next_route,
            "semantic_confidence": confidence,
            "source_occurrences": "1",
            "result_occurrences": "1",
            "association_occurrences": "0",
            "step10_assignment_status": "NOT_RUN_POST_STEP5A",
            "step11_effective_assignment_status": "NOT_RUN_POST_STEP5A",
            "canonical_business_scope_state": gap["frozen_business_scope_state"],
            "final_structural_unit_id": "",
            "final_primary_page": "",
            "canonical_structural_action": "",
            "explicit_missing_needs": "Targeted downstream refresh required by impact register.",
            "correction_lineage": delta_id,
            "authority_lineage": "STEP5A_DELTA>STEP7_POST_ACCEPTANCE>STEP8_POST_ACCEPTANCE",
            "claim_boundary": "Post-Step8 routing authority only; no final cluster, page ownership or physical action assigned.",
            "authority_revision": "POST_STEP5A_STEP8_2026-09-08",
            "input_origin": "COMPETITOR_DERIVED_STEP5A",
            "step5a_delta_id": delta_id,
            "step5a_direction_id": direction,
            "post_step8_state": disposition,
            "downstream_refresh_state": "TARGETED_STEP9_PLUS_REFRESH_REQUIRED",
            "demand_provenance_join_key": join_key,
        })
        semantic_rows.append(semantic)

        additional_search = "REQUIRED__NO_CALL_EXECUTED" if status == "REVIEW" else "NOT_REQUIRED_FOR_STEP7_ADMISSION__REASSESS_AT_STEP9_BOUNDARY"
        impact_rows.append({
            "delta_id": delta_id,
            "phrase": phrase,
            "step5a_direction_id": direction,
            "step7_status": status,
            "step8_disposition": disposition,
            "step9_existing_evidence_use": f"REUSE_DIRECTION_REPRESENTATIVE_QUERY::{row['search_representative_query']}::{row['search_raw_item_file']}",
            "step9_additional_search_requirement": additional_search,
            "step10_refresh": "TARGETED_PHRASE_ASSIGNMENT_AND_DIRECTION_MEMBER_REBUILD_REQUIRED",
            "candidate_existing_unit_for_recheck": unit_id,
            "candidate_historical_primary_page_for_recheck": historical_page,
            "step11_refresh": "TARGETED_PAGE_OWNERSHIP_RECHECK_REQUIRED__CANDIDATE_ONLY_NOT_FINAL",
            "step12_refresh": {
                "OPEN_BALCONY_WATERPROOFING": "CONTENT_BLOCK_OR_SEMANTIC_MAPPING_REVIEW",
                "SUN_PROTECTION_GLASS_UNIT": "GLASS_UNIT_CONTENT_BLOCK_OR_SEMANTIC_MAPPING_REVIEW",
                "MULTIFUNCTIONAL_GLASS_UNIT": "GLASS_UNIT_INFORMATION_CONTENT_REVIEW",
                "IMPACT_RESISTANT_GLASS_UNIT": "GLASS_UNIT_PRODUCT_SELECTION_CONTENT_REVIEW",
                "BALCONY_AS_OFFICE": "BALCONY_USE_CASE_CONTENT_OR_MAPPING_REVIEW",
                "BALCONY_ROOF_SOUNDPROOFING": "ROOF_SERVICE_SCOPE_CONTENT_OR_MAPPING_REVIEW",
                "WINDOW_PROFILE_REINFORCEMENT": "PROFILE_SELECTION_INFORMATION_CONTENT_REVIEW",
            }[direction],
            "step13_trigger": "EVALUATE_COMPETING_PAGE_TRIGGER_AFTER_STEP11_12__NO_CURRENT_VERDICT",
            "step14_refresh": "TARGETED_SEARCH_ONLY_ARCHITECTURE_REFRESH_REQUIRED_AFTER_OWNERSHIP",
            "step15_refresh": "AI_CASE_SELECTION_RECONSIDERATION_REQUIRED_AFTER_STEP14",
            "step16_provider_call_state": "NOT_AUTHORIZED__0_CALLS__CONDITIONAL_ONLY_AFTER_SEPARATE_APPROVAL",
            "step17_refresh": "CONDITIONAL_IF_STEP15_SELECTS_DIRECTION_AND_STEP16_EVIDENCE_EXISTS",
            "step18_refresh": "TARGETED_PRIORITY_AND_READINESS_REFRESH_AFTER_STEP12",
            "step19_refresh": "REGENERATE_AFFECTED_CLIENT_VIEWS_AFTER_UPSTREAM_RESOLUTION",
            "step20_refresh": "FULL_NEW_VERSION_RELEASE_QA_REQUIRED",
            "final_ownership_state": "NOT_DECIDED",
            "final_physical_action_state": "NOT_DECIDED",
            "claim_boundary": "Impact/re-run requirement only; candidate unit/page references are historical recheck targets, not final assignments.",
        })

    write_tsv(OUT / "STEP_05A_POST_ACCEPTANCE_UNION_INPUT.tsv", union_rows, union_fields)
    write_tsv(OUT / "STEP_05A_DELTA_STEP07_CLEANUP_DECISIONS.tsv", cleanup_rows, cleanup_fields)
    write_tsv(OUT / "STEP_05A_POST_ACCEPTANCE_STEP08_FREEZE.tsv", freeze_rows, freeze_fields)
    write_tsv(OUT / "STEP_05A_POST_ACCEPTANCE_DEMAND_PROVENANCE_RECONCILIATION.tsv", provenance_rows, provenance_fields)
    write_tsv(OUT / "STEP_05A_POST_ACCEPTANCE_SEMANTIC_AUTHORITY.tsv", semantic_rows, semantic_fields)
    write_tsv(OUT / "STEP_05A_POST_ACCEPTANCE_DOWNSTREAM_IMPACT_REGISTER.tsv", impact_rows, impact_fields)

    protected = protected_identities()
    write_json(OUT / "PROTECTED_ARTIFACT_IDENTITIES.json", protected)

    step7_counts = Counter(row["step7_status"] for row in cleanup_rows)
    step8_counts = Counter(row["search_stage_disposition"] for row in freeze_rows)
    directions = sorted({row["step5a_direction_id"] for row in cleanup_rows})
    candidate_units = sorted({row["candidate_existing_unit_for_recheck"] for row in impact_rows if row["candidate_existing_unit_for_recheck"]})
    search_requirements = sum(row["step9_additional_search_requirement"].startswith("REQUIRED") for row in impact_rows)

    manifest = {
        "step": "STEP5A_POST_ACCEPTANCE_PROPAGATION_THROUGH_STEP7_STEP8",
        "job": "OKNO_MSK",
        "source_head": "c65deccf63a14cc4bfa47c87f8d59761df8fde59",
        "method_authorities": [
            "../../../STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md",
            "../../../STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md",
            "../../../STEP_08_SEARCH_STAGE_FREEZE_METHOD.md",
            "../STEP_05A_ACCEPTED_DELTA_PROPAGATION_STEP07_STEP08_WORK_HANDOFF_2026-09-08.md",
        ],
        "input_universe": {"historical": 2840, "accepted_delta": 16, "union": 2856, "hold_excluded": 2},
        "reuse_existing_evidence": True,
        "planned_provider_calls": 0,
        "executed_provider_calls": 0,
        "external_web_calls": 0,
        "current_scope": "STEP7_STEP8_AND_DOWNSTREAM_IMPACT_ONLY",
        "claim_boundaries": [
            "No final Step10 cluster assignment in this task.",
            "No final Step11 page ownership in this task.",
            "No Step12 physical action or page creation in this task.",
            "No Step9, Step16 or substitute web/provider call in this task.",
        ],
        "acceptance_requirements": {
            "union_rows": 2856,
            "delta_rows_accounted": 16,
            "step7_row_reasoning": "required",
            "step8_complete_routing": "required",
            "demand_provenance_join_coverage": "100%",
            "protected_artifacts_unchanged": True,
            "remote_readback": "required_after_commit",
        },
        "implementation_files": [
            "build_post_acceptance_propagation.py",
            "validate_post_acceptance_propagation.py",
            "STEP_05A_POST_ACCEPTANCE_EXECUTION_RECEIPT.md",
        ],
    }
    write_json(OUT / "STEP_05A_POST_ACCEPTANCE_EXECUTION_MANIFEST.json", manifest)

    report = f"""# OKNO_MSK — STEP 5A POST-ACCEPTANCE PROPAGATION REPORT

Date: 2026-09-08
Scope: **Step 7 cleanup + Step 8 versioned refreeze + downstream impact mapping only**

## Verdict

```text
STEP7_POST_STEP5A_PROPAGATION = COMPLETE
STEP8_POST_STEP5A_REFREEZE = COMPLETE
DOWNSTREAM_IMPACT_MAPPING = COMPLETE
STEP9_PLUS_EXECUTION = NOT_STARTED
PROVIDER_CALLS = 0
HISTORICAL_RELEASE_OVERWRITES = 0
```

## Why this work was required

The owner accepted 16 competitor-derived phrases as acquisition additions, not as automatic final keywords or page decisions. This propagation applies the normal row-level cleanup and Search-stage routing rules before any later grouping, page ownership or implementation decision.

## Input accounting

```text
historical phrase rows = 2840
accepted Step5A rows = 16
pre-cleanup union rows = 2856
normalized baseline collisions = 0
HOLD directions inserted = 0
historical Step7 rows changed = 0
```

The unresolved `окна для старого фонда` and `кладовая на балконе` directions remain outside the accepted input.

## Step 7 result

```text
KEEP with explicit positive evidence = {step7_counts['KEEP']}
REVIEW requiring exact Search = {step7_counts['REVIEW']}
new exclusions = {step7_counts.get('EXCLUDE_SCOPE', 0) + step7_counts.get('EXCLUDE_IRRELEVANT', 0) + step7_counts.get('EXCLUDE_MECHANICAL', 0)}
delta rows accounted = {sum(step7_counts.values())}/16
```

The six REVIEW rows contain modifiers that introduce a private-house, product-selection, DIY, wooden-construction, slab-repair or inside-installation boundary. They are preserved rather than forced into KEEP.

## Step 8 versioned refreeze

```text
CORE_CANDIDATE = {step8_counts['CORE_CANDIDATE']}
REVIEW_SEARCH = {step8_counts['REVIEW_SEARCH']}
REVIEW_DEFERRED = {step8_counts['REVIEW_DEFERRED']}
EXCLUDED_PRESERVED = {step8_counts['EXCLUDED_PRESERVED']}
TOTAL = {sum(step8_counts.values())}
```

Change from historical Step8:

```text
CORE_CANDIDATE delta = +{step8_counts['CORE_CANDIDATE'] - 1388}
REVIEW_SEARCH delta = +{step8_counts['REVIEW_SEARCH'] - 944}
preserved-universe delta = +{sum(step8_counts.values()) - 2840}
final Stage5 active delta = NOT YET DECIDED
```

The historical 2026-09-05 freeze remains unchanged. The new files are a separate post-Step5A version.

## Demand/provenance result

All 2,856 phrase rows have a deterministic demand/provenance join key. Historical rows retain their accepted source IDs and occurrence paths. New rows retain exact Step5A delta ID, Wordstat row/request/raw file, region, device, operator, competitor-page lineage and representative Search evidence.

```text
phrase-key join coverage = 2856/2856
silent field loss = 0
new provider recollection = 0
```

## Downstream impact

```text
new phrases requiring targeted downstream processing = 16
affected demand directions = {len(directions)}
historical candidate structural units requiring recheck = {len(candidate_units)}
final affected clusters = UNRESOLVED UNTIL STEP10
additional exact Step9 Search requirements = {search_requirements}
Step10 phrase assignments/member rebuilds required = 16 rows / 7 directions
Step11 ownership rechecks required = 7 directions
Step12 action/content rechecks required = 7 directions
Step13 trigger evaluations required = 7 directions
Step14 targeted architecture refreshes required = 7 directions
Step15 AI case-selection reconsiderations required = 7 directions
Step16 calls authorized/executed = 0/0
Step17 conditional refresh directions = 7
Steps18-20 affected-output refresh = REQUIRED AFTER UPSTREAM RESOLUTION
```

Historical unit/page references in the impact register are only recheck candidates. They are not new final ownership decisions.

## Updated full roadmap

| Work stage | Current truth |
|---|---|
| Scope, site model and original demand acquisition | ✅ Historical accepted work preserved |
| Original Step 7–8 and downstream research/release | ✅ Historical accepted authorities preserved |
| Step 5A competitor expansion and owner acceptance | ✅ Complete and canonized |
| Propagate 16 rows through Step 7 | ✅ Complete in this versioned workspace |
| Create post-Step5A Step 8 freeze | ✅ Complete in this versioned workspace |
| Map affected downstream work | ✅ Complete in this versioned workspace |
| Step 9 targeted Search resolution | ⬜ Not executed; 6 exact requirements recorded |
| Step 10 grouping/user-task refresh | ⬜ Not executed; 16 rows / 7 directions affected |
| Step 11 page-ownership refresh | ⬜ Not executed; 7 directions require recheck |
| Step 12–18 decision/action refresh | ⬜ Not executed; targeted impact recorded |
| Step 19 client deliverable rebuild | ⬜ Not executed |
| Step 20 new-release QA | ⬜ Not executed |
| Owner acceptance and close | ⬜ Not executed |

## Completed work

- All 2,840 historical phrases were carried exactly once without changing historical Step7/Step8/Stage5 authorities.
- All 16 owner-accepted Step5A phrases were accounted exactly once.
- Ten new rows received KEEP only with explicit positive evidence; six remain REVIEW_SEARCH.
- A separate 2,856-row Step8 freeze and semantic handoff were materialized.
- Every new phrase received an explicit Step9–20 impact route.
- No provider, web or competitor-page calls were performed.

## Remaining work

1. Execute only the six recorded Step9 exact Search requirements after separate authorization.
2. Refresh Step10 assignments for the 16 phrases and seven directions.
3. Refresh Step11–14 only for affected directions and any newly discovered dependent rows.
4. Reconsider Step15 selection; perform Step16 calls only if later separately authorized.
5. Refresh affected Step17–18 decisions.
6. Rebuild client documents/workbook from the new resolved authority.
7. Run new-release QA, remote readback and owner acceptance.

## Plain-language result

The 16 phrases are no longer sitting in a separate competitor-analysis file. They have entered the real semantic process. Ten are sufficiently relevant to become candidates for later grouping; six remain deliberately unresolved because their wording may change the user's task. Nothing has yet been turned into a new page or a site change. The next work is now bounded: resolve six exact Search questions and refresh only the seven affected directions.

```text
NEXT_STEP_ALLOWED = true
NEXT_ACTION = EXECUTE_ONLY_TARGETED_DOWNSTREAM_REFRESH_REQUIRED_BY_POST_STEP5A_STEP8_IMPACT_REGISTER
```
"""
    (OUT / "STEP_05A_POST_ACCEPTANCE_PROPAGATION_REPORT.md").write_text(report, encoding="utf-8")

    checkpoint = f"""# CHECKPOINT 00 — POST-STEP5A PROPAGATION MATERIALIZED

Date: 2026-09-08

```text
BASELINE_ROWS = 2840
DELTA_ROWS = 16
UNION_ROWS = 2856
STEP7_KEEP = {step7_counts['KEEP']}
STEP7_REVIEW = {step7_counts['REVIEW']}
STEP8_CORE_CANDIDATE = {step8_counts['CORE_CANDIDATE']}
STEP8_REVIEW_SEARCH = {step8_counts['REVIEW_SEARCH']}
STEP8_REVIEW_DEFERRED = {step8_counts['REVIEW_DEFERRED']}
STEP8_EXCLUDED_PRESERVED = {step8_counts['EXCLUDED_PRESERVED']}
ADDITIONAL_STEP9_SEARCH_REQUIREMENTS = {search_requirements}
PROVIDER_CALLS = 0
```

Historical release, Stage5, Step7, Step8, Level1 and KW002 identities are recorded in `PROTECTED_ARTIFACT_IDENTITIES.json` for validator comparison.
"""
    (OUT / "CHECKPOINT_00_PROPAGATION_MATERIALIZED.md").write_text(checkpoint, encoding="utf-8")

    data_artifacts = [
        "STEP_05A_POST_ACCEPTANCE_UNION_INPUT.tsv",
        "STEP_05A_DELTA_STEP07_CLEANUP_DECISIONS.tsv",
        "STEP_05A_POST_ACCEPTANCE_STEP08_FREEZE.tsv",
        "STEP_05A_POST_ACCEPTANCE_DEMAND_PROVENANCE_RECONCILIATION.tsv",
        "STEP_05A_POST_ACCEPTANCE_SEMANTIC_AUTHORITY.tsv",
        "STEP_05A_POST_ACCEPTANCE_DOWNSTREAM_IMPACT_REGISTER.tsv",
        "STEP_05A_POST_ACCEPTANCE_EXECUTION_MANIFEST.json",
        "STEP_05A_POST_ACCEPTANCE_PROPAGATION_REPORT.md",
        "CHECKPOINT_00_PROPAGATION_MATERIALIZED.md",
        "STEP_05A_POST_ACCEPTANCE_EXECUTION_RECEIPT.md",
        "PROTECTED_ARTIFACT_IDENTITIES.json",
    ]
    qa_seed = {
        "status": "PENDING_INDEPENDENT_VALIDATOR",
        "counts": {
            "baseline_rows": len(baseline8),
            "delta_rows": len(delta),
            "union_rows": len(union_rows),
            "step7_status_counts": dict(step7_counts),
            "step8_disposition_counts": dict(step8_counts),
            "affected_directions": len(directions),
            "candidate_existing_units": len(candidate_units),
            "additional_step9_search_requirements": search_requirements,
            "provider_calls": 0,
        },
        "artifact_sha256": {name: sha256(OUT / name) for name in data_artifacts},
    }
    write_json(OUT / "STEP_05A_POST_ACCEPTANCE_PROPAGATION_QA.json", qa_seed)


if __name__ == "__main__":
    build()
