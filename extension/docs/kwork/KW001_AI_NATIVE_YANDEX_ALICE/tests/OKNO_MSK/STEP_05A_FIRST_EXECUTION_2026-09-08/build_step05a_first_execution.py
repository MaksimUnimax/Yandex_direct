#!/usr/bin/env python3
"""Deterministically materialize the OKNO_MSK Step 5A first execution.

The builder reads preserved repository evidence only. It performs no network or
provider calls. Phases are intentionally separate so every material block can
be saved, committed and read back before the next block begins.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit


JOB = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

STARTING_HEAD = "c043fda14c51b18f4016aa26ff3e3f7e7c121a13"
COMBINED = OUT / "STEP_05A_SERP_COMBINED_750.tsv"
QA = OUT / "STEP_05A_FIRST_EXECUTION_QA.json"

SOURCE_FILES = [
    JOB / "STEP_09_SERP_RESULTS.tsv",
    JOB / "STEP_09_SERP_R2_PROJECTION_RAW_PART_01.tsv",
    JOB / "STEP_09_SERP_R2_PROJECTION_RAW_PART_02.tsv",
    JOB / "STEP_09_SERP_R2_PROJECTION_RAW_PART_03.tsv",
    JOB / "STEP_09_SERP_R2_PROJECTION_RAW_PART_04.tsv",
]

COMBINED_FIELDS = [
    "query_index",
    "query_text",
    "item_id",
    "region",
    "rank",
    "url",
    "domain",
    "normalized_domain",
    "title",
    "source_file",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="raise",
        )
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_domain(domain: str, url: str) -> str:
    host = (urlsplit(url).hostname or domain).strip().lower().rstrip(".")
    if host.startswith("www."):
        host = host[4:]
    return host


def reconstruct_combined() -> tuple[list[dict[str, object]], dict[str, object]]:
    combined: list[dict[str, object]] = []
    source_accounting: list[dict[str, object]] = []

    for source_index, path in enumerate(SOURCE_FILES):
        source_rows = read_tsv(path)
        indexes: set[int] = set()
        for raw in source_rows:
            query_index = 1 if source_index == 0 else int(raw["query_index"])
            query_text = raw["query"] if source_index == 0 else raw["query_text"]
            rank = int(raw["rank"])
            region = int(raw["region"])
            indexes.add(query_index)
            combined.append(
                {
                    "query_index": query_index,
                    "query_text": query_text,
                    "item_id": raw["item_id"],
                    "region": region,
                    "rank": rank,
                    "url": raw["url"],
                    "domain": raw["domain"],
                    "normalized_domain": normalize_domain(raw["domain"], raw["url"]),
                    "title": raw["title"],
                    "source_file": path.name,
                }
            )
        source_accounting.append(
            {
                "source_file": path.name,
                "data_rows": len(source_rows),
                "query_indexes": sorted(indexes),
                "query_count": len(indexes),
                "sha256": sha256(path),
            }
        )

    combined.sort(key=lambda row: (int(row["query_index"]), int(row["rank"])))
    query_rows: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in combined:
        query_rows[int(row["query_index"])].append(row)

    expected_indexes = list(range(1, 76))
    rank_coverage = {
        str(index): sorted(int(row["rank"]) for row in query_rows[index])
        for index in expected_indexes
    }
    identity_rows = [
        (row["query_index"], row["rank"], row["item_id"], row["url"])
        for row in combined
    ]
    duplicate_row_inflation = len(identity_rows) - len(set(identity_rows))
    source_row_total = sum(int(item["data_rows"]) for item in source_accounting)

    checks = {
        "source_queries_75": sorted(query_rows) == expected_indexes,
        "source_ranked_rows_750": source_row_total == 750,
        "accounted_queries_75": len(query_rows) == 75,
        "accounted_ranked_rows_750": len(combined) == 750,
        "silent_row_drops_0": source_row_total - len(combined) == 0,
        "duplicate_row_inflation_0": duplicate_row_inflation == 0,
        "region_213_only": {int(row["region"]) for row in combined} == {213},
        "ranks_1_to_10_per_query": all(
            rank_coverage[str(index)] == list(range(1, 11)) for index in expected_indexes
        ),
        "one_query_text_per_index": all(
            len({str(row["query_text"]) for row in query_rows[index]}) == 1
            for index in expected_indexes
        ),
        "required_fields_populated": all(
            all(str(row[field]).strip() for field in COMBINED_FIELDS)
            for row in combined
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"Combined-ledger QA failed: {failed}")

    qa = {
        "status": "PASS",
        "checks": checks,
        "source_accounting": source_accounting,
        "source_queries": len(query_rows),
        "source_ranked_rows": source_row_total,
        "accounted_queries": len(query_rows),
        "accounted_ranked_rows": len(combined),
        "silent_row_drops": source_row_total - len(combined),
        "duplicate_row_inflation": duplicate_row_inflation,
        "normalized_domains": len({str(row["normalized_domain"]) for row in combined}),
        "region": 213,
        "ranks_per_query": "1..10",
    }
    return combined, qa


def load_qa() -> dict[str, object]:
    if QA.exists():
        return json.loads(QA.read_text(encoding="utf-8"))
    return {
        "artifact": "OKNO_MSK_STEP_05A_FIRST_EXECUTION",
        "date": "2026-09-08",
        "starting_head": STARTING_HEAD,
        "status": "IN_PROGRESS",
        "project_test_validated": False,
        "owner_review": "PENDING",
        "provider_calls": {
            "yandex_search": 0,
            "wordstat": 0,
            "alice": 0,
            "gensearch": 0,
            "webmaster": 0,
            "metrika": 0,
            "direct": 0,
            "paid_cost_rub": 0,
        },
        "public_competitor_page_inspection_completed": False,
        "phase_status": {},
    }


def save_qa(payload: dict[str, object]) -> None:
    QA.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def phase_combined() -> None:
    combined, combined_qa = reconstruct_combined()
    write_tsv(COMBINED, COMBINED_FIELDS, combined)
    payload = load_qa()
    payload["phase_status"]["combined_serp_ledger"] = "PASS"
    payload["combined_serp_ledger"] = {
        **combined_qa,
        "path": COMBINED.name,
        "sha256": sha256(COMBINED),
        "size_bytes": COMBINED.stat().st_size,
    }
    save_qa(payload)
    print(
        json.dumps(
            {
                "phase": "combined",
                "status": "PASS",
                "queries": combined_qa["accounted_queries"],
                "rows": combined_qa["accounted_ranked_rows"],
                "normalized_domains": combined_qa["normalized_domains"],
                "output": str(COMBINED),
            },
            ensure_ascii=False,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["combined"], required=True)
    args = parser.parse_args()
    if args.phase == "combined":
        phase_combined()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
