#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b


def main() -> None:
    rows = b.read_tsv(b.INPUT)
    decisions = b.read_tsv(b.DECISIONS)
    comparisons = b.read_tsv(b.COMPARISONS)

    assert len(rows) == b.EXPECTED["total"]
    assert len({b.norm(r["phrase"]) for r in rows}) == b.EXPECTED["total"]
    disposition_counts = Counter(r["search_stage_disposition"] for r in rows)
    for key in ("CORE_CANDIDATE", "REVIEW_SEARCH", "REVIEW_DEFERRED", "EXCLUDED_PRESERVED"):
        assert disposition_counts[key] == b.EXPECTED[key], (key, disposition_counts[key])
    assert disposition_counts["CORE_CANDIDATE"] + disposition_counts["REVIEW_SEARCH"] == b.EXPECTED["active"]
    assert len(decisions) == b.EXPECTED["direct_probes"]
    assert len(comparisons) == b.EXPECTED["duplicate_comparisons"]

    direct_by_query = {b.norm(r["query"]): r for r in decisions}
    input_by_phrase = {b.norm(r["phrase"]): r for r in rows}
    exact_direct = {q: d for q, d in direct_by_query.items() if q in input_by_phrase}
    control_direct = {q: d for q, d in direct_by_query.items() if q not in input_by_phrase}
    assert len(exact_direct) + len(control_direct) == b.EXPECTED["direct_probes"]

    # Control queries are evidence about task/cluster boundaries, not direct evidence for any Step-08 phrase row.
    control_by_task: dict[str, list[dict[str, str]]] = defaultdict(list)
    control_audit = []
    for q, d in sorted(control_direct.items()):
        task_id, reason, confidence = b.classify_semantic(d["query"])
        assert task_id, (d["query"], reason)
        control_by_task[task_id].append(d)
        control_audit.append({
            "record_type": "CONTROL_ANCHOR_AUDIT",
            "phrase": d["query"],
            "related_id": d["probe_id"],
            "cluster_evidence_state": "SERP_SUPPORTED_CONTROL_ANCHOR",
            "reason": f"Control/anchor query consumed at cluster level only: {d['observed_serp_job']} / {d['dominant_result_type']}; {reason}",
            "direct_evidence": "DIRECT_CONTROL_QUERY__NOT_TRANSFERRED_TO_UNPROBED_PHRASES",
        })

    dup4_phrases = {
        b.norm("пластиковые окна от производителя rehau"),
        b.norm("пластиковые окна рехау от производителя"),
    }

    out_rows: list[dict[str, str]] = []
    boundary_rows: list[dict[str, str]] = list(control_audit)
    cluster_members: dict[str, list[dict[str, str]]] = defaultdict(list)
    exact_direct_consumed = 0

    for src in rows:
        phrase = src["phrase"]
        pnorm = b.norm(phrase)
        disposition = src["search_stage_disposition"]
        direct = exact_direct.get(pnorm)
        if direct:
            exact_direct_consumed += 1

        row = {
            "phrase": phrase,
            "input_disposition": disposition,
            "corrected_status": src["corrected_status"],
            "corrected_reason": src["corrected_reason"],
            "user_task": "",
            "intent_orientation": "",
            "material_modifiers": b.material_modifiers(phrase),
            "public_business_fit": "",
            "step09_probe_id": direct["probe_id"] if direct else "",
            "step09_evidence_scope": direct["evidence_scope"] if direct else "NO_DIRECT_STEP09_SERP",
            "observed_serp_job": direct["observed_serp_job"] if direct else "",
            "dominant_result_type": direct["dominant_result_type"] if direct else "",
            "step09_handoff": direct["step10_handoff"] if direct else "",
            "cluster_id": "",
            "cluster_role": "",
            "cluster_evidence_state": "",
            "assignment_reason": "",
            "confidence": "",
            "additional_search_required": "false",
        }

        if disposition == "REVIEW_DEFERRED":
            row.update({
                "user_task": "Deferred upstream evidence state",
                "intent_orientation": "DEFERRED",
                "public_business_fit": "UNKNOWN_PUBLIC_FIT",
                "cluster_role": "DEFERRED_PRESERVED",
                "cluster_evidence_state": "DEFERRED_PRESERVED",
                "assignment_reason": "Step-08 REVIEW_DEFERRED preserved; Step 10 not authorized to force-cluster it",
                "confidence": "N/A",
            })
            out_rows.append(row)
            continue

        if disposition == "EXCLUDED_PRESERVED":
            row.update({
                "user_task": "Excluded upstream state preserved",
                "intent_orientation": "EXCLUDED",
                "public_business_fit": "OUTSIDE_OR_EXCLUDED_UPSTREAM",
                "cluster_role": "EXCLUDED_PRESERVED",
                "cluster_evidence_state": "EXCLUDED_PRESERVED",
                "assignment_reason": "Accepted Step-07/08 exclusion preserved; not reintroduced by clustering",
                "confidence": "N/A",
            })
            out_rows.append(row)
            continue

        task_id, semantic_reason, semantic_conf = b.classify_semantic(phrase)

        direct_outside = bool(direct and (
            direct["step10_handoff"].startswith("OUTSIDE_")
            or direct["dominant_result_type"] in {"REAL_ESTATE_PROJECT_CATALOG", "REAL_ESTATE_TRAVEL_INSPIRATION", "SECOND_HAND_MARKETPLACE"}
        ))
        direct_info = bool(direct and any(x in direct["dominant_result_type"] for x in ("INFORMATION", "REVIEWS", "VIDEO", "NAVIGATIONAL")))
        semantic_commercial = bool(task_id and b.TASKS[task_id][1].startswith("COMMERCIAL"))
        direct_contradiction = bool(direct_outside and task_id and b.TASKS[task_id][2] != "OUTSIDE")
        if direct_info and semantic_commercial and direct and direct["step10_handoff"].startswith("INFORMATIONAL_"):
            direct_contradiction = True

        if pnorm in dup4_phrases:
            label, intent, fit = b.task_fields(task_id)
            row.update({
                "user_task": label or "Rehau manufacturer-query boundary",
                "intent_orientation": intent,
                "public_business_fit": fit,
                "cluster_role": "BOUNDARY_REVIEW",
                "cluster_evidence_state": "MIXED_OR_BOUNDARY_REVIEW",
                "assignment_reason": "Mandatory DUP-0004 override: Step-09 exact URL overlap 1/10; no auto-merge",
                "confidence": "HIGH",
                "additional_search_required": "true",
            })
            boundary_rows.append({
                "record_type": "PHRASE_BOUNDARY",
                "phrase": phrase,
                "related_id": "DUP-0004",
                "cluster_evidence_state": "MIXED_OR_BOUNDARY_REVIEW",
                "reason": row["assignment_reason"],
                "direct_evidence": f"probe={row['step09_probe_id']}|serp_job={row['observed_serp_job']}",
            })
            out_rows.append(row)
            continue

        if direct_contradiction:
            label, intent, fit = b.task_fields(task_id)
            row.update({
                "user_task": label or direct["observed_serp_job"],
                "intent_orientation": intent,
                "public_business_fit": fit,
                "cluster_role": "BOUNDARY_REVIEW",
                "cluster_evidence_state": "MIXED_OR_BOUNDARY_REVIEW",
                "assignment_reason": f"Direct Step-09 SERP contradicts semantic grouping hypothesis: {direct['step10_handoff']}",
                "confidence": "MEDIUM",
                "additional_search_required": "true",
            })
            boundary_rows.append({
                "record_type": "PHRASE_BOUNDARY",
                "phrase": phrase,
                "related_id": direct["probe_id"],
                "cluster_evidence_state": "MIXED_OR_BOUNDARY_REVIEW",
                "reason": row["assignment_reason"],
                "direct_evidence": f"serp_job={direct['observed_serp_job']}|result_type={direct['dominant_result_type']}",
            })
            out_rows.append(row)
            continue

        if not task_id:
            row.update({
                "user_task": "Unresolved material user task",
                "intent_orientation": "UNKNOWN_OR_MIXED",
                "public_business_fit": "UNKNOWN_PUBLIC_FIT",
                "cluster_role": "UNRESOLVED",
                "cluster_evidence_state": "SEARCH_REQUIRED",
                "assignment_reason": semantic_reason,
                "confidence": "LOW",
                "additional_search_required": "true",
            })
            boundary_rows.append({
                "record_type": "SEARCH_REQUIRED",
                "phrase": phrase,
                "related_id": direct["probe_id"] if direct else "",
                "cluster_evidence_state": "SEARCH_REQUIRED",
                "reason": semantic_reason,
                "direct_evidence": f"serp_job={direct['observed_serp_job']}" if direct else "NO_DIRECT_STEP09_SERP",
            })
            out_rows.append(row)
            continue

        label, intent, fit = b.task_fields(task_id)
        row.update({
            "user_task": label,
            "intent_orientation": intent,
            "public_business_fit": fit,
            "cluster_id": task_id,
            "cluster_role": "DIRECT_SERP_MEMBER" if direct else "SEMANTIC_MEMBER_NO_DIRECT_SERP",
            "cluster_evidence_state": "SERP_SUPPORTED" if direct else "SEMANTIC_SUPPORTED_NO_DIRECT_SERP",
            "assignment_reason": semantic_reason + (f"; direct Step-09 evidence: {direct['observed_serp_job']} / {direct['dominant_result_type']}" if direct else ""),
            "confidence": direct["confidence"] if direct else semantic_conf,
        })
        cluster_members[task_id].append(row)
        out_rows.append(row)

    assert len(out_rows) == b.EXPECTED["total"]
    assert exact_direct_consumed == len(exact_direct)
    direct_consumed_total = exact_direct_consumed + len(control_direct)
    assert direct_consumed_total == b.EXPECTED["direct_probes"]

    dup4_seen = False
    for comp in comparisons:
        gid = comp["group_id"]
        if gid == "DUP-0004":
            dup4_seen = True
            assert comp["exact_url_overlap"] == "1"
            assert "DO_NOT_AUTO_MERGE" in comp["step10_handoff"]
        boundary_rows.append({
            "record_type": "DUPLICATE_COMPARISON_AUDIT",
            "phrase": f"{comp['query_a']} <> {comp['query_b']}",
            "related_id": f"{comp['comparison_id']}|{gid}",
            "cluster_evidence_state": "MIXED_OR_BOUNDARY_REVIEW" if gid == "DUP-0004" else "SERP_SUPPORTED_CANDIDATE_PAIR",
            "reason": comp["step09_conclusion"] + " / " + comp["step10_handoff"],
            "direct_evidence": f"exact_url_overlap={comp['exact_url_overlap']}/{comp['top_n_a']}",
        })
    assert dup4_seen

    assign_fields = [
        "phrase", "input_disposition", "corrected_status", "corrected_reason", "user_task",
        "intent_orientation", "material_modifiers", "public_business_fit", "step09_probe_id",
        "step09_evidence_scope", "observed_serp_job", "dominant_result_type", "step09_handoff",
        "cluster_id", "cluster_role", "cluster_evidence_state", "assignment_reason", "confidence",
        "additional_search_required",
    ]
    with b.OUT_ASSIGN.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=assign_fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(out_rows)

    src_by_phrase = {r["phrase"]: r for r in rows}
    summary_rows = []
    for task_id in sorted(cluster_members):
        members = cluster_members[task_id]
        label, intent, fit = b.TASKS[task_id]
        primary = max(members, key=lambda r: (int(src_by_phrase[r["phrase"]].get("max_result_count") or 0), -len(r["phrase"]), r["phrase"]))["phrase"]
        direct_members = sum(bool(r["step09_probe_id"]) for r in members)
        control_count = len(control_by_task.get(task_id, []))
        semantic_count = len(members) - direct_members
        summary_rows.append({
            "cluster_id": task_id,
            "cluster_label": label,
            "user_task": label,
            "intent_orientation": intent,
            "public_business_fit": fit,
            "primary_query": primary,
            "member_count": str(len(members)),
            "direct_serp_member_count": str(direct_members),
            "direct_serp_control_count": str(control_count),
            "semantic_only_member_count": str(semantic_count),
            "cluster_evidence_state": "SERP_SUPPORTED" if direct_members or control_count else "SEMANTIC_SUPPORTED_NO_DIRECT_SERP",
            "boundary_notes": "Working Step-10 task cluster only; control anchors do not transfer direct evidence to individual unprobed phrases",
        })
    summary_fields = list(summary_rows[0].keys())
    with b.OUT_SUMMARY.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=summary_fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(summary_rows)

    boundary_fields = ["record_type", "phrase", "related_id", "cluster_evidence_state", "reason", "direct_evidence"]
    with b.OUT_BOUNDARY.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=boundary_fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(boundary_rows)

    sample_rows = []
    for task_id in sorted(cluster_members):
        members = sorted(cluster_members[task_id], key=lambda r: b.norm(r["phrase"]))
        chosen = []
        for r in members[:3] + members[-2:] + [x for x in members if x["step09_probe_id"]]:
            if r["phrase"] not in {x["phrase"] for x in chosen}:
                chosen.append(r)
        for r in chosen:
            sample_rows.append({
                "sample_type": "CLUSTER_MEMBER", "cluster_id": task_id, "phrase": r["phrase"],
                "user_task": r["user_task"], "intent_orientation": r["intent_orientation"],
                "evidence_state": r["cluster_evidence_state"], "step09_probe_id": r["step09_probe_id"],
                "reason": r["assignment_reason"],
            })
    for task_id, controls in sorted(control_by_task.items()):
        for d in controls:
            sample_rows.append({
                "sample_type": "CONTROL_ANCHOR", "cluster_id": task_id, "phrase": d["query"],
                "user_task": b.TASKS[task_id][0], "intent_orientation": b.TASKS[task_id][1],
                "evidence_state": "SERP_SUPPORTED_CONTROL_ANCHOR", "step09_probe_id": d["probe_id"],
                "reason": f"Cluster-level control only: {d['observed_serp_job']} / {d['dominant_result_type']}",
            })
    unresolved = [r for r in out_rows if r["cluster_evidence_state"] == "SEARCH_REQUIRED"]
    for r in sorted(unresolved, key=lambda x: b.norm(x["phrase"]))[:100]:
        sample_rows.append({
            "sample_type": "SEARCH_REQUIRED_SAMPLE", "cluster_id": "", "phrase": r["phrase"],
            "user_task": r["user_task"], "intent_orientation": r["intent_orientation"],
            "evidence_state": r["cluster_evidence_state"], "step09_probe_id": r["step09_probe_id"],
            "reason": r["assignment_reason"],
        })
    sample_fields = ["sample_type", "cluster_id", "phrase", "user_task", "intent_orientation", "evidence_state", "step09_probe_id", "reason"]
    with b.OUT_SAMPLE.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=sample_fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(sample_rows)

    states = Counter(r["cluster_evidence_state"] for r in out_rows)
    active_rows = [r for r in out_rows if r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"}]
    assert len(active_rows) == b.EXPECTED["active"]
    assert all(r["cluster_evidence_state"] in {"SERP_SUPPORTED", "SEMANTIC_SUPPORTED_NO_DIRECT_SERP", "MIXED_OR_BOUNDARY_REVIEW", "SEARCH_REQUIRED"} for r in active_rows)
    assert states["DEFERRED_PRESERVED"] == b.EXPECTED["REVIEW_DEFERRED"]
    assert states["EXCLUDED_PRESERVED"] == b.EXPECTED["EXCLUDED_PRESERVED"]
    assert sum(states.values()) == b.EXPECTED["total"]

    unprobed_direct_claim = 0
    for r in out_rows:
        if not r["step09_probe_id"] and r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"}:
            if r["step09_evidence_scope"] != "NO_DIRECT_STEP09_SERP":
                unprobed_direct_claim += 1
    assert unprobed_direct_claim == 0

    dup4_assign = [r for r in out_rows if b.norm(r["phrase"]) in dup4_phrases]
    assert len(dup4_assign) == 2
    assert all(r["cluster_id"] == "" and r["cluster_evidence_state"] == "MIXED_OR_BOUNDARY_REVIEW" for r in dup4_assign)

    qa = {
        "status": "MACHINE_QA_PASS__MANUAL_SEMANTIC_QA_REQUIRED",
        "total_phrase_keys": len(out_rows),
        "active_search_stage_rows": len(active_rows),
        "input_disposition_counts": dict(sorted(disposition_counts.items())),
        "cluster_count": len(summary_rows),
        "cluster_evidence_state_counts": dict(sorted(states.items())),
        "direct_step09_probes_expected": b.EXPECTED["direct_probes"],
        "direct_step09_exact_phrase_decisions_consumed": exact_direct_consumed,
        "direct_step09_control_anchors_consumed": len(control_direct),
        "direct_step09_probes_consumed": direct_consumed_total,
        "duplicate_comparisons_expected": b.EXPECTED["duplicate_comparisons"],
        "duplicate_comparisons_consumed": len(comparisons),
        "dup0004_auto_merged": False,
        "unprobed_rows_claiming_direct_serp": unprobed_direct_claim,
        "silent_drops": b.EXPECTED["total"] - len(out_rows),
        "review_deferred_preserved": states["DEFERRED_PRESERVED"],
        "excluded_preserved": states["EXCLUDED_PRESERVED"],
        "search_required_rows": states["SEARCH_REQUIRED"],
        "mixed_boundary_rows": states["MIXED_OR_BOUNDARY_REVIEW"],
        "semantic_supported_no_direct_serp_rows": states["SEMANTIC_SUPPORTED_NO_DIRECT_SERP"],
        "serp_supported_rows": states["SERP_SUPPORTED"],
        "manual_semantic_qa_required": True,
        "manual_semantic_qa_pass": False,
        "page_ownership_decisions": 0,
        "structural_action_decisions": 0,
        "cannibalization_decisions": 0,
        "provider_requests": 0,
        "provider_cost_rub": 0,
    }
    b.OUT_QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qa, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
