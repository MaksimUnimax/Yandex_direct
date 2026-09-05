#!/usr/bin/env python3
"""Independent deterministic QA for corrected OKNO_MSK recipient artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve()
JOB = HERE.parents[2]
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
DOC1 = RELEASE / "sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md"
DOC2 = RELEASE / "sources/02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.md"
DOC3 = RELEASE / "03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.md"
AUTH = JOB / "RESEARCH_REBUILD_POST_RELEASE_SHARED_IMPLEMENTATION_AUTHORITY_CORRECTED_2026-09-05.tsv"
JSON_AUTH = JOB / "RESEARCH_REBUILD_STAGE_11_AI_KNOWLEDGE_DOCUMENT_2026-09-05.json"

EXPECTED_READY = {"S18-A009", "S18-A010", "S18-A012", "S18-A026", "S18-A028", "S18-A029", "S18-A030", "S18-A031"}
EXPECTED_ANALYTICAL = {"S18-A001", "S18-A002", "S18-A005", "S18-A006", "S18-A008", *{f"S18-A{i:03d}" for i in range(13, 26)}, "S18-A033"}
EXPECTED_RECHECK = {"S18-A003", "S18-A004", "S18-A007", "S18-A011"}


def read_tsv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def extract_workset(text: str) -> dict[str, tuple[str, str, str]]:
    result = {}
    chunks = re.split(r"(?=^### S18-A\d{3}\b)", text, flags=re.M)
    for c in chunks:
        m = re.match(r"### (S18-A\d{3})", c)
        if not m:
            continue
        aid = m.group(1)
        mode = re.search(r"\*\*Режим внедрения:\*\* `([^`]+)`", c)
        real = re.search(r"\*\*Физическое изменение сайта:\*\* `([^`]+)`", c)
        state = re.search(r"\*\*Состояние:\*\* `([^`]+)`", c)
        if mode and real and state:
            result[aid] = (mode.group(1), real.group(1), state.group(1))
    return result


def section_rows(text: str, start: str, end: str) -> int:
    s = text.index(start)
    e = text.index(end, s)
    # Rows and the header start with ``| ``; the Markdown separator starts
    # with ``|---`` and therefore is not part of this count.
    return sum(1 for line in text[s:e].splitlines() if line.startswith("| ")) - 1


def main() -> None:
    data = json.loads(JSON_AUTH.read_text(encoding="utf-8"))
    rows = read_tsv(AUTH)
    a = {r["action_id"]: r for r in rows}
    t1, t2, t3 = DOC1.read_text(encoding="utf-8"), DOC2.read_text(encoding="utf-8"), DOC3.read_text(encoding="utf-8")
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, condition: bool, detail: str):
        checks.append((name, bool(condition), detail))
        if not condition:
            raise AssertionError(f"{name}: {detail}")

    check("SHARED_ACTION_UNIVERSE", len(rows) == 34 and set(a) == {f"S18-A{i:03d}" for i in range(1, 35)}, f"rows={len(rows)}")
    check("READY_REAL_SITE_WORKSET", {x for x, r in a.items() if r["real_site_change"] == "YES" and r["recipient_state"] == "READY"} == EXPECTED_READY, str(EXPECTED_READY))
    check("ANALYTICAL_ONLY_WORKSET", {x for x, r in a.items() if r["recipient_state"] == "READY_ANALYTICAL_MAPPING"} == EXPECTED_ANALYTICAL, f"count={len(EXPECTED_ANALYTICAL)}")
    check("RECHECK_WORKSET", {x for x, r in a.items() if r["recipient_state"] == "NOT_READY__EVIDENCE_REQUIRED"} == EXPECTED_RECHECK, str(EXPECTED_RECHECK))
    check("LINK_BATCH_NOT_READY", a["S18-A032"]["recipient_state"] == "PENDING_DETAIL__PLACEMENT_NOT_PROVEN" and a["S18-A032"]["real_site_change"] == "UNRESOLVED", "A032")
    check("ROUTING_IS_NOT_SITE_CHANGE", a["S18-A033"]["implementation_mode"] == "SEMANTIC_MAPPING_ONLY" and a["S18-A033"]["real_site_change"] == "NO", "A033")
    check("HOLD_PRESERVED", a["S18-A034"]["recipient_state"] == "HOLD__EVIDENCE_REQUIRED" and a["S18-A034"]["real_site_change"] == "NO", "A034")

    for name, text in (("DOC01", t1), ("DOC02", t2), ("DOC03", t3)):
        check(f"{name}_ALL_34_ACTIONS", all(x in text for x in a), name)
    check("DOC01_SEARCH_EXACT_VISIBILITY", all(f"SP09-{i:03d}" in t1 for i in range(1, 76)), "75/75")
    check("DOC01_SEARCH_CASE_VISIBILITY", all(f"QF{i:03d}" in t1 for i in range(1, 22)), "21/21")
    check("DOC01_AI_CAUSAL_VISIBILITY", all(cid in t1 for cid in ["C15-004", "C15-006", "C15-007", "C15-010", "C15-013", "C15-018", "C15-019", "C15-020"]), "8/8")
    check("DOC01_UNCERTAINTY_EXPLANATION", all(x in t1 for x in ["SEARCH_REQUIRED — 19", "REVIEW_DEFERRED — 174", "HOLD — 20", "Пересечения — 3", "Внутренние ссылки — 15"]), "five material classes")
    check("DOC01_POSITIVE_FINDINGS", all(title in t1 for title in ["Текущая архитектура", "Связанные страницы", "Веранды", "Цены дверей"]), "positive universe")

    work2, work3 = extract_workset(t2), extract_workset(t3)
    expected_tuple = {x: (r["implementation_mode"], r["real_site_change"], r["recipient_state"]) for x, r in a.items()}
    check("DOC02_WORKSET_EQUALS_AUTHORITY", work2 == expected_tuple, f"rows={len(work2)}")
    check("DOC03_WORKSET_EQUALS_AUTHORITY", work3 == expected_tuple, f"rows={len(work3)}")
    check("DOC02_EQUALS_DOC03_CONFIRMED_WORKSET", work2 == work3, f"rows={len(work2)}")
    check("DOC02_READY_LINK_PRECISION", "PENDING_DETAIL__PLACEMENT_NOT_PROVEN" in t2 and t2.count("Почему не READY") == 15, "15 pending link cards")
    check("DOC02_ROUTE_PRECISION", t2.count("**Режим:** `SEMANTIC_MAPPING_ONLY`; **физическое изменение сайта:** `NO`.") == 46, "46 route cards")
    banned = ["Use the discovered", "Add standard/non-standard", "Strengthen existing", "Retain the current door", "Verify and if needed strengthen", "batch or non-phrase action"]
    check("DOC02_RUSSIAN_PROSE_NO_KNOWN_LEAKS", not any(x in t2 for x in banned), str([x for x in banned if x in t2]))

    numbered_03 = sorted(p.name for p in RELEASE.iterdir() if p.name.startswith("03"))
    check("DOC03_EXACTLY_ONE_PHYSICAL_FILE", numbered_03 == [DOC3.name], str(numbered_03))
    check("DOC03_IS_MARKDOWN", DOC3.suffix == ".md", DOC3.name)
    check("DOC03_SEMANTIC_UNIVERSE", section_rows(t3, "## 14. Полная семантическая вселенная", "## 15. Полный реестр остаточной неопределённости") == 2840, "2840 rows")
    check("DOC03_UNIT_UNIVERSE", section_rows(t3, "## 13. Полный канонический реестр", "## 14. Полная семантическая вселенная") == 168, "168 rows")
    check("DOC03_UNCERTAINTY_UNIVERSE", section_rows(t3, "## 15. Полный реестр остаточной неопределённости", "## 16. Как отвечать") == 221, "221 rows")
    check("DOC03_SEARCH_UNIVERSE", all(f"SP09-{i:03d}" in t3 for i in range(1, 76)) and all(f"QF{i:03d}" in t3 for i in range(1, 22)), "75 exact + 21 cases")
    check("DOC03_AI_UNIVERSE", all(cid in t3 for cid in ["C15-004", "C15-006", "C15-007", "C15-010", "C15-013", "C15-018", "C15-019", "C15-020"]), "8/8")
    check("DOC03_NO_PHYSICAL_ACCESS_CLAIM", "AI не утверждает, что изменило сайт" in t3 and "не предоставляет физический доступ к сайту" in t3, "explicit boundary")

    corrected = [r for r in data["semantic_master"] if r["correction_lineage"] != "NONE"]
    units = {u["structural_unit_id"]: u for u in data["canonical_units"]}
    field_pairs = [
        ("canonical_user_task", "user_task"), ("canonical_intent_type", "intent_type"),
        ("canonical_business_scope_state", "business_scope_state"), ("canonical_unit_page_role", "unit_page_role"),
        ("final_primary_page", "final_primary_page"), ("final_supporting_pages", "final_supporting_pages"),
        ("canonical_structural_action", "structural_action"),
    ]
    mismatches = []
    for r in corrected:
        u = units[r["final_structural_unit_id"]]
        for rf, uf in field_pairs:
            if r[rf] != u[uf]:
                mismatches.append((r["phrase"], rf, r[rf], u[uf]))
    check("SEMANTIC_69_ATOMIC_CORRECTION_ORACLE", len(corrected) == 69 and not mismatches, f"corrected={len(corrected)} mismatches={len(mismatches)}")

    # Strict clean-context/offline document walkthrough: copy only №03 and
    # verify that practical answers can be located without any companion.
    with tempfile.TemporaryDirectory() as td:
        only = Path(td) / DOC3.name
        only.write_bytes(DOC3.read_bytes())
        isolated = only.read_text(encoding="utf-8")
        questions = {
            "scope": ["Что было исследовано", "2 840", "обычный Яндекс"],
            "correct": ["Что уже правильно", "Не создавать страницы", "/verandy"],
            "why_a009": ["S18-A009", "Что означает доказательство", "французских окон"],
            "where_how_a010": ["S18-A010", "В блоке выбора/замера", "типовых и нетиповых"],
            "links": ["Пятнадцать связей", "PENDING_DETAIL__PLACEMENT_NOT_PROVEN", "точный source-блок"],
            "uncertainty": ["Полный реестр остаточной неопределённости", "SEARCH_REQUIRED", "HOLD__EVIDENCE_REQUIRED"],
            "search": ["Все 75 точных наблюдений", "SP09-075", "Только этот запрос"],
            "ai": ["AI: полная причинная цепочка", "C15-020", "INSUFFICIENT"],
            "acceptance": ["Приёмка", "Не сломать / не утверждать", "Как отвечать на практические вопросы"],
            "physical_boundary": ["AI не утверждает, что изменило сайт", "не предоставляет физический доступ к сайту"],
        }
        missing = {q: [needle for needle in needles if needle not in isolated] for q, needles in questions.items()}
        missing = {q: v for q, v in missing.items() if v}
        check("DOC03_OFFLINE_CLEAN_CONTEXT_WALKTHROUGH", not missing, f"questions={len(questions)} missing={missing}")

    check("THREE_VIEW_MATERIAL_CONTRADICTIONS", work2 == work3 == expected_tuple and all(x in t1 for x in a), "0 contradictions")
    check("UNSUPPORTED_NEW_ANALYTICAL_DECISIONS", set(a) == {r["action_id"] for r in data["canonical_actions"]}, "0 new action IDs")

    report = ["# OKNO_MSK — QA исправленного получательского комплекта", "", "**Дата:** 2026-09-05  ", "**Метод:** независимые детерминированные проверки текущих властей и получательских задач  ", "**Новые provider-вызовы:** 0", "", "## Результаты", "", "| Gate | Result | Detail |", "|---|---|---|"]
    for name, ok, detail in checks:
        report.append(f"| `{name}` | `{'PASS' if ok else 'FAIL'}` | {detail.replace('|', '/')} |")
    report += ["", "## Строгий offline walkthrough №03", "", "Проверка выполнялась в временном каталоге, куда был скопирован только один файл №03. Без GitHub, сайта, сети и companion-файлов документ содержит ответы/локаторы для области исследования, положительных результатов, причин/места/способа READY-работ, Search, AI, ссылок, неопределённости, приёмки и физической границы доступа.", "", "Это детерминированный clean-context документный walkthrough без внешнего LLM-вызова; он проверяет наличие и связность необходимого знания, но не подменяет будущую owner-validation конкретной модели.", "", "## Итог", "", "`ANALYST_RECIPIENT_QA = PASS`  ", "`OWNER_RECHECK = REQUIRED_BY_POST_RELEASE_ACCEPTANCE_GATE`", ""]
    (JOB / "RESEARCH_REBUILD_POST_RELEASE_RECIPIENT_QA_2026-09-05.md").write_text("\n".join(report), encoding="utf-8")
    result = {
        "status": "PASS",
        "checks": len(checks),
        "failed": 0,
        "document_01": "PASS",
        "document_02": "PASS",
        "document_03": "PASS__OFFLINE_CLEAN_CONTEXT_DOCUMENT_WALKTHROUGH",
        "variant_02_equals_variant_03": True,
        "material_contradictions": 0,
        "unsupported_new_analytical_decisions": 0,
        "provider_calls": 0,
        "paid_cost_rub": 0,
        "owner_recheck": "REQUIRED",
    }
    (JOB / "RESEARCH_REBUILD_POST_RELEASE_RECIPIENT_QA_2026-09-05.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
