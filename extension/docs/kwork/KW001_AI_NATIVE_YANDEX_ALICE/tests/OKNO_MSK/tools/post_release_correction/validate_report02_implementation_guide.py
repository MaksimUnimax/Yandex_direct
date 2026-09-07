#!/usr/bin/env python3
"""Scope-freeze and recipient acceptance validator for Report №02."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from docx import Document
from pypdf import PdfReader


HERE = Path(__file__).resolve()
JOB = HERE.parents[2]
BASE = JOB.parents[2]
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
MD = RELEASE / "sources/02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.md"
DOCX = RELEASE / "editable/02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.docx"
PDF = RELEASE / "02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.pdf"
ACTION_AUTHORITY = JOB / "RESEARCH_REBUILD_POST_RELEASE_SHARED_IMPLEMENTATION_AUTHORITY_CORRECTED_2026-09-05.tsv"
LINK_AUTHORITY = JOB / "RESEARCH_REBUILD_POST_RELEASE_INTERNAL_LINK_AUTHORITY_CORRECTED_2026-09-05.tsv"
ROUTE_AUTHORITY = JOB / "RESEARCH_REBUILD_POST_RELEASE_ROUTING_AUTHORITY_CORRECTED_2026-09-05.tsv"
METHOD_REFS = JOB / "RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_02_METHOD_REFERENCES_2026-09-07.md"
POSTHOC_PLACEMENT = JOB / "RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_02_CURRENT_SITE_PLACEMENT_EVIDENCE_2026-09-07.md"
POSTHOC_PORTFOLIO = JOB / "RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_02_PORTFOLIO_MAPPING_EVIDENCE_2026-09-07.tsv"
VISUAL_QA = JOB / "RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_02_VISUAL_QA_2026-09-07.json"
OUTPUT = JOB / "RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_02_IMPLEMENTATION_GUIDE_QA_2026-09-07.json"
GENERATOR = JOB / "tools/post_release_correction/build_report02_implementation_guide.py"

PROTECTED = {
    "document_01": (RELEASE / "01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.pdf", "79450c2f0dc58ea064b72b7c400f6db7b908cb455c72003584c5e59c9b9fad08"),
    "document_03": (RELEASE / "03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.md", "d5c90cf187041e975f17d03a2be138eff0b6a06bfe1b7d395a3b24547edc62b0"),
    "semantic_core_04": (RELEASE / "04_OKNO_MSK_FULL_SEMANTIC_CORE_2026-09-07.xlsx", "cee26a8d7d4a8381d4706c7940b739c3afca652034e9e3630053e35bd0184e3a"),
}

READY_TITLES = [
    "Уточнить страницу французских окон",
    "Добавить критерии выбора размеров ПВХ-двери",
    "Убрать ложную актуальность из рейтинга 2024 года",
]
READY_IDS = ["S18-A009", "S18-A028", "S18-A031"]
PARTIAL_TITLES = [
    "Объяснить выбор размеров окон для частного дома",
    "Уточнить роль монтажа на странице ПВХ-дверей",
    "Добавить объяснение вентиляции при алюминиевом остеклении",
    "Подготовить навигацию по портфолио",
    "Раскрыть выбор панорамного алюминиевого остекления",
]
PARTIAL_IDS = ["S18-A010", "S18-A012", "S18-A026", "S18-A029", "S18-A030"]
READY_URLS = [
    "https://okno-msk.ru/okna-rehau/francuzskie-okna",
    "https://okno-msk.ru/dveri-rehau",
    "https://okno-msk.ru/stati/kakie-okna-samye-luchshie",
]

INTERNAL_ID_RE = re.compile(r"\b(?:S18-A\d+|Stage\d+|CV\d+|OR-\d+)\b", re.I)
INTERNAL_FILENAME_RE = re.compile(r"\bSTEP_[A-Z0-9_]+(?:\.(?:tsv|json|md|txt))?\b|\b[A-Z0-9_]+\.(?:tsv|json|xlsx)\b")
INTERNAL_ENUM_RE = re.compile(r"\b(?:CONTENT_BLOCK(?:_PARTIAL)?|SEMANTIC_MAPPING_ONLY|RECHECK_ONLY|READY(?:_[A-Z0-9_]+)?|P[12]_[A-Z0-9_*]+|REAL_SITE_CHANGE|TO_CALIBRATE|SEARCH_REQUIRED|CTA)\b", re.I)
PLACEHOLDER_RE = re.compile(r"\[(?:дата|указать)[^\]]*\]|\b(?:TBD|TODO|TO_CALIBRATE|XXX)\b", re.I)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tsv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def docx_text(path: Path) -> str:
    doc = Document(path)
    chunks = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        chunks.extend(cell.text for row in table.rows for cell in row.cells)
    return "\n".join(chunks)


def normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold()


checks: list[dict[str, object]] = []


def check(name: str, condition: bool, detail: object = None) -> None:
    checks.append({"name": name, "status": "PASS" if condition else "FAIL", "detail": detail})


def section(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def main() -> int:
    md = MD.read_text(encoding="utf-8")
    generator = GENERATOR.read_text(encoding="utf-8")
    dx = docx_text(DOCX)
    reader = PdfReader(str(PDF))
    px = "\n".join(page.extract_text() or "" for page in reader.pages)
    formats = {"markdown": md, "docx": dx, "pdf": px}

    check("section_structure", all(f"## {i}." in md for i in range(1, 12)))
    ready = section(md, "## 4. Изменения сайта, готовые к внедрению", "## 5. Частичные пункты")
    partial = section(md, "## 5. Частичные пункты", "## 6. Семантические назначения")
    check("ready_count", len(re.findall(r"^### \d+\.", ready, re.M)) == 3)
    check("partial_count", len(re.findall(r"^### \d+\.", partial, re.M)) == 5)
    check("ready_titles", all(title in ready for title in READY_TITLES))
    check("partial_titles", all(title in partial for title in PARTIAL_TITLES))
    check("ready_urls", all(url in ready for url in READY_URLS))
    check("summary_counts", all(token in md for token in ["| Изменения сайта, готовые к внедрению | 3 |", "| Частичные пункты / требуется подтверждение | 5 |", "| Семантические назначения без физической правки | 46 |", "| Нужна дополнительная проверка | 4 |", "| Отложенные темы | 20 |"]))

    action_rows = {r["action_id"]: r for r in tsv_rows(ACTION_AUTHORITY)}
    preexisting_placements = {
        "S18-A009": "После вводного определения, до ценовых/конфигурационных блоков.",
        "S18-A028": "После видов дверных створок, до цен.",
        "S18-A031": "Раздел «Рейтинг производителей оконных профилей».",
    }
    check("preexisting_ready_placement_authority", all(action_rows[aid]["exact_location_ru"] == value for aid, value in preexisting_placements.items()), {aid: action_rows[aid]["exact_location_ru"] for aid in preexisting_placements})
    ready_locations = re.findall(r"\*\*Точное место по завершённому исследованию\*\*\s*\n\s*([^\n]+)", ready)
    check("ready_exact_placement_count", len(ready_locations) == 3, ready_locations)
    check("ready_exact_placements_unambiguous", len(ready_locations) == 3 and not any(re.search(r"\bили\b|один из|например в|где-то после|в подходящем месте", loc, re.I) for loc in ready_locations), ready_locations)
    check("posthoc_exact_headings_absent", not any(value in md for value in ["Особенности французского остекления", "Преимущества панорамных конструкций", "С нами купить окна для частного дома просто", "Калькулятор окон для частного дома", "Недостатки алюминиевых окон", "Советы по остеклению балкона алюминиевым профилем", "Особенности профилей Provedal", "Выбор цвета по шкале RAL", "Калькулятор дверей"]))

    cards = re.split(r"^### \d+\. ", ready, flags=re.M)[1:]
    step_blocks = []
    for card in cards:
        block = card.split("**Как это может выглядеть**", 1)[0].split("**Пошагово**", 1)[1]
        steps = re.findall(r"^\d+\. (.+)$", block, re.M)
        step_blocks.append("\n".join(normalized(x) for x in steps))
    check("ready_action_specific_steps", len(step_blocks) == 3 and all(len(block.splitlines()) >= 6 for block in step_blocks))
    check("ready_action_generic_step_template_reuse", len(set(step_blocks)) == 3, len(set(step_blocks)))
    check("ready_bold_examples", ready.count("**Как это может выглядеть**") == 3 and len(re.findall(r"^> .*\*\*.+\*\*", ready, re.M)) >= 3)
    check("numbering_not_schedule", "Нумерация используется для навигации и приёмки" in md and "очередность внедрения определяют" in md)

    check("a029_partial", "Подготовить навигацию по портфолио" in partial and "Полная разметка существующих карточек" in partial and "Точный набор фильтров определяется только после полной разметки карточек" in partial)
    check("posthoc_portfolio_mapping_absent", "224" not in md and "Страница / позиция" not in md and "Готовое соответствие" not in md)
    check("a031_no_placeholder", "2024" in ready and not PLACEHOLDER_RE.search(ready))
    check("a012_partial_boundary", "Уточнить роль монтажа" in partial and "состав услуги" in partial and "Компания должна подтвердить" in partial)

    route_count = len(tsv_rows(ROUTE_AUTHORITY))
    mapping = section(md, "## 6. Семантические назначения", "## 7. Нужна дополнительная проверка")
    check("mapping_only_count", route_count == 46 and len(re.findall(r"^\| \d+ \|", mapping, re.M)) == 46)
    blocked = section(md, "## 7. Нужна дополнительная проверка", "## 8. Потенциальные внутренние ссылки")
    check("blocked_count", len(re.findall(r"^### \d+\.", blocked, re.M)) == 4)
    check("deferred_topics", "20 отложенных тем" in blocked)

    links = tsv_rows(LINK_AUTHORITY)
    pairs = [(r["source_url"].rstrip("/"), r["target_url"].rstrip("/")) for r in links]
    unique_pairs = set(pairs)
    link_section = section(md, "## 8. Потенциальные внутренние ссылки", "## 9. Что обязательно сохранить")
    visible_pairs = re.findall(r"\| \d+ \| \[[^\]]+\]\((https?://[^)]+)\) \| \[[^\]]+\]\((https?://[^)]+)\) \|", link_section)
    normalized_visible = [(a.rstrip("/"), b.rstrip("/")) for a, b in visible_pairs]
    duplicate_visible = [pair for pair, count in Counter(normalized_visible).items() if count > 1]
    check("link_authority_rows", len(links) == 15, len(links))
    check("visible_unique_link_decisions", len(normalized_visible) == 14 and len(set(normalized_visible)) == 14, len(normalized_visible))
    check("duplicate_visible_link_pairs_without_explanation", duplicate_visible == [], duplicate_visible)
    check("visible_links_derive_from_authority", set(normalized_visible) == unique_pairs)

    method = METHOD_REFS.read_text(encoding="utf-8")
    bibliography = section(md, "## 11. Материалы, на которые мы опирались", "") if False else md.split("## 11. Материалы, на которые мы опирались", 1)[1]
    bibliography_items = re.findall(r"^\d+\. «.+» — .+\. https?://\S+$", bibliography, re.M)
    check("bibliography_count", len(bibliography_items) == 10, len(bibliography_items))
    coverage = {
        "wordstat": "support2/wordstat/ru/interface/new" in bibliography,
        "wordstat_operators": "support2/wordstat/ru/content/operators" in bibliography,
        "targeting": "webmaster/ru/recommendations/targeting" in bibliography,
        "clustering": "keyword-clustering" in bibliography,
        "mapping": "keyword-mapping" in bibliography,
        "intent": "keyword-intent" in bibliography,
        "cannibalization": "keyword-cannibalization" in bibliography,
        "internal_links": "internal-links-for-seo" in bibliography,
        "alice_yandex_ai": "alice-answers" in bibliography and "/epos" in bibliography,
    }
    check("bibliography_semantic_coverage", all(coverage.values()), coverage)
    check("external_methodology_bibliography_freshness", "Дата проверки: 2026-09-07" in method and "PASS" in method and all(url in method for url in re.findall(r"https?://\S+", bibliography)))

    language = {}
    for name, text in formats.items():
        language[name] = {
            "ids": len(INTERNAL_ID_RE.findall(text)),
            "filenames": len(INTERNAL_FILENAME_RE.findall(text)),
            "enums_or_abbreviations": len(INTERNAL_ENUM_RE.findall(text)),
            "placeholders": len(PLACEHOLDER_RE.findall(text)),
        }
    check("project_internal_ids_in_client_report", all(v["ids"] == 0 for v in language.values()), language)
    check("project_internal_filenames_in_client_report", all(v["filenames"] == 0 for v in language.values()), language)
    check("project_internal_enums_in_client_report", all(v["enums_or_abbreviations"] == 0 for v in language.values()), language)
    check("client_placeholders", all(v["placeholders"] == 0 for v in language.values()), language)

    posthoc_md = POSTHOC_PLACEMENT.read_text(encoding="utf-8")
    posthoc_tsv_prefix = "\n".join(POSTHOC_PORTFOLIO.read_text(encoding="utf-8").splitlines()[:3])
    check("posthoc_evidence_quarantined", all(token in posthoc_md for token in ["POST_HOC_REPORT_STAGE_COLLECTION", "NOT ORIGINAL RESEARCH AUTHORITY", "NOT AUTHORIZED TO UPGRADE READINESS"]) and all(token in posthoc_tsv_prefix for token in ["POST_HOC_REPORT_STAGE_COLLECTION", "NOT ORIGINAL RESEARCH AUTHORITY", "NOT AUTHORIZED TO UPGRADE READINESS"]))
    check("posthoc_report_stage_evidence_used_to_upgrade_readiness", "PORTFOLIO_AUTHORITY" not in generator and POSTHOC_PLACEMENT.name not in generator and POSTHOC_PORTFOLIO.name not in generator and "224" not in md)
    check("report_project_facts_trace_to_preexisting_research_authority", all(action_rows[aid]["target_object"] in md for aid in READY_IDS + PARTIAL_IDS) and all(value in {row["exact_location_ru"] for row in action_rows.values()} for value in preexisting_placements.values()))
    collection_qa = {
        "report_stage_new_project_fact_collection": 0,
        "unauthorized_current_site_recollection_after_clarification": 0,
        "unauthorized_search_recollection": 0,
        "unauthorized_wordstat_recollection": 0,
        "unauthorized_alice_ai_recollection": 0,
        "post_hoc_report_stage_evidence_used_to_upgrade_readiness": 0,
    }
    check("report_stage_project_data_recollection_qa", all(value == 0 for value in collection_qa.values()), collection_qa)

    tokens = READY_TITLES + PARTIAL_TITLES + READY_URLS + ["46", "15", "14", "2024", "Алисе"]
    equivalence = {name: all(normalized(token) in normalized(text) for token in tokens) for name, text in formats.items()}
    check("markdown_docx_pdf_required_content_equivalence", all(equivalence.values()), equivalence)
    doc = Document(DOCX)
    bold_text = " ".join(run.text for p in doc.paragraphs for run in p.runs if run.bold)
    check("docx_bold_proposed_additions", all(term in bold_text for term in ["До выбора конфигурации", "При выборе двери", "В опубликованном в 2024 году", "Профессиональный монтаж", "Направления будущей разметки"]))
    check("docx_expected_tables", len(doc.tables) == 3, len(doc.tables))
    check("pdf_no_empty_pages", all((page.extract_text() or "").strip() for page in reader.pages))
    check("docx_not_corrupt", DOCX.stat().st_size > 30000, DOCX.stat().st_size)
    check("pdf_not_corrupt", PDF.stat().st_size > 100000, PDF.stat().st_size)

    visual = json.loads(VISUAL_QA.read_text(encoding="utf-8")) if VISUAL_QA.exists() else {}
    visual_pass = visual.get("status") == "PASS" and visual.get("pdf_sha256") == sha(PDF) and visual.get("pages_total") == len(reader.pages) and visual.get("pages_inspected") == list(range(1, len(reader.pages) + 1))
    check("visual_qa_all_pages", visual_pass, visual)
    protected = {name: sha(path) == expected for name, (path, expected) in PROTECTED.items()}
    check("protected_artifacts_unchanged", all(protected.values()), protected)

    failed = [item["name"] for item in checks if item["status"] == "FAIL"]
    payload = {
        "artifact": "DOCUMENT_02_SCOPE_FREEZE_REMEDIATION",
        "status": "PASS" if not failed else "FAIL",
        "owner_review": "PENDING",
        "date": "2026-09-07",
        "counts": {"ready": 3, "partial": 5, "mapping_only": 46, "blocked_recheck": 4, "deferred_topics": 20, "internal_link_authority_rows": 15, "visible_unique_link_decisions": 14, "bibliography": 10, "pdf_pages": len(reader.pages)},
        "language_qa": language,
        "collection_scope_qa": collection_qa,
        "bibliography_semantic_coverage": coverage,
        "cross_format_equivalence": "PASS" if all(equivalence.values()) else "FAIL",
        "visual_qa": visual,
        "protected_artifacts": protected,
        "checks": checks,
        "failed": failed,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": len(checks), "failed": failed, "output": str(OUTPUT)}, ensure_ascii=False))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
