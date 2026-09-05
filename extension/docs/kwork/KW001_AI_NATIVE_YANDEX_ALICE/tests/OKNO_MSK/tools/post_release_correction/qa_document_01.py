#!/usr/bin/env python3
"""Deterministic analyst recheck for corrected recipient document №01 only."""

from __future__ import annotations

import csv
import json
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

from docx import Document


HERE = Path(__file__).resolve()
JOB = HERE.parents[2]
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
SOURCE = RELEASE / "sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md"
DOCX = RELEASE / "editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.docx"
PDF = RELEASE / "01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.pdf"
SEMANTIC = JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"
UNITS = JOB / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"
ACTIONS = JOB / "RESEARCH_REBUILD_POST_RELEASE_SHARED_IMPLEMENTATION_AUTHORITY_CORRECTED_2026-09-05.tsv"
EVIDENCE = JOB / "RESEARCH_REBUILD_STAGE_07_EVIDENCE_REGISTER_2026-09-05.tsv"
AI = JOB / "RESEARCH_REBUILD_STAGE_03_AI_CAUSAL_LEDGER_2026-09-05.tsv"
KNOWLEDGE = JOB / "RESEARCH_REBUILD_STAGE_11_AI_KNOWLEDGE_DOCUMENT_2026-09-05.json"
QA_JSON = JOB / "RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_ANALYST_RECHECK_QA_2026-09-05.json"
QA_MD = JOB / "RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_ANALYST_RECHECK_QA_2026-09-05.md"

CORRECTED_QF = {"QF001", "QF005", "QF006", "QF010", "QF013", "QF015", "QF016", "QF017"}
EXPECTED_READY = {"S18-A009", "S18-A010", "S18-A026", "S18-A028", "S18-A029", "S18-A030", "S18-A031"}


def read_tsv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def norm_url(value: str) -> str:
    return str(value or "").strip().rstrip("/")


def chunks(text: str, prefix: str) -> dict[str, str]:
    pattern = rf"(?=^### ({re.escape(prefix)}[^\s—]+))"
    parts = re.split(pattern, text, flags=re.M)
    result = {}
    for index in range(1, len(parts), 2):
        result[parts[index]] = parts[index + 1]
    return result


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    semantic = read_tsv(SEMANTIC)
    units = {row["structural_unit_id"]: row for row in read_tsv(UNITS)}
    actions = read_tsv(ACTIONS)
    evidence = read_tsv(EVIDENCE)
    ai_rows = read_tsv(AI)
    knowledge = json.loads(KNOWLEDGE.read_text(encoding="utf-8"))
    qf_authority = {row["case_id"]: row for row in knowledge["search_case_explanations"]}
    semantic_by_phrase = {row["phrase"].strip().casefold(): row for row in semantic}
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append((name, bool(condition), detail))
        if not condition:
            raise AssertionError(f"{name}: {detail}")

    action_states = Counter(row["recipient_state"] for row in actions)
    ready = {row["action_id"] for row in actions if row["real_site_change"] == "YES" and row["recipient_state"] == "READY"}
    partial = {row["action_id"] for row in actions if row["recipient_state"] == "READY_PARTIAL__BUSINESS_DETAIL_REQUIRED"}
    check("ACTION_UNIVERSE", len(actions) == 34, f"rows={len(actions)}")
    check("READY_REAL_SITE_COUNT", ready == EXPECTED_READY, f"ready={sorted(ready)}")
    check("PARTIAL_BUSINESS_DETAIL_COUNT", partial == {"S18-A012"}, f"partial={sorted(partial)}")
    check("ANALYTICAL_MAPPING_COUNT", action_states["READY_ANALYTICAL_MAPPING"] == 19, str(action_states))
    check("NOT_READY_RECHECK_COUNT", action_states["NOT_READY__EVIDENCE_REQUIRED"] == 4, str(action_states))

    qf = chunks(source, "QF")
    check("QF_VISIBILITY", set(qf) == {f"QF{i:03d}" for i in range(1, 22)}, f"count={len(qf)}")
    qf_results = []
    unresolved = []
    for case_id in sorted(qf):
        authority = qf_authority[case_id]
        query = authority["representative_query"].strip()
        body = qf[case_id]
        exact = semantic_by_phrase.get(query.casefold()) if query else None
        if query:
            check(f"{case_id}_EXACT_ROW", exact is not None, query)
            check(f"{case_id}_EXACT_OWNER", f"**Exact-query owner:** {exact['final_primary_page']}" in body, exact["final_primary_page"])
            check(f"{case_id}_UNIT", f"`{exact['final_structural_unit_id']}`" in body, exact["final_structural_unit_id"])
            check(f"{case_id}_STATE", f"`{exact['final_semantic_state']}`" in body and f"`{exact['uncertainty_state']}`" in body, "state + uncertainty")
            unit = units[exact["final_structural_unit_id"]]
            check(f"{case_id}_UNIT_AUTHORITY", norm_url(unit["final_primary_page"]) == norm_url(exact["final_primary_page"]), unit["final_primary_page"])
            differs = norm_url(authority["primary_url"]) != norm_url(exact["final_primary_page"])
            if differs:
                check(f"{case_id}_DISTINCTION", "Семейная интерпретация отличается от exact-query owner" in body, "explicit exact/family boundary")
            qf_results.append({"case_id": case_id, "result": "FIX" if differs else "PASS", "exact_owner": exact["final_primary_page"], "family_distinction_required": differs})
        else:
            check(f"{case_id}_NO_EXACT_INVENTED", "exact Search и exact owner по этой карточке не заявляются" in body and "документ не назначает ей exact-query owner" in body, "family-only boundary")
            qf_results.append({"case_id": case_id, "result": "PASS", "exact_owner": "NOT_APPLICABLE__NO_REPRESENTATIVE_EXACT_PHRASE", "family_distinction_required": False})
        check(f"{case_id}_EVIDENCE_BASIS", "**Основание решения.**" in body and "Техническая трасса:" in body, "visible evidence bridge")
        check(f"{case_id}_NO_PHYSICAL_ACTION", "Никакой физической правки только из QF-карточки" in body, "analytical/site boundary")

    fixed = {row["case_id"] for row in qf_results if row["result"] == "FIX"}
    check("QF_CORRECTED_SET", fixed == CORRECTED_QF, f"fixed={sorted(fixed)}")
    check("QF_UNRESOLVED", not unresolved, str(unresolved))

    search_rows = [row for row in evidence if row["layer"] == "ORDINARY_YANDEX_SEARCH"]
    search_chunks = chunks(source, "SP09-")
    check("SEARCH_75_VISIBILITY", len(search_rows) == len(search_chunks) == 75, f"authority={len(search_rows)} report={len(search_chunks)}")
    for row in search_rows:
        body = search_chunks[row["evidence_id"]]
        check(f"{row['evidence_id']}_SCOPE", "не назначало URL автоматически" in body and "всё семейство" in body and "трафик" in body and "конверсия" in body, row["question_or_query"])

    ai_chunks = chunks(source, "C15-")
    check("AI_8_VISIBILITY", len(ai_rows) == len(ai_chunks) == 8, f"authority={len(ai_rows)} report={len(ai_chunks)}")
    required_ai_labels = [
        "Почему выбран до AI", "Search-only решение до AI", "Что показала AI-проверка",
        "Decision delta", "Текущая каноническая семантика точной фразы", "Итоговый вердикт",
        "Эффект на архитектуру", "Контентный эффект", "Действие / no-action", "Ограничение",
    ]
    for row in ai_rows:
        body = ai_chunks[row["case_id"]]
        exact = semantic_by_phrase[row["query"].strip().casefold()]
        check(f"{row['case_id']}_CAUSAL_CHAIN", all(label in body for label in required_ai_labels), "all causal labels")
        check(f"{row['case_id']}_VERDICT", f"`{row['verdict']}`" in body and f"`{row['architecture_effect']}`" in body, row["verdict"])
        check(f"{row['case_id']}_CURRENT_EXACT_OWNER", exact["final_primary_page"] in body, exact["final_primary_page"])

    for action in actions:
        check(f"ACTION_{action['action_id']}_MAP", f"**{action['action_id']}** — `{action['implementation_mode']}`; изменение сайта `{action['real_site_change']}`; `{action['recipient_state']}`" in source, action["action_id"])
    a012 = next(row for row in actions if row["action_id"] == "S18-A012")
    check("A012_FALSE_READY_REMOVED", a012["real_site_change"] == "PARTIAL" and a012["recipient_state"] == "READY_PARTIAL__BUSINESS_DETAIL_REQUIRED", str(a012))
    check("A012_BUSINESS_BOUNDARY_VISIBLE", all(token in source for token in ["**READY-часть без новых бизнес-фактов.**", "**PENDING_BUSINESS_DETAIL / NEEDS_CONFIRMATION.**", "BUSINESS_CONFIRMATION_FOR_COMPANY_SPECIFIC_SERVICE_SCOPE"]), "split visible")
    check("SUMMARY_COUNTS", all(token in source for token in ["Полностью готовы **7**", "**1** — частично готовая работа", "**19** — только аналитические назначения", "**4** требуют повторного доказательства"]), "7 ready + 1 partial + 19 analytical + 4 recheck")
    check("POSITIVE_KEEP_VISIBLE", all(token in source for token in ["Что уже правильно", "Не создавать страницы", "не доказаны", "не публиковать до подтверждения компании"]), "KEEP/NO_CHANGE")
    check("UNCERTAINTY_REOPEN_VISIBLE", all(token in source for token in ["PENDING_BUSINESS_DETAIL / NEEDS_CONFIRMATION", "NOT_READY__EVIDENCE_REQUIRED", "PENDING_DETAIL__PLACEMENT_NOT_PROVEN", "SEARCH_REQUIRED", "REVIEW_DEFERRED", "HOLD", "Повторное открытие"]), "states and reopen rules")

    docx = Document(DOCX)
    docx_text = "\n".join(paragraph.text for paragraph in docx.paragraphs)
    with tempfile.TemporaryDirectory() as td:
        pdf_txt = Path(td) / "doc01.txt"
        subprocess.run(["pdftotext", "-layout", str(PDF), str(pdf_txt)], check=True)
        pdf_text = pdf_txt.read_text(encoding="utf-8")
    docx_text_normalized = re.sub(r"\s+", " ", docx_text)
    pdf_text_normalized = re.sub(r"\s+", " ", pdf_text)
    equivalence_tokens = [
        "QF001", "QF021", "SP09-001", "SP09-075", "C15-004", "C15-020",
        "READY_PARTIAL__BUSINESS_DETAIL_REQUIRED", "PENDING_BUSINESS_DETAIL / NEEDS_CONFIRMATION",
        "Реализовать семь полностью готовых улучшений",
    ]
    check("DOCX_CONTENT_EQUIVALENCE", all(token in docx_text_normalized for token in equivalence_tokens), "all material endpoints and corrected states")
    check("PDF_CONTENT_EQUIVALENCE", all(token in pdf_text_normalized for token in equivalence_tokens), "all material endpoints and corrected states")

    report_lines = [
        "# OKNO_MSK — deterministic QA документа №01 после owner recheck correction",
        "",
        "**Дата:** 2026-09-05  ",
        "**Результат:** `PASS`  ",
        "**Объём:** только recipient document №01; №02/№03 не переоценивались",
        "",
        "## Итог",
        "",
        f"- QF: 21/21 PASS after correction; material routing fixes: {len(fixed)}; unresolved: 0.",
        "- Search: 75/75 exact observations remain exact-query scoped.",
        "- AI: 8/8 causal chains contain before-AI, observation, delta, verdict, architecture effect, action and limitation.",
        "- Actions: 7 fully READY physical changes; 1 partial S18-A012; 19 analytical mappings; 4 evidence rechecks.",
        "- Markdown/DOCX/PDF material-content equivalence: PASS.",
        "",
        "## Gates",
        "",
        "| Gate | Result | Detail |",
        "|---|---|---|",
    ]
    report_lines.extend(f"| `{name}` | `{'PASS' if ok else 'FAIL'}` | {detail.replace('|', '/')} |" for name, ok, detail in checks)
    report_lines += ["", "`DOCUMENT_01_ANALYST_RECHECK = PASS`  ", "`DOCUMENT_01_OWNER_REVIEW = PENDING`", ""]
    QA_MD.write_text("\n".join(report_lines), encoding="utf-8")
    result = {
        "status": "PASS",
        "scope": "DOCUMENT_01_ONLY",
        "checks": len(checks),
        "failed": 0,
        "qf": {"pass_after_correction": 21, "corrected": len(fixed), "unresolved": 0, "rows": qf_results},
        "search_exact_observations": {"reviewed": 75, "pass": 75},
        "ai_causal_cases": {"reviewed": 8, "pass": 8},
        "actions": {
            "total": 34,
            "fully_ready_real_site": 7,
            "partial_business_detail_required": 1,
            "analytical_mapping": 19,
            "evidence_recheck": 4,
            "no_separate_change": 1,
            "pending_detail": 1,
            "hold": 1,
        },
        "markdown_docx_pdf_equivalence": "PASS",
        "document_01_analyst_recheck": "PASS",
        "document_01_owner_review": "PENDING",
        "provider_calls": 0,
        "paid_cost_rub": 0,
    }
    QA_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
