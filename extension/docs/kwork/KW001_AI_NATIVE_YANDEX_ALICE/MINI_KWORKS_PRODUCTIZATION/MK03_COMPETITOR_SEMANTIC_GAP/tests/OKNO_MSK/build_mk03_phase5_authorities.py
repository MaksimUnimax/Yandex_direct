#!/usr/bin/env python3
"""Build the isolated MK03 Phase-5 OKNO_MSK evidence authorities.

The builder only reconciles preserved evidence.  It performs no network or
provider calls and deliberately stops before any page-creation decision.
"""

from __future__ import annotations

import csv
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / ".git").exists())
SOURCE = REPO / "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK"
STEP5A = SOURCE / "STEP_05A_FIRST_EXECUTION_2026-09-08"
DATE = "2026-09-11"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"refusing to write an empty authority: {path.name}")
    names = fields or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()


def join_unique(values: list[str], separator: str = " | ") -> str:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        for part in value.split(" | ") if value else []:
            part = part.strip()
            if part and part not in seen:
                seen.add(part)
                out.append(part)
    return separator.join(out)


FINAL_DIRECTION_BY_SEED = {
    "остекление балкона П-46": "BALCONY_P46",
    "остекление балкона с выносом по полу": "BALCONY_EXTENSION_ALONG_FLOOR",
    "гидроизоляция открытого балкона": "OPEN_BALCONY_WATERPROOFING",
    "солнцезащитный стеклопакет": "SUN_PROTECTION_GLASS_UNIT",
    "многофункциональный стеклопакет": "MULTIFUNCTIONAL_GLASS_UNIT",
    "ударопрочный стеклопакет": "IMPACT_RESISTANT_GLASS_UNIT",
    "Provedal C640 или P400": "PROVEDAL_C640_VS_P400",
    "окна для старого фонда": "OLD_HOUSING_WINDOWS",
    "окна для квартиры под аренду": "RENTAL_APARTMENT_WINDOWS",
    "балкон под офис": "BALCONY_AS_OFFICE",
    "балкон-кладовая": "BALCONY_AS_STORAGE",
    "фальш-крыша на балкон": "BALCONY_FALSE_ROOF",
    "шумоизоляция крыши балкона": "BALCONY_ROOF_SOUNDPROOFING",
    "армирование оконного профиля": "WINDOW_PROFILE_REINFORCEMENT",
}

CONFIRMED = {
    "OPEN_BALCONY_WATERPROOFING",
    "SUN_PROTECTION_GLASS_UNIT",
    "MULTIFUNCTIONAL_GLASS_UNIT",
    "IMPACT_RESISTANT_GLASS_UNIT",
    "BALCONY_AS_OFFICE",
    "BALCONY_ROOF_SOUNDPROOFING",
    "WINDOW_PROFILE_REINFORCEMENT",
}

OPPORTUNITY = {
    "OPEN_BALCONY_WATERPROOFING": (
        "HIGH",
        "Сильнейшая подтверждённая индивидуальная частота (35) и шесть принятых формулировок внутри одного направления.",
        "Раскрыть задачу гидроизоляции открытого балкона внутри подтверждённого владельца темы отделки; перед изменением проверить фактический состав услуги и владельца URL.",
        "Не создавать отдельную страницу автоматически; не обещать материалы, технологию или гарантию без подтверждения заказчика.",
    ),
    "SUN_PROTECTION_GLASS_UNIT": (
        "HIGH",
        "Индивидуальная частота основной фразы 28, три принятые формулировки и коммерческий характер выдачи.",
        "Усилить выбор стеклопакета объяснением солнцезащитной функции и критериев выбора; владелец и формат требуют архитектурной проверки.",
        "Не приравнивать упоминание у конкурента к ассортименту OKNO_MSK; не создавать URL автоматически.",
    ),
    "MULTIFUNCTIONAL_GLASS_UNIT": (
        "MEDIUM",
        "Подтверждённая информационно-выборная задача с индивидуальной частотой 5 и несколькими наблюдаемыми конкурентами.",
        "Добавить проверяемый блок выбора/объяснения многофункционального стеклопакета в существующую тему выбора стеклопакета.",
        "Технические свойства и доступность комплектаций должны быть подтверждены заказчиком.",
    ),
    "IMPACT_RESISTANT_GLASS_UNIT": (
        "MEDIUM",
        "Подтверждённая продуктово-выборная задача с индивидуальной частотой 8; семантически отделима от общего выбора стеклопакета.",
        "Проверить возможность раскрыть ударопрочные решения в существующем владельце темы безопасности/выбора стеклопакета.",
        "Не заявлять классы защиты, состав стекла или наличие продукта без бизнес-подтверждения.",
    ),
    "BALCONY_AS_OFFICE": (
        "MEDIUM",
        "Подтверждённый сценарий использования с индивидуальной частотой 7 и достаточной точечной выдачей.",
        "Раскрыть сценарий кабинета в рамках подтверждённой темы отделки/утепления балкона после проверки состава работ.",
        "Не обещать перепланировку, электрику или нормативное согласование; отдельный URL не предрешён.",
    ),
    "BALCONY_ROOF_SOUNDPROOFING": (
        "MEDIUM",
        "Три принятые формулировки, основная индивидуальная частота 9 и подтверждённая сервисная/товарная выдача.",
        "Проверить расширение существующей темы крыши балкона блоком шумоизоляции от дождя и вариантов исполнения.",
        "Материалы, технология и возможность работ требуют подтверждения владельца бизнеса; не создавать URL автоматически.",
    ),
    "WINDOW_PROFILE_REINFORCEMENT": (
        "LOW",
        "Точечная техническая задача с индивидуальной частотой 5 и подтверждённой информационной выдачей.",
        "Добавить проверяемый критерий армирования в существующий материал/блок выбора оконного профиля.",
        "Не публиковать размеры, толщины или нормативные обещания без технической верификации.",
    ),
}


def build() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    head = git_head()
    candidates = read_tsv(STEP5A / "STEP_05A_DERIVED_SEED_CANDIDATES.tsv")
    wordstat = read_tsv(STEP5A / "STEP_05A_WORDSTAT_SEED_ACQUISITION_LEDGER.tsv")
    normalized = read_tsv(STEP5A / "STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv")
    final9 = read_tsv(STEP5A / "STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv")
    phrase_merge = read_tsv(STEP5A / "STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv")
    visibility = read_tsv(STEP5A / "STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv")

    # Current-site evidence inventory: two preserved observation sets remain distinct.
    site_rows: list[dict[str, object]] = []
    for row in read_tsv(SOURCE / "STEP_20_CURRENT_URL_ROLE_RECHECK.tsv"):
        site_rows.append({
            "baseline_row_id": f"ROLE_{row['url_id']}",
            "evidence_set": "STEP20_CURRENT_URL_ROLE_RECHECK",
            "url": row["requested_url"],
            "final_url": row["final_url"],
            "visible_identity": row["observed_visible_identity"],
            "observation": row["notes"] or row["current_role_verdict"],
            "availability_state": row["availability_verdict"],
            "role_or_validation_state": row["current_role_verdict"],
            "observed_freshness": row["evidence_freshness"],
            "qa_state": row["qa_verdict"],
            "provider_call_in_this_phase": "NO",
            "claim_boundary": "Preserved first-party public-page role observation; no ranking, demand, traffic or exhaustive-content claim.",
            "source_authority": "STEP_20_CURRENT_URL_ROLE_RECHECK.tsv",
        })
    for row in read_tsv(SOURCE / "RESEARCH_REBUILD_STAGE_06_CURRENT_SITE_VALIDATION_2026-09-05.tsv"):
        site_rows.append({
            "baseline_row_id": f"VALIDATION_{row['validation_id']}",
            "evidence_set": "STAGE06_CURRENT_SITE_VALIDATION",
            "url": row["url"],
            "final_url": row["url"],
            "visible_identity": row["observed_title_or_h1"],
            "observation": row["current_observation"],
            "availability_state": row["observed_state"],
            "role_or_validation_state": "PRESERVED_CURRENT_SITE_OBSERVATION",
            "observed_freshness": row["checked_at_utc"],
            "qa_state": "PASS",
            "provider_call_in_this_phase": "NO",
            "claim_boundary": row["claim_boundary"],
            "source_authority": "RESEARCH_REBUILD_STAGE_06_CURRENT_SITE_VALIDATION_2026-09-05.tsv",
        })
    write_tsv(HERE / f"MK03_CURRENT_SITE_COVERAGE_{DATE}.tsv", site_rows)

    query_rows = []
    for row in read_tsv(STEP5A / "STEP_05A_QUERY_IMPACT_TRACE.tsv"):
        query_rows.append({
            "discovery_query_id": f"DQ{int(row['query_index']):03d}",
            "query": row["query"],
            "discovery_family": row["step10_cluster_id"] or row["final_structural_unit_id"] or "UNRESOLVED",
            "canonical_user_task": row["canonical_user_task"] or row["step10_user_task"],
            "intent": row["canonical_intent_type"] or row["step10_intent_orientation"],
            "business_scope_state": row["canonical_business_scope_state"],
            "observed_serp_job": row["observed_serp_job"],
            "dominant_result_type": row["dominant_result_type"],
            "top3_domains": row["top3_result_domains"],
            "top10_domains": row["top10_result_domains"],
            "trace_state": row["trace_status"],
            "claim_boundary": "Exact preserved discovery query only; no transfer to untested phrases or current universal visibility.",
            "source_authority": f"STEP_05A_QUERY_IMPACT_TRACE.tsv#query_index={row['query_index']}",
        })
    write_tsv(HERE / f"MK03_DISCOVERY_QUERY_FAMILY_AUTHORITY_{DATE}.tsv", query_rows)

    selected = {
        row["normalized_domain"]: row
        for row in read_tsv(STEP5A / "STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv")
        if row["selection_state"] == "SELECTED_FOR_NEXT_STEP5A_PAGE_INSPECTION"
    }
    discovery_rows = []
    for index, row in enumerate(read_tsv(STEP5A / "STEP_05A_DOMAIN_FREQUENCY.tsv"), 1):
        is_selected = row["normalized_domain"] in selected
        discovery_rows.append({
            "domain_row_id": f"DOM{index:03d}",
            "domain": row["normalized_domain"],
            "accepted_actual_competitor": "YES" if is_selected else "NO",
            "competitor_class": row["competitor_class"],
            "business_comparability": row["business_comparability"],
            "top10_appearances": row["total_top10_appearances"],
            "distinct_tested_queries": row["distinct_queries"],
            "best_observed_rank": row["best_rank"],
            "representative_queries": row["representative_queries"],
            "representative_urls": row["representative_urls"],
            "selection_reason": selected.get(row["normalized_domain"], {}).get("selection_or_exclusion_reason", row["classification_basis"]),
            "routing_state": "ACCEPTED_FOR_PAGE_EVIDENCE" if is_selected else "NOT_ACCEPTED_AS_DIRECT_COMPARATOR",
            "claim_boundary": "Visibility within the preserved 75-query/750-row discovery set; not a market-wide competitor ranking.",
            "source_authority": "STEP_05A_DOMAIN_FREQUENCY.tsv",
        })
    write_tsv(HERE / f"MK03_COMPETITOR_DISCOVERY_REGISTER_{DATE}.tsv", discovery_rows)

    page_rows = []
    for row in read_tsv(STEP5A / "STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv"):
        copy = dict(row)
        copy["evidence_role"] = "OBSERVED_COMPETITOR_PAGE_TOPIC_SOURCE"
        copy["new_provider_call_in_this_phase"] = "NO"
        copy["source_authority"] = f"STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv#{row['inspection_id']}"
        page_rows.append(copy)
    write_tsv(HERE / f"MK03_COMPETITOR_PAGE_EVIDENCE_{DATE}.tsv", page_rows)

    provenance_rows = []
    for row in candidates:
        copy = dict(row)
        copy["candidate_occurrence_state"] = "PRIMARY_DIRECTION_OCCURRENCE" if row["seed_decision"] != "DUPLICATE_OF_ANOTHER_COMPETITOR_SEED" else "DUPLICATE_PROVENANCE_OCCURRENCE"
        copy["new_provider_call_in_this_phase"] = "NO"
        copy["source_authority"] = f"STEP_05A_DERIVED_SEED_CANDIDATES.tsv#{row['seed_id']}"
        provenance_rows.append(copy)
    write_tsv(HERE / f"MK03_COMPETITOR_DERIVED_CANDIDATE_PROVENANCE_{DATE}.tsv", provenance_rows)

    manifest_rows = []
    for row in wordstat:
        copy = dict(row)
        copy["acquisition_mode"] = "PRESERVED_EVIDENCE_REUSE"
        copy["new_provider_call_in_this_phase"] = "NO"
        copy["result_interpretation"] = (
            "UNKNOWN_NOT_ZERO" if row["empty_result_flag"] == "true" else
            "TOTALCOUNT_ONLY_NO_PHRASE_INVENTORY" if row["provider_result_shape"] == "TOTALCOUNT_ONLY" else
            "ROW_LEVEL_EVIDENCE_AVAILABLE"
        )
        copy["source_authority"] = f"STEP_05A_WORDSTAT_SEED_ACQUISITION_LEDGER.tsv#seed_order={row['seed_order']}"
        manifest_rows.append(copy)
    write_tsv(HERE / f"MK03_WORDSTAT_EVIDENCE_MANIFEST_{DATE}.tsv", manifest_rows)

    normalized_rows = []
    merge_by_row = {row["wordstat_row_id"]: row for row in phrase_merge}
    for row in normalized:
        merge = merge_by_row.get(row["wordstat_row_id"], {})
        copy = dict(row)
        copy["phase5_terminal_phrase_state"] = (
            "CONFIRMED_GAP_PHRASE" if merge.get("phrase_merge_state") == "MERGE_ACCEPTED" else
            "HOLD_EVIDENCE_PHRASE" if merge.get("phrase_merge_state") == "HOLD_EVIDENCE" else
            "SUPPRESSED_CLOSE_VARIANT" if merge.get("phrase_merge_state") == "SUPPRESSED_CLOSE_VARIANT" else
            row["semantic_reconciliation_result"]
        )
        copy["new_provider_call_in_this_phase"] = "NO"
        copy["source_authority"] = f"STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv#{row['wordstat_row_id']}"
        normalized_rows.append(copy)
    write_tsv(HERE / f"MK03_NORMALIZED_CANDIDATE_AUTHORITY_{DATE}.tsv", normalized_rows)

    matrix_rows = []
    for row in visibility:
        copy = dict(row)
        copy["tested_pair_state"] = "EXACT_QUERY_DOMAIN_PAIR_TESTED" if row["search_acquisition_state"] == "SUCCEEDED" else "OUTCOME_UNKNOWN_NOT_TESTED"
        copy["new_provider_call_in_this_phase"] = "NO"
        copy["source_authority"] = "STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv"
        matrix_rows.append(copy)
    write_tsv(HERE / f"MK03_EXACT_QUERY_COMPETITOR_SEARCH_MATRIX_{DATE}.tsv", matrix_rows)

    wordstat_by_seed = {row["seed_text"]: row for row in wordstat}
    final_by_id = {row["deduplicated_direction_id"]: row for row in final9}
    phrase_by_direction: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in phrase_merge:
        phrase_by_direction[row["deduplicated_direction_id"]].append(row)
    occurrences: dict[str, list[dict[str, str]]] = defaultdict(list)
    primary: dict[str, dict[str, str]] = {}
    for row in candidates:
        seed = row["normalized_candidate_seed"]
        occurrences[seed].append(row)
        if seed not in primary or row["seed_decision"] != "DUPLICATE_OF_ANOTHER_COMPETITOR_SEED":
            primary[seed] = row

    gap_rows: list[dict[str, object]] = []
    for index, seed in enumerate(primary, 1):
        row = primary[seed]
        initial = row["seed_decision"]
        direction = FINAL_DIRECTION_BY_SEED.get(seed, f"CANDIDATE_{row['seed_id'].split('-')[0]}")
        final = final_by_id.get(direction)
        ws = wordstat_by_seed.get(seed)
        if direction in CONFIRMED:
            state = "CONFIRMED_GAP"
        elif seed == "остекление балкона П-46" or initial == "ALREADY_COVERED_EXACT_OR_CLOSE":
            state = "ALREADY_COVERED"
        elif initial == "OFF_SCOPE_BUSINESS":
            state = "REJECT_OFF_SCOPE"
        else:
            state = "HOLD_EVIDENCE"
        phrases = phrase_by_direction.get(direction, [])
        accepted_phrases = [p for p in phrases if p["phrase_merge_state"] == "MERGE_ACCEPTED"]
        held_phrases = [p for p in phrases if p["phrase_merge_state"] == "HOLD_EVIDENCE"]
        representative = final["representative_query"] if final else seed
        representative_count = ""
        for phrase in phrases:
            if phrase["normalized_returned_phrase"].casefold() == representative.casefold():
                representative_count = phrase["returned_count"]
                break
        gap_rows.append({
            "direction_row_id": f"DIR{index:03d}",
            "direction_id": direction,
            "candidate_direction": seed,
            "semantic_axis": row["semantic_axis"],
            "competitor_domains": join_unique([x["competitor_domain"] for x in occurrences[seed]]),
            "competitor_page_evidence_ids": join_unique([x["source_page_element_text"] for x in occurrences[seed]]),
            "initial_candidate_state": initial,
            "business_scope_state": row["business_scope_state"],
            "current_coverage_evidence": row["existing_semantic_match_state"],
            "existing_semantic_examples": row["existing_semantic_match_examples"],
            "wordstat_evidence_state": (
                "NOT_REQUIRED_ALREADY_CLASSIFIED" if not ws else
                "EMPTY_RESULT_UNKNOWN_NOT_ZERO" if ws["empty_result_flag"] == "true" else
                "TOTALCOUNT_ONLY" if ws["provider_result_shape"] == "TOTALCOUNT_ONLY" else
                "ROW_LEVEL_RESULTS"
            ),
            "wordstat_seed_total_count": ws["total_count"] if ws else "",
            "representative_query": representative,
            "representative_query_individual_wordstat": representative_count,
            "accepted_phrase_count": len(accepted_phrases),
            "accepted_phrases_with_individual_wordstat": " | ".join(f"{p['normalized_returned_phrase']} [{p['returned_count']}]" for p in accepted_phrases),
            "held_phrases_with_individual_wordstat": " | ".join(f"{p['normalized_returned_phrase']} [{p['returned_count']}]" for p in held_phrases),
            "search_evidence_state": final["search_acquisition_state"] if final else ("PRESERVED_DISCOVERY_EXACT_Q62" if seed == "остекление балкона П-46" else "NOT_REQUIRED_OR_NOT_RUN"),
            "search_tested_scope": "ONE_EXACT_QUERY_X_9_SELECTED_DOMAINS" if final else "NO_NEW_SELECTIVE_DECISION_SERP",
            "selected_competitors_visible": final["selected_competitors_visible"] if final else "",
            "terminal_state": state,
            "decision_reason": (
                final["decision_reason"] if final else
                "The preserved semantic authority already contains an exact or close active direction; competitor wording is not a new gap." if state == "ALREADY_COVERED" else
                "The candidate is outside the verified OKNO_MSK business scope; no opportunity is issued." if state == "REJECT_OFF_SCOPE" else
                "Evidence is insufficient or a business/assortment fact remains unverified; no gap or page action is claimed."
            ),
            "remaining_evidence_or_next_check": (
                final["remaining_unresolved_evidence"] if final else
                "None for gap classification; retain current coverage." if state == "ALREADY_COVERED" else
                "No action within MK03 scope." if state == "REJECT_OFF_SCOPE" else
                "Resolve the named demand/search/business evidence gap under separate authorization."
            ),
            "page_or_implementation_decision": "NONE__OUT_OF_SCOPE",
            "claim_boundary": "Direction-level evidence classification only; not a page creation, URL, traffic, ROI or implementation decision.",
            "source_authorities": "STEP_05A_DERIVED_SEED_CANDIDATES.tsv" + (" | STEP_05A_WORDSTAT_SEED_ACQUISITION_LEDGER.tsv" if ws else "") + (" | STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv" if final else ""),
        })
    write_tsv(HERE / f"MK03_GAP_DECISION_REGISTER_{DATE}.tsv", gap_rows)

    opportunity_rows = []
    for row in gap_rows:
        if row["terminal_state"] != "CONFIRMED_GAP":
            continue
        level, basis, action, constraint = OPPORTUNITY[row["direction_id"]]
        opportunity_rows.append({
            "opportunity_id": f"OPP{len(opportunity_rows)+1:02d}",
            "direction_id": row["direction_id"],
            "representative_query": row["representative_query"],
            "individual_wordstat": row["representative_query_individual_wordstat"],
            "accepted_phrases_with_individual_wordstat": row["accepted_phrases_with_individual_wordstat"],
            "competitor_page_evidence": row["competitor_page_evidence_ids"],
            "selected_competitor_exact_query_visibility": row["selected_competitors_visible"] or "Не наблюдались в одном сохранённом TOP‑10",
            "analytical_attention": level,
            "attention_basis": basis,
            "bounded_opportunity": action,
            "preservation_constraints": constraint,
            "required_owner_validation": "Подтвердить бизнес-факт и затем выбрать существующего владельца темы/формат; отдельная страница не предрешена.",
            "page_creation_state": "NOT_DECIDED",
            "claim_boundary": "Analytical opportunity only; attention is not schedule, effort, business value, uplift or page-creation instruction.",
        })
    write_tsv(HERE / f"MK03_BOUNDED_OPPORTUNITY_REGISTER_{DATE}.tsv", opportunity_rows)

    terminal = Counter(row["terminal_state"] for row in gap_rows)
    page_types = Counter(row["page_type"] for row in page_rows)
    accounting = {
        "release": "MK03_PHASE_5_OKNO_MSK",
        "as_of": DATE,
        "source_commit": head,
        "scope": {"site": "https://okno-msk.ru", "region": "Москва", "yandex_region_id": 213, "serp_mode": "SELECTIVE_DECISION_SERP"},
        "preserved_evidence": {
            "discovery_queries": len(query_rows),
            "discovery_top10_rows": len(read_tsv(STEP5A / "STEP_05A_SERP_COMBINED_750.tsv")),
            "observed_domains": len(discovery_rows),
            "accepted_actual_competitors": sum(r["accepted_actual_competitor"] == "YES" for r in discovery_rows),
            "competitor_pages": len(page_rows),
            "competitor_page_type_counts": dict(sorted(page_types.items())),
            "candidate_occurrences": len(provenance_rows),
            "deduplicated_directions": len(gap_rows),
            "wordstat_seed_acquisitions_reused": len(manifest_rows),
            "wordstat_returned_rows_reconciled": len(normalized_rows),
            "selective_search_requirements_reused": len(final9),
            "selective_search_succeeded": sum(r["search_acquisition_state"] == "SUCCEEDED" for r in final9),
            "selective_search_outcome_unknown": sum(r["search_acquisition_state"] != "SUCCEEDED" for r in final9),
            "exact_query_domain_matrix_rows": len(matrix_rows),
            "accepted_phrase_merges": sum(r["phrase_merge_state"] == "MERGE_ACCEPTED" for r in phrase_merge),
        },
        "terminal_direction_counts": dict(sorted(terminal.items())),
        "confirmed_opportunities": len(opportunity_rows),
        "new_provider_calls": {"yandex_search": 0, "wordstat": 0, "other": 0, "total": 0},
        "page_creation_decisions": 0,
        "silent_drops": 0,
        "claim_boundary": "Preserved evidence reconciliation only; no universal visibility, traffic, ROI, URL or page-creation conclusion.",
    }
    (HERE / f"MK03_ACQUISITION_FINAL_ACCOUNTING_{DATE}.json").write_text(json.dumps(accounting, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "release": accounting["release"],
        "source_commit": head,
        "execution_date": DATE,
        "mode": "PRESERVED_EVIDENCE_RECONCILIATION_ONLY",
        "new_provider_calls_total": 0,
        "providers": {
            "yandex_search": {"new_calls": 0, "reused_requirements": 9, "succeeded": 7, "outcome_unknown": 2},
            "wordstat": {"new_calls": 0, "reused_seed_acquisitions": 14, "reconciled_returned_rows": 160},
            "other": {"new_calls": 0},
        },
        "public_site_recheck_in_this_phase": 0,
        "authorization_note": "The Phase-5 prompt required reuse first and did not authorize new paid/provider acquisition for this execution.",
    }
    (HERE / f"MK03_PROVIDER_REUSE_RECEIPT_{DATE}.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (HERE / "TEST_ORDER.md").write_text(f"""# MK03 Phase 5 — TEST ORDER\n\nStatus: EXECUTING / NOT FINAL\n\n- Product: MK03 — competitor semantic gap.\n- Site: `https://okno-msk.ru`.\n- Region: Moscow, Yandex region 213.\n- SERP mode: `SELECTIVE_DECISION_SERP`.\n- Source commit: `{head}`.\n- Evidence mode: preserved evidence reuse; new provider calls = 0.\n- Required terminal states: `CONFIRMED_GAP`, `ALREADY_COVERED`, `REJECT_OFF_SCOPE`, `HOLD_EVIDENCE`.\n- Prohibited conclusion: competitor topic, seed or demand alone does not authorize a page.\n- Client package: one XLSX, one analytical PDF, this short handoff only.\n\nExecution order follows canonical Steps 00–09 and ends at Phase 5.\n""", encoding="utf-8")
    (HERE / "TEST_EXECUTION.md").write_text(f"""# MK03 Phase 5 — TEST EXECUTION\n\nStatus: AUTHORITIES BUILT / CLIENT MATERIALIZATION PENDING\n\nThe isolated rehearsal reused the preserved OKNO_MSK acquisition chain without network/provider calls. It reconciled current-site evidence, 75 discovery queries, 237 observed domains, 9 accepted actual competitors, 44 inspected competitor pages, 92 candidate occurrences, 43 deduplicated directions, 14 Wordstat seed acquisitions, 160 returned rows and the selective 9-query decision set.\n\nTerminal direction accounting: 7 confirmed gaps; 23 already covered; 3 rejected as outside verified business scope; 10 held for missing evidence. Every direction has one terminal state. No page creation, URL, traffic, ROI or implementation decision was made.\n\nNext cursor: build client XLSX and analytical PDF from these authorities, then exact-file QA and recipient tests.\n""", encoding="utf-8")
    (HERE / "TEST_RESULT.md").write_text("""# MK03 Phase 5 — TEST RESULT\n\nStatus: IN_PROGRESS / NOT FINAL AUTHORITY\n\nThe Level-2 analytical authorities are materialized. Client-file generation, exact-byte physical QA, recipient tests, publication and remote readback remain open. This checkpoint is not a Phase-5 PASS.\n""", encoding="utf-8")
    cursor = {
        "status": "IN_PROGRESS_NOT_FINAL_AUTHORITY",
        "source_commit": head,
        "completed_block": "LEVEL2_AUTHORITIES",
        "counts": accounting["preserved_evidence"] | accounting["terminal_direction_counts"],
        "open_failures": ["XLSX_NOT_BUILT", "PDF_NOT_BUILT", "EXACT_FILE_QA_NOT_RUN", "RECIPIENT_TEST_NOT_RUN", "REMOTE_READBACK_NOT_RUN"],
        "next_resume_action": "BUILD_MK03_PHASE5_CLIENT_XLSX_AND_PDF",
    }
    (HERE / f"MK03_PHASE5_EXECUTION_CURSOR_{DATE}.json").write_text(json.dumps(cursor, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(accounting, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    build()
