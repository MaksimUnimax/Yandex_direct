#!/usr/bin/env python3
"""Independent deterministic QA for Step 5A.6–5A.7."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


OUT = Path(__file__).resolve().parent
JOB = OUT.parent
REPO = next(parent for parent in OUT.parents if (parent / ".git").exists())
STARTING_HEAD = "d307bd65c0c336cb37ad79a987a3bfe7d2e57219"

PACKAGE = OUT / "STEP_05A_SEARCH_RECHECK_REQUIREMENT_PACKAGE.tsv"
WORDSTAT_RECON = OUT / "STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv"
ACQUISITION = OUT / "STEP_05A_SEARCH_REQUIREMENT_ACQUISITION_LEDGER.tsv"
SERP = OUT / "STEP_05A_SEARCH_SERP_ROW_LEDGER.tsv"
MATRIX = OUT / "STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv"
INTENT = OUT / "STEP_05A_SEARCH_INTENT_PAGE_TYPE_ANALYSIS.tsv"
DECISIONS = OUT / "STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv"
MERGE = OUT / "STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv"
DELTA = OUT / "STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv"
REPORT = OUT / "STEP_05A_SEARCH_DECISION_MERGE_REPORT.md"
INFO_GAIN = OUT / "STEP_05A_INFORMATION_GAIN_INPUT.json"
PAGE_INSPECTION_QA = OUT / "STEP_05A_PAGE_INSPECTION_QA.json"
LOG = OUT / "STEP_05A_SEARCH_DECISION_MERGE_EXECUTION_LOG.md"
CHECKPOINT_05 = OUT / "CHECKPOINT_05_SEARCH_NORMALIZATION_AND_INTENT.md"
CHECKPOINT_06 = OUT / "CHECKPOINT_06_SEARCH_DECISION_MERGE.md"
BUILDER = OUT / "build_step05a_search_decision_merge.py"
QA = OUT / "STEP_05A_SEARCH_DECISION_MERGE_QA.json"

RAW_FILES = {
    1: "STEP_05A_SEARCH_ITEM_01_RAW.json",
    2: "STEP_05A_SEARCH_ITEM_02_RAW.json",
    3: "STEP_05A_SEARCH_ITEM_03_RAW.json",
    4: "STEP_05A_SEARCH_ITEM_04_RAW.json",
    5: "STEP_05A_SEARCH_ITEM_05_OUTCOME_UNKNOWN_RAW.json",
    6: "STEP_05A_SEARCH_ITEM_06_RAW.json",
    7: "STEP_05A_SEARCH_ITEM_07_OUTCOME_UNKNOWN_RAW.json",
    8: "STEP_05A_SEARCH_ITEM_08_RAW.json",
    9: "STEP_05A_SEARCH_ITEM_09_RAW.json",
}

SELECTED = {
    "mosokna.ru", "i-okna.ru", "msk.okna-servise.com", "okna-moskva.ru",
    "oknafactoria.ru", "okna-germany.ru", "fabrikaokon.ru", "aluminarium.ru", "elit-balkon.ru",
}

PAGE_TYPES = {
    "COMMERCIAL_SERVICE", "COMMERCIAL_PRODUCT", "COMMERCIAL_CATEGORY", "COMMERCIAL_LANDING",
    "ARTICLE_GUIDE", "COMPARISON_SELECTION", "MARKETPLACE", "INFORMATIONAL_PUBLISHER",
    "MANUFACTURER_BRAND_SOURCE", "PORTFOLIO_GALLERY", "OTHER_REVIEW",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, check=True, text=True, capture_output=True).stdout.strip()


def raw_truth():
    requirements = []
    rows = []
    raw_unchanged = {}
    for priority in range(1, 10):
        path = OUT / RAW_FILES[priority]
        raw = json.loads(path.read_text(encoding="utf-8"))
        provider = raw.get("provider_result") or {}
        result = provider.get("result") if isinstance(provider, dict) else None
        results = result.get("results", []) if isinstance(result, dict) else []
        requirements.append({
            "priority": priority,
            "state": raw["item"]["status"],
            "query": raw["item"]["command"]["queryText"],
            "request_id": raw["item"]["request_id"],
            "rows": len(results),
        })
        for result_row in results:
            rows.append((priority, str(result_row["rank"]), result_row["domain"], result_row["url"], result_row.get("title") or "", result_row.get("snippet") or "", result_row.get("modtime") or ""))
        rel = str(path.relative_to(REPO))
        raw_unchanged[path.name] = git("rev-parse", f"{STARTING_HEAD}:{rel}") == git("hash-object", str(path))
    return requirements, rows, raw_unchanged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("search", "final"), default="final")
    args = parser.parse_args()
    checks = []

    def check(name, passed, detail=None):
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    search_required = [ACQUISITION, SERP, MATRIX, INTENT, CHECKPOINT_05, BUILDER, Path(__file__)]
    final_required = search_required + [DECISIONS, MERGE, DELTA, REPORT, INFO_GAIN, LOG, CHECKPOINT_06]
    required = final_required if args.phase == "final" else search_required
    check("required_artifacts_exist", all(path.exists() for path in required), [path.name for path in required if not path.exists()])
    if not all(path.exists() for path in required):
        print(json.dumps({"status": "FAIL", "failed": ["required_artifacts_exist"]}))
        return 1

    package = read_tsv(PACKAGE)
    acquisition = read_tsv(ACQUISITION)
    serp = read_tsv(SERP)
    matrix = read_tsv(MATRIX)
    intent = read_tsv(INTENT)
    requirements, expected_rows, raw_unchanged = raw_truth()

    check("search_requirements_accounted_exactly_9", len(acquisition) == len(package) == 9, len(acquisition))
    check("search_priorities_exact", [int(row["search_priority"]) for row in acquisition] == list(range(1, 10)))
    check("search_queries_match_package", [row["representative_query"] for row in acquisition] == [row["representative_query"] for row in package])
    states = Counter(row["search_acquisition_state"] for row in acquisition)
    check("search_succeeded_exactly_7", states["SUCCEEDED"] == 7, dict(states))
    check("search_outcome_unknown_exactly_2", states["OUTCOME_UNKNOWN"] == 2, dict(states))
    check("unknown_priorities_exact_5_7", {int(row["search_priority"]) for row in acquisition if row["search_acquisition_state"] == "OUTCOME_UNKNOWN"} == {5, 7})
    check("unknown_is_not_empty_serp", all(row["result_count"] == "" and row["http_status"] == "" and "REQUEST_OUTCOME_UNKNOWN_NO_RETRY" in row["evidence_limitation"] for row in acquisition if row["search_acquisition_state"] == "OUTCOME_UNKNOWN"))
    check("unknown_final_envelope_executed_state_preserved", all(row["final_envelope_request_executed"] == "UNKNOWN" and row["item_request_executed"] == "true" for row in acquisition if row["search_acquisition_state"] == "OUTCOME_UNKNOWN"))
    check("unknown_retries_0", all(row["automatic_retry"] == "false" for row in acquisition), Counter(row["automatic_retry"] for row in acquisition))
    check("three_durable_jobs_accounted", len({row["durable_job_id"] for row in acquisition}) == 3, sorted({row["durable_job_id"] for row in acquisition}))
    check("acquisition_total_estimated_cost_exact", abs(sum(float(row["estimated_cost_rub"]) for row in acquisition) - 4.392) < 1e-9)

    actual_rows = [(int(row["search_priority"]), row["rank"], row["raw_domain"], row["raw_url"], row["title"], row["snippet"], row["modtime"]) for row in serp]
    check("successful_serp_rows_exactly_70", len(serp) == len(expected_rows) == 70, len(serp))
    check("all_successful_raw_rows_preserved_in_order", actual_rows == expected_rows)
    check("fabricated_unknown_serp_rows_0", not any(int(row["search_priority"]) in {5, 7} for row in serp))
    check("rank_sets_exact_top10", all({int(row["rank"]) for row in serp if int(row["search_priority"]) == p} == set(range(1, 11)) for p in {1, 2, 3, 4, 6, 8, 9}))
    selected_rows = [row for row in serp if row["selected_step5a_competitor"] == "true"]
    check("selected_competitor_flags_match_normalized_domains", all(row["normalized_domain"] in SELECTED and row["selected_competitor_domain"] == row["normalized_domain"] for row in selected_rows))
    check("selected_competitor_ranking_rows_12", len(selected_rows) == 12, len(selected_rows))
    check("selected_ranking_claim_has_raw_row", all((int(row["search_priority"]), row["rank"], row["raw_domain"], row["raw_url"], row["title"], row["snippet"], row["modtime"]) in expected_rows for row in selected_rows))
    check("exact_previously_inspected_ranking_url_matches_0", sum(row["equals_previously_inspected_competitor_url"] == "true" for row in serp) == 0)
    check("same_selected_domain_different_url_explicit", all(row["selected_competitor_url_relation"] == "SAME_SELECTED_COMPETITOR_DOMAIN__DIFFERENT_URL" for row in selected_rows))

    check("intent_rows_exactly_70", len(intent) == 70, len(intent))
    check("intent_row_ids_match_serp", [row["search_row_id"] for row in intent] == [row["search_row_id"] for row in serp])
    check("page_type_taxonomy_bounded", {row["page_type"] for row in intent} <= PAGE_TYPES, sorted({row["page_type"] for row in intent}))
    check("all_successful_queries_have_derived_intent", {int(row["search_priority"]) for row in intent} == {1, 2, 3, 4, 6, 8, 9})
    check("page_type_not_used_as_owner_decision", all(row["ownership_decision"] == "NOT_DECIDED_FROM_PAGE_TYPE" for row in intent))

    check("visibility_matrix_exact_81", len(matrix) == 81, len(matrix))
    check("visibility_matrix_unique_9x9", len({(row["search_priority"], row["selected_competitor_domain"]) for row in matrix}) == 81)
    unknown_matrix = [row for row in matrix if int(row["search_priority"]) in {5, 7}]
    check("unknown_visibility_not_observable_exact", len(unknown_matrix) == 18 and all(row["visibility_state"] == "SEARCH_OUTCOME_UNKNOWN__VISIBILITY_NOT_OBSERVABLE" for row in unknown_matrix))
    check("unknown_not_observed_misuse_0", not any(row["visibility_state"] == "NOT_OBSERVED_IN_TOP10" for row in unknown_matrix))
    visible = [row for row in matrix if row["visibility_state"] == "VISIBLE_IN_TOP10"]
    check("selected_competitor_visibility_observations_11", len(visible) == 11, len(visible))
    check("visible_matrix_cells_have_matching_raw_rows", all(row["observed_result_row_ids"] and row["best_observed_rank"] and row["observed_ranking_urls"] for row in visible))
    check("earlier_page_topic_not_ranking_proof", all(row["earlier_evidence_role"] in {"TOPIC_AND_SEED_LINEAGE_ONLY__NOT_EXACT_QUERY_RANKING_PROOF", "NO_EARLIER_DIRECTION_PAGE_FROM_THIS_DOMAIN"} for row in matrix))
    check("raw_search_envelopes_unchanged", all(raw_unchanged.values()), raw_unchanged)

    if args.phase == "final":
        decisions = read_tsv(DECISIONS)
        merge = read_tsv(MERGE)
        delta = read_tsv(DELTA)
        potentials = [row for row in read_tsv(WORDSTAT_RECON) if row["semantic_reconciliation_result"] == "POTENTIALLY_NEW_SEARCH_RECHECK"]
        allowed = {"ADD_TO_PIPELINE", "ALREADY_COVERED", "REJECT_OFF_SCOPE", "HOLD_EVIDENCE"}
        check("direction_decisions_exactly_9", len(decisions) == 9 and len({row["deduplicated_direction_id"] for row in decisions}) == 9)
        check("every_direction_has_one_bounded_state", {row["final_routing_state"] for row in decisions} <= allowed)
        counts = Counter(row["final_routing_state"] for row in decisions)
        check("final_add_to_pipeline_7", counts["ADD_TO_PIPELINE"] == 7, dict(counts))
        check("final_hold_evidence_2", counts["HOLD_EVIDENCE"] == 2, dict(counts))
        check("unknown_directions_hold", all(row["final_routing_state"] == "HOLD_EVIDENCE" for row in decisions if row["search_acquisition_state"] == "OUTCOME_UNKNOWN"))
        check("add_has_wordstat_search_business_novelty", all(row["search_acquisition_state"] == "SUCCEEDED" and row["search_evidence_sufficient_for_direction"] == "true" and row["frozen_business_scope_state"].startswith("IN_SCOPE") and row["current_semantic_coverage_state"].startswith("NO_EXACT_OR_CLOSE") for row in decisions if row["final_routing_state"] == "ADD_TO_PIPELINE"))
        check("page_ownership_creation_actions_0", all(row["page_or_implementation_decision"] == "NONE__OUT_OF_SCOPE" for row in decisions))
        check("propagation_required_for_add", all(row["propagation_state"] == "PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE" for row in decisions if row["final_routing_state"] == "ADD_TO_PIPELINE"))

        check("potentially_new_wordstat_occurrences_reconfirmed_20", len(potentials) == 20, len(potentials))
        check("merge_reconciliation_exactly_20", len(merge) == 20, len(merge))
        check("merge_wordstat_ids_exact", [row["wordstat_row_id"] for row in merge] == [row["wordstat_row_id"] for row in potentials])
        merge_counts = Counter(row["phrase_merge_state"] for row in merge)
        check("merge_states_exact", merge_counts == Counter({"MERGE_ACCEPTED": 16, "SUPPRESSED_AS_CLOSE_VARIANT_DUPLICATE": 3, "RETAIN_HOLD": 1}), dict(merge_counts))
        check("accepted_occurrence_lineage_complete", all(row["competitor_page_lineage"] and row["wordstat_raw_provider_lineage"] and row["search_raw_item_file"] and row["search_request_id"] and row["search_acquisition_state"] == "SUCCEEDED" for row in merge if row["phrase_merge_state"] == "MERGE_ACCEPTED"))
        check("close_variant_suppressions_exact", {row["wordstat_row_id"] for row in merge if row["phrase_merge_state"] == "SUPPRESSED_AS_CLOSE_VARIANT_DUPLICATE"} == {"WSR004", "WSR026", "WSR047"})
        check("unknown_storage_occurrence_retained_hold", {row["wordstat_row_id"] for row in merge if row["phrase_merge_state"] == "RETAIN_HOLD"} == {"WSR100"})

        accepted = [row for row in merge if row["phrase_merge_state"] == "MERGE_ACCEPTED"]
        check("semantic_pipeline_delta_rows_equal_accepted_16", len(delta) == len(accepted) == 16, len(delta))
        check("delta_wordstat_ids_exact_accepted", [row["wordstat_row_id"] for row in delta] == [row["wordstat_row_id"] for row in accepted])
        check("delta_duplicate_normalized_phrases_0", len({row["normalized_phrase"] for row in delta}) == len(delta))
        check("delta_provenance_complete", all(row["provenance_complete"] == "true" and row["competitor_domains"] and row["competitor_page_urls"] and row["competitor_page_evidence_ids"] and row["candidate_seed"] and row["wordstat_raw_item_file"] and row["wordstat_request_id"] and row["search_raw_item_file"] and row["search_request_id"] for row in delta))
        check("delta_actual_wordstat_counts_only", all(row["frequency_evidence_state"] == "ACTUAL_WORDSTAT_DIRECT_RESULT_COUNT" and row["frequency_count"] == row["wordstat_returned_count"] for row in delta))
        check("delta_no_totalcount_only_invention", not any(row["step5a_direction_id"] == "OLD_HOUSING_WINDOWS" for row in delta))
        check("delta_no_page_decision", all(row["page_ownership_state"] == "NOT_DECIDED" for row in delta))
        check("delta_union_propagation_state", all(row["propagation_state"] == "PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE" for row in delta))

        info = json.loads(INFO_GAIN.read_text(encoding="utf-8"))
        page_qa_counts = json.loads(PAGE_INSPECTION_QA.read_text(encoding="utf-8"))["counts"]
        check("information_gain_input_factual_only", info["scope"] == "FACTUAL_INPUT_FOR_STEP_5A_8_ONLY" and info["project_test_validated"] is False and info["level1_method_promoted"] is False)
        check("information_gain_counts_reconcile", info["search_counts"]["successful_serp_rows"] == 70 and info["semantic_pipeline_delta_rows"] == len(delta))
        check("information_gain_page_inspection_counts_trace_to_prior_qa", info["upstream_counts"]["authorized_competitor_urls"] == page_qa_counts["authorized_urls"] == 44 and info["upstream_counts"]["competitor_pages_accessible_at_requested_url"] == page_qa_counts["accessible_at_requested_url"] == 43 and info["upstream_counts"]["competitor_pages_redirected_accessible"] == page_qa_counts["redirected_accessible"] == 1 and info["upstream_counts"]["competitor_pages_inaccessible"] == page_qa_counts["inaccessible"] == 0 and info["upstream_counts"]["deduplicated_candidate_directions"] == page_qa_counts["deduplicated_candidate_directions"] == 43)
        report = REPORT.read_text(encoding="utf-8")
        required_tokens = [
            "SEARCH_REQUIREMENTS = 9", "SEARCH_SUCCEEDED = 7", "SEARCH_OUTCOME_UNKNOWN = 2", "SEARCH_SERP_ROWS = 70",
            "SELECTED_COMPETITOR_VISIBILITY_OBSERVATIONS = 11", "FINAL_ADD_TO_PIPELINE = 7", "FINAL_HOLD_EVIDENCE = 2",
            "POTENTIALLY_NEW_WORDSTAT_OCCURRENCES_RECONCILED = 20", "MERGE_ACCEPTED_PHRASE_OCCURRENCES = 16",
            "SEMANTIC_PIPELINE_DELTA_ROWS = 16", "UNKNOWN_RETRIES = 0", "NEW_PROVIDER_CALLS_BY_WORK = 0",
            "CLIENT_DELIVERABLES_MODIFIED = false", "LEVEL1_METHOD_PROMOTED = false", "PROJECT_TEST_VALIDATED = false",
        ]
        check("report_required_counts_and_boundaries", all(token in report for token in required_tokens), [token for token in required_tokens if token not in report])
        check("report_all_9_queries_present", all(row["representative_query"] in report for row in package))

    release = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
    protected = [
        release,
        JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv",
        JOB / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv",
        JOB.parent.parent / "STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md",
    ]
    protected_state = {str(path.relative_to(REPO)): subprocess.run(["git", "diff", "--quiet", STARTING_HEAD, "--", str(path.relative_to(REPO))], cwd=REPO).returncode == 0 for path in protected}
    check("protected_client_and_frozen_authorities_unchanged", all(protected_state.values()), protected_state)
    provider_calls = {"yandex_search": 0, "wordstat": 0, "alice": 0, "gensearch": 0, "webmaster": 0, "metrika": 0, "direct": 0, "web_search_substitute": 0}
    check("new_yandex_provider_calls_by_work_0", all(value == 0 for value in provider_calls.values()), provider_calls)
    changed = sorted(set(filter(None, git("diff", "--name-only", STARTING_HEAD).splitlines())) | set(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines())))
    prefix = str(OUT.relative_to(REPO)) + "/"
    check("all_changes_isolated_to_step05a_execution", all(path.startswith(prefix) for path in changed), changed)

    failed = [row["name"] for row in checks if row["status"] == "FAIL"]
    payload = {
        "status": "PASS" if not failed else "FAIL",
        "phase": args.phase,
        "execution_scope": "STEP_5A_6_SEARCH_RECONCILIATION_AND_STEP_5A_7_DECISION_MERGE",
        "starting_head": STARTING_HEAD,
        "project_test_validated": False,
        "level1_method_promoted": False,
        "owner_review": "PENDING",
        "counts": {
            "search_requirements": len(acquisition),
            "search_succeeded": states["SUCCEEDED"],
            "search_outcome_unknown": states["OUTCOME_UNKNOWN"],
            "search_serp_rows": len(serp),
            "selected_competitor_visibility_observations": len(visible),
            "selected_competitor_ranking_rows": len(selected_rows),
            "visibility_matrix_rows": len(matrix),
        },
        "provider_calls_by_work": provider_calls,
        "raw_search_envelopes_unchanged": raw_unchanged,
        "protected_paths_unchanged": protected_state,
        "deterministic_qa": {"checks_total": len(checks), "checks_passed": len(checks) - len(failed), "failed": failed, "checks": checks},
        "remote_readback": {"status": "PENDING_FINAL_REMOTE_READBACK"},
        "next_action": "STEP_5A_8_MEASURE_INFORMATION_GAIN_AND_ASSESS_FIRST_EXECUTION_PROJECT_VALIDATION_WITHOUT_AUTOMATIC_LEVEL1_PROMOTION",
    }
    if args.phase == "final":
        decisions = read_tsv(DECISIONS)
        merge = read_tsv(MERGE)
        delta = read_tsv(DELTA)
        payload["counts"].update({
            "final_routing_states": dict(sorted(Counter(row["final_routing_state"] for row in decisions).items())),
            "potentially_new_wordstat_occurrences_reconciled": len(merge),
            "merge_states": dict(sorted(Counter(row["phrase_merge_state"] for row in merge).items())),
            "semantic_pipeline_delta_rows": len(delta),
        })
        artifacts = [ACQUISITION, SERP, MATRIX, INTENT, DECISIONS, MERGE, DELTA, REPORT, INFO_GAIN, LOG, CHECKPOINT_05, CHECKPOINT_06, BUILDER, Path(__file__)]
        payload["artifact_files"] = {path.name: {"sha256": sha256(path), "size_bytes": path.stat().st_size} for path in artifacts}
        QA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "phase": args.phase, "checks": len(checks), "failed": failed, "counts": payload["counts"]}, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
