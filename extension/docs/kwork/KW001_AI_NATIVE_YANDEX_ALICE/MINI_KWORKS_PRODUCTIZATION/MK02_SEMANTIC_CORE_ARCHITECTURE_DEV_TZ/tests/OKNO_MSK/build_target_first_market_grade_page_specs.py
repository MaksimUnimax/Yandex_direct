#!/usr/bin/env python3
"""Build market-grade phrase-map and page-spec authorities from accepted MK02 data."""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

DATE = "2026-09-10"
ROOT = Path(__file__).resolve().parent
PHRASE_OUTPUT = ROOT / f"TARGET_FIRST_PHRASE_LANDING_MAP_MARKET_GRADE_{DATE}.tsv.gz"
SPEC_OUTPUT = ROOT / f"TARGET_PAGE_SPEC_REGISTER_MARKET_GRADE_{DATE}.tsv"
QA_OUTPUT = ROOT / f"TARGET_FIRST_MARKET_GRADE_AUTHORITY_QA_{DATE}.json"

RESOLVED = "TARGET_PAGE_RESOLVED"
NO_STANDALONE = "NO_STANDALONE_ROUTE_TO_PARENT"
RECHECK_STATES = {"RECHECK_NEEDS_EVIDENCE", "UNRESOLVED_TASK_ROUTING"}
TERMINAL_PREPOSITIONS = {"без", "в", "для", "до", "за", "из", "к", "на", "над", "от", "по", "под", "при", "про", "с"}
WORDSTAT_NOTE = (
    "Индивидуальный сохранённый показатель Вордстата для фразы. Значения разных фраз не суммируются "
    "в прогноз трафика или спрос страницы."
)
PRIMARY_QUERY_OVERRIDES = {
    "TP-BALCONY-GLAZING-WARM": (
        "теплое остекление балконов",
        "Выбран естественный точный запрос роли страницы; прежняя формулировка была частотнее лишь на 2 показа и содержала неестественный порядок слов.",
    ),
    "TP-WINDOW-SELECTION-GUIDE": (
        "как выбрать пластиковые окна",
        "Выбран точный запрос роли страницы: прежний представительный запрос описывал более узкую соседнюю задачу.",
    ),
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    opener = gzip.open if path.suffix == ".gz" else open
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm_text(text: str) -> str:
    return " ".join(re.findall(r"[a-zа-яё0-9]+", (text or "").casefold().replace("ё", "е")))


def stem_token(token: str) -> str:
    endings = (
        "иями", "ями", "ами", "ого", "ему", "ому", "ыми", "ими", "ая", "яя", "ое", "ее",
        "ые", "ие", "ый", "ий", "ой", "ую", "юю", "ов", "ев", "ах", "ях", "ам", "ям",
        "а", "я", "ы", "и", "у", "ю", "е", "о",
    )
    for ending in endings:
        if len(token) >= len(ending) + 4 and token.endswith(ending):
            return token[: -len(ending)]
    return token


def semantic_tokens(text: str) -> set[str]:
    stop = {"главная", "для", "или", "как", "на", "по", "с", "что", "это"}
    return {stem_token(token) for token in norm_text(text).split() if token not in stop and len(token) > 1}


def similarity(left: str, right: str) -> float:
    left_norm, right_norm = norm_text(left), norm_text(right)
    if not left_norm or not right_norm:
        return 0.0
    left_tokens, right_tokens = semantic_tokens(left), semantic_tokens(right)
    jaccard = len(left_tokens & right_tokens) / max(1, len(left_tokens | right_tokens))
    sequence = SequenceMatcher(None, left_norm, right_norm).ratio()
    return max(jaccard, sequence)


def role_alignment(page_name: str, query: str) -> float:
    role, phrase = semantic_tokens(page_name), semantic_tokens(query)
    return len(role & phrase) / max(1, len(role))


def low_quality_query(query: str) -> bool:
    tokens = norm_text(query).split()
    if not tokens or tokens[-1] in TERMINAL_PREPOSITIONS:
        return True
    if "ключ" in tokens and not any(tokens[index - 1:index + 1] == ["под", "ключ"] for index in range(1, len(tokens))):
        return True
    return False


def query_angle(query: str) -> str:
    token_set = set(norm_text(query).split())
    if token_set & {"цена", "цены", "стоимость", "сколько", "недорого"}:
        return "PRICE"
    if token_set & {"москва", "москве", "московский"}:
        return "LOCATION"
    if token_set & {"установка", "установить", "монтаж", "замена", "ремонт", "регулировка"}:
        return "INSTALL_OR_SERVICE"
    if token_set & {"купить", "заказать", "производитель", "официальный", "рассрочка"}:
        return "PURCHASE"
    if token_set & {"лучше", "лучшие", "сравнение", "сравнить", "выбрать", "виды", "размер", "цвет", "отзывы"}:
        return "CHOICE_OR_PROPERTY"
    return "CORE_OR_OTHER"


def type_family(page_type: str) -> str:
    text = (page_type or "").casefold()
    if "портфолио" in text:
        return "PORTFOLIO"
    if "интерактив" in text:
        return "TOOL"
    if "информацион" in text:
        return "INFORMATIONAL"
    if "коммерчес" in text:
        return "COMMERCIAL"
    if "требует определения" in text:
        return "UNRESOLVED"
    return "OTHER"


def compatible_no_standalone(page: dict[str, str], cluster: dict[str, str]) -> bool:
    family = type_family(page["page_type"])
    text = f"{cluster['cluster_task_name_ru']} {cluster['intent_user_task_ru']}".casefold()
    information_markers = ("самостоятель", "своими руками", "отзыв", "сравн", "разобраться", "узнать требования")
    commercial_markers = ("выбрать и заказать", "выбрать и купить", "заказать профессион", "заказать остекление")
    if family == "COMMERCIAL":
        return not any(marker in text for marker in information_markers)
    if family == "INFORMATIONAL":
        # Use the normalized page role, not the legacy mixed intent/purpose field:
        # that field is exactly what the market-grade boundary correction replaces.
        page_text = page["target_page_name_ru"].casefold()
        unrelated_diy = any(marker in text for marker in ("самостоятель", "своими руками", "ремонт")) and not any(
            marker in page_text for marker in ("самостоятель", "своими руками", "ремонт", "отрегулировать")
        )
        return not unrelated_diy and not any(marker in text for marker in commercial_markers)
    if family == "PORTFOLIO":
        return any(marker in text for marker in ("пример", "фото", "дизайн", "портфолио"))
    if family == "TOOL":
        return any(marker in text for marker in ("калькулятор", "стоимость", "цена", "рассчитать"))
    return False


def primary_page_job(page: dict[str, str], action: str) -> str:
    name = page["target_page_name_ru"].removeprefix("Главная: ").strip()
    family = type_family(page["page_type"])
    if action == "RECHECK_NEEDS_EVIDENCE" or family == "UNRESOLVED":
        return "Уточнить самостоятельную поисковую задачу до назначения целевой страницы."
    if family == "TOOL":
        return "Помочь рассчитать ориентировочную стоимость окон перед замером и обращением."
    if family == "PORTFOLIO":
        return "Показать примеры выполненных работ и помочь перейти к подходящему виду остекления."
    if page["target_page_key"] == "TP-WINDOWS-COMMERCIAL-GENERAL":
        return "Помочь выбрать окна или двери и перейти к подходящей категории, услуге или расчёту."
    if family == "INFORMATIONAL":
        return f"Дать практический ответ по теме «{name}» и направить к релевантной услуге при необходимости."
    return f"Помочь выбрать и заказать «{name}» в рамках подтверждённой роли страницы."


def h1_for(page_name: str, action: str) -> str:
    if action == "RECHECK_NEEDS_EVIDENCE":
        return "Блокер: не назначать H1 до уточнения самостоятельной поисковой задачи."
    return page_name.removeprefix("Главная: ").strip()


def title_direction(page_name: str, page_type: str, primary_query: str, action: str) -> tuple[str, str]:
    if action == "RECHECK_NEEDS_EVIDENCE":
        return "Блокер: не назначать Title до уточнения самостоятельной поисковой задачи.", "BLOCKED_UNRESOLVED_ROLE"
    if action != "OPTIMIZE_STRENGTHEN":
        return "Изменение Title не требуется по текущему решению; сохранить метаданные до отдельного обоснования.", "TITLE_CHANGE_NOT_REQUIRED"
    if "Информационная" in page_type:
        return (
            f"Направление Title: «{page_name}» + конкретный вопрос или критерий выбора; основной фокус — «{primary_query}». Не добавлять неподтверждённые коммерческие обещания.",
            "TITLE_DIRECTION_REQUIRED_AND_PRESENT",
        )
    if "Портфолио" in page_type:
        return (
            f"Направление Title: «{page_name}» + примеры работ в Москве; основной фокус — «{primary_query}». Не перечислять неподтверждённые категории.",
            "TITLE_DIRECTION_REQUIRED_AND_PRESENT",
        )
    return (
        f"Направление Title: «{primary_query}» + подтверждённый коммерческий смысл страницы + Москва. Не добавлять неподтверждённые цены, сроки или условия.",
        "TITLE_DIRECTION_REQUIRED_AND_PRESENT",
    )


def priority_for(page: dict[str, str], action: str, routed_count: int, hierarchy: dict[str, str]) -> tuple[str, str]:
    has_children = bool((page.get("child_supporting_target_page_keys") or "").strip())
    is_section = hierarchy.get("hierarchy_level") == "SECTION_LANDING_OR_STANDALONE"
    if action == "RECHECK_NEEDS_EVIDENCE":
        return "Высокий", "Неразрешённая роль блокирует окончательную рассадку. Это важность аналитической проверки, а не порядок разработки."
    if action in {"OPTIMIZE_STRENGTHEN", "ROUTE_INTERNAL_LINK_CHANGE"} and routed_count >= 20:
        return "Высокий", f"Есть подтверждённый разрыв между текущим и целевым состоянием и {routed_count} распределённых фраз. Приоритет не задаёт срок внедрения."
    if routed_count >= 100 or (is_section and routed_count >= 40):
        return "Высокий", f"Крупная или центральная роль целевой структуры: {routed_count} распределённых фраз."
    if action in {"OPTIMIZE_STRENGTHEN", "ROUTE_INTERNAL_LINK_CHANGE"}:
        return "Средний", "Есть подтверждённое изменение при меньшем охвате спроса. Это SEO-приоритет, а не производственный порядок."
    if routed_count >= 20 or is_section or has_children:
        return "Средний", f"Заметная семантическая или структурная роль: {routed_count} распределённых фраз."
    return "Низкий", f"Узкая подтверждённая роль: {routed_count} распределённых фраз. Это не оценка бизнес-ценности или ожидаемого роста."


def choose_primary_query(page, page_phrases, cluster_by_key, foundation_by_id):
    eligible = [
        row for row in page_phrases
        if cluster_by_key.get(row["cluster_task_key"], {}).get("target_route_state") in {RESOLVED, NO_STANDALONE}
    ] or page_phrases
    source_query = page["primary_representative_query"].strip()
    source = next((row for row in eligible if norm_text(row["phrase"]) == norm_text(source_query)), None)
    if page["target_page_key"] in PRIMARY_QUERY_OVERRIDES:
        override_query, basis = PRIMARY_QUERY_OVERRIDES[page["target_page_key"]]
        override = next((row for row in eligible if norm_text(row["phrase"]) == norm_text(override_query)), None)
        if override is None:
            raise AssertionError(f"primary-query override is absent from accepted routes: {page['target_page_key']} / {override_query}")
        return override, basis
    exact_role = [row for row in eligible if norm_text(row["phrase"]) == norm_text(page["target_page_name_ru"].removeprefix("Главная: "))]
    if exact_role and source and role_alignment(page["target_page_name_ru"], source_query) < 0.60:
        chosen = max(exact_role, key=lambda row: int(foundation_by_id[row["phrase_key"]]["wordstat_popular_count"] or 0))
        return chosen, "Выбран точный запрос роли страницы: прежний представительный запрос описывал более узкую соседнюю задачу."
    if source:
        return source, "Сохранён принятый представительный запрос; он присутствует среди фраз, распределённых на эту страницу."
    chosen = max(
        eligible,
        key=lambda row: (role_alignment(page["target_page_name_ru"], row["phrase"]), int(foundation_by_id[row["phrase_key"]]["wordstat_popular_count"] or 0)),
    )
    return chosen, "Запрос выбран из принятых распределённых фраз по соответствию роли страницы и индивидуальному спросу."


def select_secondaries(primary, candidates, foundation_by_id, limit=8):
    ranked = sorted(candidates, key=lambda row: (-int(foundation_by_id[row["phrase_key"]]["wordstat_popular_count"] or 0), row["phrase"]))
    usable = []
    seen_queries = [primary["phrase"]]
    for row in ranked:
        query = row["phrase"].strip()
        if norm_text(query) == norm_text(primary["phrase"]) or low_quality_query(query):
            continue
        if any(similarity(query, previous) >= 0.84 for previous in seen_queries):
            continue
        usable.append(row)
        seen_queries.append(query)

    # Demand is the principal ordering signal.  Similarity filtering above removes
    # repetitions; forcing one item from every artificial "angle" can otherwise
    # promote a noisy 1–2 impression phrase over a useful, materially demanded one.
    selected = usable[:limit]
    return [(row["phrase"].strip(), int(foundation_by_id[row["phrase_key"]]["wordstat_popular_count"] or 0)) for row in selected]


def main() -> None:
    input_paths = {
        "foundation": ROOT / f"MK02_SEMANTIC_FOUNDATION_{DATE}.tsv.gz",
        "phrase_map": ROOT / f"TARGET_FIRST_PHRASE_LANDING_MAP_{DATE}.tsv.gz",
        "clusters": ROOT / f"TARGET_FIRST_CLUSTER_LANDING_MAP_{DATE}.tsv",
        "registry": ROOT / f"TARGET_PAGE_REGISTRY_{DATE}.tsv",
        "hierarchy": ROOT / f"TARGET_ARCHITECTURE_HIERARCHY_{DATE}.tsv",
        "reconciliation": ROOT / f"CURRENT_TARGET_RECONCILIATION_{DATE}.tsv",
        "old_specs": ROOT / f"TARGET_PAGE_SPEC_REGISTER_{DATE}.tsv",
        "delta": ROOT / f"CURRENT_TARGET_CHANGE_DELTA_{DATE}.tsv",
    }
    foundation = read_tsv(input_paths["foundation"])
    phrase_map = read_tsv(input_paths["phrase_map"])
    clusters = read_tsv(input_paths["clusters"])
    registry = read_tsv(input_paths["registry"])
    hierarchy = read_tsv(input_paths["hierarchy"])
    reconciliation = read_tsv(input_paths["reconciliation"])
    old_specs = read_tsv(input_paths["old_specs"])
    delta = read_tsv(input_paths["delta"])

    foundation_by_id = {row["phrase_id"]: row for row in foundation}
    cluster_by_key = {row["cluster_task_key"]: row for row in clusters}
    registry_by_key = {row["target_page_key"]: row for row in registry}
    hierarchy_by_key = {row["target_page_key"]: row for row in hierarchy}
    recon_by_key = {row["target_page_key"]: row for row in reconciliation}
    old_spec_by_key = {row["target_page_key"]: row for row in old_specs}

    enriched_fields = list(phrase_map[0]) + ["wordstat_popular_count", "wordstat_evidence_type", "wordstat_metric_note"]
    enriched_phrase_rows = []
    for row in phrase_map:
        source = foundation_by_id[row["phrase_key"]]
        new = dict(row)
        new["wordstat_popular_count"] = source["wordstat_popular_count"]
        new["wordstat_evidence_type"] = source["wordstat_evidence_type"]
        new["wordstat_metric_note"] = WORDSTAT_NOTE
        enriched_phrase_rows.append(new)

    phrase_by_page = defaultdict(list)
    cluster_by_page = defaultdict(list)
    for row in phrase_map:
        phrase_by_page[row["target_landing_page_key"]].append(row)
    for row in clusters:
        cluster_by_page[row["intended_target_page_key"]].append(row)

    raw_boundaries = {}
    market_specs = []
    for page in registry:
        page_key = page["target_page_key"]
        old = old_spec_by_key[page_key]
        action = recon_by_key[page_key]["target_action"]
        page_clusters = cluster_by_page[page_key]
        page_phrases = phrase_by_page[page_key]
        primary_route, primary_basis = choose_primary_query(page, page_phrases, cluster_by_key, foundation_by_id)
        primary_source = foundation_by_id[primary_route["phrase_key"]]

        resolved_clusters = [row for row in page_clusters if row["target_route_state"] == RESOLVED]
        no_standalone_clusters = [row for row in page_clusters if row["target_route_state"] == NO_STANDALONE]
        embedded_clusters = [row for row in no_standalone_clusters if compatible_no_standalone(page, row)]
        support_clusters = [row for row in no_standalone_clusters if row not in embedded_clusters]
        recheck_clusters = [row for row in page_clusters if row["target_route_state"] in RECHECK_STATES]

        eligible_cluster_keys = {row["cluster_task_key"] for row in resolved_clusters + embedded_clusters}
        if action == "RECHECK_NEEDS_EVIDENCE":
            eligible_cluster_keys |= {row["cluster_task_key"] for row in recheck_clusters}
        secondary_candidates = [row for row in page_phrases if row["cluster_task_key"] in eligible_cluster_keys]
        secondaries = select_secondaries(primary_route, secondary_candidates, foundation_by_id)

        own_topics = [row["cluster_task_name_ru"] for row in resolved_clusters] or [f"{page['target_page_name_ru']}: {primary_route['phrase']}"]
        embedded_topics = [row["cluster_task_name_ru"] for row in embedded_clusters]
        support_topics = [row["cluster_task_name_ru"] for row in support_clusters]
        child_keys = [key.strip() for key in (page.get("child_supporting_target_page_keys") or "").split(";") if key.strip()]
        child_names = [registry_by_key[key]["target_page_name_ru"] for key in child_keys if key in registry_by_key]
        pending_topics = [row["cluster_task_name_ru"] for row in recheck_clusters]
        raw_boundaries[page_key] = {"own": own_topics, "embedded": embedded_topics, "support": support_topics, "elsewhere": child_names + pending_topics}

        own_display = " | ".join(f"Раскрыть на этой странице: {topic}." for topic in own_topics)
        embedded_display = " | ".join(f"Встроить без отдельного URL: {topic}." for topic in embedded_topics) or "Дополнительных совместимых тем без отдельного URL не выделено."
        support_display = " | ".join(f"Кратко упомянуть или использовать как переход: {topic}." for topic in support_topics) or "Отдельных тем только для краткого упоминания или перехода не выделено."
        elsewhere_parts = [f"«{name}» — полное раскрытие на отдельной целевой странице; здесь только обзор и переход." for name in child_names]
        elsewhere_parts.extend(f"«{topic}» — не включать в основную ответственность до отдельной проверки." for topic in pending_topics)
        elsewhere_display = " | ".join(elsewhere_parts) or "Отдельные соседние владельцы для этой роли не назначены."
        boundary_explanations = [
            f"На странице «{page['target_page_name_ru']}» допустим обзор категории и выбор направления; «{name}» отвечает за полное раскрытие конкретного подтипа."
            for name in child_names
        ]
        boundary_explanations.extend(
            f"Тема «{topic}» не входит в собственное покрытие до получения недостающих доказательств."
            for topic in pending_topics
        )
        boundary_explanations_display = " | ".join(boundary_explanations) or "Дополнительное разграничение с соседней страницей не требуется."

        secondary_display = " | ".join(f"{query} — {value}" for query, value in secondaries)
        if not secondary_display:
            secondary_display = "Нет: после удаления основного запроса дополнительных самостоятельных фраз для показа не осталось."
        routed_count = len(page_phrases)
        priority, priority_basis = priority_for(page, action, routed_count, hierarchy_by_key[page_key])
        title, title_state = title_direction(page["target_page_name_ru"], page["page_type"], primary_route["phrase"], action)

        new = dict(old)
        new.update({
            "source_primary_representative_query": old["primary_representative_query"],
            "primary_representative_query": primary_route["phrase"],
            "primary_page_job_ru": primary_page_job(page, action),
            "primary_query_selection_basis": primary_basis,
            "primary_query_wordstat": primary_source["wordstat_popular_count"],
            "primary_query_wordstat_evidence_type": primary_source["wordstat_evidence_type"],
            "secondary_queries_with_wordstat": secondary_display,
            "secondary_query_count": str(len(secondaries)),
            "total_routed_phrase_count": str(routed_count),
            "wordstat_metric_note": WORDSTAT_NOTE,
            "recommended_h1_or_blocker": h1_for(page["target_page_name_ru"], action),
            "recommended_title_direction_or_blocker": title,
            "title_requirement_state": title_state,
            "analytical_seo_priority": priority,
            "analytical_seo_priority_basis": priority_basis,
            "own_coverage_clean": own_display,
            "embedded_no_standalone_topics": embedded_display,
            "support_mention_link_topics": support_display,
            "elsewhere_named_pages": elsewhere_display,
            "boundary_overlap_explanations": boundary_explanations_display,
            "market_grade_boundary_note": (
                "Основная зона означает полное раскрытие на этой странице. Встроенная тема не получает отдельный URL. "
                "Поддерживающая тема допускает только краткое упоминание или переход. Для каждой темы в поле «отдельно/после проверки» названо, "
                "что здесь допустим только обзор, переход или ожидание доказательств."
            ),
        })
        market_specs.append(new)

    spec_fields = list(old_specs[0]) + [
        "source_primary_representative_query", "primary_page_job_ru", "primary_query_selection_basis",
        "primary_query_wordstat", "primary_query_wordstat_evidence_type", "secondary_queries_with_wordstat",
        "secondary_query_count", "total_routed_phrase_count", "wordstat_metric_note",
        "recommended_h1_or_blocker", "recommended_title_direction_or_blocker", "title_requirement_state",
        "analytical_seo_priority", "analytical_seo_priority_basis", "own_coverage_clean",
        "embedded_no_standalone_topics", "support_mention_link_topics", "elsewhere_named_pages", "market_grade_boundary_note",
        "boundary_overlap_explanations",
    ]

    action_counts = Counter(row["target_action"] for row in reconciliation)
    target_keys = {row["target_page_key"] for row in registry}
    unexplained_overlap = []
    for page_key, boundary in raw_boundaries.items():
        if any(not topic.strip() for values in boundary.values() for topic in values):
            unexplained_overlap.append({"target_page_key": page_key, "reason": "blank boundary topic"})
        for own in boundary["own"]:
            for elsewhere in boundary["elsewhere"]:
                if norm_text(own) == norm_text(elsewhere):
                    unexplained_overlap.append({"target_page_key": page_key, "own": own, "elsewhere": elsewhere})
                elif similarity(own, elsewhere) >= 0.45:
                    spec = next(row for row in market_specs if row["target_page_key"] == page_key)
                    if not spec["boundary_overlap_explanations"].strip():
                        unexplained_overlap.append({"target_page_key": page_key, "own": own, "elsewhere": elsewhere})

    checks = {
        "source_accounting_2840": len(foundation) == 2840,
        "working_phrase_routes_2185": len(enriched_phrase_rows) == 2185,
        "cluster_routes_161": len(clusters) == 161,
        "target_pages_60": len(registry) == 60,
        "market_grade_page_specs_60": len(market_specs) == 60,
        "phrase_wordstat_present": all(row["wordstat_popular_count"].strip() for row in enriched_phrase_rows),
        "primary_query_wordstat_60": all(row["primary_query_wordstat"].strip() for row in market_specs),
        "secondary_contract_60": all(row["secondary_queries_with_wordstat"].strip() for row in market_specs),
        "secondary_values_individual": all(
            int(row["secondary_query_count"]) == len(re.findall(r" — \d+(?: \||$)", row["secondary_queries_with_wordstat"]))
            for row in market_specs
        ),
        "one_primary_page_job_60": all(row["primary_page_job_ru"].strip() and ";" not in row["primary_page_job_ru"] for row in market_specs),
        "unexplained_own_elsewhere_overlap_zero": not unexplained_overlap,
        "h1_or_blocker_60": all(row["recommended_h1_or_blocker"].strip() for row in market_specs),
        "title_contract": all(row["title_requirement_state"] == "TITLE_DIRECTION_REQUIRED_AND_PRESENT" for row in market_specs if row["target_action"] == "OPTIMIZE_STRENGTHEN"),
        "priority_and_basis_60": all(row["analytical_seo_priority"].strip() and row["analytical_seo_priority_basis"].strip() for row in market_specs),
        "reconciliation_48_7_4_1": action_counts == Counter({"KEEP_LOCK_AS_TARGET_OWNER": 48, "OPTIMIZE_STRENGTHEN": 7, "ROUTE_INTERNAL_LINK_CHANGE": 4, "RECHECK_NEEDS_EVIDENCE": 1}),
        "change_delta_14_is_subset": len(delta) == 14 and {row["target_page_key"] for row in delta}.issubset(target_keys),
        "fake_create_zero": not any("CREATE" in row["target_action"] for row in market_specs),
        "routed_counts_match_registry": all(int(row["total_routed_phrase_count"]) == int(registry_by_key[row["target_page_key"]]["member_phrase_count"]) for row in market_specs),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(f"market-grade authority checks failed: {failed}")

    write_gzip_tsv(PHRASE_OUTPUT, enriched_fields, enriched_phrase_rows)
    write_tsv(SPEC_OUTPUT, spec_fields, market_specs)
    report = {
        "schema": "MK02_TARGET_FIRST_MARKET_GRADE_AUTHORITY_QA_V1",
        "date": DATE,
        "status": "PASS",
        "checks_total": len(checks),
        "checks": {name: "PASS" for name in checks},
        "counts": {
            "semantic_universe": len(foundation), "working_phrase_routes": len(enriched_phrase_rows), "cluster_tasks": len(clusters),
            "target_pages": len(registry), "page_specs": len(market_specs), "keep": action_counts["KEEP_LOCK_AS_TARGET_OWNER"],
            "optimize": action_counts["OPTIMIZE_STRENGTHEN"], "route": action_counts["ROUTE_INTERNAL_LINK_CHANGE"],
            "recheck": action_counts["RECHECK_NEEDS_EVIDENCE"], "change_delta": len(delta), "create": 0, "provider_calls": 0,
        },
        "primary_query_corrections": [
            {"target_page_key": row["target_page_key"], "source": row["source_primary_representative_query"], "market_grade": row["primary_representative_query"], "basis": row["primary_query_selection_basis"]}
            for row in market_specs if row["source_primary_representative_query"] != row["primary_representative_query"]
        ],
        "source_sha256": {name: sha256(path) for name, path in input_paths.items()},
        "outputs": {
            PHRASE_OUTPUT.name: {"bytes": PHRASE_OUTPUT.stat().st_size, "sha256": sha256(PHRASE_OUTPUT)},
            SPEC_OUTPUT.name: {"bytes": SPEC_OUTPUT.stat().st_size, "sha256": sha256(SPEC_OUTPUT)},
        },
    }
    QA_OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "checks": len(checks), "counts": report["counts"], "primary_query_corrections": report["primary_query_corrections"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
