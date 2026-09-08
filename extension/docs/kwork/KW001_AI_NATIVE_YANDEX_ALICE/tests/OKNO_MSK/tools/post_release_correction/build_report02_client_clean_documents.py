#!/usr/bin/env python3
"""Build recipient Report №02 without an empty TOC and without orphan field labels."""
from __future__ import annotations

import subprocess
from pathlib import Path

from docx import Document

import build_recipient_docx as base

HERE = Path(__file__).resolve()
JOB = HERE.parents[2]
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
SOURCE = RELEASE / "sources/02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.md"
DOCX = RELEASE / "editable/02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.docx"
PDF = RELEASE / "02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.pdf"
LABEL = "OKNO_MSK · руководство специалиста"

KEEP_WITH_NEXT_LABELS = {
    "Проблема",
    "Что изменить",
    "Где изменить",
    "Работы",
    "Пример смысловой реализации",
    "Сохранить",
    "Критерии приёмки",
    "Что уже определено",
    "Что уточнить",
    "Содержание будущего блока",
    "Результат уточнения",
    "Что проверить",
    "Результат проверки",
}


def build_docx() -> None:
    DOCX.parent.mkdir(parents=True, exist_ok=True)
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    temp_md = DOCX.with_suffix(".client-clean.pandoc.md")
    temp_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Report №02 deliberately has no generated TOC. In this compact specialist guide
    # Pandoc/LibreOffice rendered an empty TOC heading without entries.
    subprocess.run([
        "/usr/bin/pandoc", str(temp_md), "--from=gfm", "--to=docx",
        "--metadata", f"title={LABEL}", "--metadata", "lang=ru",
        "--output", str(DOCX),
    ], check=True)
    temp_md.unlink()
    base.style_doc(DOCX, "compact_reference_guide", LABEL)

    doc = Document(DOCX)
    for p in doc.paragraphs:
        if p.text.strip() in KEEP_WITH_NEXT_LABELS:
            p.paragraph_format.keep_with_next = True
    doc.save(DOCX)


def main() -> None:
    build_docx()
    base.export_optimized_pdf(DOCX, PDF)
    print(DOCX)
    print(PDF)


if __name__ == "__main__":
    main()
