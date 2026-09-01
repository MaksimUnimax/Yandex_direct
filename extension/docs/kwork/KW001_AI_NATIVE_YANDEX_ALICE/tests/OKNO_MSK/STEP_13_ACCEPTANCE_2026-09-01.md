# Step 13 acceptance — OKNO_MSK

Date: 2026-09-01
Status: **OLD FULL ACCEPTANCE WITHDRAWN / STEP 13 REOPENED**

## Why the old acceptance was wrong

The original acceptance reconciled pair accounting, current-page evidence, ordinary Search acquisition, provider outcomes, remediation strength and GitHub readback. Those checks were real and remain useful.

However, the Step-13 pre-step research had already identified official Yandex first-party query-by-URL historical analytics as materially stronger evidence for real page competition. The execution did not acquire that evidence and the acceptance gate did not require either:

```text
FIRST_PARTY_QUERY_URL_HISTORY = AVAILABLE_AND_USED
```

or an explicit owner-approved degraded closure.

This is the exact failure:

```text
SOURCE_KNOWN_BUT_NOT_OPERATIONALIZED
```

Therefore the old `COMPLETE/PASS` decision is withdrawn.

## Preserved completed gates

```text
HISTORICAL_BASE_PAIRS_ACCOUNTED = 195/195
BASE_SILENT_PAIR_DROPS = 0
FRESHNESS_EXTENSION_PAIRS = 4/4
EFFECTIVE_FINAL_PAIR_UNIVERSE = 199
EFFECTIVE_FINAL_PAIRS_ACCOUNTED = 199/199
EFFECTIVE_FINAL_SILENT_PAIR_DROPS = 0
SURVIVING_BASE_PAIRS_MAPPED_TO_CASES = 27/27
QUERY_FAMILY_CASES_PUBLIC_CURRENT_LAYER = 21/21
PRESEARCH_CASES_CLOSED = 5/5
FRESH_SEARCH_CASES_WITH_USABLE_EVIDENCE = 16/16
HISTORICAL_PROVIDER_OUTCOME_UNKNOWN = 1
UNRESOLVED_PROVIDER_OUTCOME_UNKNOWN = 0
QF007_RETRY_USED = 1/3
QF007_RETRY_FINAL_STATUS = SUCCEEDED
STEP13_PROVIDER_COST_RUB_ACCOUNTED = 8.296
CURRENT_PAGE_EVIDENCE_URLS = 49
STRONG_HARMFUL_VERDICT_FROM_ONE_PUBLIC_SERP_SNAPSHOT = 0
DESTRUCTIVE_REMEDIATION_AUTHORIZED = 0
GENSEARCH_OR_ALICE_CALLS = 0
STEP14_EXECUTED = false
```

These facts prove that the public/current-page/Search layer was executed and reconciled. They do not prove that the full cannibalization-diagnosis objective is complete.

## Blocking acceptance gates

```text
FIRST_PARTY_QUERY_URL_HISTORY_SOURCE_IDENTIFIED = true
FIRST_PARTY_QUERY_URL_HISTORY_ACQUIRED = false
OWNER_APPROVED_DEGRADED_CLOSURE = false
OKNO_MSK_WEBMASTER_HOST_ID_RESOLVED = false
CURRENT_WEBMASTER_BRIDGE_ENHANCED_QUERY_URL_EXPORT_SUPPORTED = false
RUNTIME_VERSION_BOUNDARY_RESOLVED_OR_ACCEPTED = false
BLOCKING_QA_FINDINGS = 2
```

Durable evidence already shows that the Webmaster API is reachable but the active OAuth context returned `hosts=[]`; therefore the target host ID is not resolved and must not be guessed.

Current repository Webmaster protocol is only the first read-only slice (`listHosts`, `getSummary`, `getDiagnostics`, `getPopularQueries`) and does not implement the official enhanced query-by-URL export workflow.

## Correct acceptance decision

```text
PUBLIC_CURRENT_PAGE_DIAGNOSIS = COMPLETE
PAIR_ACCOUNTING = COMPLETE
ORDINARY_SEARCH_ACQUISITION = COMPLETE
FIRST_PARTY_QUERY_URL_HISTORY = INCOMPLETE / BLOCKED
STEP13_FULL_ACCEPTANCE = REOPENED
STEP13_COMPLETE = false
NEXT_STEP_ALLOWED = false
STEP14_EXECUTED = false
```

## What is required to restore full acceptance

1. Resolve the Yandex Webmaster account/property context and obtain the target `hostId` from provider evidence.
2. Resolve an executable first-party query×URL historical evidence route: authorized Webmaster UI/export, governed Bridge enhancement, or another explicitly justified comparable first-party route.
3. Freeze a focused historical-evidence manifest for the material Step-13 cases.
4. Acquire, persist and read back the historical evidence.
5. Re-run case diagnosis separating current signal, historical competition and actual harm.
6. Rebuild remediation recommendations if historical evidence changes any case.
7. Re-run independent QA with explicit missing-evidence checks.
8. Only then restore Step-13 acceptance, unless the owner explicitly accepts a degraded evidence closure.

## Canonical correction authorities

- `../../STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md`
- `STEP_13_METHOD_POSTMORTEM_REOPEN_AND_FULL_EXECUTION_RECORD_2026-09-01.md`
- `STEP_13_QA.json`
- `STEP_13_QA_FINDINGS.tsv`
- `STEP_13_CURRENT_STATE.json`

Step 14 remains blocked.