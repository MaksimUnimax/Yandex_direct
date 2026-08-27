# PHASE 6 — Semantic Core Builder / batch evidence orchestration

Date: 2026-08-27

Status: **REQUIREMENTS READY / IMPLEMENTATION AUTHORIZED AFTER EXACT-MAIN BRANCH FREEZE**

## 1. Product objective

Phase 6 converts the already accepted Yandex provider primitives into a repeatable commercial semantic-core workflow for ChatGPT Plus.

The target is **not** an autonomous SEO program inside the extension.

Permanent worker boundary:

```text
ChatGPT Plus
= analyst / planner / semantic architect / QA / client-deliverable author

Yandex Marketing Bridge
= controlled hands for repeatable provider acquisition, persistence, queueing and recovery

Human owner/operator
= authorization boundary and extension operator
```

The extension must automate repetitive deterministic work. It must not hard-code subjective SEO strategy that ChatGPT can perform from the evidence.

## 2. Market reason

The freelance capability study produced repeated independent demand for:

- Yandex Wordstat semantic-core collection;
- 100 / 150 / 300 / 500 / 10,000-keyword jobs;
- cleanup and deduplication;
- grouping by intent / section;
- keyword → target page mapping;
- advertising semantic cores;
- competitor-derived seed discovery;
- exact-frequency enrichment as an upsell;
- TOP/SERP clustering as a higher-cost upsell.

The common operational bottleneck is not lack of reasoning. It is safe bulk acquisition and durable evidence handling.

Canonical market evidence:

`extension/docs/FREELANCE_ORDER_CAPABILITY_MATRIX.md`

## 3. Current accepted primitives

Phase 6 starts from closed Phase 5 `main` and must preserve all accepted services.

Wordstat already exposes:

```text
WORDSTAT_API_V1
getTop
getDynamics
getRegionsDistribution
getRegionsTree
```

Current `getTop` supports:

```text
phrase
numPhrases: 1..2000
regions: bounded list
devices: DEVICE_ALL / DESKTOP / PHONE / TABLET
```

Ordinary Search already exposes bounded Yandex SERP acquisition.

The existing worker already has important transaction/recovery ideas:

- run status;
- request state;
- delivery claim/commit/confirm;
- pause/stop;
- unknown-request-outcome no-retry handling;
- per-run request/cost policy;
- persisted Chrome local state.

Phase 6 should reuse these invariants rather than build a second lifecycle framework.

## 4. Primary missing hand

### `WORDSTAT_BATCH_JOB_V1`

The first implementation slice is a durable, explicit batch acquisition job over trusted `WORDSTAT_API_V1` commands.

Conceptual input:

```text
job_id
conversation_key
seed_phrases[]
method = getTop | optional exact-frequency enrichment profile
regions[]
devices[]
numPhrases per seed
request/cost bounds
```

The job must create deterministic per-item work records rather than asking ChatGPT to remember which seed has already been sent.

## 5. Required item state machine

Each seed/item must have durable identity and state such as:

```text
PENDING
CLAIMED
REQUEST_STARTED
SUCCEEDED
FAILED_TERMINAL
OUTCOME_UNKNOWN
SKIPPED
CANCELLED
```

Exact names may change after implementation audit, but semantics must not.

Critical rule:

> if provider initiation may have occurred and the outcome is unknown, do not replay automatically.

`OUTCOME_UNKNOWN` must require explicit reconciliation/operator/ChatGPT decision, preserving the project's existing no-blind-retry discipline.

## 6. Exactly-once / duplicate discipline

Every batch item needs a stable fingerprint derived from the normalized trusted provider command plus job identity.

The runtime must prevent accidental duplicate execution of the same item due to:

- service worker restart;
- tab refresh/close;
- repeated assistant text;
- double click;
- resume after pause;
- stale delivery event;
- recovery after process restart.

A successful item may be intentionally re-measured only through an explicit new observation/job revision, never by silent replay.

## 7. Persistence requirements

Persist at minimum:

```text
job identity / revision
input manifest
item fingerprints
item states
normalized command
request_id
started_at / completed_at
request_executed truth
http/provider outcome
normalized result payload or durable result reference
cost/request counters
unknown-outcome markers
cancel/pause reason
```

Do not persist credential secrets inside job evidence.

The job must survive service-worker suspension/restart without forgetting completed items.

## 8. Progress and resume

ChatGPT and the operator must be able to know:

```text
total items
pending
in flight
succeeded
failed terminal
outcome unknown
skipped
current request/cost totals
next safe action
```

Resume must continue only from safe pending items.

It must never mean `start the whole list again`.

## 9. Budget / request policy

Reuse existing provider policy and cost-ledger architecture.

Before starting the next item, admission must check current policy bounds.

Phase 6 should support:

```text
max requests per job/run
max estimated RUB where provider tariff exists
explicit STOP when bound is reached
no hidden retries
```

The system should expose progress/budget truth to ChatGPT so ChatGPT can decide whether another seed is worth the marginal request.

## 10. Evidence output

The Bridge should return/provider-store evidence in a form ChatGPT can consume without semantic loss.

Required separation:

```text
raw provider result truth
normalized observation
job/item metadata
```

Do not silently delete phrases merely because they look semantically duplicate. Provider acquisition should preserve evidence.

A deterministic **exact-text duplicate projection** may be provided as a convenience, but subjective semantic cleanup remains ChatGPT's job.

## 11. What remains ChatGPT work

The following must **not** become hard-coded Phase 6 ranking/SEO rules:

- deciding seed strategy;
- deciding whether more Wordstat expansion is useful;
- semantic noise cleaning beyond mechanical exact normalization;
- intent classification;
- ВЧ/СЧ/НЧ thresholds unless explicitly chosen for the job;
- deciding commercial vs informational value;
- clustering by user job;
- choosing page boundaries;
- keyword → target page mapping;
- cannibalization resolution;
- competitor interpretation;
- client recommendations;
- final XLSX/PDF/DOCX structure and prose.

ChatGPT Plus performs those tasks using the acquired evidence.

## 12. Semantic Core Builder workflow on top of the hand

Once batch acquisition is available, the repeatable ChatGPT workflow is:

```text
1. intake: site/topic/region/pages/competitors/exclusions
2. ChatGPT understands business and creates seed map
3. WORDSTAT_BATCH_JOB_V1 acquires bounded seed evidence
4. ChatGPT reviews marginal value and optionally expands specific branches
5. ChatGPT cleans/deduplicates semantically
6. ChatGPT classifies intent and frequency bands where useful
7. ChatGPT groups by actual user job
8. ChatGPT maps groups to current/new target pages
9. optional bounded Search measurements for uncertain page-job boundaries
10. ChatGPT resolves conflicts/cannibalization
11. ChatGPT creates client workbook/report
```

This supports current READY-NOW freelance configurations without pretending that a generic algorithm replaces expert reasoning.

## 13. Optional enrichment after first slice

Not required for Phase 6 first implementation closure, but the architecture should leave room for:

### Exact-frequency batch profile

Per-final-key Wordstat operator/exact-frequency measurements with the same durable queue/checkpoint rules.

This is valuable commercially but can be expensive at scale and therefore needs explicit job economics.

### Search/TOP batch job

A sibling durable job for paid Search measurements:

```text
keyword list + region
→ safe Search queue
→ one persisted SERP per keyword
→ domain sets
→ evidence for ChatGPT / clustering engine
```

Do not combine it blindly into every semantic-core job. TOP clustering is a higher-cost workflow.

## 14. Explicit non-goals

Phase 6 first slice does not include:

- Google organic provider;
- Ahrefs/Keys.so replacement;
- full-site crawler;
- Alice/GenSearch implementation;
- autonomous SEO recommendation scoring;
- automatic content publication;
- Direct writes/bids/budgets;
- Metrika/Webmaster writes.

Alice-specific engineering remains behind the independent `blood_sand` comparative gate.

## 15. Safety / compatibility invariants

Must preserve:

- dedicated service credentials;
- no credential consolidation;
- Manual/Autorun ownership rules;
- no blind retry after unknown provider outcome;
- active-service isolation;
- prior Wordstat/Search/Webmaster/Metrika/Direct behavior;
- accepted Phase 5 `extension/src` as exact implementation baseline;
- no provider write surface.

## 16. Implementation sequence

```text
P6-00 fetch exact live main and freeze baseline identities
P6-01 audit existing run/autorun/storage/cost lifecycle for reusable primitives
P6-02 define batch job model + storage contract + command fingerprint contract
P6-03 unit-test job state transitions/recovery first
P6-04 implement Wordstat batch job runtime
P6-05 expose bounded control/status surface to popup/content/ChatGPT path
P6-06 test service-worker restart, tab close, pause/resume, double-submit, stale events
P6-07 test unknown provider outcome => no automatic replay
P6-08 test request/cost budget stop
P6-09 prior-service regression including Direct
P6-10 freeze candidate and independent complete gate
P6-11 owner-live minimum bounded batch acceptance
P6-12 merge/close Phase 6
```

No product modification should begin before P6-00/P6-03 evidence locks the new lifecycle contract.

## 17. Acceptance target

Phase 6 first slice is accepted only when a small real Wordstat seed batch can prove:

```text
several distinct seeds execute once each
completed items persist
pause/resume does not replay completed items
worker restart does not replay completed items
unknown outcome is fail-closed/no-auto-retry
progress totals are correct
request/cost bound stops the queue
raw/normalized evidence remains available to ChatGPT
prior services regressions remain PASS
```

The acceptance gate tests the reliability of the hands, not the quality of ChatGPT's SEO judgment.

## 18. Authorized next action

Phase 5 is closed.

Authorized next implementation action:

```text
fetch exact current main
→ create Phase 6 dev branch
→ perform P6-00/P6-01 architecture audit
→ write tests/model contract before production runtime changes
```

In parallel, the Alice comparative methodology gate may be prepared/executed in a genuinely clean context. Its outcome controls Alice-specific engineering priority, not Phase 6.