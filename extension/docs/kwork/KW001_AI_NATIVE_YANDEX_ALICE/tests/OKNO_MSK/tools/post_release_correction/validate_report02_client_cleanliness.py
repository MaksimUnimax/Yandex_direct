#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

BANNED_LITERAL = [
    "руководство специалиста",
    "SEO-специалиста",
    "для SEO-специалиста",
    "для редактора",
    "для разработчика",
    "Документ №02 для",
    "Требования к существующей структуре",
    "Семантические назначения",
    "Внутренние связи для детализации",
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

ROLE_PATTERNS = [
    r"\bспециалист\w*\b",
    r"\bредактор\w*\b",
    r"\bразработчик\w*\b",
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

    add("visible_title", text.startswith("# Внедрение рекомендации\n"))

    banned = []
    for item in BANNED_LITERAL:
        banned.extend({"pattern": item, **x} for x in hit_lines(text, item))
    add("client_banned_literal_phrases", not banned, banned)

    roles = []
    for pat in ROLE_PATTERNS:
        roles.extend({"pattern": pat, **x} for x in hit_lines(text, pat, True))
    add("client_recipient_role_branding", not roles, roles)

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

    add(
        "ready_recommendations",
        all(x in text for x in [
            "### 1. Разделить французское и панорамное остекление",
            "### 2. Добавить правила выбора размеров ПВХ-двери",
            "### 3. Указать год рейтинга производителей",
        ]),
    )

    sec3 = text.split("## 3. Что уточнить перед внедрением", 1)[1].split("## 4.", 1)[0]
    add("clarification_items", len(re.findall(r"^### \d+\.", sec3, re.M)) == 5, len(re.findall(r"^### \d+\.", sec3, re.M)))

    sec4 = text.split("## 4. Распределение тем по страницам", 1)[1].split("## 5.", 1)[0]
    sec4_rows = len(re.findall(r"^\| \d+ \|", sec4, re.M))
    add("topic_page_rows", sec4_rows == 46, sec4_rows)
    add("topic_page_what_why_how", all(x in sec4 for x in ["**Что это.**", "**Для чего.**", "**Как использовать.**"]))
    add("topic_page_plain_columns", all(x in sec4 for x in ["Тема / вопрос пользователя", "Где раскрывать тему", "Связанная страница"]))

    sec5 = text.split("## 5. Проверки перед следующими изменениями", 1)[1].split("## 6.", 1)[0]
    add("additional_checks_count", len(re.findall(r"^### \d+\.", sec5, re.M)) == 4, len(re.findall(r"^### \d+\.", sec5, re.M)))
    add("additional_checks_explain_purpose_method_decision", all(sec5.count(x) == 4 for x in ["**Что нужно понять**", "**Зачем**", "**Как проверить**", "**Решение по результату**"]))

    sec6 = text.split("## 6. Связи между страницами", 1)[1].split("## 7.", 1)[0]
    sec6_rows = len(re.findall(r"^\| \d+ \|", sec6, re.M))
    add("page_link_rows", sec6_rows == 14, sec6_rows)
    add("page_link_what_why_how", all(x in sec6 for x in ["**Что это.**", "**Для чего.**", "**Как внедрять.**"]))
    add("page_link_plain_columns", all(x in sec6 for x in ["Откуда ведём", "Куда ведём"]))

    add("standalone_preservation_section_absent", "Требования к существующей структуре" not in text)
    add("old_research_funnel_absent", all(x not in text for x in ["2 415 строк", "2 965 наблюдений", "2 840 уникальных формулировок", "168 пользовательских задач"]))
    add("client_process_meta_absent", all(x not in text.casefold() for x in ["санкционирован", "post-hoc", "новые факты не собирались", "провайдер", "quarantin"]))
    add("a031_publication_date_claim_absent", not re.search(r"опубликован\w*\s+в\s+2024|дата публикации", text, re.I))
    add("a031_ranking_year_present", "рейтинг производителей за 2024 год" in text)

    bibliography = text.split("## 8. Материалы, использованные в исследовании", 1)[1]
    add("bibliography_count", len(re.findall(r"^\d+\. «", bibliography, re.M)) == 10)
    add("alice_bibliography", "Видимость сайта в Алисе AI" in text and "попадание в ответы Алисы AI" in text)
    add("section_structure", all(f"## {i}." in text for i in range(1, 9)) and "## 9." not in text)

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
