#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { gunzipSync } from "node:zlib";

const artifactToolModule = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES
  ? pathToFileURL(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES, "@oai/artifact-tool/dist/artifact_tool.mjs")).href
  : "@oai/artifact-tool";
const { FileBlob, SpreadsheetFile, Workbook } = await import(artifactToolModule);

const DATE = "2026-09-10";

function parseArgs(argv) {
  const out = {};
  for (let index = 0; index < argv.length; index += 1) {
    if (!argv[index].startsWith("--")) continue;
    out[argv[index].slice(2)] = argv[index + 1];
    index += 1;
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

function intValue(value) {
  return /^\d+$/.test(String(value)) ? Number(value) : 0;
}

function sha256(buffer) {
  return crypto.createHash("sha256").update(buffer).digest("hex");
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
  sheet.getRange("A2").format = {
    font: { name: "Arial", size: 15, bold: true, color: "#17365D" },
    verticalAlignment: "center",
  };
  sheet.getRange("A2").format.rowHeight = 28;
  sheet.mergeCells(`A3:${lastColumn}3`);
  sheet.getRange("A3").values = [[note]];
  sheet.getRange("A3").format = {
    font: { name: "Arial", size: 9, italic: true, color: "#4B5563" },
    wrapText: true,
    verticalAlignment: "center",
  };
  sheet.getRange("A3").format.rowHeight = 32;
  sheet.getRange(`A4:${lastColumn}4`).format.borders = { bottom: { style: "thin", color: "#9CA3AF" } };
}

function addDataSheet(workbook, config) {
  const {
    name, title, note, headers, rows, widths, tableName, freezeColumns = 1,
    statusColumn = null, bodyRowHeight = 30,
  } = config;
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
  sheet.getRange(`A5:${lastColumn}5`).format.rowHeight = 44;
  if (rows.length) {
    const body = sheet.getRangeByIndexes(5, 0, rows.length, headers.length);
    body.format = {
      font: { name: "Arial", size: 9, color: "#1F2937" },
      verticalAlignment: "top",
      wrapText: true,
    };
    body.format.borders = { insideHorizontal: { style: "thin", color: "#E5E7EB" } };
    body.format.rowHeight = bodyRowHeight;
  }
  widths.forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, rows.length + 5, 1).format.columnWidth = width;
  });
  const table = sheet.tables.add(`A5:${lastColumn}${rows.length + 5}`, true, tableName);
  table.style = "TableStyleMedium2";
  table.showFilterButton = true;
  table.showBandedRows = true;
  sheet.freezePanes.freezeRows(5);
  if (freezeColumns) sheet.freezePanes.freezeColumns(freezeColumns);
  if (statusColumn && rows.length) {
    const range = sheet.getRange(`${statusColumn}6:${statusColumn}${rows.length + 5}`);
    range.conditionalFormats.add("containsText", {
      text: "Готово", format: { fill: "#DCFCE7", font: { color: "#166534", bold: true } },
    });
    range.conditionalFormats.add("containsText", {
      text: "Нужно", format: { fill: "#FEF3C7", font: { color: "#92400E", bold: true } },
    });
    range.conditionalFormats.add("containsText", {
      text: "Отложено до доказательства", format: { fill: "#FEE2E2", font: { color: "#991B1B", bold: true } },
    });
    range.conditionalFormats.add("containsText", {
      text: "Исключено", format: { fill: "#FEE2E2", font: { color: "#991B1B" } },
    });
  }
  return sheet;
}

const OWNER_RU = {
  OWNER_EXISTING: "Точный владелец подтверждён",
  NO_SUITABLE_EXISTING_PAGE: "Нет подходящей точной страницы",
  OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP: "Вне целевого владения",
  PAGE_OWNERSHIP_NOT_APPLICABLE_UNTIL_TASK_RESOLVED: "Нужны доказательства для владельца",
};

const ACTION_RU = {
  KEEP_EXISTING_STRUCTURE: "Сохранить существующую структуру",
  ROUTE_TO_EXISTING_PAGE_AS_SUBTASK: "Назначить существующей странице без нового URL",
  DEFER_PENDING_EVIDENCE: "Отложить до доказательства",
  NO_STANDALONE_PAGE: "Не делать отдельную страницу",
  OUTSIDE_SCOPE_NO_ACTION: "Вне целевого действия",
  ADD_SECTION_OR_FAQ_TO_EXISTING: "Добавить раздел или FAQ на существующую страницу",
  EXPAND_EXISTING_PAGE: "Расширить существующую страницу",
};

const TARGET_RU = {
  EXISTING_FAMILY_OWNER: "Существующая страница-владелец семейства",
  OWNER_UNRESOLVED_EVIDENCE_REQUIRED: "Владелец не определён — нужны доказательства",
  NO_STANDALONE_PAGE: "Отдельная страница не требуется",
  OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP: "Целевой владелец вне области",
};

const PACKAGE_STATE_RU = {
  READY_IMPLEMENTATION_SPEC: "Готово к внедрению",
  PENDING_BUSINESS_DETAIL: "Нужна бизнес-деталь",
  PENDING_TECHNICAL_DETAIL: "Нужна техническая деталь",
  PENDING_PLACEMENT_OR_CONTEXT: "Нужно точное место",
  RECHECK_ONLY: "Только перепроверка",
  SEMANTIC_MAPPING_ONLY: "Только карта",
  NO_SITE_CHANGE: "Без изменения",
  HOLD: "Отложено до доказательства",
};

const SEARCH_ROUTE_RU = {
  CORE_CANDIDATE: "Принято в рабочее ядро",
  EXCLUDED_PRESERVED: "Исключено, строка сохранена",
  REVIEW_DEFERRED: "Проверка отложена",
  REVIEW_SEARCH: "Нужна проверка в обычной выдаче Яндекса",
};

const UNCERTAINTY_RU = {
  NONE: "Существенной неопределённости нет",
  HOLD: "Ожидает названного доказательства",
  CURRENT_OVERLAP_RECHECK: "Нужна повторная проверка похожих текущих страниц",
  LOW_CONFIDENCE: "Низкая уверенность — решение не усиливать без дополнительного доказательства",
  UNRESOLVED_SEARCH_REQUIRED: "Нужна точная проверка смысла в Яндексе",
};

function clientText(value) {
  const text = String(value ?? "").trim();
  if (!text || text === "NONE") return text ? "Дополнительное уточнение не требуется" : "";
  if (text === "AS_IS_PRESENT") return "Ссылка присутствует в сохранённом HTML";
  if (text === "AS_IS_ABSENT_PLANNED") return "Ссылка отсутствует; рекомендация сохранена";
  if (text.includes("Source and target resolve; link is visible/contextual")) {
    return "Источник и цель открываются; ссылка видима и уместна в контексте; цель соответствует задаче; повторной ссылки нет.";
  }
  return text
    .replace(/S18-A\d+(?:;S18-A\d+)*/g, "связанные принятые аналитические решения")
    .replaceAll("BUSINESS_CONFIRMATION_FOR_COMPANY_SPECIFIC_SERVICE_SCOPE", "подтверждение компанией фактического состава услуги")
    .replaceAll("DEFER_PENDING_EVIDENCE", "отложенным до появления доказательства решением")
    .replaceAll("PENDING_BUSINESS_DETAIL", "ожидает бизнес-уточнения")
    .replaceAll("READY", "готово")
    .replaceAll("HOLD", "отложено до доказательства")
    .replaceAll("Source and target resolve", "Источник и цель открываются")
    .replaceAll("link is visible/contextual", "ссылка видима и уместна в контексте")
    .replaceAll("target task matches note", "цель соответствует задаче")
    .replaceAll("no conflicting canonical owner", "нет конфликта с принятым владельцем")
    .replaceAll("PENDING:", "Ожидает уточнения:")
    .replaceAll("No visible text", "Видимого текста ссылки не было")
    .replaceAll("exact-match anchor", "анкор с точным вхождением")
    .replaceAll("exact-match", "с точным совпадением")
    .replaceAll("Literal href", "Фактический адрес ссылки")
    .replaceAll("company-specific", "подтверждённый компанией")
    .replaceAll("trigger", "условие возврата")
    .replaceAll("CTA", "призыв к действию")
    .replaceAll("CMS", "системе управления сайтом")
    .replaceAll("literal href", "фактический адрес ссылки")
    .replaceAll("phrase/unit→target map", "карту «фраза/задача → целевая страница»")
    .replaceAll("query→URL evidence", "данные «запрос → URL»")
    .replaceAll("authoritative evidence", "приемлемое доказательство")
    .replaceAll("exact owner", "точного владельца")
    .replaceAll("family owner", "владельца семейства");
}

const DELTA_RU = {
  ROUTING_SUPPORT_ADDITION: ["Добавлена поддерживающая роль", "Существующий владелец сохранён; найденная страница учитывается как узкая поддержка."],
  CANNIBALIZATION_CANDIDATE: ["Похожая страница учтена безопасно", "Пара зарегистрирована для контроля; объединение, удаление и перенаправление не доказаны."],
  BOUNDARY_SPECIALIST_OVERRIDE: ["Уточнён узкий специалист", "Узкое намерение закреплено за существующей специальной страницей, широкая роль сохранена."],
  OWNER_STATE_CHANGE: ["Уточнено владение", "Текущая страница подтверждает более точное состояние владельца без новой страницы."],
  OWNER_SPECIALIST_UPDATE: ["Найден существующий специалист", "Узкая задача направлена на найденную существующую страницу."],
  ROUTING_OWNER_UPDATE: ["Уточнён семейный маршрут", "Существующий маршрут обновлён без физического изменения структуры."],
};

const args = parseArgs(process.argv.slice(2));
if (!args["input-dir"] || !args["output-dir"]) {
  throw new Error("Usage: build_client_candidate_workbook.mjs --input-dir <dir> --output-dir <dir> [--preview-dir <dir>]");
}
const inputDir = path.resolve(args["input-dir"]);
const outputDir = path.resolve(args["output-dir"]);
const previewDir = args["preview-dir"] ? path.resolve(args["preview-dir"]) : null;

const readText = async (name) => fs.readFile(path.join(inputDir, name), "utf8");
const readGzipTsv = async (name) => parseTsv(gunzipSync(await fs.readFile(path.join(inputDir, name))).toString("utf8"));
const readTsv = async (name) => parseTsv(await readText(name));

const foundation = await readGzipTsv(`MK02_SEMANTIC_FOUNDATION_${DATE}.tsv.gz`);
const phraseMap = await readGzipTsv(`MK02_PHRASE_PAGE_MAP_${DATE}.tsv.gz`);
const unitLedger = await readTsv(`MK02_UNIT_OWNERSHIP_LEDGER_${DATE}.tsv`);
const currentTopology = await readGzipTsv(`MK02_CURRENT_SITE_TOPOLOGY_${DATE}.tsv.gz`);
const targetArchitecture = await readTsv(`MK02_TARGET_SEARCH_ARCHITECTURE_${DATE}.tsv`);
const delta = await readTsv(`MK02_CURRENT_TARGET_DELTA_${DATE}.tsv`);
const packages = await readTsv(`MK02_IMPLEMENTATION_WORK_PACKAGES_${DATE}.tsv`);
const clarifications = await readTsv(`MK02_CLARIFICATIONS_NO_CHANGE_HOLD_${DATE}.tsv`);
const relations = await readTsv(`MK02_PAGE_RELATIONSHIPS_${DATE}.tsv`);
const acceptance = await readTsv(`MK02_IMPLEMENTATION_ACCEPTANCE_${DATE}.tsv`);
const measurements = await readTsv(`MK02_ACCEPTANCE_MEASUREMENT_INTERFACE_${DATE}.tsv`);

if (foundation.length !== 2840 || phraseMap.length !== 2185 || targetArchitecture.length !== 160) {
  throw new Error("input count invariant failed");
}
if (packages.length !== 47 || clarifications.length !== 44 || relations.length !== 14 || acceptance.length !== 3) {
  throw new Error("implementation count invariant failed");
}

const phraseMapByPhrase = new Map(phraseMap.map((row) => [row.phrase, row]));
const working = foundation.filter((row) => row.in_working_core === "Да");
const review = foundation.filter((row) => ["Проверка отложена", "Нужна проверка в обычной выдаче Яндекса"].includes(row.product_status));
const excluded = foundation.filter((row) => row.product_status.startsWith("Исключено"));
if (working.length !== 2185 || review.length !== 187 || excluded.length !== 468) throw new Error("semantic status accounting failed");

const byGroup = new Map();
for (const row of working) {
  if (!byGroup.has(row.group_id)) byGroup.set(row.group_id, []);
  byGroup.get(row.group_id).push(row);
}
const groupRows = [...byGroup.entries()].map(([groupId, rows]) => {
  const sorted = [...rows].sort((a, b) => intValue(b.wordstat_popular_count) - intValue(a.wordstat_popular_count) || a.phrase.localeCompare(b.phrase, "ru"));
  const mapped = rows.map((row) => phraseMapByPhrase.get(row.phrase));
  return {
    groupId,
    name: rows[0].group_name,
    task: rows[0].user_task,
    intent: rows[0].intent,
    role: rows[0].topic_role,
    count: rows.length,
    exact: mapped.filter((row) => row?.exact_owner_state === "OWNER_EXISTING").length,
    family: mapped.filter((row) => row?.family_owner_url).length,
    examples: sorted.slice(0, 4).map((row) => row.phrase).join("; "),
  };
}).sort((a, b) => b.count - a.count || a.name.localeCompare(b.name, "ru"));
if (groupRows.length !== 54) throw new Error("working group count failed");

const allRows = [...foundation].sort((a, b) => a.phrase.localeCompare(b.phrase, "ru")).map((row) => [
  row.phrase, row.product_status, row.in_working_core, row.group_name, row.user_task, row.intent, row.topic_role,
  row.decision_basis, row.uncertainty, intValue(row.wordstat_popular_count), intValue(row.wordstat_associated_count),
  row.wordstat_evidence_type, SEARCH_ROUTE_RU[row.search_stage_disposition] || "Состояние проверки сохранено", "Москва",
]);
const workingRows = [...working].sort((a, b) => a.group_name.localeCompare(b.group_name, "ru") || intValue(b.wordstat_popular_count) - intValue(a.wordstat_popular_count)).map((row) => [
  row.group_name, row.phrase, row.user_task, row.intent, row.topic_role, intValue(row.wordstat_popular_count),
  intValue(row.wordstat_associated_count), row.uncertainty, row.decision_basis,
]);
const groupMatrix = groupRows.map((row) => [row.name, row.count, row.task, row.intent, row.role, row.exact, row.family, row.examples]);
const unitTaskInfo = new Map();
for (const row of phraseMap) {
  if (!row.structural_unit_id) continue;
  if (!unitTaskInfo.has(row.structural_unit_id)) unitTaskInfo.set(row.structural_unit_id, { tasks: new Set(), phrases: [] });
  const info = unitTaskInfo.get(row.structural_unit_id);
  info.tasks.add(row.user_task);
  info.phrases.push(row.phrase);
}
const mapRows = [...phraseMap].sort((a, b) => a.semantic_group_name.localeCompare(b.semantic_group_name, "ru") || a.phrase.localeCompare(b.phrase, "ru")).map((row) => [
  row.phrase, row.semantic_group_name, row.user_task, row.intent, OWNER_RU[row.exact_owner_state], row.exact_owner_url,
  row.family_owner_url, row.supporting_pages, row.observed_search_relevant_url || "Не наблюдался для точной фразы",
  row.observed_search_evidence_scope === "EXACT_QUERY_CHECK__TARGET_HOST_NOT_OBSERVED_IN_TOP10" ? "Точная фраза проверена; домен не найден в TOP10" : "Нет отдельной точной проверки",
  ACTION_RU[row.structural_action] || "Решение отложено до разрешения задачи", UNCERTAINTY_RU[row.uncertainty_state] || clientText(row.uncertainty_state),
]);

const currentRelevant = currentTopology.filter((row) => ["UPSTREAM_ACCEPTED_CURRENT", "ARCHITECTURE_MATERIAL"].includes(row.architecture_class));
if (currentRelevant.length !== 80) throw new Error(`current relevant expected 80, got ${currentRelevant.length}`);
const currentRows = currentRelevant.sort((a, b) => a.current_url.localeCompare(b.current_url)).map((row) => [
  row.current_url,
  row.architecture_class === "ARCHITECTURE_MATERIAL" ? "Значима для поисковой архитектуры" : "Принятая текущая страница владельца/поддержки",
  row.fetch_state === "LIVE_PASS" || row.fetch_state === "OPENED" ? "Страница открыта и прочитана" : "Состояние разрешено независимой проверкой",
  row.architecture_class === "ARCHITECTURE_MATERIAL"
    ? "Независимо найденная страница проверена против целевой структуры; её узкая или поддерживающая роль учтена."
    : "Страница подтверждена как текущий владелец, специалист или поддержка принятой пользовательской задачи.",
  row.snapshot_date, "Сохранённый публичный снимок; повторного чтения сайта в репетиции не было",
]);

const targetRows = targetArchitecture.sort((a, b) => a.user_task.localeCompare(b.user_task, "ru")).map((row) => [
  (() => {
    const info = unitTaskInfo.get(row.structural_unit_id);
    const tasks = info ? [...info.tasks].slice(0, 2).join(" / ") : "Задача требует уточнения";
    const examples = info ? [...new Set(info.phrases)].sort((a, b) => a.localeCompare(b, "ru")).slice(0, 3).join(", ") : "";
    return examples ? `${tasks}. Примеры: ${examples}` : tasks;
  })(),
  intValue(row.active_phrase_count), TARGET_RU[row.target_state], row.target_family_owner_url,
  row.supporting_pages,
  row.target_state === "EXISTING_FAMILY_OWNER"
    ? (row.supporting_pages ? "Страница-владелец с поддерживающими материалами" : "Страница-владелец задачи")
    : (row.target_state === "NO_STANDALONE_PAGE" ? "Задача без отдельной страницы" : "Целевая страница не назначена"),
  ACTION_RU[row.structural_action], UNCERTAINTY_RU[row.uncertainty_state] || clientText(row.uncertainty_state),
]);

const deltaRows = delta.map((row) => {
  if (row.delta_class === "CURRENT_PAGE_TO_TARGET_RECONCILIATION") {
    const [title, decision] = DELTA_RU[row.target_state] || ["Уточнение текущей страницы", "Роль страницы согласована с целевой картой."];
    return ["Страница", row.current_object, "", title, decision, "Нет", "Карта/граница обновлена", "Разрушительное действие не требуется"];
  }
  const present = row.action_state === "NO_CHANGE_ALREADY_PRESENT";
  return [
    "Связь страниц", row.current_object, row.target_object,
    present ? "Ссылка уже присутствует" : "Ссылка отсутствует в сохранённом снимке",
    present ? "Сохранить полезный переход" : "Подтвердить точный блок/абзац до внедрения",
    present ? "Нет" : "Не определено до уточнения места",
    present ? "Без изменения" : "Нужно точное место",
    "Не объединять страницы и не добавлять повторную ссылку",
  ];
});

const packageRows = packages.sort((a, b) => {
  const order = { READY_IMPLEMENTATION_SPEC: 0, PENDING_BUSINESS_DETAIL: 1, PENDING_PLACEMENT_OR_CONTEXT: 2, RECHECK_ONLY: 3, SEMANTIC_MAPPING_ONLY: 4, NO_SITE_CHANGE: 5, HOLD: 6 };
  return order[a.client_state] - order[b.client_state] || a.page_or_object.localeCompare(b.page_or_object, "ru");
}).map((row) => [
  PACKAGE_STATE_RU[row.client_state], clientText(row.page_or_object), clientText(row.exact_change), clientText(row.evidence_meaning),
  clientText(row.as_is_current_state), clientText(row.exact_location_or_context), clientText(row.to_be_state), clientText(row.dependencies),
  clientText(row.preservation_do_not_break), clientText(row.acceptance_check), row.analytical_importance,
  row.client_state === "READY_IMPLEMENTATION_SPEC" ? "Всё указанное действие" :
    row.client_state === "PENDING_BUSINESS_DETAIL" ? "Только нейтральное объяснение роли монтажа; состав услуги — после подтверждения" :
    row.client_state === "SEMANTIC_MAPPING_ONLY" ? "Только назначение в карте; не CMS" :
    row.client_state === "NO_SITE_CHANGE" ? "Физическое изменение не требуется" : "",
  clientText(row.one_concrete_clarification), "Номер строки не задаёт производственную очередь",
]);

const clarificationRows = clarifications.sort((a, b) => a.state.localeCompare(b.state) || a.page_or_object.localeCompare(b.page_or_object, "ru")).map((row) => [
  PACKAGE_STATE_RU[row.state], clientText(row.page_or_object), clientText(row.what_this_means), clientText(row.one_concrete_clarification_or_check),
  clientText(row.what_not_to_do_now), clientText(row.return_to_ready_condition),
]);
const relationRows = relations.sort((a, b) => a.source_url.localeCompare(b.source_url) || a.target_url.localeCompare(b.target_url)).map((row) => [
  row.source_url, row.target_url, row.current_link_present === "YES" ? "Присутствует" : "Отсутствует",
  row.current_link_present === "YES" ? "Без изменения" : "Нужно точное место", row.anchor_or_context === "No matching normalized href" ? "Подходящая ссылка не найдена" : clientText(row.anchor_or_context),
  row.current_link_present === "YES" ? "Сохранить существующий переход" : "Подтвердить блок/абзац и только затем добавить одну ссылку",
  clientText(row.acceptance_check),
]);

const workbook = Workbook.create();

const guide = workbook.worksheets.add("Начните здесь");
styleTitle(guide, "OKNO_MSK — семантика, SEO-структура и ТЗ", "Отдельный результат для действующего сайта · Москва · Яндекс · сохранённые доказательства · текущий сайт до 02.09.2026", "H");
guide.getRange("A6:H6").values = [["Что считать результатом", "", "Значение", "", "Как использовать", "", "", ""]];
guide.getRange("A6:H6").format = { fill: "#17365D", font: { name: "Arial", bold: true, color: "#FFFFFF" } };
const guideLabels = [
  ["Всего сохранено фраз", "Полный набор с причинами статуса"],
  ["Рабочее ядро", "Фразы для карты задач и страниц"],
  ["Рабочие группы", "Смысловые задачи, не готовые URL"],
  ["Точный владелец подтверждён", "Не путать с владельцем семейства"],
  ["Готовые задания", "Можно выполнять и принимать по критерию"],
  ["Нужно уточнить место", "Не передавать разработчику как готовое задание"],
  ["Новая страница / разделение / объединение", "Не обоснованы текущими доказательствами"],
];
guide.getRange("A7:B13").values = guideLabels.map(([label]) => [label, ""]);
guide.getRange("E7:H13").values = guideLabels.map(([, note]) => [note, "", "", ""]);
for (let row = 7; row <= 13; row += 1) {
  guide.mergeCells(`A${row}:B${row}`);
  guide.mergeCells(`C${row}:D${row}`);
  guide.mergeCells(`E${row}:H${row}`);
}
guide.getRange("C7:C13").values = [[0], [0], [0], [0], [0], [0], [0]];
guide.getRange("A7:H13").format = { font: { name: "Arial", size: 10 }, wrapText: true, verticalAlignment: "center" };
guide.getRange("A7:H13").format.borders = { insideHorizontal: { style: "thin", color: "#D1D5DB" } };
guide.getRange("C7:D13").format = { font: { name: "Arial", size: 12, bold: true, color: "#0F6B78" }, horizontalAlignment: "center" };
guide.getRange("A15:H15").merge();
guide.getRange("A15").values = [["Порядок работы"]];
guide.getRange("A15").format = { fill: "#0F6B78", font: { name: "Arial", bold: true, color: "#FFFFFF" } };
const guideSteps = [
  ["1", "Главные выводы", "Сначала понять спрос, покрытие страницами и безопасные границы."],
  ["2", "ТЗ на доработку", "Выполнять только строки со статусом «Готово к внедрению»."],
  ["3", "Карта страниц", "Различать точного владельца, владельца семейства и поддержку."],
  ["4", "Проверить и отложено", "Получить один названный факт или выполнить указанную перепроверку."],
  ["5", "Все запросы", "Полный набор, включая спорные и исключённые строки."],
  ["6", "Граница", "Номера не задают график; Google, ИИ и конкурентное расширение не использованы."],
];
guide.getRange("A17:H22").values = guideSteps.map((row) => [row[0], row[1], row[2], "", "", "", "", ""]);
for (let row = 17; row <= 22; row += 1) guide.mergeCells(`C${row}:H${row}`);
guide.getRange("A17:H22").format = { font: { name: "Arial", size: 10 }, wrapText: true, verticalAlignment: "top" };
guide.getRange("A17:A22").format = { font: { name: "Arial", size: 11, bold: true, color: "#17365D" }, horizontalAlignment: "center" };
guide.getRange("A1:A22").format.columnWidth = 18;
guide.getRange("B1:B22").format.columnWidth = 24;
guide.getRange("C1:D22").format.columnWidth = 14;
guide.getRange("E1:H22").format.columnWidth = 18;
guide.getRange("A7:H13").format.rowHeight = 30;
guide.getRange("A17:H22").format.rowHeight = 34;
guide.freezePanes.freezeRows(5);

const findings = [
  ["Спрос", "Рабочее ядро — 2 185 из 2 840 фраз (76,9%).", "54 рабочие смысловые группы.", "Использовать рабочее ядро; 187 спорных и 468 исключённых строк сохранены отдельно."],
  ["Крупнейшие задачи", "Пластиковые окна (282), фурнитура (239), ремонт (179), балконы (128), веранды/террасы (128).", "Группы построены по задаче, а не только по словам.", "Не превращать каждую группу или модификатор в отдельную страницу."],
  ["Точное владение", "1 647 рабочих фраз имеют точного существующего владельца.", "75,4% рабочего ядра.", "Использовать точный URL только там, где он заполнен."],
  ["Семейное покрытие", "1 882 рабочие фразы имеют владельца семейства.", "86,1% рабочего ядра.", "Владелец семейства не подменяет точного владельца."],
  ["Нет точной страницы", "518 фраз не имеют подходящей точной страницы; у части есть семейный маршрут.", "Отсутствие точной страницы сохранено явно.", "Не считать это автоматическим созданием страницы."],
  ["Неопределённость", "6 активных фраз не получили владельца до доказательства.", "URL намеренно пуст.", "Сохранить на проверке, не выдумывать цель."],
  ["Текущий сайт", "Обработано 2 683 URL; из 2 624 дополнительных только 21 изменил понимание архитектуры.", "Снимок 02.09.2026.", "Работать с 59 существующими страницами-владельцами семейств, а не со всем техническим списком."],
  ["Структурное решение", "70 смысловых единиц — сохранить, 45 — только назначить странице, 19 — отложить, 14 — без отдельной страницы.", "160 активных смысловых единиц.", "Основной результат — безопасное использование существующей структуры."],
  ["Контентный резерв", "Подтверждены 6 добавлений раздела/FAQ и 2 расширения существующей страницы.", "8 единиц с доказанным пробелом содержания.", "Выполнять три полностью готовых задания; четыре ждут одного точного места, одна — бизнес-детали."],
  ["Похожие страницы", "21 случай; вредная историческая конкуренция не доказана.", "Закрытая история запрос→URL отсутствует.", "Не объединять, не удалять и не перенаправлять по текущему сходству."],
  ["Новые/разрушительные действия", "Новая страница — 0; разделение — 0; объединение — 0; перенаправление/удаление — 0.", "Проверены текущие страницы и альтернативы.", "Ноль — полезное решение «не менять», а не отсутствие результата."],
  ["Внедрение", "47 заданий: 3 готово, 1 бизнес-деталь, 10 точных мест, 4 перепроверки, 19 назначений, 9 без изменения, 1 отложено.", "Неоднозначные места не выданы за готовность; сводный пакет ссылок разложен на уникальные пары.", "Передавать исполнителю только готовые строки; остальные обрабатывать по своему статусу."],
];
addDataSheet(workbook, {
  name: "Главные выводы", title: "Что показало исследование", note: "Результаты о спросе, владении, структуре и границах действий. Это не технический журнал выполнения.",
  headers: ["Тема", "Вывод", "Доказательная опора", "Практическое решение"], rows: findings,
  widths: [24, 78, 44, 74], tableName: "KeyFindings", freezeColumns: 0, bodyRowHeight: 46,
});

const allSheet = addDataSheet(workbook, {
  name: "Все запросы", title: "Полный сохранённый набор запросов", note: "2 840 уникальных фраз. Рабочие, спорные и исключённые строки остаются в одном наборе; ни одна не потеряна молча.",
  headers: ["Поисковая фраза", "Итоговый статус", "В рабочем ядре", "Группа", "Задача пользователя", "Интент", "Роль темы", "Причина решения", "Уверенность", "Вордстат: популярные", "Вордстат: похожие", "Тип данных Вордстата", "Маршрут проверки", "Регион"],
  rows: allRows, widths: [42, 32, 15, 32, 48, 30, 26, 62, 18, 18, 18, 40, 36, 14], tableName: "AllQueriesClient", freezeColumns: 2, statusColumn: "B",
});
allSheet.getRange(`J6:K${allRows.length + 5}`).format.numberFormat = "#,##0";

const workSheet = addDataSheet(workbook, {
  name: "Рабочее ядро", title: "Рабочее семантическое ядро", note: "2 185 фраз для практической карты задач и страниц. Частотность — относительный сигнал внутри сохранённого Wordstat-снимка, не прогноз трафика.",
  headers: ["Группа", "Поисковая фраза", "Задача пользователя", "Интент", "Роль темы", "Вордстат: популярные", "Вордстат: похожие", "Уверенность", "Основание включения"],
  rows: workingRows, widths: [32, 44, 50, 30, 26, 18, 18, 18, 62], tableName: "WorkingCoreClient", freezeColumns: 2,
});
workSheet.getRange(`F6:G${workingRows.length + 5}`).format.numberFormat = "#,##0";

const groupsSheet = addDataSheet(workbook, {
  name: "Группы и задачи", title: "Рабочие смысловые группы", note: "54 группы, сформированные по пользовательской задаче и интенту. Группа не является автоматической новой страницей.",
  headers: ["Группа", "Рабочих фраз", "Задача пользователя", "Интент", "Роль темы", "С точным владельцем", "С владельцем семейства", "Примеры формулировок"],
  rows: groupMatrix, widths: [34, 16, 54, 30, 26, 19, 21, 82], tableName: "TaskGroupsClient", freezeColumns: 1,
});
groupsSheet.getRange(`B6:B${groupMatrix.length + 5}`).format.numberFormat = "#,##0";
groupsSheet.getRange(`F6:G${groupMatrix.length + 5}`).format.numberFormat = "#,##0";

addDataSheet(workbook, {
  name: "Карта страниц", title: "Запрос → точный владелец → владелец семейства → поддержка", note: "2 185 рабочих строк. Пустой точный URL означает отсутствие доказательства, а не разрешение создать страницу.",
  headers: ["Поисковая фраза", "Группа", "Задача пользователя", "Интент", "Состояние точного владельца", "Точный владелец", "Владелец семейства", "Поддерживающие страницы", "URL из точной выдачи", "Состояние точной проверки", "Структурное решение", "Неопределённость"],
  rows: mapRows, widths: [42, 32, 48, 28, 34, 46, 46, 58, 44, 38, 46, 28], tableName: "PageOwnershipClient", freezeColumns: 2, statusColumn: "E",
});

addDataSheet(workbook, {
  name: "Текущий сайт", title: "Текущие страницы, значимые для результата", note: "80 релевантных страниц из полного технического реестра 2 683 URL. Полный список намеренно не выведен в рабочий клиентский лист.",
  headers: ["Текущий URL", "Роль в сверке", "Состояние чтения", "Что подтверждено", "Дата снимка", "Ограничение свежести"],
  rows: currentRows, widths: [62, 42, 28, 78, 16, 68], tableName: "CurrentSiteClient", freezeColumns: 1,
});

addDataSheet(workbook, {
  name: "Целевая структура", title: "Целевая поисковая структура", note: "160 активных смысловых единиц. Это поисковая архитектура, а не буквальная текущая навигация и не проект нового меню.",
  headers: ["Задача пользователя", "Рабочих фраз", "Целевое состояние", "Владелец семейства", "Поддерживающие страницы", "Роль страницы", "Решение", "Неопределённость"],
  rows: targetRows, widths: [56, 16, 42, 54, 68, 34, 52, 28], tableName: "TargetArchitectureClient", freezeColumns: 1,
});

addDataSheet(workbook, {
  name: "Изменения", title: "Текущее состояние → целевое решение", note: "21 сверка страниц + 14 уникальных отношений между страницами. Рекомендация отделена от фактического состояния ссылки.",
  headers: ["Объект", "Источник / текущая страница", "Цель", "Что обнаружено", "Целевое решение", "Нужно менять сайт", "Статус", "Граница безопасности"],
  rows: deltaRows, widths: [20, 58, 58, 42, 62, 24, 30, 58], tableName: "CurrentTargetDeltaClient", freezeColumns: 1, statusColumn: "G",
});

addDataSheet(workbook, {
  name: "ТЗ на доработку", title: "Задания и состояния готовности", note: "Внедрять можно только строки «Готово к внедрению». Нумерация не является производственной очередью.",
  headers: ["Статус", "Страница / объект", "Что сделать", "Почему", "Сейчас", "Где / контекст", "Как должно быть", "Зависимости", "Что сохранить", "Как принять", "Аналитическая значимость", "Готовая часть", "Что уточнить", "Граница"],
  rows: packageRows, widths: [28, 62, 70, 72, 70, 58, 70, 60, 68, 68, 34, 42, 72, 44], tableName: "ImplementationPackagesClient", freezeColumns: 2, statusColumn: "A", bodyRowHeight: 64,
});

addDataSheet(workbook, {
  name: "Проверить и отложено", title: "Уточнения, решения без изменения и отложенные задачи", note: "40 строк не готовы к внедрению. Здесь видно одно конкретное уточнение/проверка и условие возврата к готовности.",
  headers: ["Статус", "Страница / объект", "Что это означает", "Что уточнить или проверить", "Чего не делать сейчас", "Когда можно вернуть к готовности"],
  rows: clarificationRows, widths: [28, 62, 74, 78, 72, 72], tableName: "ClarificationsClient", freezeColumns: 2, statusColumn: "A", bodyRowHeight: 58,
});

addDataSheet(workbook, {
  name: "Связи страниц", title: "Проверенные отношения между страницами", note: "14 уникальных пар из 15 исходных строк: одна повторная пара объединена без потери происхождения. 8 пар уже присутствуют, 6 ждут точного места.",
  headers: ["Страница-источник", "Целевая страница", "Фактическое состояние", "Статус действия", "Наблюдённый контекст", "Что делать", "Как принять"],
  rows: relationRows, widths: [60, 60, 22, 28, 50, 72, 72], tableName: "PageRelationsClient", freezeColumns: 2, statusColumn: "D", bodyRowHeight: 50,
});

const verifySheet = workbook.worksheets.add("Как проверить");
styleTitle(verifySheet, "Приёмка готовых изменений", "Сначала принять 3 готовых задания по точным критериям; затем использовать 6 общих классов измерения без обещания гарантированного прироста.", "G");
const acceptanceHeaders = ["Страница / объект", "Что должно появиться", "Где проверить", "Критерий приёмки", "Что сохранить"];
const acceptanceRows = acceptance.map((row) => [row.page_or_object, clientText(row.what_must_be_present), clientText(row.where_to_check), clientText(row.acceptance_check), clientText(row.preserve)]);
verifySheet.getRangeByIndexes(4, 0, acceptanceRows.length + 1, acceptanceHeaders.length).values = [acceptanceHeaders, ...acceptanceRows];
verifySheet.getRange("A5:E5").format = { fill: "#17365D", font: { name: "Arial", bold: true, color: "#FFFFFF" }, wrapText: true };
verifySheet.getRange(`A6:E${acceptanceRows.length + 5}`).format = { font: { name: "Arial", size: 9 }, wrapText: true, verticalAlignment: "top" };
verifySheet.getRange(`A6:E${acceptanceRows.length + 5}`).format.rowHeight = 52;
verifySheet.tables.add(`A5:E${acceptanceRows.length + 5}`, true, "ReadyAcceptanceClient").style = "TableStyleMedium2";
const measurementStart = acceptanceRows.length + 8;
verifySheet.mergeCells(`A${measurementStart}:G${measurementStart}`);
verifySheet.getRange(`A${measurementStart}`).values = [["Общий интерфейс измерения"]];
verifySheet.getRange(`A${measurementStart}`).format = { fill: "#0F6B78", font: { name: "Arial", bold: true, color: "#FFFFFF" } };
const measurementHeaders = ["Применяется к", "Ожидаемый результат", "Минимальная проверка", "Опциональная метрика Яндекса", "Когда пересмотреть", "Если не прошло", "Граница обещания"];
const measurementRows = measurements.map((row) => [
  clientText(row.applies_to), clientText(row.expected_outcome), clientText(row.minimum_acceptance_verification),
  clientText(row.optional_yandex_first_party_metric), clientText(row.review_trigger), clientText(row.failure_policy), clientText(row.claim_boundary),
]);
verifySheet.getRangeByIndexes(measurementStart, 0, measurementRows.length + 1, measurementHeaders.length).values = [measurementHeaders, ...measurementRows];
verifySheet.getRange(`A${measurementStart + 1}:G${measurementStart + 1}`).format = { fill: "#17365D", font: { name: "Arial", bold: true, color: "#FFFFFF" }, wrapText: true };
verifySheet.getRange(`A${measurementStart + 2}:G${measurementStart + measurementRows.length + 1}`).format = { font: { name: "Arial", size: 9 }, wrapText: true, verticalAlignment: "top" };
verifySheet.getRange(`A${measurementStart + 2}:G${measurementStart + measurementRows.length + 1}`).format.rowHeight = 62;
verifySheet.tables.add(`A${measurementStart + 1}:G${measurementStart + measurementRows.length + 1}`, true, "MeasurementInterfaceClient").style = "TableStyleMedium2";
[58, 70, 70, 68, 58, 66, 58].forEach((width, index) => verifySheet.getRangeByIndexes(0, index, measurementStart + measurementRows.length + 2, 1).format.columnWidth = width);
verifySheet.freezePanes.freezeRows(5);
verifySheet.freezePanes.freezeColumns(1);

// Cross-sheet formulas are assigned only after every referenced sheet exists.
guide.getRange("C7:C13").formulas = [
  ["=COUNTA('Все запросы'!A6:A2845)"],
  ["=COUNTA('Рабочее ядро'!A6:A2190)"],
  ["=COUNTA('Группы и задачи'!A6:A59)"],
  ["=COUNTIF('Карта страниц'!E6:E2190,\"Точный владелец подтверждён\")"],
  ["=COUNTIF('ТЗ на доработку'!A6:A52,\"Готово к внедрению\")"],
  ["=COUNTIF('ТЗ на доработку'!A6:A52,\"Нужно точное место\")"],
  ["=0"],
];

workbook.recalculate();

const inspections = {};
const inspectRanges = {
  "Начните здесь": "A1:H23",
  "Главные выводы": "A1:D18",
  "Все запросы": "A1:N16",
  "Рабочее ядро": "A1:I16",
  "Группы и задачи": "A1:H20",
  "Карта страниц": "A1:L16",
  "Текущий сайт": "A1:G18",
  "Целевая структура": "A1:H18",
  "Изменения": "A1:H20",
  "ТЗ на доработку": "A1:N15",
  "Проверить и отложено": "A1:F16",
  "Связи страниц": "A1:G19",
  "Как проверить": `A1:G${measurementStart + measurementRows.length + 1}`,
};
for (const [sheetName, range] of Object.entries(inspectRanges)) {
  const inspected = await workbook.inspect({ kind: "table", range: `${sheetName}!${range}`, include: "values,formulas", tableMaxRows: 24, tableMaxCols: 16, maxChars: 16000 });
  inspections[sheetName] = inspected.ndjson;
}
const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 },
  summary: "MK02 candidate workbook formula error scan",
});

await fs.mkdir(outputDir, { recursive: true });
const xlsxPath = path.join(outputDir, `OKNO_MSK_MK02_CLIENT_CANDIDATE_${DATE}.xlsx`);
const buildReportPath = path.join(outputDir, `MK02_CLIENT_WORKBOOK_BUILD_REPORT_${DATE}.json`);
const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(xlsxPath);

if (previewDir) {
  await fs.mkdir(previewDir, { recursive: true });
  for (const [sheetName, range] of Object.entries(inspectRanges)) {
    const renderRange = sheetName === "Все запросы" ? "A1:J24" : sheetName === "Карта страниц" ? "A1:J24" : sheetName === "ТЗ на доработку" ? "A1:H14" : range;
    const image = await workbook.render({ sheetName, range: renderRange, scale: 1, format: "png" });
    const fileName = sheetName.replace(/\s+/g, "_") + ".png";
    await fs.writeFile(path.join(previewDir, fileName), new Uint8Array(await image.arrayBuffer()));
  }
}

const imported = await SpreadsheetFile.importXlsx(await FileBlob.load(xlsxPath));
const importedSheets = await imported.inspect({ kind: "sheet", include: "id,name", maxChars: 10000 });
const importedGuide = await imported.inspect({ kind: "table", range: "Начните здесь!A1:H23", include: "values,formulas", tableMaxRows: 24, tableMaxCols: 8, maxChars: 12000 });
const importedErrors = await imported.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 300 },
  summary: "MK02 saved candidate workbook formula error scan",
});

const xlsxBuffer = await fs.readFile(xlsxPath);
const sheetOrder = Object.keys(inspectRanges);
const buildReport = {
  schema: "MK02_OKNO_MSK_CLIENT_CANDIDATE_WORKBOOK_V1",
  date: DATE,
  status: "PASS",
  artifact_tool_used: true,
  workbook_recalculated: true,
  workbook_sheet_order: sheetOrder,
  sheet_count: sheetOrder.length,
  rendered_sheet_count: previewDir ? sheetOrder.length : 0,
  source_counts: {
    universe: foundation.length,
    working_core: working.length,
    review_uncertain: review.length,
    excluded: excluded.length,
    working_groups: groupRows.length,
    phrase_page_rows: phraseMap.length,
    current_relevant_pages: currentRelevant.length,
    target_units: targetArchitecture.length,
    delta_rows: delta.length,
    work_packages: packages.length,
    clarifications_no_change_hold: clarifications.length,
    page_relations: relations.length,
    ready_acceptance_rows: acceptance.length,
    measurement_classes: measurements.length,
  },
  formula_error_scan_before_export: formulaErrors.ndjson,
  formula_error_scan_after_import: importedErrors.ndjson,
  imported_sheet_inspection: importedSheets.ndjson,
  imported_guide_inspection: importedGuide.ndjson,
  bounded_range_inspections: inspections,
  output: { file: path.basename(xlsxPath), bytes: xlsxBuffer.length, sha256: sha256(xlsxBuffer) },
};
await fs.writeFile(buildReportPath, JSON.stringify(buildReport, null, 2) + "\n", "utf8");
await fs.rm(`${xlsxPath}.inspect.ndjson`, { force: true });

console.log(JSON.stringify({ status: "PASS", xlsxPath, buildReportPath, sheetOrder, output: buildReport.output, counts: buildReport.source_counts }, null, 2));
