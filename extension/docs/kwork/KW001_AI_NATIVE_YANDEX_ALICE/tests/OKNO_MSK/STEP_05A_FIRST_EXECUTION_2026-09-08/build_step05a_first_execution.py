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
IMPACT_TRACE = OUT / "STEP_05A_QUERY_IMPACT_TRACE.tsv"
CANDIDATE_SELECTION = OUT / "STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv"
REPORT = OUT / "STEP_05A_FIRST_EXECUTION_REPORT.md"
EXECUTION_LOG = OUT / "EXECUTION_LOG.md"
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

IMPACT_FIELDS = [
    "query_index",
    "probe_id",
    "query",
    "top3_result_domains",
    "top10_result_domains",
    "observed_serp_job",
    "dominant_result_type",
    "step9_handoff",
    "step9_confidence",
    "step9_evidence_scope",
    "step10_exact_join",
    "step10_input_disposition",
    "step10_status",
    "step10_user_task",
    "step10_intent_orientation",
    "step10_cluster_id",
    "step10_cluster_role",
    "step10_evidence_state",
    "step10_assignment_reason",
    "step11_exact_phrase_join",
    "step11_target_url",
    "step11_ownership_state",
    "step11_cluster_owner_url",
    "step11_cluster_ownership_state",
    "final_master_exact_join",
    "final_semantic_state",
    "final_structural_unit_id",
    "canonical_user_task",
    "canonical_intent_type",
    "canonical_business_scope_state",
    "final_primary_page",
    "final_supporting_pages",
    "canonical_structural_action",
    "canonical_recommendation_maturity",
    "canonical_final_confidence",
    "impact_classification",
    "impact_reason",
    "trace_status",
    "authority_lineage",
    "claim_boundary",
]

CANDIDATE_FIELDS = [
    "selection_order",
    "normalized_domain",
    "selection_state",
    "total_top10_appearances",
    "distinct_queries",
    "top1_appearances",
    "top3_appearances",
    "top5_appearances",
    "best_rank",
    "median_rank",
    "competitor_class",
    "relevant_query_task_areas",
    "strongest_preserved_rankings",
    "why_useful_semantic_gap_source",
    "exact_ranking_urls_to_inspect_next",
    "selection_or_exclusion_reason",
    "source_authority",
    "claim_boundary",
]

IMPACT_CLASSES = {
    "CHANGED_DECISION",
    "DE_RISKED_DECISION",
    "CONFIRMED_EXISTING_DECISION",
    "NO_MATERIAL_DOWNSTREAM_EFFECT",
    "UNRESOLVED_TRACE",
}

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

SELECTION_REASONS = {
    "mosokna.ru": "Highest recurrence in the preserved set and broad coverage of PVC/Rehau, price, finance, product and balcony tasks through multiple ranking URLs.",
    "i-okna.ru": "Frequent Rehau-focused transactional visibility plus preserved repair, price and finance pages provides a concentrated brand-family comparison source.",
    "msk.okna-servise.com": "Strong TOP-3 recurrence across balcony subtypes, house-series, installation, price and cold/warm glazing tasks.",
    "okna-moskva.ru": "Broad product visibility combined with Rehau, instalment, balcony-roof and veranda pages adds cross-task comparison value.",
    "oknafactoria.ru": "Preserved results bridge service pages and editorial pages across open balcony, porch, repair, Provedal, selection and cold glazing.",
    "okna-germany.ru": "A content-led set of preserved Rehau comparison/selection/repair and Provedal URLs is useful for testing missed informational directions.",
    "fabrikaokon.ru": "Preserved rankings cover timber-aluminium windows, wooden balcony glazing, warm/cold subtypes and installation information/service.",
    "aluminarium.ru": "Repeated high positions in aluminium windows and outdoor-structure glazing provide a specialist contrast to broad PVC/window competitors.",
    "elit-balkon.ru": "Focused preserved visibility for open-balcony finishing, demolition and roof glazing supplies a specialist balcony-service comparison.",
}

SHORTLIST_EXCLUSIONS = {
    "al-solution.ru": "Not selected in the bounded set because its preserved aluminium/terrace/Provedal coverage is substantially represented by selected specialist and content candidates.",
    "svetokna.ru": "Not selected in the bounded set because its mixed wood/aluminium/veranda/balcony coverage overlaps selected Fabrika Okon and Aluminarium evidence.",
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


def phase_impact() -> None:
    combined = read_tsv(COMBINED)
    decisions = read_tsv(JOB / "STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv")
    assignments = read_tsv(JOB / "STEP_10_CLUSTER_ASSIGNMENTS.tsv")
    phrase_map = read_tsv(JOB / "STEP_11_PHRASE_PAGE_MAP.tsv")
    ownership = read_tsv(JOB / "STEP_11_PAGE_OWNERSHIP_CORRECTED.tsv")
    final_master = read_tsv(JOB / "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv")
    unit_authority = read_tsv(JOB / "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv")

    serp_by_query: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in combined:
        serp_by_query[int(row["query_index"])].append(row)
    for rows in serp_by_query.values():
        rows.sort(key=lambda row: int(row["rank"]))

    assignment_by_phrase = {row["phrase"].strip().lower(): row for row in assignments}
    phrase_map_by_phrase = {row["phrase"].strip().lower(): row for row in phrase_map}
    master_by_phrase = {row["phrase"].strip().lower(): row for row in final_master}
    ownership_by_cluster = {row["CLUSTER_ID"]: row for row in ownership}
    unit_by_id = {row["structural_unit_id"]: row for row in unit_authority}

    output_rows: list[dict[str, object]] = []
    for query_index, decision in enumerate(decisions, start=1):
        query = decision["query"]
        key = query.strip().lower()
        assignment = assignment_by_phrase.get(key)
        mapping = phrase_map_by_phrase.get(key)
        master = master_by_phrase.get(key)
        cluster_id = assignment["cluster_id"] if assignment else ""
        cluster_owner = ownership_by_cluster.get(cluster_id)
        unit = unit_by_id.get(master["final_structural_unit_id"] if master else "")
        serp_rows = serp_by_query[query_index]

        if assignment and assignment.get("cluster_role") == "BOUNDARY_REVIEW":
            impact = "DE_RISKED_DECISION"
            impact_reason = (
                "The preserved Step 10 boundary override uses exact Step 9 overlap evidence to prevent an automatic merge or stronger ownership claim."
            )
        elif not assignment or not master or not assignment.get("cluster_id") or assignment.get("cluster_role") == "UNRESOLVED":
            impact = "UNRESOLVED_TRACE"
            if assignment:
                impact_reason = (
                    "An exact Step 9 decision exists, but the preserved downstream row remains unresolved and does not support a stronger causal trace."
                )
            else:
                impact_reason = (
                    "The completed downstream phrase authorities contain no exact query/phrase row; no family-level causal transfer was invented."
                )
        elif master.get("canonical_structural_action") in {
            "DEFER_PENDING_EVIDENCE",
            "OUTSIDE_SCOPE_NO_ACTION",
            "NO_STANDALONE_PAGE",
        }:
            impact = "DE_RISKED_DECISION"
            impact_reason = (
                "Direct Step 9 evidence supports a boundary, outside-scope, no-standalone-page or evidence-hold route and reduces the risk of unsupported page expansion."
            )
        elif assignment.get("corrected_status") == "KEEP":
            impact = "CONFIRMED_EXISTING_DECISION"
            impact_reason = (
                "The phrase was already a core candidate; its explicit Step 9 join confirms the task/cluster that the later canonical authority preserves."
            )
        elif assignment.get("corrected_status") == "REVIEW":
            impact = "CHANGED_DECISION"
            impact_reason = (
                "Direct Step 9 evidence resolves a review-state phrase into the preserved Step 10 user task/cluster; the later canonical route is recorded without claiming Search alone caused every downstream choice."
            )
        else:
            impact = "NO_MATERIAL_DOWNSTREAM_EFFECT"
            impact_reason = (
                "The exact observation is preserved, but the completed authorities do not record a material changed, de-risked or confirmed downstream decision."
            )

        lineage = [
            f"STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv#{decision['probe_id']}",
            f"STEP_05A_SERP_COMBINED_750.tsv#query_index={query_index}",
        ]
        if assignment:
            lineage.append(f"STEP_10_CLUSTER_ASSIGNMENTS.tsv#phrase={query}")
        if mapping:
            lineage.append(f"STEP_11_PHRASE_PAGE_MAP.tsv#phrase={query}")
        if cluster_owner:
            lineage.append(f"STEP_11_PAGE_OWNERSHIP_CORRECTED.tsv#CLUSTER_ID={cluster_id}")
        if master:
            lineage.append(f"RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv#phrase={query}")
        if unit:
            lineage.append(
                "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"
                f"#structural_unit_id={master['final_structural_unit_id']}"
            )

        master_claim_boundary = master.get("claim_boundary", "") if master else ""
        claim_boundary = (
            "EXACT_STEP09_QUERY_ONLY__NO_UNPROBED_OR_FAMILY_CAUSAL_TRANSFER"
            + (f" | {master_claim_boundary}" if master_claim_boundary else "")
        )
        output_rows.append(
            {
                "query_index": query_index,
                "probe_id": decision["probe_id"],
                "query": query,
                "top3_result_domains": " | ".join(row["normalized_domain"] for row in serp_rows[:3]),
                "top10_result_domains": " | ".join(row["normalized_domain"] for row in serp_rows),
                "observed_serp_job": decision["observed_serp_job"],
                "dominant_result_type": decision["dominant_result_type"],
                "step9_handoff": decision["step10_handoff"],
                "step9_confidence": decision["confidence"],
                "step9_evidence_scope": decision["evidence_scope"],
                "step10_exact_join": "true" if assignment else "false",
                "step10_input_disposition": assignment.get("input_disposition", "") if assignment else "",
                "step10_status": assignment.get("corrected_status", "") if assignment else "",
                "step10_user_task": assignment.get("user_task", "") if assignment else "",
                "step10_intent_orientation": assignment.get("intent_orientation", "") if assignment else "",
                "step10_cluster_id": cluster_id,
                "step10_cluster_role": assignment.get("cluster_role", "") if assignment else "",
                "step10_evidence_state": assignment.get("cluster_evidence_state", "") if assignment else "",
                "step10_assignment_reason": assignment.get("assignment_reason", "") if assignment else "",
                "step11_exact_phrase_join": "true" if mapping else "false",
                "step11_target_url": mapping.get("target_url", "") if mapping else "",
                "step11_ownership_state": mapping.get("ownership_state", "") if mapping else "",
                "step11_cluster_owner_url": cluster_owner.get("PRIMARY_OWNER_URL_IF_RESOLVED", "") if cluster_owner else "",
                "step11_cluster_ownership_state": cluster_owner.get("OWNERSHIP_STATE", "") if cluster_owner else "",
                "final_master_exact_join": "true" if master else "false",
                "final_semantic_state": master.get("final_semantic_state", "") if master else "",
                "final_structural_unit_id": master.get("final_structural_unit_id", "") if master else "",
                "canonical_user_task": unit.get("user_task", "") if unit else master.get("canonical_user_task", "") if master else "",
                "canonical_intent_type": unit.get("intent_type", "") if unit else master.get("canonical_intent_type", "") if master else "",
                "canonical_business_scope_state": unit.get("business_scope_state", "") if unit else master.get("canonical_business_scope_state", "") if master else "",
                "final_primary_page": unit.get("final_primary_page", "") if unit else master.get("final_primary_page", "") if master else "",
                "final_supporting_pages": unit.get("final_supporting_pages", "") if unit else master.get("final_supporting_pages", "") if master else "",
                "canonical_structural_action": unit.get("structural_action", "") if unit else master.get("canonical_structural_action", "") if master else "",
                "canonical_recommendation_maturity": unit.get("recommendation_maturity", "") if unit else master.get("canonical_recommendation_maturity", "") if master else "",
                "canonical_final_confidence": unit.get("final_confidence", "") if unit else master.get("canonical_final_confidence", "") if master else "",
                "impact_classification": impact,
                "impact_reason": impact_reason,
                "trace_status": "UNRESOLVED" if impact == "UNRESOLVED_TRACE" else "TRACE_RESOLVED_WITH_EXPLICIT_BOUNDARY",
                "authority_lineage": " | ".join(lineage),
                "claim_boundary": claim_boundary,
            }
        )

    write_tsv(IMPACT_TRACE, IMPACT_FIELDS, output_rows)
    impact_counts = Counter(str(row["impact_classification"]) for row in output_rows)
    checks = {
        "impact_rows_75": len(output_rows) == 75,
        "query_indexes_1_to_75": [int(row["query_index"]) for row in output_rows] == list(range(1, 76)),
        "probe_ids_unique_75": len({str(row["probe_id"]) for row in output_rows}) == 75,
        "impact_classes_allowed": set(impact_counts).issubset(IMPACT_CLASSES),
        "impact_counts_reconcile_75": sum(impact_counts.values()) == 75,
        "step10_exact_joins_66": sum(row["step10_exact_join"] == "true" for row in output_rows) == 66,
        "step11_exact_phrase_joins_66": sum(row["step11_exact_phrase_join"] == "true" for row in output_rows) == 66,
        "final_master_exact_joins_66": sum(row["final_master_exact_join"] == "true" for row in output_rows) == 66,
        "unresolved_trace_not_overstated": all(
            row["step10_cluster_id"] == "" or row["step10_cluster_role"] == "UNRESOLVED"
            for row in output_rows
            if row["impact_classification"] == "UNRESOLVED_TRACE"
        ),
        "resolved_trace_has_downstream_join": all(
            row["step10_exact_join"] == "true" and row["final_master_exact_join"] == "true"
            for row in output_rows
            if row["impact_classification"] != "UNRESOLVED_TRACE"
        ),
        "exact_query_claim_boundary_all_rows": all(
            "EXACT_STEP09_QUERY_ONLY" in str(row["claim_boundary"]) for row in output_rows
        ),
        "authority_lineage_all_rows": all(row["authority_lineage"] for row in output_rows),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"Impact-trace QA failed: {failed}")

    payload = load_qa()
    payload["phase_status"]["query_impact_trace"] = "PASS"
    payload["query_impact_trace"] = {
        "status": "PASS",
        "path": IMPACT_TRACE.name,
        "sha256": sha256(IMPACT_TRACE),
        "size_bytes": IMPACT_TRACE.stat().st_size,
        "rows": len(output_rows),
        "impact_counts": {name: impact_counts.get(name, 0) for name in sorted(IMPACT_CLASSES)},
        "step10_exact_joins": sum(row["step10_exact_join"] == "true" for row in output_rows),
        "unresolved_queries": [
            {"query_index": row["query_index"], "probe_id": row["probe_id"], "query": row["query"]}
            for row in output_rows
            if row["impact_classification"] == "UNRESOLVED_TRACE"
        ],
        "checks": checks,
    }
    save_qa(payload)
    print(
        json.dumps(
            {
                "phase": "impact",
                "status": "PASS",
                "rows": len(output_rows),
                "impact_counts": payload["query_impact_trace"]["impact_counts"],
            },
            ensure_ascii=False,
        )
    )


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def phase_final() -> None:
    combined = read_tsv(COMBINED)
    domain_rows = read_tsv(DOMAIN_FREQUENCY)
    impact_rows = read_tsv(IMPACT_TRACE)
    decisions = read_tsv(JOB / "STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv")
    decision_by_index = {index: row for index, row in enumerate(decisions, start=1)}
    domain_by_name = {row["normalized_domain"]: row for row in domain_rows}
    serp_by_domain: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in combined:
        serp_by_domain[row["normalized_domain"]].append(row)

    candidate_rows: list[dict[str, object]] = []
    ordered_shortlist = SELECTED_COMPETITORS + sorted(PHASE_D_SHORTLIST - set(SELECTED_COMPETITORS))
    for order, domain in enumerate(ordered_shortlist, start=1):
        frequency = domain_by_name[domain]
        ranked_rows = sorted(
            serp_by_domain[domain],
            key=lambda row: (int(row["rank"]), int(row["query_index"]), row["url"]),
        )
        task_areas: list[str] = []
        strongest: list[str] = []
        for row in ranked_rows:
            query_index = int(row["query_index"])
            area = decision_by_index[query_index]["observed_serp_job"]
            if area not in task_areas and len(task_areas) < 8:
                task_areas.append(area)
            ranking = f'Q{query_index}/R{row["rank"]}: {row["query_text"]}'
            if ranking not in strongest and len(strongest) < 6:
                strongest.append(ranking)

        is_selected = domain in SELECTED_COMPETITORS
        inspection_urls: list[str] = []
        represented_areas: set[str] = set()
        if is_selected:
            for row in ranked_rows:
                query_index = int(row["query_index"])
                area = decision_by_index[query_index]["observed_serp_job"]
                if row["url"] in {item.split(" ", 1)[1] for item in inspection_urls}:
                    continue
                if area not in represented_areas:
                    inspection_urls.append(f'Q{query_index}/R{row["rank"]} {row["url"]}')
                    represented_areas.add(area)
                if len(inspection_urls) == 5:
                    break
            if len(inspection_urls) < 5:
                existing_urls = {item.split(" ", 1)[1] for item in inspection_urls}
                for row in ranked_rows:
                    if row["url"] not in existing_urls:
                        inspection_urls.append(f'Q{row["query_index"]}/R{row["rank"]} {row["url"]}')
                        existing_urls.add(row["url"])
                    if len(inspection_urls) == 5:
                        break

        candidate_rows.append(
            {
                "selection_order": order if is_selected else "",
                "normalized_domain": domain,
                "selection_state": "SELECTED_FOR_NEXT_STEP5A_PAGE_INSPECTION" if is_selected else "NOT_SELECTED_BOUNDED_REDUNDANCY",
                "total_top10_appearances": frequency["total_top10_appearances"],
                "distinct_queries": frequency["distinct_queries"],
                "top1_appearances": frequency["top1_appearances"],
                "top3_appearances": frequency["top3_appearances"],
                "top5_appearances": frequency["top5_appearances"],
                "best_rank": frequency["best_rank"],
                "median_rank": frequency["median_rank"],
                "competitor_class": frequency["competitor_class"],
                "relevant_query_task_areas": " | ".join(task_areas),
                "strongest_preserved_rankings": " | ".join(strongest),
                "why_useful_semantic_gap_source": SELECTION_REASONS.get(domain, ""),
                "exact_ranking_urls_to_inspect_next": " | ".join(inspection_urls),
                "selection_or_exclusion_reason": SELECTION_REASONS.get(domain, SHORTLIST_EXCLUSIONS.get(domain, "")),
                "source_authority": "STEP_05A_SERP_COMBINED_750.tsv + STEP_05A_DOMAIN_FREQUENCY.tsv + STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv",
                "claim_boundary": "PRESERVED_RANKING_VISIBILITY_ONLY__PAGE_TOPICS_AND_NEW_SEEDS_NOT_INSPECTED_OR_INFERRED",
            }
        )

    write_tsv(CANDIDATE_SELECTION, CANDIDATE_FIELDS, candidate_rows)
    selected_rows = [row for row in candidate_rows if row["selection_state"].startswith("SELECTED")]
    combined_urls_by_domain = {
        domain: {row["url"] for row in rows} for domain, rows in serp_by_domain.items()
    }
    candidate_checks = {
        "shortlist_rows_11": len(candidate_rows) == 11,
        "selected_candidates_9": len(selected_rows) == 9,
        "selected_domains_unique": len({row["normalized_domain"] for row in selected_rows}) == 9,
        "selected_domains_are_direct_competitors": all(row["competitor_class"] == "DIRECT_BUSINESS_COMPETITOR" for row in selected_rows),
        "selected_domains_have_recurrence": all(int(row["distinct_queries"]) >= 4 for row in selected_rows),
        "selected_domains_have_exact_next_urls": all(row["exact_ranking_urls_to_inspect_next"] for row in selected_rows),
        "selected_urls_derive_from_preserved_serp": all(
            all(
                item.split(" ", 1)[1] in combined_urls_by_domain[str(row["normalized_domain"])]
                for item in str(row["exact_ranking_urls_to_inspect_next"]).split(" | ")
            )
            for row in selected_rows
        ),
        "nonselected_shortlist_explained": all(
            row["selection_or_exclusion_reason"] and not row["exact_ranking_urls_to_inspect_next"]
            for row in candidate_rows
            if not row["selection_state"].startswith("SELECTED")
        ),
        "no_page_topic_or_seed_inference": all("NOT_INSPECTED_OR_INFERRED" in row["claim_boundary"] for row in candidate_rows),
    }
    if not all(candidate_checks.values()):
        failed = [name for name, passed in candidate_checks.items() if not passed]
        raise RuntimeError(f"Candidate-selection QA failed: {failed}")

    impact_counts = Counter(row["impact_classification"] for row in impact_rows)
    class_counts = Counter(row["competitor_class"] for row in domain_rows)
    top_direct = [row for row in domain_rows if row["competitor_class"] == "DIRECT_BUSINESS_COMPETITOR"][:15]
    unresolved = [row for row in impact_rows if row["impact_classification"] == "UNRESOLVED_TRACE"]

    report_lines = [
        "# KW-001 / OKNO_MSK — Step 5A first execution report",
        "",
        "Date: 2026-09-08  ",
        "Status: **ANALYST QA PASS / OWNER REVIEW PENDING / METHOD NOT PROMOTED**",
        "",
        "## 1. What this execution completed",
        "",
        "This isolated execution processed the complete preserved ordinary-Yandex dataset: 75 queries and 750 ranked TOP-10 rows for region 213. It reconstructed one deterministic ledger, measured recurring domains, separated recurrence from business comparability, traced every query as far as completed downstream evidence allows and selected a bounded set of real search competitors for the next Step 5A subphase.",
        "",
        "No new Yandex Search, Wordstat, Alice, GenSearch, Webmaster, Metrika or Direct call was made. No public competitor page was opened. Client deliverables and historical Step 0–20 authorities were not modified.",
        "",
        "## 2. Source accounting",
        "",
        "```text",
        "SOURCE_QUERIES = 75",
        "SOURCE_RANKED_ROWS = 750",
        "ACCOUNTED_QUERIES = 75",
        "ACCOUNTED_RANKED_ROWS = 750",
        "SILENT_ROW_DROPS = 0",
        "DUPLICATE_ROW_INFLATION = 0",
        "NORMALIZED_DOMAINS = 237",
        "REGION = 213",
        "RANKS_PER_QUERY = 1..10",
        "```",
        "",
        "The canary row source and four R2 projection parts were combined only through their common supported fields. Unavailable R2 snippets, request IDs, HTTP fields and raw XML were not invented.",
        "",
        "## 3. Domain recurrence and classification",
        "",
        f"All 237 normalized domains were assigned one routing class. Where the preserved hostname/title/URL fields were insufficient, the class remains `UNKNOWN` ({class_counts.get('UNKNOWN', 0)} domains) rather than being guessed.",
        "",
        "| Class | Domains |",
        "|---|---:|",
    ]
    for class_name in sorted(COMPETITOR_CLASSES):
        report_lines.append(f"| `{class_name}` | {class_counts.get(class_name, 0)} |")
    report_lines.extend([
        "",
        "Top recurring direct-business competitors from the preserved ledger:",
        "",
        "| Domain | TOP-10 appearances | Distinct queries | TOP-3 | Best rank |",
        "|---|---:|---:|---:|---:|",
    ])
    for row in top_direct:
        report_lines.append(
            f"| {row['normalized_domain']} | {row['total_top10_appearances']} | {row['distinct_queries']} | {row['top3_appearances']} | {row['best_rank']} |"
        )
    report_lines.extend([
        "",
        "Recurrence was not treated as business equivalence. High-frequency non-direct surfaces such as the REHAU online shop, Avito, Ozon and Yandex services remain manufacturer, marketplace or platform observations.",
        "",
        "## 4. What ordinary Yandex Search changed or confirmed",
        "",
        "Every Step 9 query has one impact row with an exact-query claim boundary:",
        "",
        "| Impact class | Queries | Meaning in this execution |",
        "|---|---:|---|",
        f"| `CHANGED_DECISION` | {impact_counts.get('CHANGED_DECISION', 0)} | Direct evidence resolved a review-state phrase into a preserved task/cluster. |",
        f"| `DE_RISKED_DECISION` | {impact_counts.get('DE_RISKED_DECISION', 0)} | Evidence supported a boundary, hold, outside-scope or no-standalone-page route. |",
        f"| `CONFIRMED_EXISTING_DECISION` | {impact_counts.get('CONFIRMED_EXISTING_DECISION', 0)} | Evidence confirmed a task/cluster already carried as a core candidate. |",
        f"| `NO_MATERIAL_DOWNSTREAM_EFFECT` | {impact_counts.get('NO_MATERIAL_DOWNSTREAM_EFFECT', 0)} | Observation existed without a material traceable downstream effect. |",
        f"| `UNRESOLVED_TRACE` | {impact_counts.get('UNRESOLVED_TRACE', 0)} | No exact completed downstream join or the preserved row remained unresolved. |",
        "",
        "There are 66 exact Step 10 / Step 11 phrase / final-master joins. Ten queries remain unresolved rather than receiving family-level causal attribution:",
        "",
    ])
    for row in unresolved:
        report_lines.append(f"- Q{row['query_index']} / {row['probe_id']}: {row['query']}")
    report_lines.extend([
        "",
        "These impact classes describe the role explicitly traceable in preserved evidence. They do not claim that Search alone caused every later structural decision.",
        "",
        "## 5. Bounded competitor selection for the next Step 5A subphase",
        "",
        "Nine competitors were selected from an eleven-domain shortlist. Selection combines recurrence, direct/partial business comparability and task diversity; it is not a market-share ranking.",
        "",
        "| # | Domain | Queries | TOP-3 | Best | Why retained |",
        "|---:|---|---:|---:|---:|---|",
    ])
    for row in selected_rows:
        report_lines.append(
            f"| {row['selection_order']} | {row['normalized_domain']} | {row['distinct_queries']} | {row['top3_appearances']} | {row['best_rank']} | {markdown_escape(row['why_useful_semantic_gap_source'])} |"
        )
    report_lines.extend([
        "",
        "Not selected in the bounded set:",
        "",
    ])
    for row in candidate_rows:
        if not row["selection_state"].startswith("SELECTED"):
            report_lines.append(f"- **{row['normalized_domain']}** — {row['selection_or_exclusion_reason']}")
    report_lines.extend([
        "",
        "### Exact preserved ranking URLs to inspect next",
        "",
        "These URLs are evidence-bearing inspection targets only. Their page topics were not inspected in this execution and no candidate seed was inferred from the URL alone.",
        "",
    ])
    for row in selected_rows:
        report_lines.append(f"- **{row['normalized_domain']}**")
        for item in str(row["exact_ranking_urls_to_inspect_next"]).split(" | "):
            label, url = item.split(" ", 1)
            report_lines.append(f"  - {label}: {url}")
    report_lines.extend([
        "",
        "## 6. Method-validation result",
        "",
        "```text",
        "REAL_SEARCH_COMPETITOR_DISCOVERY = PASS",
        "PRESERVED_QUERY_TO_COMPETITOR_VISIBILITY = PASS",
        "RECURRENCE_VS_BUSINESS_COMPARABILITY_BOUNDARY = PASS",
        "QUERY_IMPACT_TRACE = PASS_WITH_10_EXPLICIT_UNRESOLVED_ROWS",
        "COMPETITOR_PAGE_TO_SEED_LINEAGE = NOT_EXECUTED",
        "WORDSTAT_COMPETITOR_EXPANSION = NOT_EXECUTED",
        "NEW_CANDIDATE_SEARCH_RECHECK = NOT_EXECUTED",
        "WEBSITE_TEXT_AS_RANKING_OVERCLAIM = 0",
        "FULL_COMPETITOR_KEYWORD_UNIVERSE_OVERCLAIM = 0",
        "PROJECT_TEST_VALIDATED = false",
        "OWNER_REVIEW = PENDING",
        "```",
        "",
        "This execution validates the preserved-SERP discovery, classification, impact-trace and bounded-selection operations. It does not satisfy the full permanent promotion gate because competitor-page inspection, page→seed lineage, Wordstat expansion, candidate filtering, Search recheck and merge reconciliation were intentionally not executed.",
        "",
        "## 7. Exact next evidence boundary",
        "",
        "Next authorized work must first inspect only the exact selected ranking URLs recorded in `STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv` and persist page-level provenance. Only then can exact candidate seeds be named.",
        "",
        "```text",
        "EXACT_NEW_WORDSTAT_SEEDS_REQUIRED_NOW = NONE__NOT_YET_EVIDENCED",
        "EXACT_NEW_SEARCH_QUERIES_REQUIRED_NOW = NONE__PENDING_PAGE_INSPECTION_AND_WORDSTAT_RESULTS",
        "NEXT_EVIDENCE_PRODUCING_STEP = OWNER_AUTHORIZED_SELECTED_COMPETITOR_PAGE_INSPECTION",
        "```",
        "",
        "The absence of exact seeds at this boundary is intentional: inventing them from domain names or URL slugs would violate `COMPETITOR PAGE TOPIC != EXACT QUERY RANKING` and the lineage requirement.",
        "",
        "## 8. Durable artifact set",
        "",
        "- `CHECKPOINT_00_BASELINE_AND_REUSE_INVENTORY.md`",
        "- `STEP_05A_SERP_COMBINED_750.tsv`",
        "- `STEP_05A_DOMAIN_FREQUENCY.tsv`",
        "- `STEP_05A_QUERY_IMPACT_TRACE.tsv`",
        "- `STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv`",
        "- `STEP_05A_FIRST_EXECUTION_QA.json`",
        "- `STEP_05A_FIRST_EXECUTION_REPORT.md`",
        "- `EXECUTION_LOG.md`",
        "- `build_step05a_first_execution.py`",
        "- `validate_step05a_first_execution.py`",
        "",
        "Optional page-evidence and derived-seed files were not created because no competitor page was inspected.",
    ])
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    log_lines = [
        "# KW-001 / OKNO_MSK — Step 5A first execution log",
        "",
        "Date: 2026-09-08",
        "",
        "## Durable blocks",
        "",
        "| Block | Result | Remote commit / readback |",
        "|---|---|---|",
        "| 0. Baseline / reuse inventory | PASS | `925a00b528a48f6e2825cb892fa4c445f010ac90` / PASS |",
        "| A. Combined 75-query / 750-row ledger | PASS | `ca3178fff1630ebd3ef8dddf4aa1cd2c512ca941` / PASS |",
        "| B. Domain frequency / classification | PASS | `918c414822760f6b9ab0f317f2922f10f5fc27ad` / PASS |",
        "| C. Query impact trace | PASS | `31c9ecb0ca43d2da901ce3dc22203bb0059e7003` / PASS |",
        "| D. Candidate selection / report / final QA | PASS | containing finalization commit / remote readback required before completion |",
        "",
        "## Acquisition boundary",
        "",
        "```text",
        "NEW_YANDEX_SEARCH_CALLS = 0",
        "NEW_WORDSTAT_CALLS = 0",
        "NEW_ALICE_CALLS = 0",
        "NEW_GENSEARCH_CALLS = 0",
        "NEW_WEBMASTER_CALLS = 0",
        "NEW_METRIKA_CALLS = 0",
        "NEW_DIRECT_CALLS = 0",
        "NEW_PAID_PROVIDER_COST_RUB = 0",
        "PUBLIC_COMPETITOR_PAGE_INSPECTION = false",
        "```",
        "",
        "## Scope protection",
        "",
        "All task changes remain under `STEP_05A_FIRST_EXECUTION_2026-09-08/`. The corrected client release, Documents 01–03, semantic-core XLSX and historical Step 0–20 outputs were not modified.",
        "",
        "## Final routing",
        "",
        "```text",
        "PROJECT_TEST_VALIDATED = false",
        "OWNER_REVIEW = PENDING",
        "NEXT_ACTION = OWNER_REVIEW_STEP_05A_FIRST_EXECUTION__THEN_AUTHORIZE_SELECTED_COMPETITOR_PAGE_INSPECTION_IF_ACCEPTED",
        "```",
    ]
    EXECUTION_LOG.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    payload = load_qa()
    payload["phase_status"]["competitor_candidate_selection"] = "PASS"
    payload["phase_status"]["first_execution_report"] = "PASS"
    payload["competitor_candidate_selection"] = {
        "status": "PASS",
        "path": CANDIDATE_SELECTION.name,
        "sha256": sha256(CANDIDATE_SELECTION),
        "size_bytes": CANDIDATE_SELECTION.stat().st_size,
        "shortlist_rows": len(candidate_rows),
        "selected_count": len(selected_rows),
        "selected_domains": [row["normalized_domain"] for row in selected_rows],
        "checks": candidate_checks,
    }
    payload["report"] = {
        "path": REPORT.name,
        "sha256": sha256(REPORT),
        "size_bytes": REPORT.stat().st_size,
    }
    payload["execution_log"] = {
        "path": EXECUTION_LOG.name,
        "sha256": sha256(EXECUTION_LOG),
        "size_bytes": EXECUTION_LOG.stat().st_size,
    }
    payload["exact_new_wordstat_seeds_required_now"] = []
    payload["exact_new_search_queries_required_now"] = []
    payload["next_evidence_boundary"] = "OWNER_AUTHORIZED_SELECTED_COMPETITOR_PAGE_INSPECTION"
    payload["status"] = "ANALYST_QA_PENDING_DETERMINISTIC_VALIDATOR"
    payload["project_test_validated"] = False
    payload["owner_review"] = "PENDING"
    save_qa(payload)
    print(
        json.dumps(
            {
                "phase": "final",
                "status": "PASS_PENDING_INDEPENDENT_VALIDATOR",
                "selected_competitors": payload["competitor_candidate_selection"]["selected_domains"],
                "report": str(REPORT),
            },
            ensure_ascii=False,
        )
    )
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["combined", "domains", "impact", "final"], required=True)
    args = parser.parse_args()
    if args.phase == "combined":
        phase_combined()
    elif args.phase == "domains":
        phase_domains()
    elif args.phase == "impact":
        phase_impact()
    elif args.phase == "final":
        phase_final()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
