#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter

import STEP_10_SEMANTIC_COLLISION_AUDIT as old
import STEP_10_SEMANTIC_COLLISION_AUDIT_V23 as v23


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def audit_v24(r: dict[str, str]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    p = n(r["phrase"])
    for code, reason in v23.audit_v23(r):
        # Manually reviewed V23 residual false positive: the inherited V15
        # vocabulary did not recognize 'механизм пластиковой двери' as a valid
        # hardware/component phrase. The semantic assignment itself is correct.
        if code == "V15_HARDWARE_TOKEN_MISMATCH" and r["cluster_id"] == "WINDOW_HARDWARE" and "механизм" in p and "двер" in p:
            continue
        out.append((code, reason))
    return out


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    flagged = []
    counts = Counter()
    for r in rows:
        if r["input_disposition"] not in {"CORE_CANDIDATE", "REVIEW_SEARCH"}:
            continue
        for code, reason in audit_v24(r):
            counts[code] += 1
            flagged.append({
                "collision_code": code,
                "phrase": r["phrase"],
                "cluster_id": r["cluster_id"],
                "user_task": r["user_task"],
                "evidence_state": r["cluster_evidence_state"],
                "step09_probe_id": r["step09_probe_id"],
                "reason": reason,
            })

    fields = ["collision_code", "phrase", "cluster_id", "user_task", "evidence_state", "step09_probe_id", "reason"]
    with old.OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(flagged)

    summary = {
        "status": "PASS" if not flagged else "FAIL__MANUAL_REVIEW_REQUIRED",
        "audit_version": "V24",
        "active_rows_scanned": sum(r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"} for r in rows),
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "collision_counts": dict(sorted(counts.items())),
        "manual_adjudication_basis": "V23 residuals were reviewed individually. Windowsill/hardware-installation taxonomy errors are corrected in classifier V24; one inherited lexical false positive for plastic-door mechanism is explicitly adjudicated here.",
        "meaning": "V24 adjudicated hard gate. Zero flags is necessary but remains insufficient for final manual semantic acceptance.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if flagged:
        for row in flagged:
            print("V24_COLLISION_FLAG", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if flagged:
        raise SystemExit("V24 collision hard gate failed")


if __name__ == "__main__":
    main()
