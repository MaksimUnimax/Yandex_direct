#!/usr/bin/env python3
"""Materialize Step19 client-facing data views from canonical accepted authorities.

This script intentionally creates DERIVED views. It never rewrites upstream authority.
It uses Python stdlib only so it can run deterministically in CI.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "step19_correction_materialized"
OUT.mkdir(exist_ok=True)


def read_tsv(name: str):
    p = ROOT / name
    with p.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_csv(name: str, fieldnames, rows):
    p = OUT / name
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return p


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# 1) Full materialized semantic core
# ---------------------------------------------------------------------------
step08 = read_tsv("STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv")
step10 = read_tsv("STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv")
step11 = read_tsv("STEP_11_PHRASE_PAGE_MAP.tsv")

assert len(step08) == 2840, len(step08)
assert len({r["phrase"] for r in step08}) == 2840
assert len(step10) == 2840, len(step10)
assert len({r["phrase"] for r in step10}) == 2840
assert len(step11) == 2332, len(step11)
assert len({r["phrase"] for r in step11}) == 2332

idx08 = {r["phrase"]: r for r in step08}
idx10 = {r["phrase"]: r for r in step10}
assert set(idx11_phrase := {r["phrase"] for r in step11}) <= set(idx08)
assert idx11_phrase <= set(idx10)

semantic_rows = []
for p11 in step11:
    phrase = p11["phrase"]
    p08 = idx08[phrase]
    p10 = idx10[phrase]

    # Step11 is the current phrase/page authority. Step10 is retained as
    # assignment-lineage evidence and must reconcile to Step11 after corrections.
    semantic_rows.append({
        "phrase": phrase,
        "wordstat_observed_result_count": p08.get("max_result_count", ""),
        "wordstat_observed_association_count": p08.get("max_association_count", ""),
        "demand_semantics": "OBSERVED_PROVIDER_COUNT_NOT_GUARANTEED_EXACT_QUERY_FREQUENCY",
        "source_occurrences": p08.get("source_occurrences", ""),
        "result_occurrences": p08.get("result_occurrences", ""),
        "association_occurrences": p08.get("association_occurrences", ""),
        "source_ids": p08.get("source_ids", ""),
        "demand_provenance": p08.get("provenance", ""),
        "step08_search_disposition": p08.get("search_stage_disposition", ""),
        "step10_assignment_status": p10.get("assignment_status", ""),
        "step10_cluster_id": p10.get("cluster_id", ""),
        "step10_assignment_confidence": p10.get("assignment_confidence", ""),
        "step10_evidence_mode": p10.get("evidence_mode", ""),
        "step10_assignment_reason": p10.get("assignment_reason", ""),
        "current_assignment_status": p11.get("effective_assignment_status", ""),
        "current_cluster_id": p11.get("effective_cluster_id", ""),
        "user_task": p11.get("cluster_user_task", ""),
        "intent_type": p11.get("intent_type", ""),
        "business_fit": p11.get("business_fit", ""),
        "assignment_confidence": p11.get("assignment_confidence", ""),
        "current_target_url": p11.get("target_url", ""),
        "ownership_state": p11.get("ownership_state", ""),
        "ownership_confidence": p11.get("ownership_confidence", ""),
        "mapping_applicability": p11.get("page_mapping_applicability", ""),
        "mapping_reason": p11.get("mapping_reason", ""),
        "evidence_provenance": p11.get("evidence_provenance", ""),
        "correction_source": p11.get("correction_source", ""),
        "materialized_view_status": "DERIVED_FROM_CANONICAL_STEP08_STEP10_STEP11",
    })

semantic_fields = list(semantic_rows[0])
semantic_file = write_csv("STEP_19_03_SEMANTIC_CORE_MATERIALIZED.csv", semantic_fields, semantic_rows)

# ---------------------------------------------------------------------------
# 2) Exact 112-package execution calibration board
# ---------------------------------------------------------------------------
actions = read_tsv("STEP_18_ACTION_REGISTER.tsv")
action_by_id = {r["action_id"]: r for r in actions}
assert len(actions) == 34

holds = read_tsv("STEP_18_HOLD_RECHECK_LEDGER.tsv")
hold_by_id = {r["hold_id"]: r for r in holds}
assert len(holds) == 20

wp = json.loads((ROOT / "STEP_18_WORK_PACKAGE_REGISTER.json").read_text(encoding="utf-8"))
assert wp["package_count"] == 112

acceptance_by_measurement = {
    "M01_OWNER_ROLE_CORRECTION": "Verify current intended owner/specialist role is reflected in navigation/routing/content and no forbidden owner replacement occurred.",
    "M02_OVERLAP_DIFFERENTIATION": "Verify both retained pages have explicit non-conflicting roles/content scope; verify no unauthorized merge/delete/redirect/canonical action occurred.",
    "M03_CONTENT_ENHANCEMENT": "Verify the named missing decision/content block is present, accurate and integrated on the accepted owner without creating a duplicate URL.",
    "M04_AI_BOUNDED_CONTENT_RECHECK": "Re-read current page and verify the bounded candidate was either implemented where still missing or explicitly closed as no-change where already sufficient.",
    "M05_INTERNAL_LINK_IMPLEMENT": "Verify the exact approved source→target contextual link exists, is crawlable, uses useful anchor/context and both pages retain accepted roles.",
    "M06_ROUTE_TO_EXISTING": "Verify the subtask is routed to the accepted existing owner/support page and no unnecessary new URL was created.",
    "M07_HOLD": "Do not implement; verify the named blocker/recheck evidence has actually been resolved before the package can re-enter prioritization.",
}

metric_by_measurement = {
    "M01_OWNER_ROLE_CORRECTION": "Optional future Yandex Webmaster query→URL association; impressions/clicks/CTR/average position by affected query/URL when authorized.",
    "M02_OVERLAP_DIFFERENTIATION": "Optional future query→URL association across the overlapping pages; impressions/clicks/CTR/average position when authorized.",
    "M03_CONTENT_ENHANCEMENT": "Implementation QA first; optional future query/page impressions, clicks, CTR, average position; visits/conversions only with authorized first-party analytics.",
    "M04_AI_BOUNDED_CONTENT_RECHECK": "Implementation QA first; future repeated AI evidence only under a separately authorized measurement design; ordinary Search metrics if first-party access exists.",
    "M05_INTERNAL_LINK_IMPLEMENT": "Link/crawl acceptance first; optional future crawl depth/indexing and affected page/query Search metrics if authorized.",
    "M06_ROUTE_TO_EXISTING": "Routing acceptance first; optional future query→URL association and affected page Search metrics if authorized.",
    "M07_HOLD": "No success metric while blocked; measure only the blocker-resolution evidence required by the exact HOLD row.",
}

package_rows = []

for item in wp["exact_action_packages"]:
    aid = item["source_action_id"]
    a = action_by_id[aid]
    mc = item["measurement_class"]
    package_rows.append({
        "package_id": item["package_id"],
        "source_action_id": aid,
        "package_kind": "EXACT_ACTION",
        "analytical_priority": item["analytical_priority"],
        "what_to_do": a["description"],
        "target_or_scope": a["target_url_or_scope"],
        "dependency_role": a["dependency_role"],
        "depends_on_action_ids": a["depends_on_action_ids"],
        "uncertainty_state": a["uncertainty_state"],
        "implementation_owner": "TO_CALIBRATE",
        "effort": "TO_CALIBRATE",
        "capacity": "TO_CALIBRATE",
        "production_sequence": "PENDING_CALIBRATION",
        "calibration_state": "NEEDS_REAL_IMPLEMENTER_CLIENT_INPUT",
        "measurement_class": mc,
        "implementation_acceptance_check": acceptance_by_measurement[mc],
        "baseline_required": "CAPTURE_CURRENT_IMPLEMENTATION_STATE; private performance baseline only if separately available/authorized",
        "future_metric_source": metric_by_measurement[mc],
        "observation_window": "TO_CALIBRATE",
        "decision_rule": "KEEP if implementation matches accepted role and later evidence does not materially contradict it; otherwise REVISE/REOPEN the affected decision only.",
        "recheck_or_blocker": a["recheck_trigger"],
        "claim_boundary": a["limitations"],
    })

for item in wp["internal_link_packages"]:
    a = action_by_id[item["source_action_id"]]
    mc = item["measurement_class"]
    package_rows.append({
        "package_id": item["package_id"],
        "source_action_id": item["source_action_id"],
        "package_kind": "INTERNAL_LINK",
        "analytical_priority": item["analytical_priority"],
        "what_to_do": f"Implement accepted contextual internal-link handoff {','.join(item['link_refs'])}",
        "target_or_scope": a["target_url_or_scope"],
        "dependency_role": a["dependency_role"],
        "depends_on_action_ids": a["depends_on_action_ids"],
        "uncertainty_state": a["uncertainty_state"],
        "implementation_owner": "TO_CALIBRATE",
        "effort": "TO_CALIBRATE",
        "capacity": "TO_CALIBRATE",
        "production_sequence": "PENDING_CALIBRATION_AFTER_OWNER_ROLE_PREREQUISITES",
        "calibration_state": "NEEDS_REAL_IMPLEMENTER_CLIENT_INPUT",
        "measurement_class": mc,
        "implementation_acceptance_check": acceptance_by_measurement[mc],
        "baseline_required": "Confirm source/target live and accepted roles before link edit.",
        "future_metric_source": metric_by_measurement[mc],
        "observation_window": "TO_CALIBRATE",
        "decision_rule": "KEEP when exact approved edge is live and roles remain coherent; REVISE if source/target role changed.",
        "recheck_or_blocker": a["recheck_trigger"],
        "claim_boundary": a["limitations"],
    })

route_contract = wp["route_package_contract"]
for i, unit in enumerate(wp["route_packages"], 1):
    a = action_by_id[route_contract["source_action_id"]]
    mc = route_contract["measurement_class"]
    package_rows.append({
        "package_id": f"S18-WP-R{i:03d}",
        "source_action_id": route_contract["source_action_id"],
        "package_kind": "ROUTE_TO_EXISTING",
        "analytical_priority": "P3_LATER",
        "what_to_do": f"Implement accepted route-to-existing relationship for structural unit {unit}; apply current accepted Step12/14/14A target authority.",
        "target_or_scope": unit,
        "dependency_role": a["dependency_role"],
        "depends_on_action_ids": a["depends_on_action_ids"],
        "uncertainty_state": a["uncertainty_state"],
        "implementation_owner": "TO_CALIBRATE",
        "effort": "TO_CALIBRATE",
        "capacity": "TO_CALIBRATE",
        "production_sequence": "PENDING_CALIBRATION_AFTER_HIGHER_PRECEDENCE_OVERLAYS",
        "calibration_state": "NEEDS_REAL_IMPLEMENTER_CLIENT_INPUT",
        "measurement_class": mc,
        "implementation_acceptance_check": acceptance_by_measurement[mc],
        "baseline_required": "Confirm current accepted target authority and overlays before routing change.",
        "future_metric_source": metric_by_measurement[mc],
        "observation_window": "TO_CALIBRATE",
        "decision_rule": "KEEP when exact subtask routes to the accepted existing target with no unnecessary new URL; REVISE on material owner/offer change.",
        "recheck_or_blocker": a["recheck_trigger"],
        "claim_boundary": a["limitations"],
    })

for item in wp["hold_packages"]:
    h = hold_by_id[item["hold_id"]]
    mc = wp["hold_package_contract"]["measurement_class"]
    package_rows.append({
        "package_id": item["package_id"],
        "source_action_id": wp["hold_package_contract"]["source_action_id"],
        "package_kind": "HOLD_RECHECK",
        "analytical_priority": "HOLD",
        "what_to_do": f"Keep {item['structural_unit_id']} blocked until named evidence/policy gap is resolved; then re-enter prioritization.",
        "target_or_scope": item["structural_unit_id"],
        "dependency_role": "BLOCKED",
        "depends_on_action_ids": "",
        "uncertainty_state": h["blocker_class"],
        "implementation_owner": "NOT_APPLICABLE_UNTIL_BLOCKER_RESOLVED",
        "effort": "NOT_ESTIMATED_WHILE_BLOCKED",
        "capacity": "NOT_APPLICABLE_WHILE_BLOCKED",
        "production_sequence": "HOLD",
        "calibration_state": "BLOCKED_BY_NAMED_UNCERTAINTY",
        "measurement_class": mc,
        "implementation_acceptance_check": acceptance_by_measurement[mc],
        "baseline_required": h["current_reason"],
        "future_metric_source": metric_by_measurement[mc],
        "observation_window": "NOT_APPLICABLE_WHILE_BLOCKED",
        "decision_rule": "Only reopen when the exact recheck evidence becomes available; HOLD is not low value or rejection.",
        "recheck_or_blocker": h["recheck_trigger"],
        "claim_boundary": "Do not create page/content/service claims while the named blocker remains unresolved.",
    })

assert len(package_rows) == 112, len(package_rows)
assert len({r["package_id"] for r in package_rows}) == 112
assert sum(r["package_kind"] == "EXACT_ACTION" for r in package_rows) == 31
assert sum(r["package_kind"] == "INTERNAL_LINK" for r in package_rows) == 15
assert sum(r["package_kind"] == "ROUTE_TO_EXISTING" for r in package_rows) == 46
assert sum(r["package_kind"] == "HOLD_RECHECK" for r in package_rows) == 20

package_fields = list(package_rows[0])
package_file = write_csv("STEP_19_EXECUTION_CALIBRATION_BOARD_112.csv", package_fields, package_rows)

# ---------------------------------------------------------------------------
# 3) Measurement protocol
# ---------------------------------------------------------------------------
measurement_rows = [
    {
        "measurement_class": "M01_OWNER_ROLE_CORRECTION",
        "purpose": "Confirm exact owner/specialist responsibility was implemented without displacing valid supporting pages.",
        "implementation_acceptance": acceptance_by_measurement["M01_OWNER_ROLE_CORRECTION"],
        "baseline_required": "Current live owner/support roles and affected query/page evidence where available.",
        "current_job_private_baseline": "NOT_AVAILABLE_IN_BASE_PUBLIC_SCOPE",
        "future_optional_authorized_sources": "Yandex Webmaster query→URL analytics; client analytics/business data if separately provided.",
        "candidate_search_signals": "Query→URL association; impressions; clicks; CTR; average position.",
        "business_signals": "Visits/conversions/leads only when appropriate first-party data exists; no current claim.",
        "observation_window": "TO_CALIBRATE_WITH_IMPLEMENTATION_DATE_AND_DATA_AVAILABILITY",
        "decision_rule": "KEEP if owner role is correctly implemented and later evidence supports/no-materially-contradicts it; REVISE on material role conflict.",
    },
    {
        "measurement_class": "M02_OVERLAP_DIFFERENTIATION",
        "purpose": "Confirm overlapping retained pages have distinct roles and do not require unsupported destructive consolidation.",
        "implementation_acceptance": acceptance_by_measurement["M02_OVERLAP_DIFFERENTIATION"],
        "baseline_required": "Current page roles/content overlap; future private query→URL split only if authorized.",
        "current_job_private_baseline": "NOT_AVAILABLE_IN_BASE_PUBLIC_SCOPE",
        "future_optional_authorized_sources": "Yandex Webmaster query→URL export across both pages.",
        "candidate_search_signals": "Query→URL distribution; impressions; clicks; CTR; average position by page/query.",
        "business_signals": "Only with client first-party data; no causal/revenue guarantee.",
        "observation_window": "TO_CALIBRATE",
        "decision_rule": "KEEP differentiated roles if implementation is clear and no stronger evidence of harmful overlap appears; otherwise reopen the exact boundary.",
    },
    {
        "measurement_class": "M03_CONTENT_ENHANCEMENT",
        "purpose": "Confirm named evidence-backed missing decision/content depth was added to the accepted owner.",
        "implementation_acceptance": acceptance_by_measurement["M03_CONTENT_ENHANCEMENT"],
        "baseline_required": "Pre-edit page content snapshot and named missing need.",
        "current_job_private_baseline": "NOT_AVAILABLE_IN_BASE_PUBLIC_SCOPE",
        "future_optional_authorized_sources": "Yandex Webmaster; Metrika/client conversion analytics where authorized.",
        "candidate_search_signals": "Affected query/page impressions, clicks, CTR, average position; indexing/visibility where relevant.",
        "business_signals": "Visits/conversions/leads only with real analytics and suitable attribution; no promised uplift.",
        "observation_window": "TO_CALIBRATE_AFTER_DEPLOYMENT",
        "decision_rule": "KEEP if content gap is correctly closed and later evidence is not materially adverse; REVISE content/role if evidence contradicts the intended task fit.",
    },
    {
        "measurement_class": "M04_AI_BOUNDED_CONTENT_RECHECK",
        "purpose": "Handle bounded AI-supported content candidate without converting a snapshot into architecture or sitewide visibility claims.",
        "implementation_acceptance": acceptance_by_measurement["M04_AI_BOUNDED_CONTENT_RECHECK"],
        "baseline_required": "Current page read + accepted bounded case evidence.",
        "current_job_private_baseline": "NOT_APPLICABLE_TO_BOUNDED_AI_SNAPSHOT",
        "future_optional_authorized_sources": "Repeated AI/GenSearch measurement only under separate approved sampling design; ordinary Yandex metrics if authorized.",
        "candidate_search_signals": "No single AI run is a success metric; ordinary Search metrics may supplement content evaluation.",
        "business_signals": "Not inferable from bounded snapshots.",
        "observation_window": "TO_CALIBRATE; longitudinal AI claim requires separate design",
        "decision_rule": "Close as NO_CHANGE if current page already has sufficient depth; otherwise implement bounded enhancement; never infer architecture/sitewide AI performance from one case.",
    },
    {
        "measurement_class": "M05_INTERNAL_LINK_IMPLEMENT",
        "purpose": "Confirm exact approved contextual handoff exists and preserves current page roles.",
        "implementation_acceptance": acceptance_by_measurement["M05_INTERNAL_LINK_IMPLEMENT"],
        "baseline_required": "Source/target live status, accepted roles and edge absence/current state.",
        "current_job_private_baseline": "NOT_REQUIRED_FOR_IMPLEMENTATION_ACCEPTANCE",
        "future_optional_authorized_sources": "Crawl/topology check; Yandex Webmaster page/query data if authorized.",
        "candidate_search_signals": "Crawlability/indexing plus affected page/query impressions/clicks/CTR/position where meaningful.",
        "business_signals": "Optional first-party path/conversion data only when available.",
        "observation_window": "TO_CALIBRATE",
        "decision_rule": "KEEP if exact link is live/useful/crawlable and page roles remain coherent; REVISE if role changed or link creates misleading handoff.",
    },
    {
        "measurement_class": "M06_ROUTE_TO_EXISTING",
        "purpose": "Confirm subtask routes to the accepted existing owner/support asset instead of creating unnecessary URLs.",
        "implementation_acceptance": acceptance_by_measurement["M06_ROUTE_TO_EXISTING"],
        "baseline_required": "Current accepted target authority including later explicit overlays.",
        "current_job_private_baseline": "NOT_REQUIRED_FOR_STRUCTURAL_ACCEPTANCE",
        "future_optional_authorized_sources": "Yandex Webmaster query→URL analytics; client analytics if material and authorized.",
        "candidate_search_signals": "Query→URL association and page Search metrics where available.",
        "business_signals": "Optional first-party data; no current business-impact claim.",
        "observation_window": "TO_CALIBRATE",
        "decision_rule": "KEEP if correct existing target serves the task; reopen only when current-site/business/Search evidence materially changes owner suitability.",
    },
    {
        "measurement_class": "M07_HOLD",
        "purpose": "Keep blocked items from becoming implementation work before named uncertainty is resolved.",
        "implementation_acceptance": acceptance_by_measurement["M07_HOLD"],
        "baseline_required": "Exact blocker/current reason from HOLD ledger.",
        "current_job_private_baseline": "VARIES_BY_BLOCKER; DO_NOT_INVENT",
        "future_optional_authorized_sources": "Exact public/client/normative/Search/provider evidence named by the recheck trigger.",
        "candidate_search_signals": "Not a performance measurement class while blocked.",
        "business_signals": "Not applicable until blocker resolves.",
        "observation_window": "NOT_APPLICABLE_WHILE_BLOCKED",
        "decision_rule": "Only re-enter prioritization after exact blocker is resolved; HOLD never means low value or rejection.",
    },
]

measurement_fields = list(measurement_rows[0])
measurement_file = write_csv("STEP_19_MEASUREMENT_PROTOCOL.csv", measurement_fields, measurement_rows)

# ---------------------------------------------------------------------------
# 4) Copy existing compact client tables into one correction data bundle
# ---------------------------------------------------------------------------
copy_names = [
    "STEP_19_02_BUSINESS_AND_PAGE_MODEL.tsv",
    "STEP_19_04_SEARCH_VS_AI_GAP_MATRIX.tsv",
    "STEP_19_05_PAGE_ACTION_MAP.tsv",
    "STEP_19_06_SOURCE_COMPETITOR_OBSERVATIONS.tsv",
    "STEP_19_07_PRIORITY_ACTION_PLAN.tsv",
]
for name in copy_names:
    (OUT / name).write_bytes((ROOT / name).read_bytes())

# ---------------------------------------------------------------------------
# 5) Machine QA / provenance
# ---------------------------------------------------------------------------
qa = {
    "date": "2026-09-03",
    "step": 19,
    "status": "PASS_MATERIALIZATION_DATA_BUILD",
    "view_type": "DERIVED_NOT_CANONICAL",
    "canonical_sources": {
        "semantic": [
            "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv",
            "STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv",
            "STEP_11_PHRASE_PAGE_MAP.tsv",
        ],
        "actions": [
            "STEP_18_ACTION_REGISTER.tsv",
            "STEP_18_WORK_PACKAGE_REGISTER.json",
            "STEP_18_HOLD_RECHECK_LEDGER.tsv",
        ],
    },
    "accounting": {
        "step08_master_phrase_rows": len(step08),
        "step10_master_phrase_rows": len(step10),
        "step11_active_phrase_rows": len(step11),
        "materialized_semantic_rows": len(semantic_rows),
        "unresolved_current_rows": sum(r["current_assignment_status"] == "SEARCH_REQUIRED" for r in semantic_rows),
        "execution_calibration_rows": len(package_rows),
        "exact_action_packages": sum(r["package_kind"] == "EXACT_ACTION" for r in package_rows),
        "internal_link_packages": sum(r["package_kind"] == "INTERNAL_LINK" for r in package_rows),
        "route_packages": sum(r["package_kind"] == "ROUTE_TO_EXISTING" for r in package_rows),
        "hold_packages": sum(r["package_kind"] == "HOLD_RECHECK" for r in package_rows),
        "measurement_classes": len(measurement_rows),
    },
    "non_fabrication": {
        "unknown_owner_values_replaced_with_guess": 0,
        "unknown_effort_values_replaced_with_guess": 0,
        "unknown_capacity_values_replaced_with_guess": 0,
        "committed_schedule_created": False,
        "numeric_performance_targets_invented": False,
        "new_provider_calls_required": False,
    },
    "outputs": {},
}

for p in [semantic_file, package_file, measurement_file] + [OUT / n for n in copy_names]:
    qa["outputs"][p.name] = {"bytes": p.stat().st_size, "sha256": sha256(p)}

qa_file = OUT / "STEP_19_CORRECTION_DATA_QA.json"
qa_file.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(json.dumps(qa, ensure_ascii=False, indent=2))
