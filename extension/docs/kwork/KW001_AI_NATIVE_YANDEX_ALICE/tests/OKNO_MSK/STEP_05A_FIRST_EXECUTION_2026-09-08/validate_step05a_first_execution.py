#!/usr/bin/env python3
"""Independent deterministic QA for the OKNO_MSK Step 5A first execution."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit


OUT = Path(__file__).resolve().parent
JOB = OUT.parent
REPO = next(parent for parent in OUT.parents if (parent / ".git").exists())
STARTING_HEAD = "c043fda14c51b18f4016aa26ff3e3f7e7c121a13"

COMBINED = OUT / "STEP_05A_SERP_COMBINED_750.tsv"
DOMAINS = OUT / "STEP_05A_DOMAIN_FREQUENCY.tsv"
IMPACT = OUT / "STEP_05A_QUERY_IMPACT_TRACE.tsv"
CANDIDATES = OUT / "STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv"
QA = OUT / "STEP_05A_FIRST_EXECUTION_QA.json"
REPORT = OUT / "STEP_05A_FIRST_EXECUTION_REPORT.md"
LOG = OUT / "EXECUTION_LOG.md"
CHECKPOINT = OUT / "CHECKPOINT_00_BASELINE_AND_REUSE_INVENTORY.md"
BUILDER = OUT / "build_step05a_first_execution.py"

REQUIRED = [CHECKPOINT, COMBINED, DOMAINS, IMPACT, CANDIDATES, QA, REPORT, LOG, BUILDER]
OPTIONAL_NOT_EXECUTED = [
    OUT / "STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv",
    OUT / "STEP_05A_DERIVED_SEED_CANDIDATES.tsv",
]

EXPECTED_SOURCE_HASHES = {
    "STEP_09_SERP_RESULTS.tsv": "3c2bb777982be527808dab06eae045c5c50b5603830681d3f9752c4c44f3460c",
    "STEP_09_SERP_R2_PROJECTION_RAW_PART_01.tsv": "98c5e166feb603b85ca17ecb4f4217b2c6ba03b519dec108d29fed8f6f5dd18c",
    "STEP_09_SERP_R2_PROJECTION_RAW_PART_02.tsv": "31c579dd4c992c6167de896454641424a4a244940a040f041540fd833745df61",
    "STEP_09_SERP_R2_PROJECTION_RAW_PART_03.tsv": "ca75c8577a43dfd3741732ccffecaa4a365f4f4b8897d83f4f19e256a86658cf",
    "STEP_09_SERP_R2_PROJECTION_RAW_PART_04.tsv": "e995d52e24bf655a8e84735a9b545ec87d8a95289f5a1e99a224e1673512a4cf",
    "STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv": "7d6058ea1ca798a667057ef6379a81e1955175a4fca83d5bf41172243b0f2497",
}

EXPECTED_PROTECTED_HASHES = {
    "01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.pdf": "79450c2f0dc58ea064b72b7c400f6db7b908cb455c72003584c5e59c9b9fad08",
    "03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.md": "d5c90cf187041e975f17d03a2be138eff0b6a06bfe1b7d395a3b24547edc62b0",
    "04_OKNO_MSK_FULL_SEMANTIC_CORE_2026-09-07.xlsx": "cee26a8d7d4a8381d4706c7940b739c3afca652034e9e3630053e35bd0184e3a",
}

EXPECTED_SELECTED = [
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        text=True,
        check=True,
        capture_output=True,
    ).stdout.strip()


def main() -> int:
    payload = json.loads(QA.read_text(encoding="utf-8"))
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, detail: object = None) -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    check("required_artifacts_exist", all(path.exists() for path in REQUIRED), [path.name for path in REQUIRED if not path.exists()])
    check("optional_page_evidence_absent", not any(path.exists() for path in OPTIONAL_NOT_EXECUTED), [path.name for path in OPTIONAL_NOT_EXECUTED if path.exists()])

    combined = read_tsv(COMBINED)
    by_query: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in combined:
        by_query[int(row["query_index"])].append(row)
    check("combined_rows_750", len(combined) == 750, len(combined))
    check("combined_queries_75", sorted(by_query) == list(range(1, 76)), sorted(by_query))
    check("combined_region_213", {row["region"] for row in combined} == {"213"})
    check("combined_ranks_1_to_10", all(sorted(int(row["rank"]) for row in rows) == list(range(1, 11)) for rows in by_query.values()))
    check("combined_one_query_text_per_index", all(len({row["query_text"] for row in rows}) == 1 for rows in by_query.values()))
    identities = [(row["query_index"], row["rank"], row["item_id"], row["url"]) for row in combined]
    check("duplicate_row_inflation_0", len(identities) == len(set(identities)))
    check("normalized_domain_matches_url", all((urlsplit(row["url"]).hostname or "").lower().removeprefix("www.").rstrip(".") == row["normalized_domain"] for row in combined))

    domain_rows = read_tsv(DOMAINS)
    check("normalized_domains_237", len(domain_rows) == 237, len(domain_rows))
    check("domain_appearance_sum_750", sum(int(row["total_top10_appearances"]) for row in domain_rows) == 750)
    check("domain_rows_unique", len({row["normalized_domain"] for row in domain_rows}) == 237)
    allowed_classes = {
        "DIRECT_BUSINESS_COMPETITOR", "ORGANIC_COMPETITOR_OTHER_MODEL", "AGGREGATOR_DIRECTORY",
        "MARKETPLACE", "MANUFACTURER_OR_BRAND_SOURCE", "INFORMATIONAL_PUBLISHER",
        "YANDEX_PLATFORM", "OTHER_REVIEW", "UNKNOWN",
    }
    check("domain_classes_allowed_and_complete", all(row["competitor_class"] in allowed_classes for row in domain_rows))
    check("recurrence_not_business_equivalence", all(next(row for row in domain_rows if row["normalized_domain"] == domain)["competitor_class"] != "DIRECT_BUSINESS_COMPETITOR" for domain in ["online-shop.rhsolutions.ru", "avito.ru", "ozon.ru", "uslugi.yandex.ru"]))

    impact_rows = read_tsv(IMPACT)
    impact_counts = Counter(row["impact_classification"] for row in impact_rows)
    expected_impact = {
        "CHANGED_DECISION": 26,
        "DE_RISKED_DECISION": 20,
        "CONFIRMED_EXISTING_DECISION": 19,
        "NO_MATERIAL_DOWNSTREAM_EFFECT": 0,
        "UNRESOLVED_TRACE": 10,
    }
    check("impact_rows_75", len(impact_rows) == 75, len(impact_rows))
    check("impact_counts_expected", {name: impact_counts.get(name, 0) for name in expected_impact} == expected_impact, dict(impact_counts))
    check("impact_probe_ids_unique", len({row["probe_id"] for row in impact_rows}) == 75)
    check("impact_exact_step10_joins_66", sum(row["step10_exact_join"] == "true" for row in impact_rows) == 66)
    check("impact_exact_step11_joins_66", sum(row["step11_exact_phrase_join"] == "true" for row in impact_rows) == 66)
    check("impact_exact_master_joins_66", sum(row["final_master_exact_join"] == "true" for row in impact_rows) == 66)
    check("unresolved_no_family_transfer", all(row["trace_status"] == "UNRESOLVED" and "NO_UNPROBED_OR_FAMILY_CAUSAL_TRANSFER" in row["claim_boundary"] for row in impact_rows if row["impact_classification"] == "UNRESOLVED_TRACE"))
    check("resolved_has_explicit_boundary", all(row["trace_status"] == "TRACE_RESOLVED_WITH_EXPLICIT_BOUNDARY" for row in impact_rows if row["impact_classification"] != "UNRESOLVED_TRACE"))

    candidate_rows = read_tsv(CANDIDATES)
    selected = [row for row in candidate_rows if row["selection_state"] == "SELECTED_FOR_NEXT_STEP5A_PAGE_INSPECTION"]
    check("candidate_shortlist_rows_11", len(candidate_rows) == 11, len(candidate_rows))
    check("selected_candidates_exact_9", [row["normalized_domain"] for row in selected] == EXPECTED_SELECTED, [row["normalized_domain"] for row in selected])
    check("selected_competitor_class_direct", all(row["competitor_class"] == "DIRECT_BUSINESS_COMPETITOR" for row in selected))
    combined_urls: dict[str, set[str]] = defaultdict(set)
    for row in combined:
        combined_urls[row["normalized_domain"]].add(row["url"])
    selected_url_check = True
    for row in selected:
        items = row["exact_ranking_urls_to_inspect_next"].split(" | ")
        selected_url_check &= bool(items) and all(item.split(" ", 1)[1] in combined_urls[row["normalized_domain"]] for item in items)
    check("selected_urls_all_from_preserved_serp", selected_url_check)
    check("no_seed_inference_from_urls", all("PAGE_TOPICS_AND_NEW_SEEDS_NOT_INSPECTED_OR_INFERRED" in row["claim_boundary"] for row in candidate_rows))

    report = REPORT.read_text(encoding="utf-8")
    report_tokens = [
        "SOURCE_QUERIES = 75", "SOURCE_RANKED_ROWS = 750", "NORMALIZED_DOMAINS = 237",
        "CHANGED_DECISION` | 26", "DE_RISKED_DECISION` | 20", "CONFIRMED_EXISTING_DECISION` | 19",
        "UNRESOLVED_TRACE` | 10", "PROJECT_TEST_VALIDATED = false",
        "EXACT_NEW_WORDSTAT_SEEDS_REQUIRED_NOW = NONE__NOT_YET_EVIDENCED",
        "EXACT_NEW_SEARCH_QUERIES_REQUIRED_NOW = NONE__PENDING_PAGE_INSPECTION_AND_WORDSTAT_RESULTS",
    ]
    check("report_required_results_present", all(token in report for token in report_tokens), [token for token in report_tokens if token not in report])
    check("report_selected_candidates_present", all(domain in report for domain in EXPECTED_SELECTED))
    check("report_no_full_method_promotion", "METHOD NOT PROMOTED" in report and "PROJECT_TEST_VALIDATED = false" in report)

    provider_calls = payload["provider_calls"]
    check("provider_calls_all_zero", all(value == 0 for value in provider_calls.values()), provider_calls)
    check("public_competitor_page_inspection_false", payload["public_competitor_page_inspection_completed"] is False)
    check("no_exact_wordstat_seeds_invented", payload.get("exact_new_wordstat_seeds_required_now") == [])
    check("no_exact_search_queries_invented", payload.get("exact_new_search_queries_required_now") == [])

    source_hashes = {name: sha256(JOB / name) for name in EXPECTED_SOURCE_HASHES}
    check("preserved_source_hashes_unchanged", source_hashes == EXPECTED_SOURCE_HASHES, source_hashes)
    release = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
    protected_hashes = {name: sha256(release / name) for name in EXPECTED_PROTECTED_HASHES}
    check("protected_artifact_hashes_unchanged", protected_hashes == EXPECTED_PROTECTED_HASHES, protected_hashes)

    relative_out = OUT.relative_to(REPO).as_posix() + "/"
    changed_paths = [line for line in git("diff", "--name-only", STARTING_HEAD).splitlines() if line]
    untracked_paths = [line for line in git("ls-files", "--others", "--exclude-standard").splitlines() if line]
    changed_paths = sorted(set(changed_paths + untracked_paths))
    check("all_changes_isolated_to_step05a_execution", all(path.startswith(relative_out) for path in changed_paths), changed_paths)
    check("historical_step_outputs_unchanged", not any(path.startswith(JOB.relative_to(REPO).as_posix() + "/STEP_") and not path.startswith(relative_out) for path in changed_paths), changed_paths)
    check("corrected_client_release_unchanged", not any(path.startswith(release.relative_to(REPO).as_posix() + "/") for path in changed_paths), changed_paths)

    phase_values = payload.get("phase_status", {})
    check("all_execution_phases_pass", all(phase_values.get(name) == "PASS" for name in ["combined_serp_ledger", "domain_frequency_and_classification", "query_impact_trace", "competitor_candidate_selection", "first_execution_report"]), phase_values)
    artifact_hashes = {
        path.name: {"sha256": sha256(path), "size_bytes": path.stat().st_size}
        for path in [CHECKPOINT, COMBINED, DOMAINS, IMPACT, CANDIDATES, REPORT, LOG, BUILDER, Path(__file__)]
    }

    failed = [item["name"] for item in checks if item["status"] == "FAIL"]
    payload["status"] = "PASS" if not failed else "FAIL"
    payload["project_test_validated"] = False
    payload["owner_review"] = "PENDING"
    payload["deterministic_qa"] = {
        "status": payload["status"],
        "checks_total": len(checks),
        "checks_passed": len(checks) - len(failed),
        "failed": failed,
        "checks": checks,
    }
    payload["final_counts"] = {
        "source_queries": len(by_query),
        "source_ranked_rows": len(combined),
        "normalized_domains": len(domain_rows),
        "impact_counts": expected_impact,
        "candidate_shortlist": len(candidate_rows),
        "selected_competitors": len(selected),
    }
    payload["protected_artifacts_modified"] = {name: protected_hashes[name] != expected for name, expected in EXPECTED_PROTECTED_HASHES.items()}
    payload["artifact_files"] = artifact_hashes
    payload.setdefault("remote_readback", {"status": "PENDING_AFTER_FINALIZATION_COMMIT"})
    QA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": len(checks), "failed": failed, "impact_counts": expected_impact, "selected": EXPECTED_SELECTED}, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
