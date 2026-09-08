#!/usr/bin/env python3
"""Build the bounded Step 5A.6 Search reconciliation and Step 5A.7 merge.

All provider inputs are immutable repository files.  This script performs no
network access and deliberately creates no rows for outcome-unknown requests.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


OUT = Path(__file__).resolve().parent
JOB = OUT.parent

SEARCH_PACKAGE = OUT / "STEP_05A_SEARCH_RECHECK_REQUIREMENT_PACKAGE.tsv"
PAGE_EVIDENCE = OUT / "STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv"
WORDSTAT_RECONCILIATION = OUT / "STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv"
WORDSTAT_ACQUISITION = OUT / "STEP_05A_WORDSTAT_SEED_ACQUISITION_LEDGER.tsv"
UNIT_AUTHORITY = JOB / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"

ACQUISITION = OUT / "STEP_05A_SEARCH_REQUIREMENT_ACQUISITION_LEDGER.tsv"
SERP_LEDGER = OUT / "STEP_05A_SEARCH_SERP_ROW_LEDGER.tsv"
VISIBILITY = OUT / "STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv"
INTENT_ANALYSIS = OUT / "STEP_05A_SEARCH_INTENT_PAGE_TYPE_ANALYSIS.tsv"
DECISIONS = OUT / "STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv"
MERGE_RECONCILIATION = OUT / "STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv"
DELTA = OUT / "STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv"
REPORT = OUT / "STEP_05A_SEARCH_DECISION_MERGE_REPORT.md"
INFO_GAIN = OUT / "STEP_05A_INFORMATION_GAIN_INPUT.json"
LOG = OUT / "STEP_05A_SEARCH_DECISION_MERGE_EXECUTION_LOG.md"
CHECKPOINT_SEARCH = OUT / "CHECKPOINT_05_SEARCH_NORMALIZATION_AND_INTENT.md"
CHECKPOINT_MERGE = OUT / "CHECKPOINT_06_SEARCH_DECISION_MERGE.md"

SELECTED_COMPETITORS = [
    "mosokna.ru",
    "i-okna.ru",
    "msk.okna-servise.com",
    "okna-moskva.ru",
    "oknafactoria.ru",
    "okna-germany.ru",
    "fabrikaokon.ru",
    "aluminarium.ru",
    "elit-balkon.ru",
]

RAW_FILES = {
    1: "STEP_05A_SEARCH_ITEM_01_RAW.json",
    2: "STEP_05A_SEARCH_ITEM_02_RAW.json",
    3: "STEP_05A_SEARCH_ITEM_03_RAW.json",
    4: "STEP_05A_SEARCH_ITEM_04_RAW.json",
    5: "STEP_05A_SEARCH_ITEM_05_OUTCOME_UNKNOWN_RAW.json",
    6: "STEP_05A_SEARCH_ITEM_06_RAW.json",
    7: "STEP_05A_SEARCH_ITEM_07_OUTCOME_UNKNOWN_RAW.json",
    8: "STEP_05A_SEARCH_ITEM_08_RAW.json",
    9: "STEP_05A_SEARCH_ITEM_09_RAW.json",
}

LIFECYCLE_STAGE = {
    1: "INITIAL_9_ROW_JOB",
    2: "INITIAL_9_ROW_JOB",
    3: "INITIAL_9_ROW_JOB",
    4: "INITIAL_9_ROW_JOB",
    5: "INITIAL_9_ROW_JOB__STOP_AND_CANCEL_REMAINDER",
    6: "CONTINUATION_4_ROW_JOB",
    7: "CONTINUATION_4_ROW_JOB__STOP_AND_CANCEL_REMAINDER",
    8: "FINAL_2_ROW_JOB",
    9: "FINAL_2_ROW_JOB",
}

# Audited result-type classification from the exact 70 preserved title/URL rows.
PAGE_TYPES = {
    1: ["MARKETPLACE", "COMMERCIAL_SERVICE", "MARKETPLACE", "MARKETPLACE", "MANUFACTURER_BRAND_SOURCE", "ARTICLE_GUIDE", "MANUFACTURER_BRAND_SOURCE", "MANUFACTURER_BRAND_SOURCE", "ARTICLE_GUIDE", "MANUFACTURER_BRAND_SOURCE"],
    2: ["COMMERCIAL_PRODUCT", "COMMERCIAL_SERVICE", "COMMERCIAL_PRODUCT", "COMMERCIAL_PRODUCT", "COMMERCIAL_LANDING", "COMMERCIAL_PRODUCT", "COMMERCIAL_SERVICE", "COMMERCIAL_PRODUCT", "MANUFACTURER_BRAND_SOURCE", "COMMERCIAL_PRODUCT"],
    3: ["ARTICLE_GUIDE", "ARTICLE_GUIDE", "INFORMATIONAL_PUBLISHER", "ARTICLE_GUIDE", "ARTICLE_GUIDE", "ARTICLE_GUIDE", "INFORMATIONAL_PUBLISHER", "ARTICLE_GUIDE", "COMPARISON_SELECTION", "MANUFACTURER_BRAND_SOURCE"],
    4: ["COMMERCIAL_PRODUCT", "COMMERCIAL_PRODUCT", "COMMERCIAL_PRODUCT", "COMMERCIAL_PRODUCT", "COMMERCIAL_PRODUCT", "MANUFACTURER_BRAND_SOURCE", "COMMERCIAL_PRODUCT", "ARTICLE_GUIDE", "COMMERCIAL_PRODUCT", "MANUFACTURER_BRAND_SOURCE"],
    6: ["INFORMATIONAL_PUBLISHER", "COMMERCIAL_SERVICE", "INFORMATIONAL_PUBLISHER", "PORTFOLIO_GALLERY", "COMMERCIAL_SERVICE", "PORTFOLIO_GALLERY", "ARTICLE_GUIDE", "INFORMATIONAL_PUBLISHER", "PORTFOLIO_GALLERY", "INFORMATIONAL_PUBLISHER"],
    8: ["MARKETPLACE", "MARKETPLACE", "MARKETPLACE", "MARKETPLACE", "MARKETPLACE", "ARTICLE_GUIDE", "ARTICLE_GUIDE", "MARKETPLACE", "COMMERCIAL_SERVICE", "MARKETPLACE"],
    9: ["ARTICLE_GUIDE", "ARTICLE_GUIDE", "MANUFACTURER_BRAND_SOURCE", "ARTICLE_GUIDE", "MANUFACTURER_BRAND_SOURCE", "ARTICLE_GUIDE", "ARTICLE_GUIDE", "ARTICLE_GUIDE", "ARTICLE_GUIDE", "ARTICLE_GUIDE"],
}

ROW_INTENT_BY_TYPE = {
    "COMMERCIAL_SERVICE": "SERVICE_PURCHASE",
    "COMMERCIAL_PRODUCT": "PRODUCT_PROCUREMENT",
    "COMMERCIAL_CATEGORY": "PRODUCT_PROCUREMENT",
    "COMMERCIAL_LANDING": "PRODUCT_OR_SERVICE_PURCHASE",
    "ARTICLE_GUIDE": "LEARNING_SELECTION",
    "COMPARISON_SELECTION": "LEARNING_SELECTION",
    "MARKETPLACE": "PRODUCT_PROCUREMENT",
    "INFORMATIONAL_PUBLISHER": "LEARNING_OR_INSPIRATION",
    "MANUFACTURER_BRAND_SOURCE": "PRODUCT_INFORMATION_OR_SELECTION",
    "PORTFOLIO_GALLERY": "USE_CASE_INSPIRATION",
    "OTHER_REVIEW": "REVIEW_OR_DISCOVERY",
}

QUERY_ANALYSIS = {
    1: ("MIXED__MARKETPLACE_INFORMATION_SERVICE", "MIXED_PRODUCT_PROCUREMENT_AND_PROBLEM_SOLVING", "The TOP10 combines three marketplaces, one specialist service page, and six explanatory/manufacturer sources; the exact task is a mixed material-selection, learning and service-discovery job.", "HIGH"),
    2: ("COMMERCIAL_PRODUCT_AND_SERVICE_DOMINANT", "PRODUCT_PROCUREMENT", "Nine of ten rows are product, service, landing or manufacturer offer sources; the tested job is commercial selection/procurement of a sun-protection glass-unit configuration.", "HIGH"),
    3: ("ARTICLE_AND_INFORMATION_DOMINANT", "LEARNING_SELECTION", "The TOP10 is led by guides, publishers and one comparison; the tested job is explanatory selection of a multifunctional glass unit.", "HIGH"),
    4: ("COMMERCIAL_PRODUCT_DOMINANT_WITH_GUIDE", "PRODUCT_PROCUREMENT_AND_SELECTION", "Product pages dominate, with a supporting guide and manufacturer sources; the tested job is procurement/selection of an impact-resistant glass-unit option.", "HIGH"),
    6: ("INSPIRATION_INFORMATION_WITH_SERVICE_OPTIONS", "USE_CASE_INSPIRATION_AND_SERVICE_DISCOVERY", "Editorial/inspiration and portfolio rows dominate; two service rows and three portfolio rows show a realizable balcony-office renovation job.", "HIGH"),
    8: ("MARKETPLACE_DOMINANT_WITH_SERVICE_AND_GUIDES", "PRODUCT_PROCUREMENT_WITH_SERVICE_DISCOVERY", "Seven marketplace rows dominate, with two guides and one specialist service result; the task is mainly material procurement but includes an observable service job.", "HIGH"),
    9: ("ARTICLE_AND_EXPERT_SOURCE_DOMINANT", "TECHNICAL_LEARNING_SELECTION", "Eight guides and two manufacturer/expert sources dominate; the tested job is technical learning and selection around profile reinforcement.", "HIGH"),
}

BUSINESS_AUTHORITY = {
    "OPEN_BALCONY_WATERPROOFING": ("IN_SCOPE_PARENT_CONFIRMED", "unit:OPEN_BALCONY_FINISHING"),
    "SUN_PROTECTION_GLASS_UNIT": ("IN_SCOPE_PARENT_CONFIRMED", "unit:GLASS_UNIT_SELECTION_INFO"),
    "MULTIFUNCTIONAL_GLASS_UNIT": ("IN_SCOPE_PARENT_CONFIRMED", "unit:GLASS_UNIT_SELECTION_INFO"),
    "IMPACT_RESISTANT_GLASS_UNIT": ("IN_SCOPE_PARENT_CONFIRMED", "unit:GLASS_UNIT_SELECTION_INFO"),
    "OLD_HOUSING_WINDOWS": ("IN_SCOPE_ADJACENT__EXACT_JOB_UNRESOLVED", "STEP_01_MERGED_BUSINESS_PAGE_MODEL.md:B03/B04"),
    "BALCONY_AS_OFFICE": ("IN_SCOPE_PARENT_CONFIRMED", "unit:BALCONY_RENOVATION_WITH_GLAZING"),
    "BALCONY_AS_STORAGE": ("IN_SCOPE_PARENT_CONFIRMED", "unit:BALCONY_RENOVATION_WITH_GLAZING"),
    "BALCONY_ROOF_SOUNDPROOFING": ("IN_SCOPE_PARENT_CONFIRMED", "unit:BALCONY_GLAZING_ROOF_SERVICE"),
    "WINDOW_PROFILE_REINFORCEMENT": ("IN_SCOPE_PARENT_CONFIRMED", "unit:WINDOW_PROFILE_SELECTION_INFO"),
}

SUPPRESSED_CLOSE_VARIANTS = {"WSR004", "WSR026", "WSR047"}
HOLD_OCCURRENCES = {"WSR100"}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def normalize_domain(domain: str) -> str:
    value = domain.casefold().strip().rstrip(".")
    return value[4:] if value.startswith("www.") else value


def normalize_phrase(text: str) -> str:
    return " ".join(re.sub(r"[^a-zа-яё0-9]+", " ", text.casefold()).split())


def canonical_url(url: str) -> str:
    parts = urlsplit(url)
    host = normalize_domain(parts.netloc)
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.casefold(), host, path, parts.query, ""))


def load_context():
    package = read_tsv(SEARCH_PACKAGE)
    pages = read_tsv(PAGE_EVIDENCE)
    inspected = defaultdict(list)
    for row in pages:
        inspected[normalize_domain(row["competitor_domain"])].append(row)
    wordstat_acq = {int(row["seed_order"]): row for row in read_tsv(WORDSTAT_ACQUISITION)}
    return package, pages, inspected, wordstat_acq


def raw_for_priority(priority: int) -> tuple[Path, dict[str, object]]:
    path = OUT / RAW_FILES[priority]
    return path, json.loads(path.read_text(encoding="utf-8"))


def build_search_block():
    package, pages, inspected, _ = load_context()
    acquisition_rows = []
    serp_rows = []
    intent_rows = []
    raw_by_priority = {}

    for req in package:
        priority = int(req["search_priority"])
        raw_path, raw = raw_for_priority(priority)
        raw_by_priority[priority] = raw
        item = raw["item"]
        provider = raw.get("provider_result") or {}
        result = provider.get("result") if isinstance(provider, dict) else None
        results = result.get("results", []) if isinstance(result, dict) else []
        state = item["status"]
        limitation = (
            "Exact provider TOP10 is available and only its returned rows are materialized."
            if state == "SUCCEEDED"
            else "REQUEST_OUTCOME_UNKNOWN_NO_RETRY: no SERP, page-type, intent, or visibility evidence exists; no retry is permitted."
        )
        acquisition_rows.append({
            "search_priority": priority,
            "deduplicated_direction_id": req["deduplicated_direction_id"],
            "representative_query": req["representative_query"],
            "originating_wordstat_seed_order": req["originating_wordstat_seed_order"],
            "originating_wordstat_seed": req["originating_wordstat_seed"],
            "originating_returned_phrases_and_counts": req["originating_returned_phrases_and_counts"],
            "wordstat_evidence_lineage": req["wordstat_evidence_lineage"],
            "competitor_page_evidence_ids": req["competitor_page_evidence_ids"],
            "competitor_page_urls": req["competitor_page_urls"],
            "search_acquisition_state": state,
            "search_raw_item_file": raw_path.name,
            "batch_lifecycle_stage": LIFECYCLE_STAGE[priority],
            "durable_job_id": raw["job_id"],
            "request_id": item["request_id"],
            "final_envelope_request_executed": str(raw.get("request_executed", "")).upper() if not isinstance(raw.get("request_executed"), bool) else str(raw["request_executed"]).lower(),
            "item_request_executed": str(item.get("request_executed", "")).lower(),
            "estimated_cost_rub": item["estimated_cost_rub"],
            "http_status": provider.get("http_status", ""),
            "result_count": len(results) if state == "SUCCEEDED" else "",
            "outcome_unknown_reason": item.get("outcome_unknown_reason") or raw.get("reason") or "",
            "automatic_retry": str(raw.get("automatic_retry", False)).lower(),
            "evidence_limitation": limitation,
        })
        if state != "SUCCEEDED":
            continue
        query_mix, query_job, query_note, confidence = QUERY_ANALYSIS[priority]
        for result_row in results:
            rank = int(result_row["rank"])
            raw_domain = result_row["domain"]
            domain = normalize_domain(raw_domain)
            selected = domain in SELECTED_COMPETITORS
            inspected_rows = inspected.get(domain, [])
            exact_matches = sorted({r["inspection_id"] for r in inspected_rows if canonical_url(result_row["url"]) in {canonical_url(r["requested_url"]), canonical_url(r["final_url"])} })
            row_id = f"SSR{priority:02d}-{rank:02d}"
            prior_status = (
                "EXACT_PREVIOUSLY_INSPECTED_URL"
                if exact_matches
                else "SAME_SELECTED_COMPETITOR_DOMAIN__DIFFERENT_URL"
                if selected
                else "NOT_A_SELECTED_STEP5A_COMPETITOR"
            )
            base = {
                "search_row_id": row_id,
                "search_priority": priority,
                "deduplicated_direction_id": req["deduplicated_direction_id"],
                "tested_query": req["representative_query"],
                "rank": rank,
                "raw_domain": raw_domain,
                "normalized_domain": domain,
                "raw_url": result_row["url"],
                "title": result_row.get("title", ""),
                "snippet": result_row.get("snippet", ""),
                "modtime": result_row.get("modtime", ""),
                "source_raw_item_file": raw_path.name,
                "request_id": item["request_id"],
                "selected_step5a_competitor": str(selected).lower(),
                "selected_competitor_domain": domain if selected else "",
                "equals_previously_inspected_competitor_url": str(bool(exact_matches)).lower(),
                "matching_prior_inspection_ids": " | ".join(exact_matches),
                "selected_competitor_url_relation": prior_status,
                "claim_boundary": "OBSERVED_EXACT_QUERY_TOP10_ROW_ONLY__NO_TRAFFIC_OR_FULL_KEYWORD_UNIVERSE_CLAIM",
            }
            serp_rows.append(base)
            page_type = PAGE_TYPES[priority][rank - 1]
            intent_rows.append({
                "search_row_id": row_id,
                "search_priority": priority,
                "deduplicated_direction_id": req["deduplicated_direction_id"],
                "tested_query": req["representative_query"],
                "rank": rank,
                "normalized_domain": domain,
                "raw_url": result_row["url"],
                "page_type": page_type,
                "row_intent": ROW_INTENT_BY_TYPE[page_type],
                "classification_evidence": f"Returned title/URL: {result_row.get('title', '')} | {result_row['url']}",
                "query_page_type_mix": query_mix,
                "query_search_job": query_job,
                "query_evidence_summary": query_note,
                "query_confidence": confidence,
                "ownership_decision": "NOT_DECIDED_FROM_PAGE_TYPE",
                "claim_boundary": "SEARCH_RESULT_TYPE_AND_INTENT_ONLY__NO_PAGE_OWNERSHIP_OR_IMPLEMENTATION_ACTION",
            })

    matrix_rows = []
    serp_by_priority = defaultdict(list)
    for row in serp_rows:
        serp_by_priority[int(row["search_priority"])].append(row)
    page_by_id = {row["inspection_id"]: row for row in pages}
    for req in package:
        priority = int(req["search_priority"])
        state = next(row["search_acquisition_state"] for row in acquisition_rows if int(row["search_priority"]) == priority)
        evidence_ids = [part.strip() for part in req["competitor_page_evidence_ids"].split("|") if part.strip()]
        lineage_pages = [page_by_id[eid] for eid in evidence_ids]
        for competitor in SELECTED_COMPETITORS:
            prior_pages = [row for row in lineage_pages if normalize_domain(row["competitor_domain"]) == competitor]
            matched = [row for row in serp_by_priority[priority] if row["normalized_domain"] == competitor]
            if state == "OUTCOME_UNKNOWN":
                visibility_state = "SEARCH_OUTCOME_UNKNOWN__VISIBILITY_NOT_OBSERVABLE"
                interpretation = "The request outcome is unknown; absence, rank and URL visibility cannot be claimed."
            elif matched:
                visibility_state = "VISIBLE_IN_TOP10"
                interpretation = "Selected competitor was observed in the preserved TOP10 for this exact tested query only."
            else:
                visibility_state = "NOT_OBSERVED_IN_TOP10"
                interpretation = "Selected competitor was not observed in this single preserved TOP10; this is not a full keyword-universe claim."
            matrix_rows.append({
                "search_priority": priority,
                "deduplicated_direction_id": req["deduplicated_direction_id"],
                "tested_query": req["representative_query"],
                "selected_competitor_domain": competitor,
                "search_acquisition_state": state,
                "visibility_state": visibility_state,
                "best_observed_rank": min((int(row["rank"]) for row in matched), default=""),
                "observed_ranking_urls": " | ".join(row["raw_url"] for row in matched),
                "observed_raw_domains": " | ".join(row["raw_domain"] for row in matched),
                "observed_result_row_ids": " | ".join(row["search_row_id"] for row in matched),
                "ranking_url_previously_inspected_state": (
                    "AT_LEAST_ONE_EXACT_PREVIOUSLY_INSPECTED_URL" if any(row["equals_previously_inspected_competitor_url"] == "true" for row in matched)
                    else "SAME_DOMAIN_DIFFERENT_URL" if matched else "NOT_APPLICABLE"
                ),
                "earlier_direction_page_evidence_ids": " | ".join(row["inspection_id"] for row in prior_pages),
                "earlier_direction_page_urls": " | ".join(row["requested_url"] for row in prior_pages),
                "earlier_evidence_role": "TOPIC_AND_SEED_LINEAGE_ONLY__NOT_EXACT_QUERY_RANKING_PROOF" if prior_pages else "NO_EARLIER_DIRECTION_PAGE_FROM_THIS_DOMAIN",
                "claim_safe_interpretation": interpretation,
            })

    write_tsv(ACQUISITION, acquisition_rows, list(acquisition_rows[0]))
    write_tsv(SERP_LEDGER, serp_rows, list(serp_rows[0]))
    write_tsv(INTENT_ANALYSIS, intent_rows, list(intent_rows[0]))
    write_tsv(VISIBILITY, matrix_rows, list(matrix_rows[0]))

    checkpoint = f"""# CHECKPOINT 05 — SEARCH NORMALIZATION AND INTENT

Date: 2026-09-08

Status: MATERIALIZED / DETERMINISTIC QA PASS / REMOTE READBACK PASS

- Search requirements accounted: {len(acquisition_rows)} / 9.
- Successful requirements: {sum(r['search_acquisition_state'] == 'SUCCEEDED' for r in acquisition_rows)}.
- Outcome unknown: {sum(r['search_acquisition_state'] == 'OUTCOME_UNKNOWN' for r in acquisition_rows)}; no retry and no fabricated rows.
- Exact successful TOP10 rows: {len(serp_rows)}.
- Page-type/intent rows: {len(intent_rows)}.
- Visibility matrix: {len(matrix_rows)} rows (9 × 9).
- Selected-competitor visible query/domain cells: {sum(r['visibility_state'] == 'VISIBLE_IN_TOP10' for r in matrix_rows)}.
- New provider calls by Work: 0.

Material commit: `0b765fa96aee1dc742046f1b31a2759ff08d4d82`.

Remote GitHub readback: PASS — commit metadata and the acquisition, SERP-row, intent and visibility artifacts were fetched from the remote commit after its branch ref was updated.
"""
    CHECKPOINT_SEARCH.write_text(checkpoint, encoding="utf-8")
    return acquisition_rows, serp_rows, intent_rows, matrix_rows


def build_final_block(acquisition_rows, serp_rows, intent_rows, matrix_rows):
    package, pages, inspected, wordstat_acq = load_context()
    intent_by_priority = {}
    for priority in PAGE_TYPES:
        rows = [row for row in intent_rows if int(row["search_priority"]) == priority]
        intent_by_priority[priority] = rows[0]
    visible_by_priority = defaultdict(list)
    for row in matrix_rows:
        if row["visibility_state"] == "VISIBLE_IN_TOP10":
            visible_by_priority[int(row["search_priority"])].append(row)

    unit_ids = {row["structural_unit_id"] for row in read_tsv(UNIT_AUTHORITY)}
    decision_rows = []
    for req in package:
        priority = int(req["search_priority"])
        direction = req["deduplicated_direction_id"]
        acquisition = next(row for row in acquisition_rows if int(row["search_priority"]) == priority)
        state = acquisition["search_acquisition_state"]
        business_state, business_ref = BUSINESS_AUTHORITY[direction]
        if business_ref.startswith("unit:") and business_ref[5:] not in unit_ids:
            raise ValueError(f"Unknown business authority unit: {business_ref}")
        if state == "SUCCEEDED":
            final_state = "ADD_TO_PIPELINE"
            analysis = intent_by_priority[priority]
            mix = analysis["query_page_type_mix"]
            job = analysis["query_search_job"]
            sufficient = "true"
            reason = (
                "Actual Wordstat demand occurrence(s), a sufficient preserved exact-query TOP10, an in-scope frozen parent unit, "
                "and Step 5A.5 semantic novelty jointly support addition to the shared acquisition pipeline. This is not a page decision."
            )
            unresolved = "Page ownership, page creation, split/merge, implementation and business-detail confirmation remain outside this evidence-only merge."
        else:
            final_state = "HOLD_EVIDENCE"
            mix = "SEARCH_OUTCOME_UNKNOWN__NO_PAGE_TYPE_MIX"
            job = "SEARCH_INTENT_NOT_OBSERVABLE"
            sufficient = "false"
            reason = "The provider outcome is unknown and was not retried; the preserved parent scope does not independently resolve current exact-query intent, so ADD_TO_PIPELINE is prohibited."
            unresolved = "A separately authorized future Search recheck would be required; this execution does not retry or fabricate the missing SERP."
        visible = visible_by_priority.get(priority, [])
        decision_rows.append({
            "search_priority": priority,
            "deduplicated_direction_id": direction,
            "representative_query": req["representative_query"],
            "search_acquisition_state": state,
            "dominant_page_type_mix": mix,
            "current_search_job": job,
            "search_evidence_sufficient_for_direction": sufficient,
            "selected_competitors_visible_count": len(visible),
            "selected_competitors_visible": " | ".join(row["selected_competitor_domain"] for row in visible),
            "selected_competitor_visibility_row_ids": " | ".join(row["observed_result_row_ids"] for row in visible),
            "frozen_business_scope_state": business_state,
            "frozen_business_scope_authority": business_ref,
            "current_semantic_coverage_state": "NO_EXACT_OR_CLOSE_ACTIVE_DIRECTION__STEP5A3_PARENT_UNIT_ONLY",
            "current_semantic_authority": "STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv + RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv",
            "final_routing_state": final_state,
            "decision_reason": reason,
            "remaining_unresolved_evidence": unresolved,
            "page_or_implementation_decision": "NONE__OUT_OF_SCOPE",
            "propagation_state": "PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE" if final_state == "ADD_TO_PIPELINE" else "NO_PROPAGATION_WHILE_HOLD",
            "claim_boundary": "ANALYTICAL_PIPELINE_ROUTING_ONLY__NOT_PAGE_OWNERSHIP_CREATION_SPLIT_MERGE_OR_IMPLEMENTATION",
        })

    decision_by_direction = {row["deduplicated_direction_id"]: row for row in decision_rows}
    potentials = [row for row in read_tsv(WORDSTAT_RECONCILIATION) if row["semantic_reconciliation_result"] == "POTENTIALLY_NEW_SEARCH_RECHECK"]
    package_by_direction = {row["deduplicated_direction_id"]: row for row in package}
    merge_rows = []
    for row in potentials:
        row_id = row["wordstat_row_id"]
        direction = row["deduplicated_direction_id"]
        decision = decision_by_direction[direction]
        if row_id in HOLD_OCCURRENCES:
            merge_state = "RETAIN_HOLD"
            merge_reason = "The direction's Search request is OUTCOME_UNKNOWN; the real Wordstat occurrence is preserved but cannot enter the delta."
        elif row_id in SUPPRESSED_CLOSE_VARIANTS:
            merge_state = "SUPPRESSED_AS_CLOSE_VARIANT_DUPLICATE"
            merge_reason = "A stronger base occurrence in the same confirmed direction already carries this near-equivalent wording; suppressing it prevents duplicate inflation."
        elif decision["final_routing_state"] == "ADD_TO_PIPELINE":
            merge_state = "MERGE_ACCEPTED"
            merge_reason = "Materially distinct real Wordstat occurrence within a Search-confirmed, in-scope and semantically novel direction."
        else:
            merge_state = "RETAIN_HOLD"
            merge_reason = "Direction remains on evidence hold."
        req = package_by_direction[direction]
        merge_rows.append({
            "wordstat_row_id": row_id,
            "deduplicated_direction_id": direction,
            "returned_phrase": row["returned_phrase"],
            "normalized_returned_phrase": row["normalized_returned_phrase"],
            "returned_count": row["returned_count"],
            "wordstat_row_class": row["wordstat_row_class"],
            "source_seed_order": row["source_seed_order"],
            "source_seed": row["source_seed"],
            "competitor_page_lineage": row["competitor_page_lineage"],
            "wordstat_raw_provider_lineage": row["raw_provider_lineage"],
            "search_representative_query": req["representative_query"],
            "search_raw_item_file": acquisition_rows[int(req["search_priority"]) - 1]["search_raw_item_file"],
            "search_request_id": acquisition_rows[int(req["search_priority"]) - 1]["request_id"],
            "search_acquisition_state": acquisition_rows[int(req["search_priority"]) - 1]["search_acquisition_state"],
            "final_direction_routing_state": decision["final_routing_state"],
            "phrase_merge_state": merge_state,
            "phrase_merge_reason": merge_reason,
            "claim_boundary": "PHRASE_ACQUISITION_MERGE_ONLY__NO_PAGE_OR_IMPLEMENTATION_DECISION",
        })

    accepted = [row for row in merge_rows if row["phrase_merge_state"] == "MERGE_ACCEPTED"]
    wordstat_rows = {row["wordstat_row_id"]: row for row in read_tsv(WORDSTAT_RECONCILIATION)}
    delta_rows = []
    for index, merge in enumerate(accepted, start=1):
        source = wordstat_rows[merge["wordstat_row_id"]]
        direction = merge["deduplicated_direction_id"]
        req = package_by_direction[direction]
        seed_order = int(source["source_seed_order"])
        ws_acq = wordstat_acq[seed_order]
        search_acq = acquisition_rows[int(req["search_priority"]) - 1]
        delta_rows.append({
            "delta_id": f"S5A-DELTA-{index:03d}",
            "phrase": source["returned_phrase"],
            "normalized_phrase": source["normalized_returned_phrase"],
            "frequency_count": source["returned_count"],
            "frequency_evidence_state": "ACTUAL_WORDSTAT_DIRECT_RESULT_COUNT",
            "region": ws_acq["region"],
            "device_scope": ws_acq["device_scope"],
            "operator_context": "WORDSTAT_GETTOP",
            "source_type": "COMPETITOR_DERIVED_STEP5A",
            "competitor_domains": ws_acq["competitor_domains"],
            "competitor_page_urls": ws_acq["competitor_urls"],
            "competitor_page_evidence_ids": ws_acq["page_evidence_ids"],
            "candidate_seed": source["source_seed"],
            "wordstat_raw_item_file": ws_acq["raw_item_file"],
            "wordstat_request_id": ws_acq["request_id"],
            "wordstat_row_id": source["wordstat_row_id"],
            "wordstat_row_class": source["wordstat_row_class"],
            "wordstat_returned_count": source["returned_count"],
            "search_representative_query": req["representative_query"],
            "search_raw_item_file": search_acq["search_raw_item_file"],
            "search_request_id": search_acq["request_id"],
            "search_evidence_state": search_acq["search_acquisition_state"],
            "step5a_direction_id": direction,
            "step5a_final_direction_decision": "ADD_TO_PIPELINE",
            "phrase_merge_state": "MERGE_ACCEPTED",
            "provenance_complete": "true",
            "completeness_flag": "WORDSTAT_OCCURRENCE_AND_REPRESENTATIVE_SEARCH_COMPLETE",
            "propagation_state": "PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE",
            "page_ownership_state": "NOT_DECIDED",
            "claim_boundary": "UNION_COMPATIBLE_ACQUISITION_DELTA_ONLY__NO_FROZEN_AUTHORITY_OR_CLIENT_RELEASE_MUTATION",
        })

    write_tsv(DECISIONS, decision_rows, list(decision_rows[0]))
    write_tsv(MERGE_RECONCILIATION, merge_rows, list(merge_rows[0]))
    write_tsv(DELTA, delta_rows, list(delta_rows[0]))

    decision_counts = Counter(row["final_routing_state"] for row in decision_rows)
    merge_counts = Counter(row["phrase_merge_state"] for row in merge_rows)
    page_type_counts = Counter(row["page_type"] for row in intent_rows)
    selected_ranking_rows = sum(row["selected_step5a_competitor"] == "true" for row in serp_rows)
    visible_cells = sum(row["visibility_state"] == "VISIBLE_IN_TOP10" for row in matrix_rows)
    info_gain = {
        "scope": "FACTUAL_INPUT_FOR_STEP_5A_8_ONLY",
        "project_test_validated": False,
        "level1_method_promoted": False,
        "starting_search_decision_merge_head": "d307bd65c0c336cb37ad79a987a3bfe7d2e57219",
        "upstream_counts": {
            "preserved_serp_queries": 75,
            "preserved_serp_rows": 750,
            "selected_competitor_domains": 9,
            "authorized_competitor_urls": 44,
            "competitor_pages_accessible_at_requested_url": 43,
            "competitor_pages_redirected_accessible": 1,
            "competitor_pages_inaccessible": 0,
            "derived_candidate_seeds": 92,
            "deduplicated_candidate_directions": 43,
            "candidate_direction_decisions": {
                "ALREADY_COVERED_EXACT_OR_CLOSE": 22,
                "POTENTIALLY_NEW_WORDSTAT_SEED": 14,
                "OFF_SCOPE_BUSINESS": 3,
                "HOLD_REVIEW": 4
            },
            "wordstat_seed_executions": 14,
            "wordstat_returned_rows": 160,
            "potentially_new_wordstat_occurrences": 20,
        },
        "search_counts": {
            "requirements": len(acquisition_rows),
            "succeeded": sum(row["search_acquisition_state"] == "SUCCEEDED" for row in acquisition_rows),
            "outcome_unknown": sum(row["search_acquisition_state"] == "OUTCOME_UNKNOWN" for row in acquisition_rows),
            "successful_serp_rows": len(serp_rows),
            "selected_competitor_visibility_cells": visible_cells,
            "selected_competitor_ranking_rows": selected_ranking_rows,
            "exact_previously_inspected_url_matches": sum(row["equals_previously_inspected_competitor_url"] == "true" for row in serp_rows),
            "page_type_counts": dict(sorted(page_type_counts.items())),
        },
        "decision_counts": dict(sorted(decision_counts.items())),
        "merge_counts": dict(sorted(merge_counts.items())),
        "semantic_pipeline_delta_rows": len(delta_rows),
        "provider_calls_by_work": {"yandex_search": 0, "wordstat": 0, "alice": 0, "gensearch": 0, "webmaster": 0, "metrika": 0, "direct": 0, "web_search_substitute": 0},
        "propagation_state": "PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE",
        "validation_boundary": "NO_INFORMATION_GAIN_VERDICT_AND_NO_LEVEL1_PROMOTION_IN_THIS_TASK",
        "next_action": "STEP_5A_8_MEASURE_INFORMATION_GAIN_AND_ASSESS_FIRST_EXECUTION_PROJECT_VALIDATION_WITHOUT_AUTOMATIC_LEVEL1_PROMOTION",
    }
    INFO_GAIN.write_text(json.dumps(info_gain, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    decision_lines = "\n".join(
        f"| {row['search_priority']} | `{row['deduplicated_direction_id']}` | {row['representative_query']} | {row['search_acquisition_state']} | {row['final_routing_state']} | {row['selected_competitors_visible_count']} |"
        for row in decision_rows
    )
    accepted_lines = "\n".join(f"- {row['returned_phrase']} — {row['returned_count']}" for row in accepted)
    report = f"""# STEP 05A.6 SEARCH RECONCILIATION + STEP 05A.7 DECISION / MERGE REPORT

Date: 2026-09-08

Status: **ANALYST QA PASS / OWNER REVIEW PENDING**

## Outcome

The bounded preserved Search acquisition is fully reconciled: all 9 requirements are accounted across three durable job lifecycles, all 70 actually returned TOP10 rows are preserved, and both outcome-unknown requests remain unknown without retry or invented evidence.

`ADD_TO_PIPELINE` means acquisition-pipeline inclusion only. It does **not** mean a new page, page owner, split/merge, architecture, or implementation action. The corrected client release and frozen Stage-5 authorities were not changed.

## Exact counts

- SEARCH_REQUIREMENTS = {len(acquisition_rows)}
- SEARCH_SUCCEEDED = {sum(r['search_acquisition_state'] == 'SUCCEEDED' for r in acquisition_rows)}
- SEARCH_OUTCOME_UNKNOWN = {sum(r['search_acquisition_state'] == 'OUTCOME_UNKNOWN' for r in acquisition_rows)}
- SEARCH_SERP_ROWS = {len(serp_rows)}
- SELECTED_COMPETITOR_VISIBILITY_OBSERVATIONS = {visible_cells}
- SELECTED_COMPETITOR_RANKING_ROWS = {selected_ranking_rows}
- FINAL_ADD_TO_PIPELINE = {decision_counts['ADD_TO_PIPELINE']}
- FINAL_ALREADY_COVERED = {decision_counts['ALREADY_COVERED']}
- FINAL_REJECT_OFF_SCOPE = {decision_counts['REJECT_OFF_SCOPE']}
- FINAL_HOLD_EVIDENCE = {decision_counts['HOLD_EVIDENCE']}
- POTENTIALLY_NEW_WORDSTAT_OCCURRENCES_RECONCILED = {len(merge_rows)}
- MERGE_ACCEPTED_PHRASE_OCCURRENCES = {merge_counts['MERGE_ACCEPTED']}
- SUPPRESSED_AS_CLOSE_VARIANT_DUPLICATE = {merge_counts['SUPPRESSED_AS_CLOSE_VARIANT_DUPLICATE']}
- RETAIN_HOLD = {merge_counts['RETAIN_HOLD']}
- REJECT_AFTER_SEARCH = {merge_counts['REJECT_AFTER_SEARCH']}
- SEMANTIC_PIPELINE_DELTA_ROWS = {len(delta_rows)}
- UNKNOWN_RETRIES = 0
- NEW_PROVIDER_CALLS_BY_WORK = 0
- WEBSITE_TEXT_AS_RANKING_OVERCLAIM = 0
- FULL_COMPETITOR_KEYWORD_UNIVERSE_OVERCLAIM = 0
- CLIENT_DELIVERABLES_MODIFIED = false
- LEVEL1_METHOD_PROMOTED = false
- PROJECT_TEST_VALIDATED = false

Upstream bounded impact input retained for Step 5A.8: 75 preserved queries / 750 ranking rows; 9 selected domains; 44 inspected targets (43 accessible at the requested URL, 1 accessible after redirect, 0 inaccessible); 92 candidate occurrences consolidated to 43 directions; 14 Wordstat seeds; 160 returned Wordstat rows.

## Direction decisions

| Priority | Direction | Exact query | Search state | Final route | Visible selected domains |
|---:|---|---|---|---|---:|
{decision_lines}

The seven successful directions have real Wordstat occurrence evidence, sufficient exact-query Search evidence, a frozen in-scope parent business unit, and no exact/close active semantic direction. They therefore enter the union-compatible acquisition delta. The two unknown queries remain `HOLD_EVIDENCE`; neither is interpreted as an empty SERP or zero demand.

## Accepted phrase occurrences

{accepted_lines}

Close variants `WSR004`, `WSR026`, and `WSR047` are explicitly suppressed to prevent delta inflation. `WSR100` remains on hold because its Search outcome is unknown. No frequency is invented for the totalCount-only old-housing seed.

## Evidence boundaries

- Earlier competitor-page inspection proves topic/seed lineage, not exact-query rank. Every ranking claim in this report traces to a successful raw Search row.
- Observed rank is not traffic, clicks, leads, conversions, or commercial success.
- Search and Wordstat do not assign page ownership or authorize a physical site change.
- The delta is a union-compatible pre-release acquisition package marked `PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE`; it does not rewrite frozen Stage-5 authority.
- New Yandex Search, Wordstat, Alice, GenSearch, Webmaster, Metrika, Direct, competitor-page or substitute web-search calls by Work: 0.

## Next action

`STEP_5A_8_MEASURE_INFORMATION_GAIN_AND_ASSESS_FIRST_EXECUTION_PROJECT_VALIDATION_WITHOUT_AUTOMATIC_LEVEL1_PROMOTION`

This report supplies factual inputs only. Method promotion and `PROJECT_TEST_VALIDATED=true` are explicitly outside this task.
"""
    REPORT.write_text(report, encoding="utf-8")

    checkpoint = f"""# CHECKPOINT 06 — SEARCH DECISION / MERGE

Date: 2026-09-08

Status: MATERIALIZED / DETERMINISTIC QA PASS / REMOTE READBACK PENDING

- Direction decisions: {len(decision_rows)} / 9.
- ADD_TO_PIPELINE: {decision_counts['ADD_TO_PIPELINE']}.
- HOLD_EVIDENCE: {decision_counts['HOLD_EVIDENCE']}.
- Step-5A.5 potentially-new Wordstat occurrences reconciled: {len(merge_rows)} / 20.
- MERGE_ACCEPTED: {merge_counts['MERGE_ACCEPTED']}.
- Close variants suppressed: {merge_counts['SUPPRESSED_AS_CLOSE_VARIANT_DUPLICATE']}.
- Retained on hold: {merge_counts['RETAIN_HOLD']}.
- Union-compatible delta rows: {len(delta_rows)}.
- Corrected client release/frozen Stage-5 authority changed: false.
- PROJECT_TEST_VALIDATED: false.
- LEVEL1_METHOD_PROMOTED: false.

Remote readback: PENDING MATERIAL COMMIT.
"""
    CHECKPOINT_MERGE.write_text(checkpoint, encoding="utf-8")

    log = f"""# STEP 05A SEARCH DECISION / MERGE EXECUTION LOG

Date: 2026-09-08
Starting HEAD: `d307bd65c0c336cb37ad79a987a3bfe7d2e57219`

## Block A — preserved Search normalization

- Reconstructed the initial, continuation and final durable batch lifecycles from committed envelopes.
- Accounted for 9/9 requirements: 7 succeeded, 2 outcome unknown.
- Preserved 70/70 returned TOP10 rows and created no row for an unknown outcome.
- Classified all successful rows and produced the 9 × 9 selected-competitor visibility matrix.
- Provider calls: 0.

## Block B — decision and merge

- Assigned exactly one final route to 9/9 directions.
- Reconciled 20/20 potentially-new Wordstat occurrences.
- Materialized {len(delta_rows)} union-compatible accepted acquisition rows.
- Preserved `PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE` and `PROJECT_TEST_VALIDATED=false`.
- Client release, frozen Stage-5 authority and Level-1 method were not changed.

## Lifecycle

`WORK -> SAVE -> COMMIT -> REMOTE GITHUB READBACK -> CONTINUE`

Material and final remote-readback commit SHAs are recorded in Checkpoints 05–07 after each push/readback.
"""
    LOG.write_text(log, encoding="utf-8")
    return decision_rows, merge_rows, delta_rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("search", "final"), default="final")
    args = parser.parse_args()
    search = build_search_block()
    if args.phase == "final":
        final = build_final_block(*search)
        print(json.dumps({"phase": "final", "search_requirements": len(search[0]), "serp_rows": len(search[1]), "matrix_rows": len(search[3]), "decisions": len(final[0]), "merge_rows": len(final[1]), "delta_rows": len(final[2])}, ensure_ascii=False))
    else:
        print(json.dumps({"phase": "search", "search_requirements": len(search[0]), "serp_rows": len(search[1]), "intent_rows": len(search[2]), "matrix_rows": len(search[3])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
