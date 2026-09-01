# KW-001 / OKNO-MSK — JOB FLOW Step 13 sync

Date: 2026-09-01
Status: **ACTIVE / CURRENT ROADMAP SYNC / STEP 13 REOPENED**

This file is a current-state synchronization overlay for `JOB_FLOW.md`. It supersedes stale Step-13 status lines in the older `JOB_FLOW.md` snapshot without rewriting historical Step-12 provenance. Canonical machine-readable authority remains `STEP_13_CURRENT_STATE.json`.

## Current roadmap

| Step | Meaning | Status |
|---|---|---|
| 0 | Scope freeze | ✅ COMPLETE |
| 1 | Existing-site discovery | ✅ COMPLETE |
| 2 | Wordstat acquisition plan | ✅ COMPLETE |
| 3 | Historical first pass | 🔁 SUPERSEDED |
| 3R | Repaired first pass | ✅ COMPLETE |
| 4 | Family-level triage | ✅ COMPLETE |
| 5 | Targeted Wordstat expansion | ✅ COMPLETE |
| 6 | Demand dynamics | ✅ COMPLETE / PRESERVED |
| 6A | Acquisition coverage revalidation | ✅ COMPLETE |
| 7 | Semantic cleanup | ✅ COMPLETE |
| 8 | Search-stage semantic freeze | ✅ COMPLETE |
| 9 | Ordinary Yandex Search validation | ✅ COMPLETE |
| 10 | User-task / SERP clustering | ✅ COMPLETE |
| 11 | Page ownership | ✅ COMPLETE |
| 12 | Structural actions | ✅ COMPLETE |
| 13 | Cannibalization diagnosis | 🔄 REOPENED — PUBLIC/CURRENT LAYER COMPLETE, FIRST-PARTY QUERY×URL HISTORY BLOCKED |
| 14 | Search-only architecture freeze | ⛔ BLOCKED / NOT EXECUTED |
| 15 | AI-case selection | ⬜ NOT STARTED |
| 16 | AI-search evidence | ⬜ NOT STARTED |
| 17 | Search-vs-AI comparison | ⬜ NOT STARTED |
| 18 | Prioritization | ⬜ NOT STARTED |
| 19 | Client deliverables | ⬜ NOT STARTED |
| 20 | Final QA | ⬜ NOT STARTED |
| 21 | Handoff / revisions | ⬜ NOT STARTED |
| 22 | Job close | ⬜ NOT STARTED |

## Step 13 preserved completed work

```text
HISTORICAL_BASE_PAIR_UNIVERSE = 195
BASE_PAIRS_ACCOUNTED = 195/195
PHASE1_CLOSED_WITHOUT_FRESH_SEARCH = 168
PHASE1_SURVIVING_PAIRS = 27
SURVIVING_PAIRS_MAPPED_TO_CASES = 27/27
QUERY_FAMILY_CASES_PUBLIC_CURRENT_LAYER = 21/21
PRESEARCH_CASES_CLOSED = 5/5
FRESH_SEARCH_CASES_WITH_USABLE_EVIDENCE = 16/16
CURRENT_SITE_SPECIALIST_URLS_ADDED = 2
PAIR_UNIVERSE_EXTENSION_ROWS = 4
EFFECTIVE_FINAL_PAIR_UNIVERSE = 199
EFFECTIVE_FINAL_PAIRS_ACCOUNTED = 199/199
SILENT_PAIR_DROPS = 0
CURRENT_PAGE_EVIDENCE_URLS = 49
PROVIDER_BOUNDARIES_STARTED = 17
SUCCESSFUL_USEFUL_PROVIDER_RESULTS_PERSISTED = 16
HISTORICAL_OUTCOME_UNKNOWN = 1
UNRESOLVED_OUTCOME_UNKNOWN = 0
QF007_RETRY_USED = 1/3
QF007_RETRY_STATUS = SUCCEEDED
STEP13_PROVIDER_COST_RUB = 8.296
STRONG_HARMFUL_VERDICT_FROM_ONE_PUBLIC_SERP = 0
DESTRUCTIVE_REMEDIATION_AUTHORIZED_CASES = 0
GENSEARCH_OR_ALICE_CALLS_IN_STEP13 = 0
ORDINARY_SEARCH_ACQUISITION_COMPLETE = true
PUBLIC_CURRENT_PAGE_DIAGNOSIS_COMPLETE = true
```

## Why the former Step-13 PASS was withdrawn

The Step-13 pre-step research had already identified official Yandex first-party query-by-URL historical analytics, but that source was not converted into a mandatory executable/acceptance gate.

```text
SOURCE_KNOWN_BUT_NOT_OPERATIONALIZED = true
```

The old QA validated the artifacts that existed instead of testing whether a known required evidence source was missing.

Current blocking state:

```text
FIRST_PARTY_QUERY_URL_HISTORY_ACQUIRED = false
OWNER_APPROVED_DEGRADED_CLOSURE = false
OKNO_MSK_WEBMASTER_HOST_ID_RESOLVED = false
CURRENT_WEBMASTER_BRIDGE_ENHANCED_QUERY_URL_EXPORT_SUPPORTED = false
BLOCKING_QA_FINDINGS = 2
STEP13_COMPLETE = false
STEP14_EXECUTED = false
NEXT_STEP_ALLOWED = false
```

## Current Webmaster blockers

Durable Step-11 probe:

```text
WEBMASTER_API_REACHABLE = true
ACTIVE_OAUTH_CONTEXT_HOSTS = []
OKNO_MSK_HOST_ID_RESOLVED = false
```

Current repository Webmaster protocol supports only:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

It does not implement the official enhanced query-by-URL export workflow.

Version boundary:

```text
REPOSITORY_EXTENSION_VERSION = 0.1.2
LAST_DURABLE_LIVE_WEBMASTER_PROBE_RUNTIME = 0.1.1
```

## Current Step-13 authorities

Reusable corrected method:

`../../STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md`

Execution postmortem/full record:

`STEP_13_METHOD_POSTMORTEM_REOPEN_AND_FULL_EXECUTION_RECORD_2026-09-01.md`

Recovery plan:

`STEP_13_FIRST_PARTY_QUERY_URL_HISTORY_RECOVERY_PLAN_2026-09-01.md`

Current state/QA:

`STEP_13_CURRENT_STATE.json`  
`STEP_13_QA.json`  
`STEP_13_QA_FINDINGS.tsv`  
`STEP_13_REPORT.md`  
`STEP_13_ACCEPTANCE_2026-09-01.md`

The existing `STEP_13_CONFLICT_DIAGNOSIS.tsv` and `STEP_13_REMEDIATION_RECOMMENDATIONS.tsv` remain valid as the **public/current evidence layer**, not as immutable full historical acceptance.

## Required next action inside Step 13

Do not execute Step 14.

Do not buy another ordinary Search snapshot.

Step 13 can continue only by resolving the first-party history route:

```text
1. correct/verify Webmaster account + property context;
2. resolve installed/runtime version boundary;
3. re-run listHosts once only after a real correction and persist/read back the result;
4. obtain exact okno-msk.ru hostId from provider evidence;
5. resolve an executable query×URL historical route (authorized UI/export, governed Bridge enhancement, or comparable first-party source);
6. freeze historical manifest;
7. acquire/persist/read back history;
8. rerun diagnosis/remediation/QA;
9. only then restore Step-13 acceptance.
```
