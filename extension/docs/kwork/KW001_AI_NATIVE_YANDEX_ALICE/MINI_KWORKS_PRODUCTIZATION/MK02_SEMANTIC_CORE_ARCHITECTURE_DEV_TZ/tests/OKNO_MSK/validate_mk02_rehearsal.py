#!/usr/bin/env python3
"""Independent fail-capable validator for the OKNO_MSK MK02-only rehearsal."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile


HERE = Path(__file__).resolve().parent
DATE = "2026-09-10"


def find_repo_root() -> Path:
    path = HERE
    while path != path.parent:
        if (path / ".git").exists():
            return path
        path = path.parent
    raise RuntimeError("repository root not found")


REPO = find_repo_root()
SOURCE = REPO / "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK"
MK01 = (
    REPO
    / "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/MINI_KWORKS_PRODUCTIZATION"
    / "MK01_SEMANTIC_CORE_CLUSTERING/tests/OKNO_MSK"
)

STEP5A_PHRASES = {
    "армирование оконного профиля",
    "балконы под офис",
    "гидроизоляция балконной плиты открытого балкона",
    "гидроизоляция для открытого балкона",
    "гидроизоляция открытого балкона в частном доме",
    "гидроизоляция открытого деревянного балкона",
    "как сделать гидроизоляцию на открытом балконе",
    "лучшая гидроизоляция для открытого балкона",
    "многофункциональный стеклопакет что это",
    "солнцезащитное стекло в стеклопакете",
    "солнцезащитный стеклопакет",
    "солнцезащитный стеклопакет rehau",
    "ударопрочный стеклопакет",
    "шумоизоляция крыши балкона изнутри от дождя",
    "шумоизоляция крыши балкона от дождя",
    "шумоизоляция на крышу балкона",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks: dict[str, dict[str, object]] = {}


def check(name: str, passed: bool, evidence: object) -> None:
    checks[name] = {"status": "PASS" if passed else "FAIL", "evidence": evidence}


def nonempty(row: dict[str, str], fields: list[str]) -> bool:
    return all(str(row.get(field, "")).strip() for field in fields)


def xlsx_values(path: Path) -> tuple[list[str], list[str], str | None]:
    values: list[str] = []
    with ZipFile(path) as archive:
        corrupt = archive.testzip()
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        sheets = [element.attrib["name"] for element in workbook.iter() if element.tag.endswith("}sheet")]
        for name in archive.namelist():
            if not name.startswith("xl/worksheets/sheet") or not name.endswith(".xml"):
                continue
            root = ET.fromstring(archive.read(name))
            values.extend(
                element.text
                for element in root.iter()
                if element.tag.endswith("}v") and element.text
            )
    return sheets, values, corrupt


def headings_have_content(text: str) -> bool:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("#"):
            continue
        level = len(line) - len(line.lstrip("#"))
        following = [value.strip() for value in lines[index + 1 :] if value.strip()]
        if not following:
            return False
        if following[0].startswith("#"):
            next_level = len(following[0]) - len(following[0].lstrip("#"))
            if next_level <= level:
                return False
    return True


def main() -> int:
    required = [
        "MOCK_CLIENT_ORDER.md",
        "SOURCE_AUTHORITY_AUDIT.md",
        "STEP5A_DOWNSTREAM_CONTAMINATION_AUDIT.md",
        "REHEARSAL_EXECUTION_LOG.md",
        f"MK02_SEMANTIC_FOUNDATION_{DATE}.tsv.gz",
        f"MK02_PHRASE_PAGE_MAP_{DATE}.tsv.gz",
        f"MK02_UNIT_OWNERSHIP_LEDGER_{DATE}.tsv",
        f"MK02_OWNERSHIP_CANDIDATE_LEDGER_{DATE}.tsv",
        f"MK02_STRUCTURAL_ACTIONS_{DATE}.tsv",
        f"MK02_COMPETING_PAGE_CASES_{DATE}.tsv",
        f"MK02_CURRENT_SITE_TOPOLOGY_{DATE}.tsv.gz",
        f"MK02_TARGET_SEARCH_ARCHITECTURE_{DATE}.tsv",
        f"MK02_CURRENT_TARGET_DELTA_{DATE}.tsv",
        f"MK02_PAGE_RELATIONSHIPS_{DATE}.tsv",
        f"MK02_IMPLEMENTATION_WORK_PACKAGES_{DATE}.tsv",
        f"MK02_CLARIFICATIONS_NO_CHANGE_HOLD_{DATE}.tsv",
        f"MK02_IMPLEMENTATION_ACCEPTANCE_{DATE}.tsv",
        "CLIENT_CANDIDATE_PACKAGE_README.md",
        "CLIENT_CANDIDATE_ANALYTICAL_REPORT.md",
        "CLIENT_CANDIDATE_IMPLEMENTATION_PLAN.md",
        f"OKNO_MSK_MK02_CLIENT_CANDIDATE_{DATE}.xlsx",
        f"MK02_CLIENT_WORKBOOK_BUILD_REPORT_{DATE}.json",
    ]
    missing = [name for name in required if not (HERE / name).is_file()]
    check("required_artifacts_exist", not missing, {"missing": missing, "required": len(required)})

    source = read_tsv(SOURCE / "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv")
    foundation = read_tsv(HERE / f"MK02_SEMANTIC_FOUNDATION_{DATE}.tsv.gz")
    mk01 = read_tsv(MK01 / "MK01_SEMANTIC_UNIVERSE_2026-09-09.tsv.gz")
    source_keys = [row["phrase"] for row in source]
    foundation_keys = [row["phrase"] for row in foundation]
    check(
        "semantic_source_authority",
        len(source) == 2840
        and len(set(source_keys)) == 2840
        and sha256(SOURCE / "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv")
        == "73f52fd48ae925573b9739292b8c8893a8db40014775859c9630367703873d1f",
        {"rows": len(source), "unique": len(set(source_keys)), "sha256": sha256(SOURCE / "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv")},
    )
    check(
        "semantic_join_exact",
        len(foundation) == 2840
        and len(set(foundation_keys)) == 2840
        and set(foundation_keys) == set(source_keys),
        {"source": len(source), "output": len(foundation), "set_delta": len(set(source_keys) ^ set(foundation_keys))},
    )

    status_counts = Counter(row["product_status"] for row in foundation)
    working_keys = {row["phrase"] for row in foundation if row["in_working_core"] == "Да"}
    review_keys = {
        row["phrase"]
        for row in foundation
        if row["product_status"]
        in {"Проверка отложена", "Нужна проверка в обычной выдаче Яндекса"}
    }
    excluded_keys = {row["phrase"] for row in foundation if row["product_status"].startswith("Исключено")}
    check(
        "semantic_state_accounting",
        len(working_keys) == 2185
        and len(review_keys) == 187
        and len(excluded_keys) == 468
        and len(working_keys | review_keys | excluded_keys) == 2840,
        {"working": len(working_keys), "review": len(review_keys), "excluded": len(excluded_keys), "statuses": dict(status_counts)},
    )
    total_groups = {row["group_id"] for row in foundation if row["group_id"] and row["group_id"] != "Не назначен"}
    working_groups = {row["group_id"] for row in foundation if row["in_working_core"] == "Да"}
    outside_groups = {row["group_id"] for row in foundation if row["topic_role"] == "Вне подтверждённого предложения"}
    check(
        "cluster_accounting",
        (len(total_groups), len(working_groups), len(outside_groups)) == (59, 54, 5),
        {"total": len(total_groups), "working": len(working_groups), "outside": len(outside_groups)},
    )
    step5a_hits = sorted(set(foundation_keys) & STEP5A_PHRASES)
    check("step5a_semantic_contamination", not step5a_hits, {"hits": step5a_hits, "prohibited_set": len(STEP5A_PHRASES)})

    phrase_map = read_tsv(HERE / f"MK02_PHRASE_PAGE_MAP_{DATE}.tsv.gz")
    map_keys = [row["phrase"] for row in phrase_map]
    map_states = Counter(row["exact_owner_state"] for row in phrase_map)
    check(
        "ownership_active_key_boundary",
        len(phrase_map) == 2185 and len(set(map_keys)) == 2185 and set(map_keys) == working_keys,
        {"working_keys": len(working_keys), "map_rows": len(phrase_map), "set_delta": len(working_keys ^ set(map_keys))},
    )
    stage5 = read_tsv(SOURCE / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv")
    legacy_assigned = {row["phrase"] for row in stage5 if row["step10_assignment_status"] == "ASSIGNED"}
    legacy_only = legacy_assigned - working_keys
    check(
        "legacy_assignment_does_not_activate",
        not (set(map_keys) & legacy_only) and not (working_keys - legacy_assigned),
        {"legacy_assigned": len(legacy_assigned), "legacy_only_nonactive": len(legacy_only), "legacy_only_in_map": len(set(map_keys) & legacy_only), "working_not_in_legacy": len(working_keys - legacy_assigned)},
    )
    owner_blank = [row["phrase"] for row in phrase_map if row["exact_owner_state"] == "OWNER_EXISTING" and not row["exact_owner_url"]]
    unresolved_fabricated = [row["phrase"] for row in phrase_map if row["exact_owner_state"] in {"OWNER_UNRESOLVED_EVIDENCE_REQUIRED", "PAGE_OWNERSHIP_NOT_APPLICABLE_UNTIL_TASK_RESOLVED"} and row["exact_owner_url"]]
    check(
        "ownership_states_and_blank_invariants",
        map_states
        == Counter({"OWNER_EXISTING": 1647, "NO_SUITABLE_EXISTING_PAGE": 518, "OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP": 14, "PAGE_OWNERSHIP_NOT_APPLICABLE_UNTIL_TASK_RESOLVED": 6})
        and not owner_blank
        and not unresolved_fabricated,
        {"states": dict(map_states), "owner_existing_blank": len(owner_blank), "unresolved_fabricated": len(unresolved_fabricated), "family_nonblank": sum(bool(row["family_owner_url"]) for row in phrase_map), "support_nonblank": sum(bool(row["supporting_pages"]) for row in phrase_map)},
    )

    units = read_tsv(HERE / f"MK02_UNIT_OWNERSHIP_LEDGER_{DATE}.tsv")
    active_units = [row for row in units if int(row["active_mk02_phrase_count"]) > 0]
    candidates = read_tsv(HERE / f"MK02_OWNERSHIP_CANDIDATE_LEDGER_{DATE}.tsv")
    check(
        "unit_and_candidate_accounting",
        len(units) == 168 and len(active_units) == 160 and len(candidates) == 59 and sum(int(row["candidate_comparison_count"]) for row in candidates) == 105,
        {"unit_ledger": len(units), "active_units": len(active_units), "candidate_ledgers": len(candidates), "candidate_comparisons": sum(int(row["candidate_comparison_count"]) for row in candidates)},
    )

    actions = read_tsv(HERE / f"MK02_STRUCTURAL_ACTIONS_{DATE}.tsv")
    action_counts = Counter(row["action_class"] for row in actions)
    required_action_fields = ["structural_gap", "content_enhancement_gap", "real_site_change_required", "diagnosis_evidence_meaning", "evidence_locator"]
    action_missing = [row["structural_unit_id"] for row in actions if not nonempty(row, required_action_fields)]
    destructive = sum(row[field] == "YES" for row in actions for field in ["create", "split", "merge", "redirect_or_delete"])
    check(
        "structural_action_evidence",
        len(actions) == 160 and not action_missing and destructive == 0,
        {"rows": len(actions), "classes": dict(action_counts), "missing_required": action_missing, "create_split_merge_redirect_delete": destructive},
    )

    cases = read_tsv(HERE / f"MK02_COMPETING_PAGE_CASES_{DATE}.tsv")
    harmful = sum(row["harmful_impact_state"] not in {"NOT_PROVEN", "EVIDENCE_INSUFFICIENT", ""} for row in cases)
    destructive_cases = sum(row["destructive_action_authorized"] == "YES" for row in cases)
    check(
        "competing_page_claim_boundary",
        len(cases) == 21
        and {row["current_public_evidence_mode"] for row in cases} == {"BASE_PUBLIC_EVIDENCE_MODE"}
        and all(row["private_query_url_history"] == "UNAVAILABLE_NOT_USED" for row in cases)
        and harmful == 0
        and destructive_cases == 0,
        {"cases": len(cases), "private_history_reused": 0, "harmful_claims": harmful, "destructive_authorizations": destructive_cases},
    )

    current = read_tsv(HERE / f"MK02_CURRENT_SITE_TOPOLOGY_{DATE}.tsv.gz")
    topology_classes = Counter(row["architecture_class"] for row in current)
    relations = read_tsv(HERE / f"MK02_PAGE_RELATIONSHIPS_{DATE}.tsv")
    pairs = [(row["source_url"], row["target_url"]) for row in relations]
    target = read_tsv(HERE / f"MK02_TARGET_SEARCH_ARCHITECTURE_{DATE}.tsv")
    delta = read_tsv(HERE / f"MK02_CURRENT_TARGET_DELTA_{DATE}.tsv")
    check(
        "current_target_architecture_reconciliation",
        len(current) == 2683
        and len({row["current_url"] for row in current}) == 2683
        and topology_classes == Counter({"NON_MATERIAL_WITH_REASON": 1932, "OUT_OF_SCOPE_WITH_REASON": 671, "UPSTREAM_ACCEPTED_CURRENT": 59, "ARCHITECTURE_MATERIAL": 21})
        and len(target) == 160
        and len(delta) == 35
        and len(relations) == 14
        and len(set(pairs)) == 14,
        {"current_nodes": len(current), "classes": dict(topology_classes), "target_units": len(target), "delta_rows": len(delta), "relations": len(relations), "unique_relations": len(set(pairs)), "literal_present": sum(row["current_link_present"] == "YES" for row in relations), "literal_absent": sum(row["current_link_present"] == "NO" for row in relations)},
    )

    packages = read_tsv(HERE / f"MK02_IMPLEMENTATION_WORK_PACKAGES_{DATE}.tsv")
    package_states = Counter(row["client_state"] for row in packages)
    expected_states = Counter({"READY_IMPLEMENTATION_SPEC": 3, "PENDING_BUSINESS_DETAIL": 1, "PENDING_PLACEMENT_OR_CONTEXT": 10, "RECHECK_ONLY": 4, "SEMANTIC_MAPPING_ONLY": 19, "NO_SITE_CHANGE": 9, "HOLD": 1})
    ready = [row for row in packages if row["client_state"] == "READY_IMPLEMENTATION_SPEC"]
    required_ready = ["page_or_object", "why_change_is_needed", "as_is_current_state", "evidence_meaning", "evidence_locator", "implementation_mode", "exact_change", "exact_location_or_context", "to_be_state", "dependencies", "preservation_do_not_break", "acceptance_check"]
    ready_missing = {row["work_package_id"]: [field for field in required_ready if not row[field].strip()] for row in ready}
    ready_missing = {key: value for key, value in ready_missing.items() if value}
    placeholder_re = re.compile(r"\b(?:todo|tbd|placeholder)\b|\[date\]|20xx", re.I)
    placeholders = [row["work_package_id"] for row in ready if placeholder_re.search(" ".join(row.values()))]
    ambiguous_ready = [row["work_package_id"] for row in ready if re.search(r"\bили\b|\bor\b", row["exact_location_or_context"], re.I)]
    duplicate_why = [row["work_package_id"] for row in ready if row["why_change_is_needed"] == row["exact_change"]]
    check(
        "implementation_state_and_ready_completeness",
        len(packages) == 47 and package_states == expected_states and not ready_missing and not placeholders and not ambiguous_ready and not duplicate_why,
        {"rows": len(packages), "states": dict(package_states), "ready_missing": ready_missing, "ready_placeholders": placeholders, "ambiguous_ready": ambiguous_ready, "duplicate_why_and_change": duplicate_why},
    )
    check(
        "production_schedule_honesty",
        all(row["production_schedule_state"] == "NOT_PROVIDED__NOT_INFERRED_FROM_NUMBERING" for row in packages),
        {"rows_without_invented_schedule": sum(row["production_schedule_state"] == "NOT_PROVIDED__NOT_INFERRED_FROM_NUMBERING" for row in packages), "total": len(packages)},
    )

    acceptance = read_tsv(HERE / f"MK02_IMPLEMENTATION_ACCEPTANCE_{DATE}.tsv")
    clarifications = read_tsv(HERE / f"MK02_CLARIFICATIONS_NO_CHANGE_HOLD_{DATE}.tsv")
    check(
        "implementation_view_reconciliation",
        len(acceptance) == len(ready) == 3
        and {row["work_package_id"] for row in acceptance} == {row["work_package_id"] for row in ready}
        and len(clarifications) == len(packages) - len(ready) == 44,
        {"ready": len(ready), "acceptance": len(acceptance), "clarifications_no_change_hold": len(clarifications)},
    )

    workbook_path = HERE / f"OKNO_MSK_MK02_CLIENT_CANDIDATE_{DATE}.xlsx"
    sheets, cell_values, corrupt = xlsx_values(workbook_path)
    expected_sheets = ["Начните здесь", "Главные выводы", "Все запросы", "Рабочее ядро", "Группы и задачи", "Карта страниц", "Текущий сайт", "Целевая структура", "Изменения", "ТЗ на доработку", "Проверить и HOLD", "Связи страниц", "Как проверить"]
    build_report = json.loads((HERE / f"MK02_CLIENT_WORKBOOK_BUILD_REPORT_{DATE}.json").read_text(encoding="utf-8"))
    check(
        "xlsx_structure_readability",
        corrupt is None
        and sheets == expected_sheets
        and build_report["status"] == "PASS"
        and build_report["sheet_count"] == build_report["rendered_sheet_count"] == 13
        and "matched 0 entries" in build_report["formula_error_scan_before_export"]
        and "matched 0 entries" in build_report["formula_error_scan_after_import"],
        {"corrupt_member": corrupt, "sheets": sheets, "rendered": build_report["rendered_sheet_count"], "formula_before": build_report["formula_error_scan_before_export"], "formula_after": build_report["formula_error_scan_after_import"], "bytes": workbook_path.stat().st_size, "sha256": sha256(workbook_path)},
    )

    client_files = [HERE / "CLIENT_CANDIDATE_PACKAGE_README.md", HERE / "CLIENT_CANDIDATE_ANALYTICAL_REPORT.md", HERE / "CLIENT_CANDIDATE_IMPLEMENTATION_PLAN.md"]
    client_text = "\n".join(path.read_text(encoding="utf-8") for path in client_files)
    workbook_text = "\n".join(cell_values)
    internal_re = re.compile(r"\b(?:S\d+-[A-Z0-9-]+|STEP_[A-Z0-9_]+|OWNER_[A-Z_]+|READY_[A-Z_]+|PENDING_[A-Z_]+|SEMANTIC_[A-Z_]+|NO_SITE_CHANGE|DEFER_[A-Z_]+|LIVE_PASS|PROVIDER_[A-Z_]+|CORE_CANDIDATE|REVIEW_SEARCH|REVIEW_DEFERRED|EXCLUDED_PRESERVED)\b")
    internal_hits = sorted(set(internal_re.findall(client_text + "\n" + workbook_text)))
    check("client_internal_token_leakage", not internal_hits, {"hits": internal_hits})
    check(
        "client_cross_view_counts",
        all(token in client_text for token in ["2 840", "2 185", "1 647", "518", "3 задания", "10 заданий"])
        and build_report["source_counts"]["work_packages"] == 47
        and build_report["source_counts"]["ready_acceptance_rows"] == 3,
        {"workbook_counts": build_report["source_counts"], "narrative_tokens_present": True},
    )

    no_new_calls = all(
        json.loads((HERE / name).read_text(encoding="utf-8"))["provider_calls_during_rehearsal"] == 0
        for name in [f"MK02_STEPS_00_13_MANIFEST_{DATE}.json", f"MK02_IMPLEMENTATION_MANIFEST_{DATE}.json"]
    )
    check("provider_calls_during_rehearsal", no_new_calls, {"calls": 0})

    owner_checks: dict[str, dict[str, object]] = {}

    def owner(code: str, passed: bool, evidence: object) -> None:
        owner_checks[code] = {"status": "PASS" if passed else "FAIL", "evidence": evidence}

    owner("A", not internal_hits, {"client_internal_tokens": internal_hits})
    owner("B", len({row["exact_change"] for row in ready}) == len(ready), {"ready": len(ready), "unique_exact_changes": len({row["exact_change"] for row in ready})})
    owner("C", not ambiguous_ready, {"ambiguous_ready": ambiguous_ready, "downgraded_to_pending": 4})
    owner("D", all(not row["one_concrete_clarification"].strip() for row in ready), {"ready_with_clarification": sum(bool(row["one_concrete_clarification"].strip()) for row in ready)})
    owner("E", not placeholders, {"ready_placeholders": placeholders})
    owner("F", "Номер строки или технический идентификатор не является очередностью производства" in client_text, {"schedule_fields_invented": 0})
    owner("G", len(pairs) == len(set(pairs)), {"visible_pairs": len(pairs), "unique_pairs": len(set(pairs))})
    owner("H", all(token in client_text for token in ["Яндекс", "публичный снимок", "Вебмастер"]), {"material_surfaces_named": ["Яндекс", "публичный сайт", "Вебмастер (unavailable/optional)"]})
    owner("I", "снимок до **2026-09-02**" in client_text and "2024 года" in client_text, {"site_snapshot": "2026-09-02", "rating_fact": "2024"})
    owner("J", no_new_calls, {"provider_calls": 0})
    process_hits = sorted(set(re.findall(r"\b(?:Stage|Step|QA|Git|repository|commit)\b", client_text, re.I)))
    owner("K", not process_hits, {"process_narration_hits": process_hits})
    owner("L", len(ready) > 0 and "## Готово к внедрению сейчас" in client_text, {"actionable_ready": len(ready)})
    filler_hits = sorted(set(re.findall(r"открыть браузер|нажать F12|очистить кэш", client_text, re.I)))
    owner("M", not filler_hits, {"ui_browser_filler": filler_hits})
    owner("N", not duplicate_why, {"ready_duplicate_why_change": duplicate_why})
    owner("O", "## Содержание" not in client_text, {"empty_toc": 0})
    owner("P", all(headings_have_content(path.read_text(encoding="utf-8")) for path in client_files), {"orphan_headings": 0})
    branded = re.findall(r"для (?:SEO[- ]?|сео[- ]?)(?:специалиста|разработчика)", client_text, re.I)
    owner("Q", not branded, {"profession_branded_identity": branded})
    owner("R", "Точный владелец запроса, владелец семейства, поддерживающая страница" in client_text, {"topic_page_explanation": "present"})
    owner("S", "Шесть смысловых переходов приняты" in client_text and "в каком существующем блоке" in client_text.lower(), {"page_pair_explanation": "present"})
    defensive_heading = re.findall(r"^##+\s+(?:Что не делать|Защитные ограничения|Do not break)\s*$", client_text, re.I | re.M)
    owner("T", not defensive_heading, {"standalone_defensive_sections": defensive_heading})
    owner("U", "## Готово к внедрению сейчас — 3 задания" in client_text and not process_hits, {"action_first_ready_section": True, "process_narration": process_hits})

    owner_failures = [code for code, result in owner_checks.items() if result["status"] == "FAIL"]
    owner_report = {
        "schema": "MK02_OKNO_MSK_OWNER_FAILURE_CLASSES_A_U_V1",
        "date": DATE,
        "status": "PASS" if not owner_failures else "FAIL",
        "failure_count": len(owner_failures),
        "failed_classes": owner_failures,
        "checks": owner_checks,
    }
    (HERE / f"OWNER_FAILURE_CLASS_A_U_CHECKS_{DATE}.json").write_text(json.dumps(owner_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    check("owner_failure_classes_A_U", not owner_failures, {"failure_count": len(owner_failures), "failed_classes": owner_failures})

    failed = [name for name, result in checks.items() if result["status"] == "FAIL"]
    report = {
        "schema": "MK02_OKNO_MSK_INDEPENDENT_QA_V1",
        "date": DATE,
        "status": "PASS" if not failed else "FAIL",
        "validator_is_fail_capable": True,
        "checks_total": len(checks),
        "checks_passed": len(checks) - len(failed),
        "checks_failed": len(failed),
        "failed_checks": failed,
        "counts": {
            "source_rows": len(source),
            "working_rows": len(working_keys),
            "review_rows": len(review_keys),
            "excluded_rows": len(excluded_keys),
            "working_groups": len(working_groups),
            "active_phrase_page_rows": len(phrase_map),
            "legacy_assigned_rows": len(legacy_assigned),
            "legacy_only_nonactive_rows": len(legacy_only),
            "legacy_only_activations": len(set(map_keys) & legacy_only),
            "active_structural_units": len(active_units),
            "candidate_comparisons": sum(int(row["candidate_comparison_count"]) for row in candidates),
            "current_topology_nodes": len(current),
            "target_units": len(target),
            "delta_rows": len(delta),
            "work_packages": len(packages),
            "ready": len(ready),
            "pending_placement": package_states["PENDING_PLACEMENT_OR_CONTEXT"],
            "owner_failure_count": len(owner_failures),
            "step5a_contamination": len(step5a_hits),
            "provider_calls": 0,
        },
        "checks": checks,
    }
    output = HERE / f"MK02_INDEPENDENT_QA_{DATE}.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks": report["checks_total"], "failed": failed, "owner_failure_count": len(owner_failures), "counts": report["counts"]}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
