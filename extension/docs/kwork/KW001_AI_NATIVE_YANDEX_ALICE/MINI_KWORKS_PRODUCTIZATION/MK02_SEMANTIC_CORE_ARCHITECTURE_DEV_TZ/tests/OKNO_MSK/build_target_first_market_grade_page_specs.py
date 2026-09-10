#!/usr/bin/env python3
from __future__ import annotations

import csv
import gzip
import io
import re
from collections import defaultdict
from pathlib import Path

DATE = "2026-09-10"
ROOT = Path(__file__).resolve().parent


def read_tsv(path: Path, gz: bool = False):
    opener = gzip.open if gz else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_gzip_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            with io.TextIOWrapper(gz, encoding="utf-8", newline="") as text:
                writer = csv.DictWriter(text, fieldnames=fields, delimiter="\t", lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def norm_tokens(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-zа-яё0-9]+", (text or "").casefold()) if len(token) > 1]


def too_similar(left: str, right: str) -> bool:
    a, b = set(norm_tokens(left)), set(norm_tokens(right))
    return bool(a and b) and len(a & b) / len(a | b) >= 0.84


def type_family(page_type: str) -> str:
    text = (page_type or "").casefold()
    if "коммерчес" in text:
        return "COMMERCIAL"
    if "информацион" in text:
        return "INFORMATIONAL"
    if "портфолио" in text:
        return "PORTFOLIO"
    if "интерактив" in text:
        return "TOOL"
    if "смешан" in text or "хаб" in text:
        return "MIXED"
    return "OTHER"


def h1_for(page_name: str, action: str) -> str:
    if action == "RECHECK_NEEDS_EVIDENCE":
        return "Не назначать H1 до уточнения поисковой задачи"
    return page_name.removeprefix("Главная: ").strip()


def title_direction(page_name: str, page_type: str, primary_query: str, action: str) -> str:
    if action == "RECHECK_NEEDS_EVIDENCE":
        return "Не назначать Title до уточнения поисковой задачи."
    if action != "OPTIMIZE_STRENGTHEN":
        return "Отдельное изменение Title не требуется в рамках текущего решения."
    if "Информационная" in page_type:
        return (
            f"Направление Title: «{page_name}» + конкретный вопрос/критерий выбора; "
            f"основной фокус — «{primary_query}». Не добавлять неподтверждённые коммерческие обещания."
        )
    if "Портфолио" in page_type:
        return (
            f"Направление Title: «{page_name}» + примеры работ в Москве; основной фокус — «{primary_query}». "
            "Не перечислять неподтверждённые категории."
        )
    return (
        f"Направление Title: «{primary_query}» + подтверждённый коммерческий смысл страницы + Москва. "
        "Не добавлять цены, сроки или условия, которых нет в подтверждённом содержании."
    )


def priority_for(page_key: str, action: str, count: int, reg_by_key: dict, hier_by_key: dict) -> tuple[str, str]:
    hierarchy = hier_by_key.get(page_key, {})
    has_children = bool((reg_by_key[page_key].get("child_supporting_target_page_keys") or "").strip())
    is_section = hierarchy.get("hierarchy_level") == "SECTION_LANDING_OR_STANDALONE"
    if action == "RECHECK_NEEDS_EVIDENCE":
        return "Высокий", "Неразрешённая роль блокирует окончательную рассадку; это важность аналитической проверки, а не порядок разработки."
    if action in {"OPTIMIZE_STRENGTHEN", "ROUTE_INTERNAL_LINK_CHANGE"} and count >= 20:
        return "Высокий", f"Есть подтверждённое изменение и заметный объём спроса ({count} рабочих фраз); это SEO-приоритет, не календарный порядок."
    if count >= 100 or (is_section and count >= 40):
        return "Высокий", f"Крупная или центральная роль целевой структуры: {count} рабочих фраз."
    if action in {"OPTIMIZE_STRENGTHEN", "ROUTE_INTERNAL_LINK_CHANGE"}:
        return "Средний", "Есть подтверждённое изменение, но объём/центральность ниже крупнейших ролей; приоритет не является сроком внедрения."
    if count >= 20 or is_section or has_children:
        return "Средний", f"Заметная семантическая или структурная роль: {count} рабочих фраз."
    return "Низкий", f"Узкая подтверждённая роль: {count} рабочих фраз. Это не оценка бизнес-ценности."


def main() -> None:
    foundation = read_tsv(ROOT / f"MK02_SEMANTIC_FOUNDATION_{DATE}.tsv.gz", True)
    phrase_map = read_tsv(ROOT / f"TARGET_FIRST_PHRASE_LANDING_MAP_{DATE}.tsv.gz", True)
    clusters = read_tsv(ROOT / f"TARGET_FIRST_CLUSTER_LANDING_MAP_{DATE}.tsv")
    registry = read_tsv(ROOT / f"TARGET_PAGE_REGISTRY_{DATE}.tsv")
    hierarchy = read_tsv(ROOT / f"TARGET_ARCHITECTURE_HIERARCHY_{DATE}.tsv")
    reconciliation = read_tsv(ROOT / f"CURRENT_TARGET_RECONCILIATION_{DATE}.tsv")
    old_specs = read_tsv(ROOT / f"TARGET_PAGE_SPEC_REGISTER_{DATE}.tsv")

    f_by_id = {row["phrase_id"]: row for row in foundation}
    f_by_phrase = {row["phrase"].strip().casefold(): row for row in foundation}
    cluster_by_key = {row["cluster_task_key"]: row for row in clusters}
    reg_by_key = {row["target_page_key"]: row for row in registry}
    hier_by_key = {row["target_page_key"]: row for row in hierarchy}
    recon_by_key = {row["target_page_key"]: row for row in reconciliation}
    old_spec_by_key = {row["target_page_key"]: row for row in old_specs}

    enriched_fields = list(phrase_map[0].keys()) + ["wordstat_popular_count", "wordstat_evidence_type"]
    enriched_phrase_rows = []
    for row in phrase_map:
        source = f_by_id[row["phrase_key"]]
        new = dict(row)
        new["wordstat_popular_count"] = source["wordstat_popular_count"]
        new["wordstat_evidence_type"] = source["wordstat_evidence_type"]
        enriched_phrase_rows.append(new)

    phrase_by_page: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in phrase_map:
        phrase_by_page[row["target_landing_page_key"]].append(row)

    market_specs = []
    for page in registry:
        page_key = page["target_page_key"]
        old = old_spec_by_key[page_key]
        reconciliation_row = recon_by_key[page_key]
        action = reconciliation_row["target_action"]
        page_family = type_family(page["page_type"])

        primary_query = page["primary_representative_query"].strip()
        primary_found = f_by_phrase[primary_query.casefold()]
        primary_wordstat = int(primary_found["wordstat_popular_count"] or 0)
        primary_route = next(
            (row for row in phrase_by_page[page_key] if row["phrase"].strip().casefold() == primary_query.casefold()),
            None,
        )
        primary_cluster = cluster_by_key.get(primary_route["cluster_task_key"]) if primary_route else None

        all_page_phrases = phrase_by_page[page_key]
        resolved_phrase_rows = [
            row for row in all_page_phrases
            if cluster_by_key.get(row["cluster_task_key"], {}).get("target_route_state") == "TARGET_PAGE_RESOLVED"
        ]
        candidate_rows = resolved_phrase_rows or all_page_phrases
        sorted_candidates = sorted(
            candidate_rows,
            key=lambda row: (-int(f_by_id[row["phrase_key"]]["wordstat_popular_count"] or 0), row["phrase"]),
        )

        secondaries: list[tuple[str, int]] = []
        seen = [primary_query]
        for phrase_row in sorted_candidates:
            query = phrase_row["phrase"].strip()
            if query.casefold() == primary_query.casefold() or any(too_similar(query, previous) for previous in seen):
                continue
            source = f_by_id[phrase_row["phrase_key"]]
            secondaries.append((query, int(source["wordstat_popular_count"] or 0)))
            seen.append(query)
            if len(secondaries) >= 8:
                break

        resolved_clusters = [
            row for row in clusters
            if row["intended_target_page_key"] == page_key and row["target_route_state"] == "TARGET_PAGE_RESOLVED"
        ]
        no_standalone = [
            row for row in clusters
            if row["intended_target_page_key"] == page_key and row["target_route_state"] == "NO_STANDALONE_ROUTE_TO_PARENT"
        ]

        primary_job = ((primary_cluster or {}).get("intent_user_task_ru") or "").split(";")[0].strip() or page["page_purpose"].strip()
        if action == "RECHECK_NEEDS_EVIDENCE":
            primary_job = "Уточнить поисковую задачу до окончательного назначения самостоятельной страницы."

        own_coverage = "; ".join(row["cluster_task_name_ru"] for row in resolved_clusters)
        if not own_coverage and primary_cluster:
            own_coverage = primary_cluster["cluster_task_name_ru"]

        compatible_embedded, incompatible_support = [], []
        for cluster in no_standalone:
            if primary_cluster and cluster["cluster_task_key"] == primary_cluster["cluster_task_key"]:
                continue
            cluster_family = type_family(cluster["page_type"])
            if cluster_family == page_family or cluster_family == "MIXED" or page_family == "MIXED":
                compatible_embedded.append(cluster["cluster_task_name_ru"])
            else:
                incompatible_support.append(cluster["cluster_task_name_ru"])

        embedded = "; ".join(compatible_embedded) or "Дополнительных совместимых тем без отдельной страницы для этой роли не выделено."
        child_keys = [key.strip() for key in (page.get("child_supporting_target_page_keys") or "").split(";") if key.strip()]
        child_names = [reg_by_key[key]["target_page_name_ru"] for key in child_keys if key in reg_by_key]
        elsewhere = "; ".join(child_names) or "Отдельные соседние роли остаются на своих целевых страницах согласно карте структуры."
        support_parts = list(dict.fromkeys(item for item in incompatible_support + child_names if item))
        support = "; ".join(support_parts) or "Специальные поддерживающие переходы не требуются."

        secondary_display = "; ".join(f"{query} — {value}" for query, value in secondaries) or "Дополнительных самостоятельных запросов для показа нет."
        priority, priority_basis = priority_for(
            page_key,
            action,
            int(page["accepted_routed_phrase_count"] or page["member_phrase_count"] or 0),
            reg_by_key,
            hier_by_key,
        )

        new = dict(old)
        new.update({
            "primary_page_job_ru": primary_job,
            "primary_query_wordstat": str(primary_wordstat),
            "secondary_queries_with_wordstat": secondary_display,
            "recommended_h1_or_blocker": h1_for(page["target_page_name_ru"], action),
            "recommended_title_direction_or_blocker": title_direction(page["target_page_name_ru"], page["page_type"], primary_query, action),
            "analytical_seo_priority": priority,
            "analytical_seo_priority_basis": priority_basis,
            "own_coverage_clean": own_coverage,
            "embedded_no_standalone_topics": embedded,
            "support_mention_link_topics": support,
            "elsewhere_named_pages": elsewhere,
            "market_grade_boundary_note": "Основная роль, встроенные совместимые темы, темы для перехода и соседние самостоятельные страницы разделены.",
        })
        market_specs.append(new)

    spec_fields = list(old_specs[0].keys()) + [
        "primary_page_job_ru", "primary_query_wordstat", "secondary_queries_with_wordstat",
        "recommended_h1_or_blocker", "recommended_title_direction_or_blocker",
        "analytical_seo_priority", "analytical_seo_priority_basis", "own_coverage_clean",
        "embedded_no_standalone_topics", "support_mention_link_topics", "elsewhere_named_pages",
        "market_grade_boundary_note",
    ]

    assert len(foundation) == 2840
    assert len(enriched_phrase_rows) == 2185
    assert len(market_specs) == 60
    assert all(row["primary_page_job_ru"] and ";" not in row["primary_page_job_ru"] for row in market_specs)
    assert all(row["primary_query_wordstat"] != "" for row in market_specs)
    assert all(row["secondary_queries_with_wordstat"] for row in market_specs)
    assert all(row["recommended_h1_or_blocker"] for row in market_specs)
    assert all(row["analytical_seo_priority_basis"] for row in market_specs)
    for row in market_specs:
        own = {item.strip().casefold() for item in row["own_coverage_clean"].split(";") if item.strip()}
        elsewhere = {item.strip().casefold() for item in row["elsewhere_named_pages"].split(";") if item.strip()}
        assert not (own & elsewhere), (row["target_page_name_ru"], own & elsewhere)

    write_gzip_tsv(ROOT / f"TARGET_FIRST_PHRASE_LANDING_MAP_MARKET_GRADE_{DATE}.tsv.gz", enriched_fields, enriched_phrase_rows)
    write_tsv(ROOT / f"TARGET_PAGE_SPEC_REGISTER_MARKET_GRADE_{DATE}.tsv", spec_fields, market_specs)
    print(f"PASS phrase_routes={len(enriched_phrase_rows)} page_specs={len(market_specs)}")


if __name__ == "__main__":
    main()
