#!/usr/bin/env python3
"""Validate and freeze the final Fresh-R1 Step-10 result."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

BASE_DIR = Path("extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK")
ACTIVE_DISPOSITIONS = {"CORE_CANDIDATE", "REVIEW_SEARCH"}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def h(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def load_classifier(base: Path):
    path = base / "step10_fresh_r1_pass3_runner_v5.py"
    source = path.read_text(encoding="utf-8")
    terminal = "module.classify = classify_v5\nmodule.invariant_violations = invariants_v5\nraise SystemExit(module.main())"
    replacement = "module.classify = classify_v5\nmodule.invariant_violations = invariants_v5"
    if terminal not in source:
        raise SystemExit("unexpected v5 runner shape")
    namespace = {"__file__": str(path), "__name__": "pass3_v5_validation_library"}
    exec(compile(source.replace(terminal, replacement), str(path), "exec"), namespace)
    return namespace["module"]


def semantic_regression_cases() -> list[tuple[str, str, str]]:
    return [
        ("rehau medea ручка окна", "ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
        ("rehau микролифт для окна", "ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
        ("rehau окна режимы", "ASSIGNED", "WINDOW_PRODUCT_TECH_INFO"),
        ("алюминиевое остекление веранды фото", "ASSIGNED", "GLAZING_DESIGN_INSPIRATION"),
        ("готовые пластиковые окна без установки", "ASSIGNED", "PVC_WINDOWS_COMMERCIAL"),
        ("пластиковые окна без установки москва", "ASSIGNED", "PVC_WINDOWS_COMMERCIAL"),
        ("пластиковые окна в москве с установкой", "ASSIGNED", "PVC_WINDOWS_COMMERCIAL"),
        ("окна rehau цена с установкой", "ASSIGNED", "REHAU_WINDOWS_COMMERCIAL"),
        ("алюминиевые окна цена с установкой", "ASSIGNED", "ALUMINIUM_WINDOWS_COMMERCIAL"),
        ("установка пластиковых окон", "ASSIGNED", "WINDOW_INSTALLATION_SERVICE"),
        ("установка окон rehau", "ASSIGNED", "WINDOW_INSTALLATION_SERVICE"),
        ("установка пластиковой двери", "ASSIGNED", "PVC_DOOR_INSTALLATION_SERVICE"),
        ("как поменять пластиковое окно", "ASSIGNED", "WINDOW_INSTALLATION_DIY_INFO"),
        ("оконная фурнитура отзывы", "ASSIGNED", "WINDOW_HARDWARE_INFO"),
        ("аксессуары для пластиковых окон и дверей", "ASSIGNED", "WINDOW_ACCESSORIES_SHOPPING"),
        ("запчасти для ремонта пластиковых окон", "ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
        ("замена остекления балкона", "ASSIGNED", "WINDOW_REPLACEMENT_SERVICE"),
        ("ремонт остекление балконов москва", "ASSIGNED", "BALCONY_RENOVATION_WITH_GLAZING"),
        ("варианты остекления веранды", "ASSIGNED", "GLAZING_SELECTION_INFO"),
        ("перепланировка французское окно", "ASSIGNED", "GLAZING_PERMISSION_INFO"),
        ("отделка пластиковых окон", "ASSIGNED", "WINDOW_FINISHING_SERVICE"),
        ("корпус пластиковый прозрачная дверь", "ASSIGNED", "OUTSIDE_OTHER"),
        ("внутренние пластиковые двери", "ASSIGNED", "OUTSIDE_INTERIOR_DOORS"),
        ("рейтинг компаний по установке пластиковых окон", "ASSIGNED", "WINDOW_REVIEWS_INFO"),
        ("пластиковые окна видео", "ASSIGNED", "WINDOW_PRODUCT_TECH_INFO"),
        ("как сделать французское окно", "ASSIGNED", "WINDOW_INSTALLATION_DIY_INFO"),
        ("пена установки пластиковых окон", "ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
        ("клинья для установки пластиковых окон", "ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
        ("установка стеклопакета", "ASSIGNED", "WINDOW_REPAIR_SERVICE"),
        ("установка оконной фурнитуры", "ASSIGNED", "WINDOW_REPAIR_SERVICE"),
        ("откосы для пластиковых окон", "ASSIGNED", "WINDOW_ACCESSORIES_SHOPPING"),
        ("подоконник для пластиковых окон", "ASSIGNED", "WINDOW_ACCESSORIES_SHOPPING"),
        ("стекло на пластиковое окно цена", "ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
        ("узлы алюминиевых окон", "ASSIGNED", "WINDOW_HARDWARE_INFO"),
        ("сверление пластикового окна", "ASSIGNED", "WINDOW_INSTALLATION_DIY_INFO"),
        ("зазор при установке пластиковых окон", "ASSIGNED", "WINDOW_INSTALLATION_DIY_INFO"),
        ("остекление балкона с крышей", "ASSIGNED", "BALCONY_GLAZING_ROOF_SERVICE"),
        ("остекление балкона с выносом", "ASSIGNED", "BALCONY_GLAZING_EXTENSION_SERVICE"),
        ("теплое остекление балконов", "ASSIGNED", "BALCONY_GLAZING_WARM"),
        ("холодное остекление балкона", "ASSIGNED", "BALCONY_GLAZING_COLD"),
        ("оконная фурнитура бренды", "ASSIGNED", "WINDOW_HARDWARE_INFO"),
        ("панорамные окна для частного дома размеры", "ASSIGNED", "PRIVATE_HOUSE_WINDOW_PLANNING_INFO"),
        ("официальный дилер окон rehau в москве", "ASSIGNED", "NAVIGATION_BRAND_SITE"),
        ("что лучше пластиковые или алюминиевые окна", "ASSIGNED", "WINDOW_COMPARISON_INFO"),
        ("москитная сетка на пластиковые окна купить", "ASSIGNED", "MOSQUITO_NET_SHOPPING"),
        ("оконные блоки фурнитурой", "SEARCH_REQUIRED", ""),
        ("остекление балкона работу", "SEARCH_REQUIRED", ""),
    ]


def validate_semantic_regression(module) -> int:
    cases = semantic_regression_cases()
    failures = []
    for phrase, expected_status, expected_cluster in cases:
        result = module.classify(phrase, "", "")
        actual = (result.status, result.cluster_id)
        expected = (expected_status, expected_cluster)
        if actual != expected:
            failures.append(
                {
                    "phrase": phrase,
                    "expected_status": expected_status,
                    "expected_cluster": expected_cluster,
                    "actual_status": result.status,
                    "actual_cluster": result.cluster_id,
                    "rule_id": result.rule_id,
                }
            )
    if failures:
        raise SystemExit(
            "semantic regression failures: "
            + json.dumps(failures, ensure_ascii=False, indent=2)
        )
    return len(cases)


def scan_full_assignments(rows: list[dict[str, str]]) -> None:
    failures = []
    professional = {
        "WINDOW_INSTALLATION_SERVICE",
        "WINDOW_REPAIR_SERVICE",
        "WINDOW_FINISHING_SERVICE",
        "WINDOW_REPLACEMENT_SERVICE",
        "WINDOW_DEMOLITION_SERVICE",
        "PVC_DOOR_INSTALLATION_SERVICE",
        "PVC_DOOR_REPAIR_SERVICE",
        "PVC_DOOR_REPLACEMENT_SERVICE",
    }
    base_products = {
        "REHAU_WINDOWS_COMMERCIAL",
        "PVC_WINDOWS_COMMERCIAL",
        "ALUMINIUM_WINDOWS_COMMERCIAL",
        "WINDOWS_COMMERCIAL_GENERAL",
        "PVC_DOORS_COMMERCIAL",
    }
    for row_number, row in enumerate(rows, start=1):
        if row.get("assignment_status") != "ASSIGNED":
            continue
        text = row.get("phrase", "").lower().replace("ё", "е")
        cluster = row.get("cluster_id", "")
        violations: list[str] = []
        component = h(text, r"фурнитур|ручк|петл|уплотн|замок|защелк|микролифт|ограничител|стеклопакет|подоконник|откос|отлив")
        accessory = h(text, r"аксессуар|запчаст|комплектующ|ремкомплект")
        diy = h(text, r"своими руками|самостоятель|самому|пошаг|инструкц|как (?:сделать|установить|снять|заменить|поменять|смонтировать)")
        visual = h(text, r"\bфото\b|дизайн|интерьер|пример|проект")
        permission = h(text, r"разрешен|можно ли|перепланиров|согласован|требован|норматив|\bгост\b|закон")
        review = h(text, r"отзыв|рейтинг|репутац")
        with_install = h(text, r"\bс установк|включая установк|вместе с установк")
        without_install = h(text, r"без (?:установк|монтаж)|не треб.*(?:установк|монтаж)")
        service_primary = h(text, r"^(?:установка|монтаж|установить|смонтировать|заказ и установка|изготовление и установка|производство и установка)\b")
        interior_door = h(text, r"внутренн|межкомнат|в комнат|в ванн|в туалет|дверь купе|гармошк")
        finishing_action = h(text, r"отделк|обшив|облицов|оштукатур|штукатур")
        bare_video = h(text, r"\bвидео\b") and not h(text, r"как|ремонт|почин|замен|поменя|установ|монтаж|снять|регулиров|отделк|остеклен|застекл")

        if component and cluster in base_products:
            violations.append("component_in_base_product")
        if h(text, r"режим|конструкц|что это|как называется") and cluster in base_products and not h(text, r"купить|заказ|цен|стоим"):
            violations.append("technical_information_in_commercial")
        if visual and cluster in {"GLAZING_SELECTION_INFO", "BALCONY_GLAZING_INFO"}:
            violations.append("visual_inspiration_in_selection")
        if h(text, r"алюмин") and cluster == "WINDOWS_COMMERCIAL_GENERAL":
            violations.append("material_object_in_generic")
        if diy and cluster in professional:
            violations.append("diy_in_professional_service")
        if h(text, r"без остеклен|открыт.*балкон") and cluster.startswith("BALCONY_GLAZING_"):
            violations.append("open_balcony_in_glazing")
        if permission and cluster in base_products | {"BALCONY_GLAZING_GENERAL", "OUTDOOR_STRUCTURE_GLAZING", "GENERAL_GLAZING_SERVICE", "FRENCH_WINDOWS_COMMERCIAL", "PANORAMIC_WINDOWS_COMMERCIAL"}:
            violations.append("permission_in_transactional_result")
        if without_install and cluster in {"WINDOW_INSTALLATION_SERVICE", "PVC_DOOR_INSTALLATION_SERVICE"}:
            violations.append("negated_installation_in_service")
        if with_install and not service_primary and cluster in {"WINDOW_INSTALLATION_SERVICE", "PVC_DOOR_INSTALLATION_SERVICE"}:
            violations.append("product_bundle_in_service_only_cluster")
        if review and cluster in professional | base_products | {"BALCONY_GLAZING_GENERAL", "OUTDOOR_STRUCTURE_GLAZING"}:
            violations.append("reviews_in_transactional_result")
        if accessory and cluster in professional | base_products:
            violations.append("accessory_or_spare_part_in_parent_task")
        if interior_door and cluster in {"PVC_DOORS_COMMERCIAL", "PVC_DOOR_INSTALLATION_SERVICE", "PVC_DOOR_REPAIR_SERVICE"}:
            violations.append("interior_door_in_target_pvc_door_task")
        if finishing_action and cluster in base_products:
            violations.append("finishing_action_in_whole_product")
        if bare_video and cluster == "WINDOW_REPAIR_DIY_INFO":
            violations.append("bare_video_in_repair_diy")
        if h(text, r"штор|жалюз|плиссе|занавес|ставн") and cluster != "OUTSIDE_CURTAINS_BLINDS":
            violations.append("curtains_not_outside")
        if h(text, r"конвектор|радиатор|батаре|отоплен|теплый пол|кондиционер") and cluster != "OUTSIDE_HEATING_HVAC":
            violations.append("heating_not_outside")

        if violations:
            failures.append(
                {
                    "source_row": row_number,
                    "phrase": row.get("phrase", ""),
                    "cluster": cluster,
                    "violations": violations,
                }
            )
    if failures:
        raise SystemExit(
            "full-ledger semantic scan failed: "
            + json.dumps(failures[:50], ensure_ascii=False, indent=2)
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    base = args.root.resolve() / BASE_DIR

    paths = {
        "input_taxonomy": base / "STEP_10_FRESH_R1_TAXONOMY.tsv",
        "final_taxonomy": base / "STEP_10_FRESH_R1_TAXONOMY_FINAL.tsv",
        "qa": base / "STEP_10_FRESH_R1_FINAL_QA.json",
        "full": base / "STEP_10_FRESH_R1_PASS3_FULL_QA_LEDGER.tsv",
        "errors": base / "STEP_10_FRESH_R1_PASS3_ERROR_LEDGER.tsv",
        "corrections": base / "STEP_10_FRESH_R1_PASS3_CONSOLIDATED_CORRECTIONS.tsv",
        "assignments": base / "STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv",
        "summary": base / "STEP_10_FRESH_R1_CLUSTER_SUMMARY_FINAL.tsv",
        "impact": base / "STEP_10_FRESH_R1_PASS3_IMPACT_RECHECK.tsv",
        "report": base / "STEP_10_FRESH_R1_PASS3_REPORT.md",
        "complete_marker": base / "STEP_10_FRESH_R1_COMPLETE.marker",
    }
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise SystemExit("missing final artifacts: " + ", ".join(missing))

    qa = json.loads(paths["qa"].read_text(encoding="utf-8"))
    input_taxonomy = read_tsv(paths["input_taxonomy"])
    final_taxonomy = read_tsv(paths["final_taxonomy"])
    full = read_tsv(paths["full"])
    errors = read_tsv(paths["errors"])
    corrections = read_tsv(paths["corrections"])
    assignments = read_tsv(paths["assignments"])
    summary = read_tsv(paths["summary"])
    impact = read_tsv(paths["impact"])

    active = [row for row in assignments if row.get("source_disposition") in ACTIVE_DISPOSITIONS]
    assigned = [row for row in active if row.get("assignment_status") == "ASSIGNED"]
    search_required = [row for row in active if row.get("assignment_status") == "SEARCH_REQUIRED"]
    deferred = [row for row in assignments if row.get("assignment_status") == "PRESERVED_DEFERRED"]
    excluded = [row for row in assignments if row.get("assignment_status") == "PRESERVED_EXCLUDED"]

    input_ids = [row["cluster_id"] for row in input_taxonomy]
    final_ids = [row["cluster_id"] for row in final_taxonomy]
    summary_ids = [row["cluster_id"] for row in summary]
    assigned_ids = {row["cluster_id"] for row in assigned}
    retired_ids = [cluster_id for cluster_id in input_ids if cluster_id not in set(final_ids)]
    unknown = sorted(assigned_ids - set(final_ids))

    checks = {
        "source_rows_2840": len(assignments) == 2840 == qa.get("source_rows"),
        "active_rows_2332": len(active) == 2332 == qa.get("active_rows"),
        "full_qa_rows_2332": len(full) == 2332 == qa.get("pass3_rows_independently_reviewed"),
        "qa_row_sequence_exact": [int(row["qa_row"]) for row in full] == list(range(1, 2333)),
        "error_ledger_complete": len(errors) == qa.get("pass3_error_ledger_rows"),
        "error_correction_identity": len(errors) == len(corrections) == qa.get("consolidated_correction_rows"),
        "correction_ids_unique": len({row["correction_id"] for row in corrections}) == len(corrections),
        "exactly_one_batch": qa.get("correction_batches_applied") == 1 and qa.get("one_consolidated_correction_batch") is True,
        "impact_correction_identity": len(impact) == len(corrections) == qa.get("impact_rows_rechecked"),
        "all_impact_rows_pass": all(row["impact_recheck_verdict"] == "PASS" for row in impact),
        "active_accounting_exact": len(assigned) + len(search_required) == 2332 == qa.get("final_active_accounted_rows"),
        "assigned_accounting_exact": len(assigned) == qa.get("final_assigned_active_rows"),
        "search_required_accounting_exact": len(search_required) == qa.get("final_search_required_active_rows"),
        "preserved_deferred_174": len(deferred) == 174 == qa.get("preserved_deferred_rows"),
        "preserved_excluded_334": len(excluded) == 334 == qa.get("preserved_excluded_rows"),
        "input_taxonomy_accounted": len(input_taxonomy) == qa.get("input_taxonomy_cluster_ids"),
        "active_taxonomy_summary_identity": final_ids == summary_ids and len(final_ids) == qa.get("taxonomy_cluster_ids") == qa.get("used_cluster_ids"),
        "active_taxonomy_has_members": all(int(row["assigned_rows"]) > 0 for row in summary),
        "assigned_clusters_equal_active_taxonomy": assigned_ids == set(final_ids),
        "retired_candidate_identity": retired_ids == qa.get("retired_zero_assignment_cluster_ids"),
        "zero_member_active_clusters_zero": qa.get("zero_assignment_cluster_ids") == [],
        "member_evidence_gate": qa.get("final_active_taxonomy_has_member_evidence") is True,
        "unknown_cluster_ids_zero": unknown == [] == qa.get("unknown_cluster_ids"),
        "impact_failures_zero": qa.get("impact_recheck_failures") == 0,
        "semantic_invariants_zero": qa.get("semantic_invariant_violations") == 0,
        "pass3_complete": qa.get("pass3_complete") is True,
        "ledger_frozen_before_correction": qa.get("complete_error_ledger_frozen_before_correction") is True,
        "full_accounting_regression_pass": qa.get("full_accounting_regression_pass") is True,
        "impact_semantic_recheck_pass": qa.get("impact_set_semantic_recheck_pass") is True,
        "old_step10_not_used": qa.get("old_step10_input_used") is False,
        "blind84_not_used": qa.get("blind84_input_used") is False,
        "target_count_not_used": qa.get("target_cluster_count_used") is False,
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise SystemExit("final accounting/taxonomy validation failed: " + ", ".join(failed))

    module = load_classifier(base)
    regression_count = validate_semantic_regression(module)
    scan_full_assignments(assignments)

    artifact_names = [
        "STEP_10_FRESH_R1_TAXONOMY_FINAL.tsv",
        "STEP_10_FRESH_R1_PASS3_FULL_QA_LEDGER.tsv",
        "STEP_10_FRESH_R1_PASS3_ERROR_LEDGER.tsv",
        "STEP_10_FRESH_R1_PASS3_CONSOLIDATED_CORRECTIONS.tsv",
        "STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv",
        "STEP_10_FRESH_R1_CLUSTER_SUMMARY_FINAL.tsv",
        "STEP_10_FRESH_R1_PASS3_IMPACT_RECHECK.tsv",
        "STEP_10_FRESH_R1_FINAL_QA.json",
        "STEP_10_FRESH_R1_PASS3_REPORT.md",
        "STEP_10_FRESH_R1_COMPLETE.marker",
    ]
    marker = {
        "status": "STEP10_FRESH_R1_FINAL_VERIFIED",
        "source_rows": qa["source_rows"],
        "active_rows": qa["active_rows"],
        "independently_reviewed_rows": qa["pass3_rows_independently_reviewed"],
        "error_ledger_rows": len(errors),
        "consolidated_correction_rows": len(corrections),
        "correction_batches": qa["correction_batches_applied"],
        "final_assigned_rows": qa["final_assigned_active_rows"],
        "final_search_required_rows": qa["final_search_required_active_rows"],
        "final_active_accounted_rows": qa["final_active_accounted_rows"],
        "input_taxonomy_cluster_ids": qa["input_taxonomy_cluster_ids"],
        "final_active_taxonomy_cluster_ids": qa["taxonomy_cluster_ids"],
        "retired_zero_assignment_cluster_ids": qa["retired_zero_assignment_cluster_ids"],
        "zero_member_active_clusters": 0,
        "impact_rows_rechecked": qa["impact_rows_rechecked"],
        "impact_failures": qa["impact_recheck_failures"],
        "semantic_invariant_violations": qa["semantic_invariant_violations"],
        "semantic_regression_cases": regression_count,
        "semantic_regression_failures": 0,
        "full_ledger_semantic_scan_failures": 0,
        "old_step10_input_used": qa["old_step10_input_used"],
        "blind84_input_used": qa["blind84_input_used"],
        "target_cluster_count_used": qa["target_cluster_count_used"],
        "sha256": {name: digest(base / name) for name in artifact_names},
    }
    marker_path = base / "STEP_10_FRESH_R1_PASS3_V5_VERIFIED.marker.json"
    marker_path.write_text(json.dumps(marker, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"checks": checks, "qa": qa, "marker": marker}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
