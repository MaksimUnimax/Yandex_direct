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
const CLAIM_BOUNDARY = "Broad Wordstat getTop, Москва 213, DEVICE_ALL, без операторов; не exact-частотность и не прогноз трафика";

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

function targetDisplay(row) {
  if (row.final_primary_page) return row.final_primary_page;
  if (ASSIGNED_STATES.has(row.final_semantic_state)) {
    return `НЕТ ОТДЕЛЬНОЙ СТРАНИЦЫ — ${row.canonical_structural_action}`;
  }
  if (row.final_semantic_state === "SEARCH_REQUIRED") return "НЕ НАЗНАЧЕНО — SEARCH_REQUIRED";
  return "НЕ ПРИМЕНИМО — ВНЕ АКТИВНОГО ЯДРА";
}

function missingText(row, fieldName) {
  if (row[fieldName]) return row[fieldName];
  if (row.final_semantic_state === "SEARCH_REQUIRED") return "НЕ НАЗНАЧЕНО — SEARCH_REQUIRED";
  if (!ACTIVE_STATES.has(row.final_semantic_state)) return "НЕ ПРИМЕНИМО — ВНЕ АКТИВНОГО ЯДРА";
  return "НЕ ПРИМЕНИМО ПО CANONICAL AUTHORITY";
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
  if (!ACTIVE_STATES.has(state)) return ["P5 — ВНЕ РАБОЧЕГО ЯДРА", `status=${state}`];
  if (state === "SEARCH_REQUIRED") {
    return ["P0 — СНЯТЬ SEARCH_REQUIRED", `status=${state}; uncertainty=${uncertainty}; broad_result=${row.resultCount}`];
  }
  if (uncertainty === "HOLD" || action === "DEFER_PENDING_EVIDENCE" || maturity.startsWith("DEFERRED")) {
    return ["P0 — СНЯТЬ НЕОПРЕДЕЛЁННОСТЬ", `action=${action}; maturity=${maturity}; uncertainty=${uncertainty}; broad_result=${row.resultCount}`];
  }
  if (["ADD_SECTION_OR_FAQ_TO_EXISTING", "EXPAND_EXISTING_PAGE"].includes(action)) {
    if (maturity.startsWith("FINAL")) {
      return ["P1 — ГОТОВОЕ ИЗМЕНЕНИЕ", `action=${action}; maturity=${maturity}; uncertainty=${uncertainty}; broad_result=${row.resultCount}`];
    }
    return ["P2 — ПРОВЕРИТЬ ПЕРЕД ВНЕДРЕНИЕМ", `action=${action}; maturity=${maturity}; uncertainty=${uncertainty}; broad_result=${row.resultCount}`];
  }
  if (["KEEP_EXISTING_STRUCTURE", "ROUTE_TO_EXISTING_PAGE_AS_SUBTASK"].includes(action)) {
    return ["P3 — СОХРАНИТЬ / МАРШРУТИЗИРОВАТЬ", `action=${action}; maturity=${maturity}; uncertainty=${uncertainty}; broad_result=${row.resultCount}`];
  }
  if (["NO_STANDALONE_PAGE", "OUTSIDE_SCOPE_NO_ACTION"].includes(action)) {
    return ["P4 — БЕЗ ОТДЕЛЬНОЙ СТРАНИЦЫ", `action=${action}; business_boundary=${row.canonical_business_scope_state}; broad_result=${row.resultCount}`];
  }
  return ["P2 — ПРОВЕРИТЬ ПЕРЕД ВНЕДРЕНИЕМ", `status=${state}; action=${action}; maturity=${maturity}; uncertainty=${uncertainty}; broad_result=${row.resultCount}`];
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
    text: "SEARCH_REQUIRED",
    format: { fill: "#FEE2E2", font: { color: "#991B1B", bold: true } },
  });
  sheet.getRange(`${statusColumn}2:${statusColumn}${last}`).conditionalFormats.add("containsText", {
    text: "ASSIGNED_HOLD",
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
  row.targetDisplay = targetDisplay(row);
}

const clusterRanks = assignRanks(activeRows, (row) => row.final_structural_unit_id);
const pageRanks = assignRanks(activeRows, (row) => row.targetDisplay);
for (const row of joined) {
  row.clusterRank = clusterRanks.get(row.id) ?? null;
  row.pageRank = pageRanks.get(row.id) ?? null;
  [row.priority, row.priorityBasis] = priorityFor(row);
  if (row.clusterRank) row.priorityBasis += `; rank_in_cluster=${row.clusterRank}`;
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
  "Wordstat result count", "Wordstat association count", "Тип частотности", "Правило агрегации", "Источники Wordstat",
  "Количество source occurrences", "Дата снимка", "ID структурной единицы", "Кластер", "Основной запрос кластера",
  "Пользовательская задача", "Интент", "Граница бизнеса", "Уверенность назначения", "URL до финальной сверки",
  "Финальная целевая страница", "Поддерживающие страницы", "Роль страницы", "Рекомендация", "Готовность решения",
  "Неопределённость", "Что нужно для пересмотра", "Ранг внутри кластера", "Ранг внутри страницы",
  "Операционный приоритет", "Основание приоритета", "Комментарий / граница вывода", "Provenance",
];

function phraseMatrix(rows) {
  return rows.map((row) => [
    row.id,
    row.phrase,
    row.final_semantic_state,
    row.active ? "ДА" : "НЕТ",
    "Москва",
    213,
    "DEVICE_ALL",
    row.resultCount,
    row.associationCount,
    `${METRIC_TYPE}__${row.frequencyRole}`,
    AGGREGATION_RULE,
    row.sourceIds,
    row.sourceOccurrences,
    row.snapshotDate,
    missingText(row, "final_structural_unit_id"),
    row.clusterName,
    row.representative?.phrase ?? missingText(row, "final_structural_unit_id"),
    missingText(row, "canonical_user_task"),
    missingText(row, "canonical_intent_type"),
    missingText(row, "canonical_business_scope_state"),
    row.canonical_final_confidence || row.semantic_confidence || "НЕ УКАЗАНО",
    row.step11_target_url || (row.active ? "НЕ БЫЛО СОХРАНЁННОГО URL" : "НЕ ПРИМЕНИМО — ВНЕ АКТИВНОГО ЯДРА"),
    row.targetDisplay,
    row.final_supporting_pages || (row.assigned ? "НЕТ КАНОНИЧЕСКОЙ ПОДДЕРЖИВАЮЩЕЙ СТРАНИЦЫ" : missingText(row, "final_supporting_pages")),
    missingText(row, "canonical_unit_page_role"),
    missingText(row, "canonical_structural_action"),
    missingText(row, "canonical_recommendation_maturity"),
    row.uncertainty_state || "НЕ УКАЗАНО",
    row.explicit_missing_needs || row.nextResolutionRoute || (row.active ? "ПЕРЕСМОТР НЕ ТРЕБУЕТСЯ ПО ТЕКУЩЕЙ AUTHORITY" : "НЕ ПРИМЕНИМО"),
    row.clusterRank,
    row.pageRank,
    row.priority,
    row.priorityBasis,
    [row.claim_boundary, row.routeReason, CLAIM_BOUNDARY].filter(Boolean).join(" | "),
    `Stage-5:${row.authority_lineage || "FINAL_SEMANTIC_MASTER"} | Step-08:${row.demandProvenance}`,
  ]);
}

const clusterHeaders = [
  "ID структурной единицы", "Кластер", "Основной запрос кластера", "Wordstat result у основного запроса",
  "Количество активных фраз", "Максимальный broad result", "Медиана broad result", "Сумма broad result (неаддитивно)",
  "Ведущие фразы", "Пользовательская задача", "Интент", "Граница бизнеса", "Финальная страница / группа",
  "Поддерживающие страницы", "Роль страницы", "Рекомендация", "Готовность решения", "Уверенность", "Неопределённость",
  "Что нужно для пересмотра", "Операционный приоритет", "Основание приоритета", "Граница метрики",
  "Source authority", "Higher-precedence authority",
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
      unit.user_task,
      unit.intent_type,
      unit.business_scope_state,
      unit.final_primary_page || `НЕТ ОТДЕЛЬНОЙ СТРАНИЦЫ — ${unit.structural_action}`,
      unit.final_supporting_pages || "НЕТ КАНОНИЧЕСКОЙ ПОДДЕРЖИВАЮЩЕЙ СТРАНИЦЫ",
      unit.unit_page_role,
      unit.structural_action,
      unit.recommendation_maturity,
      unit.final_confidence,
      unit.uncertainty_state,
      unit.explicit_missing_needs || "ПЕРЕСМОТР НЕ ТРЕБУЕТСЯ ПО ТЕКУЩЕЙ AUTHORITY",
      prioritySource.priority,
      `cluster action=${unit.structural_action}; maturity=${unit.recommendation_maturity}; uncertainty=${unit.uncertainty_state}; representative broad_result=${representative.resultCount}`,
      "SUM broad result — неаддитивный индикатор; фразы могут пересекаться по показываемым запросам",
      unit.source_authority,
      unit.higher_precedence_authority || "NONE",
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
  "Финальная страница / группа", "Тип строки", "Количество фраз", "Количество кластеров", "Максимальный broad result",
  "Медиана broad result", "Сумма broad result (неаддитивно)", "Ведущие фразы", "Кластеры", "Роли страницы",
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
    uniqueSorted(members.map((row) => row.canonical_unit_page_role)).join("; "),
    uniqueSorted(members.map((row) => row.canonical_structural_action)).join("; "),
    uniqueSorted(members.map((row) => row.canonical_recommendation_maturity)).join("; "),
    uniqueSorted(members.map((row) => row.uncertainty_state)).join("; "),
    bestPriority.priority,
    `лучший операционный класс в группе; broad_result_max=${Math.max(...members.map((row) => row.resultCount))}; не бизнес-приоритет`,
    target.startsWith("НЕТ ОТДЕЛЬНОЙ")
      ? "Пустой Stage-5 URL сохранён намеренно; причина указана в названии группы"
      : "Карта назначения из Stage-5; наличие нескольких кластеров на URL само по себе не доказывает каннибализацию",
  ];
});

const searchHeaders = [
  "ID фразы", "Поисковая фраза", "Wordstat result count", "Wordstat association count", "Регион", "Тип частотности",
  "Статус", "Неопределённость", "Search-stage disposition", "Следующий маршрут разрешения", "Причина маршрута",
  "ID структурной единицы", "Финальная страница", "Что нужно для пересмотра", "Операционный приоритет",
  "Граница вывода", "Источники Wordstat", "Provenance",
];
const searchMatrix = searchRequiredRows.sort((a, b) => b.resultCount - a.resultCount || a.phrase.localeCompare(b.phrase, "ru")).map((row) => [
  row.id,
  row.phrase,
  row.resultCount,
  row.associationCount,
  "Москва (213), DEVICE_ALL",
  `${METRIC_TYPE}__${row.frequencyRole}`,
  row.final_semantic_state,
  row.uncertainty_state,
  row.searchStageDisposition,
  row.nextResolutionRoute,
  row.routeReason,
  "НЕ НАЗНАЧЕНО — SEARCH_REQUIRED",
  "НЕ НАЗНАЧЕНО — SEARCH_REQUIRED",
  row.explicit_missing_needs || row.nextResolutionRoute,
  row.priority,
  [row.claim_boundary, CLAIM_BOUNDARY].filter(Boolean).join(" | "),
  row.sourceIds,
  `Stage-5:${row.authority_lineage || "FINAL_SEMANTIC_MASTER"} | Step-08:${row.demandProvenance}`,
]);

const dictionaryHeaders = ["Раздел", "Код / поле", "Пояснение", "Как использовать", "Источник / граница"];
const dictionaryRows = [
  ["Сводка", "Всего уникальных фраз", 2840, "Полный инвентарь находится на листе 01_Все_фразы", "Stage-5 final semantic master"],
  ["Сводка", "Активное ядро", 2332, "Основной рабочий список на листе 02_Активное_ядро", "ASSIGNED + ASSIGNED_HOLD + SEARCH_REQUIRED"],
  ["Сводка", "Назначено", 2313, "Имеет каноническую структурную единицу", "Stage-5"],
  ["Сводка", "SEARCH_REQUIRED", 19, "Отдельная очередь разрешения на листе 05_SEARCH_REQUIRED", "URL и кластер не выдумываются"],
  ["Сводка", "Канонические кластеры", 168, "Одна строка на листе 03_Кластеры", "Stage-5 unit authority"],
  ["Сводка", "Финальные URL", 60, "Плюс 3 управляемые группы без URL на листе 04_Страницы", "Stage-5 final_primary_page"],
  ["Статус фразы", "ASSIGNED", "Активная фраза назначена канонической структурной единице", "Можно фильтровать по кластеру, странице и действию", "Stage-5"],
  ["Статус фразы", "ASSIGNED_HOLD", "Назначение сохранено, но внедрение удерживается из-за неопределённости", "Не превращать в READY-действие", "Stage-5"],
  ["Статус фразы", "SEARCH_REQUIRED", "Активная фраза пока не имеет финального кластера/URL", "Сначала выполнить указанное evidence/review действие", "Stage-5"],
  ["Статус фразы", "REVIEW_DEFERRED", "Фраза сохранена, но не включена в рабочее ядро", "Не назначать страницу без нового основания", "Stage-5"],
  ["Статус фразы", "EXCLUDED_PRESERVED", "Исключённая фраза сохранена для аудита", "Не использовать как рабочую семантику", "Stage-5"],
  ["Флаг", "В рабочем ядре = ДА", "ASSIGNED, ASSIGNED_HOLD или SEARCH_REQUIRED", "Лист 02 содержит только эти строки", "Производное поле"],
  ["Частотность", METRIC_TYPE, "Broad Wordstat getTop без операторов", "Грубая сортировка и сравнение внутри принятого распределения", "Яндекс Вордстат; region=213; DEVICE_ALL; operators=NONE"],
  ["Частотность", "Wordstat result count", "Максимальный сохранённый result count для точного текста строки", "Основной числовой показатель спроса в книге", "Step-08; не exact-match"],
  ["Частотность", "Wordstat association count", "Максимальный сохранённый association count", "Вспомогательный provenance-сигнал; у активных строк есть собственный result count", "Step-08"],
  ["Частотность", AGGREGATION_RULE, "Повторные source occurrences сведены максимумом отдельно для result и association", "Не складывать повторы одной фразы", "Step-08 acceptance rule"],
  ["Частотность", "Сумма broad result (неаддитивно)", "Сумма строк внутри кластера/страницы", "Использовать только как относительный индикатор: запросы могут перекрываться", "Не является уникальным объёмом рынка"],
  ["Репрезентант", "Основной запрос кластера", "Фраза-член кластера, выбранная воспроизводимо по смысловой центральности, читаемости и broad result", "Название кластера повторяет эту русскую фразу; точечные overrides выбирают только другую реальную фразу того же кластера", "Материализатор; Stage-5 membership не меняется"],
  ["Ранг", "Ранг внутри кластера", "Убывание Wordstat result count; при равенстве — алфавит фразы и стабильный ID", "Это broad-ранг, не exact-demand rank", "Производное поле"],
  ["Ранг", "Ранг внутри страницы", "То же правило внутри финального URL или управляемой no-page группы", "SEARCH_REQUIRED не ранжируется по странице", "Производное поле"],
  ["Приоритет", "P0 — СНЯТЬ НЕОПРЕДЕЛЁННОСТЬ / SEARCH_REQUIRED", "Есть блокирующая неопределённость, HOLD или deferred evidence", "Сначала разрешить указанную причину", "Не означает высокий коммерческий потенциал"],
  ["Приоритет", "P1 — ГОТОВОЕ ИЗМЕНЕНИЕ", "Stage-5 требует расширения/блока и зрелость FINAL", "Можно планировать исполнение в пределах отдельной implementation authority", "Не заменяет specialist guide"],
  ["Приоритет", "P2 — ПРОВЕРИТЬ ПЕРЕД ВНЕДРЕНИЕМ", "Физическое изменение не имеет полностью финальной зрелости", "Нужна указанная проверка", "Производное поле"],
  ["Приоритет", "P3 — СОХРАНИТЬ / МАРШРУТИЗИРОВАТЬ", "Существующая структура сохраняется или фраза идёт подзадачей на текущую страницу", "Не создавать отдельную страницу только из-за фразы", "Stage-5 action"],
  ["Приоритет", "P4 — БЕЗ ОТДЕЛЬНОЙ СТРАНИЦЫ", "NO_STANDALONE_PAGE или OUTSIDE_SCOPE_NO_ACTION", "Не заполнять URL искусственно", "Stage-5 action"],
  ["Приоритет", "P5 — ВНЕ РАБОЧЕГО ЯДРА", "REVIEW_DEFERRED или EXCLUDED_PRESERVED", "Сохранять для аудита, не внедрять", "Stage-5 status"],
  ["No-page", "NO_STANDALONE_PAGE", "Канонически не нужна отдельная first-party страница", "Оставить URL пустым; работать только в разрешённой роли", "246 назначенных фраз"],
  ["No-page", "OUTSIDE_SCOPE_NO_ACTION", "Пользовательская задача вне подтверждённой границы бизнеса", "Не создавать посадочную страницу", "115 назначенных фраз"],
  ["No-page", "DEFER_PENDING_EVIDENCE", "Страница не назначается до получения указанного доказательства", "Соблюдать HOLD/reopen requirement", "32 назначенные фразы"],
  ["Интент", "COMMERCIAL / SERVICE", "Покупка/заказ продукта или профессиональной услуги", "Использовать вместе с user task и business boundary", "Stage-5 canonical intent"],
  ["Интент", "INFO / DIY_INFO", "Информационная или самостоятельная задача", "Не превращать автоматически в коммерческую страницу", "Stage-5 canonical intent"],
  ["Интент", "MIXED / AMBIGUOUS / NAVIGATIONAL", "Смешанный, неясный или навигационный сценарий", "Соблюдать точное кодовое значение и неопределённость", "Stage-5 canonical intent"],
  ["Граница бизнеса", "IN_SCOPE / IN_SCOPE_ADJACENT", "Подтверждённая или смежная задача сайта", "Проверять финальную роль страницы", "Stage-5"],
  ["Граница бизнеса", "NO_STANDALONE_*", "Тема может быть релевантна, но отдельная first-party страница не подтверждена", "Не создавать URL", "Stage-5"],
  ["Граница бизнеса", "OUTSIDE_SCOPE", "Вне подтверждённого предложения", "Без физического действия", "Stage-5"],
  ["Граница бизнеса", "DEFERRED_PENDING_*", "Не хватает business truth, evidence или owner policy", "Следовать reopen requirement", "Stage-5"],
  ["Рекомендация", "KEEP_EXISTING_STRUCTURE", "Сохранить существующую структуру", "Не создавать/сливать страницы без отдельного основания", "Stage-5"],
  ["Рекомендация", "ROUTE_TO_EXISTING_PAGE_AS_SUBTASK", "Маршрутизировать как подзадачу на существующую страницу", "Это аналитическое назначение, не новая CMS-страница", "Stage-5"],
  ["Рекомендация", "ADD_SECTION_OR_FAQ_TO_EXISTING / EXPAND_EXISTING_PAGE", "Расширить существующую страницу", "Исполнять по specialist guide и границам доказательств", "Stage-5"],
  ["Рекомендация", "NO_STANDALONE_PAGE / OUTSIDE_SCOPE_NO_ACTION / DEFER_PENDING_EVIDENCE", "Сохранить управляемое отсутствие отдельного URL", "Не заполнять пустой URL догадкой", "Stage-5"],
  ["Зрелость", "FINAL_*", "Решение финально в пределах указанного слоя доказательств", "Не расширять его за claim boundary", "Stage-5"],
  ["Зрелость", "PROVISIONAL_*", "Назначение принято, но код зрелости сохраняет требование проверки", "Проверить перед физическим внедрением", "Stage-5"],
  ["Зрелость", "DEFERRED_*", "Решение отложено до missing evidence", "Не внедрять", "Stage-5"],
  ["Неопределённость", "NONE", "Дополнительной неопределённости в canonical unit не зафиксировано", "Соблюдать общую границу метрики", "Stage-5"],
  ["Неопределённость", "HOLD", "Физическое действие удерживается", "Сначала выполнить reopen requirement", "Stage-5"],
  ["Неопределённость", "CURRENT_OVERLAP_RECHECK / LOW_CONFIDENCE", "Нужна точечная повторная проверка", "Не объявлять доказанную каннибализацию", "Stage-5"],
  ["Provenance", "Источники Wordstat", "S01–S18 — первый pass; P2-01–P2-04 — targeted expansion", "Фильтровать и трассировать происхождение count", "Step-08 source_ids"],
  ["Provenance", "Authority", "Stage-5 даёт финальную семантическую/page truth; Step-08 — demand/provenance", "Старый Step-19 не является финальной authority", "Материализатор не читает Step-19"],
  ["Методика", "Яндекс Вордстат", "Официальное описание метрики и операторов", "https://yandex.ru/support2/wordstat/ru/interface/new | https://yandex.ru/support2/wordstat/ru/content/operators", "Проверено 2026-09-07"],
  ["Методика", "Keyword clustering / mapping", "Разделение фразы, кластера и страницы", "https://www.semrush.com/blog/keyword-clustering/ | https://www.semrush.com/blog/keyword-mapping/", "Проверено 2026-09-07"],
  ["Методика", "Intent / cannibalization boundary", "Интент важнее объёма; пересечение не равно доказанному ущербу", "https://ahrefs.com/blog/keyword-intent/ | https://ahrefs.com/blog/keyword-cannibalization/", "Проверено 2026-09-07"],
];

const workbook = Workbook.create();
const allSheet = workbook.worksheets.add("01_Все_фразы");
const activeSheet = workbook.worksheets.add("02_Активное_ядро");
const clusterSheet = workbook.worksheets.add("03_Кластеры");
const pageSheet = workbook.worksheets.add("04_Страницы");
const searchSheet = workbook.worksheets.add("05_SEARCH_REQUIRED");
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
setColumnWidths(dictionarySheet, [24, 42, 68, 68, 68], dictionaryRows.length + 1);

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
  text: "SEARCH_REQUIRED",
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
    ["05_SEARCH_REQUIRED", "A1:R20"],
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
    "05_SEARCH_REQUIRED": searchMatrix.length,
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
