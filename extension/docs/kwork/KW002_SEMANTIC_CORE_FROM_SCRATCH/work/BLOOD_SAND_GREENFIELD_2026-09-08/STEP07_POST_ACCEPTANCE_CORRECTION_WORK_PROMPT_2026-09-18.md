# KW-002 / BLOOD & SAND — STEP07 POST-ACCEPTANCE FULL-VOLUME CORRECTION — CHATGPT WORK EXECUTION PROMPT

WORK_ID: `KW002_STEP07_POST_ACCEPTANCE_CORRECTION_2026-09-18`

CONTINUE THE EXISTING KW-002 BLOOD & SAND GREENFIELD SEMANTIC-CORE REHEARSAL.

THIS IS AN EXECUTION TASK.
THIS IS NOT A NEW PROJECT.
THIS IS NOT STEP08.
THIS IS NOT A NEW METHODOLOGY AUDIT.

Repository: `MaksimUnimax/Yandex_direct`
Branch: `roadmap/kwork-productization-2026-08-28`
Job root: `extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

## 0. First action — narrow technical preflight

Fetch the current remote branch.

Release data base:
`dcc115db6f18f69f03831d60a1ce7e87154139cf`

The live HEAD may be later only because Main Chat published this Work release and current-state control files after the release data base.
Verify that the exact input files named in the pre-handoff manifest still have the frozen Git blob identities.

Read and obey exactly:

- `STEP07_POST_ACCEPTANCE_CORRECTION_PRE_HANDOFF_MANIFEST_2026-09-18.json`
- `STEP_07_OUTPUT_SCHEMA_CONTRACT.json`
- `STEP_07_OUTPUT_SCHEMA_CONTRACT_R2_2026-09-18.json`
- `STEP07_POST_ACCEPTANCE_METHOD_AND_COVERAGE_DEFECT_RECORD_2026-09-18.md`

Do not rerun Main Chat methodology research and do not rebuild the roadmap.

If any frozen data input blob changed materially, stop with `AUTHORITY_DRIFT` and name the exact file/blob conflict.

## 1. Full-volume rule

```text
LARGE DATA != SAMPLE IT
LARGE DATA != TRUNCATE IT
LARGE DATA != SUMMARIZE BEFORE ANALYSIS

PROCESS THE COMPLETE BOUNDED EXECUTION UNIT
```

Required bounded page universe:

```text
SOURCE_URL_ROWS = 1976
AUTHORIZED_COMPETITORS = 32
```

Known pre-correction candidate state:

```text
CANDIDATE_IDENTITIES = 2172
PAGE_PROVENANCE_ROWS = 3948
STEP08_ELIGIBLE = 794
```

These are starting counts, not required final counts.

## 2. Correction unit A — access-state evidence truth

Load in full:

- `STEP07_SOURCE_URL_LEDGER.csv`
- `STEP07_COMPETITOR_COVERAGE_LEDGER.csv`
- `STEP07_BROWSER_RECOVERY_URL_LEDGER.csv`
- `STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl`
- `STEP07_BROWSER_RECOVERY_COVERAGE.csv`
- `STEP07_BROWSER_RECOVERY_QA.md`

Revalidate **1976/1976** source URL terminal states against the available canonical browser/page evidence.

Hard semantic rule:

```text
INSPECTED_CANDIDATE_YIELD
or
INSPECTED_NO_CANDIDATE
=> substantive target-page content must actually be present in stored evidence
```

Browser/network/VPN/CAPTCHA/access-denied/error/loading shells are not target semantic content.
They must map to the applicable inaccessible/error/unresolved state.

Known regression expectation:

- the current `S07A002 / ozon.ru` summary says `26 INSPECTED_NO_CANDIDATE`, `0 inaccessible`, `1 redirected`, `COMPLETE`;
- independent Main Chat audit found that the current 27 Ozon page-evidence records carry target block/error content rather than substantive Ozon semantic page content.

Do not patch only those 27 rows.
Treat Ozon as a regression test for a **full 1976-row access-state content validation**.

Do not perform new Ozon browser acquisition merely to prove this already-recorded defect.
Do not bypass any restriction.

Recompute the complete 32-row `STEP07_COMPETITOR_COVERAGE_LEDGER.csv` from corrected terminal truth.

## 3. Correction unit B — mandatory organic ranking-query discovery lane

The old Step07 page-mining corpus is preserved.
Add the missing second discovery lane.

For every authorized competitor, account for current Yandex-oriented organic ranking-query evidence under the source policy frozen in the manifest.

Preferred source:

`Keys.so` Yandex organic competitor query/page data, if legitimately accessible in the Work environment.

Allowed alternative:

a current source that explicitly provides **Yandex organic competitor query-to-domain/URL evidence** with identifiable source/snapshot/provenance.

Not allowed:

- Google-only keyword portfolios represented as Yandex evidence;
- invented ranking queries inferred from competitor page text;
- Wordstat;
- Yandex Marketing Bridge Search;
- AI-search / GenSearch;
- credentials/CAPTCHA/paywall/anti-bot bypass.

If no legitimate approved source can provide the required data, stop the Step07 PASS path with:

`BLOCKED_RANKING_QUERY_SOURCE_REQUIRED`

Materialize the partial valid correction artifacts already completed, clearly mark the ranking-query lane blocked, and do not start Step08.

### Ranking-query evidence

Persist every acquired observation into:

`STEP07_RANKING_QUERY_LEDGER.csv`

using the R2 schema exactly.

Raw query wording is immutable.
A ranking query is discovery evidence only:

```text
COMPETITOR_RANKING_QUERY != PROVEN_DEMAND
```

## 4. Reconciliation across both lanes

Reconcile all page-derived and ranking-query-derived candidate identities against:

- current Step07 candidate authority;
- accepted upstream identity universe already used by Step07;
- current reconciliation rules.

Do not merge morphology/synonyms as exact duplicates.
Do not infer demand.
Do not perform final intent, clustering, page architecture, URL/H1/Title or final query→page decisions.

Any genuinely new ranking-query-derived candidate may become:

- `NEW_CANDIDATE`; or
- eligible `POSSIBLE_VARIANT`;

but remains `NOT_VALIDATED_STEP07` and is only queued for future Step08 after Main Chat acceptance.

Recompute `COMPETITOR_GAP_CANDIDATES.csv` under the R2 schema semantics.
`provenance_row_count`, `competitor_source_count` and `source_url_count` must account for both page evidence and ranking-query evidence exactly as defined by the amendment.

Do not rewrite immutable existing page provenance.
Only replace `STEP07_CANDIDATE_PROVENANCE_LEDGER.csv` if deterministic metadata/foreign-key changes are actually required; otherwise preserve byte identity and record that fact.

## 5. Discovery-channel coverage

Create exactly 32 rows in:

`STEP07_DISCOVERY_CHANNEL_COVERAGE.csv`

Each authorized competitor must have explicit:

- page-surface lane status;
- ranking-query lane status;
- ranking-query source/snapshot;
- observation count;
- unique query count;
- candidate count;
- limitation reason;
- overall Step07 discovery status.

Silence is not a coverage state.

Source concentration diagnostics must be reported:

- discovered URL concentration by competitor;
- Step08-eligible candidate source-count bands;
- ranking-query source coverage by competitor;
- single-source vs multi-source final candidate counts.

These are confidence/recall diagnostics, not automatic acceptance/rejection rules.

## 6. Required outputs

Materialize the exact output set from the pre-handoff manifest:

1. `STEP07_SOURCE_URL_LEDGER.csv` — REPLACE
2. `STEP07_COMPETITOR_COVERAGE_LEDGER.csv` — REPLACE
3. `STEP07_RANKING_QUERY_LEDGER.csv` — NEW
4. `STEP07_DISCOVERY_CHANNEL_COVERAGE.csv` — NEW
5. `COMPETITOR_GAP_CANDIDATES.csv` — REPLACE
6. `STEP07_CANDIDATE_PROVENANCE_LEDGER.csv` — REPLACE only if required, otherwise handoff the unchanged authoritative file with unchanged hash
7. `STEP07_EXECUTION_QA.md` — REPLACE
8. `STEP07_EXECUTION_HANDOFF_MANIFEST.json` — REPLACE

## 7. Hard QA

PASS requires all applicable gates:

```text
SOURCE_URL_ROWS_REVALIDATED = 1976/1976
SILENT_SKIP = 0
AUTHORIZED_COMPETITORS_ACCOUNTED = 32/32
EVERY_INSPECTED_STATE_HAS_TARGET_CONTENT_EVIDENCE = true
BLOCK_OR_ERROR_EVIDENCE_MISCLASSIFIED_AS_INSPECTED = 0
OZON_ACCESS_STATE_DEFECT_CLOSED = true
DISCOVERY_CHANNEL_COVERAGE_ROWS = 32/32
RANKING_QUERY_LANE_REQUIRED = true
RANKING_QUERY_RAW_EVIDENCE_IMMUTABLE = true
CANDIDATE_RECONCILIATION_ACROSS_BOTH_LANES = PASS
PAGE_RAW_EVIDENCE_MUTATIONS = 0
WORDSTAT_CALLS = 0
YMB_SEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
GENSEARCH_CALLS = 0
STEP08_STARTED = false
OPEN_CRITICAL_DEFECTS = 0
```

If the ranking-query source is unavailable or materially incomplete for required competitors, overall Step07 is not PASS.
Report the exact blocked/limited state rather than forcing completeness.

## 8. Handoff / publication

Do not commit/push the large corrected artifacts directly to canonical final paths.

Package all required handoff files into one transport ZIP.
ZIP is transport only and must not be committed.

Use the staging target frozen in:
`STEP07_POST_ACCEPTANCE_CORRECTION_PRE_HANDOFF_MANIFEST_2026-09-18.json`

The owner performs one staging upload.
Main Chat then owns final placement, remote readback, return QA, state/cursor update and acceptance.

## 9. Stop boundary

Stop after the complete Step07 correction artifact set and local QA/handoff package are materialized.

Do not start Step08.
