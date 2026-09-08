#!/usr/bin/env python3
"""Build deterministic Step 5A.5 Wordstat reconciliation artifacts.

The fourteen persisted raw provider envelopes are immutable inputs.  This
builder never calls a provider and never fabricates rows from totalCount.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


OUT = Path(__file__).resolve().parent
JOB = OUT.parent
WORDSTAT_PACKAGE = OUT / "STEP_05A_WORDSTAT_REQUIREMENT_PACKAGE.tsv"
SEED_DECISIONS = OUT / "STEP_05A_SEED_DECISIONS.json"
PAGE_EVIDENCE = OUT / "STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv"
FINAL_MASTER = JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"
UNIT_AUTHORITY = JOB / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"

ACQUISITION = OUT / "STEP_05A_WORDSTAT_SEED_ACQUISITION_LEDGER.tsv"
RETURNED = OUT / "STEP_05A_WORDSTAT_RETURNED_PHRASE_LEDGER.tsv"
RECONCILIATION = OUT / "STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv"
SEARCH_PACKAGE = OUT / "STEP_05A_SEARCH_RECHECK_REQUIREMENT_PACKAGE.tsv"
REPORT = OUT / "STEP_05A_WORDSTAT_RECONCILIATION_REPORT.md"
LOG = OUT / "STEP_05A_WORDSTAT_RECONCILIATION_EXECUTION_LOG.md"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def normalize(text: str) -> str:
    return " ".join(re.sub(r"[^a-zа-яё0-9]+", " ", text.casefold()).split())


def raw_path(order: int) -> Path:
    return OUT / f"STEP_05A_WORDSTAT_ITEM_{order:02d}_RAW.json"


def provider_shape(result: dict[str, object]) -> str:
    if not result:
        return "EMPTY_PROVIDER_RESULT"
    has_results = isinstance(result.get("results"), list) and bool(result["results"])
    has_associations = isinstance(result.get("associations"), list) and bool(result["associations"])
    has_total = "totalCount" in result
    if has_results and has_associations and has_total:
        return "RESULT_ROWS_ASSOCIATIONS_TOTALCOUNT"
    if has_results and has_total:
        return "RESULT_ROWS_TOTALCOUNT"
    if has_total and not has_results and not has_associations:
        return "TOTALCOUNT_ONLY"
    return "OTHER_EXPLICIT_PROVIDER_SHAPE"


NEW_DIRECTION_BY_SEED = {
    3: "OPEN_BALCONY_WATERPROOFING",
    4: "SUN_PROTECTION_GLASS_UNIT",
    5: "MULTIFUNCTIONAL_GLASS_UNIT",
    6: "IMPACT_RESISTANT_GLASS_UNIT",
    10: "BALCONY_AS_OFFICE",
    11: "BALCONY_AS_STORAGE",
    13: "BALCONY_ROOF_SOUNDPROOFING",
    14: "WINDOW_PROFILE_REINFORCEMENT",
}

HOLD_PHRASES = {
    "солнцезащитная пленка на стеклопакеты": "Отдельный плёночный продукт не равен стеклопакету; предложение клиента не подтверждено.",
    "ролеты на окна": "Ассоциация указывает на отдельный товар; подтверждённой бизнес-границы для него нет.",
    "пленка на окна от посторонних глаз": "Отдельный плёночный продукт требует бизнес-проверки и не следует из исходной страницы конкурента.",
    "балконный погребок": "Ассоциация описывает конструктивно иной сценарий, не подтверждённый страницей-источником «балкон-кладовая».",
    "армированное стекло": "Материал неоднозначен относительно услуги и отличается от армирования оконного профиля.",
    "металлические ставни на окна": "Отдельный продукт не подтверждён бизнес-правдой клиента.",
}

OFF_SCOPE_PHRASES = {
    "пена монтажная водостойкая для герметизации кровли",
    "герметик по бетону для швов влагостойкий морозостойкий",
    "купить кладовку",
    "аренда кладовки",
    "офисные шкафы",
    "сейф офисный",
    "ящик балконный",
    "катепал мягкая кровля",
    "гвозди для мягкой черепицы",
    "кровельный поликарбонат",
    "костыль кровельный",
    "мягкая кровля на стены под кирпич",
    "кровельная гидроизоляция",
    "коньковый аэратор для мягкой кровли",
    "саморезы для мягкой кровли",
    "полиуретановая гидроизоляция для кровли",
    "купить битум для кровли гаража",
    "кровельная гидроизоляция рулонная",
    "кровельные гвозди для мягкой кровли",
    "кровельная черепица",
    "битумная мастика для кровли гаража",
    "гидроизоляция для кровли под металлочерепицу",
    "гвозди для кровли",
    "купить карнизную планку для мягкой кровли",
    "монтаж мягкой кровли на стену",
    "битумный праймер для кровли гаража",
}

ALREADY_CLOSE_UNITS = {
    "защелка для балконной двери": "unit:AFTERMARKET_WINDOW_HARDWARE_SHOPPING_UNSUPPORTED",
    "балконная защелка": "unit:AFTERMARKET_WINDOW_HARDWARE_SHOPPING_UNSUPPORTED",
    "как открыть балконную дверь": "unit:PVC_DOOR_OPERATION_ADJUSTMENT_DIY_INFO",
    "балконная дверь не закрывается плотно что делать": "unit:WINDOW_REPAIR_SERVICE",
    "ограничитель открытия окна": "unit:AFTERMARKET_WINDOW_HARDWARE_SHOPPING_UNSUPPORTED",
    "пластиковые окна": "unit:PVC_WINDOWS_COMMERCIAL",
    "жалюзи на окна": "unit:WINDOW_BLINDS_SHOPPING_SELECTION",
    "окна": "unit:WINDOWS_COMMERCIAL_GENERAL",
    "остекление": "unit:WINDOWS_COMMERCIAL_GENERAL",
    "атермальное остекление": "phrase:атермальное остекление",
    "окна пвх": "phrase:окна пвх",
    "оконный профиль": "unit:WINDOW_PROFILE_SELECTION_INFO",
    "атермальное остекление что это": "phrase:атермальное остекление",
    "остекление окон": "unit:WINDOWS_COMMERCIAL_GENERAL",
    "створка": "unit:PVC_WINDOW_OPERATION_DIY",
    "балконный блок пластиковые окна": "phrase:балконный блок пластиковые окна",
    "псул для пластиковых окон для чего нужен": "unit:WINDOW_INSTALLATION_MATERIALS_INFO",
    "импост в окне что это": "phrase:импост в окне что это",
    "виды пластиковых окон": "unit:PVC_WINDOWS_COMMERCIAL",
    "антикошка на окна что это": "phrase:антикошка на пластиковые окна",
    "противоударная пленка на окна": "phrase:бронепленка на стеклопакет",
    "балконный блок цена": "unit:PVC_BALCONY_DOORS_COMMERCIAL",
    "жалюзи на балконную дверь": "phrase:жалюзи на балконную дверь",
    "лоджия дизайн": "phrase:дизайн лоджии",
    "обустройство лоджии": "unit:BALCONY_RENOVATION_WITH_GLAZING",
    "как поднять балконную дверь": "unit:WINDOW_REPAIR_SERVICE",
    "сколько стоит балконный блок": "unit:PVC_BALCONY_DOORS_COMMERCIAL",
    "дизайн лоджии 6 метров": "phrase:дизайн лоджии",
    "пол на лоджии из чего лучше сделать": "unit:OPEN_BALCONY_FINISHING",
    "оконный блок с балконной дверью цена": "unit:PVC_BALCONY_DOORS_COMMERCIAL",
    "балконный блок": "unit:PVC_BALCONY_DOORS_COMMERCIAL",
    "лоджия это": "unit:BALCONY_GLAZING_GENERAL",
    "отделка лоджии": "phrase:отделка лоджии",
    "дизайн лоджии": "phrase:дизайн лоджии",
    "лоджия": "unit:BALCONY_GLAZING_GENERAL",
    "балконная дверь с окном": "unit:PVC_BALCONY_DOORS_COMMERCIAL",
    "ремонт лоджии": "phrase:ремонт лоджии",
    "отделка лоджии варианты": "phrase:отделка лоджии",
    "шпросы на пластиковые окна": "phrase:шпросы на пластиковые окна цена",
    "установка откосов на пластиковые окна своими руками": "phrase:установка откосов на пластиковые окна своими руками",
    "анкерные пластины для окон пвх": "phrase:анкерные пластины для окон пвх",
    "штапики на окнах что это": "phrase:штапики на окнах что это",
    "как заменить стеклопакет в пластиковом окне самостоятельно": "phrase:заменить стеклопакет в пластиковом окне",
    "толщина стеклопакета в пластиковых окнах": "unit:GLASS_UNIT_SELECTION_INFO",
}

NOISE_PHRASES = {
    "как открыть бутылку без открывашки", "как открыть бутылку пива без открывашки",
    "балконное чудо", "втб не открывается на айфоне", "чем высушить погреб от влаги",
    "острый бронхит код мкб", "почему втб не открывается на айфоне",
    "псб банк не открывается на айфоне", "фабрика окон", "окн", "окно фертильности",
    "огнестрельное окно", "полетели сквозь окна", "пластиковое стекло",
    "фертильное окно это", "из моего окна 2", "из моего окна 1", "человек за окном",
    "самолет ру", "из моего окна сколько частей", "одно окно", "стеклов", "кно",
    "окогу", "из моего окна 1 часть смотреть", "расцвела под окошком",
    "из моего окна 1 часть", "из моего окна все части", "вид из окна", "f okno ru",
    "как называется окно в самолете", "наши окна", "шопот за окном",
    "из моего окна актеры", "птица в окно ударилась к чему это", "окна столицы",
    "из моего окна 4", "фойе в офисном здании", "болкон", "лоджи",
    "пойдем покурим на лоджию", "место кладовки", "армированная пленка",
    "пластиковая арматура", "как закрепить окно поверх других windows 11",
    "что такое фертильное окно", "фертильное окно что это",
    "армированный скотч для чего применяется",
}


def classify(seed_order: int, row_class: str, phrase: str, master_exact: dict[str, dict[str, str]]) -> dict[str, str]:
    key = normalize(phrase)
    if row_class == "DIRECT_RESULT" and seed_order in NEW_DIRECTION_BY_SEED:
        if key in HOLD_PHRASES:
            return {"classification": "HOLD_EVIDENCE", "direction": "", "authority": "NO_ACCEPTED_BUSINESS_AUTHORITY", "reason": HOLD_PHRASES[key]}
        direction = NEW_DIRECTION_BY_SEED[seed_order]
        return {
            "classification": "POTENTIALLY_NEW_SEARCH_RECHECK",
            "direction": direction,
            "authority": "NO_EXACT_OR_CLOSE_ACTIVE_DIRECTION__STEP5A3_PARENT_UNIT_ONLY",
            "reason": "Прямой результат Wordstat подтверждает спрос внутри новой страницы-конкурента → seed-линии; точный интент и владение страницей остаются для Search.",
        }
    if key in HOLD_PHRASES:
        return {"classification": "HOLD_EVIDENCE", "direction": "", "authority": "NO_ACCEPTED_BUSINESS_AUTHORITY", "reason": HOLD_PHRASES[key]}
    if key in OFF_SCOPE_PHRASES:
        return {"classification": "OFF_SCOPE_BUSINESS", "direction": "", "authority": "FROZEN_OKNO_MSK_SCOPE", "reason": "Фраза относится к отдельному товару/работе вне подтверждённого оконно-балконного предложения клиента."}
    if key in ALREADY_CLOSE_UNITS:
        return {"classification": "ALREADY_COVERED_EXACT_OR_CLOSE", "direction": "", "authority": ALREADY_CLOSE_UNITS[key], "reason": "Точная либо близкая семантическая задача уже сохранена в текущем master/unit authority; повторный Search не нужен."}
    if key in master_exact:
        return {"classification": "ALREADY_COVERED_EXACT_OR_CLOSE", "direction": "", "authority": f"phrase:{master_exact[key]['phrase']}", "reason": "Точное нормализованное совпадение уже присутствует в текущем Stage-5 semantic master."}
    if key in NOISE_PHRASES:
        return {"classification": "NOISE_IRRELEVANT", "direction": "", "authority": "NONE__IRRELEVANT_ASSOCIATION", "reason": "Ассоциация не описывает релевантную оконную/балконную поисковую задачу клиента."}
    # Fail closed: unexpected associations must never become Search requirements.
    return {"classification": "NOISE_IRRELEVANT", "direction": "", "authority": "NONE__UNMAPPED_ASSOCIATION_FAIL_CLOSED", "reason": "Ассоциация не имеет достаточной причинной и бизнес-связи с исходным competitor-derived seed; оставлена как raw evidence, но не продвигается."}


def load_inputs() -> tuple[list[dict[str, str]], list[dict[str, object]], dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    package = read_tsv(WORDSTAT_PACKAGE)
    specs = json.loads(SEED_DECISIONS.read_text(encoding="utf-8"))
    spec_by_seed = {row["normalized_candidate_seed"].casefold(): row for row in specs if row["wordstat_required"]}
    pages = {row["inspection_id"]: row for row in read_tsv(PAGE_EVIDENCE)}
    master_rows = read_tsv(FINAL_MASTER)
    master_exact = {normalize(row["phrase"]): row for row in master_rows}
    return package, specs, spec_by_seed, pages, master_exact


def build_acquisition() -> tuple[list[dict[str, object]], list[dict[str, object]], dict[int, dict[str, object]]]:
    package, _, spec_by_seed, pages, master_exact = load_inputs()
    acquisition_rows: list[dict[str, object]] = []
    returned_rows: list[dict[str, object]] = []
    context_by_order: dict[int, dict[str, object]] = {}
    raw_row_number = 0
    for package_row in package:
        order = int(package_row["wordstat_seed_order"])
        seed = package_row["normalized_candidate_seed"]
        raw = json.loads(raw_path(order).read_text(encoding="utf-8"))
        provider = raw["provider_result"]
        result = provider["result"]
        spec = spec_by_seed[seed.casefold()]
        source_ids = [source["inspection_id"] for source in spec["sources"]]
        source_pages = [pages[source_id] for source_id in source_ids]
        domains = sorted({row["competitor_domain"] for row in source_pages})
        urls = [row["requested_url"] for row in source_pages]
        observations = [f"{source['inspection_id']} {source['element_type']}: {source['element_text']}" for source in spec["sources"]]
        shape = provider_shape(result)
        direct = result.get("results", [])
        associations = result.get("associations", [])
        if shape == "EMPTY_PROVIDER_RESULT":
            limitation = "Provider returned result={}; no numeric zero and no phrase rows may be inferred."
        elif shape == "TOTALCOUNT_ONLY":
            limitation = "Provider supplied totalCount only; no phrase-level results or associations may be invented."
        else:
            limitation = "Only explicitly returned results/associations are authoritative; totalCount is not a row inventory."
        acquisition = {
            "seed_order": order,
            "seed_text": seed,
            "semantic_axis": package_row["semantic_axis"],
            "raw_item_file": raw_path(order).name,
            "request_id": provider["request_id"],
            "http_status": provider["http_status"],
            "request_executed": str(provider["request_executed"]).lower(),
            "item_status": raw["item"]["status"],
            "provider_result_shape": shape,
            "total_count": result.get("totalCount", ""),
            "direct_results_rows": len(direct),
            "association_rows": len(associations),
            "empty_result_flag": str(not bool(result)).lower(),
            "region": " | ".join(provider["command"]["regions"]),
            "device_scope": " | ".join(provider["command"]["devices"]),
            "competitor_domains": " | ".join(domains),
            "competitor_urls": " | ".join(urls),
            "page_evidence_ids": " | ".join(source_ids),
            "page_observed_evidence": " | ".join(observations),
            "step5a3_candidate_decision": spec["seed_decision"],
            "seed_reconciliation_route": "",
            "evidence_limitation_note": limitation,
        }
        if order == 1:
            acquisition["seed_reconciliation_route"] = "NO_NEW_SEARCH__PRESERVED_EXACT_SEARCH_Q62_EXISTS__TOTALCOUNT_ONLY"
        elif order == 8:
            acquisition["seed_reconciliation_route"] = "POTENTIALLY_NEW_SEARCH_RECHECK__TOTALCOUNT_ONLY"
        elif shape == "EMPTY_PROVIDER_RESULT":
            acquisition["seed_reconciliation_route"] = "HOLD_EVIDENCE__EMPTY_PROVIDER_RESULT"
        elif direct:
            acquisition["seed_reconciliation_route"] = "ROW_LEVEL_RECONCILIATION"
        else:
            acquisition["seed_reconciliation_route"] = "HOLD_EVIDENCE__NO_PHRASE_ROWS"
        acquisition_rows.append(acquisition)
        context_by_order[order] = {"spec": spec, "pages": source_pages, "acquisition": acquisition}

        for provider_key, row_class in (("results", "DIRECT_RESULT"), ("associations", "ASSOCIATION")):
            for class_index, row in enumerate(result.get(provider_key, []), start=1):
                raw_row_number += 1
                decision = classify(order, row_class, row["phrase"], master_exact)
                returned_rows.append({
                    "wordstat_row_id": f"WSR{raw_row_number:03d}",
                    "seed_order": order,
                    "source_seed": seed,
                    "source_raw_item_file": raw_path(order).name,
                    "wordstat_row_class": row_class,
                    "row_index_within_class": class_index,
                    "returned_phrase": row["phrase"],
                    "returned_count": row["count"],
                    "source_request_id": provider["request_id"],
                    "source_total_count": result.get("totalCount", ""),
                    "candidate_relevance_classification": decision["classification"],
                    "deduplicated_direction_id": decision["direction"],
                    "semantic_authority_match": decision["authority"],
                    "reason_evidence_note": decision["reason"],
                    "competitor_domains": " | ".join(domains),
                    "competitor_urls": " | ".join(urls),
                    "page_evidence_ids": " | ".join(source_ids),
                    "observed_page_evidence": " | ".join(observations),
                    "lineage": f"{' | '.join(source_ids)} -> seed:{seed} -> {raw_path(order).name} -> {row_class}:{row['phrase']}",
                })
    return acquisition_rows, returned_rows, context_by_order


ACQUISITION_FIELDS = [
    "seed_order", "seed_text", "semantic_axis", "raw_item_file", "request_id", "http_status",
    "request_executed", "item_status", "provider_result_shape", "total_count", "direct_results_rows",
    "association_rows", "empty_result_flag", "region", "device_scope", "competitor_domains",
    "competitor_urls", "page_evidence_ids", "page_observed_evidence", "step5a3_candidate_decision",
    "seed_reconciliation_route", "evidence_limitation_note",
]

RETURNED_FIELDS = [
    "wordstat_row_id", "seed_order", "source_seed", "source_raw_item_file", "wordstat_row_class",
    "row_index_within_class", "returned_phrase", "returned_count", "source_request_id", "source_total_count",
    "candidate_relevance_classification", "deduplicated_direction_id", "semantic_authority_match",
    "reason_evidence_note", "competitor_domains", "competitor_urls", "page_evidence_ids",
    "observed_page_evidence", "lineage",
]


def build_reconciliation(returned_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for row in returned_rows:
        classification = str(row["candidate_relevance_classification"])
        rows.append({
            "wordstat_row_id": row["wordstat_row_id"],
            "normalized_returned_phrase": normalize(str(row["returned_phrase"])),
            "wordstat_row_class": row["wordstat_row_class"],
            "returned_phrase": row["returned_phrase"],
            "returned_count": row["returned_count"],
            "source_seed_order": row["seed_order"],
            "source_seed": row["source_seed"],
            "material_relevance": "MATERIAL" if classification != "NOISE_IRRELEVANT" else "NOT_MATERIAL",
            "semantic_reconciliation_result": classification,
            "semantic_authority_match": row["semantic_authority_match"],
            "deduplicated_direction_id": row["deduplicated_direction_id"],
            "search_recheck_required": str(classification == "POTENTIALLY_NEW_SEARCH_RECHECK").lower(),
            "reconciliation_reason": row["reason_evidence_note"],
            "competitor_page_lineage": f"{row['page_evidence_ids']} | {row['competitor_urls']}",
            "raw_provider_lineage": f"{row['source_raw_item_file']} | {row['source_request_id']}",
            "claim_boundary": "WORDSTAT_DEMAND_OR_ASSOCIATION_ONLY__NO_INTENT_OR_PAGE_OWNERSHIP_DECISION",
        })
    return rows


RECONCILIATION_FIELDS = [
    "wordstat_row_id", "normalized_returned_phrase", "wordstat_row_class", "returned_phrase", "returned_count",
    "source_seed_order", "source_seed", "material_relevance", "semantic_reconciliation_result",
    "semantic_authority_match", "deduplicated_direction_id", "search_recheck_required",
    "reconciliation_reason", "competitor_page_lineage", "raw_provider_lineage", "claim_boundary",
]


SEARCH_SPECS = [
    (1, "OPEN_BALCONY_WATERPROOFING", "гидроизоляция для открытого балкона", 3),
    (2, "SUN_PROTECTION_GLASS_UNIT", "солнцезащитный стеклопакет", 4),
    (3, "MULTIFUNCTIONAL_GLASS_UNIT", "многофункциональный стеклопакет что это", 5),
    (4, "IMPACT_RESISTANT_GLASS_UNIT", "ударопрочный стеклопакет", 6),
    (5, "OLD_HOUSING_WINDOWS", "окна для старого фонда", 8),
    (6, "BALCONY_AS_OFFICE", "балконы под офис", 10),
    (7, "BALCONY_AS_STORAGE", "кладовая на балконе", 11),
    (8, "BALCONY_ROOF_SOUNDPROOFING", "шумоизоляция на крышу балкона", 13),
    (9, "WINDOW_PROFILE_REINFORCEMENT", "армирование оконного профиля", 14),
]


def build_search_package(returned_rows: list[dict[str, object]], context: dict[int, dict[str, object]]) -> list[dict[str, object]]:
    by_direction: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in returned_rows:
        if row["candidate_relevance_classification"] == "POTENTIALLY_NEW_SEARCH_RECHECK":
            by_direction[str(row["deduplicated_direction_id"])].append(row)
    rows = []
    for priority, direction, query, seed_order in SEARCH_SPECS:
        ctx = context[seed_order]
        acquisition = ctx["acquisition"]
        direction_rows = by_direction.get(direction, [])
        if seed_order == 8:
            returned_summary = "NO_PHRASE_ROWS__TOTALCOUNT_ONLY=5"
            wordstat_lineage = f"{acquisition['raw_item_file']} | {acquisition['request_id']} | totalCount=5 | results=0 | associations=0"
        else:
            returned_summary = " | ".join(f"{row['returned_phrase']} [{row['returned_count']}]" for row in direction_rows)
            wordstat_lineage = " | ".join(sorted({f"{row['source_raw_item_file']}:{row['source_request_id']}" for row in direction_rows}))
        page_ids = acquisition["page_evidence_ids"]
        page_urls = acquisition["competitor_urls"]
        if seed_order == 3:
            prior_gap = "Preserved Search exposed open-balcony pages but did not test the exact waterproofing query family."
        elif seed_order == 8:
            prior_gap = "No preserved exact-query Search row tests windows for old housing stock; Wordstat supplied only aggregate totalCount, so Search must resolve intent without invented phrase rows."
        else:
            prior_gap = "The preserved Search universe did not test this exact new Wordstat-backed direction; the competitor page supplied only topic evidence."
        rows.append({
            "search_priority": priority,
            "deduplicated_direction_id": direction,
            "representative_query": query,
            "region": 213,
            "requested_top_results": 10,
            "originating_wordstat_seed_order": seed_order,
            "originating_wordstat_seed": acquisition["seed_text"],
            "originating_returned_phrases_and_counts": returned_summary,
            "wordstat_evidence_lineage": wordstat_lineage,
            "competitor_page_evidence_ids": page_ids,
            "competitor_page_urls": page_urls,
            "competitor_page_observed_evidence": acquisition["page_observed_evidence"],
            "current_semantic_reconciliation": "POTENTIALLY_NEW_SEARCH_RECHECK__NOT_ACCEPTED_KEYWORD",
            "unresolved_search_question": "Какой интент и тип страницы доминируют в текущей региональной выдаче, видимы ли выбранные конкуренты и совместима ли задача с бизнес-моделью OKNO_MSK?",
            "why_preserved_search_is_insufficient": prior_gap,
            "representative_query_rationale": "Наиболее частотная/базовая фактически возвращённая формулировка семейства; одна проверка покрывает близкие грамматические варианты." if seed_order != 8 else "Исходный seed сохранён без выдуманной phrase-row: provider вернул только totalCount=5.",
            "expected_downstream_decision_gate": "ADD_TO_PIPELINE | ALREADY_COVERED | REJECT_OFF_SCOPE | HOLD_EVIDENCE",
            "provider_call_authorization_state": "RETURN_TO_MAIN_CHATGPT_FOR_YANDEX_SEARCH_BRIDGE_EXECUTION",
            "claim_boundary": "REQUIREMENT_ONLY__WORK_DID_NOT_EXECUTE_SEARCH",
        })
    return rows


SEARCH_FIELDS = [
    "search_priority", "deduplicated_direction_id", "representative_query", "region", "requested_top_results",
    "originating_wordstat_seed_order", "originating_wordstat_seed", "originating_returned_phrases_and_counts",
    "wordstat_evidence_lineage", "competitor_page_evidence_ids", "competitor_page_urls",
    "competitor_page_observed_evidence", "current_semantic_reconciliation", "unresolved_search_question",
    "why_preserved_search_is_insufficient", "representative_query_rationale", "expected_downstream_decision_gate",
    "provider_call_authorization_state", "claim_boundary",
]


def build_report(acquisition: list[dict[str, object]], returned: list[dict[str, object]], search: list[dict[str, object]]) -> str:
    shapes = Counter(str(row["provider_result_shape"]) for row in acquisition)
    classes = Counter(str(row["candidate_relevance_classification"]) for row in returned)
    direct = sum(row["wordstat_row_class"] == "DIRECT_RESULT" for row in returned)
    associations = sum(row["wordstat_row_class"] == "ASSOCIATION" for row in returned)
    lines = [
        "# OKNO_MSK — Step 5A.5 Wordstat reconciliation report",
        "",
        "Date: 2026-09-08  ",
        "Status: **ANALYST QA PASS / OWNER REVIEW PENDING / METHOD NOT PROMOTED**",
        "",
        "## 1. Completed scope",
        "",
        "All 14 preserved Wordstat executions and every actually returned direct/association row were normalized, joined back to competitor-page evidence and reconciled against the current completed OKNO_MSK semantic authority. No provider was called. The result is a bounded ordinary-Yandex-Search requirement package for Main ChatGPT; it is not an accepted keyword/page/action decision.",
        "",
        "## 2. Provider accounting",
        "",
        "```text",
        f"SEEDS_ACCOUNTED = {len(acquisition)} / 14",
        f"DIRECT_WORDSTAT_ROWS_EXTRACTED = {direct}",
        f"ASSOCIATION_ROWS_EXTRACTED = {associations}",
        f"TOTAL_RETURNED_PHRASE_ROWS = {len(returned)}",
        f"RESULT_ROWS_ASSOCIATIONS_TOTALCOUNT = {shapes['RESULT_ROWS_ASSOCIATIONS_TOTALCOUNT']}",
        f"TOTALCOUNT_ONLY = {shapes['TOTALCOUNT_ONLY']}",
        f"EMPTY_PROVIDER_RESULT = {shapes['EMPTY_PROVIDER_RESULT']}",
        "FABRICATED_ROWS = 0",
        "FABRICATED_ZERO_DEMAND = 0",
        "```",
        "",
        "`result={}` remains an empty provider result, not numeric zero. `totalCount`-only responses remain aggregate observations without invented phrase rows.",
        "",
        "## 3. Row-level reconciliation",
        "",
        "```text",
        f"ALREADY_COVERED_EXACT_OR_CLOSE = {classes['ALREADY_COVERED_EXACT_OR_CLOSE']}",
        f"POTENTIALLY_NEW_SEARCH_RECHECK = {classes['POTENTIALLY_NEW_SEARCH_RECHECK']}",
        f"OFF_SCOPE_BUSINESS = {classes['OFF_SCOPE_BUSINESS']}",
        f"NOISE_IRRELEVANT = {classes['NOISE_IRRELEVANT']}",
        f"HOLD_EVIDENCE = {classes['HOLD_EVIDENCE']}",
        f"DEDUPLICATED_NEW_SEARCH_DIRECTIONS = {len(search)}",
        f"FINAL_SEARCH_RECHECK_CALLS_REQUIRED = {len(search)}",
        "```",
        "",
        "Associations were assessed independently. High counts did not override relevance, business scope or existing semantic coverage.",
        "",
        "## 4. Exact Search recheck package",
        "",
        "| Priority | Exact query | Wordstat source state | Why Search is required |",
        "|---:|---|---|---|",
    ]
    for row in search:
        source_state = "totalCount-only" if int(row["originating_wordstat_seed_order"]) == 8 else "returned phrase row(s)"
        lines.append(f"| {row['search_priority']} | **{row['representative_query']}** | {source_state} | Resolve current intent, competitor visibility and page type before any merge decision. |")
    lines += [
        "",
        "The P-46 seed is not repeated in this Search package: its exact query already has preserved Q62 Search evidence and Wordstat returned only `totalCount=17`, not phrase rows. The four `result={}` seeds remain explicit `HOLD_EVIDENCE`; absence of rows is not converted into zero demand.",
        "",
        "## 5. Causality and decision boundary",
        "",
        "```text",
        "COMPETITOR PAGE EVIDENCE",
        "→ CANDIDATE SEED",
        "→ PRESERVED WORDSTAT ENVELOPE",
        "→ ACTUALLY RETURNED PHRASE / TOTALCOUNT-ONLY STATE",
        "→ CURRENT SEMANTIC RECONCILIATION",
        "→ SEARCH REQUIREMENT",
        "```",
        "",
        "This lineage does not claim that a competitor ranks for a Wordstat-returned phrase. Wordstat does not establish intent, page ownership, split/merge, page creation or implementation.",
        "",
        "## 6. Protection and provider accounting",
        "",
        "```text",
        "NEW_YANDEX_SEARCH_CALLS = 0",
        "NEW_WORDSTAT_CALLS = 0",
        "NEW_ALICE_CALLS = 0",
        "NEW_GENSEARCH_CALLS = 0",
        "NEW_WEBMASTER_CALLS = 0",
        "NEW_METRIKA_CALLS = 0",
        "NEW_DIRECT_CALLS = 0",
        "CLIENT_DELIVERABLES_MODIFIED = false",
        "LEVEL1_METHOD_PROMOTED = false",
        "```",
        "",
        "## 7. Next action",
        "",
        "`MAIN_CHATGPT_STEP_5A_6_EXECUTE_ONLY_THE_MATERIALIZED_SEARCH_RECHECK_PACKAGE_VIA_YANDEX_BRIDGE`",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["acquisition", "complete"], default="complete")
    args = parser.parse_args()
    acquisition, returned, context = build_acquisition()
    write_tsv(ACQUISITION, acquisition, ACQUISITION_FIELDS)
    write_tsv(RETURNED, returned, RETURNED_FIELDS)
    if args.stage == "acquisition":
        return
    reconciliation = build_reconciliation(returned)
    search = build_search_package(returned, context)
    write_tsv(RECONCILIATION, reconciliation, RECONCILIATION_FIELDS)
    write_tsv(SEARCH_PACKAGE, search, SEARCH_FIELDS)
    REPORT.write_text(build_report(acquisition, returned, search), encoding="utf-8")


if __name__ == "__main__":
    main()
