#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const here = path.dirname(fileURLToPath(import.meta.url));
const date = "2026-09-11";
const outDir = path.join(here, "artifacts");
const renderDir = path.join(here, "qa", "xlsx_rendered");
const outPath = path.join(outDir, `MK03_COMPETITOR_SEMANTIC_GAP_OKNO_MSK_${date}.xlsx`);

function parseTsv(text) {
  const rows = [];
  let row = [], field = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (ch === '"') quoted = false;
      else field += ch;
    } else if (ch === '"' && field.length === 0) quoted = true;
    else if (ch === "\t") { row.push(field); field = ""; }
    else if (ch === "\n") { row.push(field.replace(/\r$/, "")); rows.push(row); row = []; field = ""; }
    else field += ch;
  }
  if (field.length || row.length) { row.push(field.replace(/\r$/, "")); rows.push(row); }
  const headers = rows.shift();
  return rows.filter(r => r.some(Boolean)).map(r => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ""])));
}

async function load(name) {
  return parseTsv(await fs.readFile(path.join(here, name), "utf8"));
}

const stateRu = {
  CONFIRMED_GAP: "Подтверждённый разрыв",
  ALREADY_COVERED: "Уже покрыто",
  REJECT_OFF_SCOPE: "Вне подтверждённого предложения",
  HOLD_EVIDENCE: "Нужны данные",
};
const searchRu = {
  SUCCEEDED: "Проверено: выдача получена",
  OUTCOME_UNKNOWN: "Результат проверки неизвестен",
  NOT_REQUIRED_OR_NOT_RUN: "Точечная проверка не требовалась",
  PRESERVED_DISCOVERY_EXACT_Q62: "Есть сохранённая точная discovery‑проверка",
};
const pageTypeRu = {
  ARTICLE_GUIDE: "Статья / руководство",
  COMMERCIAL_CATEGORY: "Коммерческая категория",
  COMMERCIAL_LANDING: "Коммерческая посадочная",
  COMMERCIAL_PRODUCT: "Товарная страница",
  COMMERCIAL_SERVICE: "Страница услуги",
  COMPARISON_SELECTION: "Сравнение / выбор",
  HOME_OR_HUB: "Главная / хаб",
  MIXED_COMMERCIAL_INFORMATIONAL: "Коммерческо‑информационная",
  PORTFOLIO_GALLERY: "Портфолио / галерея",
  PRICE_FINANCE: "Цена / финансирование",
};
const directionRu = {
  OPEN_BALCONY_WATERPROOFING: "Гидроизоляция открытого балкона",
  SUN_PROTECTION_GLASS_UNIT: "Солнцезащитный стеклопакет",
  MULTIFUNCTIONAL_GLASS_UNIT: "Многофункциональный стеклопакет",
  IMPACT_RESISTANT_GLASS_UNIT: "Ударопрочный стеклопакет",
  OLD_HOUSING_WINDOWS: "Окна для старого фонда",
  BALCONY_AS_OFFICE: "Балкон как кабинет",
  BALCONY_AS_STORAGE: "Балкон как кладовая",
  BALCONY_ROOF_SOUNDPROOFING: "Шумоизоляция крыши балкона",
  WINDOW_PROFILE_REINFORCEMENT: "Армирование оконного профиля",
};
function scopeRu(v) {
  if (v.startsWith("IN_SCOPE")) return "В подтверждённой или смежной теме";
  if (v.includes("OUTSIDE_SCOPE")) return "Вне предмета сайта";
  if (v.includes("NO_STANDALONE")) return "Нет подтверждения самостоятельного предложения";
  if (v.includes("HOLD")) return "Нужно подтверждение бизнеса";
  return "Граница требует чтения исходного доказательства";
}
function coverageRu(v) {
  if (v.includes("ALREADY_COVERED")) return "Есть точное или близкое активное покрытие";
  if (v.includes("NO_EXACT_OR_CLOSE")) return "Точного или близкого активного направления не найдено";
  if (v.includes("CLOSE_PARENT") || v.includes("PARENT_DIRECTION")) return "Есть только родительская тема";
  if (v.includes("NO_ACCEPTED")) return "Нет подтверждённого бизнес‑основания";
  return "Проверено по сохранённой семантической модели";
}
function intentRu(v) {
  if (v.includes("OUTSIDE")) return "Вне предмета сайта";
  if (v.includes("COMMERCIAL") || v === "SERVICE") return "Коммерческий / заказ услуги";
  if (v.includes("INFO")) return "Информационный / выбор";
  return "Смешанный";
}
function resultTypeRu(v) {
  if (/MARKETPLACE|ECOMMERCE|SECOND_HAND/.test(v)) return "Маркетплейсы / товарные страницы";
  if (/COMMERCIAL|SERVICE|PRODUCT|PRICE|FINANCE/.test(v)) return "Коммерческие услуги / товары";
  if (/GUIDE|ARTICLE|INFORMATION|VIDEO/.test(v)) return "Статьи / инструкции";
  return "Смешанный состав результатов";
}
const yesNo = v => String(v).toLowerCase() === "true" ? "Да" : "Нет";
const numberOrBlank = v => v === "" ? null : Number(v);

const gaps = await load(`MK03_GAP_DECISION_REGISTER_${date}.tsv`);
const opportunities = await load(`MK03_BOUNDED_OPPORTUNITY_REGISTER_${date}.tsv`);
const domains = (await load(`MK03_COMPETITOR_DISCOVERY_REGISTER_${date}.tsv`)).filter(r => r.accepted_actual_competitor === "YES");
const pages = await load(`MK03_COMPETITOR_PAGE_EVIDENCE_${date}.tsv`);
const queries = await load(`MK03_DISCOVERY_QUERY_FAMILY_AUTHORITY_${date}.tsv`);
const wordstat = await load(`MK03_WORDSTAT_EVIDENCE_MANIFEST_${date}.tsv`);
const matrix = await load(`MK03_EXACT_QUERY_COMPETITOR_SEARCH_MATRIX_${date}.tsv`);
const site = await load(`MK03_CURRENT_SITE_COVERAGE_${date}.tsv`);

await fs.mkdir(outDir, { recursive: true });
await fs.mkdir(renderDir, { recursive: true });

const wb = Workbook.create();
const FONT = "Arial";
const COLORS = {
  navy: "#17324D", blue: "#2F75B5", paleBlue: "#EAF2F8", ink: "#1F2937",
  gray: "#64748B", line: "#D7E0E8", green: "#E2F0D9", amber: "#FFF2CC",
  red: "#FCE4D6", white: "#FFFFFF", paper: "#F8FAFC",
};

function colName(index) {
  let n = index + 1, s = "";
  while (n) { n--; s = String.fromCharCode(65 + n % 26) + s; n = Math.floor(n / 26); }
  return s;
}

function addTitle(sheet, title, subtitle, width) {
  sheet.showGridLines = false;
  sheet.getRangeByIndexes(0, 0, 1, width).format.fill = COLORS.paper;
  sheet.getRange("A1").values = [[title]];
  sheet.getRange("A1").format.font = { name: FONT, size: 15, bold: true, color: COLORS.navy };
  sheet.getRange("A2").values = [[subtitle]];
  sheet.getRangeByIndexes(1, 0, 1, width).format.font = { name: FONT, size: 10, italic: true, color: COLORS.gray };
  sheet.getRangeByIndexes(2, 0, 1, width).format.borders = { bottom: { style: "thin", color: COLORS.blue } };
}

function addTableSheet({name, title, subtitle, headers, rows, widths, tableName, freezeCols = 1, statusColumn = -1, numericColumns = []}) {
  const sheet = wb.worksheets.add(name);
  addTitle(sheet, title, subtitle, headers.length);
  const matrixRows = [headers, ...rows];
  const tableRange = sheet.getRangeByIndexes(3, 0, matrixRows.length, headers.length);
  tableRange.values = matrixRows;
  tableRange.format.font = { name: FONT, size: 10, color: COLORS.ink };
  tableRange.format.verticalAlignment = "top";
  tableRange.format.wrapText = true;
  sheet.getRangeByIndexes(3, 0, 1, headers.length).format = {
    fill: COLORS.navy,
    font: { name: FONT, size: 10, bold: true, color: COLORS.white },
    horizontalAlignment: "center",
    verticalAlignment: "center",
    wrapText: true,
    borders: { insideVertical: { style: "thin", color: COLORS.white } },
  };
  const table = sheet.tables.add(`A4:${colName(headers.length - 1)}${matrixRows.length + 3}`, true, tableName);
  table.style = "TableStyleMedium2";
  table.showFilterButton = true;
  sheet.freezePanes.freezeRows(4);
  if (freezeCols) sheet.freezePanes.freezeColumns(freezeCols);
  widths.forEach((w, i) => { sheet.getRangeByIndexes(0, i, matrixRows.length + 3, 1).format.columnWidth = w; });
  numericColumns.forEach(i => {
    if (rows.length) sheet.getRangeByIndexes(4, i, rows.length, 1).format.numberFormat = "0";
  });
  if (statusColumn >= 0 && rows.length) {
    const statusRange = sheet.getRangeByIndexes(4, statusColumn, rows.length, 1);
    statusRange.conditionalFormats.add("containsText", { text: "Подтверждённый", format: { fill: COLORS.green, font: { bold: true, color: "#215E21" } } });
    statusRange.conditionalFormats.add("containsText", { text: "Уже покрыто", format: { fill: COLORS.paleBlue, font: { color: COLORS.navy } } });
    statusRange.conditionalFormats.add("containsText", { text: "Нужны данные", format: { fill: COLORS.amber, font: { bold: true, color: "#7F6000" } } });
    statusRange.conditionalFormats.add("containsText", { text: "Вне", format: { fill: COLORS.red, font: { color: "#9C0006" } } });
  }
  return sheet;
}

const start = wb.worksheets.add("Начните здесь");
addTitle(start, "MK03 · Семантические разрывы относительно конкурентов", "OKNO_MSK · Москва · Яндекс · сохранённые данные на 11.09.2026", 10);
start.getRange("A5:D5").values = [["Подтверждено", "Уже покрыто", "Вне предложения", "Нужны данные"]];
start.getRange("A6:D6").values = [[7, 23, 3, 10]];
start.getRange("A5:D5").format = { fill: COLORS.navy, font: { name: FONT, size: 10, bold: true, color: COLORS.white }, horizontalAlignment: "center" };
start.getRange("A6:D6").format = { fill: COLORS.paleBlue, font: { name: FONT, size: 15, bold: true, color: COLORS.navy }, horizontalAlignment: "center", rowHeight: 30 };
start.getRange("A9:B15").values = [
  ["Что внутри", "Как использовать"],
  ["Разрывы", "Полный реестр 43 направлений: фильтруйте по итоговому состоянию."],
  ["Возможности", "7 подтверждённых направлений с частотами, границами и следующей проверкой."],
  ["Конкуренты", "9 фактических сопоставимых доменов из сохранённой выдачи."],
  ["Страницы конкурентов", "44 наблюдения по страницам; тема страницы не означает ранжирование по каждому запросу."],
  ["Проверка выдачи", "Только 9 точечных запросов × 9 доменов; 7 запросов получены, 2 результата неизвестны."],
  ["Метод и ограничения", "Границы выводов и правила интерпретации."],
];
start.getRange("A9:B9").format = { fill: COLORS.navy, font: { name: FONT, size: 10, bold: true, color: COLORS.white } };
start.getRange("A9:B15").format.wrapText = true;
start.getRange("A9:B15").format.font = { name: FONT, size: 10, color: COLORS.ink };
start.getRange("A18:B23").values = [
  ["Ключевое ограничение", "Эта работа находит подтверждённые направления, но не принимает решение о создании страницы."],
  ["Wordstat", "Показаны индивидуальные частоты отдельных фраз. totalCount не считается суммой спроса страницы."],
  ["Выдача", "Отсутствие домена означает только: не наблюдался в одном сохранённом TOP‑10 по точному запросу."],
  ["Приоритет", "Аналитическое внимание не равно сроку, трудозатратам, бизнес-ценности или прогнозу роста."],
  ["Новые вызовы", "0 — использованы только сохранённые доказательства."],
  ["Следующий шаг", "Подтвердить бизнес-факты и владельца темы до выбора URL или формата контента."],
];
start.getRange("A18:A23").format = { fill: COLORS.paleBlue, font: { name: FONT, size: 10, bold: true, color: COLORS.navy } };
start.getRange("A18:B23").format.wrapText = true;
start.getRange("A18:B23").format.font = { name: FONT, size: 10, color: COLORS.ink };
start.getRange("A:D").format.columnWidth = 24;
start.getRange("B:B").format.columnWidth = 70;
start.getRange("A1:J30").format.verticalAlignment = "top";
start.tabColor = COLORS.navy;

addTableSheet({
  name: "Разрывы", title: "Все 43 направления", subtitle: "Одна строка = одно дедуплицированное направление; сортируйте по состоянию, спросу и типу доказательства.",
  headers: ["Направление", "Тема", "Конкуренты‑источники", "Текущее покрытие", "Wordstat‑состояние", "totalCount seed", "Проверочный запрос", "Индивид. Wordstat", "Важные фразы и Wordstat", "Проверка выдачи", "Кого увидели", "Итог", "Почему", "Что ещё проверить"],
  rows: gaps.map(r => [r.candidate_direction, r.semantic_axis, r.competitor_domains, coverageRu(r.current_coverage_evidence), r.wordstat_evidence_state === "EMPTY_RESULT_UNKNOWN_NOT_ZERO" ? "Пустой ответ: неизвестно, не ноль" : r.wordstat_evidence_state === "TOTALCOUNT_ONLY" ? "Только totalCount, без списка фраз" : r.wordstat_evidence_state === "ROW_LEVEL_RESULTS" ? "Есть построчные данные" : "Wordstat не требовался", numberOrBlank(r.wordstat_seed_total_count), r.representative_query, numberOrBlank(r.representative_query_individual_wordstat), r.accepted_phrases_with_individual_wordstat || r.held_phrases_with_individual_wordstat, searchRu[r.search_evidence_state] || "Точечная проверка не требовалась", r.selected_competitors_visible || "—", stateRu[r.terminal_state], r.terminal_state === "CONFIRMED_GAP" ? "Есть построчный спрос Wordstat, получена точечная выдача, направление находится в scope, а точного или близкого активного покрытия нет." : r.terminal_state === "ALREADY_COVERED" ? "В сохранённой семантике уже есть точное или близкое активное направление: формулировка конкурента не образует новый разрыв." : r.terminal_state === "REJECT_OFF_SCOPE" ? "Направление выходит за подтверждённое предложение OKNO_MSK; возможность не выдаётся." : r.search_evidence_state === "OUTCOME_UNKNOWN" ? "Есть сигнал спроса, но результат точечной проверки выдачи неизвестен; решение удержано." : "Доказательств недостаточно либо не подтверждён бизнес‑факт/ассортимент; разрыв и действие по странице не заявляются.", r.terminal_state === "CONFIRMED_GAP" ? "Подтвердить бизнес‑факт и владельца темы до выбора URL или формата." : r.terminal_state === "ALREADY_COVERED" ? "Сохранять текущее покрытие; дополнительная проверка для классификации не нужна." : r.terminal_state === "REJECT_OFF_SCOPE" ? "Действий в границах MK03 нет." : r.search_evidence_state === "OUTCOME_UNKNOWN" ? "Требуется отдельно разрешённая повторная проверка точной выдачи." : "Отдельно закрыть недостающее доказательство спроса, выдачи или бизнес‑факта."]),
  widths: [28, 20, 30, 25, 24, 12, 30, 14, 55, 25, 28, 24, 55, 45], tableName: "GapRegister", freezeCols: 2, statusColumn: 11, numericColumns: [5,7]
});

addTableSheet({
  name: "Возможности", title: "7 подтверждённых возможностей", subtitle: "Только подтверждённые разрывы. Формулировки ограничены доказательствами и не предрешают отдельный URL.",
  headers: ["Тема", "Проверочный запрос", "Индивид. Wordstat", "Принятые фразы с Wordstat", "Конкуренты в точном TOP‑10", "Аналитическое внимание", "Основание", "Ограниченная возможность", "Что нельзя потерять", "Что подтвердить у владельца", "Решение о новой странице"],
  rows: opportunities.map(r => [directionRu[r.direction_id] || r.representative_query, r.representative_query, Number(r.individual_wordstat), r.accepted_phrases_with_individual_wordstat, r.selected_competitor_exact_query_visibility, r.analytical_attention === "HIGH" ? "Высокое" : r.analytical_attention === "MEDIUM" ? "Среднее" : "Низкое", r.attention_basis, r.bounded_opportunity, r.preservation_constraints, r.required_owner_validation, "Не принято"]),
  widths: [26, 30, 14, 58, 33, 18, 45, 55, 55, 50, 22], tableName: "OpportunityRegister", freezeCols: 2, numericColumns: [2]
});

addTableSheet({
  name: "Конкуренты", title: "9 фактических конкурентов для сопоставления", subtitle: "Отобраны по сопоставимости бизнеса и видимости в сохранённом наборе из 75 discovery‑запросов.",
  headers: ["Домен", "Появлений в TOP‑10", "Различных запросов", "Лучшая позиция", "Основные запросы", "Примеры URL", "Почему выбран", "Граница вывода"],
  rows: domains.map(r => [r.domain, Number(r.top10_appearances), Number(r.distinct_tested_queries), Number(r.best_observed_rank), r.representative_queries, r.representative_urls, `Сопоставимый оконный бизнес: ${r.top10_appearances} появлений по ${r.distinct_tested_queries} запросам, лучшая позиция ${r.best_observed_rank}.`, "Только сохранённые 75 запросов; не рыночный рейтинг всех конкурентов."]),
  widths: [25, 14, 16, 13, 55, 65, 55, 42], tableName: "CompetitorRegister", freezeCols: 1, numericColumns: [1,2,3]
});

addTableSheet({
  name: "Страницы конкурентов", title: "44 наблюдения по страницам конкурентов", subtitle: "Фиксируется содержимое страницы. Наличие темы на странице не доказывает её ранжирование по любому запросу.",
  headers: ["Домен", "URL", "Тип страницы", "Title", "H1", "Основные темы", "Коммерческие элементы", "Продукты / услуги", "Сценарии", "Проблемы / решения", "Цена / калькулятор", "Примеры работ", "Процесс монтажа", "FAQ", "Доверие / доказательства", "Заметка"],
  rows: pages.map(r => [r.competitor_domain, r.final_url, pageTypeRu[r.page_type] || r.page_type, r.page_title, r.h1, r.material_h2_h3_topics, r.material_commercial_axes, r.material_product_service_axes, r.material_use_case_axes, r.material_problem_solution_axes, yesNo(r.price_or_calculator_presence), yesNo(r.portfolio_or_examples_presence), yesNo(r.installation_process_presence), yesNo(r.faq_presence), yesNo(r.trust_or_proof_elements_presence), r.page_evidence_notes]),
  widths: [23, 55, 24, 45, 35, 60, 40, 42, 38, 42, 14, 14, 14, 10, 18, 55], tableName: "CompetitorPages", freezeCols: 2
});

addTableSheet({
  name: "Запросы discovery", title: "75 discovery‑запросов", subtitle: "Сохранённая выборка для поиска реальных сопоставимых конкурентов; каждая строка относится только к точному запросу.",
  headers: ["Запрос", "Семейство задачи", "Пользовательская задача", "Интент", "Граница бизнеса", "Что преобладало в выдаче", "Тип результатов", "TOP‑3 домены", "TOP‑10 домены"],
  rows: queries.map(r => [r.query, r.canonical_user_task, r.canonical_user_task, intentRu(r.intent), scopeRu(r.business_scope_state), r.canonical_user_task, resultTypeRu(r.dominant_result_type), r.top3_domains, r.top10_domains]),
  widths: [34, 28, 48, 20, 25, 34, 28, 50, 75], tableName: "DiscoveryQueries", freezeCols: 1
});

addTableSheet({
  name: "Wordstat", title: "14 сохранённых Wordstat‑проверок", subtitle: "Пустой ответ — это неизвестность, а не нулевая частота. totalCount не заменяет построчный список фраз.",
  headers: ["Seed", "Смысловая ось", "Форма ответа", "totalCount", "Строк фраз", "Ассоциаций", "Пустой ответ", "Регион", "Конкуренты‑источники", "Наблюдение на странице", "Как использовано", "Ограничение"],
  rows: wordstat.map(r => [r.seed_text, r.semantic_axis, r.provider_result_shape === "EMPTY_PROVIDER_RESULT" ? "Пустой ответ — неизвестно" : r.provider_result_shape === "TOTALCOUNT_ONLY" ? "Только totalCount" : "Фразы + ассоциации + totalCount", numberOrBlank(r.total_count), Number(r.direct_results_rows), Number(r.association_rows), yesNo(r.empty_result_flag), Number(r.region), r.competitor_domains, r.page_observed_evidence, r.seed_reconciliation_route === "ROW_LEVEL_RECONCILIATION" ? "Построчная сверка" : r.seed_reconciliation_route.startsWith("HOLD") ? "Оставлено на проверку" : "Есть прежняя точная проверка; повтор не нужен", r.evidence_limitation_note.replace("Only explicitly returned results/associations are authoritative; totalCount is not a row inventory.", "Авторитетны только реально возвращённые строки; totalCount не является перечнем фраз.").replace("Provider returned result={}; no numeric zero and no phrase rows may be inferred.", "Провайдер вернул пустой объект: нельзя выводить нулевую частоту или придумывать строки.").replace("Provider supplied totalCount only; no phrase-level results or associations may be invented.", "Получен только totalCount: нельзя придумывать фразы или ассоциации.")]),
  widths: [34, 26, 25, 12, 12, 12, 12, 10, 35, 70, 30, 55], tableName: "WordstatEvidence", freezeCols: 2, numericColumns: [3,4,5,7]
});

addTableSheet({
  name: "Проверка выдачи", title: "Точечная проверка: 9 запросов × 9 доменов", subtitle: "63 пары действительно проверены (7 запросов); 18 пар для двух запросов имеют неизвестный результат и не считаются проверенными.",
  headers: ["Направление", "Точный запрос", "Домен", "Статус запроса", "Видимость в TOP‑10", "Лучшая позиция", "URL в выдаче", "Как читать результат"],
  rows: matrix.map(r => [directionRu[r.deduplicated_direction_id] || r.tested_query, r.tested_query, r.selected_competitor_domain, r.search_acquisition_state === "SUCCEEDED" ? "Выдача получена" : "Результат неизвестен", r.visibility_state === "OBSERVED_IN_TOP10" ? "Наблюдался" : r.visibility_state === "NOT_OBSERVED_IN_TOP10" ? "Не наблюдался" : "Неизвестно", numberOrBlank(r.best_observed_rank), r.observed_ranking_urls || "—", r.search_acquisition_state === "SUCCEEDED" ? "Только этот запрос, этот домен и один сохранённый TOP‑10." : "Пара не считается проверенной: результат запроса неизвестен."]),
  widths: [29, 34, 25, 23, 20, 13, 60, 48], tableName: "ExactSearchMatrix", freezeCols: 3, numericColumns: [5]
});

addTableSheet({
  name: "Покрытие сайта", title: "Сохранённые наблюдения по текущему сайту", subtitle: "62 строки двух независимых проверочных наборов; это журнал наблюдений, а не 62 уникальные страницы.",
  headers: ["Набор доказательств", "URL", "Финальный URL", "Видимая роль / заголовок", "Наблюдение", "Доступность", "Состояние роли", "Свежесть источника", "QA", "Граница вывода"],
  rows: site.map(r => [r.evidence_set === "STEP20_CURRENT_URL_ROLE_RECHECK" ? "Проверка ролей URL" : "Проверка текущего содержания", r.url, r.final_url, r.visible_identity, r.observation || "Роль страницы без заметного изменения", "Публичная страница доступна", "Роль без заметного изменения", r.observed_freshness, r.qa_state === "PASS" ? "Пройдено" : "Требует проверки", r.claim_boundary.includes("First-party current-content") ? "Наблюдение по текущей странице: без вывода о позициях, спросе, трафике или эффективности." : "Сохранённое наблюдение по публичной странице: без вывода о позициях, спросе, трафике или полном составе содержания."]),
  widths: [25, 55, 55, 48, 65, 25, 34, 20, 10, 58], tableName: "CurrentSiteEvidence", freezeCols: 2
});

const method = wb.worksheets.add("Метод и ограничения");
addTitle(method, "Как читать результат", "Сначала доказательство, затем классификация; действие по странице остаётся отдельным решением.", 8);
method.getRange("A5:C15").values = [
  ["Этап", "Что проверялось", "Что не следует из результата"],
  ["Discovery", "75 точных запросов и 750 сохранённых строк TOP‑10.", "Это не полный рынок и не универсальная видимость домена."],
  ["Конкуренты", "9 сопоставимых компаний выбраны из 237 наблюдавшихся доменов.", "Частота появления не равна доле рынка или трафику."],
  ["Страницы", "44 доступные/перенаправленные страницы прочитаны по видимым элементам.", "Тема страницы не доказывает ранжирование по seed."],
  ["Seed", "43 разных направления выведены из 92 наблюдений с сохранением дублей происхождения.", "Seed не является готовым ключевым словом или разрывом."],
  ["Wordstat", "14 прежних проверок, 160 реально возвращённых строк.", "totalCount не суммируется в спрос страницы; пустой ответ не равен нулю."],
  ["Точечная выдача", "9 запросов планировались; 7 получены, 2 остались с неизвестным результатом.", "Неполученная выдача не считается проверенной."],
  ["Разрыв", "7 подтверждено, 23 уже покрыто, 3 вне предложения, 10 требуют данных.", "Подтверждённый разрыв не означает создание страницы."],
  ["Возможность", "Формат контентного расширения описан только для 7 подтверждённых направлений.", "Аналитическое внимание не равно графику, усилию, ROI или прогнозу роста."],
  ["Провайдеры", "В этой Phase 5 новых вызовов не было.", "Исторические данные не выдаются за новое исследование."],
  ["Граница продукта", "MK03 заканчивается аналитическим gap‑реестром и проверяемыми возможностями.", "Нет полного семантического ядра, архитектуры сайта или технического задания."],
];
method.getRange("A5:C5").format = { fill: COLORS.navy, font: { name: FONT, size: 10, bold: true, color: COLORS.white }, horizontalAlignment: "center" };
method.getRange("A5:C15").format.font = { name: FONT, size: 10, color: COLORS.ink };
method.getRange("A5:C15").format.wrapText = true;
method.getRange("A:A").format.columnWidth = 24;
method.getRange("B:C").format.columnWidth = 62;
method.getRange("A18:B25").values = [
  ["Проверка получателя", "Ожидаемый ответ"],
  ["Найти любое из 43 направлений", "Есть исходная тема, доказательства и ровно одно итоговое состояние."],
  ["Проверить подтверждённый разрыв", "Видны индивидуальная частота, важные фразы, точечная выдача и граница вывода."],
  ["Проверить уже покрытое", "Понятно, почему новая формулировка не является новым разрывом."],
  ["Проверить hold", "Указано, какого именно доказательства не хватает; действие не придумано."],
  ["Проверить конкурента", "Можно перейти от домена к наблюдаемым страницам и темам."],
  ["Проверить страницу", "Видно, что это наблюдение содержания, а не позиционный факт по всем ключам."],
  ["Принять решение", "До URL/страницы требуется подтверждение бизнеса и владельца темы."],
];
method.getRange("A18:B18").format = { fill: COLORS.navy, font: { name: FONT, size: 10, bold: true, color: COLORS.white } };
method.getRange("A18:B25").format.font = { name: FONT, size: 10, color: COLORS.ink };
method.getRange("A18:B25").format.wrapText = true;
method.tabColor = "#7F8C8D";

wb.recalculate();
const inspect = await wb.inspect({ kind: "workbook,sheet,table", maxChars: 9000, tableMaxRows: 3, tableMaxCols: 5, tableMaxCellChars: 80 });
await fs.writeFile(path.join(here, "qa", `MK03_PHASE5_XLSX_INSPECT_${date}.txt`), inspect.ndjson ?? String(inspect), "utf8");
for (const sheetName of ["Начните здесь", "Разрывы", "Возможности", "Конкуренты", "Страницы конкурентов", "Запросы discovery", "Wordstat", "Проверка выдачи", "Покрытие сайта", "Метод и ограничения"]) {
  const preview = await wb.render({ sheetName, autoCrop: "all", scale: 0.8, format: "png" });
  await fs.writeFile(path.join(renderDir, `${sheetName.replaceAll(" ", "_")}.png`), new Uint8Array(await preview.arrayBuffer()));
}
const file = await SpreadsheetFile.exportXlsx(wb);
await file.save(outPath);
console.log(JSON.stringify({ output: outPath, sheets: 10, rows: { gaps: gaps.length, opportunities: opportunities.length, competitors: domains.length, pages: pages.length, queries: queries.length, wordstat: wordstat.length, matrix: matrix.length, siteEvidence: site.length } }, null, 2));
