#!/usr/bin/env python3
"""Build the corrected target-first analytical and page-specification PDFs."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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
ROOT = Path(__file__).resolve().parent
DELIVERY = ROOT / "CLIENT_DELIVERY_PHASE_7_TARGET_FIRST_CORRECTED_2026-09-10"
ANALYTICAL = DELIVERY / f"TARGET_SEO_ARCHITECTURE_REPORT_OKNO_MSK_{DATE}.pdf"
TZ = DELIVERY / f"TARGET_PAGE_SPECIFICATION_TZ_OKNO_MSK_{DATE}.pdf"
REPORT = ROOT / f"TARGET_FIRST_CLIENT_PDF_BUILD_REPORT_{DATE}.json"

NAVY = colors.HexColor("#17365D")
TEAL = colors.HexColor("#0F6B78")
PALE_BLUE = colors.HexColor("#EAF3F8")
PALE_TEAL = colors.HexColor("#E6F3F3")
PALE_GREEN = colors.HexColor("#E8F5EC")
PALE_AMBER = colors.HexColor("#FFF3D6")
PALE_RED = colors.HexColor("#FCE8E6")
GREY = colors.HexColor("#5B6573")
LIGHT_GREY = colors.HexColor("#D7DEE7")

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))


def rows(name: str, gz: bool = False) -> list[dict[str, str]]:
    opener = gzip.open if gz else open
    with opener(ROOT / name, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


FOUNDATION = rows(f"MK02_SEMANTIC_FOUNDATION_{DATE}.tsv.gz", True)
PHRASES = rows(f"TARGET_FIRST_PHRASE_LANDING_MAP_{DATE}.tsv.gz", True)
CLUSTERS = rows(f"TARGET_FIRST_CLUSTER_LANDING_MAP_{DATE}.tsv")
REGISTRY = rows(f"TARGET_PAGE_REGISTRY_{DATE}.tsv")
HIERARCHY = rows(f"TARGET_ARCHITECTURE_HIERARCHY_{DATE}.tsv")
RECON = rows(f"CURRENT_TARGET_RECONCILIATION_{DATE}.tsv")
SPECS = rows(f"TARGET_PAGE_SPEC_REGISTER_{DATE}.tsv")
DELTA = rows(f"CURRENT_TARGET_CHANGE_DELTA_{DATE}.tsv")
PAGE_NAME_BY_KEY = {row["target_page_key"]: row["target_page_name_ru"] for row in REGISTRY}
CLUSTER_NAME_BY_KEY = {row["cluster_task_key"]: row["cluster_task_name_ru"] for row in CLUSTERS}


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
    "TARGET_PAGE_RESOLVED": "Целевая посадочная определена",
    "NO_STANDALONE_ROUTE_TO_PARENT": "Отдельная страница не нужна — направить в названного владельца",
    "RECHECK_NEEDS_EVIDENCE": "Нужна дополнительная проверка",
    "NO_TARGET_OUTSIDE_SCOPE": "Вне целевой области проекта",
    "UNRESOLVED_TASK_ROUTING": "Маршрут не определён — доказательств недостаточно",
}
CHANGE_RU = {"YES": "Да", "NO": "Нет", "UNRESOLVED": "Не определено"}
READY_RU = {
    "READY_IMPLEMENTATION_SPEC": "Готово к внедрению",
    "PENDING_BUSINESS_DETAIL": "Нужно бизнес-уточнение",
    "PENDING_PLACEMENT_OR_CONTEXT": "Нужно точное место или контекст",
}


def clean(value: str | None) -> str:
    text = str(value or "").strip()
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
    mapped = ACTION_RU.get(text) or MATCH_RU.get(text) or ROUTE_RU.get(text) or CHANGE_RU.get(text) or READY_RU.get(text) or text
    for source, target in replacements.items():
        mapped = mapped.replace(source, target)
    return mapped


def names_from_keys(value: str | None, mapping: dict[str, str], empty_value: str = "Нет") -> str:
    keys = [key.strip() for key in str(value or "").split(";") if key.strip()]
    if not keys:
        return empty_value
    return "; ".join(
        mapping.get(key, "Вне целевой области проекта" if key == "NO_TARGET_OUTSIDE_SCOPE" else "Неназванная роль — требуется проверка")
        for key in keys
    )


def page_name(key: str | None, empty_value: str = "Корень раздела") -> str:
    if not key:
        return empty_value
    return PAGE_NAME_BY_KEY.get(key, "Вне целевой области проекта" if key == "NO_TARGET_OUTSIDE_SCOPE" else "Неназванная роль — требуется проверка")


def route_text(value: str | None) -> str:
    raw = str(value or "").strip()
    if raw.startswith("TARGET_ROLE::"):
        key = raw.removeprefix("TARGET_ROLE::")
        if key in PAGE_NAME_BY_KEY and key != "TP-UNRESOLVED-DIY-WINDOW-TASK":
            return f"Целевая роль «{PAGE_NAME_BY_KEY[key]}»"
        return "Маршрут не назначен до получения недостающего доказательства"
    return raw or "Не назначен до проверки"


def p(text: str | None, style: ParagraphStyle) -> Paragraph:
    normalized = clean(text).replace("; ", ";<br/>")
    return Paragraph(escape(normalized).replace("&lt;br/&gt;", "<br/>"), style)


styles = getSampleStyleSheet()
TITLE = ParagraphStyle("TitleRu", parent=styles["Title"], fontName="DejaVu-Bold", fontSize=22, leading=27, textColor=NAVY, spaceAfter=8 * mm)
SUBTITLE = ParagraphStyle("SubtitleRu", parent=styles["Normal"], fontName="DejaVu", fontSize=11, leading=15, textColor=GREY, spaceAfter=5 * mm)
H1 = ParagraphStyle("H1Ru", parent=styles["Heading1"], fontName="DejaVu-Bold", fontSize=16, leading=20, textColor=NAVY, spaceBefore=2 * mm, spaceAfter=4 * mm)
H2 = ParagraphStyle("H2Ru", parent=styles["Heading2"], fontName="DejaVu-Bold", fontSize=12, leading=15, textColor=TEAL, spaceBefore=3 * mm, spaceAfter=2 * mm)
BODY = ParagraphStyle("BodyRu", parent=styles["BodyText"], fontName="DejaVu", fontSize=9.2, leading=13, textColor=colors.HexColor("#1F2937"), spaceAfter=2.5 * mm)
SMALL = ParagraphStyle("SmallRu", parent=BODY, fontSize=7.4, leading=9.5, spaceAfter=0)
SMALL_BOLD = ParagraphStyle("SmallBoldRu", parent=SMALL, fontName="DejaVu-Bold")
CELL = ParagraphStyle("CellRu", parent=BODY, fontSize=7.6, leading=9.7, spaceAfter=0)
CELL_BOLD = ParagraphStyle("CellBoldRu", parent=CELL, fontName="DejaVu-Bold")
CALLOUT = ParagraphStyle("CalloutRu", parent=BODY, fontName="DejaVu-Bold", fontSize=10, leading=14, textColor=NAVY, alignment=TA_CENTER)
PAGE_TITLE = ParagraphStyle("PageTitleRu", parent=H1, fontSize=15, leading=18, spaceAfter=3 * mm)
BADGE = ParagraphStyle("BadgeRu", parent=SMALL_BOLD, alignment=TA_CENTER, textColor=NAVY)


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
        topMargin=13 * mm, bottomMargin=16 * mm,
        title=short_title, author="OKNO_MSK",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates(PageTemplate(id="landscape", frames=[frame], onPage=lambda c, d: footer(c, d, short_title)))
    return doc


def table(data, widths, *, header=True, font_size=7.4, row_backgrounds: dict[int, colors.Color] | None = None) -> LongTable:
    prepared = []
    for row_index, row in enumerate(data):
        style = CELL_BOLD if header and row_index == 0 else CELL
        if font_size != CELL.fontSize:
            style = ParagraphStyle(f"cell{font_size}{row_index == 0}", parent=style, fontSize=font_size, leading=font_size * 1.28)
        prepared.append([p(str(cell), style) for cell in row])
    result = LongTable(prepared, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT", splitByRow=1)
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_GREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        commands += [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
        for row_index in range(1, len(data)):
            if row_index % 2 == 0:
                commands.append(("BACKGROUND", (0, row_index), (-1, row_index), colors.HexColor("#F7F9FC")))
    if row_backgrounds:
        for row_index, color in row_backgrounds.items():
            commands.append(("BACKGROUND", (0, row_index), (-1, row_index), color))
    result.setStyle(TableStyle(commands))
    return result


def section_title(story: list, title: str, intro: str) -> None:
    story.append(Paragraph(title, H1))
    story.append(Paragraph(intro, BODY))


def build_analytical() -> None:
    doc = make_doc(ANALYTICAL, "OKNO_MSK — целевая SEO-архитектура")
    story: list = [
        Spacer(1, 18 * mm),
        Paragraph("Целевая SEO-архитектура OKNO_MSK", TITLE),
        Paragraph("Аналитический отчёт · Москва · Яндекс · 10 сентября 2026", SUBTITLE),
        HRFlowable(width="100%", thickness=1.4, color=TEAL, spaceAfter=8 * mm),
        Paragraph("Главный результат — не количество физических правок, а полная модель: запрос → задача → целевая посадочная → структура → спецификация страницы → изменение при необходимости.", ParagraphStyle("CoverCallout", parent=CALLOUT, fontSize=14, leading=20, spaceAfter=9 * mm)),
        table([
            ["Объект", "Сайт", "Регион и поиск", "Граница данных"],
            ["Семантическое ядро и целевая структура", "okno-msk.ru", "Москва · Яндекс", "Принятые сохранённые данные; без новых обращений к внешним сервисам"],
        ], [55 * mm, 65 * mm, 55 * mm, 88 * mm], font_size=8.5),
        Spacer(1, 8 * mm),
        Paragraph("Фразовая детализация находится в XLSX. Этот PDF работает на уровне задач, страниц, ролей, структуры и действий.", BODY),
        PageBreak(),
    ]

    section_title(story, "1. Как построена целевая модель", "Целевая роль выводилась из принятой семантики, пользовательской задачи, интента и ожидаемой роли страницы. Текущие URL сопоставлены только после фиксации этой модели.")
    flow = Table([
        [p("1. Принятая семантика", CALLOUT), p("2. Задачи и интенты", CALLOUT), p("3. Целевые роли страниц", CALLOUT), p("4. Сверка с текущим сайтом", CALLOUT)],
        [p("2 185 рабочих фраз", SMALL), p("161 задача посадочных страниц", SMALL), p("60 существенных ролей страниц", SMALL), p("Закрепить / усилить / изменить связь / перепроверить", SMALL)],
    ], colWidths=[doc.width / 4] * 4, rowHeights=[20 * mm, 13 * mm])
    flow.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALE_TEAL), ("GRID", (0, 0), (-1, -1), 0.6, TEAL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story += [flow, Spacer(1, 6 * mm), Paragraph("Критическая граница: существующая страница может идеально совпасть с независимо спроектированной ролью. Тогда она получает действие «Сохранить и закрепить как целевую посадочную» и остаётся полноценной строкой результата.", BODY), PageBreak()]

    section_title(story, "2. Объём семантики и ограничения", "Принятые ранее количества сохранены без косметического пересчёта. Спорные и исключённые строки не включались в рабочую архитектуру и не были потеряны.")
    count_table = [
        ["Слой", "Количество", "Роль в результате"],
        ["Семантическая вселенная", "2 840", "Полный сохранённый набор"],
        ["Рабочее ядро", "2 185", "Фразы с целевым маршрутом либо явным состоянием «отдельная страница не нужна» / «нужна проверка»"],
        ["Требуют проверки", "187", "Не усиливают целевые решения без дополнительных доказательств"],
        ["Исключены", "468", "Сохранены с причиной исключения"],
    ]
    story += [table(count_table, [70 * mm, 30 * mm, 160 * mm], font_size=8.5), Spacer(1, 5 * mm)]
    story.append(Paragraph("Граница: расширение семантики из источников конкурентов, Google, Алисы и нейропоиска не использовано; новые обращения к Вордстату, поиску Яндекса и поставщикам конкурентных данных не выполнялись. Если доказательств недостаточно, сохранено состояние «нужна проверка».", BODY))
    story.append(PageBreak())

    groups = defaultdict(list)
    for row in FOUNDATION:
        if row["in_working_core"] == "Да":
            groups[row["group_id"]].append(row)
    top_groups = sorted(groups.values(), key=lambda rs: (-len(rs), rs[0]["group_name"]))[:18]
    section_title(story, "3. Основные направления спроса", "Рабочие фразы объединены по пользовательской задаче. Смысловая группа помогает увидеть спрос, но сама по себе не является новой страницей.")
    demand_data = [["Направление", "Фраз", "Задача пользователя", "Интент", "Пример запроса"]]
    for rs in top_groups:
        representative = sorted(rs, key=lambda x: (-int(x["wordstat_popular_count"] or 0), x["phrase"]))[0]
        demand_data.append([rs[0]["group_name"], str(len(rs)), rs[0]["user_task"], rs[0]["intent"], representative["phrase"]])
    story += [table(demand_data, [48 * mm, 15 * mm, 83 * mm, 48 * mm, 70 * mm], font_size=7.2), PageBreak()]

    route_counts = Counter(r["target_route_state"] for r in CLUSTERS)
    section_title(story, "4. Как задачи сгруппированы в посадочные", "161 задача получила целевую роль, названную родительскую страницу или явное состояние неопределённости. Искусственного правила «один кластер = одна страница» нет.")
    route_data = [["Решение для задачи", "Задач", "Смысл"]]
    explanations = {
        "TARGET_PAGE_RESOLVED": "Самостоятельная целевая роль определена.",
        "NO_STANDALONE_ROUTE_TO_PARENT": "Отдельный URL не нужен; спрос включён в названную страницу-владельца.",
        "RECHECK_NEEDS_EVIDENCE": "Роль возможна, но недостаёт конкретного доказательства.",
        "NO_TARGET_OUTSIDE_SCOPE": "Задача сохранена, но находится вне целевой области этого исследования.",
        "UNRESOLVED_TASK_ROUTING": "Даже task boundary недостаточно доказана; URL не придуман.",
    }
    for key, count in route_counts.most_common():
        route_data.append([ROUTE_RU[key], str(count), explanations[key]])
    story += [table(route_data, [100 * mm, 20 * mm, 145 * mm], font_size=8.2), Spacer(1, 5 * mm)]
    examples = sorted(CLUSTERS, key=lambda r: (-int(r["member_phrase_count"]), r["cluster_task_name_ru"]))[:12]
    example_data = [["Кластер / задача", "Фраз", "Целевая посадочная", "Решение"]]
    for row in examples:
        example_data.append([row["cluster_task_name_ru"], row["member_phrase_count"], row["intended_target_page_name_ru"] or "Не назначена", ROUTE_RU[row["target_route_state"]]])
    story += [Paragraph("Примеры «кластер → посадочная»", H2), table(example_data, [88 * mm, 14 * mm, 76 * mm, 87 * mm], font_size=7.2), PageBreak()]

    section_title(story, "5. Карта целевых посадочных страниц", "Полный реестр включает все 60 существенных ролей — в том числе страницы без физического изменения. Текущий URL не участвовал в выводе самой роли.")
    pages_by_section = defaultdict(list)
    for row in REGISTRY:
        pages_by_section[row["parent_section_name_ru"]].append(row)
    for section_index, (section, page_rows) in enumerate(sorted(pages_by_section.items())):
        story.append(Paragraph(section, H2))
        data = [["Целевая страница", "Тип", "Фраз", "Представительный запрос", "Назначение"]]
        for row in sorted(page_rows, key=lambda r: r["target_page_name_ru"]):
            data.append([row["target_page_name_ru"], row["page_type"], row["member_phrase_count"], row["primary_representative_query"], row["page_purpose"]])
        story.append(table(data, [48 * mm, 38 * mm, 13 * mm, 63 * mm, 103 * mm], font_size=6.8))
        story.append(Spacer(1, 4 * mm))
        if section_index % 2 == 1:
            story.append(PageBreak())
    story.append(PageBreak())

    section_title(story, "6. Целевая SEO-структура", "Иерархия ниже читается без текущего сайта: раздел → родитель / подраздел → целевая страница → дочерние или поддерживающие роли.")
    hierarchy_data = [["Раздел", "Родитель / подраздел", "Целевая страница", "Уровень", "Фраз", "Поддерживающие роли"]]
    for row in sorted(HIERARCHY, key=lambda r: (r["section_name_ru"], r["subsection_or_parent_name_ru"], r["target_page_name_ru"])):
        hierarchy_data.append([row["section_name_ru"], row["subsection_or_parent_name_ru"], row["target_page_name_ru"], "Посадочная" if row["hierarchy_level"] == "SECTION_LANDING_OR_STANDALONE" else "Дочерняя / поддержка", row["member_phrase_count"], names_from_keys(row["child_supporting_target_page_keys"], PAGE_NAME_BY_KEY)])
    story += [table(hierarchy_data, [39 * mm, 47 * mm, 51 * mm, 32 * mm, 12 * mm, 84 * mm], font_size=6.6), PageBreak()]

    section_title(story, "7. Сверка целевой модели с текущим сайтом", "После фиксации ролей страниц выполнена отдельная сверка. Отсутствие новых страниц не означает отсутствие продукта: 48 существующих страниц получили подтверждённое целевое владение.")
    action_counts = Counter(r["target_action"] for r in RECON)
    action_data = [["Действие", "Страниц", "Интерпретация"]]
    interpretation = {
        "KEEP_LOCK_AS_TARGET_OWNER": "Существующая страница подтверждена как правильная целевая посадочная для закреплённого спроса.",
        "OPTIMIZE_STRENGTHEN": "Текущий URL подходит роли, но требует указанного усиления.",
        "ROUTE_INTERNAL_LINK_CHANGE": "Роль страницы сохраняется; меняется связь или маршрут.",
        "RECHECK_NEEDS_EVIDENCE": "Решение не выдумано; нужно названное доказательство.",
    }
    for key in ["KEEP_LOCK_AS_TARGET_OWNER", "OPTIMIZE_STRENGTHEN", "ROUTE_INTERNAL_LINK_CHANGE", "RECHECK_NEEDS_EVIDENCE"]:
        action_data.append([ACTION_RU[key], str(action_counts[key]), interpretation[key]])
    story += [table(action_data, [100 * mm, 20 * mm, 145 * mm], font_size=8.2), Spacer(1, 5 * mm)]
    recon_data = [["Целевая страница", "Сверка", "Принятый URL", "Действие", "Изменение"]]
    for row in sorted(RECON, key=lambda r: (r["target_action"], r["target_page_name_ru"])):
        recon_data.append([row["target_page_name_ru"], MATCH_RU[row["current_match_state"]], row["accepted_target_url_after_reconciliation"] or "Не назначен", ACTION_RU[row["target_action"]], CHANGE_RU[row["real_site_change_required"]]])
    story += [table(recon_data, [52 * mm, 58 * mm, 75 * mm, 65 * mm, 16 * mm], font_size=6.8), PageBreak()]

    section_title(story, "8. Что реально меняется", "14 заданий — это подмножество 60 постраничных спецификаций. Они не заменяют реестр целевых страниц.")
    delta_data = [["Страница", "Готовность", "Действие", "Что сделать", "Как принять"]]
    for row in DELTA:
        delta_data.append([row["target_page_name_ru"], READY_RU[row["readiness_state"]], ACTION_RU[row["target_action"]], row["exact_change"], row["acceptance_check"]])
    story += [table(delta_data, [43 * mm, 38 * mm, 50 * mm, 72 * mm, 63 * mm], font_size=6.8), PageBreak()]

    section_title(story, "9. Как использовать результат", "XLSX — операционная карта; этот PDF — человекочитаемая модель; второй PDF — полное постраничное ТЗ.")
    story += [table([
        ["Задача", "Где смотреть"],
        ["Найти целевую посадочную для случайной рабочей фразы", "XLSX → «Рассадка запросов»"],
        ["Понять, почему кластер направлен на страницу", "XLSX → «Посадочные страницы»"],
        ["Увидеть полную иерархию", "Этот PDF, раздел 6; XLSX → «Целевая структура»"],
        ["Понять роль существующей страницы без изменений", "XLSX → «Реестр страниц» и «ТЗ по страницам»"],
        ["Передать готовую физическую правку", "XLSX → «Изменения сайта»; второй PDF → соответствующая страница"],
    ], [105 * mm, 160 * mm], font_size=8.5), Spacer(1, 6 * mm)]
    story.append(Paragraph("Ограничение интерпретации: нулевая потребность в новой странице не является заранее заданным результатом. Она получена после самостоятельного проектирования ролей и сверки с сохранённым текущим сайтом. Для неразрешённых случаев сохранены точная причина и следующий шаг проверки.", BODY))
    doc.build(story)


def action_color(action: str) -> colors.Color:
    return {
        "KEEP_LOCK_AS_TARGET_OWNER": PALE_GREEN,
        "OPTIMIZE_STRENGTHEN": PALE_AMBER,
        "ROUTE_INTERNAL_LINK_CHANGE": PALE_BLUE,
        "RECHECK_NEEDS_EVIDENCE": PALE_RED,
    }[action]


def spec_block(row: dict[str, str], index: int) -> list:
    action = row["target_action"]
    title = f"{index}. {row['target_page_name_ru']}"
    summary = Table([
        [p(ACTION_RU[action], BADGE), p(f"Нужно менять сайт: {CHANGE_RU[row['real_site_change_required']]}", BADGE), p(f"Страница {index} из {len(SPECS)}", BADGE)],
    ], colWidths=[105 * mm, 75 * mm, 85 * mm])
    summary.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), action_color(action)),
        ("BACKGROUND", (1, 0), (2, 0), colors.HexColor("#F3F5F8")),
        ("BOX", (0, 0), (-1, -1), 0.6, LIGHT_GREY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    entries = [
        ("URL или маршрут", route_text(row["target_url_or_route"])),
        ("Тип / раздел / родитель", f"{row['page_type']} · {row['parent_section']} · {page_name(row['parent_target_page_key']).lower() if not row['parent_target_page_key'] else page_name(row['parent_target_page_key'])}"),
        ("Назначение страницы", row["page_purpose"]),
        ("Главная задача / интент", row["primary_user_task_intent"]),
        ("Представительный запрос / объём", f"{row['primary_representative_query']} · {row['member_phrase_count']} фраз"),
        ("Семантическая область", names_from_keys(row["semantic_scope_cluster_keys"], CLUSTER_NAME_BY_KEY)),
        ("Что страница должна раскрывать", row["what_page_should_cover"]),
        ("Что относится в другое место / не требует отдельной страницы", row["what_belongs_elsewhere_or_not_standalone"]),
        ("Дочерние, поддерживающие и связанные страницы", row["supporting_child_related_pages"] or "Существенные связи не требуются"),
        ("Текущее соответствие", row["current_url_match_current_state"]),
        ("Целевое действие", ACTION_RU[action]),
        ("Деталь внедрения", row["implementation_detail_if_change_is_real"]),
        ("Целевое состояние и приёмка", row["acceptance_target_end_state"]),
        ("Неопределённость / точное уточнение", row["uncertainty_exact_clarification"]),
    ]
    detail_data = [[p(label, CELL_BOLD), p(value, CELL)] for label, value in entries]
    detail = LongTable(detail_data, colWidths=[62 * mm, 203 * mm], repeatRows=0, splitByRow=1)
    detail.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_GREY),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1F5F9")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return [Paragraph(title, PAGE_TITLE), summary, Spacer(1, 3 * mm), detail]


def build_tz() -> None:
    doc = make_doc(TZ, "OKNO_MSK — постраничное ТЗ")
    action_counts = Counter(r["target_action"] for r in SPECS)
    story: list = [
        Spacer(1, 16 * mm),
        Paragraph("ТЗ на целевую SEO-структуру и посадочные страницы", TITLE),
        Paragraph("Полная постраничная спецификация OKNO_MSK · Москва · Яндекс · 10 сентября 2026", SUBTITLE),
        HRFlowable(width="100%", thickness=1.4, color=TEAL, spaceAfter=7 * mm),
        Paragraph("В документе присутствуют все существенные целевые роли. Страницы без физической правки не скрыты: для них закреплена конкретная семантическая и структурная функция.", ParagraphStyle("TzCoverCallout", parent=CALLOUT, fontSize=13, leading=18, spaceAfter=7 * mm)),
        table([
            ["Всего спецификаций", "Сохранить владельцем", "Усилить", "Изменить связь", "Перепроверить"],
            [str(len(SPECS)), str(action_counts["KEEP_LOCK_AS_TARGET_OWNER"]), str(action_counts["OPTIMIZE_STRENGTHEN"]), str(action_counts["ROUTE_INTERNAL_LINK_CHANGE"]), str(action_counts["RECHECK_NEEDS_EVIDENCE"])],
        ], [53 * mm] * 5, font_size=9),
        Spacer(1, 7 * mm),
        Paragraph("Физические задания на изменения — подмножество этого документа. Полная фразовая рассадка находится в XLSX и связывается с ТЗ по названию целевой страницы.", BODY),
        PageBreak(),
        Paragraph("Как читать спецификацию", H1),
        table([
            ["Поле", "Как интерпретировать"],
            ["Целевая роль", "Выведена из семантики и задачи пользователя до сверки с текущим сайтом."],
            ["Текущее соответствие", "Показывает, нашлась ли после этого подходящая существующая страница."],
            ["Сохранить владельцем", "Страница уже соответствует роли; это подтверждённая часть результата, а не пропуск работы."],
            ["Усилить / изменить связь", "Реальное изменение выполняется только в указанной границе и принимается по целевому состоянию."],
            ["Перепроверить", "URL или действие не придуманы; указано одно конкретное недостающее доказательство."],
        ], [70 * mm, 195 * mm], font_size=8.8),
        PageBreak(),
    ]
    sorted_specs = sorted(SPECS, key=lambda r: (r["parent_section"], r["target_page_name_ru"]))
    for index, row in enumerate(sorted_specs, start=1):
        story.extend(spec_block(row, index))
        if index != len(sorted_specs):
            story.append(PageBreak())
    doc.build(story)


def file_record(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    reader = PdfReader(path)
    return {"file": path.name, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest(), "pages": len(reader.pages)}


def main() -> None:
    if len(FOUNDATION) != 2840 or len(PHRASES) != 2185:
        raise SystemExit("semantic count invariant failed")
    if not (len(REGISTRY) == len(HIERARCHY) == len(RECON) == len(SPECS)):
        raise SystemExit("target page authority alignment failed")
    DELIVERY.mkdir(parents=True, exist_ok=True)
    build_analytical()
    build_tz()
    report = {
        "schema": "MK02_TARGET_FIRST_CLIENT_PDFS_V1",
        "date": DATE,
        "status": "PASS",
        "source_counts": {
            "semantic_universe": len(FOUNDATION), "working_phrases": len(PHRASES),
            "cluster_tasks": len(CLUSTERS), "target_pages": len(REGISTRY),
            "page_specs": len(SPECS), "change_tickets": len(DELTA),
        },
        "outputs": [file_record(ANALYTICAL), file_record(TZ)],
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
