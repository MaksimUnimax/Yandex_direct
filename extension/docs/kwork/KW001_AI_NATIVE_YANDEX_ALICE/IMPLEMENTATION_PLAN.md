# KW-001 — AI-Native Semantic Rebuild: implementation plan

Date: 2026-08-28
Status: **ACTIVE / COMMERCIAL END-TO-END REHEARSAL REQUIRED**

## 1. Working Kwork

Title:

`Пересоберу семантику сайта под Яндекс и Алису AI — обычный + генеративный поиск`

Initial test price:

`7,500 RUB`

Initial delivery target:

`4–5 days`

This price/scope is provisional until the complete rehearsal measures real work time and provider cost.

## 2. What is already proven

Technical/methodological evidence already exists:

```text
O-001 comparative methodology gate = PASS
consumer-Alice evidence produced material/de-risking deltas on blood_sand
GenSearch proxy validation = PASS
GenSearch production hand = accepted
ordinary Search = accepted
Wordstat + durable batch = accepted
Search batch/TOP evidence = accepted
```

These facts authorize productization but do not replace the commercial rehearsal.

## 3. Base-package promise to test

The base package must be deliverable using current accepted capabilities only:

```text
business/site understanding
human-demand evidence from Yandex Wordstat
ordinary Yandex Search evidence
selective official GenSearch evidence
semantic cleanup/grouping
Search-vs-AI user-job comparison
page-job decisions
source/competitor observations
prioritized recommendations
client workbook/report
```

Optional account evidence such as Webmaster/Metrika/Direct may be used only when actually available to a real client and must not be necessary for the base-package promise.

## 4. Explicit non-promises

The card/runbook must never promise:

```text
guaranteed Alice inclusion/citation
guaranteed AI visibility
guaranteed Yandex position
guaranteed traffic/leads/revenue
GenSearch == consumer Alice
source order == ranking
AI evidence must always change the SEO decision
```

A valid outcome may be `NO_CHANGE`: AI evidence can confirm a strong ordinary-search decision.

## 5. Test-project requirement

Before READY_TO_SELL, execute at least **two materially different test orders**.

Preferred test profiles:

### Test A — commercial catalog / product family

Must have:

```text
multiple related product/category intents
existing public pages
meaning/selection/compatibility questions where AI could plausibly differ from transactional SERP
observable Yandex demand
```

Purpose: stress commercial vs explanatory/hybrid page-job decisions.

### Test B — service or mixed information-commerce business

Must have:

```text
clear commercial conversion goal
informational questions around the service/product
existing public competitor/source landscape
observable Yandex demand
```

Purpose: prove the method is not overfit to symbols/jewelry/blood_sand.

`blood_sand` remains regression/methodology authority but does not count as both required new commercial rehearsals.

## 6. Mock-client order freeze

Before analysing each test site, create a test-order record containing:

```text
site URL
business description
region
client goal
base package purchased
known pages/categories
known exclusions
competitors supplied or NONE
requested output
assumed client questions
frozen timestamp
```

Do not alter the mock brief after seeing provider evidence merely to make the result look better. Any revision must be logged as a client revision.

## 7. Full execution sequence to rehearse

### Step 1 — intake and business model

ChatGPT maps:

```text
offer
audience
conversion jobs
regions
existing page roles
commercial exclusions
business ambiguity requiring client clarification
```

Output: `BUSINESS_MODEL.md` or equivalent test record.

### Step 2 — seed/query plan

ChatGPT creates a bounded query plan with reason for every important seed/root.

Separate at minimum:

```text
commercial roots
selection/comparison roots
meaning/how/why roots
problem/solution roots
brand/product-family roots where relevant
```

### Step 3 — Wordstat human-demand acquisition

Use current accepted Wordstat/Wordstat batch hands.

Record:

```text
exact commands/jobs
region/device
provider request count
cost estimate
raw result references
```

ChatGPT then cleans and groups evidence. Do not let Bridge make subjective relevance decisions.

### Step 4 — ordinary Yandex Search evidence

Choose decision-relevant roots/page-boundary questions.

Use ordinary Search or Search batch as appropriate.

Record:

```text
query
region
ranked URL/domain evidence
page/source types
commercial vs informational orientation
important competitors/sources
```

### Step 5 — pre-AI decision baseline

Before opening current-test GenSearch evidence, freeze a compact baseline for decision-relevant clusters:

```text
current page job
split/merge/new-page/reject hypothesis
priority reason
main uncertainty
what AI evidence could realistically change/de-risk
```

This is not required to be a scientific isolated Pass-A experiment for every paid order. It is an operational discipline so AI evidence has a traceable decision role rather than being decorative.

### Step 6 — AI test-set selection

ChatGPT selects only queries for which AI evidence could change or materially de-risk a decision.

For each selected query record:

```text
query
reason_selected
specific decision at stake
expected information gain
```

Default target for the base rehearsal: small bounded set, normally about 3–10 queries depending on project complexity. Do not bulk-run the semantic core through GenSearch.

### Step 7 — official GenSearch acquisition

Use current accepted `SEARCH_API_V1 method=genSearch` hand.

Preserve separately:

```text
GEN_SEARCH_INPUT
GEN_SEARCH_ANSWER
GEN_SEARCH_SOURCE
GEN_SEARCH_SOURCE_USED
GEN_SEARCH_QUERY_OBSERVED
```

Record request count and estimated provider cost.

### Step 8 — Search-vs-AI comparison

For each AI-tested decision classify:

```text
ordinary Search user job
AI user job
source-type difference
commercial/explanatory difference
source-worthiness implication
material decision delta = CHANGE / DE_RISK / NO_CHANGE / INSUFFICIENT
```

Do not force CHANGE.

### Step 9 — final semantic/page architecture

ChatGPT decides per cluster/page:

```text
KEEP_EXISTING
EXPAND_EXISTING
MERGE
SPLIT
NEW_COMMERCIAL_PAGE
NEW_INFORMATIONAL_PAGE
HYBRID_CONTENT_COMMERCE
FAQ_OR_SECTION_ONLY
REJECT
MANUAL_REVIEW
```

Resolve cannibalization and conflicting jobs explicitly.

### Step 10 — H/A/C/O reasoning

Keep reasons distinct:

```text
H = human demand
A = AI importance
C = commercial value
O = owned-asset/source value
```

Do not collapse into an unexplained magic score.

### Step 11 — client deliverables

The rehearsal must actually produce the intended sellable artifacts, not just describe them.

Minimum base-package artifact set:

```text
1. Semantic/page map workbook
2. Search-vs-AI gap matrix
3. Source/competitor map
4. Prioritized action plan
5. Short methodology/limitations sheet
6. Final client delivery message
```

Candidate workbook columns include:

```text
cluster/page
query/phrase
human-demand evidence
ordinary Search job
AI job
current/target page
H reason
A reason
C reason
O reason
decision
priority
confidence/review state
source notes
```

The exact schema is frozen only after the first full test run proves what is useful and not bloated.

### Step 12 — QA

Check at minimum:

```text
no invented provider facts
Wordstat region correct
Search provenance correct
GenSearch provenance correct
no GenSearch==Alice claim
no guaranteed outcomes
no orphan important cluster
no unsupported new-page recommendation
no obvious cannibalization left unresolved
deliverable files open correctly
client can understand next actions without reading raw evidence
```

### Step 13 — economics and operator burden

Measure:

```text
ChatGPT work stages / approximate effort
Wordstat requests + estimated cost
ordinary Search requests + estimated cost
GenSearch requests + estimated cost
owner/operator actions required
elapsed wall-clock constraints
revision-sensitive stages
```

Use these observations to confirm/revise `7,500 RUB` and package limits.

### Step 14 — simulated client revision

Every test must include one realistic revision, for example:

```text
client says one category is not sold
client adds a priority service/product
client rejects a proposed new page
client clarifies geography/audience
```

Re-run only affected reasoning/evidence where justified. Prove the workflow can revise without restarting the whole order or replaying paid provider work blindly.

## 8. Test evidence files

For each accepted test project create:

```text
TEST_ORDER_<id>.md
TEST_EXECUTION_<id>.md
TEST_DELIVERABLE_INDEX_<id>.md
TEST_ECONOMICS_<id>.md
TEST_REVISION_<id>.md
```

Never store credentials/secrets.

## 9. Card finalization after tests

Only after accepted test runs freeze:

```text
final Kwork title
final description
exact base-package limits
exact required client inputs
final delivery time
final base price
add-on menu
portfolio/demo screenshots/artifacts
FAQ
non-guarantee language
```

Marketing copy must be derived from observed workflow truth.

## 10. Final autonomous runbook

After the execution logic is stable, create:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/RUNBOOK_FOR_CHATGPT.md`

It must satisfy `extension/docs/KWORK_RUNBOOK_STANDARD_2026-08-28.md` and pass a clean-context rehearsal.

## 11. KW-001 acceptance markers

```text
KW001_TEST_A_END_TO_END_PASS
KW001_TEST_B_END_TO_END_PASS
KW001_DELIVERABLE_SET_PASS
KW001_REVISION_FLOW_PASS
KW001_ECONOMICS_RECORDED
KW001_FINAL_CARD_FROZEN
KW001_CLEAN_CONTEXT_RUNBOOK_REHEARSAL_PASS
KW001_READY_TO_SELL
```

All are required.

## 12. Immediate next action

```text
select Test A and Test B candidate sites
freeze two mock client briefs BEFORE provider analysis
then execute Test A end to end
```
