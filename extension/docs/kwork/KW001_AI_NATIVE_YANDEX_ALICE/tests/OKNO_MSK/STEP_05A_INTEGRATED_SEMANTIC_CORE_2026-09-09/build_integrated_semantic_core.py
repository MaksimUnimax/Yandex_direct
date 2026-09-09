#!/usr/bin/env python3
"""Build one linearly integrated OKNO_MSK semantic authority from preserved evidence.

The materializer performs no network or provider calls. The immutable 2026-09-05
Stage-5 rows are combined with the 16 accepted Step 5A rows before a single
deterministic sort and before the downstream final-state view is emitted.
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve()
WORK = HERE.parent
JOB = HERE.parents[1]
REPO = HERE.parents[7]
PROP = JOB / "STEP_05A_POST_ACCEPTANCE_PROPAGATION_2026-09-08"
FIRST = JOB / "STEP_05A_FIRST_EXECUTION_2026-09-08"
POST9 = JOB / "STEP_05A_POST_STEP09_DOWNSTREAM_REFRESH_2026-09-09"
HIST_RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05"
KW002 = "extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH"

BASE_MASTER = JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"
BASE_UNITS = JOB / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"
UNION_INPUT = PROP / "STEP_05A_POST_ACCEPTANCE_UNION_INPUT.tsv"
FINAL_MASTER = POST9 / "POST_STEP09_FINAL_SEMANTIC_MASTER_2856.tsv"
FINAL_UNITS = POST9 / "POST_STEP09_CANONICAL_UNIT_AUTHORITY.tsv"
DELTA_AUTHORITY = POST9 / "STEP_05A_POST_STEP09_UNIFIED_DOWNSTREAM_DELTA_AUTHORITY.tsv"
ACCEPTED_AUTHORITY = FIRST / "STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv"
EVIDENCE_REGISTER = JOB / "RESEARCH_REBUILD_STAGE_07_EVIDENCE_REGISTER_2026-09-05.tsv"
AI_LEDGER = JOB / "RESEARCH_REBUILD_STAGE_03_AI_CAUSAL_LEDGER_2026-09-05.tsv"

OUT_MASTER = WORK / "FINAL_SEMANTIC_MASTER_STEP05A_INTEGRATED_2026-09-09.tsv"
OUT_ACTIVE = WORK / "FINAL_ACTIVE_SEMANTIC_CORE_STEP05A_INTEGRATED_2026-09-09.tsv"
OUT_UNITS = WORK / "FINAL_PAGE_STRUCTURAL_AUTHORITY_STEP05A_INTEGRATED_2026-09-09.tsv"
OUT_SUMMARY = WORK / "FINAL_SEMANTIC_CORE_STEP05A_INTEGRATED_SUMMARY_2026-09-09.json"
OUT_RECEIPT = WORK / "FINAL_SEMANTIC_CORE_STEP05A_INTEGRATED_RECONCILIATION_RECEIPT_2026-09-09.md"
OUT_PROTECTED = WORK / "PROTECTED_ARTIFACT_IDENTITIES.json"

ACTIVE_STATES = {"ASSIGNED", "ASSIGNED_HOLD", "SEARCH_REQUIRED"}
NO_PAGE_ACTIONS = {"NO_STANDALONE_PAGE", "OUTSIDE_SCOPE_NO_ACTION"}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty authority: {path}")
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def norm(value: str) -> str:
    return " ".join(value.casefold().split())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_info(path: Path) -> dict[str, object]:
    return {"path": str(path.relative_to(JOB)), "bytes": path.stat().st_size, "sha256": digest(path)}


def git_object(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], cwd=REPO, text=True).strip()


def screening_state(final_state: str) -> str:
    if final_state == "EXCLUDED_PRESERVED":
        return "EXCLUDED"
    if final_state == "REVIEW_DEFERRED":
        return "REVIEW_DEFERRED"
    return "ACTIVE"


def exact_owner(row: dict[str, str], delta: dict[str, str] | None) -> tuple[str, str]:
    if delta:
        return delta["exact_query_owner_state"], delta["exact_query_owner_url"]
    if row["step11_effective_assignment_status"] == "SEARCH_REQUIRED":
        return "OWNER_UNRESOLVED_EVIDENCE_REQUIRED", ""
    action = row["canonical_structural_action"]
    if action == "NO_STANDALONE_PAGE":
        return "NO_SUITABLE_EXISTING_PAGE", ""
    if action == "OUTSIDE_SCOPE_NO_ACTION":
        return "OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP", ""
    exact_url = row["final_primary_page"] or row["step11_target_url"]
    if exact_url:
        return "OWNER_EXISTING", exact_url
    if row["step11_effective_assignment_status"] == "ASSIGNED":
        return "ASSIGNED_GOVERNED_NO_URL", ""
    return "OWNER_UNRESOLVED_EVIDENCE_REQUIRED", ""


def new_page_decision(row: dict[str, str]) -> str:
    action = row["canonical_structural_action"]
    if action in {"NEW_COMMERCIAL_PAGE", "NEW_INFORMATIONAL_PAGE"}:
        return "NEW_PAGE_DECISION_PRESENT_IN_ACCEPTED_AUTHORITY"
    if row["final_semantic_state"] in {"SEARCH_REQUIRED", "REVIEW_DEFERRED"} or action == "DEFER_PENDING_EVIDENCE":
        return "NOT_READY__NO_NEW_PAGE_DECISION"
    return "NO_NEW_PAGE"


def site_change(row: dict[str, str], is_step5a: bool) -> str:
    if is_step5a:
        return "NO"
    action = row["canonical_structural_action"]
    if action in {"EXPAND_EXISTING_PAGE", "ADD_SECTION_OR_FAQ_TO_EXISTING", "NEW_COMMERCIAL_PAGE", "NEW_INFORMATIONAL_PAGE", "SPLIT_EXISTING_PAGE", "MERGE_STRUCTURALLY_REDUNDANT_PAGES"}:
        return "YES"
    if action in {"KEEP_EXISTING_STRUCTURE", "ROUTE_TO_EXISTING_PAGE_AS_SUBTASK", "NO_STANDALONE_PAGE", "OUTSIDE_SCOPE_NO_ACTION"}:
        return "NO"
    return "UNRESOLVED"


def main() -> None:
    base = read_tsv(BASE_MASTER)
    final = read_tsv(FINAL_MASTER)
    union = read_tsv(UNION_INPUT)
    units = read_tsv(FINAL_UNITS)
    base_units = read_tsv(BASE_UNITS)
    delta_rows = read_tsv(DELTA_AUTHORITY)
    accepted_rows = read_tsv(ACCEPTED_AUTHORITY)
    evidence = read_tsv(EVIDENCE_REGISTER)
    ai_rows = read_tsv(AI_LEDGER)

    base_fields = list(base[0])
    base_map = {norm(r["phrase"]): r for r in base}
    final_map = {norm(r["phrase"]): r for r in final}
    union_map = {norm(r["phrase"]): r for r in union}
    unit_map = {r["structural_unit_id"]: r for r in units}
    delta_map = {norm(r["phrase"]): r for r in delta_rows}
    accepted_map = {norm(r["phrase"]): r for r in accepted_rows}
    search_map = {norm(r["question_or_query"]): r for r in evidence if r["layer"] == "ORDINARY_YANDEX_SEARCH"}
    ai_map = {norm(r["query"]): r for r in ai_rows}

    assert len(base_map) == 2840
    assert len(delta_map) == 16
    assert set(accepted_map) == set(delta_map)
    assert not (set(base_map) & set(delta_map))
    assert len(final_map) == len(union_map) == 2856
    assert set(final_map) == set(union_map) == set(base_map) | set(delta_map)
    assert all(final_map[k] == v for k, v in base_map.items())

    extra_fields = [
        "normalized_phrase", "canonical_phrase_id", "acquisition_source", "acquisition_stage",
        "source_provenance", "source_record_id", "wordstat_frequency", "frequency_evidence_state",
        "wordstat_region", "wordstat_device_scope", "wordstat_operator_context", "acquisition_date",
        "acquisition_request_id", "raw_evidence_locator", "business_boundary_state", "semantic_state",
        "competitor_discovery_domains", "competitor_page_evidence", "competitor_page_evidence_ids",
        "competitor_candidate_seed", "wordstat_lineage_request_id", "wordstat_lineage_row_id",
        "wordstat_lineage_row_class", "search_representative_query",
        "screening_state", "active_state", "exclusion_review_reason", "demand_direction", "user_task",
        "intent", "query_family", "structural_unit", "exact_assignment_status", "exact_query_owner_state",
        "exact_primary_page", "family_owner", "family_primary_page", "supporting_pages",
        "page_assignment_confidence", "page_assignment_uncertainty", "search_evidence_status",
        "search_evidence_locator", "ai_evidence_status", "ai_evidence_locator", "architecture_decision",
        "new_page_decision", "cannibalization_competing_page_state", "internal_linking_decision",
        "implementation_action_type", "site_change", "readiness_priority_state", "hold_resolution_state",
        "evidence_authority_locator", "methodology_version_provenance",
    ]
    fields = base_fields + extra_fields
    integrated: list[dict[str, object]] = []
    for key in sorted(final_map):
        row = final_map[key]
        demand = union_map[key]
        delta = delta_map.get(key)
        accepted = accepted_map.get(key)
        unit = unit_map.get(row["final_structural_unit_id"], {})
        is_step5a = demand["input_origin"] == "COMPETITOR_DERIVED_STEP5A"
        owner_state, exact_url = exact_owner(row, delta)
        family_owner = delta["family_owner_unit"] if delta else row["final_structural_unit_id"]
        family_url = delta["family_owner_url"] if delta else unit.get("final_primary_page", "")
        support = delta["supporting_pages"] if delta else (row["final_supporting_pages"] or unit.get("final_supporting_pages", ""))
        search = search_map.get(key)
        ai = ai_map.get(key)
        final_state = row["final_semantic_state"]
        active = final_state in ACTIVE_STATES
        search_status = "EXACT_QUERY_SEARCH_EVIDENCE_PRESERVED" if search else demand["search_evidence_state"]
        search_locator = search["source_path"] + "#" + search["evidence_id"] if search else ""
        if delta:
            search_locator = delta["evidence_provenance"]
            search_status = "EXACT_QUERY_SEARCH_EVIDENCE_PRESERVED" if "STEP_09_DELTA" in search_locator else "STEP5A_DISCOVERY_SEARCH_EVIDENCE_PRESERVED"
        reason = ""
        if not active:
            reason = row["explicit_missing_needs"] or row["claim_boundary"] or final_state
        elif owner_state == "OWNER_UNRESOLVED_EVIDENCE_REQUIRED":
            reason = row["explicit_missing_needs"] or (delta["mapping_reason"] if delta else row["claim_boundary"])
        row_id = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
        out: dict[str, object] = dict(row)
        out.update({
            "normalized_phrase": key,
            "canonical_phrase_id": f"OKNO-{row_id}",
            "acquisition_source": "COMPETITOR_GAP_VALIDATED_IN_WORDSTAT" if is_step5a else "BASE_WORDSTAT_ACQUISITION",
            "acquisition_stage": "STEP_05A" if is_step5a else "STEP_03_05_BASE",
            "source_provenance": demand["provenance"],
            "source_record_id": demand["source_record_id"],
            "wordstat_frequency": int(demand["frequency_count"]),
            "frequency_evidence_state": demand["frequency_evidence_state"],
            "wordstat_region": demand["region"],
            "wordstat_device_scope": demand["device_scope"],
            "wordstat_operator_context": demand["operator_context"],
            "acquisition_date": demand["acquisition_date"],
            "acquisition_request_id": demand["acquisition_request_id"],
            "raw_evidence_locator": demand["raw_evidence_locator"],
            "business_boundary_state": row["canonical_business_scope_state"],
            "semantic_state": final_state,
            "competitor_discovery_domains": accepted["competitor_domains"] if accepted else "",
            "competitor_page_evidence": accepted["competitor_page_urls"] if accepted else "",
            "competitor_page_evidence_ids": accepted["competitor_page_evidence_ids"] if accepted else "",
            "competitor_candidate_seed": accepted["candidate_seed"] if accepted else "",
            "wordstat_lineage_request_id": accepted["wordstat_request_id"] if accepted else "",
            "wordstat_lineage_row_id": accepted["wordstat_row_id"] if accepted else "",
            "wordstat_lineage_row_class": accepted["wordstat_row_class"] if accepted else "",
            "search_representative_query": accepted["search_representative_query"] if accepted else "",
            "screening_state": screening_state(final_state),
            "active_state": "YES" if active else "NO",
            "exclusion_review_reason": reason,
            "demand_direction": delta["direction_id"] if delta else row["final_structural_unit_id"],
            "user_task": row["canonical_user_task"],
            "intent": row["canonical_intent_type"],
            "query_family": row["final_structural_unit_id"],
            "structural_unit": row["final_structural_unit_id"],
            "exact_assignment_status": row["step11_effective_assignment_status"],
            "exact_query_owner_state": owner_state,
            "exact_primary_page": exact_url,
            "family_owner": family_owner,
            "family_primary_page": family_url,
            "supporting_pages": support,
            "page_assignment_confidence": delta["ownership_confidence"] if delta else row["canonical_final_confidence"],
            "page_assignment_uncertainty": delta["mapping_applicability"] if delta else row["uncertainty_state"],
            "search_evidence_status": search_status,
            "search_evidence_locator": search_locator,
            "ai_evidence_status": "EXACT_QUERY_AI_CHECK_PRESERVED" if ai else "NOT_USED_FOR_THIS_EXACT_PHRASE",
            "ai_evidence_locator": ai["evidence_refs"] if ai else "",
            "architecture_decision": row["canonical_structural_action"],
            "new_page_decision": new_page_decision(row),
            "cannibalization_competing_page_state": delta["step13_state"] if delta else ("PRESERVED_IN_STEP13_AUTHORITY" if row["final_supporting_pages"] or row["step14a_overlay_ids"] else "NO_ROW_LEVEL_CONFLICT_DECISION"),
            "internal_linking_decision": "SUPPORTING_RELATION_PRESERVED" if support else "NO_ROW_LEVEL_LINK_DECISION",
            "implementation_action_type": delta["step12_action"] if delta else row["canonical_structural_action"],
            "site_change": site_change(row, is_step5a),
            "readiness_priority_state": delta["step18_state"] if delta else row["canonical_recommendation_maturity"],
            "hold_resolution_state": "HOLD_EVIDENCE" if owner_state == "OWNER_UNRESOLVED_EVIDENCE_REQUIRED" else ("SEARCH_REQUIRED" if final_state == "SEARCH_REQUIRED" else "NOT_APPLICABLE"),
            "evidence_authority_locator": row["authority_lineage"],
            "methodology_version_provenance": "KW001_STEPS_03_05_05A_07_08_09_10_11_12_13_14_15_18__2026-09-09",
        })
        integrated.append(out)

    active_rows = [r for r in integrated if r["active_state"] == "YES"]
    unresolved = [r for r in active_rows if r["exact_query_owner_state"] == "OWNER_UNRESOLVED_EVIDENCE_REQUIRED"]
    assigned = [r for r in active_rows if r["exact_assignment_status"] == "ASSIGNED"]
    active_units = {r["structural_unit"] for r in active_rows if r["structural_unit"]}
    assert len(integrated) == 2856
    assert len(active_rows) == 2348
    assert len(assigned) == 2322
    assert len(unresolved) == 26
    assert len(active_units) == 168
    assert len({r["normalized_phrase"] for r in integrated}) == 2856
    assert sum(r["acquisition_stage"] == "STEP_05A" for r in integrated) == 16
    assert all(r["source_provenance"] and r["raw_evidence_locator"] for r in integrated)

    write_tsv(OUT_MASTER, integrated, fields)
    write_tsv(OUT_ACTIVE, active_rows, fields)

    members: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in integrated:
        if row["structural_unit"]:
            members[str(row["structural_unit"])].append(row)
    unit_fields = list(units[0]) + [
        "unified_phrase_count", "active_phrase_count", "exact_assignment_decision_count",
        "exact_existing_page_count", "governed_no_page_count", "unresolved_exact_owner_count",
        "step5a_phrase_count", "demand_frequency_sum_non_additive", "family_owner_unit",
        "family_primary_page", "supporting_pages", "authority_version",
    ]
    integrated_units: list[dict[str, object]] = []
    for unit in sorted(units, key=lambda r: r["structural_unit_id"]):
        rows = members[unit["structural_unit_id"]]
        active_for_unit = [r for r in rows if r["active_state"] == "YES"]
        out: dict[str, object] = dict(unit)
        out.update({
            "unified_phrase_count": len(rows),
            "active_phrase_count": len(active_for_unit),
            "exact_assignment_decision_count": sum(r["exact_assignment_status"] == "ASSIGNED" for r in active_for_unit),
            "exact_existing_page_count": sum(r["exact_query_owner_state"] == "OWNER_EXISTING" for r in active_for_unit),
            "governed_no_page_count": sum(r["exact_query_owner_state"] in {"NO_SUITABLE_EXISTING_PAGE", "OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP", "ASSIGNED_GOVERNED_NO_URL"} for r in active_for_unit),
            "unresolved_exact_owner_count": sum(r["exact_query_owner_state"] == "OWNER_UNRESOLVED_EVIDENCE_REQUIRED" for r in active_for_unit),
            "step5a_phrase_count": sum(r["acquisition_stage"] == "STEP_05A" for r in rows),
            "demand_frequency_sum_non_additive": sum(int(r["wordstat_frequency"]) for r in rows),
            "family_owner_unit": unit["structural_unit_id"],
            "family_primary_page": unit["final_primary_page"],
            "supporting_pages": unit["final_supporting_pages"],
            "authority_version": "STEP05A_INTEGRATED_2026-09-09",
        })
        integrated_units.append(out)
    assert len(integrated_units) == 168
    assert [r["structural_unit_id"] for r in base_units] == [r["structural_unit_id"] for r in units]
    write_tsv(OUT_UNITS, integrated_units, unit_fields)

    state_counts = Counter(r["semantic_state"] for r in integrated)
    source_counts = Counter(r["acquisition_stage"] for r in integrated)
    step5a_positions = [i + 1 for i, r in enumerate(integrated) if r["acquisition_stage"] == "STEP_05A"]
    summary = {
        "schema": "OKNO_MSK_FINAL_SEMANTIC_CORE_STEP05A_INTEGRATED_V1",
        "date": "2026-09-09",
        "status": "MATERIALIZED_PENDING_INDEPENDENT_QA",
        "live_starting_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip(),
        "canonical_rows": len(integrated),
        "base_rows": source_counts["STEP_03_05_BASE"],
        "step5a_rows": source_counts["STEP_05A"],
        "active_rows": len(active_rows),
        "exact_assignment_decision_rows": len(assigned),
        "active_unresolved_exact_owner_rows": len(unresolved),
        "demand_groups": len(active_units),
        "duplicate_normalized_phrases": len(integrated) - len({r["normalized_phrase"] for r in integrated}),
        "state_counts": dict(state_counts),
        "step5a_global_sorted_positions": step5a_positions,
        "step5a_is_late_append": step5a_positions == list(range(2841, 2857)),
        "new_pages_from_step5a": 0,
        "new_physical_site_changes_from_step5a": 0,
        "provider_calls": 0,
        "artifacts": {},
    }
    for path in (OUT_MASTER, OUT_ACTIVE, OUT_UNITS):
        summary["artifacts"][path.name] = file_info(path)
    OUT_SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    protected = {
        "captured_at_head": summary["live_starting_head"],
        "historical_corrected_release_tree": git_object(str(HIST_RELEASE.relative_to(REPO))),
        "historical_stage5_master_blob": git_object(str(BASE_MASTER.relative_to(REPO))),
        "historical_stage5_units_blob": git_object(str(BASE_UNITS.relative_to(REPO))),
        "kw002_tree": git_object(KW002),
        "provider_calls": 0,
    }
    OUT_PROTECTED.write_text(json.dumps(protected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    receipt = f"""# OKNO_MSK — receipt пересборки единого семантического ядра

Дата: 2026-09-09  
Статус: MATERIALIZED_PENDING_INDEPENDENT_QA

## Входы и приоритет authority

1. Неизменяемая историческая база: `{BASE_MASTER.name}` — 2 840 уникальных фраз.
2. Сохранённый acquisition/demand/provenance join: `{UNION_INPUT.name}` — 2 856 строк с полным покрытием частоты и происхождения.
3. Принятый post-Step9 downstream authority: `{FINAL_MASTER.name}`.
4. Разделение точного владельца, семейного владельца и поддерживающих страниц для 16 Step 5A фраз: `{DELTA_AUTHORITY.name}`.
5. Текущая authority групп: `{FINAL_UNITS.name}` — 168 групп.

Историческая база не изменялась. Step 5A дал 16 новых уникальных фраз без пересечения с базовыми 2 840. Обе части объединены до единой сортировки и материализации финальных состояний.

## Результат

- Единый корпус: 2 856 строк.
- Активное ядро: 2 348 строк.
- Завершённое точное решение по назначению: 2 322 строки.
- Активно без доказанного точного владельца: 26 строк.
- Группы спроса: 168.
- Step 5A в едином корпусе: 16 строк, распределены общей сортировкой, не образуют поздний блок.
- Новые страницы из Step 5A: 0.
- Физические изменения сайта только из Step 5A: 0.
- Новые provider calls: 0.

Важно: число 2 322 означает завершённое точное решение по каждой строке, включая управляемые решения «отдельная страница не нужна» и «вне границ». Непустой URL хранится отдельно и не подставляется в такие строки искусственно.

## Контрольные суммы

| Артефакт | SHA-256 | Байт |
|---|---|---:|
| `{OUT_MASTER.name}` | `{digest(OUT_MASTER)}` | {OUT_MASTER.stat().st_size} |
| `{OUT_ACTIVE.name}` | `{digest(OUT_ACTIVE)}` | {OUT_ACTIVE.stat().st_size} |
| `{OUT_UNITS.name}` | `{digest(OUT_UNITS)}` | {OUT_UNITS.stat().st_size} |
"""
    OUT_RECEIPT.write_text(receipt, encoding="utf-8")


if __name__ == "__main__":
    main()
