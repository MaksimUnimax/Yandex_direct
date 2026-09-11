#!/usr/bin/env python3
"""Build the MK03 Phase-5 client analytical PDF from Level-2 authorities."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


HERE = Path(__file__).resolve().parent
DATE = "2026-09-11"
OUT = HERE / "artifacts" / f"MK03_COMPETITOR_SEMANTIC_GAP_OKNO_MSK_{DATE}.pdf"


def tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2F75B5")
PALE = colors.HexColor("#EAF2F8")
INK = colors.HexColor("#1F2937")
GRAY = colors.HexColor("#64748B")
LINE = colors.HexColor("#D7E0E8")
GREEN = colors.HexColor("#E2F0D9")
AMBER = colors.HexColor("#FFF2CC")
RED = colors.HexColor("#FCE4D6")
WHITE = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleRu", fontName="DejaVu-Bold", fontSize=24, leading=29, textColor=NAVY, spaceAfter=10))
styles.add(ParagraphStyle(name="SubtitleRu", fontName="DejaVu", fontSize=11, leading=16, textColor=GRAY, spaceAfter=12))
styles.add(ParagraphStyle(name="H1Ru", fontName="DejaVu-Bold", fontSize=17, leading=22, textColor=NAVY, spaceBefore=4, spaceAfter=8))
styles.add(ParagraphStyle(name="H2Ru", fontName="DejaVu-Bold", fontSize=12, leading=16, textColor=NAVY, spaceBefore=7, spaceAfter=5))
styles.add(ParagraphStyle(name="BodyRu", fontName="DejaVu", fontSize=9.2, leading=13, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name="SmallRu", fontName="DejaVu", fontSize=7.6, leading=10.2, textColor=INK))
styles.add(ParagraphStyle(name="TinyRu", fontName="DejaVu", fontSize=6.7, leading=8.4, textColor=INK))
styles.add(ParagraphStyle(name="NoteRu", fontName="DejaVu", fontSize=8.2, leading=11.2, textColor=GRAY, backColor=colors.HexColor("#F8FAFC"), borderColor=LINE, borderWidth=.5, borderPadding=6, spaceBefore=4, spaceAfter=7))
styles.add(ParagraphStyle(name="CardTitle", fontName="DejaVu-Bold", fontSize=11.2, leading=14, textColor=NAVY, spaceAfter=3))
styles.add(ParagraphStyle(name="WhiteSmall", fontName="DejaVu-Bold", fontSize=7.4, leading=9, textColor=WHITE, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="CenterSmall", fontName="DejaVu", fontSize=7.5, leading=9.5, textColor=INK, alignment=TA_CENTER))


def p(text: str, style: str = "BodyRu") -> Paragraph:
    safe = (text or "—").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return Paragraph(safe, styles[style])


def state_ru(state: str) -> str:
    return {
        "CONFIRMED_GAP": "Подтверждённый разрыв",
        "ALREADY_COVERED": "Уже покрыто",
        "REJECT_OFF_SCOPE": "Вне предложения",
        "HOLD_EVIDENCE": "Нужны данные",
    }[state]


def state_color(state: str):
    return {"CONFIRMED_GAP": GREEN, "ALREADY_COVERED": PALE, "REJECT_OFF_SCOPE": RED, "HOLD_EVIDENCE": AMBER}[state]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, 13 * mm, 192 * mm, 13 * mm)
    canvas.setFont("DejaVu", 7.2)
    canvas.setFillColor(GRAY)
    canvas.drawString(18 * mm, 8.5 * mm, "MK03 · OKNO_MSK · Москва · Яндекс · 11.09.2026")
    canvas.drawRightString(192 * mm, 8.5 * mm, f"стр. {doc.page}")
    canvas.restoreState()


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.rect(0, 0, 18 * mm, A4[1], fill=1, stroke=0)
    canvas.setFont("DejaVu-Bold", 11)
    canvas.setFillColor(colors.HexColor("#B9D8F1"))
    canvas.drawString(28 * mm, 256 * mm, "MK03 · АНАЛИТИЧЕСКИЙ ОТЧЁТ")
    canvas.setFont("DejaVu-Bold", 25)
    canvas.setFillColor(WHITE)
    canvas.drawString(28 * mm, 224 * mm, "Семантические разрывы")
    canvas.drawString(28 * mm, 212 * mm, "относительно конкурентов")
    canvas.setFont("DejaVu", 12)
    canvas.setFillColor(colors.HexColor("#DCEAF5"))
    canvas.drawString(28 * mm, 194 * mm, "OKNO_MSK · Москва · Яндекс")
    canvas.setFillColor(colors.HexColor("#233F5A"))
    canvas.roundRect(28 * mm, 116 * mm, 154 * mm, 50 * mm, 4 * mm, fill=1, stroke=0)
    metrics = [("7", "подтверждено"), ("23", "уже покрыто"), ("3", "вне предложения"), ("10", "нужны данные")]
    x = 36 * mm
    for num, label in metrics:
        canvas.setFillColor(WHITE)
        canvas.setFont("DejaVu-Bold", 21)
        canvas.drawCentredString(x + 16 * mm, 143 * mm, num)
        canvas.setFillColor(colors.HexColor("#C6DAE9"))
        canvas.setFont("DejaVu", 7.5)
        canvas.drawCentredString(x + 16 * mm, 133 * mm, label)
        x += 36 * mm
    canvas.setFont("DejaVu", 9)
    canvas.setFillColor(colors.HexColor("#B9D8F1"))
    canvas.drawString(28 * mm, 44 * mm, "Сохранённые доказательства · новых вызовов провайдеров: 0")
    canvas.drawString(28 * mm, 36 * mm, "Подтверждённый разрыв не является решением о создании страницы")
    canvas.restoreState()


OUT.parent.mkdir(parents=True, exist_ok=True)
doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=17 * mm, bottomMargin=18 * mm, title="MK03 — Семантические разрывы относительно конкурентов", author="Kwork / Yandex Marketing Bridge")
normal_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
cover_frame = Frame(0, 0, A4[0], A4[1], id="cover")
doc.addPageTemplates([PageTemplate(id="cover", frames=[cover_frame], onPage=draw_cover), PageTemplate(id="body", frames=[normal_frame], onPage=footer)])

gaps = tsv(f"MK03_GAP_DECISION_REGISTER_{DATE}.tsv")
opps = tsv(f"MK03_BOUNDED_OPPORTUNITY_REGISTER_{DATE}.tsv")
domains = [r for r in tsv(f"MK03_COMPETITOR_DISCOVERY_REGISTER_{DATE}.tsv") if r["accepted_actual_competitor"] == "YES"]
pages = tsv(f"MK03_COMPETITOR_PAGE_EVIDENCE_{DATE}.tsv")
wordstat = tsv(f"MK03_WORDSTAT_EVIDENCE_MANIFEST_{DATE}.tsv")
matrix = tsv(f"MK03_EXACT_QUERY_COMPETITOR_SEARCH_MATRIX_{DATE}.tsv")
site = tsv(f"MK03_CURRENT_SITE_COVERAGE_{DATE}.tsv")

page_count_by_domain = Counter(r["competitor_domain"] for r in pages)
page_type_counts = Counter(r["page_type"] for r in pages)

story = [Spacer(1, 255 * mm), NextPageTemplate("body"), PageBreak()]
story += [p("Главный вывод", "H1Ru")]
story += [p("Из 43 уникальных направлений, обнаруженных на страницах фактических конкурентов, 7 выдержали всю цепочку доказательств: реальный Wordstat‑спрос, достаточная точечная выдача, соответствие предложению OKNO_MSK и отсутствие точного/близкого активного покрытия. Ещё 23 направления уже закрыты текущей семантикой, 3 выходят за подтверждённый бизнес‑scope, а 10 честно оставлены на проверку.")]
summary_data = [[p("Состояние", "WhiteSmall"), p("Направлений", "WhiteSmall"), p("Что это значит", "WhiteSmall")],
                [p("Подтверждённый разрыв", "SmallRu"), 7, p("Есть достаточная цепочка доказательств; можно обсуждать ограниченное контентное расширение.", "SmallRu")],
                [p("Уже покрыто", "SmallRu"), 23, p("Конкурентная формулировка не создаёт новую семантическую возможность.", "SmallRu")],
                [p("Вне предложения", "SmallRu"), 3, p("Нет подтверждённого основания включать тему в продукт OKNO_MSK.", "SmallRu")],
                [p("Нужны данные", "SmallRu"), 10, p("Не хватает спроса, выдачи либо бизнес‑подтверждения; решение не придумано.", "SmallRu")]]
tbl = Table(summary_data, colWidths=[42 * mm, 25 * mm, 103 * mm], repeatRows=1)
tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE), ("GRID", (0, 0), (-1, -1), .35, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 1), (-1, 1), GREEN), ("BACKGROUND", (0, 2), (-1, 2), PALE), ("BACKGROUND", (0, 3), (-1, 3), RED), ("BACKGROUND", (0, 4), (-1, 4), AMBER), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
story += [tbl, Spacer(1, 6 * mm), p("Что можно делать дальше", "H2Ru"), p("Для 7 подтверждённых направлений — проверить бизнес‑факты и выбрать существующего владельца темы или формат контента. Отдельный URL, новая страница, сроки, трудозатраты, ROI и прогноз роста этим исследованием не определяются."), p("Полная построчная детализация находится в XLSX: 43 направления, 14 Wordstat‑проверок, 81 точная пара запрос × домен, 44 страницы конкурентов и журнал текущего сайта.", "NoteRu")]

story += [PageBreak(), p("Что именно исследовалось", "H1Ru"), p("Объект: публичный сайт okno-msk.ru. Регион: Москва, код Яндекса 213. Поисковая система: Яндекс. Использован режим выборочной подтверждающей выдачи: точечно проверялись только материальные направления после Wordstat и семантической сверки.")]
funnel = [
    ("75", "discovery‑запросов", "750 сохранённых строк TOP‑10"),
    ("237", "наблюдавшихся доменов", "9 фактических сопоставимых конкурентов"),
    ("44", "прочитанные страницы", "92 наблюдения → 43 уникальных направления"),
    ("14", "Wordstat‑проверок", "160 реально возвращённых строк"),
    ("9", "точечных запросов", "7 получено, 2 результата неизвестны"),
]
for num, label, note in funnel:
    box = Table([[p(num, "CardTitle"), p(label, "CardTitle"), p(note, "SmallRu")]], colWidths=[18 * mm, 54 * mm, 98 * mm])
    box.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), NAVY), ("TEXTCOLOR", (0, 0), (0, 0), WHITE), ("BACKGROUND", (1, 0), (-1, 0), colors.HexColor("#F8FAFC")), ("BOX", (0, 0), (-1, -1), .6, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    story += [box, Spacer(1, 2.5 * mm)]
story += [p("Почему нет новых запросов к провайдерам", "H2Ru"), p("Канонический Phase‑5 prompt требовал сначала использовать уже сохранённую доказательную цепочку. Она полностью покрывала rehearsal: повторные платные/провайдерские вызовы не были разрешены и не были нужны. Новые вызовы Search, Wordstat и других провайдеров: 0."), p("Критическая граница", "H2Ru"), p("Тема на странице конкурента не считается её ранжированием. Seed не считается принятой фразой. Wordstat‑частота не подтверждает соответствие бизнесу. Подтверждённый gap не считается указанием создать страницу.", "NoteRu")]

story += [PageBreak(), p("Фактические конкуренты", "H1Ru"), p("Конкуренты отобраны не по памяти и не по брендовому списку, а из сохранённой выдачи: сопоставимый оконный бизнес плюс наблюдаемая видимость по 75 discovery‑запросам.")]
comp_data = [[p("Домен", "WhiteSmall"), p("TOP‑10", "WhiteSmall"), p("Запросов", "WhiteSmall"), p("Лучшая", "WhiteSmall"), p("Страниц", "WhiteSmall")]]
for row in domains:
    comp_data.append([p(row["domain"], "SmallRu"), int(row["top10_appearances"]), int(row["distinct_tested_queries"]), int(row["best_observed_rank"]), page_count_by_domain[row["domain"]]])
tbl = Table(comp_data, colWidths=[65 * mm, 25 * mm, 28 * mm, 24 * mm, 28 * mm], repeatRows=1)
tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE), ("GRID", (0, 0), (-1, -1), .35, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 1), (-1, -1), "CENTER"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
story += [tbl, Spacer(1, 6 * mm), p("Какие страницы были прочитаны", "H2Ru")]
type_ru = {"ARTICLE_GUIDE":"статьи/руководства", "COMMERCIAL_CATEGORY":"коммерческие категории", "COMMERCIAL_LANDING":"коммерческие посадочные", "COMMERCIAL_PRODUCT":"товарные страницы", "COMMERCIAL_SERVICE":"страницы услуг", "COMPARISON_SELECTION":"сравнение/выбор", "HOME_OR_HUB":"главные/хабы", "MIXED_COMMERCIAL_INFORMATIONAL":"смешанные", "PORTFOLIO_GALLERY":"портфолио", "PRICE_FINANCE":"цены/финансирование"}
type_text = "; ".join(f"{type_ru[k]} — {v}" for k, v in sorted(page_type_counts.items()))
story += [p(type_text + "."), p("Все 44 страницы были доступны: 43 напрямую и 1 после перенаправления. Наблюдались заголовки, рубрики, товарно‑сервисные оси, сценарии использования, проблемы/решения, цена/калькулятор, процесс, FAQ и элементы доверия. Эти наблюдения не являются трафиковыми или позиционными метриками.", "NoteRu")]

story += [PageBreak(), p("Что уже покрыто текущим сайтом", "H1Ru"), p("Два сохранённых набора текущих наблюдений дали 62 строки доказательств: 48 проверок роли URL и 14 проверок содержания. Это журнал наблюдений, а не 62 уникальные страницы."), p("Эти 23 направления — положительный результат gap‑анализа: они показывают, где конкурентная формулировка не требует расширять семантику. Это предотвращает дублирование работы и ложное раздувание рекомендаций.", "NoteRu")]
covered = [r for r in gaps if r["terminal_state"] == "ALREADY_COVERED"]
mid = (len(covered) + 1) // 2
left, right = covered[:mid], covered[mid:]
covered_data = [[p("Направления 1–12", "WhiteSmall"), p("Направления 13–23", "WhiteSmall")]]
for index in range(mid):
    covered_data.append([p(left[index]["candidate_direction"], "SmallRu"), p(right[index]["candidate_direction"], "SmallRu") if index < len(right) else ""])
tbl = Table(covered_data, colWidths=[85 * mm, 85 * mm], repeatRows=1)
tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), .3, LINE), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5)]))
story += [tbl]

story += [PageBreak(), p("Подтверждённые возможности", "H1Ru"), p("Ниже — полный реестр 7 направлений. Частота относится к каждой показанной фразе отдельно; значения не суммируются в вымышленный «спрос страницы».")]
opp_overview = [[p("Направление", "WhiteSmall"), p("Главная фраза", "WhiteSmall"), p("Wordstat", "WhiteSmall"), p("В выдаче из 9", "WhiteSmall"), p("Внимание", "WhiteSmall")]]
for row in opps:
    visible = row["selected_competitor_exact_query_visibility"]
    if visible.startswith("Не наблюдались"):
        visible = "0 из 9"
    else:
        visible = f"{len([x for x in visible.split(' | ') if x])} из 9"
    opp_overview.append([p(row["representative_query"], "SmallRu"), p(row["representative_query"], "SmallRu"), int(row["individual_wordstat"]), p(visible, "CenterSmall"), p({"HIGH":"Высокое", "MEDIUM":"Среднее", "LOW":"Низкое"}[row["analytical_attention"]], "CenterSmall")])
tbl = Table(opp_overview, colWidths=[50 * mm, 60 * mm, 20 * mm, 22 * mm, 22 * mm], repeatRows=1)
tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), .35, LINE), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GREEN]), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (2, 1), (-1, -1), "CENTER"), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
story += [tbl, p("Как читать «аналитическое внимание»", "H2Ru"), p("Это порядок внимания аналитика к силе и широте доказательств. Он не равен плану внедрения, трудозатратам, бизнес‑ценности, ROI или ожидаемому росту.", "NoteRu")]

for index, row in enumerate(opps, 1):
    if index in {1, 3, 5, 7}:
        story += [PageBreak(), p(f"Возможность {index} из 7", "H1Ru")]
    card_data = [
        [p(row["representative_query"], "CardTitle"), p(f"Wordstat: {row['individual_wordstat']}", "CardTitle")],
        [p("Фразы", "SmallRu"), p(row["accepted_phrases_with_individual_wordstat"], "SmallRu")],
        [p("Точная выдача", "SmallRu"), p(row["selected_competitor_exact_query_visibility"], "SmallRu")],
        [p("Почему важно", "SmallRu"), p(row["attention_basis"], "SmallRu")],
        [p("Ограниченная возможность", "SmallRu"), p(row["bounded_opportunity"], "SmallRu")],
        [p("Сохранить границы", "SmallRu"), p(row["preservation_constraints"], "SmallRu")],
        [p("До выбора URL", "SmallRu"), p(row["required_owner_validation"], "SmallRu")],
        [p("Решение о новой странице", "SmallRu"), p("Не принято", "SmallRu")],
    ]
    card = Table(card_data, colWidths=[46 * mm, 124 * mm])
    card.setStyle(TableStyle([("SPAN", (0, 0), (0, 0)), ("BACKGROUND", (0, 0), (-1, 0), PALE), ("BOX", (0, 0), (-1, -1), .7, BLUE), ("INNERGRID", (0, 1), (-1, -1), .3, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#F8FAFC")), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5)]))
    story += [KeepTogether([card, Spacer(1, 6 * mm)])]

story += [PageBreak(), p("Что осталось на проверку", "H1Ru"), p("10 направлений не были повышены до gap. Причина всегда названа: пустой ответ Wordstat, неизвестный результат точечной выдачи или неподтверждённый бизнес/ассортимент.")]
holds = [r for r in gaps if r["terminal_state"] == "HOLD_EVIDENCE"]
hold_data = [[p("Направление", "WhiteSmall"), p("Что известно", "WhiteSmall"), p("Что нужно закрыть", "WhiteSmall")]]
for row in holds:
    known = "Есть сигнал Wordstat; выдача не получена." if row["search_evidence_state"] == "OUTCOME_UNKNOWN" else ("Wordstat вернул пустой объект — это неизвестность, не ноль." if row["wordstat_evidence_state"] == "EMPTY_RESULT_UNKNOWN_NOT_ZERO" else "Есть тема на странице конкурента, но не подтверждён бизнес‑факт/ассортимент.")
    next_check = "Отдельно разрешённая повторная точная проверка выдачи." if row["search_evidence_state"] == "OUTCOME_UNKNOWN" else ("Новая отдельно разрешённая проверка спроса." if row["wordstat_evidence_state"] == "EMPTY_RESULT_UNKNOWN_NOT_ZERO" else "Подтверждение владельца бизнеса.")
    hold_data.append([p(row["candidate_direction"], "SmallRu"), p(known, "SmallRu"), p(next_check, "SmallRu")])
tbl = Table(hold_data, colWidths=[55 * mm, 66 * mm, 49 * mm], repeatRows=1)
tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), .35, LINE), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, AMBER]), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
story += [tbl, p("Три направления вне предложения", "H2Ru")]
for row in [r for r in gaps if r["terminal_state"] == "REJECT_OFF_SCOPE"]:
    story += [p(f"• {row['candidate_direction']} — нет подтверждённого основания считать это самостоятельным предложением OKNO_MSK.")]

story += [PageBreak(), p("Точечная выдача: что доказано", "H1Ru"), p("Для 9 материальных направлений была сформирована матрица из 81 пары: один точный запрос × один из 9 выбранных конкурентов. По 7 запросам выдача получена — 63 пары действительно проверены. Для 2 запросов результат неизвестен — 18 пар не считаются проверенными.")]
visible_rows = [r for r in matrix if r["visibility_state"] == "OBSERVED_IN_TOP10"]
vis_by_query: dict[str, list[str]] = defaultdict(list)
for row in visible_rows:
    vis_by_query[row["tested_query"]].append(f"{row['selected_competitor_domain']} (позиция {row['best_observed_rank']})")
search_data = [[p("Точный запрос", "WhiteSmall"), p("Получен", "WhiteSmall"), p("Выбранные конкуренты в одном TOP‑10", "WhiteSmall")]]
for query in sorted({r["tested_query"] for r in matrix}):
    qrows = [r for r in matrix if r["tested_query"] == query]
    succeeded = qrows[0]["search_acquisition_state"] == "SUCCEEDED"
    search_data.append([p(query, "SmallRu"), p("Да" if succeeded else "Нет: результат неизвестен", "CenterSmall"), p("; ".join(vis_by_query.get(query, [])) if succeeded and vis_by_query.get(query) else ("Не наблюдались среди 9" if succeeded else "Пары не тестировались"), "SmallRu")])
tbl = Table(search_data, colWidths=[62 * mm, 34 * mm, 74 * mm], repeatRows=1)
tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), .35, LINE), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
story += [tbl, p("Правильная интерпретация", "H2Ru"), p("«Не наблюдался» означает только отсутствие выбранного домена в одном сохранённом TOP‑10 по одному точному запросу. Это не доказательство отсутствия видимости домена по всему направлению и не оценка доли рынка.", "NoteRu")]

story += [PageBreak(), p("Ограничения и следующий шаг", "H1Ru")]
limitations = [
    ("Не полное ядро", "MK03 не заменяет полный сбор семантики, кластеризацию или карту релевантности."),
    ("Не архитектура", "Отчёт не назначает URL, не решает split/merge и не создаёт страницы."),
    ("Не SEO‑прогноз", "Нет расчёта трафика, ROI, business value или ожидаемого uplift."),
    ("Не полный рынок", "Конкурентный набор ограничен сохранёнными 75 discovery‑запросами и регионом Москва."),
    ("Не универсальная выдача", "Точечный режим покрывает только явно протестированные запросы и домены."),
    ("Не подтверждение ассортимента", "Наблюдение у конкурента не доказывает наличие услуги/товара у OKNO_MSK."),
]
lim_data = [[p("Граница", "WhiteSmall"), p("Что это означает", "WhiteSmall")]] + [[p(a, "SmallRu"), p(b, "SmallRu")] for a, b in limitations]
tbl = Table(lim_data, colWidths=[45 * mm, 125 * mm], repeatRows=1)
tbl.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), NAVY), ("GRID", (0, 0), (-1, -1), .35, LINE), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F8FAFC")]), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
story += [tbl, Spacer(1, 6 * mm), p("Рекомендуемый следующий шаг", "H2Ru"), p("Провести владельческую проверку 7 подтверждённых возможностей: подтвердить фактическое предложение, технические заявления и существующего владельца темы. Только после этого можно решать — встроить тему в текущую страницу, оформить отдельный материал или оставить без внедрения."), p("Где смотреть детали", "H2Ru"), p("XLSX содержит полный фильтруемый 43‑строчный gap‑реестр, индивидуальные Wordstat‑значения, все 9 конкурентов, 44 страницы, 75 discovery‑запросов, точечную матрицу 81 пара и 62 строки текущих наблюдений.", "NoteRu")]

doc.build(story)
print(OUT)
