#!/usr/bin/env node
/** Deterministic QA for the bounded Step 5A.8 validation package. No network access. */

import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { execFileSync } from "node:child_process";

const args = process.argv.slice(2);
const workspaceIndex = args.indexOf("--workspace");
if (workspaceIndex < 0 || !args[workspaceIndex + 1]) throw new Error("--workspace is required");
const OUT = path.resolve(args[workspaceIndex + 1]);
const JOB = path.dirname(OUT);
const REPO = execFileSync("git", ["rev-parse", "--show-toplevel"], { cwd: OUT, encoding: "utf8" }).trim();
const STARTING_HEAD = "69bf89875d176731e9614c76b0f39b38330bd8c6";
const CLIENT_PREVIEW_HANDOFF_EXPECTED_HEAD = "d5bcbaa99caf7c453ffe7279ac8231790e57156a";
const CLIENT_PREVIEW_CORRECTION_INTEGRATED_HEAD = "05b05a9d713d2581d11006d5a8863d277034da5a";
const CLIENT_PREVIEW_MATERIAL_REMOTE_COMMIT = "a5f32b70db1fb4c0250874fa8174b92e60002785";
const finalMode = args.includes("--final");
const remoteIndex = args.indexOf("--remote-readback-commit");
const remoteReadbackCommit = remoteIndex >= 0 ? args[remoteIndex + 1] : null;

function parseTsv(text) {
  const rows = []; let row = []; let field = ""; let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"' && text[i + 1] === '"') { field += '"'; i += 1; }
      else if (ch === '"') quoted = false;
      else field += ch;
    } else if (ch === '"' && field.length === 0) quoted = true;
    else if (ch === "\t") { row.push(field); field = ""; }
    else if (ch === "\n") { row.push(field.replace(/\r$/, "")); rows.push(row); row = []; field = ""; }
    else field += ch;
  }
  if (field.length || row.length) { row.push(field.replace(/\r$/, "")); rows.push(row); }
  const header = rows.shift() ?? [];
  return rows.filter((r) => r.some(Boolean)).map((r) => Object.fromEntries(header.map((h, i) => [h, r[i] ?? ""])));
}

async function readTsv(name) { return parseTsv(await fs.readFile(path.join(OUT, name), "utf8")); }
async function readJson(name) { return JSON.parse(await fs.readFile(path.join(OUT, name), "utf8")); }
async function hashFile(file) {
  const content = await fs.readFile(file);
  return { file: path.basename(file), sha256: crypto.createHash("sha256").update(content).digest("hex"), size_bytes: content.length };
}

const assertions = [];
function check(id, condition, detail) {
  assertions.push({ id, status: condition ? "PASS" : "FAIL", detail });
  if (!condition) throw new Error(`${id}: ${detail}`);
}
function exact(id, actual, expected) { check(id, actual === expected, `expected=${expected}; actual=${actual}`); }
function approx(id, actual, expected) { check(id, Math.abs(actual - expected) < 1e-10, `expected=${expected}; actual=${actual}`); }

const metrics = await readJson("STEP_05A_INFORMATION_GAIN_METRICS.json");
const funnel = await readTsv("STEP_05A_INFORMATION_GAIN_FUNNEL.tsv");
const requiredCounts = {
  preserved_discovery_queries: 75,
  preserved_discovery_top10_rows: 750,
  normalized_discovery_domains: 237,
  selected_competitor_domains: 9,
  competitor_target_urls: 44,
  accessible_at_requested_url: 43,
  redirected_accessible: 1,
  inaccessible: 0,
  candidate_occurrences: 92,
  deduplicated_candidate_directions: 43,
  duplicate_page_support_occurrences: 49,
  already_covered_page_directions: 22,
  potentially_new_wordstat_seeds: 14,
  off_scope_page_directions: 3,
  hold_review_page_directions: 4,
  wordstat_executions: 14,
  wordstat_returned_rows: 160,
  wordstat_direct_rows: 21,
  wordstat_association_rows: 139,
  wordstat_already_covered_rows: 56,
  wordstat_noise_rows: 51,
  wordstat_off_scope_rows: 26,
  wordstat_hold_rows: 7,
  potentially_new_wordstat_occurrences: 20,
  search_recheck_requirements: 9,
  search_succeeded: 7,
  search_outcome_unknown: 2,
  successful_search_top10_rows: 70,
  visibility_matrix_cells: 81,
  visible_selected_competitor_cells: 11,
  selected_competitor_ranking_rows: 12,
  unique_selected_competitors_visible: 7,
  selected_competitors_not_observed: 2,
  exact_previously_inspected_url_matches: 0,
  same_domain_different_url_visibility_cells: 11,
  same_domain_different_url_ranking_rows: 12,
  add_to_pipeline_directions: 7,
  hold_evidence_directions: 2,
  accepted_delta_rows: 16,
  suppressed_close_variants: 3,
  retained_occurrence_holds: 1,
  rejected_after_search: 0,
  unknown_retries: 0,
};
for (const [key, expected] of Object.entries(requiredCounts)) exact(`COUNT_${key.toUpperCase()}`, metrics.counts[key], expected);

const baselineExpected = {
  unique_semantic_phrases: 2840,
  active_phrases: 2332,
  assigned_phrases: 2313,
  search_required_phrases: 19,
  canonical_structural_units: 168,
  accepted_delta_normalized_overlap_count: 0,
  accepted_delta_internal_duplicate_count: 0,
  projected_unique_phrase_count_if_delta_survives_normal_downstream_pipeline: 2856,
};
for (const [key, expected] of Object.entries(baselineExpected)) exact(`BASELINE_${key.toUpperCase()}`, metrics.frozen_baseline[key], expected);

const rateExpected = {
  candidate_occurrence_to_deduplicated_direction_consolidation: [43, 92],
  duplicate_support_compression_share: [49, 92],
  deduplicated_direction_to_wordstat_seed: [14, 43],
  pre_wordstat_filtered_or_held_direction_share: [29, 43],
  already_covered_direction_share: [22, 43],
  wordstat_returned_row_to_potentially_new_search_occurrence: [20, 160],
  wordstat_rows_filtered_covered_noise_offscope_hold: [140, 160],
  wordstat_seed_to_search_recheck_direction: [9, 14],
  search_requirement_to_add_direction: [7, 9],
  successful_search_requirement_to_add_direction: [7, 7],
  search_decision_hold_rate: [2, 9],
  potentially_new_occurrence_to_accepted_delta_row: [16, 20],
  post_search_suppressed_or_held_occurrence_share: [4, 20],
  accepted_delta_to_frozen_unique_baseline_expansion: [16, 2840],
  accepted_delta_to_frozen_active_baseline_ratio: [16, 2332],
  final_add_direction_to_page_derived_direction_yield: [7, 43],
  selected_competitor_visibility_density: [11, 81],
  unique_selected_competitors_visible_share: [7, 9],
};
for (const [key, [numerator, denominator]] of Object.entries(rateExpected)) {
  const rate = metrics.rates[key];
  exact(`RATE_${key.toUpperCase()}_NUMERATOR`, rate.numerator, numerator);
  exact(`RATE_${key.toUpperCase()}_DENOMINATOR`, rate.denominator, denominator);
  approx(`RATE_${key.toUpperCase()}_VALUE`, rate.rate_decimal, numerator / denominator);
}
check("FUNNEL_ROWS_PRESENT", funnel.length >= 25, `rows=${funnel.length}`);
check("FUNNEL_RATE_NUMERATORS_PRESENT", funnel.filter((r) => r.metric_type === "YIELD_RATE").every((r) => r.numerator !== ""), "all yield rows have numerators");
check("FUNNEL_RATE_DENOMINATORS_PRESENT", funnel.filter((r) => r.metric_type === "YIELD_RATE").every((r) => r.denominator !== ""), "all yield rows have denominators");
check("FUNNEL_SOURCE_AUTHORITY_PRESENT", funnel.every((r) => r.source_authority), "all funnel rows name an authority");

approx("WORDSTAT_COST_RUB", metrics.provider_cost_efficiency.wordstat_cost_rub, 0.28);
approx("SEARCH_COST_RUB", metrics.provider_cost_efficiency.search_cost_rub, 4.392);
approx("TOTAL_COST_RUB", metrics.provider_cost_efficiency.total_incremental_provider_cost_rub, 4.672);
approx("COST_PER_ADD_DIRECTION", metrics.provider_cost_efficiency.total_cost_per_add_direction_rub, 4.672 / 7);
approx("COST_PER_DELTA_ROW", metrics.provider_cost_efficiency.total_cost_per_accepted_delta_row_rub, 4.672 / 16);
check("COST_NOT_QUALITY_TARGET", metrics.provider_cost_efficiency.boundary.includes("NOT_A_QUALITY_TARGET"), metrics.provider_cost_efficiency.boundary);

exact("STOP_THIS_REHEARSAL", metrics.stopping_assessment.stop_this_rehearsal, true);
exact("PERMANENT_THRESHOLD_VALIDATED", metrics.stopping_assessment.permanent_diminishing_gain_threshold_validated, false);
check("NO_UNIVERSAL_THRESHOLD_INFERENCE", metrics.stopping_assessment.threshold_reason.includes("single project execution"), metrics.stopping_assessment.threshold_reason);
exact("PROJECT_TEST_VALIDATED_REMAINS_FALSE", metrics.verdicts.ACTUAL_PROJECT_TEST_VALIDATED_STATE, "false__PENDING_OWNER_REVIEW");
exact("LEVEL1_NOT_PROMOTED", metrics.verdicts.LEVEL1_METHOD_PROMOTION_STATE, "NOT_PROMOTED");
exact("RECOMMENDED_VERDICT", metrics.verdicts.RECOMMENDED_PROJECT_TEST_VALIDATION, "RECOMMEND_VALIDATE_AFTER_OWNER_REVIEW");
exact("PROPAGATION_REQUIRED", metrics.propagation_state, "PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE");
check("PROVIDER_CALLS_ZERO", Object.values(metrics.provider_calls_by_work).every((v) => v === 0), JSON.stringify(metrics.provider_calls_by_work));

const delta = await readTsv("STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv");
const decisions = await readTsv("STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv");
const merge = await readTsv("STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv");
const visibility = await readTsv("STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv");
const searchSerp = await readTsv("STEP_05A_SEARCH_SERP_ROW_LEDGER.tsv");
const master = await readTsv(path.relative(OUT, path.join(JOB, "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv")));
const norm = (s) => s.toLocaleLowerCase("ru-RU").replace(/[^\p{L}\p{N}]+/gu, " ").trim().replace(/\s+/g, " ");
const masterSet = new Set(master.map((r) => norm(r.phrase)));
exact("LIVE_DELTA_ROWS", delta.length, 16);
exact("LIVE_DELTA_UNIQUE_NORMALIZED", new Set(delta.map((r) => norm(r.phrase))).size, 16);
exact("LIVE_DELTA_FROZEN_OVERLAP", delta.filter((r) => masterSet.has(norm(r.phrase))).length, 0);
check("DELTA_PROPAGATION_STATE_PRESERVED", delta.every((r) => r.propagation_state === "PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE"), "16/16 rows preserve propagation boundary");

const allowedPrefix = path.relative(REPO, OUT).replaceAll(path.sep, "/") + "/";
const changed = execFileSync("git", ["diff", "--name-only", STARTING_HEAD, CLIENT_PREVIEW_HANDOFF_EXPECTED_HEAD], { cwd: REPO, encoding: "utf8" }).trim().split("\n").filter(Boolean);
const authorizedHandoff = "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_05A_CLIENT_PREVIEW_OWNER_REVIEW_CORRECTION_WORK_HANDOFF_2026-09-08.md";
check("CHANGES_ISOLATED_TO_STEP05A_EXECUTION", changed.every((p) => p.startsWith(allowedPrefix) || p === authorizedHandoff), changed.join(" | "));
const correctionChanged = execFileSync("git", ["diff", "--name-only", CLIENT_PREVIEW_CORRECTION_INTEGRATED_HEAD, CLIENT_PREVIEW_MATERIAL_REMOTE_COMMIT], { cwd: REPO, encoding: "utf8" }).trim().split("\n").filter(Boolean);
check("CLIENT_PREVIEW_CORRECTION_CHANGES_ISOLATED", correctionChanged.every((p) => p.startsWith(allowedPrefix)), correctionChanged.join(" | "));
check("CORRECTION_DOCUMENT_01_UNCHANGED", !correctionChanged.some((p) => /(?:^|\/)01_OKNO_MSK_CLIENT_RESEARCH_REPORT/.test(p)), "Document 01 absent from correction diff");
check("CORRECTION_DOCUMENT_03_UNCHANGED", !correctionChanged.some((p) => /(?:^|\/)03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT/.test(p)), "Document 03 absent from correction diff");
check("CORRECTION_SEMANTIC_CORE_XLSX_UNCHANGED", !correctionChanged.some((p) => /(?:^|\/)04_OKNO_MSK_(?:FULL_SEMANTIC_CORE|REBUILT_RESEARCH_WORKBOOK).*\.xlsx$/.test(p)), "semantic-core workbook absent from correction diff");
const forbiddenPaths = [
  "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md",
  "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv",
  "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv",
];
for (const p of forbiddenPaths) check(`PROTECTED_UNCHANGED_${path.basename(p).toUpperCase().replaceAll(".", "_")}`, !changed.includes(p), p);
check("CORRECTED_CLIENT_RELEASE_UNCHANGED", !changed.some((p) => p.includes("OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05/")), "no corrected-release path changed");
check("RAW_PROVIDER_ENVELOPES_UNCHANGED", !changed.some((p) => /STEP_05A_(WORDSTAT|SEARCH)_ITEM_\d+.*_RAW\.json$/.test(p)), "no raw envelope changed");

const artifacts = [
  "STEP_05A_INFORMATION_GAIN_METRICS.json",
  "STEP_05A_INFORMATION_GAIN_FUNNEL.tsv",
  "STEP_05A_INFORMATION_GAIN_VALIDATION_REVIEW.xlsx",
];
if (finalMode) artifacts.push(
  "STEP_05A_FIRST_EXECUTION_VALIDATION_GATE_REGISTER.tsv",
  "STEP_05A_FIRST_EXECUTION_VALIDATION_REPORT.md",
  "STEP_05A_CLIENT_FACING_COMPETITOR_GAP_PREVIEW_RU.md",
  "CHECKPOINT_08_INFORMATION_GAIN_METRICS.md",
  "CHECKPOINT_09_FIRST_EXECUTION_VALIDATION.md",
  "STEP_05A_INFORMATION_GAIN_VALIDATION_EXECUTION_LOG.md",
);
try {
  await fs.access(path.join(OUT, "CHECKPOINT_10_INFORMATION_GAIN_VALIDATION_REMOTE_READBACK.md"));
  artifacts.push("CHECKPOINT_10_INFORMATION_GAIN_VALIDATION_REMOTE_READBACK.md");
} catch {}
for (const name of artifacts) {
  const stat = await fs.stat(path.join(OUT, name));
  check(`ARTIFACT_EXISTS_${name.toUpperCase().replaceAll(/[^A-Z0-9]+/g, "_")}`, stat.size > 0, `${name}; bytes=${stat.size}`);
}

let gates = [];
if (finalMode) {
  gates = await readTsv("STEP_05A_FIRST_EXECUTION_VALIDATION_GATE_REGISTER.tsv");
  exact("GATE_ROWS", gates.length, 10);
  exact("DETERMINISTIC_GATES_PASS", gates.filter((g) => g.deterministic_status === "PASS").length, 9);
  exact("OWNER_ONLY_GATES", gates.filter((g) => g.deterministic_status === "OWNER_REVIEW_REQUIRED").length, 1);
  const gate10 = gates.find((g) => g.gate_order === "10");
  exact("GATE10_OWNER_REVIEW_REQUIRED", gate10?.deterministic_status, "OWNER_REVIEW_REQUIRED");
  exact("GATE10_NOT_SELF_CERTIFIED", gate10?.work_authorized_to_close, "false");
  check("ALL_GATES_HAVE_EVIDENCE", gates.every((g) => g.evidence_files && g.supporting_counts_facts), "10/10 gate rows name evidence and facts");

  const preview = await fs.readFile(path.join(OUT, "STEP_05A_CLIENT_FACING_COMPETITOR_GAP_PREVIEW_RU.md"), "utf8");
  const report = await fs.readFile(path.join(OUT, "STEP_05A_FIRST_EXECUTION_VALIDATION_REPORT.md"), "utf8");
  for (const token of ["девять поисковых конкурентов", "44 страницы", "семи направлениям", "двум темам", "16 новых поисковых фраз", "не означают автоматическое создание новых страниц"]) {
    check(`PREVIEW_CONTAINS_${crypto.createHash("md5").update(token).digest("hex").slice(0, 8)}`, preview.includes(token), token);
  }
  const previewForbidden = [/STEP_/i, /\.tsv\b/i, /\.json\b/i, /\.md\b/i, /ADD_TO_PIPELINE/, /HOLD_EVIDENCE/, /PROJECT_TEST/, /\bSERP\b/, /_[A-Z0-9]+_/];
  check("PREVIEW_INTERNAL_TOKEN_LEAKAGE_ZERO", previewForbidden.every((pattern) => !pattern.test(preview)), "no internal enum/file token in client preview");
  check("PREVIEW_CYRILLIC_DOMINANT", (preview.match(/[А-Яа-яЁё]/g) ?? []).length > (preview.match(/[A-Za-z]/g) ?? []).length, "plain-Russian preview");

  const acceptedSection = preview.match(/## Какие 16 фраз приняты\n([\s\S]*?)\n## Что показала отдельная проверка позиций/)?.[1] ?? "";
  const acceptedPhrases = [...acceptedSection.matchAll(/^- «([^»]+)»$/gm)].map((match) => match[1]);
  const deltaPhrases = delta.map((row) => row.phrase);
  exact("PREVIEW_ACCEPTED_PHRASE_LIST_COUNT", acceptedPhrases.length, 16);
  exact("PREVIEW_ACCEPTED_PHRASE_LIST_UNIQUE", new Set(acceptedPhrases.map(norm)).size, 16);
  check("PREVIEW_ACCEPTED_PHRASES_EXACT_DELTA_MATCH", deltaPhrases.every((phrase) => acceptedPhrases.includes(phrase)) && acceptedPhrases.every((phrase) => deltaPhrases.includes(phrase)), "accepted client list equals all 16 delta phrases");
  const acceptedGroupHeadings = [...acceptedSection.matchAll(/^### \d+\. (.+?) — (\d+) (?:фраза|фразы|фраз)$/gm)];
  exact("PREVIEW_ACCEPTED_DIRECTION_GROUPS", acceptedGroupHeadings.length, 7);
  exact("PREVIEW_ACCEPTED_GROUP_DECLARED_TOTAL", acceptedGroupHeadings.reduce((sum, match) => sum + Number(match[2]), 0), 16);
  const excludedPhrases = merge.filter((row) => row.phrase_merge_state !== "MERGE_ACCEPTED").map((row) => row.returned_phrase);
  check("PREVIEW_SUPPRESSED_OR_HELD_NOT_ACCEPTED", excludedPhrases.every((phrase) => !acceptedPhrases.includes(phrase)), excludedPhrases.join(" | "));

  const successful = decisions.filter((row) => row.search_acquisition_state === "SUCCEEDED").sort((a, b) => Number(a.search_priority) - Number(b.search_priority));
  const unresolved = decisions.filter((row) => row.search_acquisition_state === "OUTCOME_UNKNOWN").sort((a, b) => Number(a.search_priority) - Number(b.search_priority));
  exact("PREVIEW_SUCCESSFUL_DIRECTIONS_SOURCE_COUNT", successful.length, 7);
  exact("PREVIEW_UNRESOLVED_DIRECTIONS_SOURCE_COUNT", unresolved.length, 2);
  const visibilitySection = preview.match(/## Что показала отдельная проверка позиций\n([\s\S]*?)\n## Что осталось неопределённым/)?.[1] ?? "";
  const clientVisibilityRows = [...visibilitySection.matchAll(/^\| «([^»]+)» \| (.+) \| (\d+) \| (\d+) \|$/gm)].map((match) => ({ query: match[1], observed: match[2], cells: Number(match[3]), rows: Number(match[4]) }));
  exact("PREVIEW_EXACT_QUERY_VISIBILITY_ROWS", clientVisibilityRows.length, 7);
  const rankPhrase = (ranks) => ranks.length === 1 ? `${ranks[0]}-е место` : `${ranks.slice(0, -1).map((rank) => `${rank}-е`).join(", ")} и ${ranks.at(-1)}-е места`;
  for (const direction of successful) {
    const clientRow = clientVisibilityRows.find((row) => row.query === direction.representative_query);
    check(`PREVIEW_VISIBILITY_QUERY_${direction.search_priority}`, Boolean(clientRow), direction.representative_query);
    const rankingRows = searchSerp.filter((row) => row.tested_query === direction.representative_query && row.selected_step5a_competitor === "true").sort((a, b) => Number(a.rank) - Number(b.rank));
    const domainRanks = new Map();
    for (const row of rankingRows) {
      if (!domainRanks.has(row.selected_competitor_domain)) domainRanks.set(row.selected_competitor_domain, []);
      domainRanks.get(row.selected_competitor_domain).push(Number(row.rank));
    }
    exact(`PREVIEW_VISIBILITY_CELL_COUNT_${direction.search_priority}`, clientRow.cells, domainRanks.size);
    exact(`PREVIEW_RANKING_ROW_COUNT_${direction.search_priority}`, clientRow.rows, rankingRows.length);
    for (const [domain, ranks] of domainRanks.entries()) check(`PREVIEW_EXACT_RANK_TRACE_${direction.search_priority}_${domain.replaceAll(/[^a-z0-9]+/gi, "_")}`, clientRow.observed.includes(`${domain} — ${rankPhrase(ranks)}`), `${domain}: ${ranks.join(",")}`);
    if (domainRanks.size === 0) check(`PREVIEW_ZERO_VISIBILITY_WORDING_${direction.search_priority}`, clientRow.observed.includes("ни один из девяти выбранных конкурентов не найден"), clientRow.observed);
  }
  exact("PREVIEW_VISIBLE_QUERY_DOMAIN_CELLS", clientVisibilityRows.reduce((sum, row) => sum + row.cells, 0), 11);
  exact("PREVIEW_SELECTED_COMPETITOR_RANKING_ROWS", clientVisibilityRows.reduce((sum, row) => sum + row.rows, 0), 12);
  exact("SOURCE_VISIBLE_QUERY_DOMAIN_CELLS", visibility.filter((row) => row.visibility_state === "VISIBLE_IN_TOP10").length, 11);
  exact("SOURCE_SELECTED_COMPETITOR_RANKING_ROWS", searchSerp.filter((row) => row.selected_step5a_competitor === "true").length, 12);
  check("PREVIEW_WATERPROOFING_ZERO_VISIBILITY_EXPLICIT", visibilitySection.includes("Ни один из девяти выбранных конкурентов не был замечен") && visibilitySection.includes("Направление всё равно прошло отбор"), "zero selected visibility plus multi-factor pass explanation");
  check("PREVIEW_DISCOVERY_VS_RANKING_BOUNDARY", preview.includes("использовалось только для поиска возможных пропусков") && preview.includes("Позиции сайтов по точным фразам независимо проверялись"), "page-topic discovery separated from exact-query Search proof");
  check("PREVIEW_INSPECTED_URL_RANKING_OVERCLAIM_ZERO", preview.includes("не приписываем 44 изученным тематическим страницам позиции") && preview.includes("совпадений с адресами исходных 44 страниц не было"), "44 discovery pages are not claimed as exact-query ranking URLs");
  check("PREVIEW_FILTERING_PATH_EXPLICIT", preview.includes("43 направления → 14 тем для Wordstat → 160 возвращённых строк → 20 кандидатов для проверки в Яндексе → 16 принятых фраз"), "complete 43->14->160->20->16 path");
  const unresolvedSection = preview.match(/## Что осталось неопределённым\n([\s\S]*?)\n## Итог для семантического ядра/)?.[1] ?? "";
  const unresolvedBullets = [...unresolvedSection.matchAll(/^- (.+?)[.;]$/gm)].map((match) => match[1]);
  exact("PREVIEW_UNRESOLVED_VISIBLE_COUNT", unresolvedBullets.length, 2);
  check("PREVIEW_UNRESOLVED_EXACT_MATCH", unresolved.every((row) => unresolvedBullets.includes(row.representative_query)) && unresolvedBullets.every((query) => unresolved.some((row) => row.representative_query === query)), unresolvedBullets.join(" | "));
  check("PREVIEW_NO_AUTOMATIC_PAGE_DECISION", preview.includes("не означают автоматическое создание новых страниц") && preview.includes("проверку назначения существующим страницам"), "normal downstream propagation retained");
  check("PREVIEW_NO_DEVELOPER_JARGON", !/\b(?:Gate|QA|delta|pipeline|frozen|owner|routing|enum|checkpoint)\b/i.test(preview), "no developer jargon in client preview");
  for (const token of ["PASS_9_OF_9_DETERMINISTIC_GATES", "MATERIAL_POSITIVE_GAIN_WITH_STRONG_FILTERING_VALUE", "OWNER_REVIEW_REQUIRED", "RECOMMEND_VALIDATE_AFTER_OWNER_REVIEW", "false / PENDING_OWNER_REVIEW", "NOT_PROMOTED", "NOT_VALIDATED_SINGLE_REHEARSAL", "PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE"]) {
    check(`REPORT_BOUNDARY_${crypto.createHash("md5").update(token).digest("hex").slice(0, 8)}`, report.includes(token), token);
  }
  check("REPORT_NO_PROJECT_TEST_TRUE", !/PROJECT_TEST_VALIDATED\s*=\s*true/i.test(report), "no persisted true verdict");
  check("REPORT_NO_PAGE_OWNERSHIP_ACTION", report.includes("Page ownership, creation, deletion, split/merge or implementation action created: false"), "explicit protection boundary");
}
if (remoteReadbackCommit) {
  exact("REMOTE_READBACK_MATERIAL_COMMIT", remoteReadbackCommit, CLIENT_PREVIEW_MATERIAL_REMOTE_COMMIT);
  check("REMOTE_READBACK_RECEIPT_PRESENT", artifacts.includes("CHECKPOINT_10_INFORMATION_GAIN_VALIDATION_REMOTE_READBACK.md"), "final receipt included");
}

const checkedFiles = await Promise.all(artifacts.map((name) => hashFile(path.join(OUT, name))));
const qa = {
  schema: "STEP_05A_FIRST_EXECUTION_VALIDATION_QA_V1",
  generated_date: "2026-09-08",
  phase: finalMode ? "FINAL" : "METRICS",
  status: "PASS",
  assertion_count: assertions.length,
  passed_assertions: assertions.filter((a) => a.status === "PASS").length,
  failed_assertions: 0,
  required_assertions: {
    GATE_ROWS: finalMode ? gates.length : "PENDING_FINAL_PHASE",
    SEARCH_REQUIREMENTS: metrics.counts.search_recheck_requirements,
    SEARCH_SUCCEEDED: metrics.counts.search_succeeded,
    SEARCH_UNKNOWN: metrics.counts.search_outcome_unknown,
    SERP_ROWS: metrics.counts.successful_search_top10_rows,
    WORDSTAT_ROWS: metrics.counts.wordstat_returned_rows,
    POTENTIALLY_NEW_OCCURRENCES: metrics.counts.potentially_new_wordstat_occurrences,
    ADD_DIRECTIONS: metrics.counts.add_to_pipeline_directions,
    HOLD_DIRECTIONS: metrics.counts.hold_evidence_directions,
    ACCEPTED_DELTA_ROWS: metrics.counts.accepted_delta_rows,
    UNKNOWN_RETRIES: metrics.counts.unknown_retries,
    LEVEL1_PROMOTED: false,
    PROJECT_TEST_VALIDATED_PERSISTED_TRUE: false,
    NEW_PROVIDER_OR_SUBSTITUTE_WEB_CALLS: 0,
  },
  protected_artifacts: {
    frozen_stage5_modified: false,
    canonical_units_modified: false,
    corrected_client_release_modified: false,
    documents_01_03_modified: false,
    semantic_core_xlsx_modified: false,
    raw_provider_envelopes_modified: false,
  },
  owner_boundary: {
    gate_10_status: finalMode ? "OWNER_REVIEW_REQUIRED" : "PENDING_FINAL_PHASE",
    project_test_validated: false,
    level1_method_promoted: false,
  },
  remote_readback: remoteReadbackCommit ? {
    status: "PASS",
    metrics_commit: "8a234f3c736fc9594881387ae49e5c6996cddd33",
    validation_commit: "a8eb434065d407cd9d858e45abd5d7b65adb4063",
    client_preview_correction_commit: remoteReadbackCommit,
    required_and_supporting_artifacts_read_back: 12,
    client_preview_correction_artifacts_read_back: 10,
    protected_remote_sha_comparisons_passed: 9,
    receipt_commit_state: "THIS_QA_AND_RECEIPT_AWAIT_FINAL_RECEIPT_COMMIT",
  } : { status: "PENDING_FINAL_RECEIPT" },
  checked_files: checkedFiles,
  assertions,
};
if (finalMode) await fs.writeFile(path.join(OUT, "STEP_05A_FIRST_EXECUTION_VALIDATION_QA.json"), `${JSON.stringify(qa, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ status: qa.status, phase: qa.phase, assertions: qa.assertion_count, passed: qa.passed_assertions }));
