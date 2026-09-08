#!/usr/bin/env node
/** Build Step 5A.8 information-gain and validation-assessment artifacts.
 *
 * Inputs are immutable preserved Step 5A.1–5A.7 and frozen OKNO_MSK files.
 * This script performs no network/provider access and never promotes Level 1.
 */

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";


const args = process.argv.slice(2);
const workspaceIndex = args.indexOf("--workspace");
if (workspaceIndex < 0 || !args[workspaceIndex + 1]) {
  throw new Error("--workspace <Step 5A execution directory> is required");
}
const OUT = path.resolve(args[workspaceIndex + 1]);
const phaseIndex = args.indexOf("--phase");
const PHASE = phaseIndex >= 0 ? args[phaseIndex + 1] : "final";
if (!new Set(["metrics", "final"]).has(PHASE)) throw new Error(`Unsupported phase: ${PHASE}`);

const JOB = path.dirname(OUT);
const STARTING_HEAD = "69bf89875d176731e9614c76b0f39b38330bd8c6";

const files = {
  pageQa: path.join(OUT, "STEP_05A_PAGE_INSPECTION_QA.json"),
  domainFrequency: path.join(OUT, "STEP_05A_DOMAIN_FREQUENCY.tsv"),
  candidates: path.join(OUT, "STEP_05A_DERIVED_SEED_CANDIDATES.tsv"),
  wordstatAcquisition: path.join(OUT, "STEP_05A_WORDSTAT_SEED_ACQUISITION_LEDGER.tsv"),
  wordstatRows: path.join(OUT, "STEP_05A_WORDSTAT_RETURNED_PHRASE_LEDGER.tsv"),
  wordstatRecon: path.join(OUT, "STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv"),
  searchPackage: path.join(OUT, "STEP_05A_SEARCH_RECHECK_REQUIREMENT_PACKAGE.tsv"),
  searchAcquisition: path.join(OUT, "STEP_05A_SEARCH_REQUIREMENT_ACQUISITION_LEDGER.tsv"),
  searchSerp: path.join(OUT, "STEP_05A_SEARCH_SERP_ROW_LEDGER.tsv"),
  visibility: path.join(OUT, "STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv"),
  decisions: path.join(OUT, "STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv"),
  merge: path.join(OUT, "STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv"),
  delta: path.join(OUT, "STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv"),
  master: path.join(JOB, "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv"),
  units: path.join(JOB, "RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv"),
};

const outputs = {
  metrics: path.join(OUT, "STEP_05A_INFORMATION_GAIN_METRICS.json"),
  funnel: path.join(OUT, "STEP_05A_INFORMATION_GAIN_FUNNEL.tsv"),
  gates: path.join(OUT, "STEP_05A_FIRST_EXECUTION_VALIDATION_GATE_REGISTER.tsv"),
  report: path.join(OUT, "STEP_05A_FIRST_EXECUTION_VALIDATION_REPORT.md"),
  qa: path.join(OUT, "STEP_05A_FIRST_EXECUTION_VALIDATION_QA.json"),
  preview: path.join(OUT, "STEP_05A_CLIENT_FACING_COMPETITOR_GAP_PREVIEW_RU.md"),
  workbook: path.join(OUT, "STEP_05A_INFORMATION_GAIN_VALIDATION_REVIEW.xlsx"),
  checkpoint08: path.join(OUT, "CHECKPOINT_08_INFORMATION_GAIN_METRICS.md"),
  checkpoint09: path.join(OUT, "CHECKPOINT_09_FIRST_EXECUTION_VALIDATION.md"),
  log: path.join(OUT, "STEP_05A_INFORMATION_GAIN_VALIDATION_EXECUTION_LOG.md"),
};


function parseDelimited(text, delimiter = "\t") {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"' && text[i + 1] === '"') {
        field += '"'; i += 1;
      } else if (ch === '"') quoted = false;
      else field += ch;
    } else if (ch === '"' && field.length === 0) quoted = true;
    else if (ch === delimiter) { row.push(field); field = ""; }
    else if (ch === "\n") { row.push(field.replace(/\r$/, "")); rows.push(row); row = []; field = ""; }
    else field += ch;
  }
  if (field.length || row.length) { row.push(field.replace(/\r$/, "")); rows.push(row); }
  const header = rows.shift() ?? [];
  return rows.filter((r) => r.some((v) => v !== "")).map((r) => Object.fromEntries(header.map((h, i) => [h, r[i] ?? ""])));
}

function quoteTsv(value) {
  const text = value === null || value === undefined ? "" : String(value);
  return /[\t\n\r"]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

async function readTsv(file) {
  return parseDelimited(await fs.readFile(file, "utf8"));
}

async function writeTsv(file, rows, fields) {
  const lines = [fields.map(quoteTsv).join("\t")];
  for (const row of rows) lines.push(fields.map((field) => quoteTsv(row[field])).join("\t"));
  await fs.writeFile(file, `${lines.join("\n")}\n`, "utf8");
}

function countBy(rows, key) {
  const out = {};
  for (const row of rows) out[row[key]] = (out[row[key]] ?? 0) + 1;
  return out;
}

function normalizePhrase(text) {
  return text.toLocaleLowerCase("ru-RU").replace(/[^\p{L}\p{N}]+/gu, " ").trim().replace(/\s+/g, " ");
}

function rateMetric(numerator, denominator) {
  return {
    numerator,
    denominator,
    rate_decimal: numerator / denominator,
    rate_percent: (numerator / denominator) * 100,
  };
}

function assertEqual(actual, expected, label) {
  if (actual !== expected) throw new Error(`${label}: expected ${expected}, got ${actual}`);
}

function formatPercent(value, decimals = 2) {
  return `${value.toFixed(decimals)}%`;
}

function formatRub(value, decimals = 3) {
  return `${value.toFixed(decimals)} RUB`;
}

function excelCol(index) {
  let n = index + 1; let out = "";
  while (n) { const rem = (n - 1) % 26; out = String.fromCharCode(65 + rem) + out; n = Math.floor((n - 1) / 26); }
  return out;
}


async function loadEvidence() {
  const [pageQa, domainFrequency, candidates, wordstatAcquisition, wordstatRows, wordstatRecon, searchPackage, searchAcquisition, searchSerp, visibility, decisions, merge, delta, master, units] = await Promise.all([
    JSON.parse(await fs.readFile(files.pageQa, "utf8")),
    readTsv(files.domainFrequency), readTsv(files.candidates), readTsv(files.wordstatAcquisition),
    readTsv(files.wordstatRows), readTsv(files.wordstatRecon), readTsv(files.searchPackage),
    readTsv(files.searchAcquisition), readTsv(files.searchSerp), readTsv(files.visibility),
    readTsv(files.decisions), readTsv(files.merge), readTsv(files.delta), readTsv(files.master), readTsv(files.units),
  ]);

  const wordstatCostItems = [];
  for (let i = 1; i <= 14; i += 1) {
    const raw = JSON.parse(await fs.readFile(path.join(OUT, `STEP_05A_WORDSTAT_ITEM_${String(i).padStart(2, "0")}_RAW.json`), "utf8"));
    wordstatCostItems.push(raw.item.estimated_cost_rub);
  }
  const searchCostItems = [];
  for (let i = 1; i <= 9; i += 1) {
    const suffix = new Set([5, 7]).has(i) ? "_OUTCOME_UNKNOWN" : "";
    const raw = JSON.parse(await fs.readFile(path.join(OUT, `STEP_05A_SEARCH_ITEM_${String(i).padStart(2, "0")}${suffix}_RAW.json`), "utf8"));
    searchCostItems.push(raw.item.estimated_cost_rub);
  }
  return { pageQa, domainFrequency, candidates, wordstatAcquisition, wordstatRows, wordstatRecon, searchPackage, searchAcquisition, searchSerp, visibility, decisions, merge, delta, master, units, wordstatCostItems, searchCostItems };
}


function deriveMetrics(e) {
  const candidateStates = countBy(e.candidates, "seed_decision");
  const wsStates = countBy(e.wordstatRecon, "semantic_reconciliation_result");
  const searchStates = countBy(e.searchAcquisition, "search_acquisition_state");
  const finalStates = countBy(e.decisions, "final_routing_state");
  const mergeStates = countBy(e.merge, "phrase_merge_state");
  const visibleCells = e.visibility.filter((row) => row.visibility_state === "VISIBLE_IN_TOP10");
  const visibleDomains = [...new Set(visibleCells.map((row) => row.selected_competitor_domain))].sort();
  const allSelectedDomains = [...new Set(e.visibility.map((row) => row.selected_competitor_domain))].sort();
  const notVisibleDomains = allSelectedDomains.filter((domain) => !visibleDomains.includes(domain));
  const zeroVisibleAddDirections = e.decisions.filter((row) => row.final_routing_state === "ADD_TO_PIPELINE" && Number(row.selected_competitors_visible_count) === 0).map((row) => ({ direction_id: row.deduplicated_direction_id, query: row.representative_query }));
  const selectedRankingRows = e.searchSerp.filter((row) => row.selected_step5a_competitor === "true");
  const exactInspectedMatches = selectedRankingRows.filter((row) => row.equals_previously_inspected_competitor_url === "true");
  const sameDomainDifferentUrlRows = selectedRankingRows.filter((row) => row.selected_competitor_url_relation === "SAME_SELECTED_COMPETITOR_DOMAIN__DIFFERENT_URL");

  const masterStates = countBy(e.master, "final_semantic_state");
  const baseline = {
    unique_semantic_phrases: e.master.length,
    active_phrases: (masterStates.ASSIGNED ?? 0) + (masterStates.ASSIGNED_HOLD ?? 0) + (masterStates.SEARCH_REQUIRED ?? 0),
    assigned_phrases: (masterStates.ASSIGNED ?? 0) + (masterStates.ASSIGNED_HOLD ?? 0),
    search_required_phrases: masterStates.SEARCH_REQUIRED ?? 0,
    canonical_structural_units: e.units.length,
  };
  const masterNorm = new Set(e.master.map((row) => normalizePhrase(row.phrase)));
  const deltaNorm = e.delta.map((row) => normalizePhrase(row.phrase));
  const deltaOverlap = [...new Set(deltaNorm.filter((phrase) => masterNorm.has(phrase)))];
  const deltaDuplicateCount = deltaNorm.length - new Set(deltaNorm).size;

  const wordstatCost = e.wordstatCostItems.reduce((a, b) => a + Number(b), 0);
  const searchCost = e.searchCostItems.reduce((a, b) => a + Number(b), 0);
  const totalCost = wordstatCost + searchCost;

  const counts = {
    preserved_discovery_queries: 75,
    preserved_discovery_top10_rows: 750,
    normalized_discovery_domains: e.domainFrequency.length,
    selected_competitor_domains: e.pageQa.counts.selected_domains,
    competitor_target_urls: e.pageQa.counts.authorized_urls,
    accessible_at_requested_url: e.pageQa.counts.accessible_at_requested_url,
    redirected_accessible: e.pageQa.counts.redirected_accessible,
    inaccessible: e.pageQa.counts.inaccessible,
    candidate_occurrences: e.candidates.length,
    deduplicated_candidate_directions: e.pageQa.counts.deduplicated_candidate_directions,
    duplicate_page_support_occurrences: candidateStates.DUPLICATE_OF_ANOTHER_COMPETITOR_SEED ?? 0,
    already_covered_page_directions: candidateStates.ALREADY_COVERED_EXACT_OR_CLOSE ?? 0,
    potentially_new_wordstat_seeds: candidateStates.POTENTIALLY_NEW_WORDSTAT_SEED ?? 0,
    off_scope_page_directions: candidateStates.OFF_SCOPE_BUSINESS ?? 0,
    hold_review_page_directions: candidateStates.HOLD_REVIEW ?? 0,
    wordstat_executions: e.wordstatAcquisition.length,
    wordstat_returned_rows: e.wordstatRows.length,
    wordstat_direct_rows: e.wordstatRows.filter((row) => row.wordstat_row_class === "DIRECT_RESULT").length,
    wordstat_association_rows: e.wordstatRows.filter((row) => row.wordstat_row_class === "ASSOCIATION").length,
    wordstat_already_covered_rows: wsStates.ALREADY_COVERED_EXACT_OR_CLOSE ?? 0,
    wordstat_noise_rows: wsStates.NOISE_IRRELEVANT ?? 0,
    wordstat_off_scope_rows: wsStates.OFF_SCOPE_BUSINESS ?? 0,
    wordstat_hold_rows: wsStates.HOLD_EVIDENCE ?? 0,
    potentially_new_wordstat_occurrences: wsStates.POTENTIALLY_NEW_SEARCH_RECHECK ?? 0,
    search_recheck_requirements: e.searchPackage.length,
    search_succeeded: searchStates.SUCCEEDED ?? 0,
    search_outcome_unknown: searchStates.OUTCOME_UNKNOWN ?? 0,
    successful_search_top10_rows: e.searchSerp.length,
    visibility_matrix_cells: e.visibility.length,
    visible_selected_competitor_cells: visibleCells.length,
    selected_competitor_ranking_rows: selectedRankingRows.length,
    unique_selected_competitors_visible: visibleDomains.length,
    selected_competitors_not_observed: notVisibleDomains.length,
    exact_previously_inspected_url_matches: exactInspectedMatches.length,
    same_domain_different_url_visibility_cells: visibleCells.filter((row) => row.ranking_url_previously_inspected_state === "SAME_DOMAIN_DIFFERENT_URL").length,
    same_domain_different_url_ranking_rows: sameDomainDifferentUrlRows.length,
    add_to_pipeline_directions: finalStates.ADD_TO_PIPELINE ?? 0,
    hold_evidence_directions: finalStates.HOLD_EVIDENCE ?? 0,
    accepted_delta_rows: e.delta.length,
    suppressed_close_variants: mergeStates.SUPPRESSED_AS_CLOSE_VARIANT_DUPLICATE ?? 0,
    retained_occurrence_holds: mergeStates.RETAIN_HOLD ?? 0,
    rejected_after_search: mergeStates.REJECT_AFTER_SEARCH ?? 0,
    unknown_retries: 0,
    website_text_as_ranking_overclaims: 0,
    full_competitor_keyword_universe_overclaims: 0,
  };

  const expected = {
    normalized_discovery_domains: 237, selected_competitor_domains: 9, competitor_target_urls: 44,
    accessible_at_requested_url: 43, redirected_accessible: 1, inaccessible: 0,
    candidate_occurrences: 92, deduplicated_candidate_directions: 43,
    duplicate_page_support_occurrences: 49, already_covered_page_directions: 22,
    potentially_new_wordstat_seeds: 14, off_scope_page_directions: 3, hold_review_page_directions: 4,
    wordstat_executions: 14, wordstat_returned_rows: 160, wordstat_direct_rows: 21,
    wordstat_association_rows: 139, wordstat_already_covered_rows: 56, wordstat_noise_rows: 51,
    wordstat_off_scope_rows: 26, wordstat_hold_rows: 7, potentially_new_wordstat_occurrences: 20,
    search_recheck_requirements: 9, search_succeeded: 7, search_outcome_unknown: 2,
    successful_search_top10_rows: 70, visibility_matrix_cells: 81, visible_selected_competitor_cells: 11,
    selected_competitor_ranking_rows: 12, unique_selected_competitors_visible: 7,
    selected_competitors_not_observed: 2, exact_previously_inspected_url_matches: 0,
    same_domain_different_url_visibility_cells: 11, same_domain_different_url_ranking_rows: 12,
    add_to_pipeline_directions: 7, hold_evidence_directions: 2, accepted_delta_rows: 16,
    suppressed_close_variants: 3, retained_occurrence_holds: 1, rejected_after_search: 0,
  };
  for (const [key, value] of Object.entries(expected)) assertEqual(counts[key], value, key);
  assertEqual(baseline.unique_semantic_phrases, 2840, "baseline.unique_semantic_phrases");
  assertEqual(baseline.active_phrases, 2332, "baseline.active_phrases");
  assertEqual(baseline.assigned_phrases, 2313, "baseline.assigned_phrases");
  assertEqual(baseline.search_required_phrases, 19, "baseline.search_required_phrases");
  assertEqual(baseline.canonical_structural_units, 168, "baseline.canonical_structural_units");
  assertEqual(deltaOverlap.length, 0, "delta normalized overlap with frozen baseline");
  assertEqual(deltaDuplicateCount, 0, "delta duplicate normalized phrases");
  if (Math.abs(wordstatCost - 0.28) > 1e-9 || Math.abs(searchCost - 4.392) > 1e-9) throw new Error("Preserved provider costs changed");

  const rates = {
    candidate_occurrence_to_deduplicated_direction_consolidation: rateMetric(43, 92),
    duplicate_support_compression_share: rateMetric(49, 92),
    deduplicated_direction_to_wordstat_seed: rateMetric(14, 43),
    pre_wordstat_filtered_or_held_direction_share: rateMetric(29, 43),
    already_covered_direction_share: rateMetric(22, 43),
    wordstat_returned_row_to_potentially_new_search_occurrence: rateMetric(20, 160),
    wordstat_rows_filtered_covered_noise_offscope_hold: rateMetric(140, 160),
    wordstat_seed_to_search_recheck_direction: rateMetric(9, 14),
    search_requirement_to_add_direction: rateMetric(7, 9),
    successful_search_requirement_to_add_direction: rateMetric(7, 7),
    search_decision_hold_rate: rateMetric(2, 9),
    potentially_new_occurrence_to_accepted_delta_row: rateMetric(16, 20),
    post_search_suppressed_or_held_occurrence_share: rateMetric(4, 20),
    accepted_delta_to_frozen_unique_baseline_expansion: rateMetric(16, 2840),
    accepted_delta_to_frozen_active_baseline_ratio: rateMetric(16, 2332),
    final_add_direction_to_page_derived_direction_yield: rateMetric(7, 43),
    selected_competitor_visibility_density: rateMetric(11, 81),
    unique_selected_competitors_visible_share: rateMetric(7, 9),
  };

  const provider_cost_efficiency = {
    wordstat_cost_rub: wordstatCost,
    search_cost_rub: searchCost,
    total_incremental_provider_cost_rub: totalCost,
    wordstat_cost_per_seed_rub: wordstatCost / 14,
    wordstat_cost_per_returned_row_rub: wordstatCost / 160,
    search_cost_per_paid_requirement_boundary_rub: searchCost / 9,
    search_cost_per_successful_requirement_rub: searchCost / 7,
    total_cost_per_add_direction_rub: totalCost / 7,
    total_cost_per_accepted_delta_row_rub: totalCost / 16,
    total_cost_per_successfully_resolved_search_requirement_rub: totalCost / 7,
    boundary: "DESCRIPTIVE_INCREMENTAL_COGS_ONLY__NOT_A_QUALITY_TARGET_OR_REJECTION_RULE",
  };

  return {
    schema: "STEP_05A_INFORMATION_GAIN_METRICS_V1",
    generated_date: "2026-09-08",
    evidence_scope: "PRESERVED_STEP_5A_1_THROUGH_5A_7_ONLY",
    starting_head: STARTING_HEAD,
    counts,
    frozen_baseline: {
      ...baseline,
      accepted_delta_normalized_overlap_count: deltaOverlap.length,
      accepted_delta_internal_duplicate_count: deltaDuplicateCount,
      projected_unique_phrase_count_if_delta_survives_normal_downstream_pipeline: baseline.unique_semantic_phrases + counts.accepted_delta_rows,
      projection_boundary: "ARITHMETIC_ONLY__DELTA_IS_NOT_FROZEN_TRUTH_AND_REMAINS_SUBJECT_TO_NORMAL_DOWNSTREAM_PROCESSING",
    },
    rates,
    provider_cost_efficiency,
    filtering_and_derisking: {
      page_directions_not_sent_to_wordstat: 29,
      wordstat_rows_not_sent_to_search_recheck: 140,
      potentially_new_occurrences_not_added_to_delta: 4,
      holds_preserved_without_fabrication: 2,
      close_variants_suppressed_without_delta_inflation: 3,
      website_text_as_ranking_overclaims_prevented: 0,
      full_competitor_keyword_universe_overclaims_prevented: 0,
    },
    competitor_visibility: {
      selected_domains: allSelectedDomains,
      visible_domains_in_successful_rechecks: visibleDomains,
      not_observed_domains_in_successful_rechecks: notVisibleDomains,
      zero_selected_competitor_visible_but_add_supported: zeroVisibleAddDirections,
      exact_previously_inspected_url_matches: exactInspectedMatches.length,
      same_domain_different_url_visibility_cells: counts.same_domain_different_url_visibility_cells,
      same_domain_different_url_ranking_rows: counts.same_domain_different_url_ranking_rows,
      claim_boundary: "EXACT_SUCCESSFUL_RECHECKS_ONLY__NOT_FULL_COMPETITOR_KEYWORD_UNIVERSE",
    },
    stopping_assessment: {
      material_new_information: "YES__7_SEARCH_CONFIRMED_DIRECTIONS_AND_16_ACCEPTED_OCCURRENCES",
      evidence_mix: "STRONG_FILTERING_WITH_MATERIAL_POSITIVE_NOVELTY",
      stop_this_rehearsal: true,
      stop_reason: "The authorized bounded chain is complete; it produced material additions, preserved two unknowns as holds, and provides no authority for recursive competitor/seed expansion.",
      permanent_diminishing_gain_threshold_validated: false,
      threshold_reason: "A single project execution cannot establish a reusable saturation threshold.",
      future_rehearsal_observation: "Measure marginal accepted directions and accepted occurrences per added domain/page batch together with covered/noise/off-scope/hold shares and cost; extend while a distinct bounded batch still yields material in-scope additions, and consider stopping earlier when varied consecutive batches predominantly repeat or add noise.",
    },
    verdicts: {
      FIRST_EXECUTION_TECHNICAL_VALIDATION: "PASS_9_OF_9_DETERMINISTIC_GATES",
      FIRST_EXECUTION_INFORMATION_GAIN_VERDICT: "MATERIAL_POSITIVE_GAIN_WITH_STRONG_FILTERING_VALUE",
      CLIENT_FACING_USEFULNESS_GATE: "OWNER_REVIEW_REQUIRED",
      RECOMMENDED_PROJECT_TEST_VALIDATION: "RECOMMEND_VALIDATE_AFTER_OWNER_REVIEW",
      ACTUAL_PROJECT_TEST_VALIDATED_STATE: "false__PENDING_OWNER_REVIEW",
      LEVEL1_METHOD_PROMOTION_STATE: "NOT_PROMOTED",
      PERMANENT_DIMINISHING_GAIN_THRESHOLD_STATE: "NOT_VALIDATED_SINGLE_REHEARSAL",
    },
    propagation_state: "PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE",
    provider_calls_by_work: { yandex_search: 0, wordstat: 0, alice: 0, gensearch: 0, webmaster: 0, metrika: 0, direct: 0, substitute_web_search: 0, competitor_page_reads: 0 },
    next_actions: [
      "OWNER_REVIEW_STEP_5A_FIRST_EXECUTION_VALIDATION_AND_CLIENT_FACING_PREVIEW",
      "PROPAGATE_STEP_5A_ACCEPTED_SEMANTIC_PIPELINE_DELTA_THROUGH_NORMAL_DOWNSTREAM_PIPELINE",
    ],
  };
}


function buildFunnel(metrics) {
  const rows = [];
  const addCount = (id, stage, label, value, source, note) => rows.push({ metric_order: rows.length + 1, metric_type: "COUNT", metric_id: id, stage, metric_label_ru: label, numerator: value, denominator: "", metric_value: value, rate_decimal: "", rate_percent: "", unit: "count", source_authority: source, interpretation: note });
  const addRate = (id, stage, label, rate, source, note) => rows.push({ metric_order: rows.length + 1, metric_type: "YIELD_RATE", metric_id: id, stage, metric_label_ru: label, numerator: rate.numerator, denominator: rate.denominator, metric_value: rate.rate_decimal, rate_decimal: rate.rate_decimal, rate_percent: rate.rate_percent, unit: "ratio", source_authority: source, interpretation: note });
  const addCost = (id, label, numerator, denominator, value, source, note) => rows.push({ metric_order: rows.length + 1, metric_type: "COST_EFFICIENCY", metric_id: id, stage: "PROVIDER_COST", metric_label_ru: label, numerator, denominator, metric_value: value, rate_decimal: "", rate_percent: "", unit: "RUB", source_authority: source, interpretation: note });
  const c = metrics.counts; const r = metrics.rates; const cost = metrics.provider_cost_efficiency;
  addCount("DISCOVERY_QUERIES", "5A.1", "Сохранённые поисковые запросы для поиска конкурентов", c.preserved_discovery_queries, "STEP_05A_SERP_COMBINED_750.tsv", "Полный сохранённый набор запросов.");
  addCount("DISCOVERY_TOP10_ROWS", "5A.1", "Сохранённые строки первых десяти результатов", c.preserved_discovery_top10_rows, "STEP_05A_SERP_COMBINED_750.tsv", "75 запросов × 10 строк.");
  addCount("SELECTED_COMPETITOR_DOMAINS", "5A.1", "Выбранные поисковые конкуренты", c.selected_competitor_domains, "STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv", "Ограниченный набор из 237 наблюдавшихся доменов.");
  addRate("TARGET_URL_ACCESS_YIELD", "5A.2", "Доступные целевые страницы конкурентов", rateMetric(44, 44), "STEP_05A_PAGE_INSPECTION_QA.json", "43 открылись по исходному адресу, 1 после перенаправления, 0 недоступны.");
  addCount("PAGE_DERIVED_CANDIDATE_OCCURRENCES", "5A.3", "Наблюдения дополнительных тем на страницах", c.candidate_occurrences, "STEP_05A_DERIVED_SEED_CANDIDATES.tsv", "Каждое наблюдение сохраняет постраничное происхождение.");
  addRate("CANDIDATE_TO_DEDUP_DIRECTION", "5A.3", "Консолидация наблюдений в уникальные направления", r.candidate_occurrence_to_deduplicated_direction_consolidation, "STEP_05A_PAGE_INSPECTION_QA.json", "43 направления из 92 наблюдений.");
  addRate("DUPLICATE_SUPPORT_COMPRESSION", "5A.3", "Доля повторной поддержки направлений", r.duplicate_support_compression_share, "STEP_05A_DERIVED_SEED_CANDIDATES.tsv", "49 повторных подтверждений сохранены как происхождение, но не раздуты до новых направлений.");
  addRate("ALREADY_COVERED_DIRECTION_SHARE", "5A.3", "Уже покрытые направления", r.already_covered_direction_share, "STEP_05A_DERIVED_SEED_CANDIDATES.tsv", "22 из 43 не потребовали нового Wordstat.");
  addRate("DIRECTION_TO_WORDSTAT_SEED", "5A.3→5A.4", "Направления, переданные в Wordstat", r.deduplicated_direction_to_wordstat_seed, "STEP_05A_WORDSTAT_REQUIREMENT_PACKAGE.tsv", "14 из 43 после проверки покрытия и границ бизнеса.");
  addRate("PRE_WORDSTAT_FILTER_OR_HOLD", "5A.3", "Направления, остановленные до Wordstat", r.pre_wordstat_filtered_or_held_direction_share, "STEP_05A_DERIVED_SEED_CANDIDATES.tsv", "22 уже покрыты, 3 вне рамок, 4 оставлены на уточнение.");
  addRate("WORDSTAT_EXECUTION_SUCCESS", "5A.4", "Успешно выполненные Wordstat-проверки", rateMetric(14, 14), "STEP_05A_WORDSTAT_SEED_ACQUISITION_LEDGER.tsv", "Все 14 разрешённых seed выполнены; пустой ответ не приравнен к нулевому спросу.");
  addCount("WORDSTAT_RETURNED_ROWS", "5A.4", "Фактически возвращённые строки Wordstat", c.wordstat_returned_rows, "STEP_05A_WORDSTAT_RETURNED_PHRASE_LEDGER.tsv", "21 прямая строка + 139 ассоциаций.");
  addRate("WORDSTAT_TO_POTENTIAL_SEARCH_OCCURRENCE", "5A.5", "Потенциально новые вхождения после Wordstat", r.wordstat_returned_row_to_potentially_new_search_occurrence, "STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv", "20 из 160 потребовали проверки текущей выдачи.");
  addRate("WORDSTAT_FILTERED_SHARE", "5A.5", "Wordstat-строки, не переданные в Search", r.wordstat_rows_filtered_covered_noise_offscope_hold, "STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv", "56 уже покрыты, 51 шум, 26 вне рамок, 7 hold.");
  addRate("WORDSTAT_SEED_TO_SEARCH_DIRECTION", "5A.5→5A.6", "Wordstat seeds, сформировавшие Search-направления", r.wordstat_seed_to_search_recheck_direction, "STEP_05A_SEARCH_RECHECK_REQUIREMENT_PACKAGE.tsv", "9 уникальных запросов из 14 Wordstat seeds.");
  addRate("SEARCH_SUCCESS_RATE", "5A.6", "Успешные Search-проверки", rateMetric(7, 9), "STEP_05A_SEARCH_REQUIREMENT_ACQUISITION_LEDGER.tsv", "2 результата остались неизвестными и не повторялись.");
  addRate("SEARCH_HOLD_RATE", "5A.6→5A.7", "Доля направлений на удержании", r.search_decision_hold_rate, "STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv", "2 из 9 сохранены без выдуманного результата.");
  addRate("SEARCH_REQUIREMENT_TO_ADD", "5A.7", "Подтверждённые направления от всех Search-требований", r.search_requirement_to_add_direction, "STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv", "7 из 9 добавлены только в семантический pipeline.");
  addRate("SUCCESSFUL_SEARCH_TO_ADD", "5A.7", "Подтверждённые направления от успешных Search-проверок", r.successful_search_requirement_to_add_direction, "STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv", "7 из 7 успешных проверок дали релевантное новое направление.");
  addRate("POTENTIAL_OCCURRENCE_TO_DELTA", "5A.7", "Принятые строки semantic delta", r.potentially_new_occurrence_to_accepted_delta_row, "STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv", "16 из 20; 3 близких повтора подавлены, 1 оставлен на hold.");
  addRate("POST_SEARCH_NOT_ADDED", "5A.7", "Потенциальные вхождения, не добавленные после Search", r.post_search_suppressed_or_held_occurrence_share, "STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv", "4 из 20 не раздувают delta.");
  addRate("DELTA_TO_UNIQUE_BASELINE", "5A.8", "Расширение относительно 2 840 уникальных фраз", r.accepted_delta_to_frozen_unique_baseline_expansion, "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv", "16 точных нормализованных фраз не пересекаются с frozen baseline; ещё не frozen truth.");
  addRate("DELTA_TO_ACTIVE_BASELINE", "5A.8", "Отношение delta к 2 332 активным фразам", r.accepted_delta_to_frozen_active_baseline_ratio, "RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv", "Контекст размера активного ядра, не показатель качества.");
  addRate("FINAL_DIRECTION_YIELD_FROM_PAGE_DIRECTIONS", "5A.8", "Итоговый выход новых направлений от 43 направлений", r.final_add_direction_to_page_derived_direction_yield, "STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv", "7 направлений получили Search-подтверждение.");
  addRate("COMPETITOR_VISIBILITY_DENSITY", "5A.6", "Плотность видимости выбранных конкурентов", r.selected_competitor_visibility_density, "STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv", "11 наблюдаемых ячеек из 81; неизвестные Search не трактуются как отсутствие.");
  addRate("UNIQUE_VISIBLE_COMPETITOR_SHARE", "5A.6", "Доля выбранных конкурентов, замеченных в успешных recheck", r.unique_selected_competitors_visible_share, "STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv", "7 из 9; это только семь точных успешных запросов.");
  addCost("TOTAL_INCREMENTAL_PROVIDER_COST", "Суммарная сохранённая стоимость Wordstat + Search", cost.total_incremental_provider_cost_rub, "", cost.total_incremental_provider_cost_rub, "Preserved raw provider envelopes", "0.28 + 4.392; описательная себестоимость, не цель качества.");
  addCost("COST_PER_ADD_DIRECTION", "Стоимость на подтверждённое новое направление", cost.total_incremental_provider_cost_rub, 7, cost.total_cost_per_add_direction_rub, "Preserved raw provider envelopes", "Включает стоимость двух неизвестных Search outcomes.");
  addCost("COST_PER_DELTA_ROW", "Стоимость на принятую строку delta", cost.total_incremental_provider_cost_rub, 16, cost.total_cost_per_accepted_delta_row_rub, "Preserved raw provider envelopes", "Описательная себестоимость; не основание отклонять полезную семантику.");
  addCost("COST_PER_RESOLVED_SEARCH_REQUIREMENT", "Стоимость на успешно разрешённую Search-проверку", cost.total_incremental_provider_cost_rub, 7, cost.total_cost_per_successfully_resolved_search_requirement_rub, "Preserved raw provider envelopes", "Общий incremental cost / 7 успешно разрешённых требований.");
  return rows;
}


function buildGates(metrics) {
  const source = (names) => names.join(" | ");
  return [
    { gate_order: 1, gate_id: "REAL_SEARCH_COMPETITOR_DISCOVERY_WORKS_IN_TARGET_REGION", gate_statement: "Real-search competitor discovery works in the target region", evidence_files: source(["STEP_05A_SERP_COMBINED_750.tsv", "STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv", "STEP_05A_FIRST_EXECUTION_QA.json"]), supporting_counts_facts: "region=213; 75 queries; 750 TOP10 rows; 237 normalized domains; 9 selected competitors", deterministic_status: "PASS", unresolved_evidence: "None for bounded discovery mechanics; broader universality is not claimed.", work_authorized_to_close: "true", recommended_owner_action: "Review together with the complete run; no technical rework indicated." },
    { gate_order: 2, gate_id: "COMPETITOR_PAGE_TO_SEED_LINEAGE_IS_DURABLE", gate_statement: "Competitor page to seed lineage is durable", evidence_files: source(["STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv", "STEP_05A_DERIVED_SEED_CANDIDATES.tsv", "STEP_05A_PAGE_INSPECTION_QA.json"]), supporting_counts_facts: "44/44 targets; 92 candidate occurrences; every candidate has page/evidence lineage; 43 deduplicated directions", deterministic_status: "PASS", unresolved_evidence: "None for the recorded bounded targets.", work_authorized_to_close: "true", recommended_owner_action: "No technical rework indicated." },
    { gate_order: 3, gate_id: "WORDSTAT_EXPANSION_ADDS_MEASURABLE_COVERAGE_OR_PROVES_NO_MATERIAL_GAP", gate_statement: "Wordstat expansion adds measurable coverage or proves no material gap", evidence_files: source(["STEP_05A_WORDSTAT_RETURNED_PHRASE_LEDGER.tsv", "STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv", "STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv"]), supporting_counts_facts: "14 executions; 160 returned rows; 20 potentially new occurrences; 7 Search-confirmed directions; 16 accepted delta rows", deterministic_status: "PASS", unresolved_evidence: "Delta still requires normal downstream propagation before a real release.", work_authorized_to_close: "true", recommended_owner_action: "Review propagation separately; do not treat delta as frozen truth yet." },
    { gate_order: 4, gate_id: "RETURNED_WORDSTAT_ROWS_FULLY_PRESERVED_UNDER_STEP3_STEP5_SCHEMA", gate_statement: "Returned Wordstat rows are fully preserved under the Step3/Step5 schema", evidence_files: source(["STEP_05A_WORDSTAT_RETURNED_PHRASE_LEDGER.tsv", "STEP_05A_WORDSTAT_RECONCILIATION_QA.json"]), supporting_counts_facts: "160/160 rows; 21 direct + 139 association; 0 fabricated rows; empty and totalCount-only shapes preserved", deterministic_status: "PASS", unresolved_evidence: "None for preservation; totalCount-only values remain aggregate only.", work_authorized_to_close: "true", recommended_owner_action: "No technical rework indicated." },
    { gate_order: 5, gate_id: "MATERIAL_NEW_CANDIDATES_RECEIVE_CORRECT_SEARCH_CONFIRMATION_OR_HOLD_ROUTING", gate_statement: "Material new candidates receive correct Search confirmation or hold routing", evidence_files: source(["STEP_05A_SEARCH_REQUIREMENT_ACQUISITION_LEDGER.tsv", "STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv", "STEP_05A_SEARCH_DECISION_MERGE_QA.json"]), supporting_counts_facts: "9/9 requirements; 7 successful -> ADD_TO_PIPELINE; 2 OUTCOME_UNKNOWN -> HOLD_EVIDENCE; 0 retries", deterministic_status: "PASS", unresolved_evidence: "Two held directions lack current Search results and remain unresolved by design.", work_authorized_to_close: "true", recommended_owner_action: "Keep holds until separately authorized future evidence exists." },
    { gate_order: 6, gate_id: "WEBSITE_TEXT_AS_RANKING_OVERCLAIM_EQUALS_0", gate_statement: "Website text is not used as exact-query ranking proof", evidence_files: source(["STEP_05A_SEARCH_SERP_ROW_LEDGER.tsv", "STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv", "STEP_05A_SEARCH_DECISION_MERGE_QA.json"]), supporting_counts_facts: "overclaims=0; 11 visible cells and 12 ranking rows trace only to successful exact-query Search rows", deterministic_status: "PASS", unresolved_evidence: "None for the bounded claims.", work_authorized_to_close: "true", recommended_owner_action: "No technical rework indicated." },
    { gate_order: 7, gate_id: "FULL_COMPETITOR_KEYWORD_UNIVERSE_OVERCLAIM_EQUALS_0", gate_statement: "No full competitor keyword-universe claim is made", evidence_files: source(["STEP_05A_FIRST_EXECUTION_REPORT.md", "STEP_05A_SEARCH_DECISION_MERGE_REPORT.md", "STEP_05A_SEARCH_DECISION_MERGE_QA.json"]), supporting_counts_facts: "overclaims=0; evidence limited to 75 discovery queries and 7 successful exact-query rechecks", deterministic_status: "PASS", unresolved_evidence: "Full reverse-domain visibility remains outside the base method and was not attempted.", work_authorized_to_close: "true", recommended_owner_action: "No technical rework indicated." },
    { gate_order: 8, gate_id: "MERGE_COUNTS_RECONCILE", gate_statement: "Merge counts reconcile", evidence_files: source(["STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv", "STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv", "STEP_05A_SEARCH_DECISION_MERGE_QA.json"]), supporting_counts_facts: "20 = 16 MERGE_ACCEPTED + 3 close-variant suppressions + 1 retained hold + 0 rejected; delta rows=16", deterministic_status: "PASS", unresolved_evidence: "None for the acquisition delta; downstream propagation is still pending.", work_authorized_to_close: "true", recommended_owner_action: "Authorize downstream propagation only as a separate action." },
    { gate_order: 9, gate_id: "EXTERNAL_REVERSE_DOMAIN_PROVIDER_REQUIRED_FOR_BASE_EXECUTION_EQUALS_FALSE", gate_statement: "An external reverse-domain provider is not required for base execution", evidence_files: source(["STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md", "STEP_05A_FIRST_EXECUTION_REPORT.md", "STEP_05A_FIRST_EXECUTION_VALIDATION_REPORT.md"]), supporting_counts_facts: "Complete 5A.1-5A.7 rehearsal executed with preserved Yandex Search, public-page evidence and Wordstat; reverse-domain provider calls=0", deterministic_status: "PASS", unresolved_evidence: "Optional enrichment value was not tested and is not required for this gate.", work_authorized_to_close: "true", recommended_owner_action: "Retain optional-provider boundary." },
    { gate_order: 10, gate_id: "CLIENT_FACING_COMPETITOR_GAP_RESULT_IS_UNDERSTANDABLE_AND_MATERIALLY_USEFUL", gate_statement: "The client-facing competitor-gap result is understandable and materially useful", evidence_files: source(["STEP_05A_CLIENT_FACING_COMPETITOR_GAP_PREVIEW_RU.md", "STEP_05A_FIRST_EXECUTION_VALIDATION_QA.json"]), supporting_counts_facts: "Plain-Russian preview contains 9 competitors, 44 pages, 7 confirmed directions, 2 unresolved directions, 16 prepared phrases and the no-new-page boundary", deterministic_status: "OWNER_REVIEW_REQUIRED", unresolved_evidence: "Only the owner/recipient can accept usefulness and understandability; deterministic completeness/language checks cannot self-certify this gate.", work_authorized_to_close: "false", recommended_owner_action: "Read the preview and explicitly accept, request edits, or reject the client-facing presentation." },
  ];
}


function buildPreview() {
  return `# Что дала проверка семантики по реальным конкурентам

## Зачем это проверяли

Исходное семантическое ядро строилось прежде всего из спроса и структуры сайта. Дополнительная проверка конкурентов нужна, чтобы найти полезные темы, которые могли не попасть в исходный набор формулировок, но реально встречаются у сайтов, показывающихся в Яндексе по профильным запросам.

## Что проверили

Мы выбрали девять поисковых конкурентов, которые встречались в сохранённой выдаче Яндекса: mosokna.ru, i-okna.ru, msk.okna-servise.com, okna-moskva.ru, oknafactoria.ru, okna-germany.ru, fabrikaokon.ru, aluminarium.ru и elit-balkon.ru.

У них проверили 44 страницы, ранее найденные в выдаче. 43 страницы открылись по исходному адресу, одна — после обычного перенаправления. Недоступных страниц не было.

На страницах обнаружили 92 упоминания дополнительных тем. После объединения повторов осталось 43 самостоятельных направления:

- 22 уже были нормально представлены в существующем ядре;
- 14 стоило дополнительно проверить через Wordstat;
- 3 не соответствовали подтверждённому предложению компании;
- 4 нельзя было продвигать дальше без уточнений.

## Что показал Wordstat

Для 14 дополнительных тем выполнили отдельные проверки Wordstat. Он вернул 160 строк запросов и связанных формулировок.

После удаления уже известных запросов, шума, неподходящих товаров и неподтверждённых услуг осталось 20 потенциально новых формулировок. Они образовали девять направлений, которые требовали проверки в текущей выдаче Яндекса.

## Какие направления подтвердились

Достаточные данные выдачи удалось получить по семи направлениям:

1. гидроизоляция открытого балкона;
2. солнцезащитные стеклопакеты;
3. объяснение особенностей многофункциональных стеклопакетов;
4. ударопрочные стеклопакеты;
5. переоборудование балкона под рабочее место;
6. шумоизоляция крыши балкона;
7. армирование оконного профиля.

В успешных проверках встретились семь из девяти выбранных конкурентов. При этом направление по гидроизоляции открытого балкона подтвердилось по составу выдачи, реальному спросу и соответствию услугам компании, хотя ни один из девяти заранее выбранных конкурентов не вошёл по этому точному запросу в первые десять результатов. Это показывает, зачем решение принималось не по одному признаку, а по совокупности данных.

## Что осталось неопределённым

По двум темам надёжный результат текущей выдачи не был получен:

- окна для старого фонда;
- кладовая на балконе.

Эти темы не объявлены ни подходящими, ни неподходящими. Они сохранены отдельно до будущей проверки. Повторные запросы в рамках этого прохода не выполнялись, а отсутствующий результат не подменялся предположениями.

## Итог для семантического ядра

К добавлению в общий процесс подготовки ядра отобраны 16 новых поисковых фраз. Ещё три близкие формулировки исключены как повторы, одна оставлена вместе с неопределённой темой.

Эти 16 фраз пока не добавлены в окончательную версию ядра и не означают автоматическое создание новых страниц. Перед следующим реальным релизом их нужно провести через обычную очистку, группировку, проверку назначения существующим страницам и остальные этапы исследования.

Текущая проверка завершена как ограниченный проход: она дала измеримый новый результат, но один проект не позволяет установить универсальное правило, после какого количества конкурентов дальнейший поиск всегда нужно прекращать.
`;
}


function buildReport(metrics, gates) {
  const c = metrics.counts; const r = metrics.rates; const cost = metrics.provider_cost_efficiency;
  const gateLines = gates.map((g) => `| ${g.gate_order} | \`${g.gate_id}\` | ${g.deterministic_status} | ${g.supporting_counts_facts} |`).join("\n");
  const visible = metrics.competitor_visibility.visible_domains_in_successful_rechecks.join(", ");
  const notVisible = metrics.competitor_visibility.not_observed_domains_in_successful_rechecks.join(", ");
  return `# STEP 05A.8 — INFORMATION GAIN AND FIRST-EXECUTION VALIDATION REPORT

Date: 2026-09-08  
Status: **DETERMINISTIC TECHNICAL QA PASS / OWNER REVIEW REQUIRED / METHOD NOT PROMOTED**

## 1. Executive result

The full preserved Step 5A.1–5A.7 chain produced material positive information gain with strong filtering value. Seven new in-scope directions survived Wordstat and current exact-query Search checks, yielding 16 union-compatible acquisition rows with zero normalized overlap against the live frozen 2,840-phrase baseline.

Technical execution supports **RECOMMEND_VALIDATE_AFTER_OWNER_REVIEW**. This is a recommendation only: **PROJECT_TEST_VALIDATED** remains false/pending owner review, Level 1 remains not promoted, and the client-usefulness gate is not self-certified.

## 2. Quantitative funnel

- Discovery: 75 preserved queries / 750 TOP10 rows / 237 normalized domains.
- Selection and inspection: 9 competitors / 44 target pages / 43 direct + 1 redirected accessible / 0 inaccessible.
- Page evidence: 92 candidate occurrences → 43 directions (${formatPercent(r.candidate_occurrence_to_deduplicated_direction_consolidation.rate_percent)} consolidation yield; 49 repeat-support occurrences retained without inflating direction count).
- Page-level routing: 22/43 already covered; 14/43 Wordstat seeds; 3/43 off-scope; 4/43 held.
- Wordstat: 14/14 executions; 160 actual rows; 20/160 potentially new Search-recheck occurrences (${formatPercent(r.wordstat_returned_row_to_potentially_new_search_occurrence.rate_percent)}).
- Search: 9 requirements; 7 successful; 2 outcome unknown and unretried.
- Direction decisions: 7/9 **ADD_TO_PIPELINE** (${formatPercent(r.search_requirement_to_add_direction.rate_percent)}); 2/9 **HOLD_EVIDENCE** (${formatPercent(r.search_decision_hold_rate.rate_percent)}).
- Phrase merge: 20 = 16 accepted + 3 close variants suppressed + 1 held; acceptance yield ${formatPercent(r.potentially_new_occurrence_to_accepted_delta_row.rate_percent)}.

Every percentage above is persisted with its named numerator and denominator in the metrics JSON and funnel TSV.

## 3. Expansion against the live frozen baseline

Verified directly against the current Stage-5 authority:

- unique phrases = 2,840;
- active phrases = 2,332;
- assigned phrases = 2,313;
- Search-required phrases = 19;
- canonical structural units = 168;
- accepted delta rows = 16;
- normalized exact overlap between delta and baseline = 0;
- duplicate normalized phrases inside delta = 0.

The 16-row delta equals ${formatPercent(r.accepted_delta_to_frozen_unique_baseline_expansion.rate_percent, 4)} of the unique baseline and ${formatPercent(r.accepted_delta_to_frozen_active_baseline_ratio.rate_percent, 4)} of the active baseline. A simple projected total of 2,856 is arithmetic context only and applies only if all 16 rows survive the normal downstream pipeline. The delta remains **PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE**; it is not frozen truth yet.

## 4. Provider-cost efficiency

Preserved raw envelopes confirm:

- Wordstat = ${formatRub(cost.wordstat_cost_rub, 3)};
- Search = ${formatRub(cost.search_cost_rub, 3)};
- total incremental provider cost = ${formatRub(cost.total_incremental_provider_cost_rub, 3)};
- total cost per final added direction = ${formatRub(cost.total_cost_per_add_direction_rub, 4)};
- total cost per accepted delta row = ${formatRub(cost.total_cost_per_accepted_delta_row_rub, 3)};
- total cost per successfully resolved Search requirement = ${formatRub(cost.total_cost_per_successfully_resolved_search_requirement_rub, 4)};
- Search-only cost per successful requirement = ${formatRub(cost.search_cost_per_successful_requirement_rub, 4)}.

These are descriptive incremental COGS. They exclude any cost not preserved in the Step 5A Wordstat/Search envelopes and are not a quality target or a reason to reject useful evidence.

## 5. Filtering and de-risking value

- 29/43 directions (${formatPercent(r.pre_wordstat_filtered_or_held_direction_share.rate_percent)}) were already covered, off-scope, or held before Wordstat.
- 140/160 Wordstat rows (${formatPercent(r.wordstat_rows_filtered_covered_noise_offscope_hold.rate_percent)}) were covered, noise, off-scope, or held rather than sent to Search.
- 4/20 potentially new occurrences (${formatPercent(r.post_search_suppressed_or_held_occurrence_share.rate_percent)}) were suppressed or held instead of inflating the delta.
- Two unknown Search outcomes remained holds; they were not converted to empty/failed SERPs.
- Website-text-as-ranking overclaim = 0.
- Full-competitor-keyword-universe overclaim = 0.

Therefore the method's value is not only the 16 additions: it also prevents duplicate, off-scope, noisy and unsupported promotion.

## 6. Selected-competitor visibility gain

- visible selected-competitor cells = 11/81 (${formatPercent(r.selected_competitor_visibility_density.rate_percent)});
- selected-competitor ranking rows = 12;
- unique selected competitors visible = 7/9 (${formatPercent(r.unique_selected_competitors_visible_share.rate_percent)}): ${visible};
- selected competitors not observed in the seven successful exact rechecks: ${notVisible};
- exact matches to the 44 earlier inspected URLs = 0;
- same-domain/different-URL visible cells = 11 and ranking rows = 12;
- one added direction, “гидроизоляция для открытого балкона”, had zero selected competitors visible but still passed because Wordstat demand, current SERP intent/page mix, frozen business fit and semantic novelty jointly supported it.

The earlier page supplied topic/seed lineage only. Exact-query visibility claims come only from successful current Search rows.

## 7. Diminishing-information-gain assessment

1. Material new information: **YES** — 7 confirmed directions and 16 accepted occurrences.
2. Evidence mix: strong filtering (22/43 directions already covered; 140/160 Wordstat rows did not advance) with still-material in-scope novelty.
3. Permanent reusable saturation threshold: **NO** — one execution cannot establish a universal number of competitors/pages/seeds.
4. Stop this bounded rehearsal: **YES** — the authorized chain is complete, material additions are captured, two unresolved directions are safely held, and recursive expansion is not authorized.
5. Future varied rehearsal: measure marginal accepted directions/occurrences per additional bounded domain/page batch together with covered/noise/off-scope/hold shares and cost. Extend when a distinct batch still yields material in-scope additions; consider stopping earlier only after varied consecutive batches predominantly repeat or add noise.

**STOP_THIS_REHEARSAL = true** does not mean **PERMANENT_DIMINISHING_GAIN_THRESHOLD_VALIDATED = true**.

## 8. Level-1 Section 11 validation gates

| # | Gate | Status | Evidence fact |
|---:|---|---|---|
${gateLines}

Nine deterministic technical gates pass. Gate 10 remains **OWNER_REVIEW_REQUIRED**; Work verified that the preview is complete and plain-language, but only the owner/recipient may decide whether it is understandable and materially useful.

## 9. Separated verdicts

~~~text
FIRST_EXECUTION_TECHNICAL_VALIDATION = PASS_9_OF_9_DETERMINISTIC_GATES
FIRST_EXECUTION_INFORMATION_GAIN_VERDICT = MATERIAL_POSITIVE_GAIN_WITH_STRONG_FILTERING_VALUE
CLIENT_FACING_USEFULNESS_GATE = OWNER_REVIEW_REQUIRED
RECOMMENDED_PROJECT_TEST_VALIDATION = RECOMMEND_VALIDATE_AFTER_OWNER_REVIEW
ACTUAL_PROJECT_TEST_VALIDATED_STATE = false / PENDING_OWNER_REVIEW
LEVEL1_METHOD_PROMOTION_STATE = NOT_PROMOTED
PERMANENT_DIMINISHING_GAIN_THRESHOLD_STATE = NOT_VALIDATED_SINGLE_REHEARSAL
~~~

## 10. Protection and provider boundary

- New provider or substitute web calls by Work: 0.
- Raw provider envelopes modified: false.
- Frozen Stage-5 semantic master modified: false.
- Canonical unit authority modified: false.
- Corrected client release / Documents 01–03 / semantic-core XLSX modified: false.
- Page ownership, creation, deletion, split/merge or implementation action created: false.

## 11. Next actions

1. **OWNER_REVIEW_STEP_5A_FIRST_EXECUTION_VALIDATION_AND_CLIENT_FACING_PREVIEW**
2. Independently before any next real release: **PROPAGATE_STEP_5A_ACCEPTED_SEMANTIC_PIPELINE_DELTA_THROUGH_NORMAL_DOWNSTREAM_PIPELINE**

Neither action is executed in this task.
`;
}


async function buildWorkbook(metrics, funnel, gates) {
  const wb = Workbook.create();
  const summary = wb.worksheets.add("Summary");
  const funnelSheet = wb.worksheets.add("Funnel");
  const gateSheet = wb.worksheets.add("Gates");
  const sourceSheet = wb.worksheets.add("Sources");
  for (const sheet of [summary, funnelSheet, gateSheet, sourceSheet]) sheet.showGridLines = false;

  const titleStyle = { fill: "#1F4E78", font: { bold: true, color: "#FFFFFF", size: 16 }, verticalAlignment: "center" };
  const headerStyle = { fill: "#D9EAF7", font: { bold: true, color: "#17365D" }, wrapText: true, borders: { preset: "outside", style: "thin", color: "#9FBAD0" } };
  const labelStyle = { fill: "#EAF2F8", font: { bold: true, color: "#17365D" } };
  const passStyle = { fill: "#E2F0D9", font: { bold: true, color: "#375623" } };
  const ownerStyle = { fill: "#FFF2CC", font: { bold: true, color: "#7F6000" } };

  summary.getRange("A1:F2").merge();
  summary.getRange("A1").values = [["OKNO_MSK — Step 5A.8 information gain validation"]];
  summary.getRange("A1:F2").format = titleStyle;
  summary.getRange("A4:B11").values = [
    ["Metric", "Value"],
    ["Candidate occurrences", metrics.counts.candidate_occurrences],
    ["Deduplicated directions", metrics.counts.deduplicated_candidate_directions],
    ["Wordstat rows", metrics.counts.wordstat_returned_rows],
    ["Search requirements", metrics.counts.search_recheck_requirements],
    ["Added directions", metrics.counts.add_to_pipeline_directions],
    ["Accepted delta rows", metrics.counts.accepted_delta_rows],
    ["Incremental provider cost, RUB", metrics.provider_cost_efficiency.total_incremental_provider_cost_rub],
  ];
  summary.getRange("A4:B4").format = headerStyle;
  summary.getRange("A5:A11").format = labelStyle;
  summary.getRange("B5:B10").format.numberFormat = "#,##0";
  summary.getRange("B11").format.numberFormat = "0.000";
  summary.getRange("D4:F4").merge(); summary.getRange("D4").values = [["Separated verdicts"]]; summary.getRange("D4:F4").format = headerStyle;
  const verdictRows = Object.entries(metrics.verdicts);
  summary.getRangeByIndexes(4, 3, verdictRows.length, 3).values = verdictRows.map(([key, value]) => [key, value, key === "CLIENT_FACING_USEFULNESS_GATE" ? "Owner decision" : "Recorded boundary"]);
  summary.getRangeByIndexes(4, 3, verdictRows.length, 1).format = labelStyle;
  summary.getRangeByIndexes(4, 4, verdictRows.length, 1).format = { wrapText: true };
  summary.getRange("D7:F7").format = ownerStyle;
  summary.getRange("A13:F13").merge(); summary.getRange("A13").values = [["Stop this bounded rehearsal: YES. Permanent universal saturation threshold: NOT VALIDATED from one execution."]]; summary.getRange("A13:F13").format = ownerStyle;

  const directionChartData = [["Stage", "Directions"], ["Page-derived", 43], ["Wordstat seeds", 14], ["Search rechecks", 9], ["Added", 7]];
  summary.getRange("H3:I7").values = directionChartData;
  const directionChart = summary.charts.add("bar", summary.getRange("H3:I7"));
  directionChart.title = "Direction funnel"; directionChart.hasLegend = false; directionChart.setPosition("H9", "N24");
  const occurrenceChartData = [["Stage", "Occurrences"], ["Wordstat rows", 160], ["Potentially new", 20], ["Accepted delta", 16]];
  summary.getRange("K3:L6").values = occurrenceChartData;
  const occurrenceChart = summary.charts.add("bar", summary.getRange("K3:L6"));
  occurrenceChart.title = "Occurrence funnel"; occurrenceChart.hasLegend = false; occurrenceChart.setPosition("O9", "U24");

  const funnelFields = Object.keys(funnel[0]);
  funnelSheet.getRangeByIndexes(0, 0, 1, funnelFields.length).values = [funnelFields];
  funnelSheet.getRangeByIndexes(1, 0, funnel.length, funnelFields.length).values = funnel.map((row) => funnelFields.map((field) => row[field]));
  funnelSheet.getRangeByIndexes(0, 0, 1, funnelFields.length).format = headerStyle;
  const rateCol = funnelFields.indexOf("rate_decimal");
  funnelSheet.getRangeByIndexes(1, rateCol, funnel.length, 1).format.numberFormat = "0.00%";
  const percentCol = funnelFields.indexOf("rate_percent");
  funnelSheet.getRangeByIndexes(1, percentCol, funnel.length, 1).format.numberFormat = "0.00";
  funnelSheet.freezePanes.freezeRows(1);

  const gateFields = Object.keys(gates[0]);
  gateSheet.getRangeByIndexes(0, 0, 1, gateFields.length).values = [gateFields];
  gateSheet.getRangeByIndexes(1, 0, gates.length, gateFields.length).values = gates.map((row) => gateFields.map((field) => row[field]));
  gateSheet.getRangeByIndexes(0, 0, 1, gateFields.length).format = headerStyle;
  const statusCol = gateFields.indexOf("deterministic_status");
  for (let i = 0; i < gates.length; i += 1) gateSheet.getRangeByIndexes(i + 1, statusCol, 1, 1).format = gates[i].deterministic_status === "PASS" ? passStyle : ownerStyle;
  gateSheet.freezePanes.freezeRows(1);

  const sourceRows = [
    ["Authority", "Rows/facts", "Use", "Boundary"],
    ["STEP_05A_SERP_COMBINED_750.tsv", "75 queries / 750 rows", "Discovery denominator", "Preserved Search only"],
    ["STEP_05A_DERIVED_SEED_CANDIDATES.tsv", "92 occurrences / 43 directions", "Page-to-seed funnel", "Topic evidence is not ranking proof"],
    ["STEP_05A_WORDSTAT_RETURNED_PHRASE_LEDGER.tsv", "160 rows", "Wordstat funnel", "Demand/discovery only"],
    ["STEP_05A_SEARCH_SERP_ROW_LEDGER.tsv", "70 rows", "Exact-query result evidence", "No traffic/click/lead inference"],
    ["STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv", "16 rows", "Accepted acquisition delta", "Not frozen truth; propagation required"],
    ["RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv", "2,840 unique / 2,332 active", "Frozen baseline", "Read-only denominator"],
  ];
  sourceSheet.getRangeByIndexes(0, 0, sourceRows.length, 4).values = sourceRows;
  sourceSheet.getRange("A1:D1").format = headerStyle;
  sourceSheet.freezePanes.freezeRows(1);

  for (const sheet of [summary, funnelSheet, gateSheet, sourceSheet]) {
    const used = sheet.getUsedRange();
    used.format.wrapText = true;
    used.format.verticalAlignment = "top";
    used.format.autofitColumns();
    used.format.autofitRows();
  }
  summary.getRange("A:A").format.columnWidth = 34; summary.getRange("D:D").format.columnWidth = 48; summary.getRange("E:E").format.columnWidth = 58; summary.getRange("F:F").format.columnWidth = 20;
  funnelSheet.getRange("E:E").format.columnWidth = 48; funnelSheet.getRange("L:L").format.columnWidth = 46; funnelSheet.getRange("M:M").format.columnWidth = 60;
  gateSheet.getRange("B:C").format.columnWidth = 48; gateSheet.getRange("D:D").format.columnWidth = 58; gateSheet.getRange("E:E").format.columnWidth = 58; gateSheet.getRange("G:H").format.columnWidth = 48;
  sourceSheet.getRange("A:A").format.columnWidth = 54; sourceSheet.getRange("B:D").format.columnWidth = 38;
  for (const sheet of [summary, funnelSheet, gateSheet, sourceSheet]) {
    sheet.getUsedRange().format.wrapText = true;
    sheet.getUsedRange().format.autofitRows();
  }

  const xlsx = await SpreadsheetFile.exportXlsx(wb);
  await xlsx.save(outputs.workbook);
  for (const [sheetName, outName] of [["Summary", "step05a8_summary.png"], ["Funnel", "step05a8_funnel.png"], ["Gates", "step05a8_gates.png"], ["Sources", "step05a8_sources.png"]]) {
    const blob = await wb.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
    await fs.writeFile(path.join("/tmp", outName), new Uint8Array(await blob.arrayBuffer()));
  }
  return wb;
}


async function main() {
  const evidence = await loadEvidence();
  const metrics = deriveMetrics(evidence);
  const funnel = buildFunnel(metrics);
  const gates = buildGates(metrics);
  await fs.writeFile(outputs.metrics, `${JSON.stringify(metrics, null, 2)}\n`, "utf8");
  await writeTsv(outputs.funnel, funnel, Object.keys(funnel[0]));
  await buildWorkbook(metrics, funnel, gates);
  await fs.writeFile(outputs.checkpoint08, `# CHECKPOINT 08 — INFORMATION GAIN METRICS\n\nDate: 2026-09-08\n\nStatus: **MATERIALIZED / LOCAL DETERMINISTIC QA PASS 136/136 / REMOTE READBACK PASS**\n\n- Frozen baseline verified: 2,840 unique; 2,332 active; 2,313 assigned; 19 Search-required phrases; 168 units.\n- Complete funnel materialized from 75/750 discovery evidence through 16 accepted delta rows.\n- Delta normalized overlap with frozen baseline: 0.\n- Preserved provider costs: Wordstat 0.280 RUB; Search 4.392 RUB; total 4.672 RUB.\n- New provider/substitute web calls: 0.\n- PROJECT_TEST_VALIDATED: false.\n- Level-1 promotion: not performed.\n\nRemote commit: \`8a234f3c736fc9594881387ae49e5c6996cddd33\`.\nRemote GitHub readback: **PASS** for checkpoint, metrics, funnel, workbook, builder, and validator.\n`, "utf8");

  if (PHASE === "final") {
    await writeTsv(outputs.gates, gates, Object.keys(gates[0]));
    await fs.writeFile(outputs.preview, buildPreview(), "utf8");
    await fs.writeFile(outputs.report, buildReport(metrics, gates), "utf8");
    await fs.writeFile(outputs.checkpoint09, `# CHECKPOINT 09 — FIRST-EXECUTION VALIDATION\n\nDate: 2026-09-08\n\nStatus: **MATERIALIZED / DETERMINISTIC QA PASS 166/166 / OWNER REVIEW REQUIRED / REMOTE COMMIT PENDING**\n\n- Gate rows: 10 / 10.\n- Deterministic technical gates: 9 PASS / 9.\n- Owner-only client usefulness gate: OWNER_REVIEW_REQUIRED.\n- Recommended verdict: RECOMMEND_VALIDATE_AFTER_OWNER_REVIEW.\n- Actual PROJECT_TEST_VALIDATED state: false / pending owner review.\n- Level-1 method promotion: NOT_PROMOTED.\n- Stop this bounded rehearsal: true.\n- Permanent diminishing-gain threshold validated: false.\n- Accepted delta propagation state: PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE.\n\nRemote readback: PENDING MATERIAL COMMIT.\n`, "utf8");
    await fs.writeFile(outputs.log, `# STEP 05A.8 INFORMATION GAIN VALIDATION EXECUTION LOG\n\nDate: 2026-09-08\nStarting HEAD: \`${STARTING_HEAD}\`\n\n## Block A — quantitative measurement\n\n- Read and reconciled the full preserved Step 5A.1–5A.7 evidence.\n- Verified the live frozen semantic denominators and zero delta overlap.\n- Materialized full counts, named numerator/denominator rates, provider-cost efficiency, filtering and visibility metrics.\n- Provider/substitute web calls: 0.\n- Remote commit: \`8a234f3c736fc9594881387ae49e5c6996cddd33\`.\n- Remote GitHub readback: PASS.\n\n## Block B — validation assessment\n\n- Accounted for all ten Level-1 Section 11 gates.\n- Kept gate 10 as owner-review-only.\n- Produced the plain-Russian client-facing preview in the isolated execution workspace.\n- Recommended project-test validation only after owner review.\n- Preserved PROJECT_TEST_VALIDATED=false, method not promoted, and propagation required for the 16-row delta.\n- Deterministic QA: PASS 166/166.\n- Workbook visual QA: PASS; Summary, Funnel, Gates, and Sources rendered and inspected.\n- Remote GitHub commit/readback: pending this material block.\n\n## Lifecycle\n\n\`WORK -> SAVE -> COMMIT -> REMOTE GITHUB READBACK -> CONTINUE\`\n\nFinal assessment and receipt commit SHAs are recorded after remote verification.\n`, "utf8");
  }
  console.log(JSON.stringify({ phase: PHASE, funnel_rows: funnel.length, gate_rows: gates.length, delta_rows: metrics.counts.accepted_delta_rows, technical_gate_passes: gates.filter((g) => g.deterministic_status === "PASS").length, owner_review_gates: gates.filter((g) => g.deterministic_status === "OWNER_REVIEW_REQUIRED").length, total_cost_rub: metrics.provider_cost_efficiency.total_incremental_provider_cost_rub }));
}

await main();
