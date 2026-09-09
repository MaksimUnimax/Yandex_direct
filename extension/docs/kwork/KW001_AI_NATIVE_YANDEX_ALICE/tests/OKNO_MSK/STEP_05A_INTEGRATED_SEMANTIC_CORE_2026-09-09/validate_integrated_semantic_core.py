#!/usr/bin/env python3
"""Independent deterministic QA for the integrated OKNO_MSK semantic core."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve()
WORK = HERE.parent
JOB = HERE.parents[1]
REPO = HERE.parents[7]
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09"
HIST_RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
KW002 = "extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH"
BASE = JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"
MASTER = WORK / "FINAL_SEMANTIC_MASTER_STEP05A_INTEGRATED_2026-09-09.tsv"
ACTIVE = WORK / "FINAL_ACTIVE_SEMANTIC_CORE_STEP05A_INTEGRATED_2026-09-09.tsv"
UNITS = WORK / "FINAL_PAGE_STRUCTURAL_AUTHORITY_STEP05A_INTEGRATED_2026-09-09.tsv"
SUMMARY = WORK / "FINAL_SEMANTIC_CORE_STEP05A_INTEGRATED_SUMMARY_2026-09-09.json"
PROTECTED = WORK / "PROTECTED_ARTIFACT_IDENTITIES.json"
VISUAL = WORK / "VISUAL_QA_RECEIPT.json"
RUNTIME = WORK / "XLSX_BUILD_RUNTIME.json"
XLSX = RELEASE / "04_OKNO_MSK_FULL_SEMANTIC_CORE_2026-09-09.xlsx"
QA = WORK / "FINAL_SEMANTIC_CORE_STEP05A_INTEGRATED_QA_2026-09-09.json"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def norm(value: str) -> str:
    return " ".join(value.casefold().split())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_object(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=REPO, text=True).strip()


def check(name: str, passed: bool, evidence: object) -> dict[str, object]:
    return {"id": name, "status": "PASS" if passed else "FAIL", "evidence": evidence}


def xlsx_facts(path: Path) -> dict[str, object]:
    ns_main = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
    with zipfile.ZipFile(path) as zf:
        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        sheets = [(s.attrib["name"], s.attrib.get("state", "visible"), s.attrib[f"{{{ns_main['r']}}}id"]) for s in wb.find("m:sheets", ns_main)]
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rel_map = {r.attrib["Id"]: r.attrib["Target"].lstrip("/") for r in rels}
        row_counts, frozen, merges = {}, {}, {}
        all_text = []
        for name, _, rid in sheets:
            target = rel_map[rid]
            if not target.startswith("xl/"):
                target = "xl/" + target
            root = ET.fromstring(zf.read(target))
            rows = root.findall(".//m:sheetData/m:row", ns_main)
            row_counts[name] = len(rows)
            frozen[name] = root.find(".//m:pane", ns_main) is not None
            merges[name] = len(root.findall(".//m:mergeCells/m:mergeCell", ns_main))
            all_text.extend(t.text or "" for t in root.findall(".//m:t", ns_main))
        formula_cells = 0
        for file in zf.namelist():
            if file.startswith("xl/worksheets/sheet") and file.endswith(".xml"):
                formula_cells += zf.read(file).count(b"<f")
        table_count = sum(1 for f in zf.namelist() if f.startswith("xl/tables/table") and f.endswith(".xml"))
        return {
            "sheets": [s[0] for s in sheets], "states": {s[0]: s[1] for s in sheets},
            "rows": row_counts, "frozen": frozen, "merges": merges,
            "formula_cells": formula_cells, "table_count": table_count,
            "text": "\n".join(all_text),
        }


def main() -> None:
    base = read_tsv(BASE)
    master = read_tsv(MASTER)
    active = read_tsv(ACTIVE)
    units = read_tsv(UNITS)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    protected = json.loads(PROTECTED.read_text(encoding="utf-8"))
    visual = json.loads(VISUAL.read_text(encoding="utf-8"))
    runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
    xfacts = xlsx_facts(XLSX)
    checks: list[dict[str, object]] = []

    base_fields = list(base[0])
    base_map = {norm(r["phrase"]): r for r in base}
    master_map = {r["normalized_phrase"]: r for r in master}
    active_map = {r["normalized_phrase"]: r for r in active}
    step5a = [r for r in master if r["acquisition_stage"] == "STEP_05A"]
    base_integrated = [r for r in master if r["acquisition_stage"] == "STEP_03_05_BASE"]
    unresolved = [r for r in active if r["exact_query_owner_state"] == "OWNER_UNRESOLVED_EVIDENCE_REQUIRED"]
    assigned = [r for r in active if r["exact_assignment_status"] == "ASSIGNED"]
    active_units = {r["structural_unit"] for r in active if r["structural_unit"]}
    duplicate_count = len(master) - len(master_map)
    positions = [i + 1 for i, r in enumerate(master) if r["acquisition_stage"] == "STEP_05A"]

    checks += [
        check("A_BASE_ROWS_REPRODUCE_HISTORICAL_SET", len(base_integrated) == 2840 and {r["normalized_phrase"] for r in base_integrated} == set(base_map) and all({k: master_map[key][k] for k in base_fields} == row for key, row in base_map.items()), len(base_integrated)),
        check("B_STEP5A_ACCEPTED_EXACTLY_16", len(step5a) == 16 and len({r["normalized_phrase"] for r in step5a}) == 16, len(step5a)),
        check("C_BASE_STEP5A_INTERSECTION_ZERO", not (set(base_map) & {r["normalized_phrase"] for r in step5a}), 0),
        check("D_UNION_2840_PLUS_16_EQUALS_2856", len(base) + len(step5a) == len(master) == 2856, [len(base), len(step5a), len(master)]),
        check("E_NO_DUPLICATE_NORMALIZED_PHRASES", duplicate_count == 0, duplicate_count),
        check("F_ALL_ROWS_HAVE_PROVENANCE", all(r["source_provenance"] and r["raw_evidence_locator"] and r["evidence_authority_locator"] for r in master), sum(bool(r["source_provenance"] and r["raw_evidence_locator"] and r["evidence_authority_locator"]) for r in master)),
        check("G_ACTIVE_ROWS_HAVE_SEMANTIC_STATE", all(r["semantic_state"] in {"ASSIGNED", "ASSIGNED_HOLD", "SEARCH_REQUIRED"} for r in active), Counter(r["semantic_state"] for r in active)),
        check("H_EXACT_ASSIGNMENTS_HAVE_AUTHORITY_TRAIL", all(r["evidence_authority_locator"] and (r["exact_primary_page"] or r["exact_query_owner_state"] != "OWNER_EXISTING") for r in active), True),
        check("I_OWNER_LAYERS_NOT_CONFLATED", all(r["exact_query_owner_state"] != "OWNER_UNRESOLVED_EVIDENCE_REQUIRED" or not r["exact_primary_page"] for r in active) and all(r["exact_query_owner_state"] != "NO_SUITABLE_EXISTING_PAGE" or not r["exact_primary_page"] for r in active), {"exact_field": "exact_primary_page", "family_field": "family_primary_page"}),
        check("J_UNRESOLVED_URLS_NOT_INVENTED", len(unresolved) == 26 and all(not r["exact_primary_page"] for r in unresolved), len(unresolved)),
        check("K_ACTIVE_ROWS_2348", len(active) == 2348, len(active)),
        check("L_EXACT_ASSIGNMENT_DECISIONS_2322", len(assigned) == 2322, len(assigned)),
        check("M_ACTIVE_UNRESOLVED_EXACT_OWNER_26", len(unresolved) == 26, len(unresolved)),
        check("N_DEMAND_GROUPS_168", len(active_units) == len(units) == 168, [len(active_units), len(units)]),
        check("O_ALL_16_STEP5A_PHRASES_PRESENT", len(step5a) == 16 and all(r["normalized_phrase"] in master_map for r in step5a), len(step5a)),
        check("P_STEP5A_PASSED_COMMON_DOWNSTREAM_MODEL", all(r["semantic_state"] in {"ASSIGNED", "ASSIGNED_HOLD"} and r["structural_unit"] and r["exact_assignment_status"] for r in step5a), Counter(r["semantic_state"] for r in step5a)),
        check("Q_NO_LATE_DELTA_APPENDIX", positions != list(range(2841, 2857)) and summary["step5a_is_late_append"] is False, positions),
        check("ACTIVE_CORE_FIELD_EXACT_SUBSET", len(active_map) == 2348 and all(active_map[k] == master_map[k] for k in active_map) and set(active_map) == {r["normalized_phrase"] for r in master if r["active_state"] == "YES"}, len(active_map)),
        check("STEP5A_LINEAGE_COMPLETE", all(r["competitor_page_evidence"] and r["competitor_candidate_seed"] and r["wordstat_lineage_request_id"] and r["wordstat_lineage_row_id"] and r["search_representative_query"] for r in step5a), 16),
        check("STEP5A_OWNER_SPLIT_9_7", Counter(r["exact_query_owner_state"] for r in step5a) == Counter({"OWNER_EXISTING": 9, "OWNER_UNRESOLVED_EVIDENCE_REQUIRED": 7}), Counter(r["exact_query_owner_state"] for r in step5a)),
        check("STEP5A_NO_NEW_PAGE_OR_PHYSICAL_CHANGE", all(r["new_page_decision"] == "NO_NEW_PAGE" and r["site_change"] == "NO" for r in step5a), True),
        check("SEARCH_EVIDENCE_BOUNDARY_PRESERVED", sum(r["search_evidence_status"] == "EXACT_QUERY_SEARCH_EVIDENCE_PRESERVED" for r in step5a) == 6, Counter(r["search_evidence_status"] for r in step5a)),
        check("AI_CHECKS_ONLY_WHERE_USED", sum(r["ai_evidence_status"] == "EXACT_QUERY_AI_CHECK_PRESERVED" for r in master) == 8, Counter(r["ai_evidence_status"] for r in master)),
    ]

    expected_sheets = ["Как пользоваться", "Итоговое ядро", "Группы спроса", "Страницы и назначение", "Не назначено точно", "Исключено и отложено", "Источники и происхождение"]
    forbidden_client = re.compile(r"дополнительные фразы|отдельное конкурентное ядро|дельта", re.I)
    checks += [
        check("XLSX_REOPENS_WITH_EXPECTED_SHEETS", runtime["status"] == "PASS" and xfacts["sheets"] == expected_sheets, xfacts["sheets"]),
        check("XLSX_ROWS_REPRODUCED_FROM_WORKBOOK", xfacts["rows"]["Итоговое ядро"] == 2857 and xfacts["rows"]["Группы спроса"] == 169 and xfacts["rows"]["Не назначено точно"] == 27 and xfacts["rows"]["Исключено и отложено"] == 509, xfacts["rows"]),
        check("XLSX_TABLES_AND_FILTERS_PRESENT", xfacts["table_count"] >= 6, xfacts["table_count"]),
        check("XLSX_FROZEN_HEADERS_PRESENT", all(xfacts["frozen"][name] for name in expected_sheets[1:]), xfacts["frozen"]),
        check("XLSX_NO_HIDDEN_SHEETS", all(v == "visible" for v in xfacts["states"].values()), xfacts["states"]),
        check("XLSX_NO_FORMULAS_OR_FORMULA_ERRORS", xfacts["formula_cells"] == 0 and runtime["formula_errors"] == 0, [xfacts["formula_cells"], runtime["formula_errors"]]),
        check("XLSX_NO_TABULAR_MERGES", all(xfacts["merges"][name] == 0 for name in expected_sheets[1:6]), xfacts["merges"]),
        check("XLSX_NO_CLIENT_DELTA_APPENDIX_LANGUAGE", not forbidden_client.search(xfacts["text"]), forbidden_client.findall(xfacts["text"])),
        check("XLSX_VISUAL_QA_7_OF_7", visual["status"] == "PASS" and visual["sheets_inspected"] == visual["sheets_total"] == 7 and visual["workbook_sha256"] == digest(XLSX), visual),
    ]

    urls = []
    for row in master:
        for field in ("exact_primary_page", "family_primary_page", "supporting_pages"):
            urls.extend([u.strip() for u in row[field].split(";") if u.strip()])
    malformed = [u for u in urls if not re.fullmatch(r"https://okno-msk\.ru/.*|https://okno-msk\.ru", u)]
    checks.append(check("URLS_WELL_FORMED", not malformed, malformed[:10]))

    checks += [
        check("R_HISTORICAL_CORRECTED_RELEASE_TREE_UNCHANGED", git_object(str(HIST_RELEASE.relative_to(REPO))) == protected["historical_corrected_release_tree"], protected["historical_corrected_release_tree"]),
        check("R_HISTORICAL_STAGE5_MASTER_UNCHANGED", git_object(str(BASE.relative_to(REPO))) == protected["historical_stage5_master_blob"], protected["historical_stage5_master_blob"]),
        check("S_KW002_WORKTREE_UNTOUCHED", not subprocess.check_output(["git", "status", "--porcelain", "--", KW002], cwd=REPO, text=True).strip(), protected["kw002_tree"]),
        check("T_PROVIDER_CALLS_ZERO", summary["provider_calls"] == protected["provider_calls"] == 0, 0),
    ]

    status = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    result = {
        "schema": "OKNO_MSK_FINAL_SEMANTIC_CORE_STEP05A_INTEGRATED_QA_V1",
        "date": "2026-09-09", "status": status,
        "checks_passed": sum(c["status"] == "PASS" for c in checks), "checks_total": len(checks),
        "totals": {"canonical": len(master), "active": len(active), "exact_assignment_decisions": len(assigned), "unresolved_exact_owner": len(unresolved), "demand_groups": len(active_units), "step5a": len(step5a), "duplicates": duplicate_count, "provider_calls": 0},
        "checks": checks,
    }
    QA.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    if status != "PASS":
        for item in checks:
            if item["status"] == "FAIL":
                print(json.dumps(item, ensure_ascii=False, default=str))
        raise SystemExit(1)
    print(f"PASS {result['checks_passed']}/{result['checks_total']}")


if __name__ == "__main__":
    main()
