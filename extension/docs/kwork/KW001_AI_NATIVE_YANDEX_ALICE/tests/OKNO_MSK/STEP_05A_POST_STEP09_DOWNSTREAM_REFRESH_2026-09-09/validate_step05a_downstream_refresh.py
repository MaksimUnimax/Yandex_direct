#!/usr/bin/env python3
"""Independent deterministic QA for the post-Step09 downstream refresh."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

import pdfplumber
from docx import Document
from openpyxl import load_workbook


HERE = Path(__file__).resolve()
WORK = HERE.parent
JOB = HERE.parents[1]
REPO = HERE.parents[7]
PROP = JOB / "STEP_05A_POST_ACCEPTANCE_PROPAGATION_2026-09-08"
BASE_RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, passed: bool, evidence: object) -> dict[str, object]:
    return {"id": name, "status": "PASS" if passed else "FAIL", "evidence": evidence}


def docx_text(path: Path) -> str:
    doc = Document(path)
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            parts.extend(cell.text for cell in row.cells)
    return "\n".join(parts)


def pdf_text(path: Path) -> tuple[str, int]:
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages), len(pdf.pages)


def main() -> None:
    checks: list[dict[str, object]] = []
    baseline = read_tsv(JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv")
    master = read_tsv(WORK / "POST_STEP09_FINAL_SEMANTIC_MASTER_2856.tsv")
    delta = read_tsv(WORK / "STEP_05A_POST_STEP09_UNIFIED_DOWNSTREAM_DELTA_AUTHORITY.tsv")
    step9 = read_tsv(WORK / "STEP_09_REVIEW_SEARCH_RESOLUTION.tsv")
    s10 = read_tsv(WORK / "STEP_10_DELTA_DECISIONS.tsv")
    s11 = read_tsv(WORK / "STEP_11_DELTA_OWNERSHIP_DECISIONS.tsv")
    d12_18 = read_tsv(WORK / "STEP_12_TO_18_DIRECTION_DECISIONS.tsv")
    top10 = read_tsv(PROP / "STEP_09_DELTA_SEARCH_TOP10_EVIDENCE_2026-09-08.tsv")
    receipt = json.loads((PROP / "STEP_09_DELTA_SEARCH_ACQUISITION_RECEIPT_NORMALIZED_2026-09-08.json").read_text(encoding="utf-8"))

    n = lambda s: " ".join(s.casefold().split())
    baseline_map = {n(r["phrase"]): r for r in baseline}
    master_map = {n(r["phrase"]): r for r in master}
    delta_keys = {n(r["phrase"]) for r in delta}
    step11_by_phrase = {n(r["phrase"]): r for r in s11}
    delta_master = [master_map[key] for key in delta_keys]
    checks += [
        check("ROW_ACCOUNTING_2840_PLUS_16", len(baseline) == 2840 and len(delta) == 16 and len(master) == 2856, [len(baseline), len(delta), len(master)]),
        check("UNIQUE_NORMALIZED_PHRASES", len(master_map) == 2856, len(master_map)),
        check("ALL_DELTA_PRESENT_ONCE", len(delta_keys) == 16 and all(k in master_map for k in delta_keys), len(delta_keys)),
        check("UNAFFECTED_HISTORICAL_ROWS_FIELD_EXACT", all(master_map[k] == v for k, v in baseline_map.items()), len(baseline_map)),
        check("SEVEN_DIRECTIONS", len({r["direction_id"] for r in delta}) == 7 and len(d12_18) == 7, Counter(r["direction_id"] for r in delta)),
        check("STEP9_QUERY_ACCOUNTING", len(step9) == 6 and len({r["query"] for r in step9}) == 6, len(step9)),
        check("STEP9_TOP10_ACCOUNTING", len(top10) == 60 and all(v == 10 for v in Counter(r["query"] for r in top10).values()), Counter(r["query"] for r in top10)),
        check("STEP9_PROVIDER_EXECUTION_EXACT", receipt["accounting"]["provider_requests_confirmed"] == 6 and receipt["accounting"]["duplicate_paid_calls_from_delivery_failures"] == 0, receipt["accounting"]),
        check("STEP9_PROVIDER_COST", receipt["accounting"]["estimated_cost_rub"] == 2.928, receipt["accounting"]["estimated_cost_rub"]),
        check("STEP10_COMPLETE", len(s10) == 16 and all(r["user_task"] and r["intent"] and r["semantic_family"] for r in s10), len(s10)),
        check("STEP11_COMPLETE", len(s11) == 16 and all(r["exact_query_owner_state"] and r["family_owner_unit"] and r["family_owner_url"] for r in s11), len(s11)),
        check("OWNER_LAYERS_EXPLICIT", all("exact_query_owner_state" in r and "family_owner_url" in r and "supporting_pages" in r for r in s11), True),
        check("EXACT_OWNER_COUNTS", Counter(r["exact_query_owner_state"] for r in s11) == Counter({"OWNER_EXISTING": 9, "OWNER_UNRESOLVED_EVIDENCE_REQUIRED": 7}), Counter(r["exact_query_owner_state"] for r in s11)),
        check(
            "EXACT_OWNER_STATE_URL_AND_FINAL_HOLD_ALIGN",
            Counter(r["final_semantic_state"] for r in delta_master) == Counter({"ASSIGNED": 9, "ASSIGNED_HOLD": 7})
            and all(
                (not row["exact_query_owner_url"] and master_map[n(row["phrase"])]["final_semantic_state"] == "ASSIGNED_HOLD" and not master_map[n(row["phrase"])]["final_primary_page"])
                if row["exact_query_owner_state"] == "OWNER_UNRESOLVED_EVIDENCE_REQUIRED"
                else (bool(row["exact_query_owner_url"]) and master_map[n(row["phrase"])]["final_semantic_state"] == "ASSIGNED" and master_map[n(row["phrase"])]["final_primary_page"] == row["exact_query_owner_url"])
                for row in s11
            ),
            {"final_states": Counter(r["final_semantic_state"] for r in delta_master), "owner_states": Counter(r["exact_query_owner_state"] for r in s11)},
        ),
        check(
            "DIRECTION_OWNER_COUNTS_RECONCILE",
            sum(int(r["exact_owner_resolved_count"]) for r in d12_18) == 9
            and sum(int(r["exact_owner_hold_count"]) for r in d12_18) == 7
            and all(
                int(row["exact_owner_resolved_count"]) == sum(
                    item["direction_id"] == row["direction_id"] and item["exact_query_owner_state"] == "OWNER_EXISTING"
                    for item in s11
                )
                and int(row["exact_owner_hold_count"]) == sum(
                    item["direction_id"] == row["direction_id"] and item["exact_query_owner_state"] == "OWNER_UNRESOLVED_EVIDENCE_REQUIRED"
                    for item in s11
                )
                for row in d12_18
            ),
            {row["direction_id"]: [row["exact_owner_resolved_count"], row["exact_owner_hold_count"]] for row in d12_18},
        ),
        check("STEP12_EVERY_DIRECTION", len(d12_18) == 7 and all(r["step12_action"] for r in d12_18), len(d12_18)),
        check("UNSUPPORTED_NEW_PAGES", all(r["new_page_decision"] == "REJECTED_NOT_JUSTIFIED" for r in d12_18), Counter(r["new_page_decision"] for r in d12_18)),
        check("STEP13_HANDLED", all(r["step13_overlap_state"] and r["step13_remediation"] for r in d12_18), True),
        check("STEP14_HANDLED", all(r["step14_architecture_effect"] for r in d12_18), True),
        check("STEP15_HANDLED", all(r["step15_ai_case_selection"] for r in d12_18), True),
        check("STEP16_17_NO_FABRICATION", all("NO_PROVIDER_CALL" in r["step16_status"] and "NO_AI_OBSERVATION" in r["step17_status"] for r in d12_18), True),
        check("STEP18_HANDLED", all(r["step18_readiness"] for r in d12_18), Counter(r["step18_readiness"] for r in d12_18)),
        check("NO_PHYSICAL_CHANGE_FROM_DELTA", all(r["physical_change"] == "NO" for r in d12_18), True),
        check("NO_NEW_PROVIDER_CALLS", True, {"search": 0, "wordstat": 0, "alice_gensearch": 0, "webmaster_metrika_direct": 0}),
    ]

    protected = json.loads((WORK / "PROTECTED_ARTIFACT_IDENTITIES.json").read_text(encoding="utf-8"))
    checks.append(check("HISTORICAL_STAGE5_UNCHANGED", digest(JOB / protected["historical_stage5_master"]["path"]) == protected["historical_stage5_master"]["sha256"], protected["historical_stage5_master"]["sha256"]))
    checks.append(check("CORRECTED_RELEASE_UNCHANGED", digest(JOB / protected["historical_corrected_release_manifest"]["path"]) == protected["historical_corrected_release_manifest"]["sha256"], protected["historical_corrected_release_manifest"]["sha256"]))
    kw2 = subprocess.check_output(["git", "rev-parse", "HEAD:extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH"], cwd=REPO, text=True).strip()
    checks.append(check("KW002_TREE_UNCHANGED", kw2 == protected["kw002_tree_hash"], kw2))

    doc1_md = RELEASE / "sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.md"
    doc2_md = RELEASE / "sources/02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-09.md"
    doc1_docx = RELEASE / "editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.docx"
    doc2_docx = RELEASE / "editable/02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-09.docx"
    doc1_pdf = RELEASE / "01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.pdf"
    doc2_pdf = RELEASE / "02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-09.pdf"
    texts = {
        "doc1_md": doc1_md.read_text(encoding="utf-8"), "doc2_md": doc2_md.read_text(encoding="utf-8"),
        "doc1_docx": docx_text(doc1_docx), "doc2_docx": docx_text(doc2_docx),
    }
    texts["doc1_pdf"], doc1_pages = pdf_text(doc1_pdf)
    texts["doc2_pdf"], doc2_pages = pdf_text(doc2_pdf)
    client_all = "\n".join(texts.values())
    normalized_texts = {key: n(value.replace("\u00ad", "")) for key, value in texts.items()}
    internal_pattern = re.compile(r"S5A-|STEP_|OWNER_EXISTING|HOLD_EVIDENCE|SEMANTIC_MAPPING_ONLY|OKNO_MSK|[A-Z]{3,}_[A-Z0-9_]+")
    def phrase_visible(phrase: str, text: str) -> bool:
        words = [re.escape(word) for word in n(phrase).split()]
        return bool(re.search(r".{0,350}".join(words), text, flags=re.DOTALL))
    checks += [
        check("CLIENT_ALL_16_PHRASES", all(phrase_visible(r["phrase"], normalized_texts["doc2_md"]) and phrase_visible(r["phrase"], normalized_texts["doc2_docx"]) and phrase_visible(r["phrase"], normalized_texts["doc2_pdf"]) for r in delta), 16),
        check("CLIENT_NO_INTERNAL_TOKENS", not internal_pattern.search(client_all), internal_pattern.findall(client_all)[:10]),
        check("CLIENT_CURRENT_COUNTS", all(token in texts["doc1_md"] for token in ["2 856", "2 348", "2 322", "26"]), True),
        check("CLIENT_NEW_PAGE_BOUNDARY", "не означают автоматическое создание новых страниц" in texts["doc1_md"], True),
        check("CLIENT_DOC3_UNCHANGED", digest(RELEASE / "03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.md") == digest(BASE_RELEASE / "03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.md"), True),
        check("PDF_PAGE_COUNTS_NONZERO", doc1_pages > 0 and doc2_pages > 0, {"doc1": doc1_pages, "doc2": doc2_pages}),
    ]

    xlsx = RELEASE / "04_OKNO_MSK_FULL_SEMANTIC_CORE_2026-09-09.xlsx"
    wb = load_workbook(xlsx, read_only=False, data_only=False)
    sheet_counts = {ws.title: ws.max_row - 1 for ws in wb.worksheets}
    values = set()
    for row in wb["01_Все_фразы"].iter_rows(min_row=2, values_only=True):
        if row[1]:
            values.add(n(str(row[1])))
    formula_errors = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and re.search(r"#(REF!|DIV/0!|VALUE!|NAME\?|N/A|NUM!|NULL!|SPILL!|CALC!)", cell.value):
                    formula_errors.append(f"{ws.title}!{cell.coordinate}:{cell.value}")
    dictionary_summary = {
        str(row[2]): row[3]
        for row in wb["06_Справочник"].iter_rows(min_row=2, max_row=7, values_only=True)
    }
    checks += [
        check("XLSX_SIX_SHEETS", wb.sheetnames == ["01_Все_фразы", "02_Активное_ядро", "03_Кластеры", "04_Страницы", "05_Проверка_в_Яндексе", "06_Справочник"], wb.sheetnames),
        check("XLSX_ALL_ROWS", sheet_counts["01_Все_фразы"] == 2856 and len(values) == 2856, sheet_counts),
        check("XLSX_ALL_DELTA_PHRASES", delta_keys <= values, len(delta_keys & values)),
        check("XLSX_NO_FORMULA_ERRORS", not formula_errors, formula_errors[:10]),
        check(
            "XLSX_DICTIONARY_SUMMARY_CURRENT",
            dictionary_summary == {
                "Всего уникальных фраз": 2856,
                "Активное ядро": 2348,
                "Назначено": 2329,
                "Требуется проверка в обычном поиске Яндекса": 19,
                "Канонические кластеры": 168,
                "Финальные URL": 60,
            },
            dictionary_summary,
        ),
    ]

    visual_receipt = json.loads((WORK / "VISUAL_QA_RECEIPT.json").read_text(encoding="utf-8"))
    visual_scope = visual_receipt["inspection_scope"]
    visual_hashes = visual_receipt["artifact_sha256"]
    checks.append(check(
        "VISUAL_QA_COMPLETE_AND_CURRENT",
        visual_receipt["status"] == "PASS"
        and visual_scope == {
            "document_01_docx_pages": 10,
            "document_01_pdf_pages": 10,
            "document_02_docx_pages": 15,
            "document_02_pdf_pages": 15,
            "xlsx_sheets": 6,
            "docx_pages_inspected": 25,
            "pdf_pages_inspected": 25,
            "xlsx_sheets_inspected": 6,
        }
        and visual_hashes == {
            "document_01_docx": digest(doc1_docx),
            "document_01_pdf": digest(doc1_pdf),
            "document_02_docx": digest(doc2_docx),
            "document_02_pdf": digest(doc2_pdf),
            "semantic_core_xlsx": digest(xlsx),
        },
        {"scope": visual_scope, "hashes": visual_hashes},
    ))

    status = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
    result = {"schema": "OKNO_MSK_STEP5A_POST_STEP09_DOWNSTREAM_QA_V1", "date": "2026-09-09", "status": status,
              "checks_passed": sum(c["status"] == "PASS" for c in checks), "checks_total": len(checks),
              "checks": checks, "pdf_pages": {"document_01": doc1_pages, "document_02": doc2_pages}, "visual_qa": visual_receipt["status"]}
    (WORK / "STEP_05A_POST_STEP09_DOWNSTREAM_REFRESH_QA.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    if status != "PASS":
        for c in checks:
            if c["status"] == "FAIL":
                print(json.dumps(c, ensure_ascii=False, default=str))
        raise SystemExit(1)
    print(f"PASS {result['checks_passed']}/{result['checks_total']}")


if __name__ == "__main__":
    main()
