#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

BANNED_LITERAL = [
    "не выдавать за готовую",
    "получить названное доказательство",
    "из них не следует",
    "не внедрять",
    "не размещать",
    "не создавать",
    "не менять",
    "что сейчас запрещено",
    "граница приёмки сейчас",
    "отдельно санкционировать",
    "новые факты о сайте",
    "новые факты не собирались",
    "не расширяет его новыми фактами",
    "post-hoc",
    "провайдер",
]

OBVIOUS_MECHANICS = [
    r"\bоткройте\b",
    r"\bперейдите\b",
    r"\bнайдите\b",
    r"\bкликните\b",
]

INTERNAL_PATTERNS = [
    r"S18-A\d+",
    r"STEP_[A-Z0-9_]+",
    r"Stage\d+",
    r"CV\d+",
    r"OR-\d+",
    r"\bCONTENT_BLOCK\b",
    r"\bSEMANTIC_MAPPING_ONLY\b",
    r"\bRECHECK_ONLY\b",
    r"\bREADY_[A-Z0-9_]+\b",
    r"\bP[12]_[A-Z]+\b",
    r"\bREAL_SITE_CHANGE\b",
]


def hit_lines(text: str, pattern: str, regex: bool = False):
    out = []
    rx = re.compile(pattern, re.I) if regex else None
    for idx, line in enumerate(text.splitlines(), 1):
        ok = bool(rx.search(line)) if rx else pattern.casefold() in line.casefold()
        if ok:
            out.append({"line": idx, "text": line.strip()})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("markdown", type=Path)
    ap.add_argument("--out", type=Path)
    ns = ap.parse_args()
    text = ns.markdown.read_text("utf-8")

    checks = []
    def add(name, ok, detail=None):
        checks.append({"name": name, "status": "PASS" if ok else "FAIL", "detail": detail})

    banned = []
    for item in BANNED_LITERAL:
        banned.extend({"pattern": item, **x} for x in hit_lines(text, item))
    add("client_negative_pseudo_action_phrases", not banned, banned)

    mechanics = []
    for pat in OBVIOUS_MECHANICS:
        mechanics.extend({"pattern": pat, **x} for x in hit_lines(text, pat, True))
    add("obvious_open_find_navigate_mechanics", not mechanics, mechanics)

    internal = []
    for pat in INTERNAL_PATTERNS:
        internal.extend({"pattern": pat, **x} for x in hit_lines(text, pat, True))
    add("project_internal_traceability", not internal, internal)

    ne_hits = hit_lines(text, r"\bне\b", True)
    add("current_job_negative_particle_ne_hits", len(ne_hits) == 0, ne_hits)

    add("ready_count", text.count("### 1. Уточнить страницу французских окон") == 1 and "### 2. Добавить критерии выбора размеров ПВХ-двери" in text and "### 3. Актуализировать маркировку рейтинга 2024 года" in text)
    add("clarification_count", text.count("## 5. Уточнить перед внедрением") == 1 and all(f"### {i}." in text.split("## 5. Уточнить перед внедрением",1)[1].split("## 6.",1)[0] for i in range(1,6)))

    sec6 = text.split("## 6. Семантические назначения", 1)[1].split("## 7.", 1)[0]
    sec8 = text.split("## 8. Внутренние связи для детализации", 1)[1].split("## 9.", 1)[0]
    add("semantic_assignment_rows", len(re.findall(r"^\| \d+ \|", sec6, re.M)) == 46, len(re.findall(r"^\| \d+ \|", sec6, re.M)))
    add("internal_link_rows", len(re.findall(r"^\| \d+ \|", sec8, re.M)) == 14, len(re.findall(r"^\| \d+ \|", sec8, re.M)))
    add("semantic_repeated_no_change_instruction_absent", "физически страницу" not in sec6.casefold())
    add("client_process_meta_absent", all(x not in text.casefold() for x in ["санкционирован", "post-hoc", "новые факты не собирались", "провайдер", "quarantin"]))
    add("a031_publication_date_claim_absent", not re.search(r"опубликован\w*\s+в\s+2024|дата публикации", text, re.I))
    add("a031_ranking_year_present", "рейтинг производителей за 2024 год" in text)
    add("bibliography_count", len(re.findall(r"^\d+\. «", text.split("## 11. Материалы, на которые мы опирались",1)[1], re.M)) == 10)
    add("alice_bibliography", "Видимость сайта в Алисе AI" in text and "попадание в ответы Алисы AI" in text)
    add("section_structure", all(f"## {i}." in text for i in range(1,12)))

    result = {
        "artifact": str(ns.markdown),
        "status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
        "checks_total": len(checks),
        "checks_passed": sum(c["status"] == "PASS" for c in checks),
        "checks": checks,
    }
    out = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if ns.out:
        ns.out.write_text(out, "utf-8")
    print(out)
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
