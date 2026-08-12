# ROADMAP v0.1 — Yandex Marketing Bridge

Status: active roadmap.
Date: 2026-08-12.

## Governing development rule

**One phase = one service = one controlled live acceptance.**

No combined multi-service autorun is implemented as the development shortcut.

Within production use, one RUN is permanently bound to one active service. Sequential service runs belong to one JOB.

Every phase follows:

```text
research official API
→ define allowlist/protocol/policy
→ implement adapter
→ source/static tests
→ exact packaged-extension tests
→ controlled real Chrome + production ChatGPT test
→ regression of previous accepted phases
→ PASS gate
→ only then next phase
```

## PHASE 0 — REPOSITORY + REFERENCE + CORE DESIGN

Goal: establish source of truth and extract the generic architecture from the supplied Wordstat Bridge 1.1.5 reference without changing proven behavior.

Deliverables:

- repository structure `extension/` + `work/`;
- `extension/docs/` canonical documentation;
- immutable reference baseline stored under `extension/reference/`;
- documented hashes/provenance;
- unified CORE design;
- JOB/RUN workspace contract;
- policy/cost/quota abstractions;
- protocol detector/router skeleton design.

Gate:

- reference fully preserved and reproducible;
- no ambiguity about source of truth;
- no client secrets in repository;
- Phase 1 implementation plan approved by evidence/tests.

## PHASE 1 — WORDSTAT ADAPTER + UNIFIED CORE

Goal: migrate the already working Wordstat capability onto the unified Yandex Marketing Bridge CORE while preserving behavior.

Service:

```text
active_service = wordstat
```

Methods:

- getTop;
- getDynamics;
- getRegionsDistribution;
- getRegionsTree.

New common mechanisms exercised first on Wordstat:

- protocol detector;
- immutable active_service per run;
- credential-present vs autorun-enabled separation;
- missing credential → SKIPPED;
- request limit;
- money/cost limit;
- per-run/job accounting;
- persistent run event/cost evidence;
- workspace persistence for paid results;
- service-mismatch block.

Acceptance matrix includes:

- valid credential;
- missing credential;
- invalid command;
- unsupported method;
- autorun disabled;
- request limit;
- cost limit;
- duplicate block;
- duplicate tab;
- conversation isolation;
- Pause / Resume / Finish;
- occupied composer handling;
- uncertain request outcome no retry;
- exact result delivery;
- persistence of raw paid evidence.

GATE 1:

`WORDSTAT + UNIFIED CORE = LIVE PASS`.

No Search development before this gate.

## PHASE 2 — YANDEX SEARCH / SERP

Goal: add real Yandex SERP collection needed for semantic clustering, intent analysis and competitor/result overlap.

Service:

```text
active_service = search
```

Subphases:

### 2A — basic text search

- query;
- region;
- supported pagination/result count;
- normalized SERP evidence;
- raw response persistence.

### 2B — deferred search

- submit logical operation once;
- persist operation identity;
- documented status/result polling;
- no duplicate billable initiation;
- resume/recovery after extension/browser interruption where provable.

### 2C — Search policy classes

Separate operator toggles and limits for materially different priced/risk operation classes, including at minimum:

- deferred text;
- synchronous text;
- generative search if later enabled;
- other expensive classes only when explicitly added.

Default: expensive optional classes OFF.

GATE 2:

- Search live PASS;
- cost guard PASS;
- deferred single-initiation PASS;
- Wordstat full regression PASS.

## PHASE 3 — WEBMASTER

Goal: add real organic-search evidence from the customer site immediately, not as a later optional project.

Service:

```text
active_service = webmaster
```

Initial scope: READ-first.

Planned capability groups:

- user/account identity needed for API use;
- hosts/sites;
- host/site summary;
- search queries;
- query history / metrics;
- indexing/statistics;
- diagnostics;
- URLs / search URL status where useful;
- sitemaps where useful;
- basic vs extended/export analytics kept as distinct policy classes.

Required behavior:

- OAuth missing → SKIPPED, not global job failure;
- basic READ independent from expensive/extended access;
- extended export has separate quota/unit guard and default OFF when costly;
- raw and normalized evidence persisted to `work/<job_id>/`.

GATE 3:

- Webmaster live READ PASS;
- missing OAuth PASS;
- quota guard PASS;
- extended-operation block PASS;
- Wordstat/Search regressions PASS.

## PHASE 4 — METRIKA

Goal: add conversion and behavioral evidence required to judge campaign effectiveness instead of relying only on CTR/CPC.

Service:

```text
active_service = metrika
```

Subphases:

### 4A — READ

- counters available to current credential;
- goals;
- reports;
- traffic/source dimensions as required by orders;
- conversions;
- ecommerce when present and requested.

### 4B — async/large data capability where justified

Logs or other async workflows are separate operation classes with their own limits.

### 4C — WRITE only after READ is accepted

Management/write operations are separate permission profile and are never implied by Metrika READ autorun.

GATE 4:

- Metrika READ live PASS;
- rate/quota guard PASS;
- optional async workflow PASS if implemented;
- WRITE disabled-by-policy test PASS;
- regressions of phases 1–3 PASS.

## PHASE 5 — DIRECT READ

Goal: safely inspect and audit real Yandex Direct accounts before introducing any mutation.

Service:

```text
active_service = direct
permission_profile = READ
```

Planned capabilities:

- campaigns;
- ad groups;
- ads;
- keywords;
- negatives/settings relevant to audit;
- targeting/autotargeting where officially exposed;
- reports;
- actual search-query performance;
- API units/quota accounting.

Special requirement:

If reports are asynchronous, treat request initiation and report polling as one logical operation while forbidding blind duplicate initiation.

GATE 5:

- real/test account READ PASS;
- reports PASS;
- search-query report PASS;
- Direct units reserve/guard PASS;
- zero account mutation proven;
- previous-service regressions PASS.

## PHASE 6 — DIRECT DRAFT / PRE-LIVE WRITE

Goal: create campaign structures under a controlled write profile without unrestricted live advertising mutation.

Service:

```text
active_service = direct
permission_profile = DRAFT_WRITE
```

Implementation order:

1. campaign object creation in supported safe state;
2. groups;
3. ads;
4. keywords;
5. negative keywords;
6. required settings;
7. read-back verification.

Every write operation must follow:

```text
validated expected changes
→ one initiation
→ API result
→ READ BACK
→ compare expected vs actual
→ persist evidence
```

GATE 6:

- minimal test campaign PASS;
- larger structured campaign PASS;
- no accidental live spend/start PASS;
- read-back consistency PASS;
- all previous regressions PASS.

## PHASE 7 — DIRECT LIVE WRITE

Goal: support production changes only behind an explicit human approval gate.

No unrestricted live-write autorun.

Workflow:

```text
ChatGPT analysis
→ proposed CHANGESET
→ bridge validates affected client/account and operations
→ operator reviews diff
→ explicit approval for that transaction
→ execute once
→ verification READ
→ persist before/after evidence
```

Includes only methods individually researched, documented, allowlisted and tested.

GATE 7:

- safety review PASS;
- approval binding PASS;
- wrong-client protection PASS;
- replay protection PASS;
- post-write verification PASS;
- controlled live/test acceptance PASS.

## PHASE 8 — FULL KWORK ORDER E2E

Goal: execute one realistic order using sequential single-service runs and persistent GitHub evidence.

Example lifecycle:

```text
create work/<job_id>/
↓
RUN Wordstat
↓ Finish
RUN Search
↓ Finish
RUN Webmaster (if credential available)
↓ Finish
RUN Metrika (if available/required)
↓ Finish
RUN Direct READ (if account exists)
↓ Finish
ChatGPT analysis + deliverables
↓
RUN Direct DRAFT_WRITE if order requires campaign build
↓ Finish
final verification
↓
deliverables committed
↓
customer delivery/acceptance
↓
remove work/<job_id>/ from current tree
```

E2E acceptance must prove that losing/restarting the ChatGPT run does not require recollecting already persisted paid evidence.

## Regression gate after every phase

Minimum checks:

- source tests PASS;
- syntax/static PASS;
- exact packaged artifact PASS;
- Chrome extension load PASS;
- current production ChatGPT writing-block capture PASS;
- Manual operation PASS where supported;
- Autorun PASS;
- Pause / Resume / Finish PASS;
- duplicate-tab/owner protection PASS;
- conversation isolation PASS;
- missing credentials semantics PASS;
- disabled autorun semantics PASS;
- cost/quota guard PASS where relevant;
- result delivery PASS;
- paid/raw evidence persistence PASS where relevant;
- all previously accepted service regressions PASS.

## Current status

- Phase 0: IN PROGRESS.
- Phase 1+: NOT STARTED.
