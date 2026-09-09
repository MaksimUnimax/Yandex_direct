#!/usr/bin/env python3
"""Build the versioned post-Step5A client DOCX/PDF files and XLSX."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH


HERE = Path(__file__).resolve()
WORK = HERE.parent
JOB = HERE.parents[1]
REPO = HERE.parents[7]
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09"
TOOLS = JOB / "tools/post_release_correction"
RUNTIME = Path(os.environ["CODEX_PRIMARY_RUNTIME_ROOT"])
PYTHON = os.environ.get("CODEX_PRIMARY_RUNTIME_PYTHON", "python3")


def build_doc(md: Path, docx: Path, pdf: Path, label: str, preset: str) -> None:
    import sys
    sys.path.insert(0, str(TOOLS))
    import build_recipient_docx as base

    lines = md.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    temp = WORK / f".{docx.stem}.pandoc.md"
    temp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    docx.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["/usr/bin/pandoc", str(temp), "--from=gfm", "--to=docx", "--metadata", f"title={label}", "--metadata", "lang=ru", "--output", str(docx)], check=True)
    temp.unlink()
    base.style_doc(docx, preset, label)
    doc = Document(docx)
    for section in doc.sections:
        header = section.header.paragraphs[0]
        for run in header.runs:
            run.text = run.text.replace("OKNO_MSK", "Окно Москва")
        footer = section.footer.paragraphs[0]
        # The base template contains a Word PAGE field whose cached value stays
        # at “1” in headless conversion. A stable, non-numbered footer avoids a
        # misleading page number in both reproducible DOCX and exported PDF.
        footer.text = "Окно Москва · обновлённый выпуск · 2026-09-09"
        footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in footer.runs:
            base.set_font(run, "Arial", 8, color="6B7280")
    doc.save(docx)
    base.export_optimized_pdf(docx, pdf)


def main() -> None:
    if os.environ.get("STEP5A_SKIP_DOCS") != "1":
        build_doc(
            RELEASE / "sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.md",
            RELEASE / "editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.docx",
            RELEASE / "01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.pdf",
            "ОКНО МОСКВА — поисковое ядро под Алису и обычную выдачу Яндекса",
            "standard_business_brief",
        )
        build_doc(
            RELEASE / "sources/02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-09.md",
            RELEASE / "editable/02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-09.docx",
            RELEASE / "02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-09.pdf",
            "Внедрение рекомендаций",
            "compact_reference_guide",
        )
    if os.environ.get("STEP5A_SKIP_XLSX") != "1":
        xlsx = RELEASE / "04_OKNO_MSK_FULL_SEMANTIC_CORE_2026-09-09.xlsx"
        preview = WORK / "xlsx_previews"
        runtime_report = WORK / "XLSX_BUILD_RUNTIME.json"
        mjs = TOOLS / "materialize_standalone_semantic_core.mjs"
        node_env = dict(os.environ)
        node_env["NODE_OPTIONS"] = "--max-old-space-size=8192"
        subprocess.run([
            os.environ.get("CODEX_PRIMARY_RUNTIME_NODE", "node"), str(mjs),
            "--repo-root", str(REPO), "--output", str(xlsx), "--preview-dir", str(preview),
            "--runtime-report", str(runtime_report), "--master", str(WORK / "POST_STEP09_FINAL_SEMANTIC_MASTER_2856.tsv"),
            "--units", str(WORK / "POST_STEP09_CANONICAL_UNIT_AUTHORITY.tsv"), "--step8", str(JOB / "STEP_05A_POST_ACCEPTANCE_PROPAGATION_2026-09-08/STEP_05A_POST_ACCEPTANCE_STEP08_FREEZE.tsv"),
            "--expected-rows", "2856", "--expected-active", "2348", "--expected-assigned", "2329", "--expected-search-required", "19",
            "--expected-page-groups", "64",
        ], check=True, env=node_env)

    # The spreadsheet runtime writes a very large cell-inspection trace beside
    # the XLSX. Keep it as a transient diagnostic outside the repository; the
    # compact runtime report above preserves the durable QA facts we need.
    xlsx_inspect = RELEASE / "04_OKNO_MSK_FULL_SEMANTIC_CORE_2026-09-09.xlsx.inspect.ndjson"
    if xlsx_inspect.exists():
        transient_inspect = Path(tempfile.gettempdir()) / "OKNO_MSK_STEP5A_2026-09-09.xlsx.inspect.ndjson"
        xlsx_inspect.replace(transient_inspect)

    artifacts = []
    for path in sorted(RELEASE.rglob("*")):
        if path.is_file() and path.name != "RELEASE_MANIFEST_2026-09-09.json" and not path.name.endswith(".inspect.ndjson"):
            import hashlib
            artifacts.append({"path": str(path.relative_to(RELEASE)), "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest = {
        "schema": "OKNO_MSK_CLIENT_RELEASE_STEP5A_PROPAGATED_V1", "date": "2026-09-09",
        "semantic_rows": 2856, "active_rows": 2348, "exact_page_assigned_rows": 2322,
        "active_hold_rows": 7, "structural_units": 168, "new_pages": 0, "new_provider_calls": 0,
        "document_03_content_state": "BYTE_IDENTICAL_TO_CORRECTED_2026-09-05",
        "artifacts": artifacts,
    }
    (RELEASE / "RELEASE_MANIFEST_2026-09-09.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
