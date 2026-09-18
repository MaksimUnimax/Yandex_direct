# KW-002 JOB MANIFEST — BLOOD_SAND_GREENFIELD_2026-09-08

Status: **STEP06 DURABLE PASS / STEP07 BROWSER RECOVERY CANONICALLY ACCEPTED / STEP07 SEMANTIC REWORK RELEASED / STEP08 BLOCKED**

## 1. Job identity

```text
KW_ID = KW-002
JOB_ID = BLOOD_SAND_GREENFIELD_2026-09-08
JOB_TYPE = PRODUCTIZATION_REHEARSAL
EXECUTION_MODE = CLEAN_FROM_SCRATCH
BUSINESS = Blood & Sand / «Кровь и Песок»
SITE = кровьипесок.рф
SITE_STATE = NEW_SITE
REGION = Russia
LANGUAGE = Russian
PRIMARY_SEARCH_ENGINE = Yandex
```

## 2. Frozen client truth

```text
Brand = «Кровь и Песок» / Blood & Sand
Business = product brand / seller
Client wording = амулеты, обереги и талисманы; в ассортименте есть в том числе товары для автомобиля
Sales channels = Ozon + Wildberries
Assortment authority = Ozon only
Primary market/search geography = Russia
New owned website planned = YES
OZON PRODUCT/LISTING ROWS = 76
WB PRODUCT/LISTING ROWS ACTIVE = 0
```

Frozen authorities:

- `CLIENT_SUPPLIED_BRIEF.md`
- `CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md`
- `CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv`
- `ALLOWED_INPUTS_AND_SEALED_SOURCES.md`

## 3. Clean-baseline boundary

```text
PRIOR BLOOD_SAND WORDSTAT/SEARCH/ALICE/COMPETITOR/CLUSTER/IA RESEARCH = SEALED / FORBIDDEN EXECUTION INPUT
```

Only explicitly allowed current-job evidence may be used.

## 4. Current accepted upstream state

```text
STEP00 = PASS / Ozon-only
STEP01 = PASS / 76 of 76
STEP02 = V2 PASS
STEP03 = PASS / 79 of 79 durable
STEP03A = PASS / 24576 identities / 25979 RAW occurrences
STEP03B = CORRECTED AUTHORITY ACCEPTED / KEEP 5100 / HOLD 13035 / EXCLUDE 6441
STEP04 = W09 CURRENT AUTHORITY ACCEPTED / 32 families / 29 observed / 13 queue rows
STEP05 = COMPLETE / PASS CURRENT RESEARCH SNAPSHOT
STEP06 = PREPARATION + RUNTIME RECONCILIATION PASS / EXECUTION NOT STARTED
```

## 5. Step05 final closure

W10C001 was the sole new Step05 provider candidate and was executed exactly once:

```text
candidate_id = W10C001
phrase = (амулет|оберег|талисман) Аум
request_id = wordstat-b3fbe6dd-121b-4e67-81ca-0b03bdc53358
http_status = 200
provider_status = OK
totalCount = 3
results_rows = 0
association_rows = 0
outcome = SUCCESS_WITH_ZERO_ROWS
raw_remote_readback = PASS
new_union_rows = 0
```

Bounded interpretation remains current-snapshot only. `totalCount=3` is not three returned keyword rows and zero returned rows is not universal zero demand.

Step05 closure authority:

`STEP_05_W10_V3_FINAL_CLOSURE_2026-09-12.md`

## 6. Step06 preparation correction

The first Step06 preparation package was prematurely called PASS before the mandatory owner-facing pre-step report existed and contained additional defects. It remains historical and is superseded for execution.

Correction authority:

`STEP_06_PREPARATION_RULE_VIOLATION_AND_CORRECTION_2026-09-12.md`

Historical V1 files, not execution authority:

- `STEP_06_PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_TRACE_2026-09-12.md`
- `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V1_2026-09-12.tsv`
- `STEP_06_PREPARATION_GATE_2026-09-12.md`

Corrected V2 preparation package:

- `STEP_06_PRE_STEP_EXTERNAL_RESEARCH_V2_2026-09-12.md`
- `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V2_2026-09-12.tsv`
- `STEP_06_PRE_EXECUTION_GATE_V2_2026-09-12.md`
- `STEP_06_PRE_STEP_QA_V2_2026-09-12.md`

## 7. Historical Step06 V2 acquisition design at 2026-09-12

The Sep-12 preparation used synchronous Search as its then-current transport plan:

```text
QUERY_ROWS = 22
COVERAGE_DIRECTIONS = 12
QUERY_SOURCE = accepted Step04 W09 observed representative phrases
SEARCH_MODE = ordinary synchronous Yandex Web Search
SEARCH_TYPE = SEARCH_TYPE_RU
REGION = 225 / Russia
PAGE = 0
GROUPS_ON_PAGE = 20
GROUP_MODE = FLAT
FIX_TYPO = OFF
MAX_NORMALIZED_RESULT_ROWS = 440
DAY_MAX_ESTIMATED_COST = 10.736 RUB
NIGHT_MAX_ESTIMATED_COST = 8.052 RUB
GENSEARCH = 0
WORDSTAT = 0
```

This section is retained as historical preparation truth. Its sync transport/pricing/runtime-blocker state is superseded for current execution by Section 13 below.

Step06 queries remain discovery probes, not final keywords, final intents, final clusters or pages.

## 8. Step06 evidence persistence contract

Existing Level1 permits raw **or durable normalized** Search result references.

For Step06, every returned normalized document row and required provenance must be durably preserved and remotely read back before the next provider action. A summary, domain-only list or representative sample is insufficient.

Original provider Base64/XML is not separately required by the current Step06 method if complete required normalized evidence is preserved with provenance.

## 9. Historical Bridge blocker at 2026-09-12

The corrected V2 package recorded an unreconciled `0.1.4` installed runtime against `0.1.2` repository product source and therefore correctly allowed zero Search calls at that time.

That blocker is historical. It is formally superseded by the 2026-09-14 reconciliation in Section 13.

## 10. Work gate

Current Step06 plan is bounded to at most 440 normalized result rows and does not require sampling or truncation in ordinary chat.

```text
WORK_TRIGGER = NOT_MET
WORK_HANDOFF = NOT_REQUIRED
```

If scale later changes materially, re-evaluate under `LEVEL1/WORK_HANDOFF_RULE.md`.

## 11. Historical hard boundary at Sep-12 cursor write

The prior cursor correctly recorded zero Search authorization before owner disclosure/runtime reconciliation. It remains historical and must not be read as the current post-reconciliation state.

## 12. Historical next action at Sep-12 cursor write

The prior required action was owner-facing disclosure → runtime reconciliation → live-head/provider recheck → separate first Search release. The first three preparation/reconciliation prerequisites are now completed in Section 13; the separate first-query release still remains pending.

## 13. Current Step06 authority refresh — 2026-09-14

Current reconciliation authority:

`STEP_06_RUNTIME_RECONCILIATION_AND_METHOD_REFRESH_2026-09-14.md`

Before any Step06 provider execution, the current workflow:

- reread applicable Level1/Level2/job authorities;
- completed the mandatory owner-facing Step06 disclosure in the current chat;
- performed fresh Internet research against current official Yandex Search API documentation;
- rechecked current limits, regions, async semantics and pricing;
- reconciled Bridge Search capability against the independently live-accepted YMB `0.1.6` async Search path;
- preserved the accepted 22 V2 query texts and 12 coverage directions unchanged;
- changed only the current provider transport from the stale Sep-12 synchronous plan to current deferred/asynchronous Search.

Current Search contract:

```text
QUERY_ROWS = 22
COVERAGE_DIRECTIONS = 12
ANALYST_INVENTED_QUERY_TEXTS = 0
SEARCH_TRANSPORT = DEFERRED_ASYNC
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
DAY_DEFERRED_PRICE_PER_REQUEST = 0.0305 RUB
NIGHT_DEFERRED_PRICE_PER_REQUEST = 0.02541 RUB
DAY_MAX_IF_ALL_22_EVENTUALLY_RELEASED = 0.671 RUB
NIGHT_MAX_IF_ALL_22_EVENTUALLY_RELEASED = 0.55902 RUB
```

Current Bridge capability authority:

```text
YMB_VERSION = 0.1.6 live-accepted Search path
BRANCH = hotfix/ymb-file-delivery-p0-2026-09-14
RELEVANT_COMMIT = 6fe2d2f992b4c35fbbc37783182e9236e9f5b1a1
LIVE_ACCEPTANCE = extension/docs/SEARCH_LIVE_ACCEPTANCE_2026-09-14.md
RUNTIME_SEARCH_CONTRACT_RECONCILED = true
```

The first execution must still be exactly one released query followed by durable persistence, remote readback and reconciliation before any next provider action.

Current hard boundary:

```text
STEP05 = COMPLETE
STEP06_PRE_STEP_V1 = SUPERSEDED_FOR_EXECUTION
STEP06_PRE_STEP_V2 = PREPARED / QUERY MANIFEST STILL CURRENT
STEP06_RUNTIME_RECONCILIATION = PASS
OWNER_FACING_STEP06_DISCLOSURE = PASS / 2026-09-14
STEP06_FIRST_QUERY_EXECUTION_RELEASED = false
DEFERRED_SEARCH_SUBMISSIONS_ALLOWED_NOW = 0
DEFERRED_SEARCH_COLLECTION_CALLS_ALLOWED_NOW = 0
SYNCHRONOUS_SEARCH_CALLS_ALLOWED_NOW = 0
WORDSTAT_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
STEP06_ACTUAL_EXECUTION = NOT_STARTED
STEP07_STARTED = false
STEP08_STARTED = false
```

## 14. Current next action

After remote readback of the reconciliation commit:

1. re-fetch current live KW-002 HEAD;
2. read the exact first row from `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V2_2026-09-12.tsv`;
3. materialize a separate first-query deferred Search execution release;
4. remote-readback that release;
5. only then authorize exactly one provider submission;
6. persist and remote-readback the complete returned evidence before any second query is released.


## 15. Current Step07 authority refresh — 2026-09-18

This section supersedes older current-status statements in this manifest; historical execution sections remain provenance.

```text
STEP06 = DURABLE_PASS
STEP07_ATTEMPT_1 = REJECTED_REWORK_REQUIRED
STEP07_BROWSER_RECOVERY = CANONICAL_REMOTE_ACCEPTED
BROWSER_RECOVERY_OWNER_UPLOAD_HEAD = 599af13c5007e1c2482e89a63f5d9ff4d9af3491
BROWSER_RECOVERY_REMOTE_BYTE_IDENTITY = 7/7 PASS
BROWSER_RECOVERY_SOURCE_URL_ROWS = 1976
BROWSER_RECOVERY_PAGE_EVIDENCE_ROWS = 725
BROWSER_RECOVERY_AUTHORIZED_COMPETITORS = 32
STEP07_SEMANTIC_REWORK = RELEASED_FOR_CHATGPT_WORK_NOT_EXECUTED
CURRENT_REWORK_PROMPT = STEP07_REWORK_WORK_PROMPT_2026-09-17.md
CURRENT_REWORK_PROMPT_BLOB = dfb5d67382438256532da873ac023c43d9100a38
CURRENT_REWORK_RELEASE = STEP07_SEMANTIC_REWORK_EXECUTION_RELEASE_2026-09-18.md
STEP08 = BLOCKED_NOT_STARTED
WORDSTAT_CALLS_ALLOWED_NOW = 0
YANDEX_SEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
```
