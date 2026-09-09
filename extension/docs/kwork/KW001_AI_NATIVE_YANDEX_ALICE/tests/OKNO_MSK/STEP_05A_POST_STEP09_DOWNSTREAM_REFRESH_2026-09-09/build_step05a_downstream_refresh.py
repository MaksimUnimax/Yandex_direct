#!/usr/bin/env python3
"""Materialize the bounded OKNO_MSK Step5A post-Step09 downstream refresh.

The script consumes only preserved repository evidence.  It does not perform
network access and does not mutate the historical Stage-5 authority or the
corrected 2026-09-05 client release.
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve()
WORK = HERE.parent
JOB = HERE.parents[1]
REPO = HERE.parents[7]
PROP = JOB / "STEP_05A_POST_ACCEPTANCE_PROPAGATION_2026-09-08"
FIRST = JOB / "STEP_05A_FIRST_EXECUTION_2026-09-08"
BASE_RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09"

BASE_MASTER = JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"
BASE_UNITS = JOB / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"
UNION = PROP / "STEP_05A_POST_ACCEPTANCE_STEP08_FREEZE.tsv"
DELTA = PROP / "STEP_05A_DELTA_STEP07_CLEANUP_DECISIONS.tsv"
ACCEPTED = FIRST / "STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv"
STEP9_RECEIPT = PROP / "STEP_09_DELTA_SEARCH_ACQUISITION_RECEIPT_NORMALIZED_2026-09-08.json"
STEP9_TOP10 = PROP / "STEP_09_DELTA_SEARCH_TOP10_EVIDENCE_2026-09-08.tsv"

STEP9_QUERIES = {
    "гидроизоляция открытого балкона в частном доме": {
        "result_mix": "8 информационных/технических, 1 услуга, 1 пользовательский материал",
        "task": "понять технологию гидроизоляции открытого балкона частного дома; возможен поиск подрядчика",
        "intent": "INFO_OR_SERVICE",
        "modifier": "частный дом задаёт отдельный строительный контекст",
        "boundary": "точное соответствие предложению компании не подтверждено",
        "disposition": "HOLD_EXACT_OWNER__KEEP_FAMILY_SIGNAL",
    },
    "лучшая гидроизоляция для открытого балкона": {
        "result_mix": "сравнение материалов и инструкции доминируют; коммерческой услуги недостаточно для назначения",
        "task": "сравнить и выбрать гидроизоляционный материал",
        "intent": "SELECTION_INFO",
        "modifier": "оценка «лучшая» меняет задачу на выбор материала",
        "boundary": "продажа материалов и точный владелец на сайте не подтверждены",
        "disposition": "HOLD_EXACT_OWNER__KEEP_FAMILY_SIGNAL",
    },
    "как сделать гидроизоляцию на открытом балконе": {
        "result_mix": "инструкции и материалы доминируют",
        "task": "выполнить гидроизоляцию самостоятельно",
        "intent": "DIY_INFO",
        "modifier": "«как сделать» формирует самостоятельную пошаговую задачу",
        "boundary": "не подтверждено, что существующая страница должна обучать самостоятельным работам",
        "disposition": "HOLD_EXACT_OWNER__KEEP_FAMILY_SIGNAL",
    },
    "гидроизоляция открытого деревянного балкона": {
        "result_mix": "материалы о деревянных домах/конструкциях доминируют; есть одна услуга",
        "task": "понять гидроизоляцию деревянной конструкции",
        "intent": "TECHNICAL_INFO_OR_SERVICE",
        "modifier": "деревянная конструкция является существенной технической границей",
        "boundary": "работа с деревянными конструкциями не подтверждена предложением компании",
        "disposition": "HOLD_EXACT_OWNER__KEEP_FAMILY_SIGNAL",
    },
    "гидроизоляция балконной плиты открытого балкона": {
        "result_mix": "технические статьи, материалы и ремонт/защита плиты",
        "task": "выбрать технологию и материалы для защиты балконной плиты",
        "intent": "TECHNICAL_INFO",
        "modifier": "балконная плита меняет объект на строительную конструкцию",
        "boundary": "ремонт/гидроизоляция плиты не подтверждены как услуга компании",
        "disposition": "HOLD_EXACT_OWNER__KEEP_FAMILY_SIGNAL",
    },
    "шумоизоляция крыши балкона изнутри от дождя": {
        "result_mix": "товары, инструкции и услуги представлены вместе",
        "task": "снизить шум дождя от крыши/козырька, в том числе внутренним способом",
        "intent": "MIXED_PRODUCT_INFO_SERVICE",
        "modifier": "«изнутри» задаёт отдельный способ выполнения",
        "boundary": "внутренний способ и состав услуги не подтверждены",
        "disposition": "HOLD_EXACT_OWNER__KEEP_FAMILY_SIGNAL",
    },
}

DIRECTIONS = {
    "OPEN_BALCONY_WATERPROOFING": {
        "cluster": "OPEN_BALCONY_FINISHING", "family_url": "https://okno-msk.ru/balkony-i-lodzhii/otdelka-balkonov",
        "support": "https://okno-msk.ru/balkony-i-lodzhii", "task": "разобраться с гидроизоляцией открытого балкона",
        "intent": "COMMERCIAL_OR_INFO", "exact_state": "OWNER_UNRESOLVED_EVIDENCE_REQUIRED",
        "action": "HOLD_EVIDENCE", "physical": "NO", "priority": "PENDING_EVIDENCE",
        "reason": "Выдача подтверждает отдельные информационные, товарные и строительные задачи; предложение компании и точный владелец не подтверждены.",
    },
    "SUN_PROTECTION_GLASS_UNIT": {
        "cluster": "GLASS_UNIT_PRODUCT_SELECTION", "family_url": "https://okno-msk.ru/okna-rehau/steklopakety-dlya-plastikovykh-okon",
        "support": "https://okno-msk.ru/stati/kak-vybrat-steklopaket-dlya-plastikovogo-okna/", "task": "выбрать солнцезащитный стеклопакет",
        "intent": "COMMERCIAL_OR_INFO", "exact_state": "OWNER_EXISTING",
        "action": "SEMANTIC_MAPPING_ONLY", "physical": "NO", "priority": "ANALYTICAL_MAPPING",
        "reason": "Коммерческий выбор конфигурации относится к существующей странице стеклопакетов; новый URL не нужен.",
    },
    "MULTIFUNCTIONAL_GLASS_UNIT": {
        "cluster": "GLASS_UNIT_SELECTION_INFO", "family_url": "https://okno-msk.ru/stati/kak-vybrat-steklopaket-dlya-plastikovogo-okna/",
        "support": "https://okno-msk.ru/stati/steklopakety-osobennosti-i-vidy", "task": "понять назначение и выбор многофункционального стеклопакета",
        "intent": "INFO", "exact_state": "OWNER_EXISTING",
        "action": "SEMANTIC_MAPPING_ONLY", "physical": "NO", "priority": "ANALYTICAL_MAPPING",
        "reason": "Информационная задача соответствует существующему руководству по выбору стеклопакета.",
    },
    "IMPACT_RESISTANT_GLASS_UNIT": {
        "cluster": "GLASS_UNIT_PRODUCT_SELECTION", "family_url": "https://okno-msk.ru/okna-rehau/steklopakety-dlya-plastikovykh-okon",
        "support": "https://okno-msk.ru/stati/kak-vybrat-steklopaket-dlya-plastikovogo-okna/", "task": "выбрать ударопрочную конфигурацию стеклопакета",
        "intent": "COMMERCIAL_OR_INFO", "exact_state": "OWNER_EXISTING",
        "action": "SEMANTIC_MAPPING_ONLY", "physical": "NO", "priority": "ANALYTICAL_MAPPING",
        "reason": "Запрос относится к выбору продукта и не доказывает необходимость отдельной страницы.",
    },
    "BALCONY_AS_OFFICE": {
        "cluster": "BALCONY_RENOVATION_WITH_GLAZING", "family_url": "https://okno-msk.ru/balkony-i-lodzhii/",
        "support": "", "task": "подготовить балкон для использования как рабочее место",
        "intent": "SERVICE_OR_SELECTION", "exact_state": "OWNER_EXISTING",
        "action": "SEMANTIC_MAPPING_ONLY", "physical": "NO", "priority": "ANALYTICAL_MAPPING",
        "reason": "Сценарий относится к комплексному ремонту и остеклению существующего балконного раздела.",
    },
    "BALCONY_ROOF_SOUNDPROOFING": {
        "cluster": "BALCONY_GLAZING_ROOF_SERVICE", "family_url": "https://okno-msk.ru/balkony-i-lodzhii/balkon-s-kryshej/",
        "support": "", "task": "снизить шум дождя от крыши или козырька балкона",
        "intent": "SERVICE_OR_SELECTION", "exact_state": "OWNER_EXISTING",
        "action": "SEMANTIC_MAPPING_ONLY", "physical": "NO", "priority": "ANALYTICAL_MAPPING",
        "reason": "Общая задача относится к существующей услуге крыши; вариант «изнутри» остаётся без точного назначения.",
    },
    "WINDOW_PROFILE_REINFORCEMENT": {
        "cluster": "WINDOW_PROFILE_SELECTION_INFO", "family_url": "https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna/",
        "support": "https://okno-msk.ru/stati/kakoj-profil-i-firma-luchshe", "task": "понять роль армирования при выборе оконного профиля",
        "intent": "INFO", "exact_state": "OWNER_EXISTING",
        "action": "SEMANTIC_MAPPING_ONLY", "physical": "NO", "priority": "ANALYTICAL_MAPPING",
        "reason": "Техническое пояснение относится к существующему руководству по выбору профиля.",
    },
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing empty TSV: {path}")
    fields = fields or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def norm(value: str) -> str:
    return " ".join(value.casefold().split())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_record(path: Path) -> dict[str, object]:
    return {"path": str(path.relative_to(JOB)), "bytes": path.stat().st_size, "sha256": sha(path)}


def main() -> None:
    base_master = read_tsv(BASE_MASTER)
    base_units = read_tsv(BASE_UNITS)
    union = read_tsv(UNION)
    delta = read_tsv(DELTA)
    accepted = read_tsv(ACCEPTED)
    top10 = read_tsv(STEP9_TOP10)
    receipt = json.loads(STEP9_RECEIPT.read_text(encoding="utf-8"))

    assert len(base_master) == 2840 and len({norm(r['phrase']) for r in base_master}) == 2840
    assert len(union) == 2856 and len({norm(r['phrase']) for r in union}) == 2856
    assert len(delta) == len(accepted) == 16
    assert len(top10) == 60
    assert receipt["accounting"]["provider_requests_confirmed"] == 6
    assert receipt["accounting"]["estimated_cost_rub"] == 2.928

    delta_by_phrase = {norm(r["phrase"]): r for r in delta}
    accepted_by_phrase = {norm(r["phrase"]): r for r in accepted}
    top10_by_query: dict[str, list[dict[str, str]]] = {}
    for row in top10:
        top10_by_query.setdefault(norm(row["query"]), []).append(row)

    step9_rows = []
    for query, decision in STEP9_QUERIES.items():
        rows = top10_by_query[norm(query)]
        step9_rows.append({
            "query": query, "request_id": rows[0]["request_id"], "region": "213", "top10_rows": len(rows),
            "observed_top10": " | ".join(f"{r['rank']}:{r['domain']}:{r['title']}" for r in rows),
            "dominant_result_types": decision["result_mix"], "dominant_user_task": decision["task"],
            "intent_interpretation": decision["intent"], "modifier_family_effect": decision["modifier"],
            "business_boundary": decision["boundary"], "common_pipeline_state": "ENTER_AS_ACTIVE_HOLD",
            "residual_uncertainty": "EXACT_OWNER_AND_IMPLEMENTATION_NOT_PROVEN",
            "final_post_step9_disposition": decision["disposition"],
            "evidence_locator": f"{STEP9_TOP10.name}#query={query}",
        })
    write_tsv(WORK / "STEP_09_REVIEW_SEARCH_RESOLUTION.tsv", step9_rows)

    step10_rows, step11_rows, full_delta_rows = [], [], []
    for accepted_row in accepted:
        phrase = accepted_row["phrase"]
        drow = delta_by_phrase[norm(phrase)]
        direction = accepted_row["step5a_direction_id"]
        cfg = DIRECTIONS[direction]
        is_step9_hold = phrase in STEP9_QUERIES
        exact_state = "OWNER_UNRESOLVED_EVIDENCE_REQUIRED" if is_step9_hold else cfg["exact_state"]
        owner_hold = exact_state == "OWNER_UNRESOLVED_EVIDENCE_REQUIRED"
        exact_url = "" if owner_hold else cfg["family_url"]
        intent = STEP9_QUERIES[phrase]["intent"] if is_step9_hold else cfg["intent"]
        confidence = "MEDIUM" if is_step9_hold else ("HIGH" if drow["semantic_confidence"] == "HIGH" else "MEDIUM")
        step10_rows.append({
            "delta_id": accepted_row["delta_id"], "phrase": phrase, "direction_id": direction,
            "user_task": STEP9_QUERIES[phrase]["task"] if is_step9_hold else cfg["task"],
            "intent": intent, "semantic_family": cfg["cluster"], "business_boundary_state": "EVIDENCE_REQUIRED" if is_step9_hold else "IN_SCOPE",
            "uncertainty_state": "HOLD" if is_step9_hold else "NONE", "assignment_state": "ASSIGNED_HOLD" if is_step9_hold else "ASSIGNED",
            "assignment_confidence": confidence,
            "evidence": (f"{STEP9_TOP10.name}#query={phrase}" if is_step9_hold else f"{accepted_row['search_raw_item_file']}#{accepted_row['search_request_id']}"),
            "decision_reason": STEP9_QUERIES[phrase]["boundary"] if is_step9_hold else cfg["reason"],
        })
        step11_rows.append({
            "delta_id": accepted_row["delta_id"], "phrase": phrase, "direction_id": direction,
            "exact_query_owner_state": exact_state, "exact_query_owner_url": exact_url,
            "family_owner_unit": cfg["cluster"], "family_owner_url": cfg["family_url"],
            "supporting_pages": cfg["support"], "ownership_confidence": confidence,
            "mapping_applicability": "HOLD_NO_EXACT_TARGET" if owner_hold else "APPLICABLE",
            "mapping_reason": STEP9_QUERIES[phrase]["boundary"] if is_step9_hold else cfg["reason"],
            "evidence_provenance": (f"{STEP9_TOP10.name}#query={phrase}" if is_step9_hold else f"{accepted_row['search_raw_item_file']}#{accepted_row['search_request_id']}"),
        })
        unit = next(r for r in base_units if r["structural_unit_id"] == cfg["cluster"])
        full_delta_rows.append({
            "phrase": phrase, "final_semantic_state": "ASSIGNED_HOLD" if owner_hold else "ASSIGNED",
            "uncertainty_state": "HOLD" if owner_hold else "NONE", "search_stage_disposition": "CORE_CANDIDATE",
            "next_resolution_route": "REVIEW_DEFERRED" if owner_hold else "ORDINARY_SEARCH_ELIGIBLE",
            "semantic_confidence": confidence, "source_occurrences": "1", "result_occurrences": "1", "association_occurrences": "0",
            "step10_assignment_status": "ASSIGNED_HOLD" if is_step9_hold else "ASSIGNED", "step10_cluster_id": cfg["cluster"],
            "step10_evidence_mode": "DIRECT_EXACT_SEARCH" if is_step9_hold else "STEP5A_PRESERVED_SEARCH",
            "step11_effective_assignment_status": "ASSIGNED_HOLD" if owner_hold else "ASSIGNED", "step11_effective_cluster_id": cfg["cluster"],
            "step11_target_url": exact_url, "step11_ownership_state": exact_state,
            "final_structural_unit_id": cfg["cluster"], "canonical_user_task": cfg["task"], "canonical_intent_type": unit["intent_type"],
            "canonical_business_scope_state": unit["business_scope_state"], "canonical_unit_page_role": unit["unit_page_role"],
            "final_primary_page": exact_url, "final_supporting_pages": cfg["support"],
            "canonical_structural_action": "KEEP_EXISTING_STRUCTURE", "canonical_recommendation_maturity": "FINAL_WITHIN_STEP12_EVIDENCE" if not owner_hold else "DEFERRED_PENDING_MISSING_EVIDENCE",
            "canonical_final_confidence": confidence, "canonical_gap_type": "NONE" if not owner_hold else "EVIDENCE_INSUFFICIENT",
            "canonical_content_enhancement_state": "NOT_ASSESSED" if not owner_hold else "CONTENT_EVIDENCE_INSUFFICIENT",
            "explicit_missing_needs": "" if not owner_hold else (STEP9_QUERIES[phrase]["boundary"] if is_step9_hold else cfg["reason"]),
            "step14a_overlay_ids": "", "correction_lineage": "STEP5A_POST_STEP09_2026-09-09",
            "authority_lineage": f"{accepted_row['delta_id']}>{'STEP09_EXACT' if is_step9_hold else 'STEP5A_SEARCH'}>STEP10>STEP11>STEP12>STEP14>STEP18",
            "claim_boundary": "No new page or physical change; exact owner is unresolved where explicitly stated.",
        })
    write_tsv(WORK / "STEP_10_DELTA_DECISIONS.tsv", step10_rows)
    write_tsv(WORK / "STEP_11_DELTA_OWNERSHIP_DECISIONS.tsv", step11_rows)

    direction_rows = []
    for direction, cfg in DIRECTIONS.items():
        phrases = [r["phrase"] for r in accepted if r["step5a_direction_id"] == direction]
        direction_ownership = [r for r in step11_rows if r["direction_id"] == direction]
        resolved_count = sum(r["exact_query_owner_state"] == "OWNER_EXISTING" for r in direction_ownership)
        hold_count = sum(r["exact_query_owner_state"] == "OWNER_UNRESOLVED_EVIDENCE_REQUIRED" for r in direction_ownership)
        direction_rows.append({
            "direction_id": direction, "phrase_count": len(phrases), "family_owner_unit": cfg["cluster"],
            "family_owner_url": cfg["family_url"], "exact_owner_resolved_count": resolved_count,
            "exact_owner_hold_count": hold_count, "step12_action": cfg["action"], "physical_change": cfg["physical"],
            "new_page_decision": "REJECTED_NOT_JUSTIFIED", "step13_overlap_state": "NO_NEW_CONFLICT_TRIGGER",
            "step13_remediation": "KEEP_EXISTING_STRUCTURE__NO_DESTRUCTIVE_ACTION",
            "step14_architecture_effect": "EXISTING_OWNER_OR_FAMILY_ROUTE_ONLY__NO_NEW_URL",
            "step15_ai_case_selection": "NOT_SELECTED__NO_SEARCH_ARCHITECTURE_CONTRADICTION",
            "step16_status": "NOT_REQUIRED__NO_PROVIDER_CALL", "step17_status": "NOT_REQUIRED__NO_AI_OBSERVATION",
            "step18_readiness": cfg["priority"], "evidence_boundary": cfg["reason"],
        })
    write_tsv(WORK / "STEP_12_TO_18_DIRECTION_DECISIONS.tsv", direction_rows)

    for step, fields in {
        "STEP_12_DELTA_ACTION_DECISIONS.tsv": ["direction_id", "phrase_count", "step12_action", "physical_change", "new_page_decision", "evidence_boundary"],
        "STEP_13_DELTA_OVERLAP_DECISIONS.tsv": ["direction_id", "family_owner_url", "step13_overlap_state", "step13_remediation", "evidence_boundary"],
        "STEP_14_DELTA_SEARCH_ONLY_ARCHITECTURE.tsv": ["direction_id", "family_owner_unit", "family_owner_url", "step14_architecture_effect", "physical_change", "evidence_boundary"],
        "STEP_15_DELTA_AI_CASE_SELECTION.tsv": ["direction_id", "step15_ai_case_selection", "evidence_boundary"],
        "STEP_16_17_DELTA_STATUS.tsv": ["direction_id", "step16_status", "step17_status", "evidence_boundary"],
        "STEP_18_DELTA_PRIORITY_READINESS.tsv": ["direction_id", "step12_action", "physical_change", "step18_readiness", "evidence_boundary"],
    }.items():
        write_tsv(WORK / step, direction_rows, fields)

    full_master = [*base_master, *full_delta_rows]
    full_master.sort(key=lambda r: norm(r["phrase"]))
    write_tsv(WORK / "POST_STEP09_FINAL_SEMANTIC_MASTER_2856.tsv", full_master, list(base_master[0]))

    unit_increments = Counter(r["final_structural_unit_id"] for r in full_delta_rows)
    units = []
    for row in base_units:
        out = dict(row)
        out["phrase_count"] = str(int(row["phrase_count"]) + unit_increments[row["structural_unit_id"]])
        units.append(out)
    write_tsv(WORK / "POST_STEP09_CANONICAL_UNIT_AUTHORITY.tsv", units, list(base_units[0]))

    unified = []
    for s10, s11 in zip(step10_rows, step11_rows):
        cfg = DIRECTIONS[s10["direction_id"]]
        unified.append({**s10, **{k: v for k, v in s11.items() if k not in s10},
                        "step12_action": cfg["action"], "physical_change": cfg["physical"],
                        "new_page_decision": "REJECTED_NOT_JUSTIFIED", "step13_state": "NO_NEW_CONFLICT_TRIGGER",
                        "step14_effect": "EXISTING_OWNER_OR_FAMILY_ROUTE_ONLY__NO_NEW_URL",
                        "step15_state": "NOT_SELECTED", "step16_17_state": "NOT_REQUIRED", "step18_state": cfg["priority"]})
    write_tsv(WORK / "STEP_05A_POST_STEP09_UNIFIED_DOWNSTREAM_DELTA_AUTHORITY.tsv", unified)

    build_release(accepted, step11_rows, direction_rows)

    protected = {
        "historical_stage5_master": file_record(BASE_MASTER), "historical_stage5_units": file_record(BASE_UNITS),
        "historical_corrected_release_manifest": file_record(BASE_RELEASE / "RELEASE_MANIFEST_2026-09-05.json"),
        "kw002_tree_hash": subprocess.check_output(["git", "rev-parse", "HEAD:extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH"], cwd=REPO, text=True).strip(),
    }
    (WORK / "PROTECTED_ARTIFACT_IDENTITIES.json").write_text(json.dumps(protected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "schema": "OKNO_MSK_STEP5A_POST_STEP09_DOWNSTREAM_REFRESH_V1", "date": "2026-09-09",
        "baseline_rows": 2840, "delta_rows": 16, "union_rows": 2856, "directions": 7,
        "step9_queries": 6, "step9_top10_rows": 60, "provider_requests_reused": 6,
        "provider_cost_reused_rub": 2.928, "new_provider_calls": 0, "new_page_count": 0,
        "exact_owner_resolved_phrases": 9, "exact_owner_hold_phrases": 7,
        "release_path": str(RELEASE.relative_to(JOB)),
    }
    (WORK / "EXECUTION_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_release(accepted: list[dict[str, str]], ownership: list[dict[str, str]], directions: list[dict[str, str]]) -> None:
    sources = RELEASE / "sources"
    editable = RELEASE / "editable"
    sources.mkdir(parents=True, exist_ok=True)
    editable.mkdir(parents=True, exist_ok=True)

    doc1 = (BASE_RELEASE / "sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md").read_text(encoding="utf-8")
    replacements = {
        "2 332 активные поисковые фразы": "2 348 активных поисковых фраз",
        "Для 2 313 из них определена подходящая существующая страница; 19 фраз оставлены": "Для 2 322 из них определена подходящая существующая страница; 26 фраз оставлены",
        "В дальнейший анализ распределения спроса по страницам вошли 2 332 активные поисковые фразы.": "В дальнейший анализ распределения спроса по страницам вошли 2 348 активных поисковых фраз.",
        "Для 2 313 из этих 2 332 фраз удалось определить подходящую существующую страницу. Ещё 19 оставлены": "Для 2 322 из этих 2 348 фраз удалось определить подходящую существующую страницу. Ещё 26 оставлены",
    }
    for old, new in replacements.items():
        doc1 = doc1.replace(old, new)
    appendix = """
### Дополнение после проверки конкурентов

После основного исследования отдельно проверили, какие темы могли быть пропущены при первоначальном сборе. Из 43 направлений 14 передали в Wordstat. В полученных 160 строках выделили 20 формулировок для проверки в обычной выдаче Яндекса. По итогам в ядро добавлены 16 новых поисковых фраз в семи направлениях. Полный сохранённый корпус теперь содержит 2 856 уникальных фраз, из которых 2 348 относятся к активному ядру.

Девять формулировок получили точное назначение на существующую страницу. Для семи сохранён тематический маршрут, но точная страница и возможность внедрения не подтверждены: это шесть вариантов о гидроизоляции открытого балкона и вариант о шумоизоляции крыши изнутри. Они остаются в ядре для дальнейшего решения, но не превращены в новые страницы или готовые задания.

| Направление | Новых фраз | Решение |
|---|---:|---|
| Гидроизоляция открытого балкона | 6 | Сохранить спрос; точный владелец и соответствие услугам требуют подтверждения |
| Солнцезащитный стеклопакет | 3 | Отнести к существующей странице выбора стеклопакетов |
| Многофункциональный стеклопакет | 1 | Отнести к существующему руководству по выбору стеклопакета |
| Ударопрочный стеклопакет | 1 | Отнести к существующей странице выбора стеклопакетов |
| Балкон под рабочее место | 1 | Отнести к существующему разделу комплексного ремонта и остекления балкона |
| Шумоизоляция крыши балкона | 3 | Две фразы относятся к существующей услуге; способ «изнутри» требует подтверждения |
| Армирование оконного профиля | 1 | Отнести к существующей статье о выборе оконного профиля |

Проверка конкурентов использовалась для обнаружения тем, а точные выводы делались только после Wordstat и обычной выдачи Яндекса. Добавленные фразы не означают автоматическое создание новых страниц и не доказывают будущий трафик.
"""
    doc1 = doc1.replace("\n## Как проводилась работа", appendix + "\n## Как проводилась работа", 1)
    doc1_path = sources / "01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.md"
    doc1_path.write_text(doc1, encoding="utf-8")

    doc2 = (BASE_RELEASE / "sources/02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-05.md").read_text(encoding="utf-8")
    assigned = [r for r in ownership if r["exact_query_owner_state"] == "OWNER_EXISTING"]
    held = [r for r in ownership if r["exact_query_owner_state"] != "OWNER_EXISTING"]
    section = ["", "### Дополнительные фразы, назначенные существующим страницам", "",
               "Эти формулировки расширяют семантическое назначение существующих страниц. Сами по себе они не требуют нового раздела сайта и не являются готовым заданием на изменение текста.", "",
               "| Поисковая фраза | Основная страница | Роль |", "|---|---|---|"]
    for r in assigned:
        section.append(f"| {r['phrase']} | {r['exact_query_owner_url']} | Семантическое назначение без физического изменения |")
    section += ["", "### Дополнительные фразы без подтверждённого точного владельца", "",
                "Эти формулировки сохранены в ядре, но не должны передаваться во внедрение до подтверждения точной страницы и границ предложения компании.", "",
                "| Поисковая фраза | Тематический маршрут | Что нужно подтвердить |", "|---|---|---|"]
    for r in held:
        section.append(f"| {r['phrase']} | {r['family_owner_url']} | {r['mapping_reason']} |")
    doc2 = doc2.replace("\n## 5. Проверки перед следующими изменениями", "\n" + "\n".join(section) + "\n\n## 5. Проверки перед следующими изменениями", 1)
    doc2_path = sources / "02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-09.md"
    doc2_path.write_text(doc2, encoding="utf-8")

    shutil.copy2(BASE_RELEASE / "03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.md", RELEASE / "03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.md")

    readme = """# Обновлённый выпуск OKNO_MSK

Выпуск включает результаты дополнительной проверки конкурентных пробелов и их точечное проведение через группировку, назначение страниц и проверку готовности.

- Полное ядро: 2 856 уникальных фраз.
- Добавлено: 16 фраз в семи направлениях.
- Точное назначение существующей странице: 9 фраз.
- Сохранено до подтверждения точного владельца или границы услуги: 7 фраз.
- Новые страницы: 0.
- Новые обращения к провайдерам при этой материализации: 0.

Документ о выдаче Алисы перенесён без содержательных изменений: новые случаи для отдельной проверки по Алисе не потребовались.
"""
    (RELEASE / "README_RU.md").write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
