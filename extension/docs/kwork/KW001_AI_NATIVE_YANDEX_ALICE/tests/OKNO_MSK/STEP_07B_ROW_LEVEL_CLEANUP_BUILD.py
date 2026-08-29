#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_SOURCE_ROWS = {
    "S01": 218, "S02": 220, "S03": 144, "S04": 29, "S05": 215, "S06": 218,
    "S07": 19, "S08": 0, "S09": 13, "S10": 192, "S11": 216, "S12": 17,
    "S13": 216, "S14": 217, "S15": 211, "S16": 81, "S17": 49, "S18": 140,
    "P2-01": 217, "P2-02": 216, "P2-03": 21, "P2-04": 96,
}
EXPECTED_INPUT_ROWS = 2965
EXPECTED_SECTION_COUNTS = {"result": 2636, "association": 329}
EXPECTED_UNIQUE = 2840
EXPECTED_DUPLICATE_OCCURRENCES = 125
EXPECTED_STATUS_COUNTS = {
    "KEEP": 1760,
    "REVIEW": 749,
    "EXCLUDE_SCOPE": 180,
    "EXCLUDE_IRRELEVANT": 120,
    "EXCLUDE_MECHANICAL": 31,
}

OUTSIDE_TERMS = [
    "екатеринбург","спб","питер","санкт петербург","санкт-петербург","новосибирск","воронеж","тамбов",
    "волгоград","волгограде","рязань","рязани","самара","красноярск","тула","кострома","смоленск",
    "ростов на дону","ростов-на-дону","донецк","днр","беларусь","беларуси","белоруссии","гомель",
    "омск","орле","орел","махачкала","белгород","иркутск","магнитогорск","комсомольск на амуре",
    "ульяновск","челябинск","курск","тверь","твери","липецк","чебоксары","пенза","анапа","анапе",
    "саратов","симферополь","брянск","архангельске","иваново","уфа","нижний новгород",
    "нижегородской области","нижегородская","волгодонске","нефтекамск","чите","ярославль","луганск",
    "сочи","новомосковск","владимир","калужской области","калуга","саранск","пермь","ставрополь",
    "краснодар","казань","ижевск","тюмень","барнаул","кемерово","томск","мурманск","вологда","оренбург",
    "пензе","одесса","омске","саратове","новосибирске","магнитогорске","ярославле","липецке",
    "челябинске","балабаново","ростов","луганске","тамани","екатеринбурге","тамбове","курске",
    "белгородской области","донецке","башкортостан","тамбова","гомеле","симферополе","владимире",
]
MARKET_SCOPE_TERMS = ["авито","леруа","лемана","озон","валберис","wildberries","мешке","профи ру","мерлен","okna balkona","okon balkona"]
COMPETITOR_NAV_TERMS = ["оконный континент","moonlight","пластиковые окна континент"]

IRRELEVANT_PATTERNS = [
    "багажник","пластиковые двери ваз","накладка на заднюю дверь",
    "фильм француз","короткометраж","французском языке","по французски","перевод на француз",
    "спряжение француз","не открывай окно на француз","на окне сидит",
    "купить квартиру","снять квартиру","квартиры посуточно","снять дом",
    "отель с панорам","гостиница с панорам","отель в москве с панорам","отель панорам",
    "ресторан с панорам","номера с панорам","отдых с панорам","глэмпинг панорама",
    "поезд с панорам","гостиница панорама","панорама на театральном",
    "владимир тяжельников","погода ","дворец бракосочетания","трансфер из",
    "оптика петров","people митинская","жк митинский лес",
    "стоимость ринопластики","какой матрас лучше","как вставить стекло в очки",
    "модальное окно","windows 11","как свернуть все окна","поверх других",
    "расцвела под окошком","над окошком месяц","домик на дереве","пластика ушей",
    "детали очков","авиационный алюминий","сплавы алюминия","как расплавить алюминий","алюминий д16т",
    "прозрачный алюминий","завод пластмасс","пластик и пластмасса","мдф пластик","доска пвх",
    "изделия из пластика","изделия из пвх","пвх ламинат","пластмассовое стекло","ао пластик",
    "теплица из оконных рам","краска для оконных рам","снять с панорамными окнами",
    "одесса французский бульвар 12 выбиты окна",
]
CLEAR_IRRELEVANT_PRODUCT = [
    "робот мойщик","окномойка робот","мойка панорамных окон","кошачий балкончик","балкончик для кошки",
    "наколки на французские окна","французский балкончик для цветов","бочка с панорамным окном",
    "баня бочка с панорамным окном","джакузи панорамные окна",
]
REALESTATE_IRRELEVANT = [
    "жк с панорамными окнами","квартира с панорамными окнами жк","жк в москве с панорамными окнами",
    "купить квартиру с панорамными окнами","новые квартиры с панорамными окнами",
    "квартиры с панорамными окнами в центре","панорамные окна новостройки",
]
MECHANICAL_EXACT = {
    "окн","окнй","пластиковые окна без","пластиковых окон г","пластиковые окна со",
    "где пластиковые окна окно пластиковое","пластиковые окна верхняя","окна пластиковые нижний",
    "пластиковые окна см","1 пластиковые окна","домашних условиях пластиковая окна",
    "пластиковая сторона окна","окна города пластиковые окна","балкон остекление п",
    "остекление балконов г","остекление балконов 1","остекление балконов 2","остекление 5 балконов",
    "пластиковых окна г установка","ли панорамные окна","окно панорамное теплая","окна в рассрочку prsl",
    "продажа окон на рассрочку в новщ","стек пластиковый двери","см двери пластиковые",
    "пластиковое окно под окном","пластиковые окна оконном","пластиковые окна стек",
    "день пластиковых окон","купить пластиковые окна без",
}
ASSOC_IRRELEVANT_EXACT = {
    "окно в париж","окно в европу","вид из окна в ле гра","жалюзийные дверцы","задвижка дверная",
    "дверные жалюзи","смотровое окно","гласс фурнитура","галс мастер фурнитура для стекла",
    "как развернуть окно на весь экран","садовый домик с верандой","пресс рехау","под окном",
}
ASSOC_MECHANICAL_EXACT = {"окн это"}

BOUNDARY_TERMS = [
    "фурнитур","уплотнител","резинк","ручк","петл","замок","защелк","фиксатор","блокиратор","ограничител",
    "гребенк","нащельник","герметик","подоконник","откос","отлив","наличник","штапик","москит","сетка",
    "антикошка","жалюзи","штор","плиссе","смазк","масло","анкер","ролик","редуктор","цапф","накладк",
    "саморез","крепление","конвектор","радиатор","отоплен","теплый пол","мойка","робот мойщик","стекло для",
    "стеклопакет","мягк","поликарбонат","оргстек","гильотин","безрамн","бескаркасн","жидкое остекление",
    "деревянн","дерево алюминиев","краска для алюминиевых","фурниторг","батаре","межкомнат","гармошк",
    "купе","в ванную","в туалет","в комнату","терморазрыв","москитная дверь","навесн","крыш","мансард",
    "решетк","навес","задвижк","книжка","кондиционер","пена ","клинья","жидкий пластик","космофен",
    "ремкомплект","клей для ремонта","средство для ремонта","набор для ремонта","запчасти","шпрос","халва",
    "работа алюминиевые окна","ремонт пластиковых окон работа","окна сок","панорамные окна пик",
    "французской гостиной","пластиковые окна комарова","домашние окна","закроем пластиковые окна",
    "рулонные пластиковые окна","видно pro","vidno pro","французский профиль","перегородка французское окно",
    "французские окна okna","французские окна okon","ограждение панорамных окон","окно панорамный блок",
    "бытовка с панорамными окнами","аксессуар",
]
ASSOC_RELEVANCE_ROOTS = [
    "окн","окон","стеклопак","остекл","балкон","лоджи","веранд","террас","бесед","пвх","rehau","рехау",
    "двер","фурнит","рама","откос","подокон","створк","москит","уплотн","жалюзи","штор","профиль","стекл",
    "форточ","импост","штапик","оконн","застекл",
]

def has_term(text: str, terms: list[str]) -> bool:
    return any(re.search(r"(?<![а-яa-z0-9])" + re.escape(t) + r"(?![а-яa-z0-9])", text) for t in terms)

def outside_geo(text: str) -> bool:
    return has_term(text, OUTSIDE_TERMS)

def used_market(text: str) -> bool:
    return has_term(text, ["бу"]) or "б у" in text or any(t in text for t in MARKET_SCOPE_TERMS)

def source_id_from_name(name: str) -> str:
    m = re.fullmatch(r"STEP_03R_(S\d\d)_RAW_NORMALIZED\.tsv", name)
    if m:
        return m.group(1)
    m = re.fullmatch(r"STEP_05_P2_(\d\d)_RAW_NORMALIZED\.tsv", name)
    if m:
        return f"P2-{m.group(1)}"
    raise AssertionError(f"unexpected input filename: {name}")

def read_rows(path: Path) -> list[dict]:
    source_id = source_id_from_name(path.name)
    out = []
    header_seen = False
    with path.open("r", encoding="utf-8", newline="") as f:
        for raw in f:
            line = raw.rstrip("\n\r")
            if not header_seen:
                if line == "section\tphrase\tcount":
                    header_seen = True
                continue
            if not line:
                continue
            section, phrase, count = line.split("\t")
            if section not in {"result", "association"}:
                raise AssertionError((path.name, section))
            out.append({"source_id": source_id, "section": section, "phrase": phrase.strip().lower(), "count": int(count)})
    if not header_seen:
        raise AssertionError(f"data header missing: {path.name}")
    return out

def classify(phrase: str, occurrences: list[dict]) -> tuple[str, str]:
    s = phrase.lower().strip()
    has_result = any(x["section"] == "result" for x in occurrences)
    if s in MECHANICAL_EXACT or (not has_result and s in ASSOC_MECHANICAL_EXACT):
        return "EXCLUDE_MECHANICAL", "MALFORMED_OR_TRUNCATED"
    if ((not has_result and s in ASSOC_IRRELEVANT_EXACT)
        or any(p in s for p in IRRELEVANT_PATTERNS)
        or any(p in s for p in CLEAR_IRRELEVANT_PRODUCT)
        or any(p in s for p in REALESTATE_IRRELEVANT)):
        return "EXCLUDE_IRRELEVANT", "UNRELATED_INTENT"
    if outside_geo(s):
        return "EXCLUDE_SCOPE", "OUTSIDE_REGION"
    if used_market(s) or any(p in s for p in COMPETITOR_NAV_TERMS):
        return "EXCLUDE_SCOPE", "OTHER_SELLER_OR_USED_MARKET"
    if not has_result:
        if not any(root in s for root in ASSOC_RELEVANCE_ROOTS):
            return "EXCLUDE_IRRELEVANT", "UNRELATED_ASSOCIATION"
        return "REVIEW", "ASSOCIATION_ONLY_NEEDS_VALIDATION"
    if any(t in s for t in BOUNDARY_TERMS):
        return "REVIEW", "BUSINESS_BOUNDARY_NEEDS_SEARCH"
    return "KEEP", "SUPPORTED_WINDOW_OR_GLAZING_TASK"

def write_tsv(path: Path, fieldnames: list[str], rows: list[dict]) -> str:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    inputs = sorted(ROOT.glob("STEP_03R_S??_RAW_NORMALIZED.tsv")) + sorted(ROOT.glob("STEP_05_P2_??_RAW_NORMALIZED.tsv"))
    rows = []
    source_counts = Counter()
    for path in inputs:
        src_rows = read_rows(path)
        rows.extend(src_rows)
        source_counts[source_id_from_name(path.name)] += len(src_rows)

    for source_id, expected in EXPECTED_SOURCE_ROWS.items():
        if source_counts.get(source_id, 0) != expected:
            raise AssertionError(f"{source_id}: got {source_counts.get(source_id, 0)}, expected {expected}")
    unknown_sources = set(source_counts) - set(EXPECTED_SOURCE_ROWS)
    if unknown_sources:
        raise AssertionError(f"unknown sources: {sorted(unknown_sources)}")
    if len(rows) != EXPECTED_INPUT_ROWS:
        raise AssertionError((len(rows), EXPECTED_INPUT_ROWS))

    section_counts = Counter(r["section"] for r in rows)
    if dict(section_counts) != EXPECTED_SECTION_COUNTS:
        raise AssertionError((dict(section_counts), EXPECTED_SECTION_COUNTS))

    by_phrase = defaultdict(list)
    for row in rows:
        by_phrase[row["phrase"]].append(row)
    if len(by_phrase) != EXPECTED_UNIQUE:
        raise AssertionError((len(by_phrase), EXPECTED_UNIQUE))
    if len(rows) - len(by_phrase) != EXPECTED_DUPLICATE_OCCURRENCES:
        raise AssertionError((len(rows) - len(by_phrase), EXPECTED_DUPLICATE_OCCURRENCES))

    decisions = {}
    for phrase, occurrences in by_phrase.items():
        decisions[phrase] = classify(phrase, occurrences)

    status_counts = Counter(status for status, _ in decisions.values())
    if dict(status_counts) != EXPECTED_STATUS_COUNTS:
        raise AssertionError((dict(status_counts), EXPECTED_STATUS_COUNTS))

    working = []
    for phrase in sorted(by_phrase):
        occurrences = by_phrase[phrase]
        status, reason = decisions[phrase]
        results = [x for x in occurrences if x["section"] == "result"]
        associations = [x for x in occurrences if x["section"] == "association"]
        working.append({
            "phrase": phrase,
            "cleanup_status": status,
            "reason_code": reason,
            "source_occurrences": len(occurrences),
            "result_occurrences": len(results),
            "association_occurrences": len(associations),
            "max_result_count": max([x["count"] for x in results] or [0]),
            "max_association_count": max([x["count"] for x in associations] or [0]),
            "source_ids": "|".join(sorted({x["source_id"] for x in occurrences})),
            "provenance": "|".join(f'{x["source_id"]}:{x["section"]}:{x["count"]}' for x in occurrences),
        })
    if sum(r["source_occurrences"] for r in working) != EXPECTED_INPUT_ROWS:
        raise AssertionError("provenance occurrence reconciliation failed")

    occurrences_out = []
    for row in rows:
        status, reason = decisions[row["phrase"]]
        occurrences_out.append({**row, "cleanup_status": status, "reason_code": reason})

    working_path = ROOT / "STEP_07B_ROW_LEVEL_CLEANUP_WORKING.tsv"
    occurrences_path = ROOT / "STEP_07B_ROW_LEVEL_CLEANUP_OCCURRENCES.tsv"
    working_sha = write_tsv(
        working_path,
        ["phrase","cleanup_status","reason_code","source_occurrences","result_occurrences","association_occurrences",
         "max_result_count","max_association_count","source_ids","provenance"],
        working,
    )
    occurrences_sha = write_tsv(
        occurrences_path,
        ["source_id","section","phrase","count","cleanup_status","reason_code"],
        occurrences_out,
    )

    summary = {
        "input_rows": len(rows),
        "result_rows": section_counts["result"],
        "association_rows": section_counts["association"],
        "unique_exact_phrases": len(by_phrase),
        "duplicate_occurrences": len(rows) - len(by_phrase),
        "duplicate_phrase_keys": sum(1 for v in by_phrase.values() if len(v) > 1),
        "status_counts": EXPECTED_STATUS_COUNTS,
        "status_sum": sum(EXPECTED_STATUS_COUNTS.values()),
        "provenance_occurrence_sum": sum(r["source_occurrences"] for r in working),
        "unclassified": 0,
        "provider_requests_executed": 0,
        "provider_cost_rub": 0,
        "working_tsv_sha256": working_sha,
        "occurrences_tsv_sha256": occurrences_sha,
        "source_rows": {k: source_counts.get(k, 0) for k in EXPECTED_SOURCE_ROWS},
        "rules": {
            "exact_dedupe_only": True,
            "low_frequency_exclusion": False,
            "association_auto_keep": False,
            "ambiguous_business_boundary_to_review": True,
        },
    }
    summary_path = ROOT / "STEP_07B_ROW_LEVEL_CLEANUP_SUMMARY.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
