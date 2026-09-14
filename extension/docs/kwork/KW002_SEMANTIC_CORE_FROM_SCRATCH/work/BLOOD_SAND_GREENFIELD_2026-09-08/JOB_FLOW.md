# KW-002 Blood & Sand — JOB FLOW

Status: **STEP04 W09 ACCEPTED / STEP05 COMPLETE / STEP06 PREPARATION + RUNTIME RECONCILIATION PASS / FIRST QUERY RELEASE PENDING / ACTUAL STEP06 NOT STARTED**

## Whole-job goal

```text
semantic core
→ user tasks / intent
→ Yandex-SERP-backed clusters
→ query→page ownership
→ Search-only site architecture
→ AI-search reconciliation
→ final IA / Page Jobs / internal-link model
→ client-ready deliverables
```

Clean-boundary rule remains active: prior Blood & Sand analytical research is sealed and is not an execution input unless explicitly whitelisted.

## Current authority order

1. current `KW002_EXECUTION_CURSOR_2026-09-11.json`;
2. accepted Main ChatGPT readback/acceptance/closure files;
3. current accepted analytical artifacts;
4. current corrected prompt/gate package for the active sub-stage;
5. current `JOB_MANIFEST.md`;
6. this `JOB_FLOW.md` as human-readable roadmap/status.

Historical prompts and superseded preparation files never override current authority.

## Full roadmap / current status

| Step | Purpose | Current status |
|---|---|---|
| 00 | Freeze order/scope/source boundary | ✅ COMPLETE / PASS / Ozon-only |
| 01 | Factual business + complete assortment model | ✅ COMPLETE / PASS / 76 of 76 |
| 02 | Seed/acquisition map | ✅ COMPLETE / V2 PASS |
| 03 | Primary Wordstat acquisition + durable evidence | ✅ COMPLETE / PASS / 79 of 79 durable |
| 03A | RAW normalization + safe deduplication | ✅ COMPLETE / PASS / 24,576 identities / 25,979 RAW |
| 03B | Conservative high-confidence sanitation | ✅ CORRECTED AUTHORITY ACCEPTED / 5,100 KEEP / 13,035 HOLD / 6,441 EXCLUDE |
| 04 | Preliminary family/topic/task triage | ✅ W09 CURRENT AUTHORITY ACCEPTED |
| 05 | Targeted expansion / coverage control | ✅ COMPLETE / PASS CURRENT SNAPSHOT |
| 06 | Current Yandex organic competitor discovery | 🟠 PREPARATION + RUNTIME RECONCILIATION PASS / FIRST QUERY RELEASE PENDING / EXECUTION NOT STARTED |
| 07 | Competitor semantic expansion | ⬜ NOT STARTED |
| 08 | Competitor-derived Wordstat expansion | ⬜ NOT STARTED |
| 09 | Candidate semantic master + reserve freeze | ⬜ NOT STARTED |
| 10 | Row-level relevance / user task / intent / priority | ⬜ NOT STARTED |
| 11 | Delivery-scope selection + Search-stage semantic freeze | ⬜ NOT STARTED |
| 12 | Current ordinary Yandex Search evidence | ⬜ NOT STARTED |
| 13 | SERP + user-task-first clustering | ⬜ NOT STARTED |
| 14 | Query→page ownership + Search-only IA | ⬜ NOT STARTED |
| 15 | AI-search diagnostic case selection | ⬜ NOT STARTED |
| 16 | AI-search evidence acquisition | ⬜ NOT STARTED |
| 17 | Search-vs-AI reconciliation | ⬜ NOT STARTED |
| 18 | Final semantic core + final IA + Page Jobs + internal links | ⬜ NOT STARTED |
| 19 | Client deliverables | ⬜ NOT STARTED |
| 20 | Final QA / recipient acceptance | ⬜ NOT STARTED |
| 21 | Revision rehearsal + productization measurement/economics | ⬜ NOT STARTED |
| 22 | Final handoff / job close | ⬜ NOT STARTED |

## Completed through Step05

```text
STEP00 = PASS / Ozon-only
STEP01 = PASS / 76 of 76
STEP02 = V2 PASS
STEP03 = PASS / 79 of 79 durable
STEP03A = PASS / 24576 identities / 25979 RAW occurrences
STEP03B = CORRECTED AUTHORITY ACCEPTED / KEEP 5100 / HOLD 13035 / EXCLUDE 6441
STEP04 = W09 CURRENT AUTHORITY ACCEPTED / 32 families / 29 observed / 13 queue rows
STEP05 = COMPLETE / PASS CURRENT SNAPSHOT
```

Step05 W10C001 was executed exactly once and returned `SUCCESS_WITH_ZERO_ROWS`: `totalCount=3`, 0 returned result rows, 0 association rows, complete durable readback, 0 new union rows. Its closure is current-snapshot-bounded.

## Step06 V1 preparation invalidation

The first Step06 preparation package was prematurely labelled PASS before the mandatory owner-facing pre-step report existed. Correction also found:

- V1 claimed 10 coverage directions while its TSV actually contained 11;
- unsupported “two ordinary result pages” wording;
- original Base64/XML was made mandatory even though current Level1 allows raw **or durable normalized** Search evidence.

V1 remains historical and is superseded for execution.

Correction authority:

`STEP_06_PREPARATION_RULE_VIOLATION_AND_CORRECTION_2026-09-12.md`

## Step06 V2 prepared state

Current query/preparation authorities retained from V2:

- `STEP_06_PRE_STEP_EXTERNAL_RESEARCH_V2_2026-09-12.md` — historical external check, now refreshed by Sep-14 authority;
- `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V2_2026-09-12.tsv` — current 22-query manifest;
- `STEP_06_PRE_EXECUTION_GATE_V2_2026-09-12.md` — historical gate, superseded where current runtime/transport/pricing differ;
- `STEP_06_PRE_STEP_QA_V2_2026-09-12.md` — historical preparation QA.

V2 query authority remains:

```text
REPRESENTATIVE_QUERY_ROWS = 22
COVERAGE_DIRECTIONS = 12
QUERY_SOURCE = accepted W09 observed representative phrases
ANALYST_INVENTED_QUERY_TEXTS = 0
```

## Step06 evidence boundary

Existing Level1 allows `raw OR durable normalized result reference` for Search evidence.

Every returned normalized result row and required provenance must be durably preserved and remotely read back before the next provider action. Summary-only, domain-only or representative sampling is forbidden.

## Sep-14 runtime/method reconciliation

Current authority:

`STEP_06_RUNTIME_RECONCILIATION_AND_METHOD_REFRESH_2026-09-14.md`

The required owner-facing disclosure was completed in the current owner chat on 2026-09-14 before provider execution. Applicable Level1/Level2/job authorities were reread and current provider documentation was freshly rechecked.

The old `installed 0.1.4 vs repository 0.1.2` blocker is superseded by reviewable, independently live-accepted YMB `0.1.6` Search capability:

```text
YMB_BRANCH = hotfix/ymb-file-delivery-p0-2026-09-14
RELEVANT_COMMIT = 6fe2d2f992b4c35fbbc37783182e9236e9f5b1a1
LIVE_ACCEPTANCE = extension/docs/SEARCH_LIVE_ACCEPTANCE_2026-09-14.md
RUNTIME_SEARCH_CONTRACT_RECONCILED = true
```

Fresh official Yandex documentation confirms current async/deferred Search operation semantics, Search request fields, region `225 = Russia`, current limits and pricing.

Material method refresh:

```text
OLD TRANSPORT = synchronous Search / historical Sep-12 plan
CURRENT TRANSPORT = deferred asynchronous Search
```

Query texts and semantic Search settings remain unchanged:

```text
SEARCH_TYPE = SEARCH_TYPE_RU
REGION = 225
PAGE = 0
GROUPS_ON_PAGE = 20
GROUP_MODE = GROUP_MODE_FLAT
DOCS_IN_GROUP = 1
SORT_MODE = SORT_MODE_BY_RELEVANCE
SORT_ORDER = DESC
FAMILY_MODE = FAMILY_MODE_MODERATE
FIX_TYPO_MODE = FIX_TYPO_MODE_OFF
RESPONSE_FORMAT = XML
```

Current deferred pricing checked 2026-09-14:

```text
DAY = 0.0305 RUB / request
NIGHT = 0.02541 RUB / request
22-query maximum if all are eventually separately authorized = 0.671 / 0.55902 RUB
```

The first provider execution is deliberately **not** released by the reconciliation itself.

## Work gate

Current Step06 unit is bounded to at most 440 normalized result rows and can be processed without sampling in ordinary chat.

```text
WORK_TRIGGER = NOT_MET
WORK_HANDOFF = NOT_REQUIRED
```

## Current hard boundary

```text
STEP05 = COMPLETE
STEP06_PRE_STEP_V1 = SUPERSEDED_FOR_EXECUTION
STEP06_V2_QUERY_MANIFEST = CURRENT
STEP06_RUNTIME_RECONCILIATION = PASS / 2026-09-14
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

## Next action

After the Sep-14 runtime/method reconciliation commit passes remote readback:

1. fetch live KW-002 HEAD again;
2. take the exact first row from the accepted V2 query manifest;
3. materialize a separate first-query deferred Search execution release;
4. remote-readback the release;
5. authorize exactly one provider submission;
6. persist and remote-readback complete returned evidence before releasing any next query.
