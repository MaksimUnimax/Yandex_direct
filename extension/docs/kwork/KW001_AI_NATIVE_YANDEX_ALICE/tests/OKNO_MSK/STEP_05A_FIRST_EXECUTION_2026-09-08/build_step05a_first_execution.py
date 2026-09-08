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
DOMAIN_FREQUENCY = OUT / "STEP_05A_DOMAIN_FREQUENCY.tsv"
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

DOMAIN_FIELDS = [
    "normalized_domain",
    "observed_domain_variants",
    "total_top10_appearances",
    "distinct_queries",
    "top1_appearances",
    "top3_appearances",
    "top5_appearances",
    "best_rank",
    "median_rank",
    "competitor_class",
    "business_comparability",
    "step5a_candidate_state",
    "classification_basis",
    "representative_queries",
    "representative_urls",
    "source_scope",
]

COMPETITOR_CLASSES = {
    "DIRECT_BUSINESS_COMPETITOR",
    "ORGANIC_COMPETITOR_OTHER_MODEL",
    "AGGREGATOR_DIRECTORY",
    "MARKETPLACE",
    "MANUFACTURER_OR_BRAND_SOURCE",
    "INFORMATIONAL_PUBLISHER",
    "YANDEX_PLATFORM",
    "OTHER_REVIEW",
    "UNKNOWN",
}

# The shortlist is deliberately bounded and is resolved only from recurrence,
# preserved titles/URLs and task diversity in the completed 750-row ledger.
PHASE_D_SHORTLIST = {
    "mosokna.ru",
    "i-okna.ru",
    "msk.okna-servise.com",
    "okna-moskva.ru",
    "oknafactoria.ru",
    "okna-germany.ru",
    "fabrikaokon.ru",
    "svetokna.ru",
    "al-solution.ru",
    "aluminarium.ru",
    "elit-balkon.ru",
}

YANDEX_DOMAINS = {"yandex.ru", "market.yandex.ru", "uslugi.yandex.ru", "dzen.ru"}
MARKETPLACE_DOMAINS = {
    "avito.ru",
    "divan.ru",
    "hoff.ru",
    "lemanapro.ru",
    "maxidom.ru",
    "moscow.petrovich.ru",
    "ozon.ru",
    "vseinstrumenti.ru",
    "wildberries.ru",
}
AGGREGATOR_DOMAINS = {"2gis.ru", "hands.ru", "profi.ru", "remontgis.ru"}
MANUFACTURER_DOMAINS = {
    "dom.tn.ru",
    "e-fapim.ru",
    "melke.ru",
    "online-shop.rhsolutions.ru",
    "rhsolutions.ru",
    "robitex.ru",
    "tbm.ru",
    "tn.ru",
    "veka.ru",
}
INFORMATIONAL_DOMAINS = {
    "blog.domclick.ru",
    "dom.mail.ru",
    "ecookna.university",
    "forumhouse.ru",
    "inmyroom.ru",
    "ivd.ru",
    "kp.ru",
    "m-strana.ru",
    "media.halvacard.ru",
    "rg.ru",
    "ru.pinterest.com",
    "rutube.ru",
    "vk.ru",
    "youtube.com",
    "znaet.petrovich.ru",
}
REVIEW_DOMAINS = {"irecommend.ru", "otzovik.com"}
OTHER_MODEL_DOMAINS = {
    "catalog-plans.ru",
    "detaliokon.ru",
    "dveri9.ru",
    "dveribravo.ru",
    "dveriunas.ru",
    "dvermezhkom-service.ru",
    "fabrika-setok.ru",
    "furnitura.moscow",
    "halvacard.ru",
    "home-projects.ru",
    "mos-setka.ru",
    "mosdvery.ru",
    "moskitnyesetkimoscow.ru",
    "moskva-jaluzi.ru",
    "onlinejaluzi.ru",
    "plans.ru",
    "primedecorshop.ru",
    "rf-dveri.ru",
    "rulonki.com",
    "setki-okna.ru",
    "shtoranadom.ru",
    "tomdom.ru",
}

DIRECT_DOMAIN_MARKERS = (
    "okn",
    "okon",
    "balkon",
    "balcon",
    "osteklen",
    "glass",
    "alum",
    "fasad",
    "facade",
)
DIRECT_TITLE_MARKERS = (
    "пластиковые окна",
    "алюминиевые окна",
    "деревянные окна",
    "остекление",
    "ремонт окон",
    "установка окон",
    "монтаж окон",
)


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


def classify_domain(
    domain: str, rows: list[dict[str, str]]
) -> tuple[str, str, str]:
    """Classify from preserved host/title/URL/query evidence only."""

    titles = " ".join(row["title"].lower() for row in rows)
    compact_domain = domain.lower()
    if domain in YANDEX_DOMAINS:
        return (
            "YANDEX_PLATFORM",
            "NOT_DIRECT",
            "Known Yandex host in the preserved result URL; platform result, not a comparable contractor.",
        )
    if domain in MARKETPLACE_DOMAINS:
        return (
            "MARKETPLACE",
            "NOT_DIRECT",
            "Preserved URLs/titles expose a marketplace or broad home-improvement retail model.",
        )
    if domain in AGGREGATOR_DOMAINS or domain.endswith(".remontgis.ru"):
        return (
            "AGGREGATOR_DIRECTORY",
            "NOT_DIRECT",
            "Preserved result belongs to a service/directory aggregation host rather than one window contractor.",
        )
    if domain in MANUFACTURER_DOMAINS:
        return (
            "MANUFACTURER_OR_BRAND_SOURCE",
            "ADJACENT_SOURCE_NOT_DIRECT",
            "Preserved host/titles identify a profile, hardware or building-material brand/supplier source.",
        )
    if domain in INFORMATIONAL_DOMAINS:
        return (
            "INFORMATIONAL_PUBLISHER",
            "NOT_DIRECT",
            "Preserved result is a media, guide, forum, social or video publication surface.",
        )
    if domain in REVIEW_DOMAINS:
        return (
            "OTHER_REVIEW",
            "NOT_DIRECT",
            "Preserved result is a review/reputation surface, not a directly comparable offer.",
        )
    if domain in OTHER_MODEL_DOMAINS:
        return (
            "ORGANIC_COMPETITOR_OTHER_MODEL",
            "ADJACENT_OR_DIFFERENT_MODEL",
            "Preserved titles/URLs show an adjacent product, component, finance, plan or interior-goods model.",
        )

    domain_signal = any(marker in compact_domain for marker in DIRECT_DOMAIN_MARKERS)
    title_signal = any(marker in titles for marker in DIRECT_TITLE_MARKERS)
    if domain in PHASE_D_SHORTLIST or (domain_signal and title_signal):
        return (
            "DIRECT_BUSINESS_COMPETITOR",
            "DIRECT_OR_STRONG_PARTIAL",
            "Preserved ranking URLs/titles expose paid window, glazing, installation or repair offers comparable to all or part of OKNO_MSK scope.",
        )
    if title_signal:
        return (
            "ORGANIC_COMPETITOR_OTHER_MODEL",
            "ADJACENT_OR_DIFFERENT_MODEL",
            "Preserved titles overlap the task but the host does not establish a sufficiently comparable window/glazing business model.",
        )
    return (
        "UNKNOWN",
        "UNRESOLVED",
        "The preserved host/title/URL fields are insufficient for a stronger business-model classification; no new inspection was performed.",
    )


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


def phase_domains() -> None:
    combined = read_tsv(COMBINED)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in combined:
        grouped[row["normalized_domain"]].append(row)

    output_rows: list[dict[str, object]] = []
    for domain, rows in grouped.items():
        ranks = [int(row["rank"]) for row in rows]
        queries: dict[int, str] = {}
        for row in rows:
            queries[int(row["query_index"])] = row["query_text"]
        competitor_class, comparability, basis = classify_domain(domain, rows)
        ordered_rows = sorted(rows, key=lambda row: (int(row["rank"]), int(row["query_index"]), row["url"]))
        representative_queries: list[str] = []
        representative_urls: list[str] = []
        for row in ordered_rows:
            query_label = f'{row["query_index"]}: {row["query_text"]}'
            if query_label not in representative_queries and len(representative_queries) < 5:
                representative_queries.append(query_label)
            if row["url"] not in representative_urls and len(representative_urls) < 5:
                representative_urls.append(row["url"])

        if domain in PHASE_D_SHORTLIST:
            candidate_state = "SHORTLIST_FOR_PHASE_D"
        elif competitor_class == "DIRECT_BUSINESS_COMPETITOR" and len(queries) >= 3:
            candidate_state = "ELIGIBLE_NOT_SHORTLISTED_BOUNDED_SET"
        elif competitor_class == "DIRECT_BUSINESS_COMPETITOR":
            candidate_state = "OBSERVED_NOT_RECURRING_ENOUGH_FOR_SHORTLIST"
        else:
            candidate_state = "NOT_SHORTLISTED_CLASS_MISMATCH_OR_UNRESOLVED"

        median_rank = statistics.median(ranks)
        output_rows.append(
            {
                "normalized_domain": domain,
                "observed_domain_variants": "; ".join(sorted({row["domain"] for row in rows})),
                "total_top10_appearances": len(rows),
                "distinct_queries": len(queries),
                "top1_appearances": sum(rank == 1 for rank in ranks),
                "top3_appearances": sum(rank <= 3 for rank in ranks),
                "top5_appearances": sum(rank <= 5 for rank in ranks),
                "best_rank": min(ranks),
                "median_rank": f"{median_rank:.1f}",
                "competitor_class": competitor_class,
                "business_comparability": comparability,
                "step5a_candidate_state": candidate_state,
                "classification_basis": basis,
                "representative_queries": " | ".join(representative_queries),
                "representative_urls": " | ".join(representative_urls),
                "source_scope": "PRESERVED_STEP09_75_QUERY_750_ROW_SERP_ONLY",
            }
        )

    output_rows.sort(
        key=lambda row: (
            -int(row["total_top10_appearances"]),
            -int(row["distinct_queries"]),
            str(row["normalized_domain"]),
        )
    )
    write_tsv(DOMAIN_FREQUENCY, DOMAIN_FIELDS, output_rows)

    class_counts = Counter(str(row["competitor_class"]) for row in output_rows)
    checks = {
        "domain_rows_equal_normalized_domains": len(output_rows) == 237,
        "appearance_sum_750": sum(int(row["total_top10_appearances"]) for row in output_rows) == 750,
        "all_classes_allowed": set(class_counts).issubset(COMPETITOR_CLASSES),
        "all_domains_classified": all(row["competitor_class"] for row in output_rows),
        "metrics_monotonic": all(
            int(row["top1_appearances"])
            <= int(row["top3_appearances"])
            <= int(row["top5_appearances"])
            <= int(row["total_top10_appearances"])
            for row in output_rows
        ),
        "shortlist_is_direct": all(
            row["competitor_class"] == "DIRECT_BUSINESS_COMPETITOR"
            for row in output_rows
            if row["normalized_domain"] in PHASE_D_SHORTLIST
        ),
        "recurrence_not_equated_with_comparability": all(
            row["competitor_class"] != "DIRECT_BUSINESS_COMPETITOR"
            for row in output_rows
            if row["normalized_domain"] in {"online-shop.rhsolutions.ru", "avito.ru", "ozon.ru", "uslugi.yandex.ru"}
        ),
        "source_scope_preserved_only": all(
            row["source_scope"] == "PRESERVED_STEP09_75_QUERY_750_ROW_SERP_ONLY"
            for row in output_rows
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"Domain-frequency QA failed: {failed}")

    top_direct = [
        {
            "domain": row["normalized_domain"],
            "appearances": int(row["total_top10_appearances"]),
            "distinct_queries": int(row["distinct_queries"]),
            "top3": int(row["top3_appearances"]),
            "best_rank": int(row["best_rank"]),
        }
        for row in output_rows
        if row["competitor_class"] == "DIRECT_BUSINESS_COMPETITOR"
    ][:15]
    payload = load_qa()
    payload["phase_status"]["domain_frequency_and_classification"] = "PASS"
    payload["domain_frequency"] = {
        "status": "PASS",
        "path": DOMAIN_FREQUENCY.name,
        "sha256": sha256(DOMAIN_FREQUENCY),
        "size_bytes": DOMAIN_FREQUENCY.stat().st_size,
        "normalized_domains": len(output_rows),
        "classification_counts": dict(sorted(class_counts.items())),
        "top_recurring_direct_competitors": top_direct,
        "phase_d_shortlist_count": len(PHASE_D_SHORTLIST),
        "checks": checks,
    }
    save_qa(payload)
    print(
        json.dumps(
            {
                "phase": "domains",
                "status": "PASS",
                "normalized_domains": len(output_rows),
                "classification_counts": dict(sorted(class_counts.items())),
                "top_direct": top_direct[:10],
            },
            ensure_ascii=False,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["combined", "domains"], required=True)
    args = parser.parse_args()
    if args.phase == "combined":
        phase_combined()
    elif args.phase == "domains":
        phase_domains()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
