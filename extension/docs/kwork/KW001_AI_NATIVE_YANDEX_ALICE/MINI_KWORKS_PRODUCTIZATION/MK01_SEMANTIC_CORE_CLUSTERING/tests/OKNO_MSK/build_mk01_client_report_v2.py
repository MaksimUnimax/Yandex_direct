#!/usr/bin/env python3
"""MK01 analytical client-report generator v2.

Permanent safety boundary:
    CLIENT REPORT != EXECUTION PROTOCOL

This generator validates analytical completeness before materialization. It does not
consider correct counts, file existence, page count or clean layout sufficient for
client-report PASS.

The accepted semantic analysis remains external authority; this script only builds
recipient views from an accepted source/manifest and never invents analytical facts.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt


REQUIRED_ANALYTICAL_SECTIONS = (
    "## Главные выводы",
    "## 2. Структура рабочего ядра по типу задачи",
    "## 3. Крупнейшие смысловые группы",
    "## 4. Что осталось на проверку и что было исключено",
    "## 5. Как пользоваться Excel-файлом",
    "## 6. Итоговые выводы для дальнейшей работы",
    "## 7. Методические источники и ограничения",
)

PROHIBITED_CLIENT_JARGON = (
    "exact-universe",
    "phrase key",
    "route state",
    "failure class",
    "provenance",
    "authority",
    "provider request",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_analytical_source(source: str, manifest: dict) -> None:
    missing = [section for section in REQUIRED_ANALYTICAL_SECTIONS if section not in source]
    if missing:
        raise SystemExit(
            "CLIENT REPORT != EXECUTION PROTOCOL gate failed. "
            f"Missing analytical sections: {missing}"
        )

    lower = source.lower()
    leaked = [token for token in PROHIBITED_CLIENT_JARGON if token.lower() in lower]
    if leaked:
        raise SystemExit(f"Client-language gate failed; internal jargon found: {leaked}")

    data = manifest["data"]
    intent = data["intent_phrase_counts"]
    intent_groups = data["intent_group_counts"]
    review = data["review_breakdown"]
    excluded = data["excluded_breakdown"]
    outside = data["outside_task_groups"]

    checks = {
        "intent phrase sum": sum(intent.values()) == data["working_core"],
        "intent group sum": sum(intent_groups.values()) == data["working_groups"],
        "review sum": sum(review.values()) == data["review"],
        "excluded sum": sum(excluded.values()) == data["excluded"],
        "outside-task sum": sum(outside.values()) == excluded["outside_task_after_clustering"],
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise SystemExit(f"Derived-metric reconciliation failed: {failed}")

    # Explicitly reject the old false proxy.
    if "must normally be 4–8 pages" in source or "обязательно 4–8" in lower:
        raise SystemExit("Page-count quality proxy is prohibited (E39).")


def make_bar_chart(labels, values, title: str, xlabel: str, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    positions = list(range(len(labels)))
    ax.barh(positions, values)
    ax.set_yticks(positions, labels=labels)
    ax.invert_yaxis()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    for i, v in enumerate(values):
        ax.text(v, i, f" {v}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)


def build_charts(manifest: dict, workdir: Path) -> dict[str, Path]:
    d = manifest["data"]

    intent_labels = [
        "Коммерческий",
        "Сервисный",
        "Информационный",
        "Самостоятельное выполнение",
        "Навигационный",
    ]
    intent_values = [
        d["intent_phrase_counts"]["commercial"],
        d["intent_phrase_counts"]["service"],
        d["intent_phrase_counts"]["informational"],
        d["intent_phrase_counts"]["informational_diy"],
        d["intent_phrase_counts"]["navigational"],
    ]
    intent_path = workdir / "intent_structure.png"
    make_bar_chart(intent_labels, intent_values, "Структура рабочего ядра", "Количество фраз", intent_path)

    exclusion_labels = [
        "Вне согласованных границ",
        "Нерелевантно",
        "Механический шум",
        "Посторонняя задача после группировки",
    ]
    exclusion_values = [
        d["excluded_breakdown"]["scope"],
        d["excluded_breakdown"]["irrelevant"],
        d["excluded_breakdown"]["mechanical"],
        d["excluded_breakdown"]["outside_task_after_clustering"],
    ]
    exclusions_path = workdir / "exclusions.png"
    make_bar_chart(exclusion_labels, exclusion_values, "Почему фразы исключены", "Количество фраз", exclusions_path)

    return {"intent": intent_path, "exclusions": exclusions_path}


def inject_chart_markers(source: str, charts: dict[str, Path]) -> str:
    intent_heading = "## 2. Структура рабочего ядра по типу задачи"
    exclusion_heading = "## 4. Что осталось на проверку и что было исключено"
    source = source.replace(
        intent_heading,
        intent_heading + f"\n\n![Структура рабочего ядра]({charts['intent'].as_posix()})",
        1,
    )
    source = source.replace(
        exclusion_heading,
        exclusion_heading + f"\n\n![Структура исключений]({charts['exclusions'].as_posix()})",
        1,
    )
    return source


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def materialize(source_path: Path, manifest_path: Path, out_docx: Path, out_pdf: Path | None) -> None:
    source = source_path.read_text(encoding="utf-8")
    manifest = load_json(manifest_path)
    validate_analytical_source(source, manifest)

    if shutil.which("pandoc") is None:
        raise SystemExit("pandoc is required to materialize the DOCX")

    out_docx.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="mk01_client_report_") as tmp:
        tmpdir = Path(tmp)
        charts = build_charts(manifest, tmpdir)
        enriched = inject_chart_markers(source, charts)
        md = tmpdir / "report.md"
        md.write_text(enriched, encoding="utf-8")

        run([
            "pandoc",
            str(md),
            "--from=gfm",
            "--to=docx",
            "--standalone",
            "--metadata", "title=Отчёт по семантическому ядру",
            "--output", str(out_docx),
        ])

    if out_pdf is not None:
        if shutil.which("libreoffice") is None:
            raise SystemExit("libreoffice is required for PDF materialization")
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="mk01_lo_") as lo_tmp:
            run([
                "libreoffice",
                "--headless",
                f"-env:UserInstallation=file://{Path(lo_tmp).as_posix()}",
                "--convert-to", "pdf",
                "--outdir", str(out_pdf.parent),
                str(out_docx),
            ])
            generated = out_pdf.parent / (out_docx.stem + ".pdf")
            if generated != out_pdf:
                generated.replace(out_pdf)

    print("ANALYTICAL_REPORT_GATE=PASS")
    print(f"DOCX={out_docx}")
    if out_pdf:
        print(f"PDF={out_pdf}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--out-docx", type=Path, required=True)
    ap.add_argument("--out-pdf", type=Path)
    args = ap.parse_args()
    materialize(args.source, args.manifest, args.out_docx, args.out_pdf)


if __name__ == "__main__":
    main()
