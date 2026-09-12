# KW-002 Blood & Sand — JOB FLOW

Status: **STEP04 W09 ACCEPTED / STEP05 COMPLETE / STEP06 PRE-STEP V2 PREPARED / ACTUAL STEP06 NOT STARTED**

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
| 06 | Current Yandex organic competitor discovery | 🟠 PRE-STEP V2 PREPARED / EXECUTION NOT STARTED / SEARCH RELEASE NOT ISSUED |
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

Current V2 artifacts:

- `STEP_06_PRE_STEP_EXTERNAL_RESEARCH_V2_2026-09-12.md`
- `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V2_2026-09-12.tsv`
- `STEP_06_PRE_EXECUTION_GATE_V2_2026-09-12.md`

Prepared plan:

```text
REPRESENTATIVE_QUERY_ROWS = 22
COVERAGE_DIRECTIONS = 12
QUERY_SOURCE = accepted W09 observed representative phrases
MODE = ordinary synchronous Yandex Web Search
SEARCH_TYPE = RU
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

The V2 plan adds the distinct `ACQUIRE_ACCESS` task family (`PSF031`) that V1 omitted.

## Step06 evidence boundary

Existing Level1 allows `raw OR durable normalized result reference` for Search evidence. Current branch Search code emits every XML `<doc>` as a result row with rank/url/domain/title/snippet/modtime and serializes the full normalized envelope.

Therefore original Base64/XML is not an automatic release blocker for Step06. The actual requirement is complete preservation/readback of every returned result row and the fields/provenance required by Step06.

## Remaining execution blocker

```text
owner-observed installed Bridge runtime = 0.1.4
current repository product version = 0.1.2
installed Search runtime/schema identity = unreconciled
```

No repository `0.1.4` source/commit was found during the corrected preparation.

Before the first paid Search request:

1. complete owner-facing Step06 pre-step disclosure in chat;
2. perform a non-provider installed-runtime/Search-schema reconciliation/handshake or sync authoritative runtime source;
3. recheck live HEAD and current official provider docs/pricing;
4. issue a separate Step06 first Search execution release;
5. execute only the released Search request(s) under the per-result durability/readback gate.

## Work gate

Current Step06 unit is bounded to at most 440 normalized rows and can be processed without sampling in ordinary chat.

```text
WORK_TRIGGER = NOT_MET
WORK_HANDOFF = NOT_REQUIRED
```

## Current hard boundary

```text
STEP05 = COMPLETE
STEP06_PRE_STEP_V1 = SUPERSEDED_FOR_EXECUTION
STEP06_PRE_STEP_V2 = PREPARED
OWNER_FACING_STEP06_DISCLOSURE = REQUIRED_BEFORE_EXECUTION
STEP06_SEARCH_EXECUTION_RELEASED = false
WORDSTAT_CALLS_ALLOWED_NOW = 0
SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
STEP06_ACTUAL_EXECUTION = NOT_STARTED
STEP07_STARTED = false
STEP08_STARTED = false
```

## Next action

Show the full required Step06 pre-step report to the owner in chat. After that, resolve only the non-provider installed-runtime/Search-schema gate. Do not make a paid Search call until a separate execution release exists.
