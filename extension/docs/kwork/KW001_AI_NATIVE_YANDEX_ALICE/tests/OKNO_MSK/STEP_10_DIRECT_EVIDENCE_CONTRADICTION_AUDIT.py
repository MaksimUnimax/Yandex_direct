#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ASSIGN = BASE / "STEP_10_CLUSTER_ASSIGNMENTS.tsv"
OUT_JSON = BASE / "STEP_10_DIRECT_EVIDENCE_CONTRADICTION_AUDIT.json"
OUT_TSV = BASE / "STEP_10_DIRECT_EVIDENCE_CONTRADICTION_AUDIT.tsv"


def direct_family(result_type: str) -> str:
    r = (result_type or "").upper()
    if "SERVICE" in r or r in {"LOCAL_SERVICE", "COMMERCIAL_REPAIR_SERVICE"}:
        return "SERVICE"
    if "PRODUCT" in r or r in {"PRODUCT_CATALOG", "LOCAL_COMMERCIAL_PRODUCT", "OFFICIAL_SHOP_PRODUCT_HEAVY"}:
        return "PRODUCT"
    return "OTHER"


def semantic_family(intent: str) -> str:
    i = (intent or "").upper()
    if i.startswith("COMMERCIAL_SERVICE"):
        return "SERVICE"
    if i.startswith("COMMERCIAL_PRODUCT"):
        return "PRODUCT"
    return "OTHER"


def main() -> None:
    with ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    checked = 0
    contradictions = []
    for r in rows:
        if not r["step09_probe_id"] or not r["cluster_id"]:
            continue
        df = direct_family(r["dominant_result_type"])
        sf = semantic_family(r["intent_orientation"])
        if df == "OTHER" or sf == "OTHER":
            continue
        checked += 1
        if df != sf:
            contradictions.append({
                "phrase": r["phrase"],
                "probe_id": r["step09_probe_id"],
                "dominant_result_type": r["dominant_result_type"],
                "direct_family": df,
                "cluster_id": r["cluster_id"],
                "intent_orientation": r["intent_orientation"],
                "semantic_family": sf,
                "observed_serp_job": r["observed_serp_job"],
                "step09_handoff": r["step09_handoff"],
            })

    fields = [
        "phrase", "probe_id", "dominant_result_type", "direct_family", "cluster_id",
        "intent_orientation", "semantic_family", "observed_serp_job", "step09_handoff",
    ]
    with OUT_TSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(contradictions)

    summary = {
        "status": "PASS" if not contradictions else "FAIL",
        "direct_clustered_rows_with_comparable_family": checked,
        "service_product_contradictions": len(contradictions),
        "rule": "Direct Step-09 COMMERCIAL_SERVICE vs Step-10 COMMERCIAL_PRODUCT, or the reverse, is a material contradiction and cannot pass as a normal cluster member.",
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    assert not contradictions, contradictions


if __name__ == "__main__":
    main()
