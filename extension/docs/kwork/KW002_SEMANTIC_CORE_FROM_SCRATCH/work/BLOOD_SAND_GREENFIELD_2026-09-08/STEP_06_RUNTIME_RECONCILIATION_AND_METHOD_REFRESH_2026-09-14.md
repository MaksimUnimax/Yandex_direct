# STEP 06 — RUNTIME RECONCILIATION AND METHOD REFRESH — 2026-09-14

Status: **PASS / OWNER DISCLOSURE COMPLETE / RUNTIME RECONCILED / EXECUTION STILL NOT RELEASED**

Job: `BLOOD_SAND_GREENFIELD_2026-09-08`  
Step: `06 — current Yandex organic competitor discovery`  
Prepared against live KW-002 branch commit: `e6f7910a2aa6be8be3c96d97761a5ff28f292f42`

## 1. Purpose

This artifact closes the non-provider gate that remained after the corrected Step06 V2 preparation.

It does **not** execute Yandex Search and does **not** release any provider request by itself.

Required order remains:

```text
owner-facing Step06 disclosure
→ current provider documentation recheck
→ current Bridge capability reconciliation
→ durable reconciliation artifact + remote readback
→ separate first-query execution release
→ only then one provider submission
```

## 2. Current roadmap state

```text
STEP00 = COMPLETE / PASS
STEP01 = COMPLETE / PASS
STEP02 = COMPLETE / V2 PASS
STEP03 = COMPLETE / PASS
STEP03A = COMPLETE / PASS
STEP03B = CORRECTED AUTHORITY ACCEPTED
STEP04 = W09 CURRENT AUTHORITY ACCEPTED
STEP05 = COMPLETE / PASS CURRENT SNAPSHOT
STEP06 = PREPARATION COMPLETE / ACTUAL SEARCH EXECUTION NOT STARTED
STEP07+ = NOT STARTED
```

Step06 still exists to identify **current Yandex Search competitors** from actual current SERP evidence across representative retained demand directions.

```text
BUSINESS RIVAL != SEARCH COMPETITOR
```

## 3. Level1 / Level2 gates reread

Applicable authorities were reread before this reconciliation, including:

- `LEVEL1/COMMON_RULES.md`;
- `LEVEL1/INHERITED_KW001_UNIVERSAL_RULES.md`;
- `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`;
- `LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md`;
- `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`;
- `LEVEL1/RESULT_QUALITY_SCORING_RULE.md`;
- `LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md`;
- `LEVEL1/WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md`;
- `LEVEL1/WORK_HANDOFF_RULE.md`;
- `LEVEL2/STEP_RULES_INDEX.md`;
- `LEVEL2/INHERITED_KW001_STEP_RULES.md`;
- current job manifest/flow/cursor/failure ledger and Step06 V2 preparation package.

The mandatory owner-facing pre-step disclosure was completed in the current owner chat on 2026-09-14 before any Step06 provider execution.

## 4. Previous blocker and why it is now resolvable

The 2026-09-12 V2 package recorded:

```text
owner-observed installed runtime = 0.1.4
repository product version = 0.1.2
runtime Search contract = UNRECONCILED
```

Since then, the Yandex Marketing Bridge Search path was materially advanced and independently live-tested as version `0.1.6` on the dedicated YMB hotfix branch.

Reviewable project-test authority:

- repository: `MaksimUnimax/Yandex_direct`;
- branch: `hotfix/ymb-file-delivery-p0-2026-09-14`;
- Search live acceptance: `extension/docs/SEARCH_LIVE_ACCEPTANCE_2026-09-14.md`;
- relevant production commit: `6fe2d2f992b4c35fbbc37783182e9236e9f5b1a1`.

That acceptance covers the async/deferred Search lifecycle materially needed by Step06, including bounded batch/submit behavior, provider-call accounting, saved-result export/persistence, duplicate-submit/duplicate-collect controls, pause/resume/cancel behavior, stale-revision protection, normalization idempotency, browser/extension persistence, and in-flight operation recovery preserving provider operation identity across extension restart.

A remaining composer/file-delivery UX imperfection is **not** treated as Search-core capability proof or as a Step06 evidence-path dependency. Step06 requires durable Search evidence, not automatic chat-file delivery.

Therefore the old `0.1.4 vs 0.1.2` mismatch is historical and no longer the current Bridge capability boundary.

```text
BRIDGE_SEARCH_CAPABILITY_SOURCE = YMB 0.1.6 LIVE ACCEPTANCE
RUNTIME_SEARCH_CONTRACT_RECONCILED = true
```

## 5. Fresh external research — checked 2026-09-14

### YS01 — Web Search API, REST: WebSearch.Search

Publisher/class: Yandex AI Studio / OFFICIAL_PROVIDER  
URL: https://aistudio.yandex.ru/ru/docs/search-api/api-ref/WebSearch/search  
Checked: 2026-09-14

Supports:

- `SEARCH_TYPE_RU`;
- query text;
- `familyMode`;
- zero-based `page` with minimum `0`;
- `fixTypoMode`;
- relevance sorting;
- `GROUP_MODE_FLAT`;
- `groupsOnPage` range `1..100`;
- `docsInGroup` range `1..3`;
- region field;
- XML/HTML response formats.

Project application: preserves the semantic request settings already prepared in Step06 V2.

Claim boundary: this documentation defines provider request semantics; it does not prove that the chosen 22 queries are analytically sufficient by itself.

### YS02 — Web Search API, REST: WebSearchAsync.Search

Publisher/class: Yandex AI Studio / OFFICIAL_PROVIDER  
URL: https://aistudio.yandex.ru/ru/docs/search-api/api-ref/WebSearchAsync/search  
Checked: 2026-09-14

Supports: deferred/asynchronous Web Search using the same material search body fields as ordinary Web Search.

Project application: permits Step06 to use the validated deferred/async Bridge transport without changing the query identity or search semantics.

Claim boundary: provider support alone does not prove Bridge implementation; Bridge capability is separately established by project live acceptance.

### YS03 — How to perform text search in deferred/asynchronous mode

Publisher/class: Yandex AI Studio / OFFICIAL_PROVIDER  
URL: https://aistudio.yandex.ru/ru/docs/search-api/operations/web-search  
Checked: 2026-09-14

Supports: asynchronous operation lifecycle, later Operation retrieval, and result body in `response.rawData` after completion.

Project application: operation identity and delayed collection must remain durable; a pending operation is not a negative Search observation and must not be blindly resubmitted.

### YS04 — Yandex Search API quotas and limits

Publisher/class: Yandex AI Studio / OFFICIAL_PROVIDER  
URL: https://aistudio.yandex.ru/ru/docs/search-api/concepts/limits  
Checked: 2026-09-14

Supports current limits including:

```text
synchronous requests/hour = 10000
synchronous requests/second = 10
deferred requests/hour = 35000
deferred requests/second = 10
deferred-result reads/second = 10
max returned results = 250
max query length = 400 characters
max query words = 40
minimum deferred processing time = 5 minutes
maximum deferred-result retention = 12 hours
```

Project application: Step06 remains a small bounded job; no throughput burst is necessary. Deferred result collection must respect delayed availability and retention.

### YS05 — Yandex Search API pricing

Publisher/class: Yandex AI Studio / OFFICIAL_PROVIDER  
URL: https://aistudio.yandex.ru/ru/docs/search-api/pricing  
Checked: 2026-09-14

Current RUB prices per 1000 requests, VAT included:

```text
day synchronous = 488 RUB
day deferred = 30.5 RUB
night synchronous = 366 RUB
night deferred = 25.41 RUB
```

Therefore per request:

```text
day synchronous = 0.488 RUB
day deferred = 0.0305 RUB
night synchronous = 0.366 RUB
night deferred = 0.02541 RUB
```

For the full 22-query Step06 ceiling, if every query is eventually authorized and executed once:

```text
day deferred maximum = 22 × 0.0305 = 0.671 RUB
night deferred maximum = 22 × 0.02541 = 0.55902 RUB
```

Project application: the Sep-12 synchronous cost plan is stale. Cost is not the only reason for the method change; deferred is selected because it is currently official and the Bridge async path is separately live-validated.

### YS06 — Search regions

Publisher/class: Yandex AI Studio / OFFICIAL_PROVIDER  
URL: https://aistudio.yandex.ru/en/docs/search-api/reference/regions  
Checked: 2026-09-14

Supports: region ID `225 = Russia`.

Project application: retained Step06 region remains `225`.

### IP01 — Ahrefs: finding competitor sites from a keyword list

Publisher/class: Ahrefs / INDUSTRY_PRACTICE  
URL: https://help.ahrefs.com/en/articles/2073915-how-can-i-find-new-competitor-websites-using-the-traffic-share-reports  
Checked: 2026-09-14

Supports: competitor discovery can start from an arbitrary keyword list and target country, then examine domains/pages appearing for those keywords.

Project application: corroborates the general analytical practice of discovering Search competitors from representative query evidence rather than owner labels.

Claim boundary: this is not a Yandex rule and does not set an automatic recurrence threshold for KW-002.

### IP02 — Semrush: discover online competitors

Publisher/class: Semrush / INDUSTRY_PRACTICE  
URL: https://www.semrush.com/kb/844-discover-competitors  
Checked: 2026-09-14

Supports: organic competitors can differ from direct business competitors and can be discovered through shared organic-search visibility.

Project application: corroborates `BUSINESS RIVAL != SEARCH COMPETITOR`.

Claim boundary: Semrush methodology does not replace current Yandex SERP evidence.

## 6. Source → method reconciliation

| Method element | Source class | Current decision | Claim boundary |
|---|---|---|---|
| Search type RU | OFFICIAL_PROVIDER | keep | no claim about analytical sufficiency |
| Region 225 | OFFICIAL_PROVIDER | keep | Russia only |
| Page 0 | OFFICIAL_PROVIDER + PROJECT_HEURISTIC | keep | first result page/discovery cutoff only |
| Flat grouping | OFFICIAL_PROVIDER + PROJECT_HEURISTIC | keep | does not prove competitor inclusion |
| groupsOnPage 20 | OFFICIAL_PROVIDER + PROJECT_HEURISTIC | keep | bounded discovery depth, not full SERP |
| docsInGroup 1 | OFFICIAL_PROVIDER + PROJECT_HEURISTIC | keep | one returned document per flat group |
| relevance sort | OFFICIAL_PROVIDER | keep | current relevance ordering only |
| moderate family mode | OFFICIAL_PROVIDER | keep | provider filtering semantics only |
| typo correction OFF | OFFICIAL_PROVIDER + PROJECT_SPECIFIC | keep | protects exact observed query identity |
| 22 V2 query texts | PROJECT_EVIDENCE | keep unchanged | discovery probes, not final keywords |
| 12 coverage directions | PROJECT_EVIDENCE | keep unchanged | preliminary coverage, not final IA |
| sync transport | stale Sep-12 job plan | superseded for execution | historical only |
| deferred async transport | OFFICIAL_PROVIDER + PROJECT_TEST_VALIDATED | use | transport choice, not semantic truth |
| per-query persistence/readback | LEVEL1 | keep hard gate | no next provider action before PASS |
| recurrence | INDUSTRY_PRACTICE + PROJECT_METHOD | evidence tier only | not automatic competitor acceptance |

## 7. Refreshed Step06 execution contract

Unchanged analytical/search settings:

```text
QUERY_ROWS = 22
COVERAGE_DIRECTIONS = 12
QUERY_SOURCE = accepted Step04 W09 observed representative phrases
ANALYST_INVENTED_QUERY_TEXTS = 0
SEARCH_TYPE = SEARCH_TYPE_RU
REGION = 225 / Russia
PAGE = 0
GROUPS_ON_PAGE = 20
GROUP_MODE = GROUP_MODE_FLAT
DOCS_IN_GROUP = 1
SORT_MODE = SORT_MODE_BY_RELEVANCE
SORT_ORDER = DESC
FAMILY_MODE = FAMILY_MODE_MODERATE
FIX_TYPO_MODE = FIX_TYPO_MODE_OFF
RESPONSE_FORMAT = XML
MAX_NORMALIZED_RESULT_ROWS = 440
```

Refreshed transport/cost:

```text
SEARCH_TRANSPORT = DEFERRED_ASYNC
MAX_PROVIDER_SUBMISSIONS_IF_FULL_STEP06_EVENTUALLY_RELEASED = 22
DAY_PRICE_PER_DEFERRED_REQUEST_RUB = 0.0305
NIGHT_PRICE_PER_DEFERRED_REQUEST_RUB = 0.02541
DAY_MAX_COST_RUB = 0.671
NIGHT_MAX_COST_RUB = 0.55902
```

This artifact **does not authorize all 22 submissions**.

The first execution release must authorize exactly one query initially.

## 8. Provider execution sequencing — hard gate

```text
release exactly one query
→ submit exactly one deferred Search operation
→ persist operation/request identity immediately
→ do not treat WAITING/PENDING as failure or zero evidence
→ collect only through the validated operation lifecycle
→ receive full normalized result envelope
→ preserve every returned normalized result row required by Step06
→ preserve request/provenance/status fields
→ publish durable evidence
→ remote readback
→ reconcile result_count / row count / required fields / operation identity
→ only then decide whether the next query may be released
```

Forbidden:

```text
22-query burst before first durability proof
blind resubmit of an accepted operation
blind automatic retry
summary-only persistence
domain-only persistence
representative-row sampling
treat pending/deferred as zero results
start Step07 from unaccepted Step06 evidence
```

## 9. Evidence boundary

For Step06 the accepted Level1 contract remains:

```text
complete durable normalized evidence + provenance
```

Original Base64/XML need not be separately duplicated as an independent mandatory artifact if the complete required normalized result set and provider provenance are durably preserved and remotely read back.

Every returned normalized result row required by Step06 must survive. No silent sampling.

## 10. Work gate

```text
MAX_NORMALIZED_RESULT_ROWS = 440
WORK_TRIGGER = NOT_MET
WORK_HANDOFF = NOT_REQUIRED
```

The current unit remains safe for complete ordinary-chat orchestration without sampling. If scale or transformation complexity changes materially, the Level1 Work gate must be re-evaluated.

## 11. Claim boundaries

```text
TOP20_DISCOVERY != FULL SERP COVERAGE
STEP06 != STEP12 FULL_SERP_COVERAGE
ONE SERP APPEARANCE != SELECTED SEARCH COMPETITOR
SEARCH COMPETITOR != DIRECT BUSINESS RIVAL
RECURRENCE != AUTOMATIC INCLUSION
PROVIDER SUCCESS != DURABLE PROJECT EVIDENCE
ASYNC OPERATION ACCEPTED != SEARCH EVIDENCE RECEIVED
```

## 12. Reconciliation verdict

```text
FRESH_EXTERNAL_RESEARCH = PASS / 2026-09-14
OWNER_FACING_SOURCE_DISCLOSURE = PASS / CURRENT CHAT
PLAIN_LANGUAGE_DISCLOSURE = PASS
BRIDGE_SEARCH_RUNTIME_CAPABILITY = RECONCILED_TO_LIVE_ACCEPTED_V0.1.6
SEARCH_METHOD_SETTINGS = RETAINED
SEARCH_TRANSPORT = CHANGED_SYNC_TO_DEFERRED_ASYNC
CURRENT_PROVIDER_PRICING_RECHECK = PASS
CURRENT_PROVIDER_LIMITS_RECHECK = PASS
RUNTIME_RECONCILIATION = PASS
WORK_TRIGGER = NOT_MET
PROVIDER_EXECUTION_RELEASED = false
SEARCH_SUBMISSIONS_ALLOWED_NOW = 0
SEARCH_COLLECTION_CALLS_ALLOWED_NOW = 0
WORDSTAT_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
STEP06_ACTUAL_EXECUTION = NOT_STARTED
STEP07_STARTED = false
STEP08_STARTED = false
```

## 13. Next physical action

After this reconciliation is committed and remotely read back from the KW-002 branch:

1. re-fetch live KW-002 HEAD;
2. materialize a **separate first-query execution release** tied to the exact first row of the accepted V2 query manifest;
3. remote-readback that release;
4. only then provide the owner the exact YMB v0.1.6 command for **one** deferred Search submission.

No provider request is authorized by this reconciliation artifact itself.
