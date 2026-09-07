#!/usr/bin/env node

import crypto from "node:crypto";
import { execFile } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import { promisify } from "node:util";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const execFileAsync = promisify(execFile);

const ACTIVE_STATES = new Set(["ASSIGNED", "ASSIGNED_HOLD", "SEARCH_REQUIRED"]);
const ASSIGNED_STATES = new Set(["ASSIGNED", "ASSIGNED_HOLD"]);
const METRIC_TYPE = "BROAD_GETTOP_NO_OPERATORS";
const AGGREGATION_RULE = "MAX_PER_PHRASE_SEPARATELY_FOR_RESULT_AND_ASSOCIATION";
const METRIC_DISPLAY = "Топы запросов Вордстата, без операторов";
const AGGREGATION_DISPLAY = "При повторных наблюдениях сохранено максимальное значение отдельно для популярных и похожих запросов";
const CLAIM_BOUNDARY = "Статистика из раздела «Топы запросов» Вордстата по Москве, для всех устройств, без операторов. Значение нельзя трактовать как точную частотность фразы или прогноз трафика.";

const DISPLAY_MAPS = Object.freeze({
  semanticStatus: Object.freeze({
    ASSIGNED: "Назначено",
    ASSIGNED_HOLD: "Назначено, внедрение требует дополнительной проверки",
    SEARCH_REQUIRED: "Требуется проверка в обычном поиске Яндекса",
    REVIEW_DEFERRED: "Проверка отложена",
    EXCLUDED_PRESERVED: "Исключено, сохранено для полноты исследования",
  }),
  intent: Object.freeze({
    AMBIGUOUS: "Неоднозначный",
    COMMERCIAL: "Коммерческий",
    COMMERCIAL_INFO: "Коммерческий с информационной потребностью",
    COMMERCIAL_OR_INFO: "Коммерческий или информационный",
    COMMERCIAL_OR_SERVICE: "Коммерческий или сервисный",
    DIY_INFO: "Информационный — самостоятельное выполнение",
    INFO: "Информационный",
    INFO_OR_COMMERCIAL: "Информационный или коммерческий",
    INFO_OR_SHOPPING: "Информационный или выбор товара",
    NAVIGATIONAL: "Навигационный",
    NAVIGATIONAL_COMMERCIAL: "Навигационный с коммерческой целью",
    OUTSIDE: "Вне целевой тематики",
    SERVICE: "Сервисный",
    SERVICE_OR_COMMERCIAL: "Сервисный или коммерческий",
    SERVICE_OR_SELECTION: "Сервисный или выбор услуги/решения",
  }),
  businessScope: Object.freeze({
    DEFERRED_PENDING_BUSINESS_TRUTH: "Отложено до подтверждения фактов о предложении компании",
    DEFERRED_PENDING_MISSING_EVIDENCE: "Отложено до получения недостающих доказательств",
    DEFERRED_PENDING_OWNER_POLICY: "Отложено до решения владельца",
    IN_SCOPE: "Входит в подтверждённое предложение",
    IN_SCOPE_ADJACENT: "Смежно с подтверждённым предложением",
    NO_STANDALONE_FIRST_PARTY: "Релевантно без отдельной собственной страницы",
    NO_STANDALONE_UNVERIFIED_BUSINESS: "Отдельная страница не подтверждена фактами о предложении",
    OUTSIDE_SCOPE: "Вне подтверждённого предложения",
  }),
  pageRole: Object.freeze({
    BASE_UNIT_PENDING_ACTION_REEVALUATION: "Базовая единица; действие требует повторной оценки",
    DEFERRED: "Роль страницы отложена",
    NEW_COMMERCIAL_CANDIDATE: "Кандидат на новую коммерческую страницу",
    NEW_INFORMATIONAL_CANDIDATE: "Кандидат на новую информационную страницу",
    NEW_INFORMATIONAL_SUBUNIT_CANDIDATE: "Кандидат на отдельный информационный подраздел",
    NO_STANDALONE_UNVERIFIED_CATALOG: "Отдельная страница каталога не подтверждена",
    NO_STANDALONE_UNVERIFIED_PRODUCT: "Отдельная страница продукта не подтверждена",
    NO_STANDALONE_UNVERIFIED_SERVICE: "Отдельная страница услуги не подтверждена",
    OUTSIDE: "Страница не требуется: запрос вне предложения",
    PRIMARY_EXISTING_HUB: "Основной существующий раздел",
    PRIMARY_EXISTING_INFO: "Основная существующая информационная страница",
    PRIMARY_EXISTING_PORTFOLIO: "Основная существующая страница портфолио",
    PRIMARY_EXISTING_PRODUCT: "Основная существующая страница продукта",
    PRIMARY_EXISTING_SERVICE: "Основная существующая страница услуги",
    PRIMARY_EXISTING_TRUST_COMMERCIAL: "Основная существующая коммерческая страница доверия и репутации",
    PRIMARY_EXISTING_UTILITY: "Основной существующий инструмент или сервисный раздел",
    PROVISIONAL_EXISTING_INFO: "Предварительно назначенная существующая информационная страница",
    PROVISIONAL_OBJECT_VS_MATERIAL_PAGE: "Предварительное назначение: страница объекта или материала",
    SUPPORTING_CONTENT: "Поддерживающий контент",
    SUPPORTING_CROSS_CUTTING_UTILITY: "Поддерживающий сквозной инструмент или раздел",
    SUPPORTING_EXISTING_INFO: "Поддерживающая существующая информационная страница",
    SUPPORTING_EXISTING_PAGE: "Поддерживающая существующая страница",
    SUPPORTING_PRODUCT_CONTENT: "Поддерживающий контент о продукте",
    SUPPORTING_SAFETY_CONTENT: "Поддерживающий контент о безопасности",
    SUPPORTING_SERVICE_OR_PRODUCT: "Поддерживающая страница услуги или продукта",
    UNSERVABLE_NEUTRAL_REVIEW: "Нейтральный обзор без подтверждённой возможности обслужить спрос",
  }),
  structuralAction: Object.freeze({
    ADD_SECTION_OR_FAQ_TO_EXISTING: "Добавить раздел или ответы на вопросы на существующую страницу",
    DEFER_PENDING_EVIDENCE: "Отложить до получения подтверждений",
    EXPAND_EXISTING_PAGE: "Расширить существующую страницу",
    KEEP_EXISTING_STRUCTURE: "Сохранить текущую структуру",
    NO_STANDALONE_PAGE: "Отдельная страница не требуется",
    OUTSIDE_SCOPE_NO_ACTION: "Вне рамок предложения — действий не требуется",
    ROUTE_TO_EXISTING_PAGE_AS_SUBTASK: "Отнести к существующей странице как подзадачу",
  }),
  maturity: Object.freeze({
    DEFERRED_PENDING_MISSING_EVIDENCE: "Решение отложено: не хватает доказательств",
    FINAL_AFTER_STEP14A_CURRENT_SITE_DISCOVERY: "Финальное после актуальной проверки структуры сайта",
    FINAL_WITHIN_STEP12_EVIDENCE: "Финальное в пределах имеющихся доказательств",
    PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK: "Предварительное до проверки возможного конфликта страниц",
  }),
  uncertainty: Object.freeze({
    CURRENT_OVERLAP_RECHECK: "Требуется повторно проверить текущее пересечение страниц",
    HOLD: "Решение приостановлено до снятия неопределённости",
    LOW_CONFIDENCE: "Низкая уверенность — требуется дополнительное подтверждение",
    NONE: "Дополнительная неопределённость не зафиксирована",
    RESOLVED_EXCLUSION: "Исключение подтверждено",
    UNRESOLVED_DEFERRED: "Неопределённость сохранена, проверка отложена",
    UNRESOLVED_SEARCH_REQUIRED: "Неопределённость требует проверки в обычном поиске Яндекса",
  }),
  confidence: Object.freeze({ HIGH: "Высокая", MEDIUM: "Средняя", LOW: "Низкая" }),
  searchDisposition: Object.freeze({
    CORE_CANDIDATE: "Кандидат в рабочее семантическое ядро",
    EXCLUDED_PRESERVED: "Исключено, сохранено для полноты исследования",
    REVIEW_DEFERRED: "Проверка отложена",
    REVIEW_SEARCH: "Передать на проверку в обычном поиске Яндекса",
  }),
  resolutionRoute: Object.freeze({
    NO_ACTIVE_SEARCH_ROUTE: "Активная проверка в поиске не требуется",
    ORDINARY_SEARCH_ELIGIBLE: "Можно проверить в обычной выдаче Яндекса",
    REVIEW_DEFERRED: "Проверка отложена",
    REVIEW_SEARCH: "Проверить в обычной выдаче Яндекса",
  }),
  frequencyRole: Object.freeze({
    "RESULT + ASSOCIATION": "Есть данные по популярным и похожим запросам",
    RESULT: "Есть данные по популярным запросам",
    ASSOCIATION_ONLY: "Есть данные только по похожим запросам",
    NO_POSITIVE_COUNT: "Положительных значений не зафиксировано",
  }),
  gapType: Object.freeze({
    EVIDENCE_INSUFFICIENT: "Недостаточно доказательств",
    NONE: "Содержательный пробел не зафиксирован",
    QUALITY_GAP: "Нуждается в улучшении качества содержания",
  }),
  contentEnhancement: Object.freeze({
    CONTENT_EVIDENCE_INSUFFICIENT: "Недостаточно доказательств для изменения содержания",
    NONE: "Изменение содержания не требуется",
    NOT_ASSESSED: "Содержание не оценивалось",
    QUALITY_GAP: "Содержание нуждается в улучшении",
  }),
});

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i += 1) {
    if (!argv[i].startsWith("--")) continue;
    result[argv[i].slice(2)] = argv[i + 1];
    i += 1;
  }
  return result;
}

function parseTsv(text) {
  const lines = text.replace(/^\uFEFF/, "").split(/\r?\n/).filter((line) => line.length > 0);
  const headers = lines[0].split("\t");
  return lines.slice(1).map((line) => {
    const cells = line.split("\t");
    return Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? ""]));
  });
}

function normalize(value) {
  return String(value ?? "").normalize("NFKC").trim().replace(/\s+/g, " ").toLocaleLowerCase("ru-RU");
}

function phraseId(phrase) {
  return `PHR-${crypto.createHash("sha1").update(normalize(phrase), "utf8").digest("hex").slice(0, 12).toUpperCase()}`;
}

function asInteger(value, field, phrase) {
  if (!/^\d+$/.test(String(value))) throw new Error(`Non-numeric ${field} for ${phrase}: ${value}`);
  return Number(value);
}

function capitalize(value) {
  if (!value) return value;
  return value[0].toLocaleUpperCase("ru-RU") + value.slice(1);
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
}

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, "ru"));
}

function sourceSnapshotDate(sourceIds) {
  const hasPass1 = /(^|\|)S\d+($|\|)/.test(sourceIds);
  const hasPass2 = /(^|\|)P2-\d+($|\|)/.test(sourceIds);
  if (hasPass1 && hasPass2) return "2026-08-28; 2026-08-29";
  if (hasPass2) return "2026-08-28";
  if (hasPass1) return "2026-08-29";
  return "ДАТА НЕ РАЗРЕШЕНА ИЗ SOURCE IDS";
}

function frequencyRole(resultCount, associationCount) {
  if (resultCount > 0 && associationCount > 0) return "RESULT + ASSOCIATION";
  if (resultCount > 0) return "RESULT";
  if (associationCount > 0) return "ASSOCIATION_ONLY";
  return "NO_POSITIVE_COUNT";
}

function displayEnum(group, code, fieldName) {
  if (!code) return "Не применимо по финальному решению";
  const value = DISPLAY_MAPS[group]?.[code];
  if (!value) throw new Error(`Unknown client-visible enum without Russian display label: ${fieldName}=${code}`);
  return value;
}

function clientTask(intentCode, representativePhrase) {
  const subject = `«${representativePhrase}»`;
  const templates = {
    AMBIGUOUS: `Уточнить неоднозначную задачу по теме ${subject}`,
    COMMERCIAL: `Выбрать или заказать по теме ${subject}`,
    COMMERCIAL_INFO: `Изучить условия и выбрать решение по теме ${subject}`,
    COMMERCIAL_OR_INFO: `Уточнить: выбор/заказ или получение информации по теме ${subject}`,
    COMMERCIAL_OR_SERVICE: `Уточнить: покупка продукта или заказ услуги по теме ${subject}`,
    DIY_INFO: `Разобраться, как выполнить самостоятельно задачу по теме ${subject}`,
    INFO: `Получить информацию по теме ${subject}`,
    INFO_OR_COMMERCIAL: `Уточнить: получить информацию или выбрать решение по теме ${subject}`,
    INFO_OR_SHOPPING: `Изучить варианты и при необходимости выбрать товар по теме ${subject}`,
    NAVIGATIONAL: `Перейти к официальному сайту или нужному разделу по теме ${subject}`,
    NAVIGATIONAL_COMMERCIAL: `Найти официальный коммерческий раздел по теме ${subject}`,
    OUTSIDE: `Запрос вне подтверждённого предложения по теме ${subject}`,
    SERVICE: `Заказать профессиональную услугу по теме ${subject}`,
    SERVICE_OR_COMMERCIAL: `Уточнить: заказать услугу или купить решение по теме ${subject}`,
    SERVICE_OR_SELECTION: `Выбрать подходящую услугу или решение по теме ${subject}`,
  };
  const value = templates[intentCode];
  if (!value) throw new Error(`Unknown intent for client task display: ${intentCode}`);
  return value;
}

function reopenDisplay(row) {
  if (row.final_semantic_state === "SEARCH_REQUIRED") {
    return "Проверить точную фразу в обычной выдаче Яндекса, затем подтвердить задачу, кластер и целевую страницу";
  }
  if (row.final_semantic_state === "REVIEW_DEFERRED") {
    return "Возобновить проверку только после появления нового подтверждающего источника или уточнения задачи";
  }
  if (row.final_semantic_state === "EXCLUDED_PRESERVED") {
    return "Возвращать в рабочее ядро только при появлении нового доказательства релевантности предложению сайта";
  }
  if (row.uncertainty_state === "HOLD") {
    return "Сначала снять зафиксированную блокирующую неопределённость; до этого физическое внедрение запрещено";
  }
  if (row.uncertainty_state === "CURRENT_OVERLAP_RECHECK") {
    return "Повторно проверить текущее пересечение страниц в выдаче Яндекса до структурного изменения";
  }
  if (row.uncertainty_state === "LOW_CONFIDENCE") {
    return "Получить дополнительное подтверждение задачи, интента или владельца страницы";
  }
  return "Пересмотр не требуется по текущему финальному решению";
}

function routeReasonDisplay(row) {
  if (row.final_semantic_state === "SEARCH_REQUIRED") {
    return "Сохранённых доказательств недостаточно для окончательного назначения фразы кластеру и странице";
  }
  if (row.final_semantic_state === "REVIEW_DEFERRED") {
    return "Фраза сохранена для аудита, но немедленная проверка не обоснована";
  }
  if (row.final_semantic_state === "EXCLUDED_PRESERVED") {
    return "Фраза исключена из рабочего ядра, но сохранена для полноты исходного корпуса";
  }
  return "Маршрут соответствует текущему финальному семантическому решению";
}

function unitReopenDisplay(unit) {
  if (unit.uncertainty_state === "HOLD" || unit.structural_action === "DEFER_PENDING_EVIDENCE") {
    return "Сначала получить недостающее подтверждение и снять блокирующую неопределённость";
  }
  if (unit.uncertainty_state === "CURRENT_OVERLAP_RECHECK") {
    return "Повторно проверить текущее пересечение страниц в выдаче Яндекса до структурного изменения";
  }
  if (unit.uncertainty_state === "LOW_CONFIDENCE") {
    return "Получить дополнительное подтверждение задачи, интента или владельца страницы";
  }
  return "Пересмотр не требуется по текущему финальному решению";
}

function targetDisplay(row) {
  if (row.final_primary_page) return row.final_primary_page;
  if (ASSIGNED_STATES.has(row.final_semantic_state)) {
    return `НЕТ ОТДЕЛЬНОЙ СТРАНИЦЫ — ${displayEnum("structuralAction", row.canonical_structural_action, "canonical_structural_action")}`;
  }
  if (row.final_semantic_state === "SEARCH_REQUIRED") return "НЕ НАЗНАЧЕНО — требуется проверка в обычном поиске Яндекса";
  return "НЕ ПРИМЕНИМО — ВНЕ АКТИВНОГО ЯДРА";
}

function missingText(row, fieldName) {
  if (row[fieldName]) return row[fieldName];
  if (row.final_semantic_state === "SEARCH_REQUIRED") return "НЕ НАЗНАЧЕНО — требуется проверка в обычном поиске Яндекса";
  if (!ACTIVE_STATES.has(row.final_semantic_state)) return "НЕ ПРИМЕНИМО — ВНЕ АКТИВНОГО ЯДРА";
  return "НЕ ПРИМЕНИМО ПО ФИНАЛЬНОМУ РЕШЕНИЮ";
}

const REPRESENTATIVE_OVERRIDES = {
  BALCONY_GLAZING_WARM: "теплое остекление балконов",
  FRENCH_WINDOW_DEFINITION_INFO: "французское окно как называется",
  MOSQUITO_NET_INSTALLATION_SERVICE: "установка москитной сетки на пластиковое окно",
  PRIVATE_HOUSE_WINDOWS_COMMERCIAL: "купить пластиковые окна для частного дома",
  PVC_DOOR_REPAIR_SERVICE: "ремонт пластиковых дверей",
  TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL: "деревянно алюминиевые окна",
};

const GENERIC_TOKENS = new Set([
  "для", "из", "на", "в", "во", "с", "со", "и", "или", "по", "под", "без", "к", "как", "что",
  "окно", "окна", "окон", "оконный", "оконная", "оконные", "пластиковый", "пластиковые", "пластиковых",
]);

function candidateScore(candidate, members) {
  const words = normalize(candidate.phrase).split(" ").filter(Boolean);
  const significant = new Set(words.filter((word) => word.length >= 4 && !GENERIC_TOKENS.has(word)).map((word) => word.slice(0, 6)));
  let shared = 0;
  for (const member of members) {
    const memberTokens = new Set(normalize(member.phrase).split(" ").filter((word) => word.length >= 4 && !GENERIC_TOKENS.has(word)).map((word) => word.slice(0, 6)));
    if ([...significant].some((token) => memberTokens.has(token))) shared += 1;
  }
  const naturalLength = words.length >= 2 && words.length <= 6 ? 12 : words.length === 1 ? 4 : 0;
  const noDigits = /\d/.test(candidate.phrase) ? 0 : 8;
  const noGeo = /москв|район|город|телефон|адрес/i.test(candidate.phrase) ? 0 : 5;
  const noPriceModifier = /цена|стоимост|недорог|дешев/i.test(candidate.phrase) ? 0 : 5;
  const demand = Math.log10(candidate.resultCount + 1) * 8;
  const centrality = members.length ? (shared / members.length) * 20 : 0;
  return naturalLength + noDigits + noGeo + noPriceModifier + demand + centrality;
}

function selectRepresentative(unitId, members) {
  const override = REPRESENTATIVE_OVERRIDES[unitId];
  if (override) {
    const found = members.find((row) => normalize(row.phrase) === normalize(override));
    if (!found) throw new Error(`Representative override is not a canonical member: ${unitId} -> ${override}`);
    return found;
  }
  return [...members].sort((a, b) => {
    const delta = candidateScore(b, members) - candidateScore(a, members);
    if (Math.abs(delta) > 1e-9) return delta;
    if (b.resultCount !== a.resultCount) return b.resultCount - a.resultCount;
    return a.phrase.localeCompare(b.phrase, "ru");
  })[0];
}

function assignRanks(rows, keyFn) {
  const groups = new Map();
  for (const row of rows) {
    const key = keyFn(row);
    if (!key || row.final_semantic_state === "SEARCH_REQUIRED") continue;
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  const result = new Map();
  for (const members of groups.values()) {
    members.sort((a, b) => b.resultCount - a.resultCount || a.phrase.localeCompare(b.phrase, "ru") || a.id.localeCompare(b.id));
    members.forEach((row, index) => result.set(row.id, index + 1));
  }
  return result;
}

function priorityFor(row) {
  const state = row.final_semantic_state;
  const action = row.canonical_structural_action;
  const maturity = row.canonical_recommendation_maturity;
  const uncertainty = row.uncertainty_state;
  const demand = `число запросов = ${row.resultCount}`;
  if (!ACTIVE_STATES.has(state)) return ["P5 — ВНЕ РАБОЧЕГО ЯДРА", `статус: ${displayEnum("semanticStatus", state, "final_semantic_state")}`];
  if (state === "SEARCH_REQUIRED") {
    return ["P0 — ПРОВЕСТИ ПРОВЕРКУ В ЯНДЕКСЕ", `статус: ${displayEnum("semanticStatus", state, "final_semantic_state")}; неопределённость: ${displayEnum("uncertainty", uncertainty, "uncertainty_state")}; ${demand}`];
  }
  if (uncertainty === "HOLD" || action === "DEFER_PENDING_EVIDENCE" || maturity.startsWith("DEFERRED")) {
    return ["P0 — СНЯТЬ НЕОПРЕДЕЛЁННОСТЬ", `рекомендация: ${displayEnum("structuralAction", action, "canonical_structural_action")}; готовность: ${displayEnum("maturity", maturity, "canonical_recommendation_maturity")}; неопределённость: ${displayEnum("uncertainty", uncertainty, "uncertainty_state")}; ${demand}`];
  }
  if (["ADD_SECTION_OR_FAQ_TO_EXISTING", "EXPAND_EXISTING_PAGE"].includes(action)) {
    if (maturity.startsWith("FINAL")) {
      return ["P1 — ГОТОВОЕ ИЗМЕНЕНИЕ", `рекомендация: ${displayEnum("structuralAction", action, "canonical_structural_action")}; готовность: ${displayEnum("maturity", maturity, "canonical_recommendation_maturity")}; неопределённость: ${displayEnum("uncertainty", uncertainty, "uncertainty_state")}; ${demand}`];
    }
    return ["P2 — ПРОВЕРИТЬ ПЕРЕД ВНЕДРЕНИЕМ", `рекомендация: ${displayEnum("structuralAction", action, "canonical_structural_action")}; готовность: ${displayEnum("maturity", maturity, "canonical_recommendation_maturity")}; неопределённость: ${displayEnum("uncertainty", uncertainty, "uncertainty_state")}; ${demand}`];
  }
  if (["KEEP_EXISTING_STRUCTURE", "ROUTE_TO_EXISTING_PAGE_AS_SUBTASK"].includes(action)) {
    return ["P3 — СОХРАНИТЬ / ОТНЕСТИ К СТРАНИЦЕ", `рекомендация: ${displayEnum("structuralAction", action, "canonical_structural_action")}; готовность: ${displayEnum("maturity", maturity, "canonical_recommendation_maturity")}; неопределённость: ${displayEnum("uncertainty", uncertainty, "uncertainty_state")}; ${demand}`];
  }
  if (["NO_STANDALONE_PAGE", "OUTSIDE_SCOPE_NO_ACTION"].includes(action)) {
    return ["P4 — БЕЗ ОТДЕЛЬНОЙ СТРАНИЦЫ", `рекомендация: ${displayEnum("structuralAction", action, "canonical_structural_action")}; граница предложения: ${displayEnum("businessScope", row.canonical_business_scope_state, "canonical_business_scope_state")}; ${demand}`];
  }
  return ["P2 — ПРОВЕРИТЬ ПЕРЕД ВНЕДРЕНИЕМ", `статус: ${displayEnum("semanticStatus", state, "final_semantic_state")}; рекомендация: ${displayEnum("structuralAction", action, "canonical_structural_action")}; готовность: ${displayEnum("maturity", maturity, "canonical_recommendation_maturity")}; неопределённость: ${displayEnum("uncertainty", uncertainty, "uncertainty_state")}; ${demand}`];
}

function colLetter(index) {
  let value = index + 1;
  let result = "";
  while (value > 0) {
    const remainder = (value - 1) % 26;
    result = String.fromCharCode(65 + remainder) + result;
    value = Math.floor((value - 1) / 26);
  }
  return result;
}

function styleHeaderBands(sheet, lastRow, lastCol) {
  const headerRanges = [
    ["A1:D1", "#17365D"],
    ["E1:N1", "#0F6B78"],
    ["O1:U1", "#245A9A"],
    ["V1:AC1", "#5B3F8C"],
    [`AD1:${colLetter(lastCol - 1)}1`, "#374151"],
  ];
  for (const [address, fill] of headerRanges) {
    sheet.getRange(address).format = {
      fill,
      font: { bold: true, color: "#FFFFFF", size: 10 },
      wrapText: true,
      verticalAlignment: "center",
    };
  }
  sheet.getRangeByIndexes(0, 0, lastRow, lastCol).format.font = { name: "Arial", size: 9 };
  sheet.getRangeByIndexes(0, 0, lastRow, lastCol).format.verticalAlignment = "top";
  sheet.getRangeByIndexes(0, 0, lastRow, lastCol).format.borders = {
    insideHorizontal: { style: "thin", color: "#E5E7EB" },
  };
  sheet.getRangeByIndexes(0, 0, 1, lastCol).format.rowHeight = 42;
  if (lastRow > 1) sheet.getRangeByIndexes(1, 0, lastRow - 1, lastCol).format.rowHeight = 30;
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(2);
  sheet.showGridLines = false;
}

function setColumnWidths(sheet, widths, rowCount) {
  widths.forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, rowCount, 1).format.columnWidth = width;
  });
}

function addStatusFormatting(sheet, rowCount, statusColumn, activeColumn, pageColumn, priorityColumn) {
  if (rowCount < 2) return;
  const last = rowCount;
  sheet.getRange(`${statusColumn}2:${statusColumn}${last}`).conditionalFormats.add("containsText", {
    text: "Требуется проверка в обычном поиске Яндекса",
    format: { fill: "#FEE2E2", font: { color: "#991B1B", bold: true } },
  });
  sheet.getRange(`${statusColumn}2:${statusColumn}${last}`).conditionalFormats.add("containsText", {
    text: "внедрение требует дополнительной проверки",
    format: { fill: "#FEF3C7", font: { color: "#92400E", bold: true } },
  });
  sheet.getRange(`${activeColumn}2:${activeColumn}${last}`).conditionalFormats.add("containsText", {
    text: "ДА",
    format: { fill: "#DCFCE7", font: { color: "#166534", bold: true } },
  });
  sheet.getRange(`${pageColumn}2:${pageColumn}${last}`).conditionalFormats.add("containsText", {
    text: "НЕТ ОТДЕЛЬНОЙ СТРАНИЦЫ",
    format: { fill: "#F3F4F6", font: { color: "#4B5563" } },
  });
  sheet.getRange(`${priorityColumn}2:${priorityColumn}${last}`).conditionalFormats.add("beginsWith", {
    text: "P0",
    format: { fill: "#FEE2E2", font: { color: "#991B1B", bold: true } },
  });
  sheet.getRange(`${priorityColumn}2:${priorityColumn}${last}`).conditionalFormats.add("beginsWith", {
    text: "P1",
    format: { fill: "#DCFCE7", font: { color: "#166534", bold: true } },
  });
}

function addTable(sheet, rowCount, colCount, name) {
  const table = sheet.tables.add(`A1:${colLetter(colCount - 1)}${rowCount}`, true, name);
  table.style = "TableStyleMedium2";
  table.showFilterButton = true;
  table.showBandedRows = true;
}

const args = parseArgs(process.argv.slice(2));
if (!args["repo-root"] || !args.output) {
  throw new Error("Usage: materialize_standalone_semantic_core.mjs --repo-root <repo> --output <xlsx> [--preview-dir <dir>] [--runtime-report <json>]");
}

const repoRoot = path.resolve(args["repo-root"]);
const outputPath = path.resolve(args.output);
const previewDir = args["preview-dir"] ? path.resolve(args["preview-dir"]) : null;
const runtimeReportPath = args["runtime-report"] ? path.resolve(args["runtime-report"]) : null;
const jobRoot = path.join(repoRoot, "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK");
const files = {
  master: path.join(jobRoot, "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"),
  units: path.join(jobRoot, "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"),
  step8: path.join(jobRoot, "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv"),
};

const [master, units, step8] = await Promise.all([
  fs.readFile(files.master, "utf8").then(parseTsv),
  fs.readFile(files.units, "utf8").then(parseTsv),
  fs.readFile(files.step8, "utf8").then(parseTsv),
]);

const masterByPhrase = new Map(master.map((row) => [normalize(row.phrase), row]));
const step8ByPhrase = new Map(step8.map((row) => [normalize(row.phrase), row]));
const unitsById = new Map(units.map((row) => [row.structural_unit_id, row]));
if (master.length !== 2840 || masterByPhrase.size !== 2840) throw new Error(`Stage-5 phrase invariant failed: rows=${master.length}, unique=${masterByPhrase.size}`);
if (step8.length !== 2840 || step8ByPhrase.size !== 2840) throw new Error(`Step-08 phrase invariant failed: rows=${step8.length}, unique=${step8ByPhrase.size}`);
if (units.length !== 168 || unitsById.size !== 168) throw new Error(`Unit invariant failed: rows=${units.length}, unique=${unitsById.size}`);
for (const key of masterByPhrase.keys()) if (!step8ByPhrase.has(key)) throw new Error(`Missing Step-08 row: ${key}`);

const joined = master.map((row) => {
  const demand = step8ByPhrase.get(normalize(row.phrase));
  const resultCount = asInteger(demand.max_result_count, "max_result_count", row.phrase);
  const associationCount = asInteger(demand.max_association_count, "max_association_count", row.phrase);
  const sourceOccurrences = asInteger(demand.source_occurrences, "source_occurrences", row.phrase);
  const active = ACTIVE_STATES.has(row.final_semantic_state);
  const assigned = ASSIGNED_STATES.has(row.final_semantic_state);
  const unit = assigned ? unitsById.get(row.final_structural_unit_id) : null;
  if (assigned && !unit) throw new Error(`Missing unit authority for ${row.phrase}: ${row.final_structural_unit_id}`);
  if (active && resultCount <= 0) throw new Error(`Active phrase without positive result count: ${row.phrase}`);
  return {
    ...row,
    id: phraseId(row.phrase),
    active,
    assigned,
    resultCount,
    associationCount,
    sourceOccurrences,
    sourceIds: demand.source_ids,
    demandProvenance: demand.provenance,
    searchStageDisposition: demand.search_stage_disposition,
    nextResolutionRoute: demand.next_resolution_route,
    routeReason: demand.route_reason,
    snapshotDate: sourceSnapshotDate(demand.source_ids),
    frequencyRole: frequencyRole(resultCount, associationCount),
    unit,
  };
});

const activeRows = joined.filter((row) => row.active);
const assignedRows = joined.filter((row) => row.assigned);
const searchRequiredRows = joined.filter((row) => row.final_semantic_state === "SEARCH_REQUIRED");
if (activeRows.length !== 2332 || assignedRows.length !== 2313 || searchRequiredRows.length !== 19) {
  throw new Error(`Active-state invariant failed: active=${activeRows.length}, assigned=${assignedRows.length}, search_required=${searchRequiredRows.length}`);
}

const membersByUnit = new Map();
for (const row of assignedRows) {
  if (!membersByUnit.has(row.final_structural_unit_id)) membersByUnit.set(row.final_structural_unit_id, []);
  membersByUnit.get(row.final_structural_unit_id).push(row);
}
if (membersByUnit.size !== 168) throw new Error(`Assigned unit coverage failed: ${membersByUnit.size}`);

const representativeByUnit = new Map();
for (const [unitId, members] of membersByUnit.entries()) representativeByUnit.set(unitId, selectRepresentative(unitId, members));
for (const row of joined) {
  const representative = row.assigned ? representativeByUnit.get(row.final_structural_unit_id) : null;
  row.representative = representative;
  row.clusterName = representative ? capitalize(representative.phrase) : missingText(row, "final_structural_unit_id");
  row.clientTask = representative
    ? clientTask(row.canonical_intent_type, representative.phrase)
    : row.final_semantic_state === "SEARCH_REQUIRED"
      ? "Пользовательская задача будет определена после проверки в обычном поиске Яндекса"
      : "Пользовательская задача не применяется к строке вне рабочего ядра";
  row.targetDisplay = targetDisplay(row);
}

const clusterRanks = assignRanks(activeRows, (row) => row.final_structural_unit_id);
const pageRanks = assignRanks(activeRows, (row) => row.targetDisplay);
for (const row of joined) {
  row.clusterRank = clusterRanks.get(row.id) ?? null;
  row.pageRank = pageRanks.get(row.id) ?? null;
  [row.priority, row.priorityBasis] = priorityFor(row);
  if (row.clusterRank) row.priorityBasis += `; место внутри кластера = ${row.clusterRank}`;
}

const uniqueFinalUrls = new Set(assignedRows.filter((row) => row.final_primary_page).map((row) => row.final_primary_page));
const blankActionCounts = new Map();
for (const row of assignedRows.filter((item) => !item.final_primary_page)) {
  blankActionCounts.set(row.canonical_structural_action, (blankActionCounts.get(row.canonical_structural_action) ?? 0) + 1);
}
const expectedBlank = { NO_STANDALONE_PAGE: 246, OUTSIDE_SCOPE_NO_ACTION: 115, DEFER_PENDING_EVIDENCE: 32 };
for (const [key, expected] of Object.entries(expectedBlank)) {
  if (blankActionCounts.get(key) !== expected) throw new Error(`No-page invariant failed for ${key}: ${blankActionCounts.get(key)} != ${expected}`);
}
if (uniqueFinalUrls.size !== 60) throw new Error(`Final URL invariant failed: ${uniqueFinalUrls.size}`);

const phraseHeaders = [
  "ID фразы", "Поисковая фраза", "Статус фразы", "В рабочем ядре", "Регион", "Код региона", "Устройства",
  "Число запросов — популярные", "Число запросов — похожие", "Тип статистики Вордстата", "Правило объединения наблюдений", "Идентификаторы источников Вордстата",
  "Количество исходных наблюдений", "Дата сбора / снимка", "ID структурной единицы", "Кластер", "Основной запрос кластера",
  "Пользовательская задача", "Интент", "Граница бизнеса", "Уверенность назначения", "URL до финальной сверки",
  "Финальная целевая страница", "Поддерживающие страницы", "Роль страницы", "Рекомендация", "Готовность решения",
  "Неопределённость", "Что нужно для пересмотра", "Ранг внутри кластера", "Ранг внутри страницы",
  "Операционный приоритет", "Основание приоритета", "Комментарий / граница вывода", "Происхождение данных",
];

function phraseMatrix(rows) {
  return rows.map((row) => [
    row.id,
    row.phrase,
    displayEnum("semanticStatus", row.final_semantic_state, "final_semantic_state"),
    row.active ? "ДА" : "НЕТ",
    "Москва",
    213,
    "Все устройства",
    row.resultCount,
    row.associationCount,
    `${METRIC_DISPLAY}; ${displayEnum("frequencyRole", row.frequencyRole, "frequency_role")}`,
    AGGREGATION_DISPLAY,
    row.sourceIds,
    row.sourceOccurrences,
    row.snapshotDate,
    missingText(row, "final_structural_unit_id"),
    row.clusterName,
    row.representative?.phrase ?? missingText(row, "final_structural_unit_id"),
    row.clientTask,
    row.canonical_intent_type ? displayEnum("intent", row.canonical_intent_type, "canonical_intent_type") : "Не применимо по финальному решению",
    row.canonical_business_scope_state ? displayEnum("businessScope", row.canonical_business_scope_state, "canonical_business_scope_state") : "Не применимо по финальному решению",
    displayEnum("confidence", row.canonical_final_confidence || row.semantic_confidence, "confidence"),
    row.step11_target_url || (row.active ? "НЕ БЫЛО СОХРАНЁННОГО URL" : "НЕ ПРИМЕНИМО — ВНЕ АКТИВНОГО ЯДРА"),
    row.targetDisplay,
    row.final_supporting_pages || (row.assigned ? "НЕТ КАНОНИЧЕСКОЙ ПОДДЕРЖИВАЮЩЕЙ СТРАНИЦЫ" : missingText(row, "final_supporting_pages")),
    row.canonical_unit_page_role ? displayEnum("pageRole", row.canonical_unit_page_role, "canonical_unit_page_role") : "Не применимо по финальному решению",
    row.canonical_structural_action ? displayEnum("structuralAction", row.canonical_structural_action, "canonical_structural_action") : "Не применимо по финальному решению",
    row.canonical_recommendation_maturity ? displayEnum("maturity", row.canonical_recommendation_maturity, "canonical_recommendation_maturity") : "Не применимо по финальному решению",
    displayEnum("uncertainty", row.uncertainty_state, "uncertainty_state"),
    reopenDisplay(row),
    row.clusterRank,
    row.pageRank,
    row.priority,
    row.priorityBasis,
    [routeReasonDisplay(row), CLAIM_BOUNDARY].join(" | "),
    `Финальное семантическое решение Stage 5: ${row.authority_lineage || "FINAL_SEMANTIC_MASTER"} | Данные спроса Step 08: ${row.demandProvenance}`,
  ]);
}

const clusterHeaders = [
  "ID структурной единицы", "Кластер", "Основной запрос кластера", "Число запросов у основного запроса",
  "Количество активных фраз", "Максимальное число запросов", "Медианное число запросов", "Сумма числа запросов (не считать объёмом рынка)",
  "Ведущие фразы", "Пользовательская задача", "Интент", "Граница бизнеса", "Финальная страница / группа",
  "Поддерживающие страницы", "Роль страницы", "Рекомендация", "Готовность решения", "Уверенность", "Неопределённость",
  "Что нужно для пересмотра", "Операционный приоритет", "Основание приоритета", "Граница метрики",
  "Источник решения (файл)", "Приоритетный источник решения (файл)",
];

const clusterRows = [...membersByUnit.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([unitId, members]) => {
  const unit = unitsById.get(unitId);
  const representative = representativeByUnit.get(unitId);
  const sorted = [...members].sort((a, b) => b.resultCount - a.resultCount || a.phrase.localeCompare(b.phrase, "ru"));
  const prioritySource = sorted.sort((a, b) => a.priority.localeCompare(b.priority) || a.clusterRank - b.clusterRank)[0];
  return {
    unitId,
    values: [
      unitId,
      capitalize(representative.phrase),
      representative.phrase,
      representative.resultCount,
      members.length,
      Math.max(...members.map((row) => row.resultCount)),
      median(members.map((row) => row.resultCount)),
      members.reduce((sum, row) => sum + row.resultCount, 0),
      [...members].sort((a, b) => b.resultCount - a.resultCount || a.phrase.localeCompare(b.phrase, "ru")).slice(0, 5).map((row) => `${row.phrase} [${row.resultCount}]`).join("; "),
      clientTask(unit.intent_type, representative.phrase),
      displayEnum("intent", unit.intent_type, "intent_type"),
      displayEnum("businessScope", unit.business_scope_state, "business_scope_state"),
      unit.final_primary_page || `НЕТ ОТДЕЛЬНОЙ СТРАНИЦЫ — ${displayEnum("structuralAction", unit.structural_action, "structural_action")}`,
      unit.final_supporting_pages || "НЕТ КАНОНИЧЕСКОЙ ПОДДЕРЖИВАЮЩЕЙ СТРАНИЦЫ",
      displayEnum("pageRole", unit.unit_page_role, "unit_page_role"),
      displayEnum("structuralAction", unit.structural_action, "structural_action"),
      displayEnum("maturity", unit.recommendation_maturity, "recommendation_maturity"),
      displayEnum("confidence", unit.final_confidence, "final_confidence"),
      displayEnum("uncertainty", unit.uncertainty_state, "uncertainty_state"),
      unitReopenDisplay(unit),
      prioritySource.priority,
      `Рекомендация: ${displayEnum("structuralAction", unit.structural_action, "structural_action")}; готовность: ${displayEnum("maturity", unit.recommendation_maturity, "recommendation_maturity")}; неопределённость: ${displayEnum("uncertainty", unit.uncertainty_state, "uncertainty_state")}; число запросов у основного запроса = ${representative.resultCount}`,
      "Сумма числа запросов — неаддитивный относительный индикатор: показываемые запросы могут пересекаться",
      unit.source_authority,
      unit.higher_precedence_authority === "NONE" ? "Дополнительного приоритетного источника нет" : unit.higher_precedence_authority,
    ],
  };
});

const pageGroups = new Map();
for (const row of assignedRows) {
  if (!pageGroups.has(row.targetDisplay)) pageGroups.set(row.targetDisplay, []);
  pageGroups.get(row.targetDisplay).push(row);
}
if (pageGroups.size !== 63) throw new Error(`Page summary invariant failed: ${pageGroups.size}`);
const pageHeaders = [
  "Финальная страница / группа", "Тип строки", "Количество фраз", "Количество кластеров", "Максимальное число запросов",
  "Медианное число запросов", "Сумма числа запросов (не считать объёмом рынка)", "Ведущие фразы", "Кластеры", "Роли страницы",
  "Рекомендации", "Готовность", "Неопределённость", "Операционный приоритет", "Основание приоритета", "Комментарий",
];
const pageRows = [...pageGroups.entries()].sort(([a], [b]) => {
  const aGroup = a.startsWith("НЕТ ОТДЕЛЬНОЙ");
  const bGroup = b.startsWith("НЕТ ОТДЕЛЬНОЙ");
  if (aGroup !== bGroup) return aGroup ? 1 : -1;
  return a.localeCompare(b, "ru");
}).map(([target, members]) => {
  const sorted = [...members].sort((a, b) => b.resultCount - a.resultCount || a.phrase.localeCompare(b.phrase, "ru"));
  const bestPriority = [...members].sort((a, b) => a.priority.localeCompare(b.priority) || a.pageRank - b.pageRank)[0];
  return [
    target,
    target.startsWith("НЕТ ОТДЕЛЬНОЙ") ? "УПРАВЛЯЕМАЯ ГРУППА БЕЗ URL" : "ФИНАЛЬНЫЙ URL",
    members.length,
    new Set(members.map((row) => row.final_structural_unit_id)).size,
    Math.max(...members.map((row) => row.resultCount)),
    median(members.map((row) => row.resultCount)),
    members.reduce((sum, row) => sum + row.resultCount, 0),
    sorted.slice(0, 8).map((row) => `${row.phrase} [${row.resultCount}]`).join("; "),
    uniqueSorted(members.map((row) => row.clusterName)).join("; "),
    uniqueSorted(members.map((row) => displayEnum("pageRole", row.canonical_unit_page_role, "canonical_unit_page_role"))).join("; "),
    uniqueSorted(members.map((row) => displayEnum("structuralAction", row.canonical_structural_action, "canonical_structural_action"))).join("; "),
    uniqueSorted(members.map((row) => displayEnum("maturity", row.canonical_recommendation_maturity, "canonical_recommendation_maturity"))).join("; "),
    uniqueSorted(members.map((row) => displayEnum("uncertainty", row.uncertainty_state, "uncertainty_state"))).join("; "),
    bestPriority.priority,
    `Лучший операционный класс в группе; максимальное число запросов = ${Math.max(...members.map((row) => row.resultCount))}; это не оценка бизнес-приоритета`,
    target.startsWith("НЕТ ОТДЕЛЬНОЙ")
      ? "Пустой Stage-5 URL сохранён намеренно; причина указана в названии группы"
      : "Карта назначения из Stage-5; наличие нескольких кластеров на URL само по себе не доказывает каннибализацию",
  ];
});

const searchHeaders = [
  "ID фразы", "Поисковая фраза", "Число запросов — популярные", "Число запросов — похожие", "Регион и устройства", "Тип статистики Вордстата",
  "Статус", "Неопределённость", "Статус перед проверкой в Яндексе", "Следующий маршрут проверки", "Причина маршрута",
  "ID структурной единицы", "Финальная страница", "Что нужно для пересмотра", "Операционный приоритет",
  "Граница вывода", "Идентификаторы источников Вордстата", "Происхождение данных",
];
const searchMatrix = searchRequiredRows.sort((a, b) => b.resultCount - a.resultCount || a.phrase.localeCompare(b.phrase, "ru")).map((row) => [
  row.id,
  row.phrase,
  row.resultCount,
  row.associationCount,
  "Москва (код региона 213), все устройства",
  `${METRIC_DISPLAY}; ${displayEnum("frequencyRole", row.frequencyRole, "frequency_role")}`,
  displayEnum("semanticStatus", row.final_semantic_state, "final_semantic_state"),
  displayEnum("uncertainty", row.uncertainty_state, "uncertainty_state"),
  displayEnum("searchDisposition", row.searchStageDisposition, "search_stage_disposition"),
  displayEnum("resolutionRoute", row.nextResolutionRoute, "next_resolution_route"),
  routeReasonDisplay(row),
  "НЕ НАЗНАЧЕНО — требуется проверка в обычном поиске Яндекса",
  "НЕ НАЗНАЧЕНО — требуется проверка в обычном поиске Яндекса",
  reopenDisplay(row),
  row.priority,
  [routeReasonDisplay(row), CLAIM_BOUNDARY].join(" | "),
  row.sourceIds,
  `Финальное семантическое решение Stage 5: ${row.authority_lineage || "FINAL_SEMANTIC_MASTER"} | Данные спроса Step 08: ${row.demandProvenance}`,
]);

const dictionaryHeaders = ["Раздел", "Технический код", "Русское отображение", "Значение / пояснение", "Как использовать", "Источник / граница"];

function dictionaryEnumRows(section, field, displayMap, usage, source) {
  return Object.entries(displayMap).map(([code, label]) => [
    section,
    code,
    label,
    "Понятное русское отображение внутреннего значения; технический код приведён в соседней колонке",
    usage,
    source,
  ]);
}

const dictionaryRows = [
  ["Сводка", "—", "Всего уникальных фраз", 2840, "Полный инвентарь находится на листе 01_Все_фразы", "Финальная семантическая таблица Stage 5"],
  ["Сводка", "—", "Активное ядро", 2332, "Основной рабочий список находится на листе 02_Активное_ядро", "Назначенные фразы и очередь проверки в Яндексе"],
  ["Сводка", "—", "Назначено", 2313, "Каждая строка имеет каноническую структурную единицу", "Финальная семантическая таблица Stage 5"],
  ["Сводка", "SEARCH_REQUIRED", "Требуется проверка в обычном поиске Яндекса", 19, "Отдельная очередь находится на пятом листе; кластер и URL не выдумываются", "Финальная семантическая таблица Stage 5"],
  ["Сводка", "—", "Канонические кластеры", 168, "Одна строка на листе 03_Кластеры", "Таблица структурных единиц Stage 5"],
  ["Сводка", "—", "Финальные URL", 60, "Дополнительно показаны три управляемые группы без URL", "Поле финальной целевой страницы Stage 5"],
  ["Частотность", METRIC_TYPE, METRIC_DISPLAY, "Популярные запросы, содержащие заданную фразу, и похожие запросы из раздела «Топы запросов»", "Использовать для грубой сортировки и сравнения внутри принятого распределения", "Вордстат; Москва, код 213; все устройства; без операторов"],
  ["Частотность", "result count", "Число запросов — популярные", "Сохранённое число для популярного запроса с точным текстом строки", "Основной числовой показатель спроса в книге; не точная частотность", "Данные спроса Step 08"],
  ["Частотность", "association count", "Число запросов — похожие", "Сохранённое число для похожего запроса с точным текстом строки", "Вспомогательный показатель происхождения фразы", "Данные спроса Step 08"],
  ["Частотность", AGGREGATION_RULE, AGGREGATION_DISPLAY, "Повторные наблюдения одной фразы не складываются", "Сравнивать фразы без двойного счёта повторных источников", "Правило объединения Step 08"],
  ["Частотность", "—", "Сумма числа запросов (не считать объёмом рынка)", "Сумма строк внутри кластера или страницы", "Только относительный индикатор: показываемые запросы могут пересекаться", "Не является уникальным объёмом рынка"],
  ["Частотность", "GetTop / DEVICE_ALL / results[] / associations[] / phrase / count", "Технические обозначения API", "Нужны для воспроизводимости получения данных, но не используются как основной язык рабочих листов", "Смотреть только при техническом аудите происхождения данных", "https://aistudio.yandex.ru/ru/docs/search-api/operations/wordstat-gettop"],
  ["Репрезентант", "—", "Основной запрос кластера", "Реальная фраза-член кластера, выбранная воспроизводимо по смысловой центральности, читаемости и числу запросов", "Название кластера повторяет эту русскую фразу; точечные уточнения выбирают только другую реальную фразу того же кластера", "Материализатор; принадлежность Stage 5 не меняется"],
  ["Ранг", "—", "Ранг внутри кластера", "Убывание числа популярных запросов; при равенстве — алфавит фразы и стабильный ID", "Это относительный ранг по статистике без операторов, не ранг точного спроса", "Производное поле"],
  ["Ранг", "—", "Ранг внутри страницы", "То же правило внутри финального URL или управляемой группы без URL", "Нерешённые фразы не ранжируются по странице", "Производное поле"],
  ["Приоритет", "P0", "Сначала снять неопределённость или провести проверку в Яндексе", "Есть блокирующая неопределённость, отложенное доказательство или нерешённое назначение", "Сначала разрешить указанную причину", "Не означает высокий коммерческий потенциал"],
  ["Приоритет", "P1", "Готовое изменение", "Финальное решение требует расширения существующей страницы", "Планировать исполнение только вместе с отдельным руководством специалиста", "Не заменяет руководство по внедрению"],
  ["Приоритет", "P2", "Проверить перед внедрением", "Физическое изменение ещё не имеет полностью финальной зрелости", "Выполнить указанную проверку", "Производное поле"],
  ["Приоритет", "P3", "Сохранить или отнести к существующей странице", "Существующая структура сохраняется либо фраза является подзадачей текущей страницы", "Не создавать отдельную страницу только из-за фразы", "Финальное структурное действие Stage 5"],
  ["Приоритет", "P4", "Без отдельной страницы", "Отдельная страница не нужна или тема вне предложения", "Не заполнять URL искусственно", "Финальное структурное действие Stage 5"],
  ["Приоритет", "P5", "Вне рабочего ядра", "Проверка отложена или фраза исключена", "Сохранять для аудита, не внедрять", "Финальный статус Stage 5"],
  ["Происхождение данных", "source IDs", "Идентификаторы источников Вордстата", "Идентификаторы первого и дополнительного проходов", "Фильтровать и трассировать происхождение числа запросов", "Данные спроса Step 08"],
  ["Происхождение данных", "source occurrences", "Количество исходных наблюдений", "Сколько исходных наблюдений содержали эту фразу", "Показывает повторное обнаружение без суммирования частотности", "Данные спроса Step 08"],
  ["Власть решения", "Stage 5", "Финальное семантическое решение", "Определяет статус, кластер, интент, границу предложения, страницу и действие", "Не заменять старой материализацией Step 19", "Финальная семантическая таблица и таблица структурных единиц"],
  ...dictionaryEnumRows("Статус фразы", "final_semantic_state", DISPLAY_MAPS.semanticStatus, "Фильтровать рабочее ядро и очередь проверки; русское значение является основным отображением", "Финальная семантическая таблица Stage 5"),
  ...dictionaryEnumRows("Интент", "canonical_intent_type", DISPLAY_MAPS.intent, "Использовать вместе с пользовательской задачей и границей предложения", "Финальная семантическая таблица Stage 5"),
  ...dictionaryEnumRows("Граница предложения", "canonical_business_scope_state", DISPLAY_MAPS.businessScope, "Не создавать страницу за пределами подтверждённого предложения", "Финальная семантическая таблица Stage 5"),
  ...dictionaryEnumRows("Роль страницы", "canonical_unit_page_role", DISPLAY_MAPS.pageRole, "Показывает роль владельца или поддерживающей страницы", "Таблица структурных единиц Stage 5"),
  ...dictionaryEnumRows("Рекомендация", "canonical_structural_action", DISPLAY_MAPS.structuralAction, "Не путать аналитическое назначение с физической CMS-задачей", "Финальная семантическая таблица Stage 5"),
  ...dictionaryEnumRows("Готовность решения", "canonical_recommendation_maturity", DISPLAY_MAPS.maturity, "Проверять перед физическим внедрением", "Финальная семантическая таблица Stage 5"),
  ...dictionaryEnumRows("Неопределённость", "uncertainty_state", DISPLAY_MAPS.uncertainty, "Следовать правилу пересмотра; не скрывать нерешённое", "Stage 5 и сохранённый семантический handoff"),
  ...dictionaryEnumRows("Уверенность", "confidence", DISPLAY_MAPS.confidence, "Не использовать как замену доказательствам", "Stage 5"),
  ...dictionaryEnumRows("Статус перед проверкой", "search_stage_disposition", DISPLAY_MAPS.searchDisposition, "Определяет маршрут на этапе обычного поиска Яндекса", "Сохранённый семантический handoff Step 08"),
  ...dictionaryEnumRows("Маршрут проверки", "next_resolution_route", DISPLAY_MAPS.resolutionRoute, "Показывает реальное следующее действие для нерешённой фразы", "Сохранённый семантический handoff Step 08"),
  ...dictionaryEnumRows("Наличие статистики", "frequency_role", DISPLAY_MAPS.frequencyRole, "Различает популярные и похожие запросы без технических API-ярлыков", "Данные спроса Step 08"),
  ...dictionaryEnumRows("Пробел содержания", "canonical_gap_type", DISPLAY_MAPS.gapType, "Не превращать недостаток доказательств в готовую задачу", "Stage 5"),
  ...dictionaryEnumRows("Состояние содержания", "canonical_content_enhancement_state", DISPLAY_MAPS.contentEnhancement, "Отделять подтверждённое улучшение от неоценённого или недоказанного", "Stage 5"),
  ["Методика", "—", "Официальная терминология интерфейса Вордстата", "Вордстат, Топы запросов, популярные запросы, похожие запросы, число запросов, регион, тип устройства", "Использовать как основной язык клиентских листов", "https://yandex.ru/support2/wordstat/ru/interface/new"],
  ["Методика", "—", "Операторы Вордстата", "Сбор выполнен без операторов, поэтому показатель нельзя называть точной частотностью", "Сохранять границу вывода", "https://yandex.ru/support2/wordstat/ru/content/operators"],
  ["Методика", "—", "Кластеризация и назначение страниц", "Разделение фразы, кластера и страницы", "Не создавать отдельную страницу автоматически для каждой фразы", "https://www.semrush.com/blog/keyword-clustering/ | https://www.semrush.com/blog/keyword-mapping/"],
  ["Методика", "—", "Интент и граница каннибализации", "Интент важнее одного числа запросов; пересечение не равно доказанному ущербу", "Не рекомендовать объединение/удаление без доказательств", "https://ahrefs.com/blog/keyword-intent/ | https://ahrefs.com/blog/keyword-cannibalization/"],
];

const workbook = Workbook.create();
const allSheet = workbook.worksheets.add("01_Все_фразы");
const activeSheet = workbook.worksheets.add("02_Активное_ядро");
const clusterSheet = workbook.worksheets.add("03_Кластеры");
const pageSheet = workbook.worksheets.add("04_Страницы");
const searchSheet = workbook.worksheets.add("05_Проверка_в_Яндексе");
const dictionarySheet = workbook.worksheets.add("06_Справочник");

const sortedAll = [...joined].sort((a, b) => a.phrase.localeCompare(b.phrase, "ru"));
const sortedActive = [...activeRows].sort((a, b) => a.final_structural_unit_id.localeCompare(b.final_structural_unit_id) || (a.clusterRank ?? 999999) - (b.clusterRank ?? 999999) || a.phrase.localeCompare(b.phrase, "ru"));

allSheet.getRangeByIndexes(0, 0, sortedAll.length + 1, phraseHeaders.length).values = [phraseHeaders, ...phraseMatrix(sortedAll)];
activeSheet.getRangeByIndexes(0, 0, sortedActive.length + 1, phraseHeaders.length).values = [phraseHeaders, ...phraseMatrix(sortedActive)];
clusterSheet.getRangeByIndexes(0, 0, clusterRows.length + 1, clusterHeaders.length).values = [clusterHeaders, ...clusterRows.map((row) => row.values)];
pageSheet.getRangeByIndexes(0, 0, pageRows.length + 1, pageHeaders.length).values = [pageHeaders, ...pageRows];
searchSheet.getRangeByIndexes(0, 0, searchMatrix.length + 1, searchHeaders.length).values = [searchHeaders, ...searchMatrix];
dictionarySheet.getRangeByIndexes(0, 0, dictionaryRows.length + 1, dictionaryHeaders.length).values = [dictionaryHeaders, ...dictionaryRows];

// Formula-driven ranks on the main working sheet. The complete inventory keeps the same deterministic values as a static audit view.
const activeEnd = sortedActive.length + 1;
const rankFormulas = sortedActive.map((row, index) => {
  const excelRow = index + 2;
  if (row.final_semantic_state === "SEARCH_REQUIRED") return ["", ""];
  return [
    `=COUNTIFS($O$2:$O$${activeEnd},$O${excelRow},$H$2:$H$${activeEnd},\">\"&$H${excelRow})+COUNTIFS($O$2:$O$${activeEnd},$O${excelRow},$H$2:$H$${activeEnd},$H${excelRow},$B$2:$B$${activeEnd},\"<\"&$B${excelRow})+1`,
    `=COUNTIFS($W$2:$W$${activeEnd},$W${excelRow},$H$2:$H$${activeEnd},\">\"&$H${excelRow})+COUNTIFS($W$2:$W$${activeEnd},$W${excelRow},$H$2:$H$${activeEnd},$H${excelRow},$B$2:$B$${activeEnd},\"<\"&$B${excelRow})+1`,
  ];
});
activeSheet.getRange(`AD2:AE${activeEnd}`).formulas = rankFormulas;

// Formula-driven count/sum columns in cluster and page summaries keep the summaries auditable inside Excel.
clusterSheet.getRange(`E2:E${clusterRows.length + 1}`).formulas = clusterRows.map((_, index) => [[`=COUNTIF('02_Активное_ядро'!$O$2:$O$${activeEnd},$A${index + 2})`][0]]);
clusterSheet.getRange(`H2:H${clusterRows.length + 1}`).formulas = clusterRows.map((_, index) => [[`=SUMIF('02_Активное_ядро'!$O$2:$O$${activeEnd},$A${index + 2},'02_Активное_ядро'!$H$2:$H$${activeEnd})`][0]]);
pageSheet.getRange(`C2:C${pageRows.length + 1}`).formulas = pageRows.map((_, index) => [[`=COUNTIF('02_Активное_ядро'!$W$2:$W$${activeEnd},$A${index + 2})`][0]]);
pageSheet.getRange(`G2:G${pageRows.length + 1}`).formulas = pageRows.map((_, index) => [[`=SUMIF('02_Активное_ядро'!$W$2:$W$${activeEnd},$A${index + 2},'02_Активное_ядро'!$H$2:$H$${activeEnd})`][0]]);

styleHeaderBands(allSheet, sortedAll.length + 1, phraseHeaders.length);
styleHeaderBands(activeSheet, sortedActive.length + 1, phraseHeaders.length);
styleHeaderBands(clusterSheet, clusterRows.length + 1, clusterHeaders.length);
styleHeaderBands(pageSheet, pageRows.length + 1, pageHeaders.length);
styleHeaderBands(searchSheet, searchMatrix.length + 1, searchHeaders.length);
styleHeaderBands(dictionarySheet, dictionaryRows.length + 1, dictionaryHeaders.length);

setColumnWidths(allSheet, [19, 42, 22, 14, 14, 11, 15, 18, 20, 34, 34, 24, 16, 21, 34, 38, 38, 42, 24, 34, 22, 44, 48, 44, 34, 38, 34, 26, 48, 15, 15, 38, 52, 62, 64], sortedAll.length + 1);
setColumnWidths(activeSheet, [19, 42, 22, 14, 14, 11, 15, 18, 20, 34, 34, 24, 16, 21, 34, 38, 38, 42, 24, 34, 22, 44, 48, 44, 34, 38, 34, 26, 48, 15, 15, 38, 52, 62, 64], sortedActive.length + 1);
setColumnWidths(clusterSheet, [38, 38, 38, 20, 18, 18, 18, 23, 72, 48, 24, 34, 50, 44, 34, 38, 34, 22, 24, 48, 38, 54, 54, 38, 38], clusterRows.length + 1);
setColumnWidths(pageSheet, [58, 27, 17, 18, 20, 18, 23, 84, 72, 54, 54, 46, 36, 38, 50, 64], pageRows.length + 1);
setColumnWidths(searchSheet, [19, 46, 18, 20, 24, 36, 22, 28, 32, 40, 56, 36, 42, 48, 38, 64, 24, 70], searchMatrix.length + 1);
setColumnWidths(dictionarySheet, [24, 45, 55, 68, 68, 68], dictionaryRows.length + 1);

for (const sheet of [allSheet, activeSheet]) {
  sheet.getRange(`H2:I${sheet === allSheet ? sortedAll.length + 1 : sortedActive.length + 1}`).format.numberFormat = "#,##0";
  sheet.getRange(`M2:M${sheet === allSheet ? sortedAll.length + 1 : sortedActive.length + 1}`).format.numberFormat = "#,##0";
  sheet.getRange(`AD2:AE${sheet === allSheet ? sortedAll.length + 1 : sortedActive.length + 1}`).format.numberFormat = "#,##0";
  sheet.getRangeByIndexes(0, 0, sheet === allSheet ? sortedAll.length + 1 : sortedActive.length + 1, phraseHeaders.length).format.wrapText = true;
}
clusterSheet.getRange(`D2:H${clusterRows.length + 1}`).format.numberFormat = "#,##0";
pageSheet.getRange(`C2:G${pageRows.length + 1}`).format.numberFormat = "#,##0";
searchSheet.getRange(`C2:D${searchMatrix.length + 1}`).format.numberFormat = "#,##0";

addTable(allSheet, sortedAll.length + 1, phraseHeaders.length, "AllPhrasesTable");
addTable(activeSheet, sortedActive.length + 1, phraseHeaders.length, "ActiveCoreTable");
addTable(clusterSheet, clusterRows.length + 1, clusterHeaders.length, "ClustersTable");
addTable(pageSheet, pageRows.length + 1, pageHeaders.length, "PagesTable");
addTable(searchSheet, searchMatrix.length + 1, searchHeaders.length, "SearchRequiredTable");
addTable(dictionarySheet, dictionaryRows.length + 1, dictionaryHeaders.length, "DictionaryTable");

addStatusFormatting(allSheet, sortedAll.length + 1, "C", "D", "W", "AF");
addStatusFormatting(activeSheet, sortedActive.length + 1, "C", "D", "W", "AF");
searchSheet.getRange(`G2:G${searchMatrix.length + 1}`).conditionalFormats.add("containsText", {
  text: "Требуется проверка в обычном поиске Яндекса",
  format: { fill: "#FEE2E2", font: { color: "#991B1B", bold: true } },
});
clusterSheet.getRange(`U2:U${clusterRows.length + 1}`).conditionalFormats.add("beginsWith", {
  text: "P0",
  format: { fill: "#FEE2E2", font: { color: "#991B1B", bold: true } },
});
pageSheet.getRange(`N2:N${pageRows.length + 1}`).conditionalFormats.add("beginsWith", {
  text: "P0",
  format: { fill: "#FEE2E2", font: { color: "#991B1B", bold: true } },
});

const workbookInspect = await workbook.inspect({ kind: "sheet", include: "id,name", maxChars: 8000 });
const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "standalone semantic core formula error scan",
});

await fs.mkdir(path.dirname(outputPath), { recursive: true });
const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(outputPath);

// artifact-tool 2.8.6 currently omits documented freezePanes metadata during export.
// Apply a narrow, reproducible OpenXML view-only repair after artifact-tool authoring.
const freezePatcher = path.join(jobRoot, "tools/post_release_correction/patch_xlsx_freeze_panes.py");
const pythonRuntime = process.env.CODEX_PRIMARY_RUNTIME_PYTHON || "python3";
await execFileAsync(pythonRuntime, [freezePatcher, "--xlsx", outputPath]);

const previewFiles = [];
if (previewDir) {
  await fs.mkdir(previewDir, { recursive: true });
  const previewSpecs = [
    ["01_Все_фразы", "A1:L22"],
    ["02_Активное_ядро", "A1:L22"],
    ["03_Кластеры", "A1:Y22"],
    ["04_Страницы", "A1:P22"],
    ["05_Проверка_в_Яндексе", "A1:R20"],
    ["06_Справочник", `A1:E${Math.min(dictionaryRows.length + 1, 40)}`],
  ];
  for (const [sheetName, range] of previewSpecs) {
    const blob = await workbook.render({ sheetName, range, scale: 1, format: "png" });
    const fileName = `${sheetName}.png`;
    await fs.writeFile(path.join(previewDir, fileName), new Uint8Array(await blob.arrayBuffer()));
    previewFiles.push({ sheet: sheetName, range, file: fileName });
  }
}

const outputBytes = await fs.readFile(outputPath);
const runtimeReport = {
  status: "MATERIALIZED",
  output: outputPath,
  size_bytes: outputBytes.length,
  sha256: crypto.createHash("sha256").update(outputBytes).digest("hex"),
  source_counts: {
    all_phrases: joined.length,
    active_phrases: activeRows.length,
    assigned_phrases: assignedRows.length,
    search_required: searchRequiredRows.length,
    canonical_units: units.length,
    unique_final_urls: uniqueFinalUrls.size,
    page_summary_rows: pageRows.length,
  },
  no_page_breakdown: Object.fromEntries([...blankActionCounts.entries()].sort()),
  representative_overrides: REPRESENTATIVE_OVERRIDES,
  sheets: {
    "01_Все_фразы": sortedAll.length,
    "02_Активное_ядро": sortedActive.length,
    "03_Кластеры": clusterRows.length,
    "04_Страницы": pageRows.length,
    "05_Проверка_в_Яндексе": searchMatrix.length,
    "06_Справочник": dictionaryRows.length,
  },
  metric: { method: "getTop", region: 213, devices: "DEVICE_ALL", operators: "NONE", type: METRIC_TYPE },
  inspect: workbookInspect.ndjson,
  formula_error_scan: formulaErrors.ndjson,
  previews: previewFiles,
};
if (runtimeReportPath) {
  await fs.mkdir(path.dirname(runtimeReportPath), { recursive: true });
  await fs.writeFile(runtimeReportPath, JSON.stringify(runtimeReport, null, 2) + "\n", "utf8");
}
process.stdout.write(JSON.stringify(runtimeReport, null, 2) + "\n");
