#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILDER = ROOT / "STEP_07C_SEMANTIC_CORRECTION_BUILD.py"

spec = importlib.util.spec_from_file_location("kw001_step07c_builder", BUILDER)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load semantic correction builder")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

_original_positive_for_source = module.positive_for_source
_original_corrected_keep_decision = module.corrected_keep_decision


def positive_for_source_with_russian_window_inflection(text: str, source_id: str) -> bool:
    return _original_positive_for_source(text.replace("окон", "окн"), source_id)


EXTRA_NAVIGATION_RISK = [" сайт", "сайт ", " ru", ".ru", "номер телефона", "номер ремонта", "телефоны"]
EXTRA_TECHNICAL_INFORMATION_RISK = [
    " режим", "режимы", " конструкц", " устройство", "схема", " форум", "можно ли", "разрешение",
    "согласован", "правильная установка", "правильно установить", "после установки", "зазор при установке",
    "инструкция по", "технология установки", "технология монтажа", " поставки", " название", "это какие",
]
EXTRA_COMPONENT_RISK = [
    "панель для", "створк", "профиль для", "комплект для", "направляющ", "ригель", "заглушк", "узлы ",
    "покраск", "сборка", "добор", "пластина для", "анкерная пластина", "стекло для пластиковой двери",
]
HARDWARE_BRAND_RISK = [
    " roto", "рото ", " fapim", "фапим", " aubi", "ауби", " maco", "мако", " siegenia", "зигения",
    " internika", "internica", "интерника", " vorne", "ворне", " winkhaus", "винхаус", " accado",
]
EXTRA_DOOR_AMBIGUITY = [
    "задняя дверь", "металлическая пластиковая", "деревянные пластиковые", "пластиковые навесные двери",
    "пластиковые двери старый", "пластиковая дверь старый",
]
BALCONY_REGULATORY_OR_NEGATION = ["без остекления", "можно ли", "разрешение", "форум", "согласован"]
INSTALLATION_ADJACENT_RISK = [
    "работа установки", "работа по установке", "работа монтаж", "монтажник", "установка пластиковых окон метр",
    "установка пластиковых окон размером", "наружной установки", "день ночь", "установка пластиковых панелей",
    "после установки", "зазор при установке", "правильная установка",
]
STATE_OR_FRAGMENT_RISK = [
    "закрыто", "открытое пластиковое окно", "пластиковое окно внутри", "пластиковое окно снаружи",
    "пластиковые окна район", "окна пластиковые район",
]
PRICE_OR_MATERIAL_AMBIGUITY = ["цены материала", "цена материала", "материалы на пластиковые окна"]
PANORAMIC_REAL_ESTATE_OR_INSPIRATION = [
    "квартира с панорам", "кв с панорам", "студия с панорам", "апартаменты с панорам", "комната с панорам",
    "одноэтажный с панорам", "одноэтажный дом с панорам", "одноэтажные дома с панорам", "каркасный дом с панорам",
    "панорамные окна в каркасном", "панорамные окна в лесу", "панорамные окна лес", "панорамные окна на море",
    "панорамные окна в россии", "панорамные окна в здании", "панорамные окна и потолок", "панорамные окна как называются",
    "баня панорам", "домик с панорам", "дом в лесу с панорам", "треугольный дом с панорам", "барнхаус с панорам",
    "зал с панорам", "кухня гостиная с панорам", "дача с панорам",
]
REPAIR_CONTACT_OR_ENTITY_RISK = ["ремонт пластиковых окон номер", "ремонт пластикового окна номер", "ремонт пластиковых окон телефон", "ремонт пластиковых окон пик"]
REPAIR_FRAGMENT_OR_DIY_RISK = [
    "ремонт пластиковых окон самому", "ремонт пластиковых окон руками", "ремонт пластиковых окон район",
    "ремонт пластиковых окон купить", "ремонт пластиковых окон новых", "ремонт пластиковых окон частный",
]


def any_in(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def corrected_keep_decision_v2(row: dict[str, str]) -> tuple[str, str, str]:
    s = row["phrase"].lower().strip()
    sources = set(x for x in row["source_ids"].split("|") if x)
    if s.endswith(" без"):
        return "EXCLUDE_MECHANICAL", "POST_AUDIT_INCOMPLETE_QUERY_FRAGMENT", "HIGH"
    if any_in(s, EXTRA_NAVIGATION_RISK):
        return "REVIEW", "NAVIGATIONAL_OR_ENTITY_INTENT_NEEDS_VALIDATION", "LOW"
    if any_in(s, EXTRA_TECHNICAL_INFORMATION_RISK):
        return "REVIEW", "TECHNICAL_INFORMATION_INTENT_NEEDS_CONTENT_FIT", "LOW"
    if " или " in s and any(x in sources for x in {"S02", "S11"}):
        return "REVIEW", "COMPARISON_INTENT_NEEDS_SEARCH_VALIDATION", "MEDIUM"
    if s.startswith("демонтаж "):
        return "REVIEW", "DEMOLITION_SERVICE_BOUNDARY_NEEDS_VALIDATION", "MEDIUM"
    if any_in(s, EXTRA_COMPONENT_RISK):
        return "REVIEW", "COMPONENT_OR_ACCESSORY_INTENT_NEEDS_BUSINESS_FIT", "MEDIUM"
    if any_in(s, HARDWARE_BRAND_RISK):
        return "REVIEW", "HARDWARE_BRAND_INTENT_NEEDS_BUSINESS_FIT", "MEDIUM"
    if "S05" in sources and any_in(s, EXTRA_DOOR_AMBIGUITY):
        return "REVIEW", "PVC_DOOR_SUBTYPE_BUSINESS_FIT_NEEDS_VALIDATION", "MEDIUM"
    if ("S06" in sources or "S07" in sources) and any_in(s, BALCONY_REGULATORY_OR_NEGATION):
        return "REVIEW", "BALCONY_REGULATORY_OR_NEGATED_INTENT_NEEDS_SEARCH", "MEDIUM"
    if "S13" in sources and any_in(s, INSTALLATION_ADJACENT_RISK):
        return "REVIEW", "INSTALLATION_ADJACENT_OR_JOB_INTENT_NEEDS_VALIDATION", "MEDIUM"
    if "S14" in sources and any_in(s, REPAIR_CONTACT_OR_ENTITY_RISK):
        return "REVIEW", "REPAIR_NAVIGATIONAL_OR_ENTITY_INTENT_NEEDS_VALIDATION", "LOW"
    if "S14" in sources and any_in(s, REPAIR_FRAGMENT_OR_DIY_RISK):
        return "REVIEW", "REPAIR_FRAGMENT_OR_DIY_INTENT_NEEDS_VALIDATION", "LOW"
    if any_in(s, STATE_OR_FRAGMENT_RISK):
        return "REVIEW", "STATE_OR_CONTEXT_FRAGMENT_NEEDS_VALIDATION", "LOW"
    if any_in(s, PRICE_OR_MATERIAL_AMBIGUITY):
        return "REVIEW", "MATERIAL_OR_PRICE_CONTEXT_NEEDS_VALIDATION", "LOW"
    if "P2-02" in sources and any_in(s, PANORAMIC_REAL_ESTATE_OR_INSPIRATION):
        return "REVIEW", "PANORAMIC_REAL_ESTATE_OR_INSPIRATION_INTENT_NEEDS_SEARCH", "MEDIUM"
    return _original_corrected_keep_decision(row)


module.positive_for_source = positive_for_source_with_russian_window_inflection
module.corrected_keep_decision = corrected_keep_decision_v2
module.main()

working_path = ROOT / "STEP_07C_SEMANTIC_CORRECTION_WORKING.tsv"
with working_path.open("r", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f, delimiter="\t"))
by_phrase = {r["phrase"]: r for r in rows}

must_not_keep = {
    "rehau окна режимы", "rehau окно конструкция", "окна rehau сайт", "окна rehau ru", "окно rehau roto",
    "алюминиевые окна fapim", "панель для пластиковой двери", "балкон без остекления",
    "разрешение на остекление балкона", "остекления балкона форум", "правильная установка пластиковых окон",
    "после установки пластиковых окон", "окно пластиковое закрыто", "открытое пластиковое окно",
    "окна в рассрочку без", "пластиковое окно в рассрочку без", "квартира с панорамными окнами",
    "студия с панорамными окнами", "апартаменты с панорамными окнами", "панорамные окна в россии",
    "панорамные окна в здании", "панорамные окна лес", "панорамные окна на море", "панорамные окна как называются",
    "как сейчас выглядят поставки окон rehau", "какие окна лучше веко или rehau",
    "какие окна лучше пластиковые или алюминиевые", "демонтаж алюминиевых окон", "демонтаж остекления балкона",
    "ремонт пластиковых окон самому", "ремонт пластиковых окон руками закрывается", "ремонт пластиковых окон район",
    "ремонт пластиковых окон купить", "ремонт пластиковых окон новых", "ремонт пластиковых окон частный",
    "французские окна название", "французские окна это какие", "дача с панорамными окнами",
}

must_keep = {
    "пластиковые окна", "пластиковые окна москва", "пластиковые окна цена", "окна rehau", "остекление балкона",
    "остекление балкона цена", "остекление веранды", "алюминиевые окна", "алюминиевые окна москва",
    "установка пластиковых окон", "ремонт пластиковых окон", "цены на пластиковые окна", "окна в рассрочку",
    "пластиковые окна от производителя", "панорамные окна", "панорамные окна купить", "панорамные окна цена",
    "панорамные окна москва", "панорамные окна для загородного дома", "панорамные окна на террасу",
    "окна для частного дома", "пластиковые двери", "французские окна", "французские окна купить",
    "какие пластиковые окна лучше", "как правильно выбрать пластиковые окна",
}

qa_rows: list[dict[str, str]] = []
failures: list[str] = []
for phrase in sorted(must_not_keep | must_keep):
    row = by_phrase.get(phrase)
    expected = "MUST_NOT_KEEP" if phrase in must_not_keep else "MUST_KEEP"
    if row is None:
        failures.append(f"QA phrase missing: {phrase}")
        qa_rows.append({"phrase": phrase, "expectation": expected, "corrected_status": "MISSING", "corrected_reason": "", "qa_result": "FAIL"})
        continue
    status = row["corrected_status"]
    ok = (status != "KEEP") if phrase in must_not_keep else (status == "KEEP")
    if not ok:
        failures.append(f"{expected}: {phrase} -> {status} / {row['corrected_reason']}")
    qa_rows.append({"phrase": phrase, "expectation": expected, "corrected_status": status, "corrected_reason": row["corrected_reason"], "qa_result": "PASS" if ok else "FAIL"})

qa2_path = ROOT / "STEP_07C_SEMANTIC_QA_CASES_V2.tsv"
with qa2_path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["phrase", "expectation", "corrected_status", "corrected_reason", "qa_result"], delimiter="\t", lineterminator="\n")
    writer.writeheader(); writer.writerows(qa_rows)

summary_path = ROOT / "STEP_07C_SEMANTIC_CORRECTION_SUMMARY.json"
summary = json.loads(summary_path.read_text(encoding="utf-8"))
summary["second_semantic_qa_case_count"] = len(qa_rows)
summary["second_semantic_qa_failures"] = len(failures)
summary["second_semantic_qa_tsv_sha256"] = hashlib.sha256(qa2_path.read_bytes()).hexdigest()
summary["manual_semantic_saturation_passes"] = 3
summary["candidate_status"] = "SEMANTIC_SATURATION_CANDIDATE_OWNER_REVIEW_PENDING" if not failures else "SECOND_SEMANTIC_QA_FAILED"
summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if failures:
    raise AssertionError("; ".join(failures))
