#!/usr/bin/env python3
"""Build the market-grade analytical and implementation PDFs for OKNO_MSK."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

from pypdf import PdfReader
from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    LongTable,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


DATE = "2026-09-10"
rl_config.invariant = 1
ROOT = Path(__file__).resolve().parent
DELIVERY = ROOT / f"CLIENT_DELIVERY_PHASE_7_TARGET_FIRST_MARKET_GRADE_{DATE}"
ANALYTICAL = DELIVERY / f"TARGET_SEO_ARCHITECTURE_REPORT_OKNO_MSK_{DATE}.pdf"
TZ = DELIVERY / f"TARGET_PAGE_SPECIFICATION_TZ_OKNO_MSK_{DATE}.pdf"
REPORT = ROOT / f"TARGET_FIRST_MARKET_GRADE_CLIENT_PDF_BUILD_REPORT_{DATE}.json"

NAVY = colors.HexColor("#17365D")
TEAL = colors.HexColor("#0F6B78")
INK = colors.HexColor("#1F2937")
GREY = colors.HexColor("#5B6573")
LIGHT_GREY = colors.HexColor("#D7DEE7")
VERY_LIGHT = colors.HexColor("#F7F9FC")
PALE_BLUE = colors.HexColor("#EAF3F8")
PALE_TEAL = colors.HexColor("#E6F3F3")
PALE_GREEN = colors.HexColor("#E8F5EC")
PALE_AMBER = colors.HexColor("#FFF3D6")
PALE_RED = colors.HexColor("#FCE8E6")

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))


def read_rows(name: str, gz: bool = False) -> list[dict[str, str]]:
    opener = gzip.open if gz else open
    with opener(ROOT / name, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


FOUNDATION = read_rows(f"MK02_SEMANTIC_FOUNDATION_{DATE}.tsv.gz", True)
PHRASES = read_rows(f"TARGET_FIRST_PHRASE_LANDING_MAP_MARKET_GRADE_{DATE}.tsv.gz", True)
CLUSTERS = read_rows(f"TARGET_FIRST_CLUSTER_LANDING_MAP_{DATE}.tsv")
REGISTRY = read_rows(f"TARGET_PAGE_REGISTRY_{DATE}.tsv")
HIERARCHY = read_rows(f"TARGET_ARCHITECTURE_HIERARCHY_{DATE}.tsv")
RECON = read_rows(f"CURRENT_TARGET_RECONCILIATION_{DATE}.tsv")
SPECS = read_rows(f"TARGET_PAGE_SPEC_REGISTER_MARKET_GRADE_{DATE}.tsv")
DELTA = read_rows(f"CURRENT_TARGET_CHANGE_DELTA_{DATE}.tsv")

PAGE_NAME_BY_KEY = {row["target_page_key"]: row["target_page_name_ru"] for row in REGISTRY}
SPEC_BY_KEY = {row["target_page_key"]: row for row in SPECS}
RECON_BY_KEY = {row["target_page_key"]: row for row in RECON}
DELTA_BY_PAGE: dict[str, list[dict[str, str]]] = defaultdict(list)
for delta_row in DELTA:
    DELTA_BY_PAGE[delta_row["target_page_key"]].append(delta_row)

ACTION_RU = {
    "KEEP_LOCK_AS_TARGET_OWNER": "Сохранить и закрепить как целевую посадочную",
    "OPTIMIZE_STRENGTHEN": "Усилить существующую страницу",
    "ROUTE_INTERNAL_LINK_CHANGE": "Изменить маршрут или внутреннюю связь",
    "RECHECK_NEEDS_EVIDENCE": "Перепроверить — нужны доказательства",
}
MATCH_RU = {
    "EXISTING_MATCH": "Существующая страница подтверждена",
    "EXISTING_NEEDS_OPTIMIZATION": "Существующую страницу нужно усилить",
    "EXISTING_RELATIONSHIP_CHANGE": "Нужно изменить связь страниц",
    "UNRESOLVED": "Требуется проверка",
}
ROUTE_RU = {
    "TARGET_PAGE_RESOLVED": "Самостоятельная целевая посадочная определена",
    "NO_STANDALONE_ROUTE_TO_PARENT": "Отдельный URL не нужен — включить в названного владельца",
    "RECHECK_NEEDS_EVIDENCE": "Нужна дополнительная проверка",
    "NO_TARGET_OUTSIDE_SCOPE": "Вне области исследования",
    "UNRESOLVED_TASK_ROUTING": "Маршрут не определён — доказательств недостаточно",
}
CHANGE_RU = {"YES": "Да", "NO": "Нет", "UNRESOLVED": "Не определено"}
READY_RU = {
    "READY_IMPLEMENTATION_SPEC": "Готово к внедрению",
    "PENDING_BUSINESS_DETAIL": "Нужно бизнес-уточнение",
    "PENDING_PLACEMENT_OR_CONTEXT": "Нужно точное место или контекст",
}


def display_page_name(value: str | None) -> str:
    return str(value or "").replace("DIY-задача", "задача самостоятельного выполнения")


def clean(value: str | None) -> str:
    text = str(value or "").strip()
    mapped = ACTION_RU.get(text) or MATCH_RU.get(text) or ROUTE_RU.get(text) or CHANGE_RU.get(text) or READY_RU.get(text) or text
    replacements = {
        "NONE": "Нет",
        "EXACT_SEARCH_TASK_BOUNDARY_REQUIRED": "Нужна точная проверка границы поисковой задачи",
        "EXISTING_MATCH:": "Текущая страница подтверждена:",
        "EXISTING_NEEDS_OPTIMIZATION:": "Текущую страницу нужно усилить:",
        "EXISTING_RELATIONSHIP_CHANGE:": "Для текущей страницы нужна корректировка связи:",
        "REUSE_CURRENT_PAGE": "Повторно использовать существующую страницу",
        "SUPPORTED_WITHIN_ACCEPTED_SCOPE": "Подтверждено в принятой области",
        "NO_CREATE_SPLIT_MERGE_REDIRECT_DELETE_AUTHORIZED": "Создание, разделение, объединение, редирект и удаление не разрешены",
        "PENDING_BUSINESS_DETAIL": "нужно бизнес-уточнение",
        "PENDING_PLACEMENT_OR_CONTEXT": "нужно точное место или контекст",
        "READY_IMPLEMENTATION_SPEC": "готово к внедрению",
        "TARGET_ROLE::": "Целевая роль: ",
        "company-specific": "подтверждённый компанией",
        "exact-match": "с точным вхождением",
        "READY-часть": "часть, готовая к публикации",
        "CTA": "кнопки обращения и формы заявки",
        "PENDING:": "До внедрения уточнить:",
        "Source and target resolve; link is visible/contextual; target task matches note; no conflicting canonical owner.": "Страница-источник и целевая страница открываются; ссылка видима и соответствует контексту; переход ведёт на страницу с нужной задачей; конфликт владельцев не возникает.",
        "Source and target resolve; placement context is named; target task matches note; preservation holds.": "Страница-источник и целевая страница открываются; точное место ссылки названо; переход соответствует задаче целевой страницы; ограничения по сохранению соблюдены.",
        "Source and target resolve": "Страница-источник и целевая страница открываются",
        "link is visible/contextual": "ссылка видима и соответствует контексту",
        "target task matches note": "переход соответствует задаче целевой страницы",
        "no conflicting canonical owner": "конфликт владельцев не возникает",
    }
    for source, target in replacements.items():
        mapped = mapped.replace(source, target)
    return display_page_name(mapped)


def route_text(value: str | None) -> str:
    raw = str(value or "").strip()
    if raw.startswith("TARGET_ROLE::"):
        key = raw.removeprefix("TARGET_ROLE::")
        if key in PAGE_NAME_BY_KEY and key != "TP-UNRESOLVED-DIY-WINDOW-TASK":
            return f"Целевая роль «{display_page_name(PAGE_NAME_BY_KEY[key])}»"
        return "Маршрут не назначен до получения недостающего доказательства"
    return raw or "Не назначен до проверки"


def page_name(key: str | None, empty: str = "Корень раздела") -> str:
    if not key:
        return empty
    return display_page_name(PAGE_NAME_BY_KEY.get(key, "Неназванная роль — требуется проверка"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


styles = getSampleStyleSheet()
TITLE = ParagraphStyle("TitleRu", parent=styles["Title"], fontName="DejaVu-Bold", fontSize=22, leading=27, textColor=NAVY, spaceAfter=8 * mm)
SUBTITLE = ParagraphStyle("SubtitleRu", parent=styles["Normal"], fontName="DejaVu", fontSize=11, leading=15, textColor=GREY, spaceAfter=5 * mm)
H1 = ParagraphStyle("H1Ru", parent=styles["Heading1"], fontName="DejaVu-Bold", fontSize=16, leading=20, textColor=NAVY, spaceBefore=2 * mm, spaceAfter=4 * mm)
H2 = ParagraphStyle("H2Ru", parent=styles["Heading2"], fontName="DejaVu-Bold", fontSize=12, leading=15, textColor=TEAL, spaceBefore=3 * mm, spaceAfter=2 * mm)
BODY = ParagraphStyle("BodyRu", parent=styles["BodyText"], fontName="DejaVu", fontSize=9.2, leading=13, textColor=INK, spaceAfter=2.5 * mm)
SMALL = ParagraphStyle("SmallRu", parent=BODY, fontSize=7.3, leading=9.3, spaceAfter=0)
SMALL_BOLD = ParagraphStyle("SmallBoldRu", parent=SMALL, fontName="DejaVu-Bold")
CELL = ParagraphStyle("CellRu", parent=BODY, fontSize=7.4, leading=9.4, spaceAfter=0)
CELL_BOLD = ParagraphStyle("CellBoldRu", parent=CELL, fontName="DejaVu-Bold")
TREE_ROOT = ParagraphStyle("TreeRoot", parent=CELL_BOLD, fontSize=8.2, leading=10.5, textColor=NAVY)
TREE_CHILD = ParagraphStyle("TreeChild", parent=CELL, fontSize=7.8, leading=10, leftIndent=8)
CALLOUT = ParagraphStyle("CalloutRu", parent=BODY, fontName="DejaVu-Bold", fontSize=10, leading=14, textColor=NAVY, alignment=TA_CENTER)
BADGE = ParagraphStyle("BadgeRu", parent=SMALL_BOLD, alignment=TA_CENTER, textColor=NAVY)


def paragraph(value: str | None, style: ParagraphStyle = BODY) -> Paragraph:
    normalized = clean(value).replace(" | ", "<br/>").replace("; ", ";<br/>")
    return Paragraph(escape(normalized).replace("&lt;br/&gt;", "<br/>"), style)


def footer(canvas, doc, short_title: str) -> None:
    canvas.saveState()
    width, _height = landscape(A4)
    canvas.setStrokeColor(LIGHT_GREY)
    canvas.line(14 * mm, 12 * mm, width - 14 * mm, 12 * mm)
    canvas.setFont("DejaVu", 7)
    canvas.setFillColor(GREY)
    canvas.drawString(14 * mm, 7.5 * mm, short_title)
    canvas.drawRightString(width - 14 * mm, 7.5 * mm, f"Страница {doc.page}")
    canvas.restoreState()


def make_doc(path: Path, short_title: str) -> BaseDocTemplate:
    page = landscape(A4)
    doc = BaseDocTemplate(
        str(path), pagesize=page, leftMargin=14 * mm, rightMargin=14 * mm,
        topMargin=13 * mm, bottomMargin=16 * mm, title=short_title, author="okno-msk.ru",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates(PageTemplate(id="landscape", frames=[frame], onPage=lambda c, d: footer(c, d, short_title)))
    return doc


def data_table(data, widths, *, font_size=7.4, header=True, row_backgrounds=None) -> LongTable:
    prepared = []
    for row_index, row in enumerate(data):
        base = CELL_BOLD if header and row_index == 0 else CELL
        style = ParagraphStyle(f"cell-{font_size}-{row_index == 0}", parent=base, fontSize=font_size, leading=font_size * 1.28)
        prepared.append([paragraph(str(cell), style) for cell in row])
    result = LongTable(prepared, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT", splitByRow=1)
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        commands.extend([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)])
        for row_index in range(1, len(data)):
            if row_index % 2 == 0:
                commands.append(("BACKGROUND", (0, row_index), (-1, row_index), VERY_LIGHT))
    if row_backgrounds:
        for row_index, color in row_backgrounds.items():
            commands.append(("BACKGROUND", (0, row_index), (-1, row_index), color))
    result.setStyle(TableStyle(commands))
    return result


def section(story: list, title: str, intro: str) -> None:
    story.extend([Paragraph(title, H1), Paragraph(intro, BODY)])


def cover(title: str, subtitle: str, callout: str) -> list:
    return [
        Spacer(1, 16 * mm), Paragraph(title, TITLE), Paragraph(subtitle, SUBTITLE),
        HRFlowable(width="100%", thickness=1.4, color=TEAL, spaceAfter=8 * mm),
        Paragraph(callout, ParagraphStyle("CoverCallout", parent=CALLOUT, fontSize=13, leading=19, spaceAfter=8 * mm)),
        data_table([
            ["Сайт", "Регион", "Поисковая система", "Граница"],
            ["okno-msk.ru", "Москва", "Яндекс", "Сохранённые данные; новых внешних обращений нет"],
        ], [68 * mm, 48 * mm, 55 * mm, 94 * mm], font_size=8.5),
        Spacer(1, 7 * mm),
    ]


def build_tree_section(story: list) -> tuple[int, int]:
    by_section: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in HIERARCHY:
        by_section[row["section_name_ru"]].append(row)
    sections = sorted(by_section)
    role_count = 0
    for index, section_name in enumerate(sections):
        branch = sorted(by_section[section_name], key=lambda row: (bool(row["subsection_or_parent_page_key"]), row["target_page_name_ru"]))
        branch_data = []
        for row in branch:
            root = not row["subsection_or_parent_page_key"]
            role = ("● " if root else "↳ ") + display_page_name(row["target_page_name_ru"])
            spec = SPEC_BY_KEY[row["target_page_key"]]
            rec = RECON_BY_KEY[row["target_page_key"]]
            branch_data.append([
                paragraph(role, TREE_ROOT if root else TREE_CHILD), paragraph(row["page_type"], SMALL),
                paragraph(f"{spec['total_routed_phrase_count']} фраз", SMALL), paragraph(spec["analytical_seo_priority"], SMALL),
                paragraph(ACTION_RU[rec["target_action"]], SMALL),
            ])
            role_count += 1
        block = Table(branch_data, colWidths=[91 * mm, 48 * mm, 24 * mm, 22 * mm, 80 * mm], hAlign="LEFT")
        block.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.25, LIGHT_GREY),
            ("BACKGROUND", (0, 0), (-1, 0), PALE_TEAL),
            ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(KeepTogether([Paragraph(section_name, H2), block, Spacer(1, 3 * mm)]))
        if (index + 1) % 3 == 0 and index + 1 < len(sections):
            story.extend([PageBreak(), Paragraph("6. Целевое SEO-дерево — продолжение", H1)])
    return role_count, len(sections)


def build_analytical() -> dict[str, int]:
    doc = make_doc(ANALYTICAL, "OKNO_MSK — целевая SEO-архитектура")
    story: list = cover(
        "Целевая SEO-архитектура okno-msk.ru",
        "Аналитический отчёт · Москва · Яндекс · 10 сентября 2026",
        "Полный результат: запрос и индивидуальный спрос → задача → целевая посадочная → структура → сверка с текущим сайтом → изменение при необходимости.",
    )
    story.extend([
        Paragraph("Детальная рассадка 2 185 рабочих фраз находится в XLSX. Этот отчёт объясняет направления спроса, 60 целевых ролей, их иерархию, ключевые запросы, приоритеты и расхождения с текущим сайтом.", BODY),
        PageBreak(),
    ])

    section(story, "1. Что исследовано", "Семантика собрана в границе существующего публичного сайта, одного региона и спроса Яндекса. Целевая модель построена от пользовательских задач; текущие URL использованы только при последующей сверке.")
    story.extend([
        data_table([
            ["Слой", "Что сделано", "Что получено"],
            ["Спрос", "Сохранены и классифицированы запросы", "2 840 фраз с рабочим, проверочным или исключённым статусом"],
            ["Задачи", "Рабочие запросы сгруппированы по смыслу и посадочной задаче", "161 кластер / задача посадочной"],
            ["Посадочные", "Каждая рабочая фраза получила страницу-владельца или явную границу", "2 185 маршрутов фраз"],
            ["Архитектура", "Роли страниц и отношения зафиксированы до сверки с сайтом", "60 целевых ролей"],
            ["Сверка", "Целевые роли сопоставлены с существующими страницами", "48 сохранить · 7 усилить · 4 изменить связь · 1 перепроверить"],
        ], [42 * mm, 112 * mm, 111 * mm], font_size=8.2),
        Spacer(1, 5 * mm),
        Paragraph("Вордстат указан как индивидуальный сохранённый показатель каждой фразы. Значения разных фраз не суммируются в прогноз трафика или спрос страницы.", BODY),
        PageBreak(),
    ])

    section(story, "2. Область и ограничения", "Результат относится к Москве и Яндексу. Он не расширяет базовую услугу метаданными или исследованиями, которых не было в принятом контуре.")
    story.extend([
        data_table([
            ["Включено", "Не включено", "Как трактовать неопределённость"],
            ["Сохранённая семантика, Вордстат, задачи, целевая структура, текущая сверка, постраничные решения", "Google, Алиса, нейропоиск, новое расширение по конкурентам, прогноз трафика, окупаемость, производственный график", "Недостаток доказательств остаётся явным состоянием проверки; URL, H1 или действие не придумываются"],
        ], [92 * mm, 89 * mm, 84 * mm], font_size=8.3),
        Spacer(1, 5 * mm),
        Paragraph("Аналитический SEO-приоритет показывает важность роли по охвату спроса, центральности, подтверждённому разрыву и неопределённости. Это не срок, не трудоёмкость, не бизнес-ценность и не обещание роста.", BODY),
        PageBreak(),
    ])

    section(story, "3. Семантические итоги", "Счётчики сохранены без косметической мутации данных.")
    story.extend([
        data_table([
            ["Слой", "Количество", "Назначение"],
            ["Семантическая вселенная", "2 840", "Полный сохранённый набор"],
            ["Рабочее ядро", "2 185", "Фразы, участвующие в целевой рассадке"],
            ["Проверить", "187", "Не усиливают решение без дополнительных доказательств"],
            ["Исключено", "468", "Сохранено с причиной исключения"],
            ["Кластеры / задачи", "161", "Задачи посадочных, а не автоматические новые URL"],
            ["Целевые роли", "60", "Полная модель страниц"],
        ], [78 * mm, 30 * mm, 157 * mm], font_size=8.5),
        PageBreak(),
    ])

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in FOUNDATION:
        if row["in_working_core"] == "Да":
            groups[row["group_id"]].append(row)
    top_groups = sorted(groups.values(), key=lambda items: (-len(items), items[0]["group_name"]))[:16]
    section(story, "4. Основные направления спроса", "Крупные смысловые направления помогают оценить ширину спроса. Группа не равна отдельной странице: конечная рассадка сделана по задаче и роли посадочной.")
    demand_data = [["Направление", "Фраз", "Задача пользователя", "Интент", "Сильный пример + Вордстат"]]
    for group in top_groups:
        example = max(group, key=lambda item: int(item["wordstat_popular_count"] or 0))
        demand_data.append([group[0]["group_name"], len(group), group[0]["user_task"], group[0]["intent"], f"{example['phrase']} — {example['wordstat_popular_count']}"])
    story.extend([data_table(demand_data, [48 * mm, 15 * mm, 81 * mm, 47 * mm, 74 * mm], font_size=7.0), PageBreak()])

    route_counts = Counter(row["target_route_state"] for row in CLUSTERS)
    section(story, "5. Кластер / задача → целевая посадочная", "Все 161 задачи имеют самостоятельную страницу, названного владельца или явную границу. Ни одна задача не превращалась в новую страницу автоматически.")
    route_data = [["Решение", "Задач", "Смысл"]]
    route_explanation = {
        "TARGET_PAGE_RESOLVED": "Самостоятельная целевая роль подтверждена.",
        "NO_STANDALONE_ROUTE_TO_PARENT": "Отдельный URL не нужен; тема включается в названную страницу.",
        "RECHECK_NEEDS_EVIDENCE": "Возможная роль требует названного доказательства.",
        "NO_TARGET_OUTSIDE_SCOPE": "Тема сохранена, но находится вне области исследования.",
        "UNRESOLVED_TASK_ROUTING": "Граница задачи не доказана; URL не придуман.",
    }
    for key, count in route_counts.most_common():
        route_data.append([ROUTE_RU[key], count, route_explanation[key]])
    story.extend([data_table(route_data, [103 * mm, 20 * mm, 142 * mm], font_size=8.2), Spacer(1, 5 * mm)])
    examples = sorted(CLUSTERS, key=lambda row: (-int(row["member_phrase_count"]), row["cluster_task_name_ru"]))[:14]
    example_data = [["Кластер / задача", "Фраз", "Посадочная", "Решение"]]
    for row in examples:
        example_data.append([row["cluster_task_name_ru"], row["member_phrase_count"], display_page_name(row["intended_target_page_name_ru"] or "Не назначена"), ROUTE_RU[row["target_route_state"]]])
    story.extend([Paragraph("Крупные маршруты", H2), data_table(example_data, [88 * mm, 14 * mm, 72 * mm, 91 * mm], font_size=7.0), PageBreak()])

    section(story, "6. Целевое SEO-дерево: быстрый обзор", "Ниже — реальная модель из 60 ролей в виде ветвей. Точка означает корневую посадочную раздела; стрелка — дочернюю или поддерживающую роль. Каждая строка показывает охват фраз, аналитический приоритет и итоговое действие.")
    tree_role_count, tree_section_count = build_tree_section(story)
    story.append(PageBreak())

    section(story, "7. Полная модель целевых страниц", "Полный реестр остаётся видимым: для каждой роли показаны родитель, основной запрос с индивидуальным спросом, полезные дополнительные запросы, охват, приоритет и действие.")
    register_data = [["Страница / родитель", "Основной запрос + Вордстат", "Дополнительные запросы + Вордстат", "Фраз", "Приоритет", "Действие"]]
    for row in sorted(SPECS, key=lambda item: (item["parent_section"], item["target_page_name_ru"])):
        register_data.append([
            f"{display_page_name(row['target_page_name_ru'])}\nРодитель: {page_name(row['parent_target_page_key'])}",
            f"{row['primary_representative_query']} — {row['primary_query_wordstat']}", row["secondary_queries_with_wordstat"],
            row["total_routed_phrase_count"], row["analytical_seo_priority"], ACTION_RU[row["target_action"]],
        ])
    story.extend([data_table(register_data, [53 * mm, 50 * mm, 75 * mm, 14 * mm, 20 * mm, 53 * mm], font_size=6.6), PageBreak()])

    section(story, "8. Подробная иерархия", "Таблица служит справочником к дереву и показывает точную связь раздел → родитель → роль без привязки к текущему меню.")
    hierarchy_data = [["Раздел", "Родитель", "Целевая роль", "Уровень", "Тип", "Фраз"]]
    for row in sorted(HIERARCHY, key=lambda item: (item["section_name_ru"], item["subsection_or_parent_name_ru"], item["target_page_name_ru"])):
        hierarchy_data.append([
            row["section_name_ru"], row["subsection_or_parent_name_ru"], display_page_name(row["target_page_name_ru"]),
            "Корневая посадочная" if row["hierarchy_level"] == "SECTION_LANDING_OR_STANDALONE" else "Дочерняя / поддержка",
            row["page_type"], row["member_phrase_count"],
        ])
    story.extend([data_table(hierarchy_data, [45 * mm, 49 * mm, 57 * mm, 38 * mm, 56 * mm, 20 * mm], font_size=6.8), Spacer(1, 4 * mm)])

    section(story, "9. Аналитические SEO-приоритеты", "Приоритеты описывают исследовательскую важность роли и всегда сопровождаются основанием. Они не задают производственный график.")
    priority_counts = Counter(row["analytical_seo_priority"] for row in SPECS)
    story.extend([data_table([
        ["Приоритет", "Страниц", "Как читать"],
        ["Высокий", priority_counts["Высокий"], "Крупная/центральная роль, подтверждённый разрыв или блокирующая неопределённость"],
        ["Средний", priority_counts["Средний"], "Заметная семантическая/структурная роль или подтверждённое изменение меньшего охвата"],
        ["Низкий", priority_counts["Низкий"], "Узкая подтверждённая роль; это не оценка бизнес-ценности"],
    ], [54 * mm, 24 * mm, 187 * mm], font_size=8.3), Spacer(1, 5 * mm)])
    ranked_priority_examples = sorted(SPECS, key=lambda row: ({"Высокий": 0, "Средний": 1, "Низкий": 2}[row["analytical_seo_priority"]], -int(row["total_routed_phrase_count"])))
    priority_examples = ranked_priority_examples[:12]
    recheck_example = next(row for row in SPECS if row["target_action"] == "RECHECK_NEEDS_EVIDENCE")
    if recheck_example not in priority_examples:
        priority_examples.append(recheck_example)
    priority_data = [["Страница", "Приоритет", "Основание"]]
    for row in priority_examples:
        priority_data.append([display_page_name(row["target_page_name_ru"]), row["analytical_seo_priority"], row["analytical_seo_priority_basis"]])
    story.extend([data_table(priority_data, [62 * mm, 24 * mm, 179 * mm], font_size=7.2), PageBreak()])

    section(story, "10. Сверка с текущим сайтом", "После фиксации 60 ролей выполнена отдельная сверка. Нулевая потребность в новых страницах — реальный результат этой сверки, а не заранее заданная цель.")
    action_counts = Counter(row["target_action"] for row in RECON)
    story.extend([data_table([
        ["Решение", "Страниц", "Смысл"],
        [ACTION_RU["KEEP_LOCK_AS_TARGET_OWNER"], action_counts["KEEP_LOCK_AS_TARGET_OWNER"], "Текущая страница подтверждена как владелец роли"],
        [ACTION_RU["OPTIMIZE_STRENGTHEN"], action_counts["OPTIMIZE_STRENGTHEN"], "Роль совпала; требуется содержательное усиление"],
        [ACTION_RU["ROUTE_INTERNAL_LINK_CHANGE"], action_counts["ROUTE_INTERNAL_LINK_CHANGE"], "Роль сохраняется; требуется корректировка связи"],
        [ACTION_RU["RECHECK_NEEDS_EVIDENCE"], action_counts["RECHECK_NEEDS_EVIDENCE"], "Решение открыто до названного доказательства"],
    ], [102 * mm, 20 * mm, 143 * mm], font_size=8.2), Spacer(1, 5 * mm)])
    recon_data = [["Целевая роль", "Текущий URL", "Сверка", "Действие", "Изменение"]]
    keep_examples: list[dict[str, str]] = []
    changed_or_open = sorted([row for row in RECON if row["target_action"] != "KEEP_LOCK_AS_TARGET_OWNER"], key=lambda item: (item["target_action"], item["target_page_name_ru"]))
    for row in keep_examples + changed_or_open:
        recon_data.append([
            display_page_name(row["target_page_name_ru"]), row["accepted_target_url_after_reconciliation"] or "Не назначен",
            MATCH_RU[row["current_match_state"]], ACTION_RU[row["target_action"]], CHANGE_RU[row["real_site_change_required"]],
        ])
    story.extend([data_table(recon_data, [53 * mm, 76 * mm, 52 * mm, 65 * mm, 19 * mm], font_size=6.7), PageBreak()])

    section(story, "11. Физические изменения — подмножество", "14 заданий относятся к 11 изменяемым страницам; ещё одна роль требует аналитической перепроверки. Полный реестр из 60 ролей не сводится к этим заданиям.")
    delta_data = [["Страница", "Готовность", "Что сделать", "Где", "Как принять"]]
    for row in DELTA:
        delta_data.append([display_page_name(row["target_page_name_ru"]), READY_RU[row["readiness_state"]], row["exact_change"], row["exact_location_or_context"], row["acceptance_check"]])
    story.extend([data_table(delta_data, [43 * mm, 37 * mm, 68 * mm, 57 * mm, 60 * mm], font_size=6.6), Spacer(1, 4 * mm)])

    section(story, "12. Где находится полная детализация", "PDF даёт самостоятельное понимание архитектуры; XLSX остаётся точной операционной картой на уровне каждой фразы.")
    story.extend([
        data_table([
            ["Задача", "Где смотреть"],
            ["Найти фразу, Вордстат, кластер, страницу, URL и действие; отсортировать запросы страницы по спросу", "XLSX → «Рассадка запросов»"],
            ["Понять главную задачу и границы страницы", "XLSX → «ТЗ по страницам»; карточки второго PDF — для изменений"],
            ["Увидеть все 60 ролей", "Этот PDF, разделы 6–8; XLSX → «Реестр страниц»"],
            ["Передать физическое изменение", "XLSX → «Изменения сайта»; карточки второго PDF"],
        ], [112 * mm, 153 * mm], font_size=8.0),
    ])
    doc.build(story)
    return {"tree_roles": tree_role_count, "tree_sections": tree_section_count}


def action_color(action: str) -> colors.Color:
    return {
        "KEEP_LOCK_AS_TARGET_OWNER": PALE_GREEN,
        "OPTIMIZE_STRENGTHEN": PALE_AMBER,
        "ROUTE_INTERNAL_LINK_CHANGE": PALE_BLUE,
        "RECHECK_NEEDS_EVIDENCE": PALE_RED,
    }[action]


def detail_pair(label: str, value: str) -> list[Paragraph]:
    return [paragraph(label, CELL_BOLD), paragraph(value, CELL)]


def concise_boundary_explanation(row: dict[str, str]) -> str:
    if row["elsewhere_named_pages"].startswith("Отдельные соседние владельцы"):
        return "Собственное покрытие, встроенные темы и поддержка уже разделены; дополнительное разграничение с соседней страницей не требуется."
    return (
        "Для перечисленных соседних страниц действует единое правило: здесь допустим только обзор и переход, "
        "а полное раскрытие принадлежит названному владельцу. Темы на проверке не входят в собственное покрытие до решения."
    )


def detailed_card(row: dict[str, str], index: int, total: int) -> list:
    action = row["target_action"]
    badge = Table([[paragraph(ACTION_RU[action], BADGE), paragraph(f"Карточка {index} из {total}", BADGE)]], colWidths=[180 * mm, 85 * mm])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), action_color(action)), ("BACKGROUND", (1, 0), (1, 0), VERY_LIGHT),
        ("BOX", (0, 0), (-1, -1), 0.6, LIGHT_GREY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    entries = [
        detail_pair("URL / маршрут", route_text(row["target_url_or_route"])),
        detail_pair("Тип · раздел · родитель", f"{row['page_type']} · {row['parent_section']} · {page_name(row['parent_target_page_key'])}"),
        detail_pair("Главная задача страницы", row["primary_page_job_ru"]),
        detail_pair("Основной запрос", f"{row['primary_representative_query']} — Вордстат {row['primary_query_wordstat']}"),
        detail_pair("Полезные дополнительные запросы", row["secondary_queries_with_wordstat"]),
        detail_pair("Всего распределённых фраз", row["total_routed_phrase_count"]),
        detail_pair("Собственное покрытие", row["own_coverage_clean"]),
        detail_pair("Встроить без отдельного URL", row["embedded_no_standalone_topics"]),
        detail_pair("Только упомянуть / связать", row["support_mention_link_topics"]),
        detail_pair("Отдать названной соседней странице", row["elsewhere_named_pages"]),
        detail_pair("Пояснение границы", concise_boundary_explanation(row)),
        detail_pair("Рекомендуемый H1 / блокер", row["recommended_h1_or_blocker"]),
        detail_pair("Title: направление / статус", row["recommended_title_direction_or_blocker"]),
        detail_pair("Аналитический SEO-приоритет", f"{row['analytical_seo_priority']}. {row['analytical_seo_priority_basis']}"),
        detail_pair("Текущее состояние", row["current_url_match_current_state"]),
        detail_pair("Точное действие", ACTION_RU[action]),
        detail_pair("Базовая деталь внедрения", row["implementation_detail_if_change_is_real"]),
        detail_pair("Целевое состояние / приёмка", row["acceptance_target_end_state"]),
        detail_pair("Уточнение / блокер", row["uncertainty_exact_clarification"]),
    ]
    detail = LongTable(entries, colWidths=[62 * mm, 203 * mm], splitByRow=1)
    detail.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_GREY),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1F5F9")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    blocks: list = [KeepTogether([Paragraph(f"{index}. {display_page_name(row['target_page_name_ru'])}", H1), badge, Spacer(1, 3 * mm)]), detail]
    tickets = DELTA_BY_PAGE.get(row["target_page_key"], [])
    if tickets:
        blocks.extend([Spacer(1, 3 * mm), Paragraph("Физические задания для этой страницы", H2)])
        for ticket_index, ticket in enumerate(tickets, 1):
            task_rows = [
                ["Готовность", READY_RU[ticket["readiness_state"]]], ["Почему", ticket["why_change_is_needed"]],
                ["Что сделать", ticket["exact_change"]], ["Где / в каком контексте", ticket["exact_location_or_context"]],
                ["Что сохранить", ticket["preservation_do_not_break"]], ["Как принять", ticket["acceptance_check"]],
                ["Что уточнить", ticket["one_concrete_clarification"] or "Дополнительное уточнение не требуется"],
            ]
            blocks.extend([Paragraph(f"Задание {ticket_index}", H2), data_table(task_rows, [62 * mm, 203 * mm], header=False, font_size=7.2)])
    else:
        blocks.extend([Spacer(1, 3 * mm), Paragraph("Физическое изменение не назначено до разрешения указанного аналитического блокера.", BODY)])
    return blocks


def build_tz() -> dict[str, int]:
    doc = make_doc(TZ, "OKNO_MSK — постраничное ТЗ")
    action_counts = Counter(row["target_action"] for row in SPECS)
    detailed = sorted([row for row in SPECS if row["target_action"] != "KEEP_LOCK_AS_TARGET_OWNER"], key=lambda row: (row["target_action"], row["target_page_name_ru"]))
    story: list = cover(
        "ТЗ на целевую SEO-структуру и посадочные страницы",
        "Полный реестр + детальные карточки изменений · Москва · Яндекс · 10 сентября 2026",
        "Все 60 целевых ролей остаются видимыми. Детальные карточки сосредоточены на 7 усилениях, 4 изменениях связей и 1 нерешённой роли — без 48 повторяющихся полноформатных страниц «оставить как есть».",
    )
    story.extend([
        data_table([
            ["Всего ролей", "Сохранить", "Усилить", "Изменить связь", "Перепроверить", "Детальных карточек"],
            [len(SPECS), action_counts["KEEP_LOCK_AS_TARGET_OWNER"], action_counts["OPTIMIZE_STRENGTHEN"], action_counts["ROUTE_INTERNAL_LINK_CHANGE"], action_counts["RECHECK_NEEDS_EVIDENCE"], len(detailed)],
        ], [42 * mm, 42 * mm, 42 * mm, 48 * mm, 48 * mm, 43 * mm], font_size=8.7),
        Spacer(1, 6 * mm), Paragraph("Полный список фраз находится в XLSX. Вордстат показывается по каждой фразе отдельно и не складывается в искусственный объём страницы.", BODY), PageBreak(),
    ])

    section(story, "Часть A. Как использовать ТЗ", "Сначала найдите роль в полном реестре. Если действие требует изменения или проверки, перейдите к детальной карточке. Сохранённые страницы остаются доказанными владельцами, но не раздувают документ повторяющимися карточками.")
    story.extend([
        data_table([
            ["Поле", "Как читать"],
            ["Главная задача", "Одна основная ответственность страницы; не объединение разнородных конечных задач"],
            ["Основной / дополнительные запросы", "Индивидуальные показатели Вордстата; полный состав фраз — в XLSX"],
            ["Собственное покрытие", "Темы, которые эта страница раскрывает полностью"],
            ["Встроить", "Совместимые темы без отдельного URL"],
            ["Поддержать / связать", "Краткое упоминание или переход, но не основная ответственность"],
            ["Отдать соседней странице", "Названный владелец полного раскрытия"],
            ["H1 / Title", "H1 обязателен для разрешённой роли; Title-направление требуется для усиления, а для сохранения не навязывается"],
            ["SEO-приоритет", "Аналитическая важность, не порядок разработки, срок, усилие, бизнес-ценность или прогноз"],
        ], [68 * mm, 197 * mm], font_size=8.2),
        Spacer(1, 5 * mm), Paragraph("Готовыми к внедрению считаются только задания с точным изменением, местом/контекстом, ограничениями сохранения и проверкой приёмки. Остальные сначала требуют указанного уточнения.", BODY), PageBreak(),
    ])

    section(story, "Часть B. Полный компактный реестр 60 целевых страниц", "Реестр сохраняет полноту архитектуры: страница, URL/маршрут, тип, основной запрос и спрос, охват, приоритет, действие, текущая сверка и состояние изменения.")
    register = [["Страница", "URL / маршрут", "Тип", "Основной запрос + Вордстат", "Фраз", "Приоритет", "Действие", "Текущая сверка", "Изм."]]
    row_backgrounds = {}
    for index, row in enumerate(sorted(SPECS, key=lambda item: (item["parent_section"], item["target_page_name_ru"])), 1):
        register.append([
            display_page_name(row["target_page_name_ru"]), route_text(row["target_url_or_route"]), row["page_type"],
            f"{row['primary_representative_query']} — {row['primary_query_wordstat']}", row["total_routed_phrase_count"],
            row["analytical_seo_priority"], ACTION_RU[row["target_action"]], clean(row["current_url_match_current_state"]), CHANGE_RU[row["real_site_change_required"]],
        ])
        if row["target_action"] != "KEEP_LOCK_AS_TARGET_OWNER":
            row_backgrounds[index] = action_color(row["target_action"])
    story.extend([data_table(register, [35 * mm, 48 * mm, 31 * mm, 48 * mm, 12 * mm, 18 * mm, 37 * mm, 30 * mm, 10 * mm], font_size=5.9, row_backgrounds=row_backgrounds), PageBreak()])

    section(story, "Часть C. Детальные карточки изменений и решений", "Ниже — только страницы, где требуется усиление, изменение маршрута/связи или дополнительное доказательство. Детальная карточка подтверждённой страницы без изменений не добавляется без реальной исключительной причины.")
    for index, row in enumerate(detailed, 1):
        story.extend(detailed_card(row, index, len(detailed)))
    doc.build(story)
    return {
        "register_rows": len(SPECS), "detailed_cards": len(detailed), "detailed_keep_cards": 0,
        "detailed_optimize_cards": sum(row["target_action"] == "OPTIMIZE_STRENGTHEN" for row in detailed),
        "detailed_route_cards": sum(row["target_action"] == "ROUTE_INTERNAL_LINK_CHANGE" for row in detailed),
        "detailed_recheck_cards": sum(row["target_action"] == "RECHECK_NEEDS_EVIDENCE" for row in detailed),
    }


def file_record(path: Path) -> dict[str, object]:
    return {"file": path.name, "bytes": path.stat().st_size, "sha256": sha256(path), "pages": len(PdfReader(path).pages)}


def main() -> None:
    if len(FOUNDATION) != 2840 or len(PHRASES) != 2185 or len(CLUSTERS) != 161:
        raise SystemExit("semantic count invariant failed")
    if not (len(REGISTRY) == len(HIERARCHY) == len(RECON) == len(SPECS) == 60):
        raise SystemExit("target page authority alignment failed")
    actions = Counter(row["target_action"] for row in SPECS)
    if actions != Counter({"KEEP_LOCK_AS_TARGET_OWNER": 48, "OPTIMIZE_STRENGTHEN": 7, "ROUTE_INTERNAL_LINK_CHANGE": 4, "RECHECK_NEEDS_EVIDENCE": 1}):
        raise SystemExit(f"action invariant failed: {actions}")
    if any("CREATE" in row["target_action"] for row in SPECS):
        raise SystemExit("fake CREATE action detected")
    DELIVERY.mkdir(parents=True, exist_ok=True)
    analytical_qa = build_analytical()
    tz_qa = build_tz()
    report = {
        "schema": "MK02_TARGET_FIRST_MARKET_GRADE_CLIENT_PDFS_V2",
        "date": DATE,
        "status": "PASS",
        "provider_calls": 0,
        "source_authorities": [
            f"TARGET_FIRST_PHRASE_LANDING_MAP_MARKET_GRADE_{DATE}.tsv.gz",
            f"TARGET_PAGE_SPEC_REGISTER_MARKET_GRADE_{DATE}.tsv",
            f"TARGET_ARCHITECTURE_HIERARCHY_{DATE}.tsv",
            f"CURRENT_TARGET_RECONCILIATION_{DATE}.tsv",
            f"CURRENT_TARGET_CHANGE_DELTA_{DATE}.tsv",
        ],
        "source_counts": {
            "semantic_universe": len(FOUNDATION), "working_phrases": len(PHRASES), "cluster_tasks": len(CLUSTERS),
            "target_pages": len(REGISTRY), "page_specs": len(SPECS), "keep": actions["KEEP_LOCK_AS_TARGET_OWNER"],
            "optimize": actions["OPTIMIZE_STRENGTHEN"], "route": actions["ROUTE_INTERNAL_LINK_CHANGE"],
            "recheck": actions["RECHECK_NEEDS_EVIDENCE"], "change_tickets": len(DELTA), "create": 0,
        },
        "analytical_contract": {
            "scannable_tree_marker": "Целевое SEO-дерево: быстрый обзор",
            "tree_role_count": analytical_qa["tree_roles"], "tree_section_count": analytical_qa["tree_sections"],
            "complete_page_model_rows": len(SPECS), "primary_secondary_wordstat_visible": True,
        },
        "tz_contract": tz_qa,
        "no_fixed_pdf_page_count_requirement": True,
        "outputs": [file_record(ANALYTICAL), file_record(TZ)],
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
