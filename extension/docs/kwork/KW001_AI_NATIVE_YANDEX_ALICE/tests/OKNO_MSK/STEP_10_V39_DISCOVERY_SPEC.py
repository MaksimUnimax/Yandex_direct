#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent
LEDGER = BASE / "STEP_10_V38_FULL_MANUAL_ERROR_LEDGER.tsv"


def read_rows() -> list[dict[str, str]]:
    with LEDGER.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    assert len(rows) == 22, len(rows)
    assert len({r["phrase"] for r in rows}) == 22
    assert all(not r.get("step09_probe_id") for r in rows)
    assert all(r.get("direct_serp_transfer") == "NO" for r in rows)
    return rows


ROWS = read_rows()
EXPECTED_BY_PHRASE = {r["phrase"]: r for r in ROWS}

if __name__ == "__main__":
    print(f"V39_FROZEN_DISCOVERY_SPEC_PASS rows={len(ROWS)}")
