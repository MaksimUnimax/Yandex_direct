#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "STEP_10_FRESH_R1_ASSIGNMENT.tsv"
OUT = ROOT / "STEP_10_FRESH_R1_PASS3_REVIEW_PACK.tsv"

with SRC.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f, delimiter="\t"))

active = [r for r in rows if r["source_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"}]
if len(active) != 2332:
    raise RuntimeError(f"expected 2332 active rows, got {len(active)}")

with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["qa_row", "phrase", "source_disposition", "assignment_status", "cluster_id", "evidence_mode"])
    for i, r in enumerate(active, 1):
        w.writerow([i, r["phrase"], r["source_disposition"], r["assignment_status"], r["cluster_id"], r["evidence_mode"]])

print(f"PASS3_REVIEW_PACK_ROWS={len(active)}")
