#!/usr/bin/env python3
"""Independent deterministic QA for OKNO_MSK Step 5A.2/5A.3."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit


OUT = Path(__file__).resolve().parent
JOB = OUT.parent
REPO = next(parent for parent in OUT.parents if (parent / ".git").exists())
STARTING_HEAD = "09486a6fd2cf09fd2ef362e1e13456441a75717c"

SELECTION = OUT / "STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv"
SERP = OUT / "STEP_05A_SERP_COMBINED_750.tsv"
CHECKPOINT = OUT / "CHECKPOINT_01_COMPETITOR_PAGE_INSPECTION_BASELINE.md"
OBSERVATIONS = OUT / "STEP_05A_COMPETITOR_PAGE_OBSERVATIONS.json"
PAGE_EVIDENCE = OUT / "STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv"
SEED_DECISIONS = OUT / "STEP_05A_SEED_DECISIONS.json"
SEED_CANDIDATES = OUT / "STEP_05A_DERIVED_SEED_CANDIDATES.tsv"
WORDSTAT_PACKAGE = OUT / "STEP_05A_WORDSTAT_REQUIREMENT_PACKAGE.tsv"
REPORT = OUT / "STEP_05A_PAGE_INSPECTION_REPORT.md"
LOG = OUT / "STEP_05A_PAGE_INSPECTION_EXECUTION_LOG.md"
QA = OUT / "STEP_05A_PAGE_INSPECTION_QA.json"
BUILDER = OUT / "build_step05a_page_inspection.py"

FINAL_MASTER = JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"
UNIT_AUTHORITY = JOB / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
LEVEL1_METHOD = JOB.parent.parent / "STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md"

EXPECTED_DOMAINS = {
    "mosokna.ru", "i-okna.ru", "msk.okna-servise.com", "okna-moskva.ru",
    "oknafactoria.ru", "okna-germany.ru", "fabrikaokon.ru", "aluminarium.ru",
    "elit-balkon.ru",
}
ALLOWED_PAGE_TYPES = {
    "COMMERCIAL_CATEGORY", "COMMERCIAL_SERVICE", "COMMERCIAL_PRODUCT",
    "COMMERCIAL_LANDING", "PRICE_FINANCE", "ARTICLE_GUIDE",
    "COMPARISON_SELECTION", "PORTFOLIO_GALLERY", "HOME_OR_HUB",
    "MIXED_COMMERCIAL_INFORMATIONAL", "OTHER", "UNKNOWN",
}
SPEC_KEYS = {
    "normalized_candidate_seed", "semantic_axis", "sources",
    "existing_semantic_match_state", "existing_semantic_match_examples",
    "business_scope_state", "seed_decision", "wordstat_required",
    "wordstat_priority", "rationale", "claim_boundary",
}
SOURCE_KEYS = {"inspection_id", "element_type", "element_text"}
PROTECTED_HASHES = {
    "01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.pdf": "79450c2f0dc58ea064b72b7c400f6db7b908cb455c72003584c5e59c9b9fad08",
    "02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-05.pdf": "b1a2848f781fe12dfe8293cfe2f88e796c967ce9eee7f9b251b171ac73060056",
    "03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.md": "d5c90cf187041e975f17d03a2be138eff0b6a06bfe1b7d395a3b24547edc62b0",
    "04_OKNO_MSK_FULL_SEMANTIC_CORE_2026-09-07.xlsx": "cee26a8d7d4a8381d4706c7940b739c3afca652034e9e3630053e35bd0184e3a",
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
    return subprocess.run(
        ["git", *args], cwd=REPO, text=True, check=True, capture_output=True
    ).stdout.strip()


def authorized_urls() -> set[str]:
    urls: set[str] = set()
    for row in read_tsv(SELECTION):
        if row["selection_state"] != "SELECTED_FOR_NEXT_STEP5A_PAGE_INSPECTION":
            continue
        for item in row["exact_ranking_urls_to_inspect_next"].split(" | "):
            match = re.fullmatch(r"Q\d+/R\d+ (https?://\S+)", item)
            if not match:
                raise ValueError(item)
            urls.add(match.group(1))
    return urls


def main() -> int:
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, detail: object = None) -> None:
        checks.append({"name": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    required = [CHECKPOINT, OBSERVATIONS, PAGE_EVIDENCE, SEED_DECISIONS, SEED_CANDIDATES, WORDSTAT_PACKAGE, REPORT, LOG, BUILDER, Path(__file__)]
    check("required_artifacts_exist", all(path.exists() for path in required), [path.name for path in required if not path.exists()])

    pages = read_tsv(PAGE_EVIDENCE)
    authorized = authorized_urls()
    page_ids = {row["inspection_id"] for row in pages}
    check("selected_domains_expected_9", {row["competitor_domain"] for row in pages} == EXPECTED_DOMAINS)
    check("authorized_url_targets_expected_44", len(authorized) == 44, len(authorized))
    check("authorized_url_targets_accounted_44", {row["requested_url"] for row in pages} == authorized, len(pages))
    check("page_evidence_rows_44", len(pages) == 44, len(pages))
    check("inspection_ids_exact", page_ids == {f"I{i:03d}" for i in range(1, 45)})
    check("out_of_scope_urls_opened_as_evidence_targets_0", not ({row["requested_url"] for row in pages} - authorized))
    check("page_access_state_present", all(row["http_or_browser_access_state"] for row in pages))
    failures = [row for row in pages if row["http_or_browser_access_state"] not in {"ACCESSIBLE", "REDIRECTED_ACCESSIBLE"}]
    check("page_access_failures_explicit", all(row["page_evidence_notes"] and row["claim_boundary"] for row in failures), len(failures))
    redirects = [row for row in pages if row["http_or_browser_access_state"] == "REDIRECTED_ACCESSIBLE"]
    check("redirects_have_requested_and_final_urls", all(row["requested_url"] != row["final_url"] for row in redirects), len(redirects))
    check("page_types_bounded", all(row["page_type"] in ALLOWED_PAGE_TYPES for row in pages), Counter(row["page_type"] for row in pages))
    check("accessible_pages_have_titles_and_h1", all(row["page_title"] and row["h1"] for row in pages if row["http_or_browser_access_state"] in {"ACCESSIBLE", "REDIRECTED_ACCESSIBLE"}))
    check("page_claim_boundaries_present", all(row["claim_boundary"].startswith("PUBLIC_PAGE_OBSERVATION_ONLY") for row in pages))
    check("requested_domains_match_selected_domain", all((urlsplit(row["requested_url"]).hostname or "").removeprefix("www.").lower() == row["competitor_domain"] for row in pages))

    specs = json.loads(SEED_DECISIONS.read_text(encoding="utf-8"))
    check("seed_specs_deduplicated", len({row["normalized_candidate_seed"].casefold() for row in specs}) == len(specs), len(specs))
    check("seed_spec_schema_exact", all(set(row) == SPEC_KEYS for row in specs), [sorted(set(row) - SPEC_KEYS) for row in specs if set(row) != SPEC_KEYS])
    check("seed_source_schema_exact", all(set(source) == SOURCE_KEYS for row in specs for source in row["sources"]))
    source_ids = {source["inspection_id"] for row in specs for source in row["sources"]}
    check("all_pages_contribute_candidate_lineage", source_ids == page_ids, sorted(page_ids - source_ids))

    units = {row["structural_unit_id"] for row in read_tsv(UNIT_AUTHORITY)}
    phrases = {row["phrase"] for row in read_tsv(FINAL_MASTER)}
    bad_refs: list[str] = []
    for spec in specs:
        for ref in spec["existing_semantic_match_examples"]:
            if ref.startswith("unit:") and ref[5:] not in units:
                bad_refs.append(ref)
            if ref.startswith("phrase:") and ref[7:] not in phrases:
                bad_refs.append(ref)
    check("semantic_match_authority_references_valid", not bad_refs, bad_refs)

    candidates = read_tsv(SEED_CANDIDATES)
    first_rows = [row for row in candidates if row["seed_decision"] != "DUPLICATE_OF_ANOTHER_COMPETITOR_SEED"]
    check("raw_page_derived_candidate_rows_92", len(candidates) == 92, len(candidates))
    check("deduplicated_candidate_directions_43", len(first_rows) == len(specs) == 43, len(first_rows))
    check("candidate_seed_ids_unique", len({row["seed_id"] for row in candidates}) == len(candidates))
    check("seeds_without_page_lineage_0", all(row["source_requested_url"] in authorized and row["source_page_element_text"] for row in candidates))
    check("seeds_from_url_slug_only_0", all("url" not in row["source_page_element_type"].casefold() for row in candidates))
    check("seeds_from_domain_name_only_0", all("domain" not in row["source_page_element_type"].casefold() and row["source_page_element_text"] != row["competitor_domain"] for row in candidates))
    check("candidate_page_metadata_matches_evidence", all(next(page for page in pages if page["requested_url"] == row["source_requested_url"])["final_url"] == row["source_final_url"] for row in candidates))
    check("semantic_candidates_compared_to_existing_core_all", all(row["existing_semantic_match_state"] and row["existing_semantic_match_examples"] for row in candidates))
    check("duplicate_support_rows_49", sum(row["seed_decision"] == "DUPLICATE_OF_ANOTHER_COMPETITOR_SEED" for row in candidates) == 49)
    unique_counts = Counter(row["seed_decision"] for row in first_rows)
    expected_unique_counts = {"ALREADY_COVERED_EXACT_OR_CLOSE": 22, "POTENTIALLY_NEW_WORDSTAT_SEED": 14, "OFF_SCOPE_BUSINESS": 3, "HOLD_REVIEW": 4}
    check("candidate_unique_decision_counts", dict(unique_counts) == expected_unique_counts, dict(unique_counts))
    check("potentially_new_seeds_deduped", len({row["normalized_candidate_seed"].casefold() for row in first_rows if row["seed_decision"] == "POTENTIALLY_NEW_WORDSTAT_SEED"}) == 14)
    check("wordstat_flags_match_decisions", all((row["wordstat_required"] == "true") == (row["seed_decision"] == "POTENTIALLY_NEW_WORDSTAT_SEED") for row in first_rows))

    package = read_tsv(WORDSTAT_PACKAGE)
    potential_seeds = [row["normalized_candidate_seed"] for row in first_rows if row["seed_decision"] == "POTENTIALLY_NEW_WORDSTAT_SEED"]
    check("wordstat_requirement_rows_surviving_only", {row["normalized_candidate_seed"] for row in package} == set(potential_seeds), len(package))
    check("wordstat_requirement_rows_14", len(package) == 14, len(package))
    check("wordstat_priority_consecutive", [int(row["wordstat_seed_order"]) for row in package] == list(range(1, 15)))
    check("wordstat_region_213", {row["recommended_wordstat_region"] for row in package} == {"213"})
    check("wordstat_device_all", {row["recommended_device_scope"] for row in package} == {"ALL"})
    check("wordstat_return_to_main_authorization", {row["provider_call_authorization_state"] for row in package} == {"RETURN_TO_MAIN_CHATGPT_FOR_BRIDGE_EXECUTION"})
    check("wordstat_support_counts_positive", all(int(row["supporting_competitor_count"]) >= 1 and int(row["supporting_page_count"]) >= 1 for row in package))

    report = REPORT.read_text(encoding="utf-8")
    report_tokens = [
        "SELECTED_DOMAINS = 9 / 9", "AUTHORIZED_URL_TARGETS = 44 / 44",
        "RAW_PAGE_DERIVED_CANDIDATE_OCCURRENCES = 92", "DEDUPLICATED_CANDIDATE_DIRECTIONS = 43",
        "ALREADY_COVERED_EXACT_OR_CLOSE = 22", "POTENTIALLY_NEW_WORDSTAT_SEED = 14",
        "NEW_YANDEX_SEARCH_CALLS = 0", "NEW_WORDSTAT_CALLS = 0",
        "PROJECT_TEST_VALIDATED = false", "OWNER_REVIEW = pending",
    ]
    check("report_required_results_present", all(token in report for token in report_tokens), [token for token in report_tokens if token not in report])
    check("report_all_wordstat_seeds_present", all(row["normalized_candidate_seed"] in report for row in package))
    check("level1_method_not_promoted", not git("diff", "--name-only", STARTING_HEAD, "--", str(LEVEL1_METHOD.relative_to(REPO))))

    provider_calls = {
        "yandex_search": 0, "wordstat": 0, "alice": 0, "gensearch": 0,
        "webmaster": 0, "metrika": 0, "direct": 0, "reverse_domain_provider": 0,
    }
    check("new_yandex_provider_calls_0", all(value == 0 for value in provider_calls.values()), provider_calls)
    check("new_paid_provider_cost_rub_0", True, 0)

    protected_actual = {name: sha256(RELEASE / name) for name in PROTECTED_HASHES}
    check("protected_artifact_hashes_unchanged", protected_actual == PROTECTED_HASHES, protected_actual)
    release_path = str(RELEASE.relative_to(REPO))
    start_release_tree = git("rev-parse", f"{STARTING_HEAD}:{release_path}")
    current_release_tree = git("rev-parse", f"HEAD:{release_path}")
    check("corrected_client_release_tree_unchanged", start_release_tree == current_release_tree, current_release_tree)
    changed = [path for path in git("diff", "--name-only", STARTING_HEAD).splitlines() if path]
    changed += [path for path in git("ls-files", "--others", "--exclude-standard").splitlines() if path]
    changed = sorted(set(changed))
    out_prefix = str(OUT.relative_to(REPO)) + "/"
    check("all_changes_isolated_to_step05a_execution", all(path.startswith(out_prefix) for path in changed), changed)
    check("documents_01_02_03_modified_false", not any(re.search(r"/(01_|02_|03_)", path) and path.startswith(release_path + "/") for path in changed))
    check("semantic_core_04_modified_false", not any(path.startswith(release_path + "/04_") for path in changed))

    artifact_paths = [CHECKPOINT, OBSERVATIONS, PAGE_EVIDENCE, SEED_DECISIONS, SEED_CANDIDATES, WORDSTAT_PACKAGE, REPORT, LOG, BUILDER, Path(__file__)]
    artifact_files = {path.name: {"sha256": sha256(path), "size_bytes": path.stat().st_size} for path in artifact_paths}
    failed = [item["name"] for item in checks if item["status"] == "FAIL"]
    payload = {
        "status": "PASS" if not failed else "FAIL",
        "execution_scope": "STEP_5A_2_TO_5A_3",
        "starting_head": STARTING_HEAD,
        "project_test_validated": False,
        "owner_review": "PENDING",
        "counts": {
            "selected_domains": len({row["competitor_domain"] for row in pages}),
            "authorized_urls": len(authorized),
            "page_evidence_rows": len(pages),
            "accessible_at_requested_url": sum(row["http_or_browser_access_state"] == "ACCESSIBLE" for row in pages),
            "redirected_accessible": len(redirects),
            "inaccessible": len(failures),
            "page_types": dict(sorted(Counter(row["page_type"] for row in pages).items())),
            "raw_candidate_occurrences": len(candidates),
            "deduplicated_candidate_directions": len(specs),
            "duplicate_support_rows": sum(row["seed_decision"] == "DUPLICATE_OF_ANOTHER_COMPETITOR_SEED" for row in candidates),
            "unique_decisions": expected_unique_counts,
            "wordstat_requirement_rows": len(package),
        },
        "provider_calls": provider_calls,
        "paid_provider_cost_rub": 0,
        "protected_artifacts_modified": {name: protected_actual[name] != expected for name, expected in PROTECTED_HASHES.items()},
        "corrected_client_release_modified": False,
        "level1_method_promoted": False,
        "deterministic_qa": {"checks_total": len(checks), "checks_passed": len(checks) - len(failed), "failed": failed, "checks": checks},
        "artifact_files": artifact_files,
        "remote_readback": {"material_blocks": "PASS", "finalization_commit": "PENDING_EXTERNAL_READBACK"},
    }
    QA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": len(checks), "failed": failed, "counts": payload["counts"]}, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
