# KW001 OKNO_MSK — Step 13 competing-page / cannibalization diagnosis

Date: 2026-09-01
Status: **REOPENED AFTER POST-RUN METHOD AUDIT / PUBLIC+CURRENT LAYER COMPLETE / FIRST-PARTY HISTORY BLOCKED**

## Executive result

Step 13 completed the full declared pair accounting, current-page freshness work and bounded ordinary Yandex Search program, but the former full `PASS/COMPLETE` status is withdrawn.

Reason:

```text
SOURCE_KNOWN_BUT_NOT_OPERATIONALIZED
```

The pre-step research had already identified official Yandex historical query-by-URL evidence as the strongest source for repeated page competition, but that source was not converted into a mandatory executable/acceptance gate. The step therefore finished with strong current/public evidence but without first-party `query × URL × time` history.

Canonical detailed postmortem and complete execution record:

`STEP_13_METHOD_POSTMORTEM_REOPEN_AND_FULL_EXECUTION_RECORD_2026-09-01.md`

Corrected reusable method:

`../../STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md`

## Work completed and preserved

### Pair and case accounting

```text
historical Step-12 pair universe = 195
base pairs accounted = 195/195
Phase-1 normal relationships closed without fresh Search = 168
Phase-1 surviving pairs = 27
surviving pairs mapped to cases = 27/27
query-family cases = 21
presearch cases closed = 5
```

### Ordinary Yandex Search acquisition

```text
fresh Search cases = 16
usable fresh Search evidence = 16/16
historical provider OUTCOME_UNKNOWN = 1
unresolved OUTCOME_UNKNOWN = 0
QF007 retry used = 1/3
QF007 retry final status = SUCCEEDED
provider boundaries started = 17
successful useful results persisted = 16
Step-13 provider cost accounted = 8.296 RUB
GenSearch/Alice calls = 0
```

### Current-site freshness correction

Step 13 discovered two material specialist pages absent from the frozen historical evidence:

QF016:

`https://okno-msk.ru/okna-rehau/po-tipu-doma/panoramnoe-osteklenie-domov-i-kottedzhej/`

QF017:

`https://okno-msk.ru/verandy/panoramnye-okna-na-terrasu/`

These discoveries created four additional effective pair relationships.

Final current/public accounting:

```text
freshness extension pairs = 4
effective pair universe = 199
effective pairs accounted = 199/199
silent pair drops = 0
current page evidence URLs = 49
```

### Public/current diagnosis

The preserved public/current evidence does not justify a confirmed harmful-cannibalization verdict or destructive remediation.

```text
confirmed harmful cannibalization from existing public/current evidence = 0
strong harmful verdict from one public SERP snapshot = 0
destructive remediation authorized = 0
```

The dominant observed pattern remains legitimate coexistence with clearer primary responsibility: specialist vs broad category, specialist service vs supporting product/accessory page, narrow troubleshooting article vs broad guide, and similar primary/supporting boundaries.

QF019 remains explicitly evidence-limited because the direct query drifted toward external/emergency opening intent.

## What was missing

No first-party historical query×URL series for `okno-msk.ru` was acquired.

Therefore Step 13 still lacks the evidence needed to test, over time:

- repeated ownership switching between candidate URLs;
- simultaneous/alternating impressions for the same query family;
- fragmentation of clicks/impressions;
- stable one-owner dominance vs incidental secondary visibility;
- whether any observed competition is actually harmful rather than normal multi-page coverage.

Official Yandex extended query analytics by URL exposes the relevant dimensions: date, URL, query, region, clicks, impressions and position.

## Why this was missed despite pre-step research

The research correctly found the source but the execution logic treated it as “ideal evidence” instead of a mandatory availability/use gate.

The old QA then validated the artifacts that existed instead of asking whether a required evidence source was missing.

The Step-11 Webmaster blocker also was not inherited correctly. Durable Step-11 evidence already showed:

```text
Webmaster API reachable = true
active OAuth context hosts = []
OKNO_MSK hostId resolved = false
```

Additionally, current repository `webmaster_protocol.js` supports only:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

and does not implement the official enhanced query-by-URL export workflow.

The repository extension manifest is `0.1.2`, while the durable Step-11 live probe reported runtime `0.1.1`; that boundary must be resolved or explicitly accepted before new live Webmaster evidence is treated as current production evidence.

## Current QA

The old QA PASS is withdrawn.

Current blocking findings:

```text
S13-F001 = SOURCE_KNOWN_BUT_NOT_OPERATIONALIZED
S13-F002 = ACCESS_AND_TOOL_CAPABILITY_UNRESOLVED
blocking findings = 2
```

See:

- `STEP_13_QA.json`
- `STEP_13_QA_FINDINGS.tsv`

## Remaining work

1. Correct/verify the Webmaster account/property context and resolve `okno-msk.ru` hostId from provider evidence.
2. Resolve an executable first-party query×URL history route: authorized Webmaster UI/export, governed Bridge enhancement, or comparable explicitly justified first-party source.
3. Freeze a focused historical-evidence manifest for material Step-13 cases.
4. Acquire and persist complete historical evidence, one provider/export result at a time with readback/completeness QA.
5. Re-run historical competition analysis.
6. Rebuild diagnosis/remediation where history changes the public/current verdict.
7. Re-run independent QA, including missing-required-source checks.
8. Restore full Step-13 acceptance only after the history gate passes or the owner explicitly approves a degraded closure.

## Current roadmap handoff

```text
STEP13_PUBLIC_CURRENT_ANALYSIS_COMPLETE = true
STEP13_PAIR_ACCOUNTING_COMPLETE = true
STEP13_ORDINARY_SEARCH_COMPLETE = true
STEP13_FIRST_PARTY_QUERY_URL_HISTORY_COMPLETE = false
STEP13_COMPLETE = false
STEP14_EXECUTED = false
NEXT_STEP_ALLOWED = false
```

No further paid ordinary Search query is justified at this point. The missing information is first-party historical query×URL behavior, not another public SERP snapshot.