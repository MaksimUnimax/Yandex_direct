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
const OUTPUT_NAME = `SEMANTIC_CORE_AND_TARGET_SEO_STRUCTURE_OKNO_MSK_${DATE}.xlsx`;

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
    return Object.fromEntries(headers.map((h, i) => [h, cells[i] ?? ""]));
  });
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

function sha256(buffer) {
  return crypto.createHash("sha256").update(buffer).digest("hex");
}

function intValue(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n : 0;
}

const ROUTE_RU = {
  TARGET_PAGE_RESOLVED: "Целевая посадочная определена",
  NO_STANDALONE_ROUTE_TO_PARENT: "Отдельная страница не нужна — включить в названного владельца",
  RECHECK_NEEDS_EVIDENCE: "Нужна дополнительная проверка",
  NO_TARGET_OUTSIDE_SCOPE: "Вне целевой области проекта",
  UNRESOLVED_TASK_ROUTING: "Маршрут не определён — доказательств недостаточно",
};

const ACTION_RU = {
  KEEP_LOCK_TARGET_OWNER: "Сохранить и закрепить как целевую посадочную",
  KEEP_LOCK_AS_TARGET_OWNER: "Сохранить и закрепить как целевую посадочную",
  OPTIMIZE_STRENGTHEN: "Усилить существующую страницу",
  ROUTE_INTERNAL_LINK_CHANGE: "Изменить маршрут или внутреннюю связь",
  NO_STANDALONE_INCLUDE_IN_NAMED_OWNER: "Не создавать отдельную страницу; включить в названного владельца",
  NO_STANDALONE_OUTSIDE_SCOPE: "Не создавать отдельную страницу; оставить вне области",
  RECHECK_NEEDS_EVIDENCE: "Перепроверить — нужны доказательства",
};

const MATCH_RU = {
  EXISTING_MATCH: "Существующая страница подтверждена как целевая",
  EXISTING_NEEDS_OPTIMIZATION: "Существующая страница требует усиления",
  EXISTING_RELATIONSHIP_CHANGE: "Существующей странице нужна корректировка связи",
  UNRESOLVED: "Соответствие не определено",
  OWNER_EXISTING: "Точный текущий владелец найден",
  NO_SUITABLE_EXISTING_PAGE: "Подходящая точная текущая страница не найдена",
  CURRENT_PAGE_AVAILABLE_AS_SEPARATE_EVIDENCE: "Текущая страница найдена отдельной сверкой",
  CURRENT_OWNER_NOT_APPLICABLE_UNTIL_TASK_RESOLVED: "Текущий владелец не назначается до разрешения задачи",
  PAGE_OWNERSHIP_NOT_APPLICABLE_UNTIL_TASK_RESOLVED: "Текущий владелец не назначается до разрешения задачи",
  OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP: "Текущий владелец не назначается: задача вне области проекта",
  NO_CURRENT_PAGE_MATCH__EXPLICIT_SCOPE_BOUNDARY: "Текущая страница не назначена: явная граница области",
};

const YES_NO_RU = { YES: "Да", NO: "Нет", UNRESOLVED: "Не определено" };
const READY_RU = {
  READY_IMPLEMENTATION_SPEC: "Готово к внедрению",
  PENDING_BUSINESS_DETAIL: "Нужно бизнес-уточнение",
  PENDING_PLACEMENT_OR_CONTEXT: "Нужно точное место или контекст",
};
const HIERARCHY_RU = {
  SECTION_LANDING_OR_STANDALONE: "Посадочная раздела или самостоятельная страница",
  CHILD_OR_SUPPORT_PAGE: "Дочерняя или поддерживающая страница",
  TARGET_SEMANTIC_ROLE_TREE__NOT_CURRENT_NAVIGATION_TREE: "Целевая семантическая структура; не копия текущего меню",
};
const URL_STATE_RU = {
  LOGICAL_TARGET_ROLE_DEFINED__URL_NOT_USED_AS_DESIGN_INPUT: "Целевая роль определена независимо; URL назначен только после сверки",
  UNRESOLVED__NO_URL_FABRICATED: "URL не придуман: роль требует доказательств",
};

function textRu(value) {
  const source = String(value ?? "").trim();
  if (!source) return "";
  return ROUTE_RU[source] || ACTION_RU[source] || MATCH_RU[source] || YES_NO_RU[source] || READY_RU[source] || HIERARCHY_RU[source] || URL_STATE_RU[source] || source
    .replaceAll("SUPPORTED_WITHIN_ACCEPTED_SCOPE", "Подтверждено в принятой области")
    .replaceAll("NEEDS_EVIDENCE", "Нужны доказательства")
    .replaceAll("NO_CREATE_SPLIT_MERGE_REDIRECT_DELETE_AUTHORIZED", "Создание, разделение, объединение, редирект и удаление не разрешены")
    .replaceAll("TARGET_PAGE_REGISTRY_GROUPING__NOT_CURRENT_NAVIGATION_COPY", "Иерархия выведена из целевых ролей и не копирует текущую навигацию")
    .replaceAll("REUSE_CURRENT_PAGE", "Повторно использовать существующую страницу")
    .replaceAll("EXACT_SEARCH_TASK_BOUNDARY_REQUIRED", "Нужна точная проверка границы поисковой задачи")
    .replaceAll("EXISTING_MATCH:", "Текущая страница подтверждена:")
    .replaceAll("EXISTING_NEEDS_OPTIMIZATION:", "Текущую страницу нужно усилить:")
    .replaceAll("EXISTING_RELATIONSHIP_CHANGE:", "Для текущей страницы нужна корректировка связи:")
    .replaceAll("NONE", "Нет")
    .replaceAll("READY_IMPLEMENTATION_SPEC", "Готово к внедрению")
    .replaceAll("PENDING_BUSINESS_DETAIL", "Нужно бизнес-уточнение")
    .replaceAll("PENDING_PLACEMENT_OR_CONTEXT", "Нужно точное место или контекст");
}

function clientText(value) {
  return textRu(value)
    .replaceAll("См. целевую иерархию по ключу страницы.", "См. связи этой страницы на листе «Целевая структура».")
    .replaceAll("Source and target resolve; link is visible/contextual; target task matches note; no conflicting canonical owner.", "Страница-источник и целевая страница открываются; ссылка видима и соответствует контексту; переход ведёт на страницу с нужной задачей; конфликт владельцев не возникает.")
    .replaceAll("Source and target resolve; placement context is named; target task matches note; preservation holds.", "Страница-источник и целевая страница открываются; точное место ссылки названо; переход соответствует задаче целевой страницы; ограничения по сохранению соблюдены.")
    .replaceAll("Source and target resolve", "Страница-источник и целевая страница открываются")
    .replaceAll("link is visible/contextual", "ссылка видима и соответствует контексту")
    .replaceAll("target task matches note", "переход соответствует задаче целевой страницы")
    .replaceAll("no conflicting canonical owner", "конфликт владельцев не возникает")
    .replaceAll("company-specific", "подтверждённый компанией")
    .replaceAll("exact-match", "с точным вхождением")
    .replaceAll("READY-часть", "часть, готовая к публикации")
    .replaceAll("CTA", "кнопки обращения и формы заявки")
    .replaceAll("PENDING:", "До внедрения уточнить:");
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
  sheet.getRange("A3").format.rowHeight = 42;
}

function addDataSheet(workbook, config) {
  const { name, title, note, headers, rows, widths, tableName, freezeColumns = 1, bodyRowHeight = 30 } = config;
  const sheet = workbook.worksheets.add(name);
  const lastColumn = colLetter(headers.length - 1);
  styleTitle(sheet, title, note, lastColumn);
  sheet.getRangeByIndexes(4, 0, rows.length + 1, headers.length).values = [headers, ...rows];
  sheet.getRange(`A5:${lastColumn}5`).format = {
    fill: "#17365D",
    font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
    wrapText: true,
    horizontalAlignment: "center",
    verticalAlignment: "center",
  };
  sheet.getRange(`A5:${lastColumn}5`).format.rowHeight = 44;
  if (rows.length) {
    const body = sheet.getRangeByIndexes(5, 0, rows.length, headers.length);
    body.format = { font: { name: "Arial", size: 9, color: "#1F2937" }, verticalAlignment: "top", wrapText: true };
    body.format.borders = { insideHorizontal: { style: "thin", color: "#E5E7EB" } };
    body.format.rowHeight = bodyRowHeight;
  }
  widths.forEach((width, i) => {
    sheet.getRangeByIndexes(0, i, rows.length + 5, 1).format.columnWidth = width;
  });
  const table = sheet.tables.add(`A5:${lastColumn}${rows.length + 5}`, true, tableName);
  table.style = "TableStyleMedium2";
  table.showFilterButton = true;
  table.showBandedRows = true;
  sheet.freezePanes.freezeRows(5);
  if (freezeColumns) sheet.freezePanes.freezeColumns(freezeColumns);
  return sheet;
}

const args = parseArgs(process.argv.slice(2));
if (!args["input-dir"] || !args["output-dir"]) {
  throw new Error("Usage: build_target_first_client_workbook.mjs --input-dir <dir> --output-dir <dir> [--preview-dir <dir>] [--report <path>]");
}
const inputDir = path.resolve(args["input-dir"]);
const outputDir = path.resolve(args["output-dir"]);
const previewDir = args["preview-dir"] ? path.resolve(args["preview-dir"]) : null;
const reportPath = args.report ? path.resolve(args.report) : path.join(inputDir, `TARGET_FIRST_MARKET_GRADE_CLIENT_WORKBOOK_BUILD_REPORT_${DATE}.json`);
const readText = async (name) => fs.readFile(path.join(inputDir, name), "utf8");
const readTsv = async (name) => parseTsv(await readText(name));
const readGzipTsv = async (name) => parseTsv(gunzipSync(await fs.readFile(path.join(inputDir, name))).toString("utf8"));

const foundation = await readGzipTsv(`MK02_SEMANTIC_FOUNDATION_${DATE}.tsv.gz`);
const phraseMap = await readGzipTsv(`TARGET_FIRST_PHRASE_LANDING_MAP_MARKET_GRADE_${DATE}.tsv.gz`);
const clusters = await readTsv(`TARGET_FIRST_CLUSTER_LANDING_MAP_${DATE}.tsv`);
const registry = await readTsv(`TARGET_PAGE_REGISTRY_${DATE}.tsv`);
const hierarchy = await readTsv(`TARGET_ARCHITECTURE_HIERARCHY_${DATE}.tsv`);
const reconciliation = await readTsv(`CURRENT_TARGET_RECONCILIATION_${DATE}.tsv`);
const specs = await readTsv(`TARGET_PAGE_SPEC_REGISTER_MARKET_GRADE_${DATE}.tsv`);
const delta = await readTsv(`CURRENT_TARGET_CHANGE_DELTA_${DATE}.tsv`);
const relations = await readTsv(`MK02_PAGE_RELATIONSHIPS_${DATE}.tsv`);

const pageNameByKey = new Map(registry.map((r) => [r.target_page_key, r.target_page_name_ru]));
const clusterNameByKey = new Map(clusters.map((r) => [r.cluster_task_key, r.cluster_task_name_ru]));
const pageNameByUrl = new Map();
for (const row of reconciliation) {
  if (row.current_url_match) pageNameByUrl.set(row.current_url_match, row.target_page_name_ru);
  if (row.accepted_target_url_after_reconciliation) pageNameByUrl.set(row.accepted_target_url_after_reconciliation, row.target_page_name_ru);
}

function namesFromKeys(value, mapping, emptyValue = "Нет") {
  const keys = String(value || "").split(";").map((key) => key.trim()).filter(Boolean);
  if (!keys.length) return emptyValue;
  return keys.map((key) => mapping.get(key) || (key === "NO_TARGET_OUTSIDE_SCOPE" ? "Вне целевой области проекта" : "Неназванная роль — требуется проверка")).join("; ");
}

function pageNameFromKey(key, emptyValue = "Корень раздела") {
  if (!key) return emptyValue;
  return pageNameByKey.get(key) || (key === "NO_TARGET_OUTSIDE_SCOPE" ? "Вне целевой области проекта" : "Неназванная роль — требуется проверка");
}

function humanizeRelation(value) {
  let result = clientText(value).replaceAll("NO_TARGET_OUTSIDE_SCOPE", "«Вне целевой области проекта»");
  for (const [key, name] of [...pageNameByKey.entries()].sort((a, b) => b[0].length - a[0].length)) {
    result = result.replaceAll(key, `«${name}»`);
  }
  return result;
}

const working = foundation.filter((r) => r.in_working_core === "Да");
const review = foundation.filter((r) => ["Проверка отложена", "Нужна проверка в обычной выдаче Яндекса"].includes(r.product_status));
const excluded = foundation.filter((r) => r.product_status.startsWith("Исключено"));
if (foundation.length !== 2840 || working.length !== 2185 || review.length !== 187 || excluded.length !== 468) throw new Error("semantic accounting invariant failed");
if (phraseMap.length !== working.length) throw new Error("phrase target map row count failed");
if (registry.length !== specs.length || registry.length !== reconciliation.length || registry.length !== hierarchy.length) throw new Error("target page register alignment failed");
if (phraseMap.some((r) => String(r.wordstat_popular_count ?? "").trim() === "")) throw new Error("market-grade phrase map is missing individual Wordstat");
if (specs.some((r) => !r.primary_page_job_ru || !r.primary_query_wordstat || !r.secondary_queries_with_wordstat || !r.recommended_h1_or_blocker || !r.analytical_seo_priority || !r.analytical_seo_priority_basis)) throw new Error("market-grade page-spec fields are incomplete");

const phraseTargetByKey = new Map(phraseMap.map((r) => [r.phrase_key, r]));
const allRows = [...foundation].sort((a, b) => a.phrase.localeCompare(b.phrase, "ru")).map((r) => {
  const m = phraseTargetByKey.get(r.phrase_id);
  return [
    r.phrase, r.product_status, r.in_working_core, r.group_name, r.user_task, r.intent,
    m?.cluster_task_name_ru || "", m?.target_landing_page_name_ru || "", m ? textRu(m.target_route_state) : "",
    m?.target_url_after_reconciliation || "", m ? textRu(m.target_action) : "", m ? textRu(m.real_site_change_required) : "",
    intValue(r.wordstat_popular_count), clientText(r.decision_basis), r.uncertainty,
  ];
});

const groupMap = new Map();
for (const r of working) {
  if (!groupMap.has(r.group_id)) groupMap.set(r.group_id, []);
  groupMap.get(r.group_id).push(r);
}
const groupRows = [...groupMap.entries()].map(([key, rows]) => {
  const sorted = [...rows].sort((a, b) => intValue(b.wordstat_popular_count) - intValue(a.wordstat_popular_count));
  const mapped = rows.map((r) => phraseTargetByKey.get(r.phrase_id)).filter(Boolean);
  return [rows[0].group_name, rows.length, rows[0].user_task, rows[0].intent, rows[0].topic_role,
    new Set(mapped.map((r) => r.cluster_task_key)).size, new Set(mapped.map((r) => r.target_landing_page_key).filter(Boolean)).size,
    sorted.slice(0, 4).map((r) => r.phrase).join("; ")];
}).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "ru"));

const phraseRows = [...phraseMap].sort((a, b) => a.cluster_task_name_ru.localeCompare(b.cluster_task_name_ru, "ru") || a.phrase.localeCompare(b.phrase, "ru")).map((r) => [
  r.phrase, intValue(r.wordstat_popular_count), r.cluster_task_name_ru, r.intent_user_task_ru,
  r.target_landing_page_name_ru || "Не назначена", textRu(r.target_route_state),
  r.target_url_after_reconciliation, r.current_exact_page_match_separate, r.current_family_page_match_separate,
  textRu(r.current_match_state_separate), textRu(r.target_action), textRu(r.real_site_change_required), clientText(r.uncertainty_reason),
]);

const clusterRows = [...clusters].sort((a, b) => a.intended_target_page_name_ru.localeCompare(b.intended_target_page_name_ru, "ru") || a.cluster_task_name_ru.localeCompare(b.cluster_task_name_ru, "ru")).map((r) => [
  r.cluster_task_name_ru, r.primary_representative_query, intValue(r.member_phrase_count), r.intent_user_task_ru,
  r.intended_target_page_name_ru || "Не назначена", clientText(r.page_purpose), r.page_type,
  r.intended_parent_or_section, humanizeRelation(r.supporting_or_child_relation), textRu(r.target_route_state), r.target_url_after_reconciliation,
  textRu(r.current_match_state_separate), r.current_page_match_separate, textRu(r.target_action), textRu(r.real_site_change_required), clientText(r.uncertainty_evidence_boundary),
]);

const hierarchyRows = [...hierarchy].sort((a, b) => a.section_name_ru.localeCompare(b.section_name_ru, "ru") || a.subsection_or_parent_name_ru.localeCompare(b.subsection_or_parent_name_ru, "ru") || a.target_page_name_ru.localeCompare(b.target_page_name_ru, "ru")).map((r) => [
  r.section_name_ru, r.subsection_or_parent_name_ru, r.target_page_name_ru,
  textRu(r.hierarchy_level), r.page_type, intValue(r.member_phrase_count), namesFromKeys(r.child_supporting_target_page_keys, pageNameByKey), textRu(r.hierarchy_basis),
]);

const reconByKey = new Map(reconciliation.map((r) => [r.target_page_key, r]));
const registryByKey = new Map(registry.map((r) => [r.target_page_key, r]));
const registryRows = [...specs].sort((a, b) => a.parent_section.localeCompare(b.parent_section, "ru") || a.target_page_name_ru.localeCompare(b.target_page_name_ru, "ru")).map((r) => {
  const rec = reconByKey.get(r.target_page_key);
  const reg = registryByKey.get(r.target_page_key);
  return [
    r.target_page_name_ru,
    r.target_url_or_route.startsWith("TARGET_ROLE::") ? "Маршрут не назначен до проверки" : r.target_url_or_route,
    r.page_type,
    r.parent_section,
    pageNameFromKey(r.parent_target_page_key),
    r.primary_representative_query,
    intValue(r.primary_query_wordstat),
    r.secondary_queries_with_wordstat,
    intValue(r.total_routed_phrase_count),
    r.recommended_h1_or_blocker,
    r.recommended_title_direction_or_blocker,
    r.analytical_seo_priority,
    r.analytical_seo_priority_basis,
    rec ? textRu(rec.current_match_state) : "",
    rec ? textRu(rec.target_action) : "",
    rec ? textRu(rec.real_site_change_required) : "",
    reg ? namesFromKeys(reg.child_supporting_target_page_keys, pageNameByKey) : "Нет",
  ];
});

const specRows = [...specs].sort((a, b) => a.parent_section.localeCompare(b.parent_section, "ru") || a.target_page_name_ru.localeCompare(b.target_page_name_ru, "ru")).map((r) => [
  r.target_page_name_ru, r.target_url_or_route.startsWith("TARGET_ROLE::") ? "Маршрут не назначен до проверки" : r.target_url_or_route, r.page_type, r.parent_section, pageNameFromKey(r.parent_target_page_key),
  r.primary_page_job_ru, r.primary_representative_query, intValue(r.primary_query_wordstat), r.secondary_queries_with_wordstat, intValue(r.total_routed_phrase_count),
  r.own_coverage_clean, r.embedded_no_standalone_topics, r.support_mention_link_topics, r.elsewhere_named_pages, r.boundary_overlap_explanations,
  r.recommended_h1_or_blocker, r.recommended_title_direction_or_blocker, r.analytical_seo_priority, r.analytical_seo_priority_basis,
  clientText(r.current_url_match_current_state), textRu(r.target_action), textRu(r.real_site_change_required), clientText(r.implementation_detail_if_change_is_real),
  clientText(r.acceptance_target_end_state), clientText(r.uncertainty_exact_clarification),
]);

const deltaRows = [...delta].sort((a, b) => (a.readiness_state === "READY_IMPLEMENTATION_SPEC" ? -1 : 1) || a.target_page_name_ru.localeCompare(b.target_page_name_ru, "ru")).map((r) => [
  r.target_page_name_ru, r.current_object, textRu(r.target_action), textRu(r.readiness_state), textRu(r.real_site_change_required),
  clientText(r.why_change_is_needed), clientText(r.exact_change), clientText(r.exact_location_or_context), clientText(r.target_end_state), clientText(r.acceptance_check),
  clientText(r.preservation_do_not_break), clientText(r.one_concrete_clarification),
]);

const checkRows = clusters.filter((r) => ["RECHECK_NEEDS_EVIDENCE", "UNRESOLVED_TASK_ROUTING", "NO_TARGET_OUTSIDE_SCOPE"].includes(r.target_route_state)).map((r) => [
  "Кластер / задача", r.cluster_task_name_ru, r.primary_representative_query, textRu(r.target_route_state),
  r.intended_target_page_name_ru || "Не назначена", clientText(r.uncertainty_evidence_boundary),
  r.target_route_state === "NO_TARGET_OUTSIDE_SCOPE" ? "Не создавать страницу в рамках этого исследования" : "Вернуться к решению после получения названного доказательства",
]);
for (const r of delta.filter((x) => x.readiness_state !== "READY_IMPLEMENTATION_SPEC")) {
  checkRows.push(["Изменение сайта", r.target_page_name_ru, r.current_object, textRu(r.readiness_state), r.target_page_name_ru, clientText(r.one_concrete_clarification), "Не передавать как готовое внедрение до уточнения"]);
}

const relationRows = [...registry].filter((r) => r.parent_target_page_key || r.child_supporting_target_page_keys).map((r) => [
  r.target_page_name_ru, pageNameFromKey(r.parent_target_page_key, r.parent_section_name_ru), namesFromKeys(r.child_supporting_target_page_keys, pageNameByKey),
  "Целевая структура", "Не относится к текущей ссылке", "Целевая семантическая связь; не копия текущего меню",
]);
for (const r of relations) {
  relationRows.push([`${pageNameByUrl.get(r.source_url) || "Текущая страница"}: ${r.source_url}`, `${pageNameByUrl.get(r.target_url) || "Целевая страница"}: ${r.target_url}`, "Нет", "Проверенная текущая ссылка", r.current_link_present === "YES" ? "Ссылка присутствует" : "Ссылка отсутствует", r.current_link_present === "YES" ? "Сохранить полезный переход" : "Добавлять только после уточнения точного места"]);
}

const currentRows = [...reconciliation].sort((a, b) => a.target_page_name_ru.localeCompare(b.target_page_name_ru, "ru")).map((r) => [
  r.target_page_name_ru, clientText(r.independent_target_role), textRu(r.current_match_state), r.current_url_match,
  r.accepted_target_url_after_reconciliation, textRu(r.target_action), textRu(r.real_site_change_required), textRu(r.current_content_reuse),
  textRu(r.business_fit_state), textRu(r.structural_safety_state), clientText(r.uncertainty_evidence_boundary),
]);

const workbook = Workbook.create();
const guide = workbook.worksheets.add("Начните здесь");
styleTitle(guide, "OKNO_MSK — семантическое ядро и целевая SEO-архитектура", "Что показывает: полный результат для Москвы и Яндекса — от фразы и её индивидуального Вордстата до целевой страницы, структуры и ТЗ. Значения Вордстата по фразам не суммируются в прогноз спроса страницы. SEO-приоритет — аналитическая важность, а не календарный порядок работ.", "H");
guide.getRange("A5:H5").values = [["Показатель", "Значение", "", "Что означает", "", "", "", ""]];
guide.getRange("A5:H5").format = { fill: "#17365D", font: { name: "Arial", bold: true, color: "#FFFFFF" } };
const actionCounts = Object.fromEntries([...new Set(reconciliation.map((r) => r.target_action))].map((key) => [key, reconciliation.filter((r) => r.target_action === key).length]));
const summary = [
  ["Семантическая вселенная", foundation.length, "Все принятые фразы сохранены: рабочие, спорные и исключённые."],
  ["Рабочие фразы", working.length, "Каждая имеет целевой маршрут либо явное состояние «не нужна отдельная страница» / «нужна проверка»."],
  ["Кластеры / задачи", clusters.length, "Это задачи посадочных страниц; кластер не равен автоматической новой странице."],
  ["Целевые роли страниц", registry.length, "Полный реестр ролей, спроектированный до сверки с текущим сайтом."],
  ["Закрепить существующим владельцем", actionCounts.KEEP_LOCK_AS_TARGET_OWNER || 0, "Существующие страницы подтверждены как правильные целевые посадочные и не исключены из результата."],
  ["Усилить существующую страницу", actionCounts.OPTIMIZE_STRENGTHEN || 0, "Целевая роль совпала с текущей страницей, но требуется содержательное усиление."],
  ["Изменить маршрут или связь", actionCounts.ROUTE_INTERNAL_LINK_CHANGE || 0, "Нужно изменить маршрут или внутреннюю связь без создания новой роли."],
  ["Требует перепроверки", actionCounts.RECHECK_NEEDS_EVIDENCE || 0, "Решение сохранено открытым; URL не придуман."],
  ["Задания на физические изменения", delta.length, "Подмножество полного реестра ТЗ по страницам, а не весь продукт."],
];
guide.getRangeByIndexes(5, 0, summary.length, 8).values = summary.map(([a, b, c]) => [a, b, "", c, "", "", "", ""]);
for (let row = 6; row < 6 + summary.length; row += 1) {
  guide.mergeCells(`B${row}:C${row}`);
  guide.mergeCells(`D${row}:H${row}`);
}
guide.getRange(`A6:H${5 + summary.length}`).format = { font: { name: "Arial", size: 10 }, wrapText: true, verticalAlignment: "center" };
guide.getRange(`A6:H${5 + summary.length}`).format.rowHeight = 34;
guide.getRange(`B6:C${5 + summary.length}`).format = { font: { name: "Arial", size: 12, bold: true, color: "#0F6B78" }, horizontalAlignment: "center" };
const start = 17;
guide.mergeCells(`A${start}:H${start}`);
guide.getRange(`A${start}`).values = [["Порядок проверки результата"]];
guide.getRange(`A${start}`).format = { fill: "#0F6B78", font: { name: "Arial", bold: true, color: "#FFFFFF" } };
const guideSteps = [
  ["1", "Найдите фразу", "Лист «Рассадка запросов» показывает индивидуальный Вордстат, кластер, целевую страницу, сверку с текущим сайтом и действие."],
  ["2", "Проверьте кластер", "Лист «Посадочные страницы» объясняет, почему задача направлена на эту роль и нужен ли отдельный URL."],
  ["3", "Посмотрите структуру", "Лист «Целевая структура» читается без открытия текущего сайта."],
  ["4", "Откройте ТЗ страницы", "Видны главная задача, основной и дополнительные запросы с Вордстатом, границы покрытия, H1, Title-решение и аналитический приоритет."],
  ["5", "Передавайте изменения", "Лист «Изменения сайта» — только подмножество реальных заданий на физические изменения."],
];
guide.getRangeByIndexes(start, 0, guideSteps.length, 8).values = guideSteps.map((r) => [r[0], r[1], r[2], "", "", "", "", ""]);
for (let row = start + 1; row <= start + guideSteps.length; row += 1) guide.mergeCells(`C${row}:H${row}`);
guide.getRange(`A${start + 1}:H${start + guideSteps.length}`).format = { font: { name: "Arial", size: 10 }, wrapText: true, verticalAlignment: "top" };
guide.getRange(`A${start + 1}:H${start + guideSteps.length}`).format.rowHeight = 36;
[23, 20, 16, 24, 18, 18, 18, 18].forEach((w, i) => guide.getRangeByIndexes(0, i, start + guideSteps.length, 1).format.columnWidth = w);
guide.freezePanes.freezeRows(5);

addDataSheet(workbook, { name: "Все запросы", title: "Все сохранённые запросы", note: "Что показывает: 2 840 фраз с итоговым статусом и целевым маршрутом для рабочих строк. Зачем: доказать полное сохранение данных. Как пользоваться: фильтруйте по статусу, кластеру, посадочной и действию.", headers: ["Поисковая фраза", "Статус", "В рабочем ядре", "Смысловая группа", "Задача пользователя", "Интент", "Кластер / задача посадочной", "Целевая посадочная", "Состояние маршрута", "Целевой URL после сверки", "Целевое действие", "Нужно менять сайт", "Вордстат", "Основание", "Неопределённость"], rows: allRows, widths: [42, 32, 15, 32, 48, 28, 44, 40, 42, 54, 46, 20, 14, 64, 24], tableName: "DataQueries", freezeColumns: 1 });
addDataSheet(workbook, { name: "Кластеры и задачи", title: "Смысловые группы спроса", note: "Что показывает: 54 принятые смысловые группы рабочего ядра. Зачем: увидеть основные направления спроса до дробления на задачи посадочных страниц. Как пользоваться: сравнивайте объём, задачу, интент и число целевых ролей.", headers: ["Группа", "Рабочих фраз", "Задача пользователя", "Интент", "Роль темы", "Задач посадочных страниц", "Целевых ролей", "Примеры запросов"], rows: groupRows, widths: [34, 16, 54, 28, 26, 20, 18, 82], tableName: "DataGroups", freezeColumns: 1 });
addDataSheet(workbook, { name: "Рассадка запросов", title: "Рабочая фраза → спрос → кластер → целевая посадочная", note: "Что показывает: целевой маршрут каждой из 2 185 рабочих фраз и её индивидуальный сохранённый показатель Вордстата. Значения разных фраз не суммируются в спрос страницы. Как пользоваться: найдите фразу или отсортируйте Вордстат, затем проследите кластер, посадочную, URL, сверку и действие.", headers: ["Фраза", "Вордстат", "Кластер / задача", "Интент / задача пользователя", "Целевая посадочная", "Состояние маршрута", "Целевой URL после сверки", "Текущая точная страница", "Текущая семейная страница", "Состояние сверки", "Действие", "Нужно менять сайт", "Неопределённость"], rows: phraseRows, widths: [42, 14, 46, 58, 40, 46, 54, 54, 54, 38, 48, 20, 54], tableName: "DataPhraseMap", freezeColumns: 2 });
addDataSheet(workbook, { name: "Посадочные страницы", title: "Кластер / задача → целевая посадочная", note: "Что показывает: 161 задача посадочных страниц и решение о странице. Зачем: отделить проектирование целевой роли от удобства текущих URL. Как пользоваться: начинайте с задачи пользователя, затем проверяйте назначение, родителя, состояние целевого маршрута и только потом сверку с текущим сайтом.", headers: ["Кластер / задача", "Представительный запрос", "Фраз", "Интент / задача пользователя", "Посадочная", "Назначение страницы", "Тип", "Родитель / раздел", "Поддержка / дочерняя связь", "Состояние целевого маршрута", "URL после сверки", "Сверка с текущим сайтом", "Текущая страница", "Действие", "Нужно менять сайт", "Граница доказательств"], rows: clusterRows, widths: [46, 42, 12, 58, 40, 64, 30, 42, 58, 46, 54, 38, 54, 48, 20, 64], tableName: "DataLandingMap", freezeColumns: 1 });
addDataSheet(workbook, { name: "Целевая структура", title: "Целевая SEO-иерархия", note: "Что показывает: раздел → родитель / подраздел → посадочная или поддерживающая страница. Зачем: понять будущую поисковую структуру без открытия текущего сайта. Как пользоваться: фильтруйте по разделу и уровню; это семантическая архитектура, а не копия текущего меню.", headers: ["Раздел", "Родитель / подраздел", "Целевая страница", "Уровень", "Тип страницы", "Фраз", "Дочерние / поддерживающие страницы", "Основание иерархии"], rows: hierarchyRows, widths: [32, 42, 42, 38, 30, 12, 82, 72], tableName: "DataHierarchy", freezeColumns: 2 });
addDataSheet(workbook, { name: "Реестр страниц", title: "Полный реестр 60 целевых ролей", note: "Что показывает: все целевые страницы, включая 48 подтверждённых без изменения, с главным запросом, индивидуальным спросом, полезными дополнительными запросами, H1, Title-решением и аналитическим SEO-приоритетом. «Всего фраз» — размер маршрута, не сумма Вордстата.", headers: ["Целевая страница", "URL / маршрут", "Тип", "Раздел", "Родитель", "Основной запрос", "Вордстат основного", "Дополнительные запросы + Вордстат", "Всего распределённых фраз", "Рекомендуемый H1 / блокер", "Title: направление / статус", "SEO-приоритет", "Основание приоритета", "Сверка с текущим сайтом", "Действие", "Нужно менять сайт", "Дочерние страницы"], rows: registryRows, widths: [42, 54, 30, 34, 42, 42, 17, 92, 20, 50, 78, 18, 68, 42, 48, 20, 78], tableName: "DataPageRegistry", freezeColumns: 2, bodyRowHeight: 62 });
addDataSheet(workbook, { name: "ТЗ по страницам", title: "Полное постраничное ТЗ", note: "Что показывает: 60 спецификаций с одной главной задачей страницы и раздельными зонами ответственности. Как пользоваться: фильтруйте страницу/действие; затем читайте запросы с индивидуальным спросом, собственное покрытие, встроенные темы, поддержку, соседних владельцев, H1, Title и критерий приёмки.", headers: ["Целевая страница", "URL / маршрут", "Тип", "Раздел", "Родитель", "Главная задача страницы", "Основной запрос", "Вордстат основного", "Дополнительные запросы + Вордстат", "Всего распределённых фраз", "Собственное покрытие", "Встроить без отдельного URL", "Только упомянуть / связать", "Отдать другой названной странице", "Пояснение границы", "Рекомендуемый H1 / блокер", "Title: направление / статус", "SEO-приоритет", "Основание приоритета", "Текущее состояние", "Действие", "Нужно менять сайт", "Деталь внедрения", "Целевой результат / приёмка", "Что уточнить / блокер"], rows: specRows, widths: [42, 54, 30, 34, 42, 68, 42, 17, 92, 20, 84, 78, 78, 92, 92, 50, 78, 18, 68, 68, 48, 20, 82, 86, 76], tableName: "DataPageSpecs", freezeColumns: 2, bodyRowHeight: 92 });
addDataSheet(workbook, { name: "Изменения сайта", title: "Текущий сайт → целевая модель: изменения", note: "Что показывает: только реальные или потенциальные физические изменения сайта. Зачем: не смешивать полное постраничное ТЗ с заданиями на изменения. Как пользоваться: внедряйте только «Готово к внедрению»; остальные строки сначала уточните.", headers: ["Страница", "Текущий объект", "Действие", "Готовность", "Нужно менять сайт", "Почему", "Что сделать", "Где", "Целевой результат", "Как принять", "Что сохранить", "Что уточнить"], rows: deltaRows, widths: [42, 58, 42, 34, 20, 66, 78, 68, 74, 76, 72, 72], tableName: "DataSiteChanges", freezeColumns: 1, bodyRowHeight: 64 });
addDataSheet(workbook, { name: "Проверить и отложено", title: "Что требует проверки или уточнения", note: "Что показывает: неразрешённые, требующие перепроверки, внешние для проекта задачи и неготовые задания на изменения. Зачем: не придумывать URL, страницу или место внедрения. Как пользоваться: выполните ровно указанное уточнение и только затем меняйте состояние решения.", headers: ["Тип объекта", "Объект", "Запрос / текущий объект", "Состояние", "Предполагаемый владелец", "Что уточнить", "Что делать сейчас"], rows: checkRows, widths: [24, 48, 56, 42, 48, 78, 72], tableName: "DataChecks", freezeColumns: 2, bodyRowHeight: 56 });
addDataSheet(workbook, { name: "Связи страниц", title: "Целевые и проверенные связи страниц", note: "Что показывает: родительские, дочерние и поддерживающие отношения, а также отдельно проверенные текущие ссылки. Зачем: видеть архитектурные зависимости. Как пользоваться: целевые отношения не трактуйте как буквальную копию меню; текущие ссылки меняйте только при готовом контексте.", headers: ["Страница / источник", "Родитель или цель", "Дочерние / поддерживающие страницы", "Тип связи", "Текущее состояние", "Интерпретация"], rows: relationRows, widths: [72, 72, 82, 42, 34, 74], tableName: "DataRelations", freezeColumns: 1, bodyRowHeight: 50 });
addDataSheet(workbook, { name: "Текущий сайт", title: "Сверка целевых ролей с текущим сайтом", note: "Что показывает: сверку с текущим сайтом только после независимого проектирования целевой модели. Зачем: существующий URL не должен определять роль заранее. Как пользоваться: читайте слева направо — независимая роль, совпадение, принятый URL, действие и граница безопасности.", headers: ["Целевая страница", "Независимая целевая роль", "Сверка с текущим сайтом", "Текущий URL", "Принятый целевой URL", "Действие", "Нужно менять сайт", "Повторное использование контента", "Соответствие бизнесу", "Структурная безопасность", "Граница доказательств"], rows: currentRows, widths: [42, 70, 42, 54, 54, 48, 20, 66, 34, 60, 68], tableName: "DataCurrentSite", freezeColumns: 1 });

const qaRows = [
  ["Случайная рабочая фраза", "Найти строку на листе «Рассадка запросов»", "На одной строке видны фраза, индивидуальный Вордстат, кластер, посадочная, URL, сверка и действие"],
  ["Случайный существенный кластер", "Найти на листе «Посадочные страницы»", "Понятны задача пользователя, назначение страницы, родитель, целевой маршрут и причина"],
  ["Целевая структура", "Прочитать лист «Целевая структура» без сайта", "Понятна иерархия раздел → родитель → страница → поддержка"],
  ["Запросы страницы", "Открыть «Реестр страниц» или «ТЗ по страницам»", "Видны основной и полезные дополнительные запросы с индивидуальным Вордстатом"],
  ["Границы страницы", "Открыть «ТЗ по страницам»", "Раздельно видны собственное покрытие, встроенные темы, поддержка и названные соседние владельцы"],
  ["H1 / Title", "Открыть «ТЗ по страницам»", "Есть H1 или блокер; для усиления есть направление Title, а для сохранения не навязана перепись метаданных"],
  ["SEO-приоритет", "Сверить приоритет и его основание", "Понятно, что это аналитическая важность, а не срок, усилие, бизнес-ценность или прогноз"],
  ["Подтверждённая страница без изменения", "Отфильтровать действие «Сохранить и закрепить…»", "Все 48 ролей видны с закреплённой семантикой и целевым состоянием"],
  ["Готовое изменение", "Отфильтровать «Готово к внедрению»", "Есть что/где/зачем/что сохранить/как принять"],
  ["Граница данных", "Сверить 2 840 = 2 185 + 187 + 468", "Новых обращений к внешним сервисам нет; данные Google, Алисы, нейропоиска и расширение по конкурентам не включены"],
];
addDataSheet(workbook, { name: "Как проверить", title: "Приёмка клиентского результата", note: "Что показывает: независимые проверки получателя по основным сценариям. Зачем: доказать пригодность пакета без внутренних журналов. Как пользоваться: выполните проверки на случайных строках и сопоставьте с двумя PDF.", headers: ["Проверка", "Действие", "Ожидаемый результат"], rows: qaRows, widths: [38, 64, 96], tableName: "DataAcceptance", freezeColumns: 1, bodyRowHeight: 56 });

workbook.recalculate();
const sheetNames = ["Начните здесь", "Все запросы", "Кластеры и задачи", "Рассадка запросов", "Посадочные страницы", "Целевая структура", "Реестр страниц", "ТЗ по страницам", "Изменения сайта", "Проверить и отложено", "Связи страниц", "Текущий сайт", "Как проверить"];
const inspectRanges = {
  "Начните здесь": "A1:H23", "Все запросы": "A1:O18", "Кластеры и задачи": "A1:H20",
  "Рассадка запросов": "A1:M18", "Посадочные страницы": "A1:P18", "Целевая структура": "A1:H18",
  "Реестр страниц": "A1:Q15", "ТЗ по страницам": "A1:Y11", "Изменения сайта": "A1:L18",
  "Проверить и отложено": "A1:G18", "Связи страниц": "A1:F18", "Текущий сайт": "A1:K18", "Как проверить": "A1:C12",
};
const inspections = {};
for (const [name, range] of Object.entries(inspectRanges)) {
  const result = await workbook.inspect({ kind: "table", range: `${name}!${range}`, include: "values,formulas", tableMaxRows: 20, tableMaxCols: 20, maxChars: 18000 });
  inspections[name] = result.ndjson;
}
const formulaErrorsBefore = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 300 }, summary: "target-first workbook formula error scan" });

await fs.mkdir(outputDir, { recursive: true });
const xlsxPath = path.join(outputDir, OUTPUT_NAME);
const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(xlsxPath);
if (previewDir) {
  await fs.mkdir(previewDir, { recursive: true });
  for (const [name, range] of Object.entries(inspectRanges)) {
    const renderRange = name === "Все запросы" || name === "Рассадка запросов" ? range.replace(/18$/, "14") : range;
    const rendered = await workbook.render({ sheetName: name, range: renderRange, scale: 1, format: "png" });
    await fs.writeFile(path.join(previewDir, `${sheetNames.indexOf(name) + 1}_${name.replace(/\s+/g, "_")}.png`), new Uint8Array(await rendered.arrayBuffer()));
  }
}

const imported = await SpreadsheetFile.importXlsx(await FileBlob.load(xlsxPath));
const importedSheets = await imported.inspect({ kind: "sheet", include: "id,name", maxChars: 12000 });
const formulaErrorsAfter = await imported.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!", options: { useRegex: true, maxResults: 300 }, summary: "saved target-first workbook formula error scan" });
const outputBuffer = await fs.readFile(xlsxPath);
const report = {
  schema: "MK02_TARGET_FIRST_MARKET_GRADE_CLIENT_WORKBOOK_V2",
  date: DATE,
  status: "PASS",
  artifact_tool_used: true,
  source_authorities: [`TARGET_FIRST_PHRASE_LANDING_MAP_MARKET_GRADE_${DATE}.tsv.gz`, `TARGET_PAGE_SPEC_REGISTER_MARKET_GRADE_${DATE}.tsv`],
  source_counts: { semantic_universe: foundation.length, working: working.length, review: review.length, excluded: excluded.length, semantic_groups: groupRows.length, phrase_routes: phraseMap.length, cluster_routes: clusters.length, target_pages: registry.length, page_specs: specs.length, change_tickets: delta.length },
  workbook_sheet_order: sheetNames,
  sheet_count: sheetNames.length,
  rendered_sheet_count: previewDir ? sheetNames.length : 0,
  formula_error_scan_before_export: formulaErrorsBefore.ndjson,
  formula_error_scan_after_import: formulaErrorsAfter.ndjson,
  imported_sheet_inspection: importedSheets.ndjson,
  bounded_range_inspections: inspections,
  output: { file: OUTPUT_NAME, bytes: outputBuffer.length, sha256: sha256(outputBuffer) },
};
await fs.writeFile(reportPath, JSON.stringify(report, null, 2) + "\n", "utf8");
await fs.rm(`${xlsxPath}.inspect.ndjson`, { force: true });
console.log(JSON.stringify({ status: "PASS", xlsxPath, reportPath, output: report.output, counts: report.source_counts, sheets: sheetNames }, null, 2));
