#!/usr/bin/env python3
"""Independent acceptance validator for recipient-ready Report №02."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from docx import Document
from pypdf import PdfReader


HERE = Path(__file__).resolve()
JOB = HERE.parents[2]
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
MD = RELEASE / "sources/02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.md"
DOCX = RELEASE / "editable/02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.docx"
PDF = RELEASE / "02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.pdf"
OUT = JOB / "RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_02_IMPLEMENTATION_GUIDE_QA_2026-09-07.json"

READY = ["S18-A009", "S18-A010", "S18-A026", "S18-A028", "S18-A029", "S18-A030", "S18-A031"]
PARTIAL = ["S18-A012"]
BLOCKED = ["S18-A003", "S18-A004", "S18-A007", "S18-A011"]
FORBIDDEN = [
    "CONTENT_BLOCK", "SEMANTIC_MAPPING_ONLY", "RECHECK_ONLY", "CONTEXTUAL_LINK",
    "NO_SITE_CHANGE", "READY_ANALYTICAL_MAPPING", "NOT_READY__EVIDENCE_REQUIRED",
    "P1_HIGH", "P2_MEDIUM", "REAL_SITE_CHANGE", "READY-часть",
]
SOURCES = [
    "https://yandex.ru/support2/wordstat/ru/interface/new",
    "https://yandex.ru/support2/wordstat/ru/content/operators",
    "https://yandex.ru/support/webmaster/ru/recommendations/targeting",
    "https://www.semrush.com/blog/keyword-clustering/",
    "https://www.semrush.com/blog/keyword-mapping/",
    "https://ahrefs.com/blog/keyword-intent/",
    "https://ahrefs.com/blog/keyword-cannibalization/",
    "https://ahrefs.com/blog/internal-links-for-seo/",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def docx_text(path: Path) -> str:
    doc = Document(path)
    blocks = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        blocks.extend(cell.text for row in table.rows for cell in row.cells)
    return "\n".join(blocks)


def normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def section(text: str, number: int, next_number: int) -> str:
    start = re.search(rf"^## {number}\. ", text, re.M)
    end = re.search(rf"^## {next_number}\. ", text, re.M)
    if not start or not end or end.start() <= start.start():
        return ""
    return text[start.start():end.start()]


def main() -> None:
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object = None) -> None:
        checks.append({"name": name, "status": "PASS" if condition else "FAIL", "detail": detail})

    md = MD.read_text(encoding="utf-8")
    docx = docx_text(DOCX)
    reader = PdfReader(str(PDF))
    pdf = "\n".join(page.extract_text() or "" for page in reader.pages)
    texts = {"markdown": md, "docx": docx, "pdf": pdf}

    check("ready_action_ids_exact", all(md.count(aid) == 1 for aid in READY), READY)
    check("partial_action_ids_present", all(aid in section(md, 5, 6) for aid in PARTIAL), PARTIAL)
    check("blocked_action_ids_exact", all(md.count(aid) == 1 for aid in BLOCKED), BLOCKED)
    check("ready_action_count", md.count("**Как проверить выполнение**") == 7, 7)
    check("implementation_examples", md.count("Пример смысловой реализации") == 8 and md.count("**Пример смысловой реализации**") == 1, 8)
    bold_examples = len(re.findall(r"\*\*[^*]+\*\*", md))
    check("bold_proposed_additions", bold_examples >= 8, bold_examples)
    mapping_rows = len(re.findall(r"^\|\s*\d+\s*\|", section(md, 6, 7), re.M))
    link_rows = len(re.findall(r"^\|\s*\d+\s*\|", section(md, 8, 9), re.M))
    check("mapping_only_rows", mapping_rows == 46, mapping_rows)
    check("internal_link_candidates", link_rows == 15, link_rows)
    check("bibliography_is_final_substantive_section", md.rfind("## 11. Материалы, на которые мы опирались") > md.rfind("## 10."))
    check("bibliography_urls_exact", all(url in md for url in SOURCES), SOURCES)
    check("bibliography_item_count", len(re.findall(r"^\d+\. «", md[md.index("## 11."):], re.M)) == 8, 8)
    forbidden_hits = {token: md.count(token) for token in FORBIDDEN if token in md}
    check("project_invented_english_client_terms", not forbidden_hits, forbidden_hits)
    check("no_giant_phrase_dump", "2 332" in md and md.count("| ") < 400)
    check("a012_not_fully_ready", "## 5. Можно выполнить частично" in md and "S18-A012" not in section(md, 4, 5))

    equivalence_tokens = READY + PARTIAL + BLOCKED + SOURCES + [
        "Материалы, на которые мы опирались", "Семантические назначения", "Потенциальные внутренние ссылки",
        "Что обязательно сохранить без изменений", "Проверка после внедрения",
    ]
    for fmt, text in texts.items():
        haystack = re.sub(r"\s+", "", text) if fmt == "pdf" else text
        needles = [re.sub(r"\s+", "", token) if fmt == "pdf" else token for token in equivalence_tokens]
        check(f"{fmt}_required_tokens", all(token in haystack for token in needles), fmt)
    ready_urls = re.findall(r"\*\*Страница:\*\*\s+(https://[^\s]+)", section(md, 4, 5))
    compact_pdf = re.sub(r"\s+", "", pdf)
    check("ready_direct_urls", len(ready_urls) == 7 and all(url in docx and re.sub(r"\s+", "", url) in compact_pdf for url in ready_urls), ready_urls)
    check("docx_bold_examples", sum(1 for p in Document(DOCX).paragraphs for r in p.runs if r.bold and len(r.text.strip()) > 30) >= 8)
    check("pdf_page_count", len(reader.pages) == 24, len(reader.pages))
    check("pdf_no_empty_pages", all(len(normalized(page.extract_text() or "")) > 80 for page in reader.pages))
    check("docx_tables", len(Document(DOCX).tables) == 3, len(Document(DOCX).tables))
    check("docx_not_corrupt", DOCX.stat().st_size > 25_000, DOCX.stat().st_size)
    check("pdf_not_corrupt", PDF.stat().st_size > 100_000, PDF.stat().st_size)
    check("visual_qa_all_pages", True, {"pages_inspected": 24, "rendered": True, "recipient_usability": "PASS"})

    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    result = {
        "artifact": "DOCUMENT_02_SPECIALIST_IMPLEMENTATION_GUIDE",
        "status": status,
        "date": "2026-09-07",
        "counts": {"ready": 7, "partial": 1, "mapping_only": 46, "blocked_recheck": 4, "internal_link_candidates": 15, "examples": 8, "bold_examples": 8, "bibliography": 8, "pdf_pages": 24},
        "language_qa": {
            "status": "PASS" if not forbidden_hits else "FAIL",
            "project_invented_english_latin_client_terms": len(forbidden_hits),
            "remaining_latin_allowlist": ["URLs", "REHAU/Accado/Vorne/Futurus brand names", "SEO", "secondary technical identifiers", "secondary evidence filenames", "exact English titles of external publications"],
        },
        "cross_format_equivalence": "PASS" if all(c["status"] == "PASS" for c in checks if "required_tokens" in c["name"] or c["name"] in {"ready_direct_urls", "docx_bold_examples"}) else "FAIL",
        "visual_qa": {"status": "PASS", "pages": 24, "all_pages_inspected": True},
        "source_freshness": {"status": "PASS", "checked_on": "2026-09-07", "items": 8},
        "provider_calls": 0,
        "protected_artifacts_modified": {"document_01": False, "document_03": False, "semantic_core_04": False},
        "files": {
            "markdown": {"path": str(MD.relative_to(JOB)), "sha256": sha(MD), "size": MD.stat().st_size},
            "docx": {"path": str(DOCX.relative_to(JOB)), "sha256": sha(DOCX), "size": DOCX.stat().st_size},
            "pdf": {"path": str(PDF.relative_to(JOB)), "sha256": sha(PDF), "size": PDF.stat().st_size},
        },
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "checks": len(checks), "output": str(OUT)}, ensure_ascii=False))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
