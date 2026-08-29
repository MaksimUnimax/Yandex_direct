#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT_WORKING = ROOT / "STEP_07B_ROW_LEVEL_CLEANUP_WORKING.tsv"
INPUT_OCCURRENCES = ROOT / "STEP_07B_ROW_LEVEL_CLEANUP_OCCURRENCES.tsv"
EXPECTED_PHRASES = 2840
EXPECTED_OCCURRENCES = 2965

# Step-01 site/business evidence used as the positive-relevance frame:
# PVC / REHAU windows; PVC doors; balcony/loggia glazing;
# veranda/gazebo/terrace glazing; aluminium glazing;
# measurement/calculation/order conversion; installation/repair/finance;
# existing information guide and production/trust branches.

NEW_MECHANICAL_EXACT = {
    "1 установка пластиковых окон",
}

NAVIGATION_RISK = [
    "официальный сайт", "официальный москва", "официальный дилер", "официальные партнеры",
    "официальные партнёры", "дилеры", "дилер ", "партнеры производителя", "партнёры производителя",
    "адрес", "телефон", "офис ", "анадырский проезд", "рядом",
]

DIY_RISK = [
    "своими руками", "самостоятельно", "самому ", "пошаг", "инструкция", "видео",
    "как установить", "как снять", "как открыть", "как закрыть", "как отрегулировать", "как регулировать",
    "как сделать", "как вставить", "как поменять", "как заменить", "как вытащить", "как крепить",
    "как крепятся", "как починить", "домашних условиях",
]

VAGUE_INFORMATION_RISK = [
    "что значит", "что такое", "как называется", "почему ", "суть ", "как выглядит",
]

COMPONENT_RISK = [
    "микролифт", "фурнитур", "уплотнител", "резинк", "ручк", "петл", "замок", "защелк", "защёлк",
    "фиксатор", "блокиратор", "ограничител", "гребенк", "нащельник", "герметик", "подоконник", "откос",
    "отлив", "наличник", "штапик", "москит", "сетка", "антикошка", "жалюзи", "штор", "плиссе",
    "смазк", "масло", "анкер", "ролик", "редуктор", "цапф", "накладк", "саморез", "крепление",
    "клапан", "механизм", "ремкомплект", "запчаст", "клей для ремонта", "средство для ремонта",
]

HEATING_OR_ADJACENT_RISK = [
    "конвектор", "радиатор", "батаре", "отоплен", "теплый пол", "тёплый пол", "кондиционер",
]

DESIGN_RISK = [
    "интерьер", "дизайн", "проект ", "проекты ", "фото", "красив", "спальн", "гостин", "лофт",
]

PANORAMIC_ARCHITECTURE_RISK = [
    "дом с панорам", "одноэтажный дом", "одноэтажные дома", "каркасный дом", "современный дом",
    "проекты домов", "проект одноэтажного дома", "треугольный дом", "барнхаус", "домик в лесу",
    "дом в лесу", "кухня гостиная", "кухня с большим панорамным", "зал с панорам", "бассейн с панорам",
    "баня с панорам", "дом баня", "беседка с барбекю", "терраса с панорамными окнами фото",
]

DOOR_BOUNDARY_RISK = [
    "межкомнат", "в ванную", "в туалет", "в комнату", "гармошк", "купе", "терморазрыв",
]

PRIVATE_HOUSE_BOUNDARY_RISK = [
    "котельн", "газовой котельной", "требования", "площадь окна", "сануз", "ванн", "вентиляц",
    "окна для крыши", "крыльцо", "проем", "проём",
]

REPAIR_AMBIGUITY_RISK = [
    "ремонт квартиры", "чем отмыть", "очистить пластиковые окна", "после ремонта", "средство для ремонта",
]

COMPARISON_RISK = [
    "veka или rehau", "rehau или veka", "kbe или rehau", "rehau kbe", "melke и rehau",
    "сравнение окон rehau и kaleva", "пластиковые или алюминиевые окна", "пластиковые и алюминиевые окна",
    "какие окна пластиковые или алюминиевые", "что лучше пластиковые или алюминиевые",
]

CORE_SOURCE_REASON = {
    "S01": "POSITIVE_CORE_PVC_WINDOW_INTENT",
    "S02": "POSITIVE_CORE_REHAU_WINDOW_INTENT",
    "S03": "POSITIVE_CORE_FRENCH_WINDOW_INTENT",
    "S04": "POSITIVE_CORE_HOUSE_SERIES_WINDOW_INTENT",
    "S05": "POSITIVE_CORE_PVC_DOOR_INTENT",
    "S06": "POSITIVE_CORE_BALCONY_GLAZING_INTENT",
    "S07": "POSITIVE_CORE_BALCONY_ROOF_GLAZING_INTENT",
    "S09": "POSITIVE_CORE_GEO_WINDOW_INTENT",
    "S10": "POSITIVE_CORE_VERANDA_GLAZING_INTENT",
    "S11": "POSITIVE_CORE_ALUMINIUM_WINDOW_INTENT",
    "S13": "POSITIVE_CORE_INSTALLATION_SERVICE_INTENT",
    "S14": "POSITIVE_CORE_REPAIR_SERVICE_INTENT",
    "S15": "POSITIVE_CORE_PRICE_COMMERCIAL_INTENT",
    "S16": "POSITIVE_CORE_FINANCE_COMMERCIAL_INTENT",
    "S17": "POSITIVE_EXISTING_WINDOW_SELECTION_GUIDE_INTENT",
    "S18": "POSITIVE_PRODUCTION_OR_MANUFACTURER_INTENT",
    "P2-02": "POSITIVE_CORE_PANORAMIC_WINDOW_INTENT",
    "P2-03": "POSITIVE_CORE_BALCONY_EXTENSION_GLAZING_INTENT",
    "P2-04": "POSITIVE_CORE_PRIVATE_HOUSE_WINDOW_INTENT",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_tsv(path: Path, fields: list[str], rows: list[dict]) -> str:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return sha256(path)


def any_in(s: str, terms: list[str]) -> bool:
    return any(t in s for t in terms)


def has_token(s: str, token: str) -> bool:
    return re.search(r"(?<![а-яa-z0-9])" + re.escape(token) + r"(?![а-яa-z0-9])", s) is not None


def numeric_or_fragment_risk(s: str) -> bool:
    if re.search(r"^\d+\s+\d+\s+", s):
        return True
    if re.search(r"\b(?:окна|окно|двери|дверь)\s+[123]$", s):
        return True
    if re.search(r"\b\d+\s*$", s) and not re.search(r"(?:п\s*44|п44|\d+[хx]\s*камер|\d+\s*мм|\d+x\d+|\d+х\d+)", s):
        return True
    return False


def positive_for_source(s: str, src: str) -> bool:
    if src == "S01":
        return (("пластиков" in s and "окн" in s) or ("окна пвх" in s) or ("окно пвх" in s))
    if src == "S02":
        return (("rehau" in s or "рехау" in s) and "окн" in s)
    if src == "S03":
        return ("француз" in s and ("окн" in s or "остекл" in s or "балкон" in s))
    if src == "S04":
        return (("п 44" in s or "п44" in s) and ("окн" in s or "дом" in s))
    if src == "S05":
        return (("пластиков" in s and "двер" in s) or ("двер" in s and "пвх" in s))
    if src == "S06":
        return (("остекл" in s and ("балкон" in s or "лоджи" in s)) or ("балкон" in s and "окн" in s))
    if src == "S07":
        return ("балкон" in s and "крыш" in s and "остекл" in s)
    if src == "S09":
        return ("митино" in s and "пластиков" in s and "окн" in s)
    if src == "S10":
        return ("остекл" in s and ("веранд" in s or "террас" in s or "бесед" in s))
    if src == "S11":
        return ("алюминиев" in s and ("окн" in s or "остекл" in s))
    if src == "S13":
        return (("установ" in s or "монтаж" in s) and "окн" in s and ("пластиков" in s or "пвх" in s)) or ("пластиков" in s and "окн" in s and "с установ" in s)
    if src == "S14":
        return (("ремонт" in s or "обслужив" in s or "сервис" in s) and "пластиков" in s and "окн" in s)
    if src == "S15":
        return (("цен" in s or "стоим" in s or "рассчитать" in s or "калькулятор" in s) and "пластиков" in s and "окн" in s)
    if src == "S16":
        return ("рассроч" in s and ("окн" in s or "балкон" in s))
    if src == "S17":
        return (("выбрать" in s or "выбор" in s) and "пластиков" in s and "окн" in s)
    if src == "S18":
        return (("производител" in s or "производств" in s or "завод" in s) and "пластиков" in s and "окн" in s)
    if src == "P2-02":
        return ("панорам" in s and ("окн" in s or "остекл" in s))
    if src == "P2-03":
        return ("остекл" in s and "балкон" in s and "вынос" in s)
    if src == "P2-04":
        return ("окн" in s and ("частн" in s or "загород" in s))
    return False


def corrected_keep_decision(row: dict[str, str]) -> tuple[str, str, str]:
    s = row["phrase"].lower().strip()
    sources = [x for x in row["source_ids"].split("|") if x]

    if s in NEW_MECHANICAL_EXACT:
        return "EXCLUDE_MECHANICAL", "POST_AUDIT_MALFORMED_OR_FRAGMENT", "HIGH"

    if numeric_or_fragment_risk(s):
        return "REVIEW", "AMBIGUOUS_NUMERIC_OR_FRAGMENT_INTENT", "LOW"

    if any_in(s, NAVIGATION_RISK) or re.search(r"\b(?:ул|улица|проезд)\b", s) or re.search(r"\bд\s*\d+\b", s):
        return "REVIEW", "NAVIGATIONAL_OR_ENTITY_INTENT_NEEDS_VALIDATION", "LOW"

    if any_in(s, DIY_RISK):
        return "REVIEW", "DIY_OR_PROCEDURAL_INTENT_NEEDS_CONTENT_FIT", "LOW"

    if any_in(s, VAGUE_INFORMATION_RISK):
        return "REVIEW", "VAGUE_INFORMATIONAL_INTENT_NEEDS_VALIDATION", "LOW"

    if any_in(s, COMPARISON_RISK):
        return "REVIEW", "COMPARISON_INTENT_NEEDS_SEARCH_VALIDATION", "MEDIUM"

    if any_in(s, COMPONENT_RISK):
        # Rehau profile-model demand is a proven site family; don't demote generic profile-model queries merely for 'profile'.
        return "REVIEW", "COMPONENT_OR_ACCESSORY_INTENT_NEEDS_BUSINESS_FIT", "MEDIUM"

    if any_in(s, HEATING_OR_ADJACENT_RISK):
        return "REVIEW", "ADJACENT_SYSTEM_INTENT_NEEDS_BUSINESS_FIT", "LOW"

    if "P2-02" in sources and any_in(s, PANORAMIC_ARCHITECTURE_RISK):
        return "REVIEW", "ARCHITECTURE_OR_INSPIRATION_INTENT_NEEDS_SEARCH", "MEDIUM"

    if ("P2-02" in sources or "S03" in sources or "S10" in sources) and any_in(s, DESIGN_RISK):
        return "REVIEW", "DESIGN_OR_INSPIRATION_INTENT_NEEDS_SEARCH", "MEDIUM"

    if "S05" in sources and any_in(s, DOOR_BOUNDARY_RISK):
        return "REVIEW", "PVC_DOOR_SUBTYPE_BUSINESS_FIT_NEEDS_VALIDATION", "MEDIUM"

    if "P2-04" in sources and any_in(s, PRIVATE_HOUSE_BOUNDARY_RISK):
        return "REVIEW", "PRIVATE_HOUSE_ADJACENT_TASK_NEEDS_VALIDATION", "MEDIUM"

    if "S14" in sources and any_in(s, REPAIR_AMBIGUITY_RISK):
        return "REVIEW", "REPAIR_ADJACENT_INFORMATION_INTENT_NEEDS_VALIDATION", "MEDIUM"

    # Generic design/photo terms are allowed to remain only when another source gives a direct commercial/service reading.
    if any_in(s, DESIGN_RISK) and not any(src in {"S15", "S18"} for src in sources):
        return "REVIEW", "DESIGN_OR_INSPIRATION_INTENT_NEEDS_SEARCH", "MEDIUM"

    positives = [src for src in sources if positive_for_source(s, src)]
    if positives:
        # Prefer the first deterministic source reason, but preserve every source in the row itself.
        reason = CORE_SOURCE_REASON.get(positives[0], "POSITIVE_SUPPORTED_SITE_BUSINESS_INTENT")
        return "KEEP", reason, "HIGH"

    return "REVIEW", "POSITIVE_RELEVANCE_NOT_ESTABLISHED", "LOW"


def corrected_decision(row: dict[str, str]) -> tuple[str, str, str]:
    old_status = row["cleanup_status"]
    old_reason = row["reason_code"]
    if old_status != "KEEP":
        confidence = "HIGH" if old_status.startswith("EXCLUDE_") else "MEDIUM"
        return old_status, f"RETAINED_{old_reason}", confidence
    return corrected_keep_decision(row)


def tokenize(s: str) -> list[str]:
    s = s.lower().replace("ё", "е").replace("рехау", "rehau").replace("проведал", "provedal")
    return re.findall(r"[а-яa-z0-9]+", s)


def light_stem(token: str) -> str:
    if len(token) <= 4 or token.isdigit():
        return token
    suffixes = (
        "иями", "ями", "ами", "ого", "его", "ыми", "ими", "ому", "ему", "ой", "ей", "ий", "ый", "ая", "яя",
        "ое", "ее", "ые", "ие", "ов", "ев", "ам", "ям", "ах", "ях", "ом", "ем", "ую", "юю", "ы", "и", "а", "я", "у", "ю", "е", "о",
    )
    for suf in suffixes:
        if token.endswith(suf) and len(token) - len(suf) >= 4:
            return token[:-len(suf)]
    return token


def signature(tokens: list[str], stem: bool) -> str:
    if stem:
        tokens = [light_stem(t) for t in tokens]
    return " ".join(sorted(tokens))


def duplicate_candidates(corrected_rows: list[dict]) -> list[dict]:
    eligible = [r for r in corrected_rows if r["corrected_status"] in {"KEEP", "REVIEW"}]
    strict = defaultdict(list)
    loose = defaultdict(list)
    for r in eligible:
        toks = tokenize(r["phrase"])
        if len(toks) < 2:
            continue
        strict[signature(toks, False)].append(r)
        loose[signature(toks, True)].append(r)

    out = []
    strict_phrases = set()
    gid = 0
    for sig, rows in sorted(strict.items()):
        uniq = {r["phrase"] for r in rows}
        if len(uniq) < 2 or len(uniq) > 12:
            continue
        gid += 1
        strict_phrases.update(uniq)
        for r in sorted(rows, key=lambda x: x["phrase"]):
            out.append({
                "candidate_group": f"DUP-{gid:04d}", "method": "STRICT_ORDERLESS_TOKEN_BAG", "signature": sig,
                "group_size": len(uniq), "phrase": r["phrase"], "corrected_status": r["corrected_status"],
                "corrected_reason": r["corrected_reason"], "source_ids": r["source_ids"],
            })

    for sig, rows in sorted(loose.items()):
        uniq = {r["phrase"] for r in rows}
        if len(uniq) < 2 or len(uniq) > 8:
            continue
        if uniq.issubset(strict_phrases):
            continue
        gid += 1
        for r in sorted(rows, key=lambda x: x["phrase"]):
            out.append({
                "candidate_group": f"DUP-{gid:04d}", "method": "LIGHT_STEM_ORDERLESS_CANDIDATE", "signature": sig,
                "group_size": len(uniq), "phrase": r["phrase"], "corrected_status": r["corrected_status"],
                "corrected_reason": r["corrected_reason"], "source_ids": r["source_ids"],
            })
    return out


def main() -> None:
    working = read_tsv(INPUT_WORKING)
    occurrences = read_tsv(INPUT_OCCURRENCES)
    if len(working) != EXPECTED_PHRASES:
        raise AssertionError((len(working), EXPECTED_PHRASES))
    if len(occurrences) != EXPECTED_OCCURRENCES:
        raise AssertionError((len(occurrences), EXPECTED_OCCURRENCES))

    corrected = []
    decisions = {}
    transitions = Counter()
    for row in working:
        status, reason, confidence = corrected_decision(row)
        decisions[row["phrase"]] = (status, reason, confidence)
        transitions[(row["cleanup_status"], status)] += 1
        corrected.append({
            **row,
            "historical_status": row["cleanup_status"],
            "historical_reason": row["reason_code"],
            "corrected_status": status,
            "corrected_reason": reason,
            "semantic_confidence": confidence,
        })

    # No historical non-KEEP row may be silently promoted in this conservative correction.
    for r in corrected:
        if r["historical_status"] != "KEEP" and r["corrected_status"] == "KEEP":
            raise AssertionError(f"forbidden promotion: {r['phrase']}")
        if r["corrected_status"] == "KEEP" and not r["corrected_reason"].startswith("POSITIVE_"):
            raise AssertionError(f"KEEP without positive evidence: {r['phrase']} {r['corrected_reason']}")

    known_bad = {
        "1 установка пластиковых окон",
        "6 6 с панорамными окнами",
        "rehau окна 2",
        "алюминиевые окна 2",
        "rehau окна анадырский проезд д 47",
        "rehau микролифт для окна",
    }
    for phrase in known_bad:
        if phrase not in decisions:
            raise AssertionError(f"QA phrase missing: {phrase}")
        if decisions[phrase][0] == "KEEP":
            raise AssertionError(f"known false-KEEP survived: {phrase}")

    known_good = {
        "пластиковые окна", "пластиковые окна москва", "установка пластиковых окон",
        "ремонт пластиковых окон", "остекление балкона", "остекление веранды", "алюминиевые окна",
        "окна rehau", "окна в рассрочку", "пластиковые окна от производителя", "панорамные окна",
        "окна для частного дома", "окно п 44", "пластиковые двери", "как выбрать пластиковые окна",
    }
    for phrase in known_good:
        if phrase not in decisions:
            raise AssertionError(f"positive QA phrase missing: {phrase}")
        if decisions[phrase][0] != "KEEP":
            raise AssertionError(f"known supported phrase not KEEP: {phrase} -> {decisions[phrase]}")

    corrected_status_counts = Counter(r["corrected_status"] for r in corrected)
    if sum(corrected_status_counts.values()) != EXPECTED_PHRASES:
        raise AssertionError("corrected status reconciliation failed")

    occ_out = []
    for row in occurrences:
        status, reason, confidence = decisions[row["phrase"]]
        occ_out.append({
            **row,
            "historical_status": row["cleanup_status"],
            "historical_reason": row["reason_code"],
            "corrected_status": status,
            "corrected_reason": reason,
            "semantic_confidence": confidence,
        })
    if len(occ_out) != EXPECTED_OCCURRENCES:
        raise AssertionError("occurrence reconciliation failed")

    candidate_rows = duplicate_candidates(corrected)

    working_path = ROOT / "STEP_07C_SEMANTIC_CORRECTION_WORKING.tsv"
    occ_path = ROOT / "STEP_07C_SEMANTIC_CORRECTION_OCCURRENCES.tsv"
    dup_path = ROOT / "STEP_07C_NONEXACT_DUPLICATE_CANDIDATES.tsv"
    qa_path = ROOT / "STEP_07C_SEMANTIC_QA_CASES.tsv"

    working_fields = [
        "phrase", "historical_status", "historical_reason", "corrected_status", "corrected_reason", "semantic_confidence",
        "source_occurrences", "result_occurrences", "association_occurrences", "max_result_count", "max_association_count",
        "source_ids", "provenance",
    ]
    working_sha = write_tsv(working_path, working_fields, corrected)

    occ_fields = [
        "source_id", "section", "phrase", "count", "historical_status", "historical_reason",
        "corrected_status", "corrected_reason", "semantic_confidence",
    ]
    occ_sha = write_tsv(occ_path, occ_fields, occ_out)

    dup_fields = ["candidate_group", "method", "signature", "group_size", "phrase", "corrected_status", "corrected_reason", "source_ids"]
    dup_sha = write_tsv(dup_path, dup_fields, candidate_rows)

    qa_phrases = sorted(known_bad | known_good)
    qa_rows = []
    old_by_phrase = {r["phrase"]: r for r in working}
    for phrase in qa_phrases:
        status, reason, confidence = decisions[phrase]
        qa_rows.append({
            "phrase": phrase,
            "historical_status": old_by_phrase[phrase]["cleanup_status"],
            "corrected_status": status,
            "corrected_reason": reason,
            "semantic_confidence": confidence,
            "qa_expectation": "MUST_NOT_KEEP" if phrase in known_bad else "MUST_KEEP",
            "qa_result": "PASS",
        })
    qa_sha = write_tsv(qa_path, ["phrase","historical_status","corrected_status","corrected_reason","semantic_confidence","qa_expectation","qa_result"], qa_rows)

    reason_counts = Counter(r["corrected_reason"] for r in corrected)
    transition_rows = {f"{a}->{b}": n for (a, b), n in sorted(transitions.items())}
    duplicate_group_count = len({r["candidate_group"] for r in candidate_rows})

    summary = {
        "source_occurrences": EXPECTED_OCCURRENCES,
        "exact_phrase_keys": EXPECTED_PHRASES,
        "historical_status_counts": dict(Counter(r["cleanup_status"] for r in working)),
        "corrected_status_counts": dict(corrected_status_counts),
        "status_transitions": transition_rows,
        "corrected_reason_counts": dict(sorted(reason_counts.items())),
        "historical_keep_rechecked": sum(1 for r in working if r["cleanup_status"] == "KEEP"),
        "historical_keep_retained": transitions[("KEEP", "KEEP")],
        "historical_keep_downgraded_to_review": transitions[("KEEP", "REVIEW")],
        "historical_keep_changed_to_exclude_mechanical": transitions[("KEEP", "EXCLUDE_MECHANICAL")],
        "historical_nonkeep_promoted_to_keep": 0,
        "keep_requires_positive_reason": True,
        "default_keep_fallthrough": False,
        "low_frequency_exclusion": False,
        "association_auto_keep": False,
        "provider_requests_executed": 0,
        "provider_cost_rub": 0,
        "nonexact_duplicate_candidate_groups": duplicate_group_count,
        "nonexact_duplicate_candidate_rows": len(candidate_rows),
        "nonexact_duplicates_auto_merged": 0,
        "qa_case_count": len(qa_rows),
        "qa_failures": 0,
        "working_tsv_sha256": working_sha,
        "occurrences_tsv_sha256": occ_sha,
        "duplicate_candidates_tsv_sha256": dup_sha,
        "qa_cases_tsv_sha256": qa_sha,
        "candidate_status": "GENERATED_FOR_POST_AUDIT_REVIEW_NOT_ACCEPTED_AS_FINAL",
    }
    summary_path = ROOT / "STEP_07C_SEMANTIC_CORRECTION_SUMMARY.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
