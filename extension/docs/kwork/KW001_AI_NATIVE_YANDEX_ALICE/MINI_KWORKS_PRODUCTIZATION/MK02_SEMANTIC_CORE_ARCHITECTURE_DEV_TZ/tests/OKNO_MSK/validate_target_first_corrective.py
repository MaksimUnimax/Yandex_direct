#!/usr/bin/env python3
"""Fail-capable validator for the corrected target-first OKNO_MSK delivery."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import posixpath
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile


HERE = Path(__file__).resolve().parent
DATE = "2026-09-10"
DELIVERY = HERE / f"CLIENT_DELIVERY_PHASE_7_TARGET_FIRST_CORRECTED_{DATE}"
OUTPUT = HERE / f"TARGET_FIRST_CORRECTIVE_MACHINE_QA_{DATE}.json"

FOUNDATION = HERE / f"MK02_SEMANTIC_FOUNDATION_{DATE}.tsv.gz"
PHRASES = HERE / f"TARGET_FIRST_PHRASE_LANDING_MAP_{DATE}.tsv.gz"
CLUSTERS = HERE / f"TARGET_FIRST_CLUSTER_LANDING_MAP_{DATE}.tsv"
REGISTRY = HERE / f"TARGET_PAGE_REGISTRY_{DATE}.tsv"
HIERARCHY = HERE / f"TARGET_ARCHITECTURE_HIERARCHY_{DATE}.tsv"
RECONCILIATION = HERE / f"CURRENT_TARGET_RECONCILIATION_{DATE}.tsv"
SPECS = HERE / f"TARGET_PAGE_SPEC_REGISTER_{DATE}.tsv"
DELTA = HERE / f"CURRENT_TARGET_CHANGE_DELTA_{DATE}.tsv"
MANIFEST = HERE / f"TARGET_FIRST_CORRECTIVE_MANIFEST_{DATE}.json"
WORKBOOK_REPORT = HERE / f"TARGET_FIRST_CLIENT_WORKBOOK_BUILD_REPORT_{DATE}.json"
PDF_REPORT = HERE / f"TARGET_FIRST_CLIENT_PDF_BUILD_REPORT_{DATE}.json"
PHYSICAL_REPORT = HERE / f"TARGET_FIRST_FINAL_BYTE_PHYSICAL_QA_{DATE}.json"
RECIPIENT_REPORT = HERE / f"TARGET_FIRST_PRODUCT_RECIPIENT_QA_{DATE}.md"

XLSX_NAME = f"SEMANTIC_CORE_AND_TARGET_SEO_STRUCTURE_OKNO_MSK_{DATE}.xlsx"
ANALYTICAL_NAME = f"TARGET_SEO_ARCHITECTURE_REPORT_OKNO_MSK_{DATE}.pdf"
TZ_NAME = f"TARGET_PAGE_SPECIFICATION_TZ_OKNO_MSK_{DATE}.pdf"

EXPECTED_SHEETS = [
    "Начните здесь",
    "Все запросы",
    "Кластеры и задачи",
    "Рассадка запросов",
    "Посадочные страницы",
    "Целевая структура",
    "Реестр страниц",
    "ТЗ по страницам",
    "Изменения сайта",
    "Проверить и отложено",
    "Связи страниц",
    "Текущий сайт",
    "Как проверить",
]

ROUTE_STATES = {
    "TARGET_PAGE_RESOLVED",
    "NO_STANDALONE_ROUTE_TO_PARENT",
    "RECHECK_NEEDS_EVIDENCE",
    "NO_TARGET_OUTSIDE_SCOPE",
    "UNRESOLVED_TASK_ROUTING",
}
UNRESOLVED_ROUTE_STATES = {
    "RECHECK_NEEDS_EVIDENCE",
    "NO_TARGET_OUTSIDE_SCOPE",
    "UNRESOLVED_TASK_ROUTING",
}
ACTION_STATES = {
    "KEEP_LOCK_AS_TARGET_OWNER",
    "OPTIMIZE_STRENGTHEN",
    "ROUTE_INTERNAL_LINK_CHANGE",
    "RECHECK_NEEDS_EVIDENCE",
}
READY_STATES = {
    "READY_IMPLEMENTATION_SPEC",
    "PENDING_BUSINESS_DETAIL",
    "PENDING_PLACEMENT_OR_CONTEXT",
}

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

checks: dict[str, dict[str, object]] = {}


def check(name: str, passed: bool, evidence: object) -> None:
    checks[name] = {"status": "PASS" if passed else "FAIL", "evidence": evidence}


def read_tsv(path: Path) -> list[dict[str, str]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nonempty(row: dict[str, str], fields: list[str]) -> bool:
    return all(str(row.get(field, "")).strip() for field in fields)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def command_text(arguments: list[str]) -> str:
    completed = subprocess.run(arguments, check=True, capture_output=True, text=True, encoding="utf-8")
    return completed.stdout


def pdf_pages(path: Path) -> int:
    match = re.search(r"^Pages:\s+(\d+)\s*$", command_text(["pdfinfo", str(path)]), re.MULTILINE)
    if not match:
        raise RuntimeError(f"page count unavailable for {path.name}")
    return int(match.group(1))


def pdf_text(path: Path) -> str:
    return command_text(["pdftotext", "-layout", str(path), "-"])


def normalize_xl_target(base: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(base), target))


def xlsx_inspect(path: Path) -> dict[str, object]:
    main_ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    package_rel_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    m = f"{{{main_ns}}}"
    r = f"{{{rel_ns}}}"
    pr = f"{{{package_rel_ns}}}"
    texts: list[str] = []
    with ZipFile(path) as archive:
        corrupt = archive.testzip()
        names = set(archive.namelist())
        shared: list[str] = []
        if "xl/sharedStrings.xml" in names:
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = ["".join(node.text or "" for node in item.iter(m + "t")) for item in shared_root.iter(m + "si")]

        workbook_path = "xl/workbook.xml"
        workbook = ET.fromstring(archive.read(workbook_path))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {node.attrib["Id"]: normalize_xl_target(workbook_path, node.attrib["Target"]) for node in rels.iter(pr + "Relationship")}
        sheets: list[str] = []
        frozen: list[str] = []
        table_part_sheets: list[str] = []
        for node in workbook.iter(m + "sheet"):
            sheet_name = node.attrib["name"]
            sheets.append(sheet_name)
            sheet_path = targets[node.attrib[r + "id"]]
            sheet_root = ET.fromstring(archive.read(sheet_path))
            pane = sheet_root.find(".//" + m + "pane")
            if pane is not None and pane.attrib.get("state") == "frozen":
                frozen.append(sheet_name)
            table_parts = sheet_root.find(m + "tableParts")
            if table_parts is not None and int(table_parts.attrib.get("count", "0")) > 0:
                table_part_sheets.append(sheet_name)
            for cell in sheet_root.iter(m + "c"):
                value_type = cell.attrib.get("t")
                value = cell.find(m + "v")
                if value_type == "inlineStr":
                    texts.append("".join(item.text or "" for item in cell.iter(m + "t")))
                elif value is not None and value.text:
                    if value_type == "s":
                        texts.append(shared[int(value.text)])
                    else:
                        texts.append(value.text)

        table_paths = sorted(name for name in names if re.fullmatch(r"xl/tables/table\d+\.xml", name))
        tables_with_filters = 0
        for table_path in table_paths:
            root = ET.fromstring(archive.read(table_path))
            if root.find(m + "autoFilter") is not None:
                tables_with_filters += 1
        return {
            "corrupt_member": corrupt,
            "sheets": sheets,
            "frozen_sheets": frozen,
            "table_part_sheets": table_part_sheets,
            "table_count": len(table_paths),
            "tables_with_filters": tables_with_filters,
            "texts": texts,
        }


def main() -> int:
    required = [
        FOUNDATION,
        PHRASES,
        CLUSTERS,
        REGISTRY,
        HIERARCHY,
        RECONCILIATION,
        SPECS,
        DELTA,
        MANIFEST,
        WORKBOOK_REPORT,
        PDF_REPORT,
        PHYSICAL_REPORT,
        RECIPIENT_REPORT,
        HERE / "build_target_first_corrective_rework.py",
        HERE / "build_target_first_client_workbook.mjs",
        HERE / "build_target_first_client_pdfs.py",
        DELIVERY / XLSX_NAME,
        DELIVERY / ANALYTICAL_NAME,
        DELIVERY / TZ_NAME,
    ]
    missing = [str(path.relative_to(HERE)) for path in required if not path.is_file()]
    check("required_target_first_artifacts_exist", not missing, {"required": len(required), "missing": missing})
    if missing:
        return finalize()

    foundation = read_tsv(FOUNDATION)
    phrases = read_tsv(PHRASES)
    clusters = read_tsv(CLUSTERS)
    registry = read_tsv(REGISTRY)
    hierarchy = read_tsv(HIERARCHY)
    reconciliation = read_tsv(RECONCILIATION)
    specs = read_tsv(SPECS)
    delta = read_tsv(DELTA)
    manifest = load_json(MANIFEST)
    workbook_report = load_json(WORKBOOK_REPORT)
    pdf_report = load_json(PDF_REPORT)
    physical_report = load_json(PHYSICAL_REPORT)

    working = {row["phrase_id"] for row in foundation if row["in_working_core"] == "Да"}
    review = {
        row["phrase_id"]
        for row in foundation
        if row["product_status"] in {"Проверка отложена", "Нужна проверка в обычной выдаче Яндекса"}
    }
    excluded = {row["phrase_id"] for row in foundation if row["product_status"].startswith("Исключено")}
    all_ids = [row["phrase_id"] for row in foundation]
    check(
        "source_authority_accounting",
        len(foundation) == len(set(all_ids)) == 2840
        and len(working) == 2185
        and len(review) == 187
        and len(excluded) == 468
        and working.isdisjoint(review)
        and working.isdisjoint(excluded)
        and review.isdisjoint(excluded)
        and len(working | review | excluded) == 2840,
        {"universe": len(foundation), "unique": len(set(all_ids)), "working": len(working), "review": len(review), "excluded": len(excluded)},
    )

    phrase_keys = [row["phrase_key"] for row in phrases]
    route_counts = Counter(row["target_route_state"] for row in phrases)
    phrase_missing_fields = [
        row["phrase_key"]
        for row in phrases
        if not nonempty(row, ["phrase_key", "phrase", "cluster_task_key", "cluster_task_name_ru", "target_route_state", "target_action"])
    ]
    check(
        "working_phrase_routes_complete",
        len(phrases) == len(set(phrase_keys)) == 2185
        and set(phrase_keys) == working
        and not phrase_missing_fields
        and set(route_counts).issubset(ROUTE_STATES),
        {"rows": len(phrases), "unique": len(set(phrase_keys)), "silent_drops": len(working ^ set(phrase_keys)), "states": dict(route_counts), "missing_fields": phrase_missing_fields[:20]},
    )
    no_standalone_bad = [
        row["phrase_key"]
        for row in phrases
        if row["target_route_state"] == "NO_STANDALONE_ROUTE_TO_PARENT"
        and (not row["target_landing_page_key"] or not row["target_landing_page_name_ru"] or not row["target_url_after_reconciliation"])
    ]
    fabricated_phrase_urls = [
        row["phrase_key"] for row in phrases if row["target_route_state"] in UNRESOLVED_ROUTE_STATES and row["target_url_after_reconciliation"]
    ]
    resolved_without_url = [
        row["phrase_key"]
        for row in phrases
        if row["target_route_state"] in {"TARGET_PAGE_RESOLVED", "NO_STANDALONE_ROUTE_TO_PARENT"} and not row["target_url_after_reconciliation"]
    ]
    check(
        "phrase_route_safety",
        not no_standalone_bad and not fabricated_phrase_urls and not resolved_without_url,
        {"no_standalone_without_named_owner": len(no_standalone_bad), "unresolved_with_fabricated_url": len(fabricated_phrase_urls), "resolved_without_url": len(resolved_without_url)},
    )

    cluster_keys = [row["cluster_task_key"] for row in clusters]
    cluster_missing = [row["cluster_task_key"] for row in clusters if not nonempty(row, ["cluster_task_key", "cluster_task_name_ru", "intent_user_task_ru", "intended_target_page_name_ru", "target_route_state", "target_action"])]
    cluster_fabricated_urls = [row["cluster_task_key"] for row in clusters if row["target_route_state"] in UNRESOLVED_ROUTE_STATES and row["target_url_after_reconciliation"]]
    check(
        "cluster_routes_complete_and_explicit",
        len(clusters) == len(set(cluster_keys)) == 161
        and not cluster_missing
        and not cluster_fabricated_urls
        and {row["target_route_state"] for row in clusters}.issubset(ROUTE_STATES),
        {"rows": len(clusters), "unique": len(set(cluster_keys)), "missing_fields": cluster_missing[:20], "unresolved_with_fabricated_url": cluster_fabricated_urls},
    )

    registry_keys = [row["target_page_key"] for row in registry]
    hierarchy_keys = [row["target_page_key"] for row in hierarchy]
    reconciliation_keys = [row["target_page_key"] for row in reconciliation]
    spec_target_keys = [row["target_page_key"] for row in specs]
    key_sets = [set(registry_keys), set(hierarchy_keys), set(reconciliation_keys), set(spec_target_keys)]
    headers_registry = set(registry[0]) if registry else set()
    headers_hierarchy = set(hierarchy[0]) if hierarchy else set()
    current_columns = sorted(
        [f"registry:{name}" for name in headers_registry if "current" in name.lower()]
        + [f"hierarchy:{name}" for name in headers_hierarchy if "current" in name.lower()]
    )
    provisional_http = [row["target_page_key"] for row in registry if "http" in row["provisional_target_route"].lower()]
    accepted_derivation_bases = {
        "ACCEPTED_WORKING_SEMANTICS__USER_TASK__INTENT__EXPECTED_PAGE_ROLE",
        "EXPLICIT_UNRESOLVED_ROUTE__NOT_CURRENT_URL_COPY",
    }
    derivation_bad = [
        row["target_page_key"]
        for row in registry
        if row["target_derivation_basis"] not in accepted_derivation_bases
    ]
    check(
        "target_model_frozen_before_current_reconciliation",
        len(registry_keys) == len(set(registry_keys)) == 60
        and all(len(keys) == 60 for keys in [hierarchy_keys, reconciliation_keys, spec_target_keys])
        and all(keys == key_sets[0] for keys in key_sets[1:])
        and not current_columns
        and not provisional_http
        and not derivation_bad,
        {"registry": len(registry_keys), "hierarchy": len(hierarchy_keys), "reconciliation": len(reconciliation_keys), "specs": len(spec_target_keys), "current_columns": current_columns, "provisional_http": provisional_http, "derivation_failures": derivation_bad},
    )
    unresolved_registry = [row for row in registry if row["target_route_url_state"] == "UNRESOLVED__NO_URL_FABRICATED"]
    registry_bad_routes = [
        row["target_page_key"]
        for row in registry
        if row["target_route_url_state"] not in {"LOGICAL_TARGET_ROLE_DEFINED__URL_NOT_USED_AS_DESIGN_INPUT", "UNRESOLVED__NO_URL_FABRICATED"}
    ]
    check(
        "unresolved_target_role_is_explicit",
        len(unresolved_registry) == 1
        and unresolved_registry[0]["provisional_target_route"].startswith("TARGET_ROLE::")
        and not registry_bad_routes,
        {"unresolved_roles": len(unresolved_registry), "unknown_route_states": registry_bad_routes},
    )

    spec_keys = [row["page_spec_key"] for row in specs]
    required_spec_fields = [
        "page_spec_key",
        "target_page_key",
        "target_page_name_ru",
        "target_url_or_route",
        "page_type",
        "page_purpose",
        "primary_user_task_intent",
        "what_page_should_cover",
        "what_belongs_elsewhere_or_not_standalone",
        "target_action",
        "real_site_change_required",
        "acceptance_target_end_state",
        "uncertainty_exact_clarification",
    ]
    incomplete_specs = [row["target_page_key"] for row in specs if not nonempty(row, required_spec_fields)]
    keep_keys = {row["target_page_key"] for row in reconciliation if row["target_action"] == "KEEP_LOCK_AS_TARGET_OWNER"}
    recon_states = Counter(row["current_match_state"] for row in reconciliation)
    action_states = Counter(row["target_action"] for row in reconciliation)
    check(
        "full_page_specs_include_keep",
        len(specs) == len(set(spec_keys)) == 60
        and not incomplete_specs
        and keep_keys.issubset(set(spec_target_keys))
        and set(action_states).issubset(ACTION_STATES)
        and action_states == Counter({"KEEP_LOCK_AS_TARGET_OWNER": 48, "OPTIMIZE_STRENGTHEN": 7, "ROUTE_INTERNAL_LINK_CHANGE": 4, "RECHECK_NEEDS_EVIDENCE": 1}),
        {"specs": len(specs), "unique_spec_keys": len(set(spec_keys)), "incomplete_specs": incomplete_specs, "keep_pages": len(keep_keys), "keep_without_spec": len(keep_keys - set(spec_target_keys)), "reconciliation_states": dict(recon_states), "actions": dict(action_states)},
    )

    spec_by_key = {row["page_spec_key"]: row for row in specs}
    delta_missing_spec = [row["change_delta_key"] for row in delta if row["page_spec_key"] not in spec_by_key or row["target_page_key"] != spec_by_key.get(row["page_spec_key"], {}).get("target_page_key")]
    delta_missing_fields = [
        row["change_delta_key"]
        for row in delta
        if not nonempty(row, ["change_delta_key", "page_spec_key", "target_page_key", "target_page_name_ru", "current_object", "target_action", "readiness_state", "why_change_is_needed", "exact_change", "exact_location_or_context", "target_end_state", "acceptance_check", "preservation_do_not_break"])
    ]
    ready = [row for row in delta if row["readiness_state"] == "READY_IMPLEMENTATION_SPEC"]
    ready_with_clarification = [row["change_delta_key"] for row in ready if row["one_concrete_clarification"].strip()]
    check(
        "change_delta_is_spec_subset",
        len(delta) == 14
        and not delta_missing_spec
        and not delta_missing_fields
        and {row["readiness_state"] for row in delta}.issubset(READY_STATES)
        and len(ready) == 3
        and not ready_with_clarification
        and Counter(row["real_site_change_required"] for row in delta) == Counter({"YES": 8, "UNRESOLVED": 6}),
        {"change_rows": len(delta), "ready": len(ready), "physical_change_states": dict(Counter(row["real_site_change_required"] for row in delta)), "missing_spec": delta_missing_spec, "missing_fields": delta_missing_fields, "ready_with_clarification": ready_with_clarification},
    )

    step5a_hits = sorted({row["phrase"] for row in foundation} & STEP5A_PHRASES)
    manifest_invariants = manifest.get("qa_invariants", {})
    manifest_outputs = manifest.get("outputs", {})
    manifest_hash_failures = [
        name
        for name, record in manifest_outputs.items()
        if not (HERE / name).is_file()
        or sha256(HERE / name) != record.get("sha256")
        or (HERE / name).stat().st_size != record.get("bytes")
    ]
    check(
        "manifest_boundaries_and_authority_hashes",
        manifest.get("status") == "PASS"
        and manifest.get("provider_calls") == 0
        and manifest.get("source_counts") == {"semantic_universe": 2840, "working": 2185, "review": 187, "excluded": 468}
        and manifest_invariants
        and all(value == 0 for value in manifest_invariants.values())
        and not manifest_hash_failures
        and not step5a_hits,
        {"provider_calls": manifest.get("provider_calls"), "invariants": manifest_invariants, "hash_failures": manifest_hash_failures, "step5a_hits": step5a_hits},
    )

    client_files = sorted(path for path in DELIVERY.iterdir() if path.is_file())
    check(
        "client_package_exactly_three_files",
        [path.name for path in client_files] == sorted([XLSX_NAME, ANALYTICAL_NAME, TZ_NAME]),
        {"files": [path.name for path in client_files], "count": len(client_files)},
    )

    xlsx_path = DELIVERY / XLSX_NAME
    workbook = xlsx_inspect(xlsx_path)
    workbook_text = "\n".join(workbook["texts"])
    check(
        "xlsx_structure_filters_freezes_and_formulas",
        workbook["corrupt_member"] is None
        and workbook["sheets"] == EXPECTED_SHEETS
        and len(workbook["frozen_sheets"]) == 13
        and len(workbook["table_part_sheets"]) == 12
        and workbook["table_count"] == workbook["tables_with_filters"] == 12
        and workbook_report.get("status") == "PASS"
        and workbook_report.get("sheet_count") == workbook_report.get("rendered_sheet_count") == 13
        and "matched 0 entries" in str(workbook_report.get("formula_error_scan_before_export"))
        and "matched 0 entries" in str(workbook_report.get("formula_error_scan_after_import"))
        and workbook_report.get("output", {}).get("sha256") == sha256(xlsx_path)
        and workbook_report.get("output", {}).get("bytes") == xlsx_path.stat().st_size,
        {"corrupt_member": workbook["corrupt_member"], "sheets": workbook["sheets"], "frozen": len(workbook["frozen_sheets"]), "table_sheets": len(workbook["table_part_sheets"]), "tables": workbook["table_count"], "filter_tables": workbook["tables_with_filters"], "sha256": sha256(xlsx_path), "bytes": xlsx_path.stat().st_size},
    )
    page_names = [row["target_page_name_ru"] for row in registry]
    missing_page_names_xlsx = [name for name in page_names if name not in workbook_text]
    check(
        "xlsx_client_content_reconciliation",
        not missing_page_names_xlsx
        and all(token in workbook_text for token in ["2840", "2185", "187", "468", "161", "60", "48", "14"]),
        {"visible_cells": len(workbook["texts"]), "characters": len(workbook_text), "missing_target_page_names": missing_page_names_xlsx},
    )

    analytical_path = DELIVERY / ANALYTICAL_NAME
    tz_path = DELIVERY / TZ_NAME
    analytical_pages = pdf_pages(analytical_path)
    tz_pages = pdf_pages(tz_path)
    analytical_text = pdf_text(analytical_path)
    tz_text = pdf_text(tz_path)
    pdf_records = {record["file"]: record for record in pdf_report.get("outputs", [])}
    pdf_hash_failures = [
        path.name
        for path, pages in [(analytical_path, analytical_pages), (tz_path, tz_pages)]
        if path.name not in pdf_records
        or pdf_records[path.name].get("sha256") != sha256(path)
        or pdf_records[path.name].get("bytes") != path.stat().st_size
        or pdf_records[path.name].get("pages") != pages
    ]
    missing_page_names_tz = [name for name in page_names if name not in tz_text]
    required_analytical_sections = [
        "1. Как построена целевая модель",
        "5. Карта целевых посадочных страниц",
        "6. Целевая SEO-структура",
        "7. Сверка целевой модели с текущим сайтом",
        "8. Что реально меняется",
        "9. Как использовать результат",
    ]
    check(
        "pdf_hashes_pages_and_client_content",
        pdf_report.get("status") == "PASS"
        and analytical_pages == 22
        and tz_pages == 71
        and not pdf_hash_failures
        and not missing_page_names_tz
        and all(section in analytical_text for section in required_analytical_sections)
        and "Страница 60 из 60" in tz_text,
        {"analytical_pages": analytical_pages, "page_specification_pages": tz_pages, "hash_failures": pdf_hash_failures, "missing_target_page_names": missing_page_names_tz, "required_sections_present": all(section in analytical_text for section in required_analytical_sections)},
    )

    combined_client_text = "\n".join([workbook_text, analytical_text, tz_text])
    leakage_patterns = {
        "authority_id": re.compile(r"\b(?:TP|PS|CTD|WP|SEC)-[A-Z0-9-]+\b"),
        "raw_state": re.compile(r"\b(?:STEP|TARGET|OWNER|CURRENT|READY|PENDING|RECHECK|ROUTE|NO_STANDALONE|NO_TARGET|OUTSIDE_SCOPE)_[A-Z0-9_]+\b"),
        "process_english": re.compile(r"\b(?:Stage|Phase|provider calls?|evidence|tickets?|company-specific|exact-match|CTA|AI|Alice|Neuro|Git|commit|repository)\b", re.IGNORECASE),
        "project_process_label": re.compile(r"\bMK02\b"),
        "source_id": re.compile(r"\b(?:ФР-[0-9A-F]+|S\d{2})\b"),
        "internal_key_phrase": re.compile(r"по ключу (?:страницы|целевой страницы)", re.IGNORECASE),
    }
    leakage = {name: sorted(set(pattern.findall(combined_client_text))) for name, pattern in leakage_patterns.items()}
    leakage = {name: values for name, values in leakage.items() if values}
    generic_enums = sorted(set(re.findall(r"\b[A-Z]{2,}_[A-Z0-9_]+\b", combined_client_text)) - {"OKNO_MSK"})
    replacement_glyphs = combined_client_text.count("\ufffd")
    check(
        "client_visible_internal_leakage",
        not leakage and not generic_enums and replacement_glyphs == 0,
        {"specific_hits": leakage, "generic_raw_enums": generic_enums, "replacement_glyphs": replacement_glyphs},
    )

    physical_records = {record["file"]: record for record in physical_report.get("client_artifacts", [])}
    physical_hash_failures = [
        path.name
        for path in [xlsx_path, analytical_path, tz_path]
        if path.name not in physical_records
        or physical_records[path.name].get("sha256") != sha256(path)
        or physical_records[path.name].get("bytes") != path.stat().st_size
    ]
    check(
        "final_byte_physical_qa",
        physical_report.get("status") == "PASS"
        and physical_report.get("failure_count") == 0
        and not physical_hash_failures
        and physical_report.get("xlsx_visual_inspection", {}).get("inspected_sheets") == 13
        and physical_records.get(ANALYTICAL_NAME, {}).get("inspected_pages") == 22
        and physical_records.get(TZ_NAME, {}).get("inspected_pages") == 71
        and physical_report.get("text_and_package_checks", {}).get("internal_identifier_or_process_token_hits") == 0,
        {"status": physical_report.get("status"), "hash_failures": physical_hash_failures, "xlsx_sheets": physical_report.get("xlsx_visual_inspection", {}).get("inspected_sheets"), "pdf_pages": [physical_records.get(ANALYTICAL_NAME, {}).get("inspected_pages"), physical_records.get(TZ_NAME, {}).get("inspected_pages")]},
    )

    recipient_text = RECIPIENT_REPORT.read_text(encoding="utf-8")
    recipient_hashes_present = all(sha256(path) in recipient_text for path in [xlsx_path, analytical_path, tz_path])
    check(
        "product_recipient_qa",
        "Итог: **PASS**" in recipient_text
        and recipient_text.count("| PASS |") >= 6
        and recipient_hashes_present
        and "только по трём клиентским файлам" in recipient_text,
        {"pass_rows": recipient_text.count("| PASS |"), "final_hashes_present": recipient_hashes_present},
    )

    return finalize(
        {
            "semantic_universe": len(foundation),
            "working_phrases": len(phrases),
            "cluster_tasks": len(clusters),
            "target_pages": len(registry),
            "page_specs": len(specs),
            "change_tickets": len(delta),
            "ready_change_tickets": len(ready),
            "keep_pages": len(keep_keys),
            "provider_calls": manifest.get("provider_calls"),
            "client_files": len(client_files),
            "xlsx_sheets": len(workbook["sheets"]),
            "pdf_pages": analytical_pages + tz_pages,
        }
    )


def finalize(counts: dict[str, object] | None = None) -> int:
    failed = [name for name, result in checks.items() if result["status"] == "FAIL"]
    report = {
        "schema": "MK02_TARGET_FIRST_CORRECTIVE_MACHINE_QA_V1",
        "date": DATE,
        "status": "PASS" if not failed else "FAIL",
        "validator_is_fail_capable": True,
        "checks_total": len(checks),
        "checks_passed": len(checks) - len(failed),
        "checks_failed": len(failed),
        "failed_checks": failed,
        "counts": counts or {},
        "checks": checks,
    }
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks_total": report["checks_total"], "failed_checks": failed, "counts": report["counts"]}, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        check("validator_runtime", False, {"error": type(error).__name__, "message": str(error)})
        sys.exit(finalize())
