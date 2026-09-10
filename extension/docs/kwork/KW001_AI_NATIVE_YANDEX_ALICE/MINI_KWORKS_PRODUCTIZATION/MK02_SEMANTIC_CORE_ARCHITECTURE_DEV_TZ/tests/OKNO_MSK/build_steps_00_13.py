#!/usr/bin/env python3
"""Deterministic preserved-evidence projection for MK02 OKNO_MSK steps 00-13."""

from __future__ import annotations

import base64
import csv
import gzip
import hashlib
import io
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


HERE = Path(__file__).resolve().parent


def find_repo_root() -> Path:
    path = HERE
    while path != path.parent:
        if (path / ".git").exists():
            return path
        path = path.parent
    raise RuntimeError("repository root not found")


REPO = find_repo_root()
PARENT = REPO / "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE"
SOURCE = PARENT / "tests/OKNO_MSK"
MK01 = (
    PARENT
    / "MINI_KWORKS_PRODUCTIZATION/MK01_SEMANTIC_CORE_CLUSTERING/tests/OKNO_MSK"
)
DATE = "2026-09-10"

STEP5A_PHRASES = {
    "армирование оконного профиля",
    "балконы под офис",
    "гидроизоляция балконной плиты открытого балкона",
    "гидроизоляция для открытого балкона",
    "гидроизоляция открытого балкона в частном доме",
    "гидроизоляция открытого деревянного балкона",
    "как сделать гидроизоляцию на открытом балконе",
    "лучшая гидроизоляция для открытого балкона",
    "многофункциональный стеклопакет что это",
    "солнцезащитное стекло в стеклопакете",
    "солнцезащитный стеклопакет",
    "солнцезащитный стеклопакет rehau",
    "ударопрочный стеклопакет",
    "шумоизоляция крыши балкона изнутри от дождя",
    "шумоизоляция крыши балкона от дождя",
    "шумоизоляция на крышу балкона",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tsv_bytes(rows: list[dict[str, object]], fields: list[str]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=fields,
        delimiter="\t",
        lineterminator="\n",
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.write_bytes(tsv_bytes(rows, fields))


def write_tsv_gz(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    raw = tsv_bytes(rows, fields)
    with path.open("wb") as target:
        with gzip.GzipFile(filename="", mode="wb", fileobj=target, compresslevel=9, mtime=0) as zipped:
            zipped.write(raw)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_urls(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def normalize_path(url_or_path: str) -> str:
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        parsed = urlparse(url_or_path)
        value = parsed.path or "/"
        if parsed.query:
            value += "?" + parsed.query
        return value
    return url_or_path or "/"


def action_projection(action: str) -> tuple[str, str, str]:
    if action in {"ADD_SECTION_OR_FAQ_TO_EXISTING", "EXPAND_EXISTING_PAGE"}:
        return "CONTENT_CHANGE", "YES", "ACTION"
    if action == "DEFER_PENDING_EVIDENCE":
        return "DEFER", "UNRESOLVED", "DEFER"
    if action == "KEEP_EXISTING_STRUCTURE":
        return "KEEP", "NO", "NO_CHANGE"
    if action == "ROUTE_TO_EXISTING_PAGE_AS_SUBTASK":
        return "SEMANTIC_MAPPING_ONLY", "NO", "NO_CHANGE"
    if action in {"NO_STANDALONE_PAGE", "OUTSIDE_SCOPE_NO_ACTION"}:
        return "NO_CHANGE", "NO", "NO_CHANGE"
    raise AssertionError(f"unmapped structural action: {action}")


def main() -> None:
    semantic_source = SOURCE / "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv"
    mk01_source = MK01 / "MK01_SEMANTIC_UNIVERSE_2026-09-09.tsv.gz"
    stage5_source = SOURCE / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"
    unit_source = SOURCE / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"
    step12_source = SOURCE / "STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv"

    semantic_base = read_tsv(semantic_source)
    mk01_rows = read_tsv(mk01_source)
    stage5_rows = read_tsv(stage5_source)
    unit_rows = read_tsv(unit_source)
    step12_rows = read_tsv(step12_source)

    assert len(semantic_base) == len(mk01_rows) == len(stage5_rows) == 2840
    assert len({row["phrase"] for row in semantic_base}) == 2840
    assert len({row["Поисковая фраза"] for row in mk01_rows}) == 2840
    assert len({row["phrase"] for row in stage5_rows}) == 2840
    assert not (STEP5A_PHRASES & {row["phrase"] for row in semantic_base})

    semantic_by_phrase = {row["phrase"]: row for row in semantic_base}
    stage5_by_phrase = {row["phrase"]: row for row in stage5_rows}
    unit_by_id = {row["structural_unit_id"]: row for row in unit_rows}
    step12_by_id = {row["structural_unit_id"]: row for row in step12_rows}
    assert set(semantic_by_phrase) == set(stage5_by_phrase) == {
        row["Поисковая фраза"] for row in mk01_rows
    }
    assert len(unit_rows) == len(unit_by_id) == len(step12_rows) == len(step12_by_id) == 168

    # Exact phrase-level ordinary Search observations are kept distinct from owner decisions.
    direct_query_urls: dict[str, list[str]] = defaultdict(list)
    step11_search = SOURCE / "STEP_11_SEARCH_PROJECTION_RECOVERY_01_000_019_2026-08-30.tsv"
    for row in read_tsv(step11_search):
        query = row.get("QUERY_TEXT") or ""
        if query and "okno-msk.ru" in (row.get("DOMAIN") or ""):
            direct_query_urls[query].append(row["URL"])
        elif query:
            direct_query_urls.setdefault(query, [])
    for path in sorted(SOURCE.glob("STEP_13_SEARCH_RESULT_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        query = payload.get("query") or ""
        urls = [
            item["url"]
            for item in payload.get("results", [])
            if "okno-msk.ru" in (item.get("domain") or "")
        ]
        if query:
            direct_query_urls[query].extend(urls)

    foundation: list[dict[str, object]] = []
    phrase_map: list[dict[str, object]] = []
    active_unit_phrase_rows: dict[str, list[dict[str, object]]] = defaultdict(list)

    for client_row in mk01_rows:
        phrase = client_row["Поисковая фраза"]
        raw = semantic_by_phrase[phrase]
        downstream = stage5_by_phrase[phrase]
        foundation_row = {
            "phrase_id": client_row["ID фразы (для аудита)"],
            "phrase": phrase,
            "product_status": client_row["Итоговый статус"],
            "in_working_core": client_row["В рабочем ядре"],
            "group_id": client_row["Код группы (для аудита)"],
            "group_name": client_row["Группа запросов"],
            "user_task": client_row["Задача пользователя"],
            "intent": client_row["Интент"],
            "topic_role": client_row["Роль темы"],
            "decision_basis": client_row["Основание решения"],
            "uncertainty": client_row["Уверенность"],
            "wordstat_popular_count": client_row["Число запросов — популярные"],
            "wordstat_associated_count": client_row["Число запросов — похожие"],
            "wordstat_evidence_type": client_row["Тип данных Вордстата"],
            "source_occurrences": raw["source_occurrences"],
            "source_ids": raw["source_ids"],
            "search_stage_disposition": raw["search_stage_disposition"],
            "structural_unit_id_crosscheck": downstream["final_structural_unit_id"],
            "source_authority": "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv + accepted MK01 overlay",
        }
        foundation.append(foundation_row)

        if client_row["В рабочем ядре"] != "Да":
            continue

        owner_state = downstream["step11_ownership_state"]
        exact_url = downstream["step11_target_url"]
        if owner_state == "OWNER_EXISTING":
            assert exact_url
        else:
            assert not exact_url
        observed_urls = sorted(set(direct_query_urls.get(phrase, [])))
        if phrase in direct_query_urls:
            observation_state = (
                "EXACT_QUERY_TARGET_URL_OBSERVED"
                if observed_urls
                else "EXACT_QUERY_CHECK__TARGET_HOST_NOT_OBSERVED_IN_TOP10"
            )
        else:
            observation_state = "NOT_DIRECTLY_CHECKED_AT_EXACT_PHRASE_LEVEL"
        mapping_use = {
            "OWNER_EXISTING": "EXACT_OWNER_AVAILABLE",
            "NO_SUITABLE_EXISTING_PAGE": "NO_EXACT_OWNER__FAMILY_ROUTE_OR_NO_PAGE_BOUNDARY",
            "OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP": "OUTSIDE_SCOPE_NO_TARGET",
            "PAGE_OWNERSHIP_NOT_APPLICABLE_UNTIL_TASK_RESOLVED": "OWNER_UNRESOLVED_EVIDENCE_REQUIRED",
        }[owner_state]
        mapped = {
            "phrase_id": client_row["ID фразы (для аудита)"],
            "phrase": phrase,
            "semantic_group_id": client_row["Код группы (для аудита)"],
            "semantic_group_name": client_row["Группа запросов"],
            "user_task": client_row["Задача пользователя"],
            "intent": client_row["Интент"],
            "topic_role": client_row["Роль темы"],
            "structural_unit_id": downstream["final_structural_unit_id"],
            "exact_owner_state": owner_state,
            "exact_owner_url": exact_url,
            "family_owner_url": downstream["final_primary_page"],
            "supporting_pages": downstream["final_supporting_pages"],
            "observed_search_relevant_url": ";".join(observed_urls),
            "observed_search_evidence_scope": observation_state,
            "structural_action": downstream["canonical_structural_action"],
            "mapping_use": mapping_use,
            "uncertainty_state": downstream["uncertainty_state"],
            "ownership_evidence_locator": (
                "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv#phrase="
                + phrase
            ),
            "claim_boundary": "OWNER_ROLE_LAYERS_SEPARATE__OBSERVED_SEARCH_URL_NOT_INFERRED",
        }
        phrase_map.append(mapped)
        if downstream["final_structural_unit_id"]:
            active_unit_phrase_rows[downstream["final_structural_unit_id"]].append(mapped)

    assert len(foundation) == 2840
    assert Counter(row["in_working_core"] for row in foundation) == Counter({"Да": 2185, "Нет": 655})
    assert len(phrase_map) == 2185
    assert len({row["phrase"] for row in phrase_map}) == 2185
    assert Counter(row["product_status"] for row in foundation) == Counter(
        {
            "В рабочем ядре": 2185,
            "Исключено после построчной очистки": 334,
            "Проверка отложена": 174,
            "Исключено после смысловой группировки": 134,
            "Нужна проверка в обычной выдаче Яндекса": 13,
        }
    )
    assert Counter(row["exact_owner_state"] for row in phrase_map) == Counter(
        {
            "OWNER_EXISTING": 1647,
            "NO_SUITABLE_EXISTING_PAGE": 518,
            "OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP": 14,
            "PAGE_OWNERSHIP_NOT_APPLICABLE_UNTIL_TASK_RESOLVED": 6,
        }
    )

    foundation_fields = list(foundation[0])
    phrase_map_fields = list(phrase_map[0])
    foundation_path = HERE / f"MK02_SEMANTIC_FOUNDATION_{DATE}.tsv.gz"
    phrase_map_path = HERE / f"MK02_PHRASE_PAGE_MAP_{DATE}.tsv.gz"
    write_tsv_gz(foundation_path, foundation, foundation_fields)
    write_tsv_gz(phrase_map_path, phrase_map, phrase_map_fields)

    unit_ledger: list[dict[str, object]] = []
    structural_actions: list[dict[str, object]] = []
    for unit in unit_rows:
        uid = unit["structural_unit_id"]
        active_rows = active_unit_phrase_rows.get(uid, [])
        owner_states = sorted({str(row["exact_owner_state"]) for row in active_rows})
        exact_urls = sorted({str(row["exact_owner_url"]) for row in active_rows if row["exact_owner_url"]})
        current = step12_by_id[uid]
        product_state = "ACTIVE_MK02_WORKING_CORE" if active_rows else "INACTIVE_CROSSCHECK_ONLY"
        summary = owner_states[0] if len(owner_states) == 1 else (
            "MIXED_EXACT_PHRASE_OWNERSHIP" if owner_states else "NOT_APPLICABLE_INACTIVE"
        )
        unit_row = {
            "structural_unit_id": uid,
            "product_state": product_state,
            "source_phrase_count_pre_step5a": unit["phrase_count"],
            "active_mk02_phrase_count": len(active_rows),
            "user_task": unit["user_task"],
            "intent_type": unit["intent_type"],
            "business_scope_state": unit["business_scope_state"],
            "unit_page_role": unit["unit_page_role"],
            "exact_owner_state_summary": summary,
            "exact_owner_urls": ";".join(exact_urls),
            "family_owner_url": unit["final_primary_page"],
            "supporting_pages": unit["final_supporting_pages"],
            "structural_action": unit["structural_action"],
            "recommendation_maturity": unit["recommendation_maturity"],
            "final_confidence": unit["final_confidence"],
            "uncertainty_state": unit["uncertainty_state"],
            "gap_type": unit["gap_type"],
            "content_enhancement_state": unit["content_enhancement_state"],
            "direct_serp_queries": current["direct_serp_queries"],
            "owner_goal_evidence_source": current["owner_goal_evidence_source"],
            "evidence_locator": (
                "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv#"
                + uid
            ),
        }
        unit_ledger.append(unit_row)
        if not active_rows:
            continue
        action_class, real_change, disposition = action_projection(unit["structural_action"])
        structural_actions.append(
            {
                "structural_unit_id": uid,
                "active_phrase_count": len(active_rows),
                "user_task": unit["user_task"],
                "family_owner_url": unit["final_primary_page"],
                "supporting_pages": unit["final_supporting_pages"],
                "source_structural_action": unit["structural_action"],
                "action_class": action_class,
                "disposition": disposition,
                "structural_gap": "YES" if unit["gap_type"] not in {"", "NONE"} else "NO",
                "content_enhancement_gap": (
                    "YES" if unit["content_enhancement_state"] == "QUALITY_GAP" else
                    "UNRESOLVED" if unit["content_enhancement_state"] in {"CONTENT_EVIDENCE_INSUFFICIENT", "NOT_ASSESSED"} else
                    "NO"
                ),
                "real_site_change_required": real_change,
                "create": "NO",
                "split": "NO",
                "merge": "NO",
                "redirect_or_delete": "NO",
                "diagnosis_evidence_meaning": current["gap_evidence"],
                "current_content_evidence": current["current_content_evidence"],
                "explicit_missing_needs": unit["explicit_missing_needs"],
                "uncertainty_state": unit["uncertainty_state"],
                "evidence_locator": f"STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv#{uid}",
            }
        )

    assert len(unit_ledger) == 168
    assert len(structural_actions) == 160
    write_tsv(HERE / f"MK02_UNIT_OWNERSHIP_LEDGER_{DATE}.tsv", unit_ledger, list(unit_ledger[0]))
    write_tsv(
        HERE / f"MK02_STRUCTURAL_ACTIONS_{DATE}.tsv",
        structural_actions,
        list(structural_actions[0]),
    )

    candidate_rows = read_tsv(SOURCE / "STEP_11_CLUSTER_PAGE_CANDIDATES.tsv")
    candidate_ledger: list[dict[str, object]] = []
    for row in candidate_rows:
        candidate_ledger.append(
            {
                "cluster_id": row["CLUSTER_ID"],
                "cluster_user_task": row["CLUSTER_USER_TASK"],
                "business_fit": row["BUSINESS_FIT"],
                "candidate_urls": row["CANDIDATE_URLS"],
                "candidate_comparison_count": len(split_urls(row["CANDIDATE_URLS"])),
                "candidate_page_evidence": row["CANDIDATE_PAGE_PROFILE_EVIDENCE"],
                "direct_search_evidence": row["DIRECT_SEARCH_EVIDENCE"],
                "review_result": row["CANDIDATE_REVIEW_RESULT"],
                "unresolved_route": row["UNRESOLVED_EVIDENCE_ROUTE"],
                "last_verified": row["LAST_VERIFIED"],
                "authority_state": "REUSABLE_INDEPENDENT_EVIDENCE",
            }
        )
    assert len(candidate_ledger) == 59
    assert sum(int(row["candidate_comparison_count"]) for row in candidate_ledger) == 105
    write_tsv(
        HERE / f"MK02_OWNERSHIP_CANDIDATE_LEDGER_{DATE}.tsv",
        candidate_ledger,
        list(candidate_ledger[0]),
    )

    diagnosis = read_tsv(SOURCE / "STEP_13_CONFLICT_DIAGNOSIS.tsv")
    remediation = {
        row["case_id"]: row
        for row in read_tsv(SOURCE / "STEP_13_REMEDIATION_RECOMMENDATIONS.tsv")
    }
    family_cases = {
        row["case_id"]: row
        for row in read_tsv(SOURCE / "STEP_13_QUERY_FAMILY_CASES.tsv")
    }
    competing_cases: list[dict[str, object]] = []
    for row in diagnosis:
        cid = row["case_id"]
        competing_cases.append(
            {
                "case_id": cid,
                "query_family": row["query_family"],
                "representative_query": row["representative_query"],
                "candidate_urls": family_cases[cid]["candidate_urls"],
                "primary_owner": row["primary_owner"],
                "supporting_or_other_url": row["supporting_or_other_url"],
                "relation_class": row["final_verdict"],
                "current_public_evidence_mode": row["evidence_mode"],
                "private_query_url_history": "UNAVAILABLE_NOT_USED",
                "historical_competition_state": "NOT_PROVEN_PRIVATE_HISTORY_UNAVAILABLE",
                "harmful_impact_state": "NOT_PROVEN",
                "destructive_action_authorized": "NO",
                "recommendation": remediation[cid]["recommendation"],
                "decision_note": row["decision_note"],
                "claim_boundary": row["evidence_scope"],
            }
        )
    assert len(competing_cases) == 21
    assert all(row["destructive_action_authorized"] == "NO" for row in competing_cases)
    write_tsv(
        HERE / f"MK02_COMPETING_PAGE_CASES_{DATE}.tsv",
        competing_cases,
        list(competing_cases[0]),
    )

    # Decode the accepted lossless current-minus-upstream transport.
    transport = json.loads(
        (SOURCE / "STEP_14A_CURRENT_SITE_RECONCILIATION_TRANSPORT.json").read_text(encoding="utf-8")
    )
    chunk_names = transport.get("chunks") or transport.get("parts") or transport.get("chunk_files")
    if not chunk_names:
        chunk_names = transport["ordered_chunk_files"]
    chunk_files = [item["file"] if isinstance(item, dict) else item for item in chunk_names]
    encoded = "".join((SOURCE / name).read_text(encoding="utf-8").strip() for name in chunk_files)
    decoded = gzip.decompress(base64.b64decode(encoded))
    assert hashlib.sha256(decoded).hexdigest() == "d7329636c7959dcb44f93f59699720e4945ee740ce94b88e3acc033fa457fc6a"
    current_minus = list(csv.DictReader(io.StringIO(decoded.decode("utf-8")), delimiter="\t"))
    assert len(current_minus) == 2624

    current_nodes: list[dict[str, object]] = []
    known_paths: set[str] = set()
    for row in read_tsv(SOURCE / "STEP_14_CURRENT_URL_RECHECK.tsv"):
        path = normalize_path(row["url"])
        assert path not in known_paths
        known_paths.add(path)
        current_nodes.append(
            {
                "current_url": row["url"],
                "path": path,
                "source_layer": "STEP14_KNOWN_CURRENT_RECHECK",
                "fetch_state": row["live_state"],
                "architecture_class": "UPSTREAM_ACCEPTED_CURRENT",
                "reason_code": "CRITICAL_OWNER_OR_SUPPORT_PAGE_RECHECKED",
                "current_role": row["step13_page_role"],
                "current_task": row["step13_primary_user_task"],
                "snapshot_date": "2026-09-01",
                "freshness_boundary": "PRESERVED_PUBLIC_SNAPSHOT__NO_REHEARSAL_REFETCH",
            }
        )
    for row in current_minus:
        path = row["path"]
        assert path not in known_paths
        known_paths.add(path)
        current_nodes.append(
            {
                "current_url": "https://okno-msk.ru" + (path if path.startswith("/") else "/" + path),
                "path": path,
                "source_layer": "STEP14A_RUN10_CURRENT_MINUS_UPSTREAM",
                "fetch_state": row["source_status"],
                "architecture_class": row["architecture_class"],
                "reason_code": row["reason_code"],
                "current_role": "",
                "current_task": "",
                "snapshot_date": "2026-09-02",
                "freshness_boundary": "PRESERVED_PUBLIC_SNAPSHOT__OPERATIONAL_COMPLETENESS_NOT_MATHEMATICAL_EXHAUSTIVENESS",
            }
        )
    assert len(current_nodes) == len(known_paths) == 2683
    current_path = HERE / f"MK02_CURRENT_SITE_TOPOLOGY_{DATE}.tsv.gz"
    write_tsv_gz(current_path, current_nodes, list(current_nodes[0]))

    target_architecture: list[dict[str, object]] = []
    for unit in unit_ledger:
        if unit["product_state"] != "ACTIVE_MK02_WORKING_CORE":
            continue
        if unit["family_owner_url"]:
            target_state = "EXISTING_FAMILY_OWNER"
        elif unit["structural_action"] == "DEFER_PENDING_EVIDENCE":
            target_state = "OWNER_UNRESOLVED_EVIDENCE_REQUIRED"
        elif unit["structural_action"] == "NO_STANDALONE_PAGE":
            target_state = "NO_STANDALONE_PAGE"
        elif unit["structural_action"] == "OUTSIDE_SCOPE_NO_ACTION":
            target_state = "OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP"
        else:
            raise AssertionError(f"target state unresolved for {unit['structural_unit_id']}")
        target_architecture.append(
            {
                "structural_unit_id": unit["structural_unit_id"],
                "active_phrase_count": unit["active_mk02_phrase_count"],
                "user_task": unit["user_task"],
                "target_state": target_state,
                "target_family_owner_url": unit["family_owner_url"],
                "supporting_pages": unit["supporting_pages"],
                "unit_page_role": unit["unit_page_role"],
                "structural_action": unit["structural_action"],
                "uncertainty_state": unit["uncertainty_state"],
                "architecture_basis": "NATIVE_2840__ACTIVE_2185__STAGE5_PRE_STEP5A_WITH_ACCEPTED_CURRENT_SITE_OVERLAY",
            }
        )
    assert len(target_architecture) == 160
    assert len({row["target_family_owner_url"] for row in target_architecture if row["target_family_owner_url"]}) == 59
    write_tsv(
        HERE / f"MK02_TARGET_SEARCH_ARCHITECTURE_{DATE}.tsv",
        target_architecture,
        list(target_architecture[0]),
    )

    page_deltas = read_tsv(SOURCE / "STEP_14A_ARCHITECTURE_DELTA.tsv")
    link_as_is = read_tsv(SOURCE / "STEP_14A_RUN9_INTERNAL_LINK_AS_IS_RECONCILIATION.tsv")
    link_specs = {
        row["link_action_id_or_group"]: row
        for row in read_tsv(SOURCE / "RESEARCH_REBUILD_STAGE_06_INTERNAL_LINK_SPECIFICATIONS_2026-09-05.tsv")
    }
    deltas: list[dict[str, object]] = []
    for row in page_deltas:
        deltas.append(
            {
                "delta_id": row["delta_id"],
                "delta_class": "CURRENT_PAGE_TO_TARGET_RECONCILIATION",
                "current_object": row["path"],
                "target_object": row["final_owner_decision"],
                "current_state": row["previous_owner_or_state"],
                "target_state": row["delta_type"],
                "action_state": "SEMANTIC_MAPPING_OR_BOUNDARY_UPDATE",
                "real_site_change": "NO",
                "destructive_action": "NO",
                "evidence_locator": f"STEP_14A_ARCHITECTURE_DELTA.tsv#{row['delta_id']}",
                "evidence_meaning": row["semantic_rationale"],
                "uncertainty": "NONE_WITHIN_PRESERVED_SNAPSHOT",
            }
        )
    page_relationships: list[dict[str, object]] = []
    link_pair_groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in link_as_is:
        link_pair_groups[(row["source_url"], row["target_url"])].append(row)
    for (source_url, target_url), group in link_pair_groups.items():
        row = group[0]
        source_ids = sorted(item["edge_id"] for item in group)
        specs = [link_specs[item["edge_id"]] for item in group]
        assert len({item["current_link_present"] for item in group}) == 1
        assert len({item["recommendation_state"] for item in group}) == 1
        present = row["current_link_present"].lower() in {"true", "yes", "1"}
        action_state = "NO_CHANGE_ALREADY_PRESENT" if present else "PENDING_PLACEMENT_OR_CONTEXT"
        deltas.append(
            {
                "delta_id": ";".join(source_ids),
                "delta_class": "INTERNAL_LINK_RELATION",
                "current_object": source_url,
                "target_object": target_url,
                "current_state": row["run9_as_is_state"],
                "target_state": row["recommendation_state"],
                "action_state": action_state,
                "real_site_change": "NO" if present else "UNRESOLVED",
                "destructive_action": "NO",
                "evidence_locator": "STEP_14A_RUN9_INTERNAL_LINK_AS_IS_RECONCILIATION.tsv#" + ";".join(source_ids),
                "evidence_meaning": row["reconciliation_decision"],
                "uncertainty": "NONE" if present else "EXACT_PLACEMENT_NOT_PROVEN",
            }
        )
        page_relationships.append(
            {
                "relationship_id": ";".join(source_ids),
                "source_url": source_url,
                "target_url": target_url,
                "recommended_relation": row["recommendation_state"],
                "literal_current_state": row["run9_as_is_state"],
                "current_link_present": "YES" if present else "NO",
                "implementation_state": action_state,
                "anchor_or_context": row["anchor_or_context"],
                "placement_instruction": " | ".join(sorted({spec["anchor_guidance"] for spec in specs})),
                "acceptance_check": " | ".join(sorted({spec["acceptance_criteria"] for spec in specs})),
                "claim_boundary": "RECOMMENDATION_STATE_SEPARATE_FROM_LITERAL_AS_IS_STATE",
            }
        )
    assert len(deltas) == 35
    assert len(page_relationships) == 14
    assert Counter(row["current_link_present"] for row in page_relationships) == Counter({"YES": 8, "NO": 6})
    assert len({(row["source_url"], row["target_url"]) for row in page_relationships}) == 14
    write_tsv(HERE / f"MK02_CURRENT_TARGET_DELTA_{DATE}.tsv", deltas, list(deltas[0]))
    write_tsv(
        HERE / f"MK02_PAGE_RELATIONSHIPS_{DATE}.tsv",
        page_relationships,
        list(page_relationships[0]),
    )

    outputs = [
        foundation_path,
        phrase_map_path,
        HERE / f"MK02_UNIT_OWNERSHIP_LEDGER_{DATE}.tsv",
        HERE / f"MK02_OWNERSHIP_CANDIDATE_LEDGER_{DATE}.tsv",
        HERE / f"MK02_STRUCTURAL_ACTIONS_{DATE}.tsv",
        HERE / f"MK02_COMPETING_PAGE_CASES_{DATE}.tsv",
        current_path,
        HERE / f"MK02_TARGET_SEARCH_ARCHITECTURE_{DATE}.tsv",
        HERE / f"MK02_CURRENT_TARGET_DELTA_{DATE}.tsv",
        HERE / f"MK02_PAGE_RELATIONSHIPS_{DATE}.tsv",
    ]
    manifest = {
        "schema": "MK02_OKNO_MSK_STEPS_00_13_PROJECTION_V1",
        "date": DATE,
        "status": "PASS",
        "provider_calls_during_rehearsal": 0,
        "inputs": {
            str(semantic_source.relative_to(REPO)): {"rows": 2840, "sha256": sha256(semantic_source)},
            str(mk01_source.relative_to(REPO)): {"rows": 2840, "sha256": sha256(mk01_source)},
            str(stage5_source.relative_to(REPO)): {"rows": 2840, "sha256": sha256(stage5_source)},
            str(unit_source.relative_to(REPO)): {"rows": 168, "sha256": sha256(unit_source)},
            str(step12_source.relative_to(REPO)): {"rows": 168, "sha256": sha256(step12_source)},
        },
        "semantic_accounting": {
            "source_unique_phrases": 2840,
            "working_core": 2185,
            "review_uncertain": 187,
            "excluded": 468,
            "total_groups": 59,
            "working_groups": 54,
            "outside_groups": 5,
            "step5a_additions": 0,
        },
        "ownership_accounting": {
            "active_phrase_mapping_rows": 2185,
            "OWNER_EXISTING": 1647,
            "NO_SUITABLE_EXISTING_PAGE": 518,
            "OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP": 14,
            "OWNER_UNRESOLVED_EVIDENCE_REQUIRED": 6,
            "family_owner_nonblank_rows": sum(bool(row["family_owner_url"]) for row in phrase_map),
            "supporting_page_nonblank_rows": sum(bool(row["supporting_pages"]) for row in phrase_map),
            "active_structural_units": 160,
            "preserved_unit_ledger_rows": 168,
            "ownership_candidate_ledger_rows": 59,
            "ownership_candidate_comparisons": 105,
        },
        "structural_action_accounting_active_units": dict(
            sorted(Counter(row["source_structural_action"] for row in structural_actions).items())
        ),
        "competing_page_accounting": {
            "historical_base_pairs": 195,
            "effective_pairs": 199,
            "query_family_cases": 21,
            "private_history_reused": 0,
            "harmful_impact_proven": 0,
            "destructive_actions_authorized": 0,
        },
        "current_site_accounting": {
            "current_public_nodes": 2683,
            "known_critical_rechecked_urls": 59,
            "current_minus_upstream_classified": 2624,
            "architecture_material": 21,
            "non_material": 1932,
            "out_of_scope": 671,
            "discovery_unclassified": 0,
            "current_internal_edges_processed": 15,
            "literal_edges_present": 9,
            "literal_edges_absent_planned": 6,
        },
        "target_architecture_accounting": {
            "active_units": 160,
            "unique_existing_family_owner_pages": 59,
            "unit_supporting_relations": sum(len(split_urls(row["supporting_pages"])) for row in target_architecture),
            "source_page_to_page_relation_rows_checked": 15,
            "distinct_visible_page_to_page_relations": 14,
            "page_deltas": 21,
            "combined_current_target_delta_rows": 35,
            "create": 0,
            "split": 0,
            "merge": 0,
            "redirect_delete": 0,
        },
        "preserved_ordinary_search_evidence_reused": {
            "step11_queries": 69,
            "step13_queries": 16,
            "total_queries": 85,
            "active_phrases_with_direct_exact_query_row_in_structured_preserved_results": sum(
                row["observed_search_evidence_scope"].startswith("EXACT_QUERY") for row in phrase_map
            ),
            "target_host_urls_observed_for_those_exact_rows": sum(
                bool(row["observed_search_relevant_url"]) for row in phrase_map
            ),
        },
        "outputs": {
            path.name: {
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in outputs
        },
        "claim_boundaries": [
            "PRESERVED_EVIDENCE_ONLY",
            "ACTIVE_INPUT_EQUALS_ACCEPTED_MK01_WORKING_CORE_2185",
            "LATE_EVIDENCE_DATE_DOES_NOT_IMPLY_STEP5A_CAUSATION",
            "OBSERVED_SEARCH_URL_NOT_INFERRED_FROM_OWNER",
            "CURRENT_TOPOLOGY_SNAPSHOT_2026_09_02_NOT_LIVE_2026_09_10",
            "PRIVATE_QUERY_URL_HISTORY_UNAVAILABLE",
            "TARGET_ARCHITECTURE_NOT_CURRENT_AS_IS_TOPOLOGY",
            "NO_NEW_PROVIDER_CALLS",
        ],
    }
    manifest_path = HERE / f"MK02_STEPS_00_13_MANIFEST_{DATE}.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
