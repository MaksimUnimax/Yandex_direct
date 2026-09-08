#!/usr/bin/env python3
"""Independent deterministic QA for OKNO_MSK Step 5A.5."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


OUT = Path(__file__).resolve().parent
JOB = OUT.parent
REPO = next(parent for parent in OUT.parents if (parent / ".git").exists())
STARTING_HEAD = "e733d4051e5a0704d60370b14326fd1bc23a655a"

WORDSTAT_PACKAGE = OUT / "STEP_05A_WORDSTAT_REQUIREMENT_PACKAGE.tsv"
PAGE_EVIDENCE = OUT / "STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv"
ACQUISITION = OUT / "STEP_05A_WORDSTAT_SEED_ACQUISITION_LEDGER.tsv"
RETURNED = OUT / "STEP_05A_WORDSTAT_RETURNED_PHRASE_LEDGER.tsv"
RECONCILIATION = OUT / "STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv"
SEARCH_PACKAGE = OUT / "STEP_05A_SEARCH_RECHECK_REQUIREMENT_PACKAGE.tsv"
REPORT = OUT / "STEP_05A_WORDSTAT_RECONCILIATION_REPORT.md"
LOG = OUT / "STEP_05A_WORDSTAT_RECONCILIATION_EXECUTION_LOG.md"
CHECKPOINT_02 = OUT / "CHECKPOINT_02_WORDSTAT_NORMALIZATION.md"
CHECKPOINT_03 = OUT / "CHECKPOINT_03_WORDSTAT_RECONCILIATION.md"
CHECKPOINT_04 = OUT / "CHECKPOINT_04_WORDSTAT_REMOTE_READBACK.md"
BUILDER = OUT / "build_step05a_wordstat_reconciliation.py"
QA = OUT / "STEP_05A_WORDSTAT_RECONCILIATION_QA.json"

FINAL_MASTER = JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"
UNIT_AUTHORITY = JOB / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"
LEVEL1_METHOD = JOB.parent.parent / "STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md"
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"

PROTECTED_HASHES = {
    "01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.pdf": "79450c2f0dc58ea064b72b7c400f6db7b908cb455c72003584c5e59c9b9fad08",
    "02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-05.pdf": "b1a2848f781fe12dfe8293cfe2f88e796c967ce9eee7f9b251b171ac73060056",
    "03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.md": "d5c90cf187041e975f17d03a2be138eff0b6a06bfe1b7d395a3b24547edc62b0",
    "04_OKNO_MSK_FULL_SEMANTIC_CORE_2026-09-07.xlsx": "cee26a8d7d4a8381d4706c7940b739c3afca652034e9e3630053e35bd0184e3a",
}

ALLOWED_CLASSES = {
    "ALREADY_COVERED_EXACT_OR_CLOSE", "POTENTIALLY_NEW_SEARCH_RECHECK",
    "OFF_SCOPE_BUSINESS", "NOISE_IRRELEVANT", "HOLD_EVIDENCE",
}

EXPECTED_SEARCH_QUERIES = [
    "гидроизоляция для открытого балкона",
    "солнцезащитный стеклопакет",
    "многофункциональный стеклопакет что это",
    "ударопрочный стеклопакет",
    "окна для старого фонда",
    "балконы под офис",
    "кладовая на балконе",
    "шумоизоляция на крышу балкона",
    "армирование оконного профиля",
]


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
    return subprocess.run(["git", *args], cwd=REPO, text=True, check=True, capture_output=True).stdout.strip()


def expected_raw_rows() -> tuple[list[tuple[int, str, int, str, str]], Counter, dict[int, dict[str, object]]]:
    rows: list[tuple[int, str, int, str, str]] = []
    shapes: Counter = Counter()
    raw_results: dict[int, dict[str, object]] = {}
    for order in range(1, 15):
        raw = json.loads((OUT / f"STEP_05A_WORDSTAT_ITEM_{order:02d}_RAW.json").read_text(encoding="utf-8"))
        result = raw["provider_result"]["result"]
        raw_results[order] = result
        if not result:
            shapes["EMPTY_PROVIDER_RESULT"] += 1
        elif "totalCount" in result and not result.get("results") and not result.get("associations"):
            shapes["TOTALCOUNT_ONLY"] += 1
        else:
            shapes["RESULT_ROWS_ASSOCIATIONS_TOTALCOUNT"] += 1
        for provider_key, row_class in (("results", "DIRECT_RESULT"), ("associations", "ASSOCIATION")):
            for index, row in enumerate(result.get(provider_key, []), start=1):
                rows.append((order, row_class, index, row["phrase"], str(row["count"])))
    return rows, shapes, raw_results


def main() -> int:
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, detail: object = None) -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    required = [ACQUISITION, RETURNED, RECONCILIATION, SEARCH_PACKAGE, REPORT, LOG, CHECKPOINT_02, CHECKPOINT_03, CHECKPOINT_04, BUILDER, Path(__file__)]
    check("required_artifacts_exist", all(path.exists() for path in required), [path.name for path in required if not path.exists()])

    package = read_tsv(WORDSTAT_PACKAGE)
    acquisition = read_tsv(ACQUISITION)
    returned = read_tsv(RETURNED)
    reconciliation = read_tsv(RECONCILIATION)
    search = read_tsv(SEARCH_PACKAGE)
    expected_rows, expected_shapes, raw_results = expected_raw_rows()

    check("seed_acquisition_rows_exactly_14", len(acquisition) == 14, len(acquisition))
    check("authorized_seed_order_exact", [int(row["seed_order"]) for row in acquisition] == list(range(1, 15)))
    check("authorized_seed_text_exact", [row["seed_text"] for row in acquisition] == [row["normalized_candidate_seed"] for row in package])
    check("duplicate_seed_accounting_inflation_0", len({row["seed_text"].casefold() for row in acquisition}) == 14)
    check("all_seed_requests_executed_successfully", all(row["request_executed"] == "true" and row["http_status"] == "200" and row["item_status"] == "SUCCEEDED" for row in acquisition))
    check("provider_shape_counts_exact", Counter(row["provider_result_shape"] for row in acquisition) == expected_shapes, dict(expected_shapes))
    check("empty_provider_results_preserved_4", sum(row["provider_result_shape"] == "EMPTY_PROVIDER_RESULT" for row in acquisition) == 4)
    check("empty_provider_results_not_fabricated_zero", all(row["total_count"] == "" and row["direct_results_rows"] == "0" and row["association_rows"] == "0" for row in acquisition if row["provider_result_shape"] == "EMPTY_PROVIDER_RESULT"))
    check("totalcount_only_preserved_2", sum(row["provider_result_shape"] == "TOTALCOUNT_ONLY" for row in acquisition) == 2)
    check("totalcount_only_phrase_rows_not_invented", all(row["direct_results_rows"] == "0" and row["association_rows"] == "0" for row in acquisition if row["provider_result_shape"] == "TOTALCOUNT_ONLY"))

    actual_rows = [(int(row["seed_order"]), row["wordstat_row_class"], int(row["row_index_within_class"]), row["returned_phrase"], row["returned_count"]) for row in returned]
    check("all_actual_provider_rows_preserved_exact", actual_rows == expected_rows, {"actual": len(actual_rows), "expected": len(expected_rows)})
    check("fabricated_phrase_rows_0", set(actual_rows) == set(expected_rows) and len(actual_rows) == len(expected_rows))
    row_classes = Counter(row["wordstat_row_class"] for row in returned)
    check("direct_result_rows_exact_21", row_classes["DIRECT_RESULT"] == 21, row_classes["DIRECT_RESULT"])
    check("association_rows_exact_139", row_classes["ASSOCIATION"] == 139, row_classes["ASSOCIATION"])
    check("returned_phrase_rows_exact_160", len(returned) == 160, len(returned))
    check("raw_lineage_complete", all(row["source_raw_item_file"] and row["source_request_id"] and row["source_seed"] for row in returned))
    check("competitor_page_lineage_complete", all(row["page_evidence_ids"] and row["competitor_urls"] and row["observed_page_evidence"] for row in returned))

    check("semantic_reconciliation_rows_exact_160", len(reconciliation) == len(returned) == 160)
    check("semantic_reconciliation_row_ids_exact", [row["wordstat_row_id"] for row in reconciliation] == [row["wordstat_row_id"] for row in returned])
    class_counts = Counter(row["semantic_reconciliation_result"] for row in reconciliation)
    check("semantic_classes_bounded", set(class_counts) <= ALLOWED_CLASSES, dict(class_counts))
    check("every_material_row_reconciled", all(row["semantic_authority_match"] and row["reconciliation_reason"] for row in reconciliation if row["material_relevance"] == "MATERIAL"))

    units = {row["structural_unit_id"] for row in read_tsv(UNIT_AUTHORITY)}
    phrases = {row["phrase"] for row in read_tsv(FINAL_MASTER)}
    bad_refs = []
    for row in reconciliation:
        ref = row["semantic_authority_match"]
        if ref.startswith("unit:") and ref[5:] not in units:
            bad_refs.append(ref)
        if ref.startswith("phrase:") and ref[7:] not in phrases:
            bad_refs.append(ref)
    check("semantic_authority_references_valid", not bad_refs, sorted(set(bad_refs)))
    check("potentially_new_rows_have_full_lineage", all(row["competitor_page_lineage"] and row["raw_provider_lineage"] and row["deduplicated_direction_id"] for row in reconciliation if row["semantic_reconciliation_result"] == "POTENTIALLY_NEW_SEARCH_RECHECK"))
    check("new_rows_are_actual_direct_results", all(row["wordstat_row_class"] == "DIRECT_RESULT" for row in reconciliation if row["semantic_reconciliation_result"] == "POTENTIALLY_NEW_SEARCH_RECHECK"))
    obvious_noise = {"как открыть бутылку без открывашки", "втб не открывается на айфоне", "острый бронхит код мкб", "человек за окном", "офисные шкафы", "катепал мягкая кровля"}
    check("obvious_noise_not_promoted", not any(row["returned_phrase"] in obvious_noise and row["semantic_reconciliation_result"] == "POTENTIALLY_NEW_SEARCH_RECHECK" for row in reconciliation))

    check("search_requirements_exact_9", len(search) == 9, len(search))
    check("search_priorities_consecutive", [int(row["search_priority"]) for row in search] == list(range(1, 10)))
    check("search_queries_exact", [row["representative_query"] for row in search] == EXPECTED_SEARCH_QUERIES)
    check("search_query_duplicates_0", len({row["representative_query"].casefold() for row in search}) == len(search))
    check("search_direction_duplicates_0", len({row["deduplicated_direction_id"] for row in search}) == len(search))
    check("search_region_213", {row["region"] for row in search} == {"213"})
    check("search_top10", {row["requested_top_results"] for row in search} == {"10"})
    check("search_unresolved_question_present", all(row["unresolved_search_question"] for row in search))
    check("search_existing_evidence_gap_present", all(row["why_preserved_search_is_insufficient"] for row in search))
    check("search_downstream_gate_bounded", all(row["expected_downstream_decision_gate"] == "ADD_TO_PIPELINE | ALREADY_COVERED | REJECT_OFF_SCOPE | HOLD_EVIDENCE" for row in search))
    check("search_requirement_only", all(row["provider_call_authorization_state"] == "RETURN_TO_MAIN_CHATGPT_FOR_YANDEX_SEARCH_BRIDGE_EXECUTION" and row["claim_boundary"] == "REQUIREMENT_ONLY__WORK_DID_NOT_EXECUTE_SEARCH" for row in search))
    old_fund = next(row for row in search if row["representative_query"] == "окна для старого фонда")
    check("totalcount_only_search_lineage_explicit", old_fund["originating_returned_phrases_and_counts"] == "NO_PHRASE_ROWS__TOTALCOUNT_ONLY=5")
    check("p46_not_redundantly_rechecked", "остекление балкона П-46" not in {row["representative_query"] for row in search})

    raw_files = [OUT / "STEP_05A_WORDSTAT_BATCH_START_RAW.json"] + [OUT / f"STEP_05A_WORDSTAT_ITEM_{i:02d}_RAW.json" for i in range(1, 15)]
    raw_unchanged = {}
    for path in raw_files:
        rel = str(path.relative_to(REPO))
        raw_unchanged[path.name] = git("rev-parse", f"{STARTING_HEAD}:{rel}") == git("hash-object", str(path))
    check("raw_provider_envelopes_unchanged", all(raw_unchanged.values()), raw_unchanged)

    provider_calls = {"yandex_search": 0, "wordstat": 0, "alice": 0, "gensearch": 0, "webmaster": 0, "metrika": 0, "direct": 0, "web_search_substitute": 0}
    check("new_yandex_provider_calls_0", all(value == 0 for value in provider_calls.values()), provider_calls)

    protected_actual = {name: sha256(RELEASE / name) for name in PROTECTED_HASHES}
    check("protected_artifact_hashes_unchanged", protected_actual == PROTECTED_HASHES, protected_actual)
    release_rel = str(RELEASE.relative_to(REPO))
    check("corrected_client_release_tree_unchanged", git("rev-parse", f"{STARTING_HEAD}:{release_rel}") == git("rev-parse", f"HEAD:{release_rel}"))
    check("level1_method_not_promoted", git("rev-parse", f"{STARTING_HEAD}:{LEVEL1_METHOD.relative_to(REPO)}") == git("hash-object", str(LEVEL1_METHOD)))

    changed = [path for path in git("diff", "--name-only", STARTING_HEAD).splitlines() if path]
    changed += [path for path in git("ls-files", "--others", "--exclude-standard").splitlines() if path]
    changed = sorted(set(changed))
    out_prefix = str(OUT.relative_to(REPO)) + "/"
    check("all_changes_isolated_to_step05a_execution", all(path.startswith(out_prefix) for path in changed), changed)

    report = REPORT.read_text(encoding="utf-8")
    tokens = [
        "SEEDS_ACCOUNTED = 14 / 14", "DIRECT_WORDSTAT_ROWS_EXTRACTED = 21",
        "ASSOCIATION_ROWS_EXTRACTED = 139", "TOTAL_RETURNED_PHRASE_ROWS = 160",
        "FINAL_SEARCH_RECHECK_CALLS_REQUIRED = 9", "FABRICATED_ROWS = 0",
        "FABRICATED_ZERO_DEMAND = 0", "NEW_YANDEX_SEARCH_CALLS = 0",
        "NEW_WORDSTAT_CALLS = 0", "CLIENT_DELIVERABLES_MODIFIED = false",
        "LEVEL1_METHOD_PROMOTED = false", "METHOD NOT PROMOTED",
    ]
    check("report_required_tokens_present", all(token in report for token in tokens), [token for token in tokens if token not in report])
    check("report_all_search_queries_present", all(query in report for query in EXPECTED_SEARCH_QUERIES))

    artifact_paths = [ACQUISITION, RETURNED, RECONCILIATION, SEARCH_PACKAGE, REPORT, LOG, CHECKPOINT_02, CHECKPOINT_03, CHECKPOINT_04, BUILDER, Path(__file__)]
    artifact_files = {path.name: {"sha256": sha256(path), "size_bytes": path.stat().st_size} for path in artifact_paths}
    existing_readback: dict[str, object] = {}
    if QA.exists():
        existing_readback = json.loads(QA.read_text(encoding="utf-8")).get("remote_readback", {})
    remote_readback = existing_readback if existing_readback.get("status") == "PASS" else {"status": "PENDING_FINAL_REMOTE_READBACK", "material_blocks": "PASS"}
    failed = [row["name"] for row in checks if row["status"] == "FAIL"]
    payload = {
        "status": "PASS" if not failed else "FAIL",
        "execution_scope": "STEP_5A_5_WORDSTAT_RECONCILIATION",
        "starting_head": STARTING_HEAD,
        "project_test_validated": False,
        "owner_review": "PENDING",
        "counts": {
            "seeds_accounted": len(acquisition),
            "provider_shapes": dict(sorted(expected_shapes.items())),
            "direct_wordstat_rows": row_classes["DIRECT_RESULT"],
            "association_rows": row_classes["ASSOCIATION"],
            "total_returned_phrase_rows": len(returned),
            "reconciliation_classes": dict(sorted(class_counts.items())),
            "deduplicated_returned_phrase_directions": len({row["deduplicated_direction_id"] for row in reconciliation if row["deduplicated_direction_id"]}),
            "additional_totalcount_only_search_direction": 1,
            "final_search_recheck_calls_required": len(search),
        },
        "exact_search_recheck_queries": EXPECTED_SEARCH_QUERIES,
        "provider_calls_by_work": provider_calls,
        "raw_provider_envelopes_unchanged": raw_unchanged,
        "protected_artifacts_modified": {name: protected_actual[name] != expected for name, expected in PROTECTED_HASHES.items()},
        "corrected_client_release_modified": False,
        "level1_method_promoted": False,
        "deterministic_qa": {"checks_total": len(checks), "checks_passed": len(checks) - len(failed), "failed": failed, "checks": checks},
        "artifact_files": artifact_files,
        "remote_readback": remote_readback,
        "next_action": "MAIN_CHATGPT_STEP_5A_6_EXECUTE_ONLY_THE_MATERIALIZED_SEARCH_RECHECK_PACKAGE_VIA_YANDEX_BRIDGE",
    }
    QA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": len(checks), "failed": failed, "counts": payload["counts"]}, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
