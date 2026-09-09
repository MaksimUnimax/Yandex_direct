#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { gzipSync } from "node:zlib";

const artifactToolModule = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES
  ? pathToFileURL(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES, "@oai/artifact-tool/dist/artifact_tool.mjs")).href
  : "@oai/artifact-tool";
const { FileBlob, SpreadsheetFile, Workbook } = await import(artifactToolModule);

const REHEARSAL_DATE = "2026-09-09";
const SOURCE_ROWS = 2840;
const SOURCE_OCCURRENCES = 2965;
const METRIC = "Топы запросов Вордстата по Москве, все устройства, без операторов";
const METRIC_BOUNDARY = "Показатель помогает сравнивать формулировки внутри исследования. Это не точная частотность фразы, не число уникальных людей и не прогноз трафика.";

const GROUPS = Object.freeze({
  WINDOWS_COMMERCIAL_GENERAL: ["Окна общего назначения", "Выбрать и заказать окна без уточнения материала или отдельного вида"],
  PVC_WINDOWS_COMMERCIAL: ["Пластиковые окна", "Выбрать и заказать пластиковые окна"],
  REHAU_WINDOWS_COMMERCIAL: ["Окна REHAU", "Выбрать и заказать окна или профильные системы REHAU"],
  ALUMINIUM_WINDOWS_COMMERCIAL: ["Алюминиевые окна", "Выбрать и заказать алюминиевые окна"],
  WOOD_WINDOWS_COMMERCIAL: ["Деревянные окна", "Выбрать и заказать деревянные окна"],
  TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL: ["Дерево-алюминиевые окна", "Выбрать и заказать комбинированные дерево-алюминиевые окна"],
  SOFT_WINDOWS_COMMERCIAL: ["Мягкие окна", "Выбрать и заказать мягкие окна"],
  FRENCH_WINDOWS_COMMERCIAL: ["Французские окна", "Выбрать и заказать французские окна"],
  PANORAMIC_WINDOWS_COMMERCIAL: ["Панорамные окна", "Выбрать и заказать панорамные окна"],
  ROOF_WINDOWS_COMMERCIAL: ["Мансардные окна", "Выбрать и заказать окна для крыши или мансарды"],
  WINDOWS_DOORS_COMBINED_COMMERCIAL: ["Окна и двери вместе", "Заказать комплект окон и дверей"],
  PVC_DOORS_COMMERCIAL: ["Пластиковые двери", "Выбрать и заказать пластиковые двери"],
  GENERAL_GLAZING_SERVICE: ["Остекление общего назначения", "Заказать остекление без уточнения отдельного объекта"],
  BALCONY_GLAZING_GENERAL: ["Остекление балконов и лоджий", "Заказать остекление балкона или лоджии"],
  BALCONY_GLAZING_WARM: ["Тёплое остекление балконов", "Заказать тёплое остекление балкона или лоджии"],
  BALCONY_GLAZING_COLD: ["Холодное остекление балконов", "Заказать холодное остекление балкона или лоджии"],
  BALCONY_GLAZING_EXTENSION_SERVICE: ["Остекление балкона с выносом", "Заказать остекление балкона с выносом или расширением"],
  BALCONY_GLAZING_ROOF_SERVICE: ["Остекление балкона с крышей", "Заказать остекление балкона с устройством крыши"],
  BALCONY_RENOVATION_WITH_GLAZING: ["Ремонт балкона с остеклением", "Заказать комплексный ремонт балкона вместе с остеклением"],
  OUTDOOR_STRUCTURE_GLAZING: ["Остекление веранд, террас и беседок", "Заказать остекление веранды, террасы, беседки или крыльца"],
  OPEN_BALCONY_FINISHING: ["Отделка открытого балкона", "Заказать ремонт или отделку открытого балкона без остекления как основной задачи"],
  WINDOW_INSTALLATION_SERVICE: ["Установка окон", "Заказать профессиональную установку окон"],
  PVC_DOOR_INSTALLATION_SERVICE: ["Установка пластиковых дверей", "Заказать профессиональную установку пластиковой двери"],
  WINDOW_REPAIR_SERVICE: ["Ремонт окон", "Заказать профессиональный ремонт окон"],
  PVC_DOOR_REPAIR_SERVICE: ["Ремонт пластиковых дверей", "Заказать профессиональный ремонт пластиковой двери"],
  WINDOW_REPLACEMENT_SERVICE: ["Замена окон", "Заказать полную замену окон"],
  PVC_DOOR_REPLACEMENT_SERVICE: ["Замена пластиковых дверей", "Заказать полную замену пластиковой двери"],
  WINDOW_DEMOLITION_SERVICE: ["Демонтаж окон и рам", "Заказать демонтаж окна, рамы или балконной конструкции"],
  WINDOW_FINISHING_SERVICE: ["Отделка откосов и оконных проёмов", "Заказать профессиональную отделку откосов и зоны вокруг окна"],
  WINDOWSILL_REPAIR_SERVICE: ["Ремонт подоконников", "Заказать ремонт или восстановление подоконника"],
  MOSQUITO_NET_INSTALLATION_SERVICE: ["Установка москитных сеток", "Заказать профессиональную установку москитной сетки"],
  MOSQUITO_NET_REPAIR_SERVICE: ["Ремонт москитных сеток", "Заказать ремонт москитной сетки"],
  WINDOW_HARDWARE_SHOPPING: ["Оконная фурнитура", "Выбрать и купить оконную фурнитуру или комплектующие"],
  WINDOW_ACCESSORIES_SHOPPING: ["Аксессуары для окон", "Выбрать и купить дополнительные аксессуары для окон"],
  MOSQUITO_NET_SHOPPING: ["Москитные сетки", "Выбрать и купить москитную сетку"],
  WINDOW_SELECTION_INFO: ["Как выбрать окна", "Получить помощь в выборе окон или оконной системы"],
  WINDOW_COMPARISON_INFO: ["Сравнение окон и профильных систем", "Сравнить окна, бренды, материалы или профильные системы"],
  WINDOW_REVIEWS_INFO: ["Отзывы об окнах", "Изучить отзывы и опыт использования окон или выбора производителя"],
  WINDOW_PRODUCT_TECH_INFO: ["Устройство и свойства окон", "Разобраться в технологии, устройстве, определениях и свойствах окон"],
  WINDOW_DIMENSIONS_INFO: ["Размеры окон", "Узнать размеры и правила подбора размеров окон или дверей"],
  PRIVATE_HOUSE_WINDOW_PLANNING_INFO: ["Планирование окон для частного дома", "Спланировать характеристики и размещение окон в частном доме"],
  WINDOW_INSTALLATION_DIY_INFO: ["Самостоятельная установка окон", "Узнать, как установить окно самостоятельно"],
  WINDOW_REPAIR_DIY_INFO: ["Самостоятельный ремонт окон", "Диагностировать неисправность или отремонтировать окно самостоятельно"],
  WINDOW_FINISHING_DIY_INFO: ["Самостоятельная отделка откосов", "Узнать, как самостоятельно отделать откосы или оконный проём"],
  WINDOW_HARDWARE_INFO: ["Выбор и устройство оконной фурнитуры", "Разобраться в видах, свойствах и выборе оконной фурнитуры"],
  WINDOW_ACCESSORY_SELECTION_INFO: ["Выбор аксессуаров для окон", "Подобрать подходящие аксессуары и дополнительные элементы для окон"],
  MOSQUITO_NET_SELECTION_INFO: ["Выбор москитной сетки", "Подобрать тип и характеристики москитной сетки"],
  PVC_DOOR_INFO: ["Информация о пластиковых дверях", "Разобраться в выборе, размерах, устройстве и эксплуатации пластиковых дверей"],
  GLAZING_SELECTION_INFO: ["Как выбрать остекление", "Выбрать тип или систему остекления для объекта"],
  GLAZING_DIY_INFO: ["Самостоятельное остекление", "Узнать, как выполнить остекление самостоятельно"],
  GLAZING_PERMISSION_INFO: ["Согласование и правила остекления", "Узнать требования, разрешения и ограничения для остекления"],
  BALCONY_GLAZING_INFO: ["Как выбрать остекление балкона", "Разобраться в вариантах и характеристиках остекления балкона"],
  GLAZING_DESIGN_INSPIRATION: ["Примеры и дизайн остекления", "Посмотреть фотографии, идеи и примеры окон или остекления"],
  NAVIGATION_BRAND_SITE: ["Поиск официального сайта бренда", "Перейти на официальный сайт бренда, производителя или нужный фирменный раздел"],
  OUTSIDE_CURTAINS_BLINDS: ["Шторы и жалюзи", "Найти шторы, жалюзи, их установку или ремонт"],
  OUTSIDE_HEATING_HVAC: ["Отопление и климатическое оборудование", "Найти радиаторы, конвекторы, отопление или климатическое оборудование"],
  OUTSIDE_REAL_ESTATE_ARCHITECTURE: ["Недвижимость и архитектурные проекты", "Найти недвижимость, архитектурный проект или общую идею здания без задачи заказать окна"],
  OUTSIDE_INTERIOR_DOORS: ["Межкомнатные двери", "Выбрать межкомнатные двери вне предложения пластиковых наружных и балконных дверей"],
  OUTSIDE_OTHER: ["Другие темы вне предложения", "Решить другую подтверждённо постороннюю задачу, не относящуюся к окнам и остеклению"],
});

const INTENT_RU = Object.freeze({
  COMMERCIAL: "Коммерческий — выбор или заказ товара",
  SERVICE: "Сервисный — заказ профессиональной услуги",
  INFO: "Информационный",
  DIY_INFO: "Информационный — самостоятельное выполнение",
  NAVIGATIONAL: "Навигационный",
  OUTSIDE: "Вне целевой тематики",
});

const CONFIDENCE_RU = Object.freeze({ HIGH: "Высокая", MEDIUM: "Средняя", LOW: "Низкая", "": "Не определена" });
const FIT_RU = Object.freeze({ CORE: "Основная тема бизнеса", ADJACENT: "Смежная полезная тема", OUTSIDE: "Вне подтверждённого предложения" });
const MODIFIER_RU = Object.freeze({
  accessory_type: "вид аксессуара", accordion: "складная конструкция", action: "действие", brand: "бренд",
  building_type: "тип здания", component: "комплектующая", dimensions: "размеры", door_subtype: "вид двери",
  equipment_type: "вид оборудования", fault: "неисправность", finance: "рассрочка или кредит",
  finishing_component: "элемент отделки", finishing_material: "материал отделки", frameless: "безрамная конструкция",
  french_style: "французский формат", geo: "география", guillotine: "гильотинная система", house_series: "серия дома",
  house_style: "тип частного дома", manufacturer: "производитель", material: "материал", net_type: "вид сетки",
  object: "объект", object_type: "вид объекта", orientation: "расположение", panoramic_style: "панорамный формат",
  polycarbonate: "поликарбонат", price: "цена", price_band: "ценовой диапазон", product_type: "вид продукта",
  profile_model: "модель профиля", project_type: "тип проекта", room: "помещение", seller_source: "продавец или источник",
  soft: "мягкая конструкция", structure_type: "вид конструкции", style: "стиль", system: "система",
  system_brand: "бренд системы", tool: "инструмент", topic: "тема", warm_cold: "тёплый или холодный режим",
  window_type: "вид окна", wood_species: "порода дерева",
});

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    if (!argv[i].startsWith("--")) continue;
    out[argv[i].slice(2)] = argv[i + 1];
    i += 1;
  }
  return out;
}

function parseTsv(text) {
  const lines = text.replace(/^\uFEFF/, "").replace(/\r/g, "").trimEnd().split("\n");
  const headers = lines.shift().split("\t");
  return lines.filter(Boolean).map((line) => {
    const cells = line.split("\t");
    return Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? ""]));
  });
}

function normalize(value) {
  return String(value ?? "").normalize("NFKC").trim().replace(/\s+/g, " ").toLocaleLowerCase("ru-RU");
}

function asInt(value, label) {
  if (!/^\d+$/.test(String(value))) throw new Error(`Expected integer ${label}: ${value}`);
  return Number(value);
}

function median(values) {
  const ordered = [...values].sort((a, b) => a - b);
  const middle = Math.floor(ordered.length / 2);
  return ordered.length % 2 ? ordered[middle] : (ordered[middle - 1] + ordered[middle]) / 2;
}

function sha256(buffer) {
  return crypto.createHash("sha256").update(buffer).digest("hex");
}

function phraseId(phrase) {
  return `ФР-${crypto.createHash("sha1").update(normalize(phrase)).digest("hex").slice(0, 12).toUpperCase()}`;
}

function sourceLayer(sourceIds) {
  const first = /(^|\|)S\d+($|\|)/.test(sourceIds);
  const second = /(^|\|)P2-\d+($|\|)/.test(sourceIds);
  if (first && second) return "Первый и точечный второй проход Вордстата";
  if (second) return "Точечный второй проход Вордстата";
  if (first) return "Первый проход Вордстата";
  return "Сохранённые данные Вордстата";
}

function sourceDate(sourceIds) {
  const first = /(^|\|)S\d+($|\|)/.test(sourceIds);
  const second = /(^|\|)P2-\d+($|\|)/.test(sourceIds);
  if (first && second) return "28–29.08.2026";
  if (second) return "28.08.2026";
  if (first) return "29.08.2026";
  return "Сохранённый снимок августа 2026";
}

function tsvCell(value) {
  return String(value ?? "").replace(/[\t\r\n]+/g, " ").trim();
}

function toTsv(headers, rows) {
  return [headers, ...rows].map((row) => row.map(tsvCell).join("\t")).join("\n") + "\n";
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

function styleTitle(sheet, title, note, lastColumn) {
  sheet.showGridLines = false;
  sheet.mergeCells(`A2:${lastColumn}2`);
  sheet.getRange("A2").values = [[title]];
  sheet.getRange("A2").format = { font: { name: "Arial", size: 15, bold: true, color: "#17365D" }, verticalAlignment: "center" };
  sheet.getRange("A2").format.rowHeight = 28;
  sheet.mergeCells(`A3:${lastColumn}3`);
  sheet.getRange("A3").values = [[note]];
  sheet.getRange("A3").format = { font: { name: "Arial", size: 9, italic: true, color: "#4B5563" }, wrapText: true, verticalAlignment: "center" };
  sheet.getRange("A3").format.rowHeight = 30;
  sheet.getRange(`A4:${lastColumn}4`).format.borders = { bottom: { style: "thin", color: "#9CA3AF" } };
}

function addDataSheet(workbook, { name, title, note, headers, rows, widths, tableName, freezeColumns = 1, statusColumn = null }) {
  const sheet = workbook.worksheets.add(name);
  const lastColumn = colLetter(headers.length - 1);
  styleTitle(sheet, title, note, lastColumn);
  const matrix = [headers, ...rows];
  sheet.getRangeByIndexes(4, 0, matrix.length, headers.length).values = matrix;
  sheet.getRange(`A5:${lastColumn}5`).format = {
    fill: "#17365D",
    font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
    wrapText: true,
    horizontalAlignment: "center",
    verticalAlignment: "center",
    borders: { insideVertical: { style: "thin", color: "#FFFFFF" } },
  };
  sheet.getRange(`A5:${lastColumn}5`).format.rowHeight = 42;
  if (rows.length) {
    const body = sheet.getRangeByIndexes(5, 0, rows.length, headers.length);
    body.format = { font: { name: "Arial", size: 9, color: "#1F2937" }, verticalAlignment: "top", wrapText: true };
    body.format.borders = { insideHorizontal: { style: "thin", color: "#E5E7EB" } };
    body.format.rowHeight = 30;
  }
  widths.forEach((width, index) => sheet.getRangeByIndexes(0, index, rows.length + 5, 1).format.columnWidth = width);
  const table = sheet.tables.add(`A5:${lastColumn}${rows.length + 5}`, true, tableName);
  table.style = "TableStyleMedium2";
  table.showFilterButton = true;
  table.showBandedRows = true;
  sheet.freezePanes.freezeRows(5);
  if (freezeColumns) sheet.freezePanes.freezeColumns(freezeColumns);
  if (statusColumn && rows.length) {
    const range = sheet.getRange(`${statusColumn}6:${statusColumn}${rows.length + 5}`);
    range.conditionalFormats.add("containsText", { text: "Нужна проверка", format: { fill: "#FEF3C7", font: { color: "#92400E", bold: true } } });
    range.conditionalFormats.add("containsText", { text: "Исключено", format: { fill: "#FEE2E2", font: { color: "#991B1B" } } });
    range.conditionalFormats.add("containsText", { text: "В рабочем ядре", format: { fill: "#DCFCE7", font: { color: "#166534", bold: true } } });
  }
  return sheet;
}

const args = parseArgs(process.argv.slice(2));
if (!args["repo-root"] || !args["output-dir"]) {
  throw new Error("Usage: build_mk01_rehearsal.mjs --repo-root <repo> --output-dir <dir> [--preview-dir <dir>]");
}

const repoRoot = path.resolve(args["repo-root"]);
const outputDir = path.resolve(args["output-dir"]);
const previewDir = args["preview-dir"] ? path.resolve(args["preview-dir"]) : null;
const sourceRoot = path.join(repoRoot, "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK");

const sourcePaths = {
  semantic: path.join(sourceRoot, "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv"),
  assignments: path.join(sourceRoot, "STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv"),
  taxonomy: path.join(sourceRoot, "STEP_10_FRESH_R1_TAXONOMY_FINAL.tsv"),
  searchDecisions: path.join(sourceRoot, "STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv"),
  occurrences: path.join(sourceRoot, "STEP_07C_SEMANTIC_CORRECTION_OCCURRENCES.tsv"),
  stage5: path.join(sourceRoot, "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"),
  step5aDelta: path.join(sourceRoot, "STEP_05A_FIRST_EXECUTION_2026-09-08/STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv"),
  integrated: path.join(sourceRoot, "STEP_05A_INTEGRATED_SEMANTIC_CORE_2026-09-09/FINAL_SEMANTIC_MASTER_STEP05A_INTEGRATED_2026-09-09.tsv"),
};

const entries = await Promise.all(Object.entries(sourcePaths).map(async ([key, file]) => [key, await fs.readFile(file)]));
const sourceBuffers = Object.fromEntries(entries);
const semantic = parseTsv(sourceBuffers.semantic.toString("utf8"));
const assignments = parseTsv(sourceBuffers.assignments.toString("utf8"));
const taxonomy = parseTsv(sourceBuffers.taxonomy.toString("utf8"));
const searchDecisions = parseTsv(sourceBuffers.searchDecisions.toString("utf8"));
const occurrences = parseTsv(sourceBuffers.occurrences.toString("utf8"));
const stage5 = parseTsv(sourceBuffers.stage5.toString("utf8"));
const step5aDelta = parseTsv(sourceBuffers.step5aDelta.toString("utf8"));
const integrated = parseTsv(sourceBuffers.integrated.toString("utf8"));

const uniqueMap = (rows, field, label) => {
  const map = new Map();
  for (const row of rows) {
    const key = normalize(row[field]);
    if (map.has(key)) throw new Error(`Duplicate ${label}: ${row[field]}`);
    map.set(key, row);
  }
  return map;
};

const semanticByPhrase = uniqueMap(semantic, "phrase", "semantic phrase");
const assignmentByPhrase = uniqueMap(assignments, "phrase", "assignment phrase");
const stage5ByPhrase = uniqueMap(stage5, "phrase", "stage5 phrase");
const integratedByPhrase = uniqueMap(integrated, "phrase", "integrated phrase");
const taxonomyById = new Map(taxonomy.map((row) => [row.cluster_id, row]));
const searchByPhrase = new Map(searchDecisions.map((row) => [normalize(row.query), row]));

if (semantic.length !== SOURCE_ROWS || semanticByPhrase.size !== SOURCE_ROWS) throw new Error("Step08 2840-row invariant failed");
if (assignments.length !== SOURCE_ROWS || assignmentByPhrase.size !== SOURCE_ROWS) throw new Error("Step10 2840-row invariant failed");
if (stage5.length !== SOURCE_ROWS || stage5ByPhrase.size !== SOURCE_ROWS) throw new Error("Stage5 2840-row cross-check failed");
if (occurrences.length !== SOURCE_OCCURRENCES) throw new Error("2965 occurrence invariant failed");
if (taxonomy.length !== 59 || taxonomyById.size !== 59) throw new Error("59-cluster taxonomy invariant failed");
if (searchDecisions.length !== 75 || searchByPhrase.size !== 75) throw new Error("75 exact Search decision invariant failed");
if (step5aDelta.length !== 16 || integrated.length !== 2856) throw new Error("Step5A contamination control source invariant failed");
if (Object.keys(GROUPS).length !== 59 || [...taxonomyById.keys()].some((id) => !GROUPS[id])) throw new Error("Russian group dictionary does not cover all 59 clusters");

for (const key of semanticByPhrase.keys()) {
  if (!assignmentByPhrase.has(key) || !stage5ByPhrase.has(key)) throw new Error(`Pre-Step5A phrase-set mismatch: ${key}`);
}
const step5aKeys = new Set(step5aDelta.map((row) => normalize(row.phrase)));
const searchDecisionsInUniverse = searchDecisions.filter((row) => semanticByPhrase.has(normalize(row.query)));
const searchControlDecisionsOutsideUniverse = searchDecisions.filter((row) => !semanticByPhrase.has(normalize(row.query)));
if (searchDecisionsInUniverse.length !== 66 || searchControlDecisionsOutsideUniverse.length !== 9) {
  throw new Error("Search decision projection must reconcile as 66 universe phrases + 9 external control anchors");
}
const integratedAdditions = [...integratedByPhrase.keys()].filter((key) => !semanticByPhrase.has(key));
if (integratedAdditions.length !== 16 || integratedAdditions.some((key) => !step5aKeys.has(key))) throw new Error("Integrated core difference is not exactly the 16-row Step5A delta");

const joined = semantic.map((demand) => {
  const assignment = assignmentByPhrase.get(normalize(demand.phrase));
  const taxonomyRow = assignment.cluster_id ? taxonomyById.get(assignment.cluster_id) : null;
  if (assignment.cluster_id && !taxonomyRow) throw new Error(`Unknown cluster ${assignment.cluster_id}`);
  const search = searchByPhrase.get(normalize(demand.phrase));
  const popular = asInt(demand.max_result_count, "max_result_count");
  const similar = asInt(demand.max_association_count, "max_association_count");
  const sourceOccurrences = asInt(demand.source_occurrences, "source_occurrences");
  let category;
  let status;
  if (assignment.assignment_status === "PRESERVED_EXCLUDED") {
    category = "excluded";
    status = "Исключено после построчной очистки";
  } else if (assignment.assignment_status === "PRESERVED_DEFERRED") {
    category = "review";
    status = "Проверка отложена";
  } else if (assignment.assignment_status === "SEARCH_REQUIRED") {
    category = "review";
    status = "Нужна проверка в обычной выдаче Яндекса";
  } else if (assignment.assignment_status === "ASSIGNED" && taxonomyRow?.business_fit === "OUTSIDE") {
    category = "excluded";
    status = "Исключено после смысловой группировки";
  } else if (assignment.assignment_status === "ASSIGNED" && ["CORE", "ADJACENT"].includes(taxonomyRow?.business_fit)) {
    category = "working";
    status = "В рабочем ядре";
  } else {
    throw new Error(`Unsupported final category for ${demand.phrase}`);
  }
  const group = taxonomyRow ? GROUPS[assignment.cluster_id] : null;
  const groupName = group?.[0] ?? "Не назначена до дополнительной проверки";
  const userTask = group?.[1] ?? "Задача пользователя не определена окончательно";
  const intent = taxonomyRow ? INTENT_RU[taxonomyRow.intent_type] : "Не определён окончательно";
  const businessFit = taxonomyRow ? FIT_RU[taxonomyRow.business_fit] : "Не определена окончательно";
  if (!intent || !businessFit) throw new Error(`Missing Russian display mapping for ${demand.phrase}`);

  let reason;
  if (category === "working") {
    reason = `Фраза соответствует задаче группы «${groupName}» и ${taxonomyRow.business_fit === "CORE" ? "основному" : "смежному полезному"} смыслу предложения сайта.`;
  } else if (assignment.assignment_status === "SEARCH_REQUIRED") {
    reason = "По сохранённым данным смысл фразы нельзя определить достаточно надёжно. Нужна точечная проверка обычной выдачи Яндекса.";
  } else if (assignment.assignment_status === "PRESERVED_DEFERRED") {
    reason = "Фраза пришла как похожий запрос. Данных недостаточно для включения, а немедленная проверка не была обоснована.";
  } else if (taxonomyRow?.business_fit === "OUTSIDE") {
    reason = `Смысл относится к группе «${groupName}», которая не входит в подтверждённое предложение этого заказа.`;
  } else if (demand.corrected_status === "EXCLUDE_MECHANICAL") {
    reason = "Формулировка неполная, искажённая или не имеет устойчивого пользовательского смысла.";
  } else if (demand.corrected_status === "EXCLUDE_SCOPE" && demand.corrected_reason.includes("OUTSIDE_REGION")) {
    reason = "Запрос относится к другому региону и не входит в московский срез этого заказа.";
  } else if (demand.corrected_status === "EXCLUDE_SCOPE") {
    reason = "Запрос выходит за зафиксированные направления, сегмент или регион заказа.";
  } else {
    reason = "По смыслу запрос не относится к товарам и услугам, включённым в этот заказ.";
  }

  let nextStep;
  if (category === "working") nextStep = "Использовать при дальнейшей работе с семантикой и содержанием по смысловой группе. Не назначать URL автоматически.";
  else if (assignment.assignment_status === "SEARCH_REQUIRED") nextStep = "Проверить точную фразу в обычной выдаче Яндекса и заново подтвердить её смысл.";
  else if (assignment.assignment_status === "PRESERVED_DEFERRED") nextStep = "Вернуться при появлении нового источника или уточнении предложения клиента.";
  else nextStep = "Не использовать в рабочем ядре. Пересматривать только при изменении заказа или появлении нового доказательства релевантности.";

  const searchState = search
    ? (assignment.assignment_status === "SEARCH_REQUIRED" ? "Сохранённое наблюдение не сняло неопределённость" : "Есть сохранённая проверка этой точной фразы")
    : "Отдельная проверка этой фразы не проводилась";

  return {
    id: phraseId(demand.phrase),
    phrase: demand.phrase,
    category,
    status,
    groupId: assignment.cluster_id,
    groupName,
    userTask,
    intent,
    businessFit,
    reason,
    confidence: CONFIDENCE_RU[assignment.assignment_confidence || assignment.source_semantic_confidence || demand.semantic_confidence],
    popular,
    similar,
    sourceIds: demand.source_ids,
    sourceOccurrences,
    sourceLayer: sourceLayer(demand.source_ids),
    sourceDate: sourceDate(demand.source_ids),
    provenance: demand.provenance,
    searchState,
    search,
    nextStep,
    taxonomyRow,
  };
});

const workingRows = joined.filter((row) => row.category === "working");
const reviewRows = joined.filter((row) => row.category === "review");
const excludedRows = joined.filter((row) => row.category === "excluded");
const outsideRows = joined.filter((row) => row.taxonomyRow?.business_fit === "OUTSIDE");
const workingGroupIds = new Set(workingRows.map((row) => row.groupId));
const allGroupIds = new Set(joined.filter((row) => row.groupId).map((row) => row.groupId));
const contamination = joined.filter((row) => step5aKeys.has(normalize(row.phrase)));

const expected = { working: 2185, review: 187, excluded: 468, outside: 134, groups: 59, workingGroups: 54 };
if (workingRows.length !== expected.working || reviewRows.length !== expected.review || excludedRows.length !== expected.excluded) throw new Error("Final client-state reconciliation failed");
if (outsideRows.length !== expected.outside || allGroupIds.size !== expected.groups || workingGroupIds.size !== expected.workingGroups) throw new Error("Cluster/business-fit reconciliation failed");
if (workingRows.length + reviewRows.length + excludedRows.length !== SOURCE_ROWS) throw new Error("Silent row loss detected");
if (contamination.length !== 0) throw new Error(`Step5A contamination detected: ${contamination.length}`);

const membersByGroup = new Map();
for (const row of joined.filter((item) => item.groupId)) {
  if (!membersByGroup.has(row.groupId)) membersByGroup.set(row.groupId, []);
  membersByGroup.get(row.groupId).push(row);
}

const representativeScore = (row, members) => {
  const words = normalize(row.phrase).split(" ").filter(Boolean);
  const natural = words.length >= 2 && words.length <= 6 ? 20 : words.length === 1 ? 5 : 0;
  const noDigits = /\d/.test(row.phrase) ? 0 : 8;
  const noGeo = /москв|район|город|телефон|адрес/i.test(row.phrase) ? 0 : 6;
  const noPrice = /цена|стоимост|недорог|дешев/i.test(row.phrase) ? 0 : 4;
  const centralTokens = new Set(words.filter((word) => word.length >= 4).map((word) => word.slice(0, 6)));
  const shared = members.filter((member) => normalize(member.phrase).split(" ").some((word) => centralTokens.has(word.slice(0, 6)))).length;
  return natural + noDigits + noGeo + noPrice + Math.log10(row.popular + 1) * 8 + (shared / members.length) * 20;
};

const groupRows = [...taxonomy].map((tax) => {
  const members = membersByGroup.get(tax.cluster_id) ?? [];
  if (!members.length) throw new Error(`Cluster without member: ${tax.cluster_id}`);
  const representative = [...members].sort((a, b) => representativeScore(b, members) - representativeScore(a, members) || b.popular - a.popular || a.phrase.localeCompare(b.phrase, "ru"))[0];
  if (!members.some((row) => row.id === representative.id)) throw new Error(`Representative is not a member: ${tax.cluster_id}`);
  const values = members.map((row) => row.popular);
  const modifiers = tax.absorbed_modifiers.split(";").filter(Boolean).map((item) => MODIFIER_RU[item]);
  if (modifiers.some((item) => !item)) throw new Error(`Untranslated modifier in ${tax.cluster_id}`);
  return {
    groupId: tax.cluster_id,
    groupName: GROUPS[tax.cluster_id][0],
    userTask: GROUPS[tax.cluster_id][1],
    intent: INTENT_RU[tax.intent_type],
    businessFit: FIT_RU[tax.business_fit],
    role: tax.business_fit === "OUTSIDE" ? "Исключённая смысловая группа" : "Рабочая смысловая группа",
    members: members.length,
    workingMembers: members.filter((row) => row.category === "working").length,
    representative: representative.phrase,
    representativeCount: representative.popular,
    max: Math.max(...values),
    median: median(values),
    sum: values.reduce((total, value) => total + value, 0),
    examples: [...members].sort((a, b) => b.popular - a.popular || a.phrase.localeCompare(b.phrase, "ru")).slice(0, 5).map((row) => `${row.phrase} [${row.popular}]`).join("; "),
    boundary: `Объединены запросы с задачей «${GROUPS[tax.cluster_id][1].toLocaleLowerCase("ru-RU")}». Варианты «${modifiers.join(", ")}» сами по себе не создают новую группу.`,
  };
}).sort((a, b) => {
  const roleOrder = { "Рабочая смысловая группа": 0, "Исключённая смысловая группа": 1 };
  return roleOrder[a.role] - roleOrder[b.role] || a.groupName.localeCompare(b.groupName, "ru");
});

const universeHeaders = [
  "Поисковая фраза", "Итоговый статус", "В рабочем ядре", "Группа запросов", "Задача пользователя", "Интент",
  "Роль темы", "Основание решения", "Уверенность", "Число запросов — популярные", "Число запросов — похожие",
  "Тип данных Вордстата", "Проверка в Яндексе", "Следующий шаг", "Регион", "Происхождение данных",
  "Коды источников", "Исходных наблюдений", "Код группы (для аудита)", "ID фразы (для аудита)",
];
const sortedUniverse = [...joined].sort((a, b) => a.phrase.localeCompare(b.phrase, "ru"));
const universeMatrix = sortedUniverse.map((row) => [
  row.phrase, row.status, row.category === "working" ? "Да" : "Нет", row.groupName, row.userTask, row.intent,
  row.businessFit, row.reason, row.confidence, row.popular, row.similar, METRIC, row.searchState, row.nextStep, "Москва",
  `${row.sourceLayer}; снимок ${row.sourceDate}`, row.sourceIds, row.sourceOccurrences, row.groupId || "Не назначен", row.id,
]);

const workingHeaders = [
  "Группа запросов", "Поисковая фраза", "Задача пользователя", "Интент", "Роль темы", "Число запросов — популярные",
  "Число запросов — похожие", "Место внутри группы", "Уверенность", "Проверка в Яндексе", "Основание включения",
  "Регион", "Коды источников", "Код группы (для аудита)", "ID фразы (для аудита)",
];
const rankById = new Map();
for (const groupId of workingGroupIds) {
  const members = workingRows.filter((row) => row.groupId === groupId).sort((a, b) => b.popular - a.popular || a.phrase.localeCompare(b.phrase, "ru"));
  members.forEach((row, index) => rankById.set(row.id, index + 1));
}
const workingMatrix = [...workingRows].sort((a, b) => a.groupName.localeCompare(b.groupName, "ru") || rankById.get(a.id) - rankById.get(b.id)).map((row) => [
  row.groupName, row.phrase, row.userTask, row.intent, row.businessFit, row.popular, row.similar, rankById.get(row.id), row.confidence,
  row.searchState, row.reason, "Москва", row.sourceIds, row.groupId, row.id,
]);

const groupHeaders = [
  "Группа запросов", "Роль в результате", "Задача пользователя", "Интент", "Роль темы", "Всего фраз", "Фраз в рабочем ядре",
  "Основная формулировка", "Число запросов у основной формулировки", "Максимальное число запросов", "Медианное число запросов",
  "Сумма числа запросов (не объём рынка)", "Примеры фраз", "Граница группы", "Код группы (для аудита)",
];
const groupMatrix = groupRows.map((row) => [
  row.groupName, row.role, row.userTask, row.intent, row.businessFit, row.members, row.workingMembers, row.representative,
  row.representativeCount, row.max, row.median, row.sum, row.examples, row.boundary, row.groupId,
]);

const reviewHeaders = [
  "Поисковая фраза", "Состояние", "Почему не включена сейчас", "Что сделать дальше", "Число запросов — популярные",
  "Число запросов — похожие", "Проверка в Яндексе", "Уверенность", "Происхождение данных", "Коды источников",
  "Исходных наблюдений", "ID фразы (для аудита)",
];
const reviewMatrix = [...reviewRows].sort((a, b) => a.status.localeCompare(b.status, "ru") || b.popular - a.popular || a.phrase.localeCompare(b.phrase, "ru")).map((row) => [
  row.phrase, row.status, row.reason, row.nextStep, row.popular, row.similar, row.searchState, row.confidence,
  `${row.sourceLayer}; снимок ${row.sourceDate}`, row.sourceIds, row.sourceOccurrences, row.id,
]);

const excludedHeaders = [
  "Поисковая фраза", "Причина исключения", "Этап исключения", "Смысловая группа", "Число запросов — популярные",
  "Число запросов — похожие", "Происхождение данных", "Когда пересматривать", "ID фразы (для аудита)",
];
const excludedMatrix = [...excludedRows].sort((a, b) => a.status.localeCompare(b.status, "ru") || a.reason.localeCompare(b.reason, "ru") || b.popular - a.popular).map((row) => [
  row.phrase, row.reason, row.status, row.groupId ? row.groupName : "Не применимо", row.popular, row.similar,
  `${row.sourceLayer}; ${row.sourceIds}`, row.nextStep, row.id,
]);

const semanticTsvHeaders = [...universeHeaders, "Полная техническая provenance"];
const semanticTsvRows = universeMatrix.map((row, index) => [...row, sortedUniverse[index].provenance]);
const groupTsvRows = groupMatrix;

await fs.mkdir(outputDir, { recursive: true });
const semanticTsvPath = path.join(outputDir, `MK01_SEMANTIC_UNIVERSE_${REHEARSAL_DATE}.tsv`);
const semanticTsvGzipPath = `${semanticTsvPath}.gz`;
const groupTsvPath = path.join(outputDir, `MK01_CLUSTER_SUMMARY_${REHEARSAL_DATE}.tsv`);
const xlsxPath = path.join(outputDir, `MK01_OKNO_MSK_SEMANTIC_CORE_${REHEARSAL_DATE}.xlsx`);
const buildReportPath = path.join(outputDir, `MK01_WORKBOOK_BUILD_REPORT_${REHEARSAL_DATE}.json`);
const manifestPath = path.join(outputDir, `MK01_MATERIALIZATION_MANIFEST_${REHEARSAL_DATE}.json`);
await fs.writeFile(semanticTsvPath, toTsv(semanticTsvHeaders, semanticTsvRows), "utf8");
await fs.writeFile(semanticTsvGzipPath, gzipSync(await fs.readFile(semanticTsvPath), { level: 9 }));
await fs.rm(semanticTsvPath, { force: true });
await fs.writeFile(groupTsvPath, toTsv(groupHeaders, groupTsvRows), "utf8");

const workbook = Workbook.create();
const guide = workbook.worksheets.add("Как пользоваться");
styleTitle(guide, "Семантическое ядро сайта okno-msk.ru", "Москва · Яндекс Вордстат · отдельный результат сбора, чистки и смысловой группировки", "H");
guide.getRange("A6:H15").values = [
  ["Что открыть первым", "", "Лист «Рабочее ядро» — это готовый набор подтверждённых фраз для дальнейшей работы.", "", "", "", "", ""],
  ["Сайт", "", "https://okno-msk.ru/", "", "", "", "", ""],
  ["Регион", "", "Москва", "", "", "", "", ""],
  ["Всего сохранено фраз", "", SOURCE_ROWS, "", "", "", "", ""],
  ["В рабочем ядре", "", workingRows.length, "", "", "", "", ""],
  ["На проверку", "", reviewRows.length, "", "", "", "", ""],
  ["Исключено", "", excludedRows.length, "", "", "", "", ""],
  ["Смысловых групп всего", "", allGroupIds.size, "", "", "", "", ""],
  ["Рабочих смысловых групп", "", workingGroupIds.size, "", "", "", "", ""],
  ["Добавлено из анализа конкурентов", "", 0, "", "", "", "", ""],
];
for (let row = 6; row <= 15; row += 1) {
  guide.getRange(`A${row}:B${row}`).merge();
  guide.getRange(`C${row}:H${row}`).merge();
}
guide.getRange("A6:H6").format = { fill: "#17365D", font: { name: "Arial", bold: true, color: "#FFFFFF" } };
guide.getRange("A7:H15").format = { font: { name: "Arial", size: 10 }, verticalAlignment: "center", wrapText: true };
guide.getRange("A6:H15").format.borders = { insideHorizontal: { style: "thin", color: "#D1D5DB" } };
guide.getRange("A17:H17").merge();
guide.getRange("A17").values = [["Как работать с файлом"]];
guide.getRange("A17").format = { fill: "#0F6B78", font: { name: "Arial", bold: true, color: "#FFFFFF" } };
guide.getRange("A19:H25").values = [
  ["1", "Рабочее ядро", "Фильтруйте по группе, задаче, интенту и относительному спросу.", "", "", "", "", ""],
  ["2", "Группы запросов", "Используйте как карту смыслов. Группа не является готовым URL и не требует отдельной страницы автоматически.", "", "", "", "", ""],
  ["3", "На проверку", "Не смешивайте эти фразы с рабочим ядром, пока не выполнен указанный следующий шаг.", "", "", "", "", ""],
  ["4", "Исключено", "Смотрите причину исключения. Фразы сохранены и не исчезли из исследования.", "", "", "", "", ""],
  ["5", "Все запросы", "Используйте для полного аудита 2840 строк и проверки происхождения данных.", "", "", "", "", ""],
  ["6", "Показатели", "Число запросов Вордстата собрано без операторов. Не трактуйте его как точную частотность или прогноз трафика.", "", "", "", "", ""],
  ["7", "Граница результата", "В файле нет назначения URL, архитектуры сайта, конкурентных добавлений, ИИ-анализа и технических заданий.", "", "", "", "", ""],
];
for (let row = 19; row <= 25; row += 1) guide.getRange(`C${row}:H${row}`).merge();
guide.getRange("A19:H25").format = { font: { name: "Arial", size: 10 }, verticalAlignment: "top", wrapText: true };
guide.getRange("A19:A25").format = { font: { name: "Arial", size: 11, bold: true, color: "#17365D" }, horizontalAlignment: "center" };
guide.getRange("A1:A25").format.columnWidth = 8;
guide.getRange("B1:B25").format.columnWidth = 28;
guide.getRange("C1:H25").format.columnWidth = 15;
guide.getRange("A6:H15").format.rowHeight = 24;
guide.getRange("A6:H6").format.rowHeight = 34;
guide.getRange("A19:H25").format.rowHeight = 38;
guide.showGridLines = false;

const allSheet = addDataSheet(workbook, {
  name: "Все запросы", title: "Все сохранённые запросы", note: "Полный набор из 2840 уникальных фраз. Здесь видны рабочие, спорные и исключённые строки; ни одна фраза не удалена молча.",
  headers: universeHeaders, rows: universeMatrix, widths: [40, 30, 15, 30, 45, 30, 26, 55, 16, 18, 18, 38, 35, 52, 14, 35, 24, 16, 35, 22], tableName: "AllQueries", freezeColumns: 2, statusColumn: "B",
});
const workSheet = addDataSheet(workbook, {
  name: "Рабочее ядро", title: "Рабочее семантическое ядро", note: "2185 подтверждённых фраз из основных и смежных полезных тем. Откройте этот лист первым для практической работы.",
  headers: workingHeaders, rows: workingMatrix, widths: [30, 42, 48, 30, 26, 18, 18, 16, 16, 34, 52, 14, 24, 35, 22], tableName: "WorkingCore", freezeColumns: 2,
});
const groupsSheet = addDataSheet(workbook, {
  name: "Группы запросов", title: "Смысловые группы запросов", note: "59 подтверждённых задач: 54 рабочие группы и 5 групп вне предложения. Суммы показателей не являются объёмом рынка.",
  headers: groupHeaders, rows: groupMatrix, widths: [34, 26, 48, 30, 27, 14, 18, 34, 22, 19, 19, 24, 70, 70, 36], tableName: "QueryGroups", freezeColumns: 1, statusColumn: "B",
});
const reviewSheet = addDataSheet(workbook, {
  name: "На проверку", title: "Запросы, по которым решение не завершено", note: "187 фраз: 13 требуют проверки обычной выдачи Яндекса, 174 сохранены до появления достаточного основания для новой проверки.",
  headers: reviewHeaders, rows: reviewMatrix, widths: [44, 32, 62, 58, 18, 18, 38, 16, 35, 24, 16, 22], tableName: "ReviewQueue", freezeColumns: 1, statusColumn: "B",
});
const excludedSheet = addDataSheet(workbook, {
  name: "Исключено", title: "Исключённые запросы", note: "468 фраз сохранены вместе с причиной: 334 исключены при очистке, ещё 134 признаны отдельными задачами вне предложения после смысловой группировки.",
  headers: excludedHeaders, rows: excludedMatrix, widths: [44, 62, 32, 34, 18, 18, 42, 62, 22], tableName: "ExcludedQueries", freezeColumns: 1, statusColumn: "C",
});

const methodRows = [
  ["Объём", "Полный набор", "2840 уникальных фраз из 2965 сохранённых наблюдений.", "Повторные наблюдения сохранены в истории происхождения данных."],
  ["Объём", "Рабочее ядро", "2185 фраз: 1151 основных и 1034 смежных полезных.", "134 фразы из подтверждённо посторонних смысловых групп не включены."],
  ["Статус", "В рабочем ядре", "Смысл фразы соответствует подтверждённой основной или смежной задаче сайта.", "Это не назначение конкретной странице."],
  ["Статус", "Нужна проверка", "13 фраз требуют дополнительной точечной проверки обычной выдачи Яндекса.", "До проверки не включать в рабочее ядро."],
  ["Статус", "Проверка отложена", "174 похожих запроса сохранены без достаточного основания для немедленной проверки.", "Возобновить при появлении нового источника или уточнении предложения."],
  ["Статус", "Исключено", "468 фраз признаны нерелевантными, регионально неподходящими, искажёнными или относящимися к другому пользовательскому результату.", "Фразы не удалены и доступны для аудита."],
  ["Вордстат", "Число запросов — популярные", "Максимальное сохранённое значение для точного текста строки в разделе популярных запросов.", METRIC_BOUNDARY],
  ["Вордстат", "Число запросов — похожие", "Максимальное сохранённое значение для точного текста строки в разделе похожих запросов.", "Вспомогательный показатель происхождения, а не автоматическое основание для включения."],
  ["Вордстат", "Повторные наблюдения", "Максимальные значения популярных и похожих запросов сохраняются отдельно; наблюдения не складываются.", "Это предотвращает двойной счёт одной фразы из нескольких исходных запросов."],
  ["Вордстат", "Регион и режим", "Москва, код региона 213, все устройства, без операторов.", "Google и данные частных кабинетов не смешиваются с показателями."],
  ["Группировка", "Принцип", "Фразы объединены по ожидаемому результату и задаче пользователя, а не только по совпадающим словам.", "Цена, география, бренд и другие модификаторы не создают новую группу автоматически."],
  ["Группировка", "Количество групп", "59 смысловых групп возникли из данных: 54 рабочие и 5 подтверждённо посторонних.", "Количество не задавалось заранее ради красивого отчёта."],
  ["Группировка", "Основная формулировка", "Реальная фраза из группы, выбранная по смысловой типичности, читаемости и показателю Вордстата.", "Это пример смысла группы, а не обязательный заголовок страницы."],
  ["Обычный поиск", "Точечная проверка", "Сохранены 75 проверок: 66 относятся к точным фразам полного набора, ещё 9 — к контрольным формулировкам вне него.", "Наблюдение относится только к проверенной фразе и не доказывает свойства всего семейства."],
  ["Ограничение", "Не входит в результат", "Назначение URL, новая архитектура, создание или объединение страниц, перелинковка, контентные задания, анализ конкурентов и ИИ-ответов.", "Эти работы требуют отдельного продукта и отдельных доказательств."],
  ["Ограничение", "Коммерческий приоритет", "В данных нет маржинальности, загрузки производства, конверсий и выручки.", "Порядок строк по спросу не является коммерческим приоритетом."],
  ["Происхождение", "Коды источников", "Технические коды показывают, в каких запросах Вордстата встретилась фраза.", "Нужны только для аудита; основная клиентская трактовка дана русским текстом."],
];
const methodSheet = addDataSheet(workbook, {
  name: "Методика", title: "Методика и значения показателей", note: "Короткий словарь, необходимый для правильного использования результата без чтения внутренних файлов проекта.",
  headers: ["Раздел", "Понятие", "Что означает", "Как использовать и чего не утверждать"], rows: methodRows,
  widths: [22, 34, 78, 78], tableName: "MethodDictionary", freezeColumns: 0,
});

allSheet.getRange(`J6:K${universeMatrix.length + 5}`).format.numberFormat = "#,##0";
allSheet.getRange(`R6:R${universeMatrix.length + 5}`).format.numberFormat = "#,##0";
workSheet.getRange(`F6:H${workingMatrix.length + 5}`).format.numberFormat = "#,##0";
groupsSheet.getRange(`F6:L${groupMatrix.length + 5}`).format.numberFormat = "#,##0";
reviewSheet.getRange(`E6:F${reviewMatrix.length + 5}`).format.numberFormat = "#,##0";
reviewSheet.getRange(`K6:K${reviewMatrix.length + 5}`).format.numberFormat = "#,##0";
excludedSheet.getRange(`E6:F${excludedMatrix.length + 5}`).format.numberFormat = "#,##0";

workbook.recalculate();
const inspections = {};
for (const [sheet, range] of [
  ["Как пользоваться", "A1:H27"], ["Все запросы", "A1:T15"], ["Рабочее ядро", "A1:O15"],
  ["Группы запросов", "A1:O20"], ["На проверку", "A1:L15"], ["Исключено", "A1:I15"], ["Методика", "A1:D22"],
]) {
  const inspected = await workbook.inspect({ kind: "table", range: `${sheet}!${range}`, include: "values,formulas", tableMaxRows: 22, tableMaxCols: 20, maxChars: 12000 });
  inspections[sheet] = inspected.ndjson;
}
const formulaErrors = await workbook.inspect({
  kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 }, summary: "MK01 final formula error scan",
});

const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(xlsxPath);

if (previewDir) {
  await fs.mkdir(previewDir, { recursive: true });
  const renderRanges = {
    "Как пользоваться": "A1:H27", "Все запросы": "A1:L24", "Рабочее ядро": "A1:L24",
    "Группы запросов": "A1:L25", "На проверку": "A1:L24", "Исключено": "A1:I24", "Методика": "A1:D22",
  };
  for (const [sheetName, range] of Object.entries(renderRanges)) {
    const image = await workbook.render({ sheetName, range, scale: 1, format: "png" });
    const fileName = sheetName.replace(/\s+/g, "_") + ".png";
    await fs.writeFile(path.join(previewDir, fileName), new Uint8Array(await image.arrayBuffer()));
  }
}

const imported = await SpreadsheetFile.importXlsx(await FileBlob.load(xlsxPath));
const importedSheets = await imported.inspect({ kind: "sheet", include: "id,name", maxChars: 8000 });
const importedErrors = await imported.inspect({
  kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 }, summary: "MK01 saved-file formula error scan",
});

const buildReport = {
  schema: "MK01_OKNO_MSK_WORKBOOK_BUILD_REPORT_V1",
  date: REHEARSAL_DATE,
  status: "PASS",
  artifact_tool_used: true,
  workbook_recalculated: true,
  workbook_sheet_order: ["Как пользоваться", "Все запросы", "Рабочее ядро", "Группы запросов", "На проверку", "Исключено", "Методика"],
  rendered_sheet_count: previewDir ? 7 : 0,
  formula_error_scan_before_export: formulaErrors.ndjson,
  formula_error_scan_after_import: importedErrors.ndjson,
  imported_sheet_inspection: importedSheets.ndjson,
  bounded_range_inspections: inspections,
};
await fs.writeFile(buildReportPath, JSON.stringify(buildReport, null, 2) + "\n", "utf8");

const artifactBuffers = {
  semantic_tsv_gzip: await fs.readFile(semanticTsvGzipPath), cluster_tsv: await fs.readFile(groupTsvPath),
  xlsx: await fs.readFile(xlsxPath), build_report: await fs.readFile(buildReportPath),
};
const manifest = {
  schema: "MK01_OKNO_MSK_REHEARSAL_MATERIALIZATION_V1",
  date: REHEARSAL_DATE,
  status: "PASS",
  source_authority: path.relative(repoRoot, sourcePaths.semantic),
  clustering_authority: [path.relative(repoRoot, sourcePaths.assignments), path.relative(repoRoot, sourcePaths.taxonomy)],
  source_counts: { raw_occurrences: SOURCE_OCCURRENCES, unique_phrases: SOURCE_ROWS },
  final_counts: {
    universe: joined.length,
    working_core: workingRows.length,
    review_or_uncertain: reviewRows.length,
    excluded_total: excludedRows.length,
    excluded_during_cleanup: excludedRows.filter((row) => !row.groupId).length,
    excluded_after_task_clustering: outsideRows.length,
    semantic_groups_total: allGroupIds.size,
    working_groups: workingGroupIds.size,
    outside_groups: allGroupIds.size - workingGroupIds.size,
    exact_search_decisions_available: searchDecisions.length,
    exact_search_decisions_joined_to_universe: searchDecisionsInUniverse.length,
    search_control_anchors_outside_universe: searchControlDecisionsOutsideUniverse.length,
    step5a_contamination: contamination.length,
  },
  provider_calls_during_rehearsal: 0,
  source_sha256: Object.fromEntries(Object.entries(sourceBuffers).map(([key, buffer]) => [key, sha256(buffer)])),
  artifacts: {
    semantic_universe_tsv_gzip: { file: path.basename(semanticTsvGzipPath), compression: "gzip", uncompressed_format: "UTF-8 TSV", rows: joined.length, bytes: artifactBuffers.semantic_tsv_gzip.length, sha256: sha256(artifactBuffers.semantic_tsv_gzip) },
    cluster_summary_tsv: { file: path.basename(groupTsvPath), rows: groupRows.length, bytes: artifactBuffers.cluster_tsv.length, sha256: sha256(artifactBuffers.cluster_tsv) },
    client_xlsx: { file: path.basename(xlsxPath), sheets: 7, bytes: artifactBuffers.xlsx.length, sha256: sha256(artifactBuffers.xlsx) },
    workbook_build_report: { file: path.basename(buildReportPath), bytes: artifactBuffers.build_report.length, sha256: sha256(artifactBuffers.build_report) },
  },
  invariants: {
    silent_row_loss: SOURCE_ROWS - workingRows.length - reviewRows.length - excludedRows.length,
    duplicate_phrase_keys: joined.length - new Set(joined.map((row) => normalize(row.phrase))).size,
    step08_step10_phrase_set_difference: 0,
    step08_stage5_phrase_set_difference: 0,
    integrated_core_used_as_source: false,
    downstream_url_fields_exported: false,
    architecture_recommendations_exported: false,
  },
};
await fs.writeFile(manifestPath, JSON.stringify(manifest, null, 2) + "\n", "utf8");

// artifact-tool may externalize an oversized inspection as a sidecar. The bounded
// inspection evidence above is the authority; do not retain a duplicate 50+ MB dump.
await fs.rm(`${xlsxPath}.inspect.ndjson`, { force: true });

console.log(JSON.stringify({
  status: "PASS", outputDir, files: [semanticTsvGzipPath, groupTsvPath, xlsxPath, buildReportPath, manifestPath],
  counts: manifest.final_counts, sha256: manifest.artifacts,
}, null, 2));
