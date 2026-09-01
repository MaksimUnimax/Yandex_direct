# KW-001 / OKNO-MSK — JOB FLOW Step 13 sync

Date: 2026-09-01
Status: **ACTIVE / CURRENT ROADMAP SYNC / STEP 13 REOPENED FOR POLICY QA RECONCILIATION**

This file is a current-state synchronization overlay for `JOB_FLOW.md`. It supersedes stale Step-13 status lines in the older `JOB_FLOW.md` snapshot without rewriting historical Step-12 provenance. Canonical machine-readable authority remains `STEP_13_CURRENT_STATE.json`.

Current Layer-A private-data authority:

`../../CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`

Owner-established current-job state:

```text
YANDEX_WEBMASTER_ACCESS_STATE = UNAVAILABLE
YANDEX_WEBMASTER_PRIVATE_EVIDENCE_USED = false
BASE_PUBLIC_EVIDENCE_MODE = true
```

The base Kwork no longer treats lack of client Webmaster access as a provider/operator blocker. Historical/private claims remain bounded by available evidence.

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
| 13 | Cannibalization diagnosis | 🔄 REOPENED — PUBLIC/CURRENT LAYER COMPLETE; PRIVATE HISTORY UNAVAILABLE; BASE-MODE POLICY ADOPTED; QA RECONCILIATION REQUIRED |
| 14 | Search-only architecture freeze | ⛔ BLOCKED / NOT EXECUTED UNTIL STEP-13 POLICY QA CLOSES |
| 15 | AI-case selection | ⬜ NOT STARTED |
| 16 | AI-search evidence | ⬜ NOT STARTED — WEBMASTER ACCESS CHECK REQUIRED; GENSEARCH BASE FALLBACK EXISTS |
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

That methodological finding remains valid: public SERP must not be misrepresented as historical first-party evidence.

What changed is the commercial/base-package policy. The owner has now explicitly established:

```text
CLIENT_PRIVATE_DATA_UNAVAILABLE
-> NORMAL BASE MODE
-> NOT A PROCESS FAILURE
-> NOT A PURCHASE BLOCKER
-> BASE STEP MAY CLOSE WITH EXPLICIT EVIDENCE BOUNDARY
```

Therefore the two historical Step-13 QA findings must now be reconciled against the new Layer-A policy instead of forcing a Webmaster acquisition that this test project cannot provide.

Current state:

```text
FIRST_PARTY_QUERY_URL_HISTORY_ACQUIRED = false
YANDEX_WEBMASTER_ACCESS_STATE = UNAVAILABLE
BASE_PUBLIC_EVIDENCE_MODE = true
PRIVATE HISTORY CLAIMS ALLOWED = false
PROVIDER_OPERATOR_ACTION_PENDING = false
STEP13_COMPLETE = false
CURRENT_POLICY_QA_RERUN_REQUIRED = true
STEP14_EXECUTED = false
NEXT_STEP_ALLOWED = false
```

## Current Webmaster capability facts preserved for first future access

Historical durable Step-11 probe:

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

Version evidence:

```text
REPOSITORY_EXTENSION_VERSION = 0.1.2
LAST_DURABLE_LIVE_WEBMASTER_PROBE_RUNTIME = 0.1.1
```

These are not current OKNO-MSK execution blockers under base mode. They are preserved capability/access facts to resolve when the first real client Webmaster access becomes available and the mandatory WITH_ACCESS vs WITHOUT_ACCESS comparison is triggered.

## Current Step-13 authorities

Layer-A client-private-data policy:

`../../CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`

Reusable Step-13 method:

`../../STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md`

Where the older Step-13 hard-history pass condition conflicts with the later owner-approved Layer-A base-package policy, the Layer-A policy has precedence for base Kwork jobs.

Execution postmortem/full record:

`STEP_13_METHOD_POSTMORTEM_REOPEN_AND_FULL_EXECUTION_RECORD_2026-09-01.md`

Historical recovery plan retained for future enhanced/with-access work:

`STEP_13_FIRST_PARTY_QUERY_URL_HISTORY_RECOVERY_PLAN_2026-09-01.md`

Current state/QA:

`STEP_13_CURRENT_STATE.json`  
`STEP_13_QA.json`  
`STEP_13_QA_FINDINGS.tsv`  
`STEP_13_REPORT.md`  
`STEP_13_ACCEPTANCE_2026-09-01.md`

The existing `STEP_13_CONFLICT_DIAGNOSIS.tsv` and `STEP_13_REMEDIATION_RECOMMENDATIONS.tsv` remain valid as the public/current evidence layer.

## Required next action inside Step 13

Do not execute Step 14 yet.

Do not buy another ordinary Search snapshot.

Do not attempt to obtain Webmaster access for this test project; the owner has established that it is unavailable.

Next action:

```text
1. re-run Step-13 QA against CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md;
2. reclassify absent private query×URL history as an explicit BASE_PUBLIC_EVIDENCE_MODE boundary rather than a blocker;
3. verify that no historical switching / historical absence / traffic-loss / harm claim exceeds public evidence;
4. verify all 199/199 accounting and existing public evidence remain intact;
5. update Step-13 report/remediation wording where the old hard-history gate leaked into conclusions;
6. write new acceptance state;
7. GitHub readback;
8. only if QA has zero current-policy blocking findings may Step 13 close and Step 14 pre-step begin.
```
