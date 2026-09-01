# OKNO_MSK — STEP 13 METHOD POSTMORTEM, REOPEN AND FULL EXECUTION RECORD

Date: 2026-09-01
Status: **POST-RUN AUDIT COMPLETE / OLD PASS WITHDRAWN / STEP 13 REOPENED / FIRST-PARTY QUERY×URL HISTORY BLOCKED**

Job: `KW001_AI_NATIVE_YANDEX_ALICE / OKNO_MSK`

## 1. Why this document exists

The first Step-13 execution completed a substantial amount of useful work and then incorrectly declared the step complete.

A later audit found that the method had already identified Yandex Webmaster historical query×URL evidence as the strongest evidence for real page competition, but the execution never acquired that layer and the acceptance gate did not require it.

This document preserves:

- everything Step 13 actually did;
- what was correct;
- what was incomplete;
- why the error happened despite pre-step research;
- the corrected method;
- the exact remaining blocker;
- what must happen before Step 13 can become fully complete again.

## 2. The core methodological failure

The pre-step research was not empty or superficial. It explicitly found official Yandex sources for historical query-by-URL analytics.

The failure happened **after research**.

The source-to-method trace described this evidence as:

```text
YANDEX_QUERY_URL_HISTORY_IDEAL_EVIDENCE
```

and the project-specific note said Webmaster was unavailable in the current base scope.

That wording created the loophole:

```text
WE KNOW THE BEST EVIDENCE EXISTS
+ WE CURRENTLY DO NOT HAVE IT
→ TREAT IT AS A LIMITATION
→ CONTINUE WITH WEAKER EVIDENCE
→ ALLOW PASS
```

The correct logic should have been:

```text
WE KNOW THIS SOURCE MATERIALLY CHANGES THE DIAGNOSIS
→ CHECK ACCESS + TOOL CAPABILITY BEFORE EXECUTION
→ IF AVAILABLE: ACQUIRE IT
→ IF UNAVAILABLE: RECORD EXACT BLOCKER
→ FULL PASS IS BLOCKED UNLESS OWNER EXPLICITLY ACCEPTS DEGRADED CLOSURE
```

Classification:

```text
SOURCE_KNOWN_BUT_NOT_OPERATIONALIZED
```

## 3. Why the pre-step gate failed to catch it

### 3.1 The source existed in research but not in the pass gate

The pre-step review correctly stated:

- history/query×URL performance is stronger than one snapshot;
- public Search cannot prove historical URL swapping or traffic harm;
- without private Webmaster/Metrika some strong conclusions are impossible.

But the proposed pass condition only checked:

- pair accounting;
- current page/task evidence;
- search evidence reuse/acquisition;
- no strong harmful verdict from one snapshot;
- no destructive remediation from weak evidence;
- QA/readback.

It did **not** require:

```text
FIRST_PARTY_QUERY_URL_HISTORY_STATUS
FIRST_PARTY_QUERY_URL_HISTORY_USED
EXPLICIT_DEGRADED_CLOSURE_IF_UNAVAILABLE
```

Therefore the step could satisfy every declared acceptance field while still missing an evidence source that its own research had identified as materially stronger.

### 3.2 Step-11 blocker was not inherited

On 2026-08-30 the Webmaster Bridge probe returned:

```text
HTTP 200
result.hosts = []
OKNO_MSK_HOST_ID_RESOLVED = false
```

The probe correctly said:

```text
HTTP_200 != TARGET_SITE_ACCESS_CONFIRMED
EMPTY_HOST_LIST = CURRENT_API_ACCOUNT_CONTEXT_SEES_ZERO_HOSTS
HOST_ID_MUST_NOT_BE_GUESSED
```

It also required account/version correction before another host-scoped call.

Step 13 did not convert this unresolved Step-11 state into a hard dependency.

### 3.3 Tool capability was not checked against the source requirement

Current repository Webmaster protocol supports only:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

The official Yandex enhanced query-by-URL export is a different workflow and is not implemented by this first-slice protocol.

Therefore even a corrected OAuth/property context would still leave a Bridge capability gap for the exact historical export required by the corrected Step-13 method.

This was not checked before the original Step-13 execution.

### 3.4 QA verified existing artifacts rather than missing required evidence

The old QA asked whether the produced artifacts were internally consistent.

It did not ask:

```text
WHICH REQUIRED EVIDENCE SOURCE SHOULD EXIST BUT DOES NOT?
```

That made it possible for a complete set of weaker artifacts to pass while a stronger mandatory evidence layer was absent.

## 4. What Step 13 actually completed correctly

The following work remains valid and must not be discarded.

### Phase A — input accounting

Historical Step-12 handoff:

```text
base pair universe = 195
pairs marked by Step 12 for future review = 186
Step-13 dependency units = 98
```

All 195 historical pairs were normalized and accounted.

### Phase B — eligibility / pre-search reduction

The Step-13 process separated normal related-page relationships from material competition candidates.

Result:

```text
phase1_closed_without_fresh_search = 168
phase1_surviving_pairs = 27
```

The 27 surviving base pairs were mapped to 21 query-family cases.

### Phase C — query-family model

The primary analytical unit was changed from raw pair to:

```text
QUERY FAMILY × CANDIDATE URL SET
```

This was a correct improvement because repeated pair edges can belong to one real search-ownership question.

Final base case count:

```text
query_family_cases = 21
```

### Phase D — reuse and fresh ordinary Search

Five cases were closed without new provider Search after current-page / saved-evidence review.

Sixteen material cases required fresh ordinary Yandex Search.

The Search provider work used ordinary Search only; no GenSearch/Alice call was used in Step 13.

Provider truth after reconciliation:

```text
planned direct Search cases = 16
usable direct Search results = 16/16
historical OUTCOME_UNKNOWN = 1
unresolved OUTCOME_UNKNOWN = 0
QF007 retry used = 1/3
QF007 retry final status = SUCCEEDED
provider boundaries started = 17
successful useful results persisted = 16
Step-13 provider cost accounted = 8.296 RUB
```

The QF007 recovery correctly followed a separate retry policy and stopped after retry 1 succeeded.

### Phase E — current-page freshness

Step 13 rechecked current first-party pages and did not rely only on frozen historical evidence.

Two material live specialist pages were discovered after the frozen pair universe:

QF016:

`https://okno-msk.ru/okna-rehau/po-tipu-doma/panoramnoe-osteklenie-domov-i-kottedzhej/`

QF017:

`https://okno-msk.ru/verandy/panoramnye-okna-na-terrasu/`

These discoveries were correctly persisted as current-site corrections.

They created four new effective pair relationships without rewriting the historical 195-pair provenance.

Final current/public evidence universe:

```text
historical base pairs = 195
freshness extension pairs = 4
effective pair universe = 199
effective pairs accounted = 199/199
silent pair drops = 0
current page evidence URLs = 49
```

### Phase F — current/public diagnosis

The preserved public/current evidence did **not** justify any strong harmful-cannibalization conclusion.

Correct preserved conclusions include:

```text
confirmed harmful cannibalization from existing evidence = 0
destructive remediation authorized = 0
strong harmful verdict from one public SERP = 0
```

The dominant observed relationship was legitimate coexistence with clearer primary responsibility:

- specialist vs broad category;
- specialist service vs accessory/product support;
- special form/use case vs broad use case;
- narrow troubleshooting article vs broad guide;
- specific comparison/best article vs general selection guide.

QF019 was correctly preserved as an intent-drift limitation instead of being forced into a strong verdict.

## 5. What Step 13 did NOT complete

### Missing evidence layer

No authorized first-party historical:

```text
query × URL × time
```

series for `okno-msk.ru` was acquired.

Therefore the execution cannot answer strongly enough:

```text
Did the same query family repeatedly alternate between candidate URLs?
Did two candidate URLs repeatedly fragment impressions/clicks?
Was one URL consistently dominant and the second incidental?
Did apparent page switching correlate with position/click/impression loss?
Was public current coexistence stable historically or only true on the sampled date?
```

### Consequence

The old statement:

```text
STEP13 = COMPLETE / PASS
```

is withdrawn.

The corrected state is:

```text
PUBLIC_AND_CURRENT_PAGE_DIAGNOSIS = COMPLETE
PAIR_ACCOUNTING = COMPLETE
ORDINARY_SEARCH_ACQUISITION = COMPLETE
FIRST_PARTY_QUERY_URL_HISTORY = NOT COMPLETE
STEP13_FULL_ACCEPTANCE = REOPENED
STEP14 = BLOCKED
```

## 6. Current blockers

There are two separate blockers and they must not be collapsed into one.

### Blocker A — property/account access

Existing durable probe:

```text
WEBMASTER listHosts
HTTP 200
hosts = []
```

Meaning:

```text
API reachable = true
current OAuth context sees target property = false/unproved
hostId resolved = false
```

The host ID must not be guessed.

### Blocker B — Bridge capability

Repository source `extension/src/shared/webmaster_protocol.js` supports only:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

It does not implement the official enhanced export endpoints under `/pro/serp/queries/download/`.

Therefore account correction alone is not sufficient for Bridge-native enhanced-export acquisition.

### Version boundary

Current repository extension manifest is `0.1.2`.

The durable Step-11 probe was produced by installed runtime `0.1.1`.

Before relying on a new Bridge Webmaster execution as current production evidence, the runtime/version difference must be resolved or explicitly accepted.

## 7. Official Yandex capability that should have been operationalized

Current official Yandex documentation states that extended query analytics by URL can expose:

```text
date
host
URL
query
region
clicks
impressions
position
```

and supports data for a long historical window (currently documented up to 550 days).

The API enhanced-export workflow includes operations for:

```text
regions
limits
dates
initialize query export
get export status
```

This is exactly the kind of first-party evidence needed to distinguish one-time public Search selection from repeated query-level page competition.

## 8. Corrected Step-13 execution protocol

Canonical reusable authority:

`STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md`

Mandatory corrected order:

```text
INPUT ACCOUNTING
→ CURRENT PAGE FRESHNESS
→ CURRENT-SITE SPECIALIST DISCOVERY
→ QUERY-FAMILY × URL-SET CASES
→ SOURCE/CAPABILITY/ACCESS MATRIX
→ REUSE EXISTING FIRST-PARTY HISTORY
→ REUSE ORDINARY SEARCH
→ BOUNDED FRESH SEARCH WHERE NEEDED
→ FIRST-PARTY QUERY×URL HISTORY FOR MATERIAL COMPETITION CASES
→ SEPARATE CURRENT SIGNAL / HISTORICAL COMPETITION / HARM
→ VERDICT
→ REMEDIATION
→ QA THAT CHECKS MISSING REQUIRED EVIDENCE
→ READBACK
→ ACCEPTANCE
```

## 9. Remaining work to finish Step 13

### R13-01 — correct Webmaster access context

Before another live host-scoped command:

```text
confirm the active Yandex account has okno-msk.ru in Webmaster;
confirm Bridge OAuth belongs to that account;
resolve installed/runtime version boundary;
run listHosts once only after correction;
persist the result immediately;
resolve exact hostId only from provider evidence.
```

Do not blind-repeat the old zero-host call.

### R13-02 — obtain an executable query×URL history route

One of these must become real:

```text
A. manual/authorized Webmaster UI export/monitoring for the required candidate cases;
B. governed Bridge enhancement implementing official enhanced-export operations;
C. another explicit first-party route that provides comparable query×URL historical evidence.
```

A theoretical route does not satisfy this item.

### R13-03 — freeze a historical evidence manifest

For each material case, define:

```text
case id
query/query family
candidate URLs
region
date scope
why this scope is sufficient/partial
expected fields
source route
quota implications
storage artifact
```

Do not invent a universal number of days. The window must be justified from actual provider availability, seasonality, query volume and decision value.

### R13-04 — acquire and persist first-party history

For every executed first-party provider/export interaction:

```text
provider result
→ immediate durable persistence
→ readback
→ accounting/completeness QA
→ only then next interaction
```

### R13-05 — historical competition analysis

For each material case distinguish:

```text
stable one-owner behavior
legitimate complementary long-tail behavior
current-only multi-URL signal
repeated historical multi-URL competition
repeated owner switching
performance fragmentation
harmful impact supported
insufficient evidence
```

### R13-06 — rebuild final diagnosis / remediation

The current public/current-page verdicts remain evidence inputs, not final immutable truth.

Historical evidence may:

- confirm current coexistence;
- upgrade a case to historical competition;
- reveal a problem missed by the public snapshot;
- show one page has been consistently dominant;
- preserve uncertainty.

### R13-07 — rerun independent QA

QA must fail if a required source is known but silently absent.

### R13-08 — only then restore acceptance

Full PASS is allowed only when:

```text
FIRST_PARTY_QUERY_URL_HISTORY_GATE = AVAILABLE_AND_USED
```

or the owner explicitly approves a degraded closure with the limitation preserved in the final deliverable.

Until then:

```text
STEP13_COMPLETE = false
NEXT_STEP_ALLOWED = false
STEP14_EXECUTED = false
```

## 10. Artifacts produced by the first execution and still valid

Core accounting / case artifacts:

- `STEP_13_PAIR_INPUT_NORMALIZED.tsv`
- `STEP_13_PAIR_ELIGIBILITY.tsv`
- `STEP_13_PAIR_ELIGIBILITY_MANUAL_RESOLUTIONS.tsv`
- `STEP_13_QUERY_FAMILY_DEFINITIONS.tsv`
- `STEP_13_QUERY_FAMILY_CASES.tsv`
- `STEP_13_SURVIVOR_PHRASE_EVIDENCE.tsv`
- `STEP_13_PRESEARCH_CASE_DECISIONS.tsv`
- `STEP_13_CURRENT_PAGE_EVIDENCE.tsv`
- `STEP_13_CURRENT_PAGE_EVIDENCE_EXTENSION.tsv`
- `STEP_13_SEARCH_MANIFEST.tsv`
- persisted per-query Search JSON evidence
- `STEP_13_QF016_CURRENT_SITE_CORRECTION_2026-09-01.json`
- `STEP_13_QF017_CURRENT_SITE_CORRECTION_2026-09-01.json`
- `STEP_13_PAIR_UNIVERSE_EXTENSION.tsv`
- `STEP_13_FINAL_PAIR_ACCOUNTING.json`

Artifacts that must now be treated as superseded in their old PASS semantics until historical evidence is resolved:

- `STEP_13_CONFLICT_DIAGNOSIS.tsv` — valid as current/public diagnosis layer, not complete historical diagnosis;
- `STEP_13_REMEDIATION_RECOMMENDATIONS.tsv` — non-destructive recommendations remain provisional;
- `STEP_13_QA.json` — old PASS withdrawn;
- `STEP_13_REPORT.md` — old completion semantics withdrawn;
- `STEP_13_ACCEPTANCE_2026-09-01.md` — old full acceptance withdrawn;
- `STEP_13_CURRENT_STATE.json` — must show reopened/blocker state.

## 11. Non-repeat controls

```text
SOURCE_KNOWN_BUT_NOT_OPERATIONALIZED = BLOCKING DEFECT
LIMITATION_DISCLOSED != ACCEPTANCE_CONTROL
PREVIOUS_STEP_ACCESS_BLOCKER MUST BE INHERITED
ACCOUNT ACCESS != TOOL CAPABILITY
QA MUST TEST FOR MISSING REQUIRED EVIDENCE
PUBLIC SERP SNAPSHOT != HISTORICAL QUERY×URL SERIES
PAIR ACCOUNTING PASS != CANNIBALIZATION DIAGNOSIS PASS
SEARCH PROVIDER COMPLETION != FIRST-PARTY HISTORY COMPLETION
FULL PASS REQUIRES HISTORY OR EXPLICIT OWNER DEGRADED EXCEPTION
```

## 12. Current status

```text
STEP13_PUBLIC_CURRENT_ANALYSIS_COMPLETE = true
STEP13_PAIR_ACCOUNTING_COMPLETE = true
STEP13_ORDINARY_SEARCH_COMPLETE = true
STEP13_FIRST_PARTY_QUERY_URL_HISTORY_COMPLETE = false
STEP13_OLD_PASS_WITHDRAWN = true
STEP13_REOPENED = true
STEP14_ALLOWED = false
```

No additional paid ordinary Search request is justified by this correction. The remaining evidence need is first-party historical query×URL behavior, not another public SERP snapshot.