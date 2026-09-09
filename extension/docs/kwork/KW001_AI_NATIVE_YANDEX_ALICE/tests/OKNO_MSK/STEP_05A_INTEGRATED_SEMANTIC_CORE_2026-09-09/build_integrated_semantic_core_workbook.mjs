#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

function args(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 2) out[argv[i].replace(/^--/, "")] = argv[i + 1];
  return out;
}

function parseTsv(text) {
  const lines = text.replace(/^\uFEFF/, "").split(/\r?\n/).filter(Boolean);
  const headers = lines[0].split("\t");
  return lines.slice(1).map((line) => {
    const cells = line.split("\t");
    return Object.fromEntries(headers.map((h, i) => [h, cells[i] ?? ""]));
  });
}

const DISPLAY = {
  status: {
    ASSIGNED: "Назначено",
    ASSIGNED_HOLD: "Назначено; внедрение требует подтверждения",
    SEARCH_REQUIRED: "Требуется проверка в обычном Яндексе",
    REVIEW_DEFERRED: "Проверка отложена",
    EXCLUDED_PRESERVED: "Исключено; сохранено для аудита",
  },
  intent: {
    AMBIGUOUS: "Неоднозначный", COMMERCIAL: "Коммерческий",
    COMMERCIAL_INFO: "Коммерческий с информационной потребностью",
    COMMERCIAL_OR_INFO: "Коммерческий или информационный",
    COMMERCIAL_OR_SERVICE: "Коммерческий или сервисный",
    DIY_INFO: "Самостоятельное выполнение / инструкция", INFO: "Информационный",
    INFO_OR_COMMERCIAL: "Информационный или коммерческий",
    INFO_OR_SHOPPING: "Информационный или выбор товара",
    NAVIGATIONAL: "Навигационный", NAVIGATIONAL_COMMERCIAL: "Навигационный с коммерческой целью",
    OUTSIDE: "Вне целевой тематики", SERVICE: "Сервисный",
    SERVICE_OR_COMMERCIAL: "Сервисный или коммерческий",
    SERVICE_OR_SELECTION: "Сервисный или выбор решения",
  },
  owner: {
    OWNER_EXISTING: "Назначена существующая страница",
    OWNER_UNRESOLVED_EVIDENCE_REQUIRED: "Точный владелец требует подтверждения",
    NO_SUITABLE_EXISTING_PAGE: "Отдельная страница не требуется",
    OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP: "Страница не назначается: вне предложения",
    ASSIGNED_GOVERNED_NO_URL: "Решение принято без отдельного URL",
  },
  uncertainty: {
    NONE: "Неопределённость не зафиксирована",
    RESOLVED_EXCLUSION: "Исключение подтверждено",
    UNRESOLVED_DEFERRED: "Проверка отложена",
    CURRENT_OVERLAP_RECHECK: "Нужно повторно проверить пересечение страниц",
    HOLD: "Требуется снять неопределённость",
    LOW_CONFIDENCE: "Нужны дополнительные доказательства",
    UNRESOLVED_SEARCH_REQUIRED: "Нужна проверка в обычном Яндексе",
    APPLICABLE: "Назначение подтверждено",
    HOLD_NO_EXACT_TARGET: "Точная страница не доказана",
  },
  action: {
    KEEP_EXISTING_STRUCTURE: "Сохранить текущую структуру",
    NO_STANDALONE_PAGE: "Отдельная страница не требуется",
    ROUTE_TO_EXISTING_PAGE_AS_SUBTASK: "Отнести к существующей странице как подзадачу",
    OUTSIDE_SCOPE_NO_ACTION: "Вне предложения; действие не требуется",
    ADD_SECTION_OR_FAQ_TO_EXISTING: "Добавить раздел или ответы на вопросы",
    EXPAND_EXISTING_PAGE: "Расширить существующую страницу",
    DEFER_PENDING_EVIDENCE: "Отложить до получения подтверждений",
    SEMANTIC_MAPPING_ONLY: "Только семантическое назначение",
    HOLD_EVIDENCE: "Сохранить до подтверждения точного владельца",
  },
  newPage: {
    NO_NEW_PAGE: "Новая страница не требуется",
    NOT_READY__NO_NEW_PAGE_DECISION: "Решение о новой странице не готово",
    NEW_PAGE_DECISION_PRESENT_IN_ACCEPTED_AUTHORITY: "Есть принятое решение о новой странице",
  },
  siteChange: { YES: "Да", NO: "Нет", UNRESOLVED: "Не определено" },
  confidence: { HIGH: "Высокая", MEDIUM: "Средняя", LOW: "Низкая" },
  business: {
    IN_SCOPE: "Входит в подтверждённое предложение",
    IN_SCOPE_ADJACENT: "Смежно с подтверждённым предложением",
    NO_STANDALONE_FIRST_PARTY: "Релевантно без отдельной страницы",
    NO_STANDALONE_UNVERIFIED_BUSINESS: "Отдельная страница не подтверждена",
    OUTSIDE_SCOPE: "Вне подтверждённого предложения",
    DEFERRED_PENDING_MISSING_EVIDENCE: "Отложено до получения доказательств",
    DEFERRED_PENDING_BUSINESS_TRUTH: "Нужно подтвердить факты о предложении",
    DEFERRED_PENDING_OWNER_POLICY: "Нужно решение владельца",
  },
};

function show(group, code, field) {
  if (!code) return "Не применимо";
  const value = DISPLAY[group]?.[code];
  if (!value) throw new Error(`Нет русского отображения: ${field}=${code}`);
  return value;
}

function taskText(intent, phrase) {
  const p = `«${phrase}»`;
  const map = {
    AMBIGUOUS: `Уточнить неоднозначную задачу по теме ${p}`,
    COMMERCIAL: `Выбрать или заказать по теме ${p}`,
    COMMERCIAL_INFO: `Изучить условия и выбрать решение по теме ${p}`,
    COMMERCIAL_OR_INFO: `Уточнить: выбор/заказ или информация по теме ${p}`,
    COMMERCIAL_OR_SERVICE: `Уточнить: покупка продукта или заказ услуги по теме ${p}`,
    DIY_INFO: `Разобраться, как выполнить задачу самостоятельно по теме ${p}`,
    INFO: `Получить информацию по теме ${p}`,
    INFO_OR_COMMERCIAL: `Уточнить: получить информацию или выбрать решение по теме ${p}`,
    INFO_OR_SHOPPING: `Изучить варианты и при необходимости выбрать товар по теме ${p}`,
    NAVIGATIONAL: `Найти официальный раздел по теме ${p}`,
    NAVIGATIONAL_COMMERCIAL: `Найти официальный коммерческий раздел по теме ${p}`,
    OUTSIDE: `Запрос вне подтверждённого предложения по теме ${p}`,
    SERVICE: `Заказать профессиональную услугу по теме ${p}`,
    SERVICE_OR_COMMERCIAL: `Уточнить: заказать услугу или купить решение по теме ${p}`,
    SERVICE_OR_SELECTION: `Выбрать подходящую услугу или решение по теме ${p}`,
  };
  if (!intent) return "Не применимо к текущему состоянию строки";
  if (!map[intent]) throw new Error(`Неизвестный тип намерения: ${intent}`);
  return map[intent];
}

function reason(row) {
  if (row.semantic_state === "EXCLUDED_PRESERVED") return "Исключено при финальной очистке; строка сохранена для аудита.";
  if (row.semantic_state === "REVIEW_DEFERRED") return "Проверка отложена; строка не входит в активное ядро.";
  if (row.exact_query_owner_state === "OWNER_UNRESOLVED_EVIDENCE_REQUIRED") return "Точный владелец не доказан; URL не назначен.";
  if (row.exact_query_owner_state === "NO_SUITABLE_EXISTING_PAGE") return "Отдельная страница не требуется по принятому структурному решению.";
  if (row.exact_query_owner_state === "OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP") return "Спрос находится вне подтверждённого предложения.";
  if (row.exact_query_owner_state === "ASSIGNED_GOVERNED_NO_URL") return "Точное решение сохранено без отдельного URL.";
  return "Решение сохранено из итогового исследования.";
}

function capitalize(s) { return s ? s[0].toLocaleUpperCase("ru-RU") + s.slice(1) : s; }
function unique(values) { return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, "ru")); }
function colLetter(index) { let n = index + 1, s = ""; while (n) { const r = (n - 1) % 26; s = String.fromCharCode(65 + r) + s; n = Math.floor((n - 1) / 26); } return s; }

function styleDataSheet(sheet, rowCount, colCount, widths, tableName) {
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(2);
  const used = sheet.getRangeByIndexes(0, 0, rowCount, colCount);
  used.format.font = { name: "Arial", size: 9 };
  used.format.verticalAlignment = "top";
  used.format.wrapText = true;
  const header = sheet.getRangeByIndexes(0, 0, 1, colCount);
  header.format = { fill: "#17365D", font: { name: "Arial", size: 9, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", verticalAlignment: "center", wrapText: true };
  header.format.rowHeight = 38;
  for (let i = 0; i < widths.length; i += 1) sheet.getRangeByIndexes(0, i, rowCount, 1).format.columnWidth = widths[i];
  if (rowCount > 1) sheet.getRangeByIndexes(1, 0, rowCount - 1, colCount).format.rowHeight = 31;
  const table = sheet.tables.add(`A1:${colLetter(colCount - 1)}${rowCount}`, true, tableName);
  table.style = "TableStyleMedium2";
}

function writeTable(sheet, headers, rows) {
  sheet.getRangeByIndexes(0, 0, rows.length + 1, headers.length).values = [headers, ...rows];
}

const a = args(process.argv.slice(2));
for (const required of ["master", "units", "output", "preview-dir", "runtime-report"]) if (!a[required]) throw new Error(`Не задан --${required}`);
const master = parseTsv(await fs.readFile(a.master, "utf8"));
const units = parseTsv(await fs.readFile(a.units, "utf8"));
if (master.length !== 2856 || units.length !== 168) throw new Error(`Неверные входные размеры: ${master.length}/${units.length}`);
const active = master.filter((r) => r.active_state === "YES");
const unresolved = active.filter((r) => r.exact_query_owner_state === "OWNER_UNRESOLVED_EVIDENCE_REQUIRED");
const inactive = master.filter((r) => r.active_state === "NO");
if (active.length !== 2348 || unresolved.length !== 26 || inactive.length !== 508) throw new Error("Не сошлись контрольные состояния");

const byUnit = new Map();
for (const row of master) {
  if (!row.structural_unit) continue;
  if (!byUnit.has(row.structural_unit)) byUnit.set(row.structural_unit, []);
  byUnit.get(row.structural_unit).push(row);
}
const representatives = new Map();
for (const [unit, rows] of byUnit) {
  const candidates = rows.filter((r) => r.active_state === "YES");
  const pool = candidates.length ? candidates : rows;
  const rep = [...pool].sort((x, y) => Number(y.wordstat_frequency) - Number(x.wordstat_frequency) || x.phrase.length - y.phrase.length || x.phrase.localeCompare(y.phrase, "ru"))[0];
  representatives.set(unit, rep.phrase);
}

const wb = Workbook.create();
const readme = wb.worksheets.add("Как пользоваться");
const core = wb.worksheets.add("Итоговое ядро");
const groups = wb.worksheets.add("Группы спроса");
const pages = wb.worksheets.add("Страницы и назначение");
const unassigned = wb.worksheets.add("Не назначено точно");
const excluded = wb.worksheets.add("Исключено и отложено");
const sources = wb.worksheets.add("Источники и происхождение");

readme.showGridLines = false;
readme.getRange("A2:H2").merge();
readme.getRange("A2").values = [["ОКНО МОСКВА — единое семантическое ядро"]];
readme.getRange("A2:H2").format = { font: { name: "Arial", size: 16, bold: true, color: "#17365D" }, rowHeight: 28 };
readme.getRange("A3:H3").merge();
readme.getRange("A3").values = [["Базовый сбор и принятые формулировки из анализа конкурентов объединены до финальной очистки, группировки и назначения страниц."]];
readme.getRange("A3:H3").format = { font: { name: "Arial", size: 10, italic: true, color: "#44546A" }, wrapText: true, rowHeight: 34 };
const metrics = [
  ["Показатель", "Значение", "Как читать"],
  ["Единый приобретённый корпус", 2856, "2 840 базовых фраз + 16 фраз из штатного этапа анализа конкурентов"],
  ["Активное ядро", 2348, "Фразы, которые остаются в рабочем семантическом покрытии"],
  ["Завершённое решение по назначению", 2322, "Включает существующую страницу и управляемые решения без отдельного URL"],
  ["Без доказанного точного владельца", 26, "URL не подставлен; семейный маршрут показан отдельно, если он подтверждён"],
  ["Группы спроса", 168, "Группы по задаче пользователя и поисковому смыслу"],
  ["Новые страницы только из анализа конкурентов", 0, "Наличие темы у конкурента не является основанием для новой страницы"],
  ["Новые обращения к провайдерам при сборке", 0, "Использованы только сохранённые результаты исследования"],
];
readme.getRangeByIndexes(5, 0, metrics.length, 3).values = metrics;
readme.getRange("A6:C6").format = { fill: "#17365D", font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center" };
readme.getRange("A7:C13").format.font = { name: "Arial", size: 10 };
readme.getRange("B7:B13").format.numberFormat = "#,##0";
readme.getRange("A15:H15").merge();
readme.getRange("A15").values = [["Рабочее правило"]];
readme.getRange("A15:H15").format = { fill: "#D9EAF7", font: { name: "Arial", size: 11, bold: true, color: "#17365D" } };
readme.getRange("A16:H19").merge();
readme.getRange("A16").values = [["Сначала найдите фразу на листе «Итоговое ядро». Точный владелец отвечает за конкретную фразу. Семейная страница показывает маршрут группы и не подменяет точного владельца. Пустой точный URL может быть корректным результатом: отдельная страница не нужна, запрос вне предложения или доказательств пока недостаточно. Число запросов взято из сохранённого Вордстата без операторов и не является точной частотностью или прогнозом трафика."]];
readme.getRange("A16:H19").format = { font: { name: "Arial", size: 10 }, wrapText: true, verticalAlignment: "top" };
for (const [i, w] of [46, 18, 75, 3, 3, 3, 3, 3].entries()) readme.getRangeByIndexes(0, i, 22, 1).format.columnWidth = w;
readme.tabColor = "#17365D";

const coreHeaders = ["Фраза", "Число запросов", "Статус", "Активная", "Группа спроса", "Задача пользователя", "Намерение", "Граница предложения", "Решение по точному владельцу", "Точная страница", "Семейная страница", "Поддерживающие страницы", "Неопределённость", "Рекомендация", "Новая страница", "Изменение сайта", "Основание"];
const coreRows = master.map((r) => {
  const rep = representatives.get(r.structural_unit) || r.phrase;
  return [r.phrase, Number(r.wordstat_frequency), show("status", r.semantic_state, "semantic_state"), r.active_state === "YES" ? "Да" : "Нет", r.structural_unit ? capitalize(rep) : "Не назначено", taskText(r.intent, rep), show("intent", r.intent, "intent"), show("business", r.business_boundary_state, "business_boundary_state"), show("owner", r.exact_query_owner_state, "exact_query_owner_state"), r.exact_primary_page || "", r.family_primary_page || "", r.supporting_pages || "", show("uncertainty", r.page_assignment_uncertainty, "page_assignment_uncertainty"), show("action", r.implementation_action_type, "implementation_action_type"), show("newPage", r.new_page_decision, "new_page_decision"), show("siteChange", r.site_change, "site_change"), reason(r)];
});
writeTable(core, coreHeaders, coreRows);
styleDataSheet(core, coreRows.length + 1, coreHeaders.length, [30, 12, 24, 10, 27, 39, 23, 28, 30, 45, 45, 45, 30, 34, 28, 14, 42], "IntegratedCoreTable");
core.getRange(`B2:B${coreRows.length + 1}`).format.numberFormat = "#,##0";
core.tabColor = "#1F4E78";

const groupHeaders = ["Группа спроса", "Пример фразы", "Все фразы", "Активные фразы", "Решение по назначению принято", "Существующая точная страница", "Управляемо без URL", "Точный владелец не доказан", "Сумма числа запросов*", "Задача пользователя", "Намерение", "Семейная страница", "Поддерживающие страницы", "Структурное решение", "Неопределённость", "Фразы из анализа конкурентов"];
const groupRows = units.map((u) => {
  const rep = representatives.get(u.structural_unit_id);
  return [capitalize(rep), rep, Number(u.unified_phrase_count), Number(u.active_phrase_count), Number(u.exact_assignment_decision_count), Number(u.exact_existing_page_count), Number(u.governed_no_page_count), Number(u.unresolved_exact_owner_count), Number(u.demand_frequency_sum_non_additive), taskText(u.intent_type, rep), show("intent", u.intent_type, "intent_type"), u.family_primary_page || "", u.supporting_pages || "", show("action", u.structural_action, "structural_action"), show("uncertainty", u.uncertainty_state, "uncertainty_state"), Number(u.step5a_phrase_count)];
});
writeTable(groups, groupHeaders, groupRows);
styleDataSheet(groups, groupRows.length + 1, groupHeaders.length, [29, 29, 11, 11, 14, 14, 14, 14, 16, 40, 22, 45, 45, 35, 28, 14], "DemandGroupsTable");
groups.getRange(`C2:I${groupRows.length + 1}`).format.numberFormat = "#,##0";
groups.getRange(`P2:P${groupRows.length + 1}`).format.numberFormat = "#,##0";

const pageMap = new Map();
for (const r of active.filter((x) => x.exact_primary_page)) {
  if (!pageMap.has(r.exact_primary_page)) pageMap.set(r.exact_primary_page, []);
  pageMap.get(r.exact_primary_page).push(r);
}
const pageHeaders = ["Точная страница", "Активные фразы", "Группы спроса", "Сумма числа запросов*", "Примеры фраз", "Поддерживающие страницы", "Изменение сайта"];
const pageRows = [...pageMap.entries()].sort(([a], [b]) => a.localeCompare(b, "ru")).map(([url, rows]) => [url, rows.length, unique(rows.map((r) => capitalize(representatives.get(r.structural_unit)))).join("; "), rows.reduce((s, r) => s + Number(r.wordstat_frequency), 0), rows.slice().sort((a, b) => Number(b.wordstat_frequency) - Number(a.wordstat_frequency)).slice(0, 5).map((r) => r.phrase).join("; "), unique(rows.flatMap((r) => r.supporting_pages.split(";").filter(Boolean))).join("; "), unique(rows.map((r) => show("siteChange", r.site_change, "site_change"))).join("; ")]);
writeTable(pages, pageHeaders, pageRows);
styleDataSheet(pages, pageRows.length + 1, pageHeaders.length, [50, 13, 42, 16, 52, 52, 18], "PageAssignmentTable");
pages.getRange(`B2:B${pageRows.length + 1}`).format.numberFormat = "#,##0";
pages.getRange(`D2:D${pageRows.length + 1}`).format.numberFormat = "#,##0";

const unHeaders = ["Фраза", "Число запросов", "Группа спроса", "Задача пользователя", "Намерение", "Семейная страница", "Поддерживающие страницы", "Почему точный URL не назначен", "Следующий допустимый шаг"];
const unRows = unresolved.map((r) => { const rep = representatives.get(r.structural_unit) || r.phrase; return [r.phrase, Number(r.wordstat_frequency), capitalize(rep), taskText(r.intent, rep), show("intent", r.intent, "intent"), r.family_primary_page || "", r.supporting_pages || "", reason(r), r.semantic_state === "SEARCH_REQUIRED" ? "Проверить точную фразу в обычном Яндексе в отдельном разрешённом этапе" : "Получить недостающее подтверждение владельца страницы или границы услуги"]; });
writeTable(unassigned, unHeaders, unRows);
styleDataSheet(unassigned, unRows.length + 1, unHeaders.length, [34, 12, 29, 42, 22, 48, 48, 42, 46], "UnresolvedOwnerTable");
unassigned.getRange(`B2:B${unRows.length + 1}`).format.numberFormat = "#,##0";
unassigned.tabColor = "#C65911";

const exHeaders = ["Фраза", "Число запросов", "Статус", "Граница предложения", "Причина сохранения вне активного ядра"];
const exRows = inactive.map((r) => [r.phrase, Number(r.wordstat_frequency), show("status", r.semantic_state, "semantic_state"), show("business", r.business_boundary_state, "business_boundary_state"), reason(r)]);
writeTable(excluded, exHeaders, exRows);
styleDataSheet(excluded, exRows.length + 1, exHeaders.length, [38, 12, 28, 32, 58], "ExcludedDeferredTable");
excluded.getRange(`B2:B${exRows.length + 1}`).format.numberFormat = "#,##0";

sources.showGridLines = false;
sources.getRange("A2:H2").merge();
sources.getRange("A2").values = [["Источники и происхождение фраз"]];
sources.getRange("A2:H2").format = { font: { name: "Arial", size: 15, bold: true, color: "#17365D" } };
sources.getRange("A4:D6").values = [
  ["Этап получения", "Фраз", "Роль", "Граница вывода"],
  ["Базовый сбор спроса", 2840, "Исходная семантика сайта и бизнеса", "Сохранена исходная provenance каждой фразы"],
  ["Анализ конкурентных пробелов", 16, "Штатное расширение после проверки спроса", "Тема конкурента не равна новой странице и не доказывает будущий трафик"],
];
sources.getRange("A4:D4").format = { fill: "#17365D", font: { name: "Arial", size: 9, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center" };
sources.getRange("A5:D6").format.font = { name: "Arial", size: 9 };
sources.getRange("B5:B6").format.numberFormat = "#,##0";
sources.getRange("A8:H8").values = [["Фраза", "Направление спроса", "Страница конкурента — источник темы", "Формулировка для проверки спроса", "Число запросов", "Точный запрос для проверки в Яндексе", "Результат назначения", "Точная страница"]];
const directionNames = new Map([...byUnit.keys()].map((u) => [u, capitalize(representatives.get(u))]));
const step5a = master.filter((r) => r.acquisition_stage === "STEP_05A");
const srcRows = step5a.map((r) => [r.phrase, directionNames.get(r.structural_unit), r.competitor_page_evidence, r.competitor_candidate_seed, Number(r.wordstat_frequency), r.search_representative_query, show("owner", r.exact_query_owner_state, "exact_query_owner_state"), r.exact_primary_page]);
sources.getRangeByIndexes(8, 0, srcRows.length, 8).values = srcRows;
sources.getRange("A8:H8").format = { fill: "#17365D", font: { name: "Arial", size: 9, bold: true, color: "#FFFFFF" }, horizontalAlignment: "center", wrapText: true, rowHeight: 38 };
sources.getRange("A9:H24").format = { font: { name: "Arial", size: 9 }, wrapText: true, verticalAlignment: "top", rowHeight: 42 };
const sourceTable = sources.tables.add("A8:H24", true, "SourceLineageTable");
sourceTable.style = "TableStyleMedium2";
for (const [i, w] of [34, 27, 55, 34, 12, 36, 32, 50].entries()) sources.getRangeByIndexes(0, i, 26, 1).format.columnWidth = w;
sources.freezePanes.freezeRows(8);
sources.tabColor = "#8497B0";

wb.recalculate();
const formulaErrors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 100 }, summary: "final formula error scan" });
if (formulaErrors.ndjson && /#(REF!|DIV\/0!|VALUE!|NAME\?|N\/A|NUM!|NULL!|SPILL!|CALC!)/.test(formulaErrors.ndjson)) throw new Error("Обнаружены ошибки формул");
await fs.mkdir(path.dirname(a.output), { recursive: true });
await fs.mkdir(a["preview-dir"], { recursive: true });
const exported = await SpreadsheetFile.exportXlsx(wb);
await exported.save(a.output);

const saved = await SpreadsheetFile.importXlsx(await FileBlob.load(a.output));
const sheetNames = ["Как пользоваться", "Итоговое ядро", "Группы спроса", "Страницы и назначение", "Не назначено точно", "Исключено и отложено", "Источники и происхождение"];
const actualNames = saved.worksheets.items.map((s) => s.name);
if (JSON.stringify(actualNames) !== JSON.stringify(sheetNames)) throw new Error(`Неверные листы после открытия: ${actualNames}`);
const savedCounts = {};
for (const name of sheetNames) savedCounts[name] = saved.worksheets.getItem(name).getUsedRange(true).values.length;
if (savedCounts["Итоговое ядро"] !== 2857 || savedCounts["Группы спроса"] !== 169 || savedCounts["Не назначено точно"] !== 27 || savedCounts["Исключено и отложено"] !== 509) throw new Error(`Неверные строки после открытия: ${JSON.stringify(savedCounts)}`);

const previews = [
  ["Как пользоваться", "A1:H20"], ["Итоговое ядро", "A1:Q24"], ["Группы спроса", "A1:P24"],
  ["Страницы и назначение", `A1:G${Math.min(pageRows.length + 1, 24)}`], ["Не назначено точно", "A1:I27"],
  ["Исключено и отложено", "A1:E24"], ["Источники и происхождение", "A1:H24"],
];
const previewFiles = [];
for (const [sheetName, range] of previews) {
  const blob = await saved.render({ sheetName, range, scale: 1, format: "png" });
  const file = `${sheetName.replace(/\s+/g, "_")}.png`;
  await fs.writeFile(path.join(a["preview-dir"], file), new Uint8Array(await blob.arrayBuffer()));
  previewFiles.push({ sheet: sheetName, range, file });
}
const runtime = {
  schema: "OKNO_MSK_INTEGRATED_CORE_XLSX_RUNTIME_V1", status: "PASS", output: a.output,
  sheets: actualNames, saved_used_rows: savedCounts, source_counts: { canonical: master.length, active: active.length, unresolved_exact_owner: unresolved.length, excluded_deferred: inactive.length, groups: units.length, step5a: step5a.length, exact_pages: pageRows.length },
  formula_errors: 0, previews: previewFiles,
};
await fs.writeFile(a["runtime-report"], `${JSON.stringify(runtime, null, 2)}\n`, "utf8");
console.log(JSON.stringify(runtime));
