#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


OUT = Path(__file__).resolve().parent
JOB = OUT.parent
LEVEL1 = JOB.parent.parent
STEP5A = JOB / "STEP_05A_FIRST_EXECUTION_2026-09-08"

BASE_STEP7 = JOB / "STEP_07C_SEMANTIC_CORRECTION_WORKING.tsv"
BASE_STEP8 = JOB / "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv"
BASE_STAGE5 = JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"
DELTA = STEP5A / "STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv"

UNION = OUT / "STEP_05A_POST_ACCEPTANCE_UNION_INPUT.tsv"
CLEANUP = OUT / "STEP_05A_DELTA_STEP07_CLEANUP_DECISIONS.tsv"
FREEZE = OUT / "STEP_05A_POST_ACCEPTANCE_STEP08_FREEZE.tsv"
PROVENANCE = OUT / "STEP_05A_POST_ACCEPTANCE_DEMAND_PROVENANCE_RECONCILIATION.tsv"
SEMANTIC = OUT / "STEP_05A_POST_ACCEPTANCE_SEMANTIC_AUTHORITY.tsv"
IMPACT = OUT / "STEP_05A_POST_ACCEPTANCE_DOWNSTREAM_IMPACT_REGISTER.tsv"
PROTECTED = OUT / "PROTECTED_ARTIFACT_IDENTITIES.json"
QA = OUT / "STEP_05A_POST_ACCEPTANCE_PROPAGATION_QA.json"

HOLD_PHRASES = {"окна для старого фонда", "кладовая на балконе"}
ALLOWED_STEP8 = {"CORE_CANDIDATE", "REVIEW_SEARCH", "REVIEW_DEFERRED", "EXCLUDED_PRESERVED"}
FORBIDDEN_STEP8 = {"REVIEW_BUSINESS", "REVIEW_SEARCH_AND_BUSINESS"}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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


def require(condition: bool, name: str, checks: list[dict[str, str]]) -> None:
    if not condition:
        raise AssertionError(name)
    checks.append({"check": name, "status": "PASS"})


def validate() -> None:
    checks: list[dict[str, str]] = []
    baseline7 = read_tsv(BASE_STEP7)
    baseline8 = read_tsv(BASE_STEP8)
    stage5 = read_tsv(BASE_STAGE5)
    delta = read_tsv(DELTA)
    union = read_tsv(UNION)
    cleanup = read_tsv(CLEANUP)
    freeze = read_tsv(FREEZE)
    provenance = read_tsv(PROVENANCE)
    semantic = read_tsv(SEMANTIC)
    impact = read_tsv(IMPACT)

    require(len(baseline7) == len(baseline8) == len(stage5) == 2840, "historical_authorities_are_2840_rows", checks)
    require(len(delta) == len(cleanup) == len(impact) == 16, "accepted_delta_cleanup_and_impact_are_16_rows", checks)
    require(len(union) == len(freeze) == len(provenance) == len(semantic) == 2856, "all_full_universe_outputs_are_2856_rows", checks)

    delta_phrases = {row["phrase"] for row in delta}
    baseline_phrases = {row["phrase"] for row in baseline8}
    require(len(delta_phrases) == 16 and not delta_phrases & baseline_phrases, "delta_is_unique_and_exactly_disjoint_from_baseline", checks)
    require(not HOLD_PHRASES & delta_phrases, "hold_phrases_are_absent_from_delta", checks)
    require({row["phrase"] for row in union} == baseline_phrases | delta_phrases, "union_phrase_set_is_exact", checks)
    require(len({row["phrase"] for row in union}) == 2856, "union_has_no_duplicate_phrase_keys", checks)

    baseline7_by_phrase = {row["phrase"]: row for row in baseline7}
    baseline8_by_phrase = {row["phrase"]: row for row in baseline8}
    stage5_by_phrase = {row["phrase"]: row for row in stage5}
    freeze_by_phrase = {row["phrase"]: row for row in freeze}
    semantic_by_phrase = {row["phrase"]: row for row in semantic}
    union_by_phrase = {row["phrase"]: row for row in union}

    require(all(union_by_phrase[p]["historical_step7_status"] == baseline7_by_phrase[p]["corrected_status"] for p in baseline_phrases), "baseline_step7_states_are_carried_exactly", checks)
    require(all(union_by_phrase[p]["historical_step8_disposition"] == baseline8_by_phrase[p]["search_stage_disposition"] for p in baseline_phrases), "baseline_step8_states_are_carried_exactly", checks)
    freeze_base_fields = list(baseline8[0])
    require(all(all(freeze_by_phrase[p][field] == baseline8_by_phrase[p][field] for field in freeze_base_fields) for p in baseline_phrases), "historical_step8_rows_are_field_exact", checks)
    stage5_fields = list(stage5[0])
    require(all(all(semantic_by_phrase[p][field] == stage5_by_phrase[p][field] for field in stage5_fields) for p in baseline_phrases), "historical_stage5_fields_are_preserved_exactly", checks)

    cleanup_counts = Counter(row["step7_status"] for row in cleanup)
    require(cleanup_counts == Counter({"KEEP": 10, "REVIEW": 6}), "step7_delta_counts_are_10_keep_6_review", checks)
    require(all(row["positive_evidence_or_review_basis"].strip() for row in cleanup), "every_step7_row_has_explicit_evidence_or_review_basis", checks)
    require(all(row["step7_reason"].strip() and row["claim_boundary"].strip() for row in cleanup), "every_step7_row_has_reason_and_claim_boundary", checks)
    require(all(row["semantic_relevance"] == "POSITIVE_EVIDENCE_ESTABLISHED" for row in cleanup if row["step7_status"] == "KEEP"), "keep_rows_name_positive_evidence", checks)
    require(all(row["search_required_reason"].strip() not in {"", "NONE"} for row in cleanup if row["step7_status"] == "REVIEW"), "review_rows_preserve_exact_search_requirement", checks)
    require(all(row["historical_row_interactions"] == "0" for row in cleanup), "delta_cleanup_does_not_mutate_historical_rows", checks)

    step8_counts = Counter(row["search_stage_disposition"] for row in freeze)
    require(step8_counts == Counter({"CORE_CANDIDATE": 1398, "REVIEW_SEARCH": 950, "REVIEW_DEFERRED": 174, "EXCLUDED_PRESERVED": 334}), "step8_refreeze_counts_reconcile", checks)
    require(set(step8_counts) <= ALLOWED_STEP8 and not set(step8_counts) & FORBIDDEN_STEP8, "step8_uses_only_allowed_dispositions", checks)
    cleanup_by_phrase = {row["phrase"]: row for row in cleanup}
    require(all(freeze_by_phrase[p]["search_stage_disposition"] == cleanup_by_phrase[p]["step8_disposition"] for p in delta_phrases), "delta_step7_to_step8_mapping_is_exact", checks)

    provenance_by_phrase = {row["phrase"]: row for row in provenance}
    require(len(provenance_by_phrase) == 2856, "provenance_has_one_unique_row_per_phrase", checks)
    require(all(row["demand_provenance_join_key"].strip() for row in provenance), "all_provenance_join_keys_are_present", checks)
    require(len({row["demand_provenance_join_key"] for row in provenance}) == 2856, "all_provenance_join_keys_are_unique", checks)
    require(all(row["join_state"].startswith("COMPLETE_DETERMINISTIC") and row["silent_field_loss"] == "0" for row in provenance), "all_provenance_joins_are_complete_without_silent_loss", checks)
    require(all(row["frequency_count"].strip() and row["raw_evidence_locator"].strip() for row in provenance), "all_rows_retain_demand_count_and_raw_locator", checks)
    require(all(provenance_by_phrase[p]["competitor_page_lineage"] != "NOT_APPLICABLE_HISTORICAL_BASELINE" for p in delta_phrases), "delta_retains_competitor_page_lineage", checks)
    require(all(provenance_by_phrase[p]["search_evidence_locator"].strip() for p in delta_phrases), "delta_retains_representative_search_lineage", checks)

    new_semantic = [semantic_by_phrase[p] for p in delta_phrases]
    require(all(row["final_semantic_state"] == "NOT_YET_FINAL__POST_STEP8" for row in new_semantic), "new_rows_are_not_misrepresented_as_final_stage5_truth", checks)
    require(all(not row["final_structural_unit_id"] and not row["final_primary_page"] and not row["canonical_structural_action"] for row in new_semantic), "new_rows_have_no_premature_unit_page_or_action_assignment", checks)
    require(all(row["downstream_refresh_state"] == "TARGETED_STEP9_PLUS_REFRESH_REQUIRED" for row in new_semantic), "new_rows_are_routed_to_targeted_downstream_refresh", checks)

    require(len({row["step5a_direction_id"] for row in impact}) == 7, "impact_register_covers_seven_directions", checks)
    require(sum(row["step9_additional_search_requirement"].startswith("REQUIRED") for row in impact) == 6, "impact_register_contains_six_exact_step9_requirements", checks)
    require(all(row["step10_refresh"].startswith("TARGETED") and row["step11_refresh"].startswith("TARGETED") for row in impact), "all_delta_rows_have_targeted_step10_and_step11_routes", checks)
    require(all(row["step16_provider_call_state"] == "NOT_AUTHORIZED__0_CALLS__CONDITIONAL_ONLY_AFTER_SEPARATE_APPROVAL" for row in impact), "step16_provider_calls_are_zero_and_not_authorized", checks)
    require(all(row["final_ownership_state"] == "NOT_DECIDED" and row["final_physical_action_state"] == "NOT_DECIDED" for row in impact), "impact_register_does_not_make_final_ownership_or_action_decisions", checks)

    protected = json.loads(PROTECTED.read_text(encoding="utf-8"))
    protected_paths = {
        "level1_step5a_method": LEVEL1 / "STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md",
        "level1_step_rules_index": LEVEL1 / "STEP_RULES_INDEX.md",
        "level1_lessons_ledger": LEVEL1 / "STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md",
        "level1_step8_method": LEVEL1 / "STEP_08_SEARCH_STAGE_FREEZE_METHOD.md",
        "historical_stage5_master": BASE_STAGE5,
        "historical_stage5_units": JOB / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv",
        "historical_step7": BASE_STEP7,
        "historical_step8": BASE_STEP8,
        "historical_step8_review_routes": JOB / "STEP_08_REVIEW_RESOLUTION_ROUTES.tsv",
        "historical_step8_duplicate_handoff": JOB / "STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv",
    }
    require(all(sha256(path) == protected["files"][name]["sha256"] for name, path in protected_paths.items()), "protected_file_hashes_are_unchanged", checks)
    require(tree_sha256(JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05") == protected["trees"]["corrected_release"]["sha256"], "historical_corrected_release_tree_is_unchanged", checks)
    require(tree_sha256(LEVEL1.parent / "KW002_SEMANTIC_CORE_FROM_SCRATCH") == protected["trees"]["kw002"]["sha256"], "kw002_tree_is_unchanged", checks)

    artifacts = [UNION, CLEANUP, FREEZE, PROVENANCE, SEMANTIC, IMPACT, OUT / "STEP_05A_POST_ACCEPTANCE_EXECUTION_MANIFEST.json", OUT / "STEP_05A_POST_ACCEPTANCE_PROPAGATION_REPORT.md", OUT / "CHECKPOINT_00_PROPAGATION_MATERIALIZED.md", OUT / "STEP_05A_POST_ACCEPTANCE_EXECUTION_RECEIPT.md", OUT / "build_post_acceptance_propagation.py", OUT / "validate_post_acceptance_propagation.py", PROTECTED]
    qa = {
        "status": "PASS",
        "validator": "validate_post_acceptance_propagation.py",
        "checks_passed": len(checks),
        "checks_failed": 0,
        "checks": checks,
        "counts": {
            "baseline_rows": 2840,
            "accepted_delta_rows": 16,
            "union_rows": 2856,
            "step7_status_counts": dict(sorted(cleanup_counts.items())),
            "step8_disposition_counts": dict(sorted(step8_counts.items())),
            "affected_directions": 7,
            "candidate_existing_units": len({row["candidate_existing_unit_for_recheck"] for row in impact if row["candidate_existing_unit_for_recheck"]}),
            "additional_step9_search_requirements": 6,
            "provider_calls": 0,
        },
        "artifact_sha256": {path.name: sha256(path) for path in artifacts},
    }
    QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "checks_passed": len(checks), "counts": qa["counts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    validate()
