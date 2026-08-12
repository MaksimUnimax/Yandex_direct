# ROADMAP v0.2 — Yandex Marketing Bridge

Status: active roadmap.
Date: 2026-08-12.

## Governing development rule

**One phase = one service = one controlled live acceptance.**

Within production use:

```text
one RUN = one immutable active SERVICE
multiple sequential RUNs = one JOB/order
```

No new service starts until the current service passes:

```text
official API research
→ protocol/allowlist/policy definition
→ implementation
→ source tests
→ exact packaged-extension tests
→ controlled real Chrome + production ChatGPT acceptance
→ regression of all earlier accepted services
→ PASS gate
```

## PHASE 0 — REPOSITORY + REFERENCE + CORE DESIGN

**Status: PASS — completed 2026-08-12.**

Completed:

- repository source of truth `MaksimUnimax/Yandex_direct`;
- permanent `extension/` and temporary `work/` split;
- canonical documentation under `extension/docs/`;
- append-only development context;
- exact owner-supplied reference identification and hashes;
- fresh reference extraction and 283/283 test PASS;
- exact 41-file reference inventory;
- known stale 1.1.5 result-version defect documented;
- CORE extraction map;
- Job/Run/policy/cost architecture;
- Phase 1 implementation plan.

Reference authority:

```text
wordstat-bridge-v1.1.5-full-function-environment-audit(4).zip
SHA-256 a39bbe65b046ef6eac5a7890b8afd84e69550db34debf271b7c373d08a1fef1a
```

## PHASE 1 — WORDSTAT ADAPTER + UNIFIED CORE

Service:

```text
active_service = wordstat
```

Supported methods:

- getTop;
- getDynamics;
- getRegionsDistribution;
- getRegionsTree.

### Phase 1 implementation scope

Implemented in the pre-live candidate:

- unified product identity/version `0.1.0`;
- service registry with **Wordstat only**;
- trusted Job ID;
- immutable active service per run;
- credential capability separated from autorun permission;
- missing credentials → controlled `SKIPPED / NO_CREDENTIALS`, zero fetch;
- operator-controlled Wordstat Autorun permission;
- allowed-method policy;
- hard request limits per run/job;
- hard estimated-cost limits per run/job;
- method tariff snapshot/configuration;
- run/job request and cost accounting;
- result provenance: product/service/operation/job/run/cost;
- corrected authoritative result version `0.1.0`;
- Manual cost guard so Manual cannot bypass Job ceilings;
- reference conversation binding, owner-tab, single-flight, commit/reconciliation and no-retry semantics retained;
- four proven Business Bridge common modules preserved by exact hash.

### Pre-live evidence

Exact candidate:

```text
yandex-marketing-bridge-0.1.0-phase1-wordstat-candidate.zip
SHA-256 79c2bca5e2e65aaa1cb7cc38754589a0bf3b0b436c82f36416934cd175cafa2a
```

Automated/pre-live status:

```text
source full suite:          299/299 PASS
fresh ZIP full suite:       299/299 PASS
source ↔ fresh ZIP:          41/41 byte-identical
fresh ZIP JS/MJS syntax:     36/36 PASS
manifest/package JSON:        2/2 PASS
Chromium 144 load smoke:     PASS
```

The full 299 consists of migrated reference regression coverage plus 16 new Phase 1 unified-core tests.

### Phase 1 current gate

**Status: PRE-LIVE PASS / PRODUCTION CHATGPT LIVE ACCEPTANCE PENDING.**

Required live procedure is canonicalized in:

```text
extension/docs/PHASE_1_LIVE_ACCEPTANCE.md
```

It must prove at minimum:

- current production ChatGPT Copy/writing-block behavior;
- missing-credential SKIP with zero Yandex request;
- operator-disabled/cost-limit guards with zero request;
- one real free Wordstat network request if still officially free at test time;
- one minimal paid Wordstat request after fresh official price check;
- exactly-once request/delivery;
- correct version/job/run/cost provenance;
- immediate persistence of paid raw evidence to `work/<job_id>/` through connected GitHub;
- Pause/Resume/Finish;
- duplicate-tab/conversation ownership;
- Manual cannot bypass Job cost ceiling.

### GATE 1

```text
WORDSTAT + UNIFIED CORE = LIVE PASS
```

**Not passed yet. Search development is blocked until the operator live test passes.**

## PHASE 2 — YANDEX SEARCH / SERP

**Status: BLOCKED BY PHASE 1 LIVE GATE.**

Goal after unlock: add real Yandex SERP evidence for semantic clustering, intent analysis and competitor/result overlap.

Service:

```text
active_service = search
```

Planned subphases:

### 2A — basic text search

- query;
- region;
- supported pagination/result count;
- raw + normalized SERP evidence.

### 2B — deferred search

- submit billable logical operation once;
- persist operation identity;
- documented status/result polling;
- never duplicate paid initiation during recovery.

### 2C — operation-cost classes

Separate operator toggles/limits for materially different priced classes such as deferred, synchronous and any later generative operation.

Expensive optional classes default OFF.

GATE 2 requires Search live PASS + cost guard PASS + deferred single-initiation PASS + Wordstat regression PASS.

## PHASE 3 — WEBMASTER

**Status: BLOCKED.**

Service:

```text
active_service = webmaster
```

READ-first scope:

- user/account identity;
- hosts/sites;
- host summary;
- search queries and history/metrics;
- indexing/statistics;
- diagnostics;
- useful URL/sitemap data;
- basic and extended/export analytics as separate policy classes.

Required behavior:

- OAuth missing → SKIPPED, not Job failure;
- extended/costly access separate and default-protected;
- raw/normalized evidence persisted to `work/<job_id>/`.

## PHASE 4 — METRIKA

**Status: BLOCKED.**

Service:

```text
active_service = metrika
```

Order:

1. READ — counters, goals, reports, sources, conversions, ecommerce when present;
2. async/large-data operations as a separate limited class if justified;
3. WRITE only after READ acceptance and under a separate permission profile.

## PHASE 5 — DIRECT READ

**Status: BLOCKED.**

Service:

```text
active_service = direct
permission_profile = READ
```

Planned:

- campaigns;
- groups;
- ads;
- keywords/negatives/settings;
- targeting/autotargeting when officially exposed;
- reports;
- actual search-query performance;
- Direct units/quota guard.

Zero account mutation must be proven before write development begins.

## PHASE 6 — DIRECT DRAFT / PRE-LIVE WRITE

**Status: BLOCKED.**

Service:

```text
active_service = direct
permission_profile = DRAFT_WRITE
```

Implementation order:

```text
campaign
→ groups
→ ads
→ keywords
→ negative keywords
→ settings
→ READ BACK verification
```

Every write:

```text
validated expected changes
→ one initiation
→ result
→ read back
→ compare expected vs actual
→ persist evidence
```

## PHASE 7 — DIRECT LIVE WRITE

**Status: BLOCKED.**

No unrestricted live-write autorun.

Required flow:

```text
ChatGPT proposed CHANGESET
→ bridge validates client/account/operations
→ operator reviews exact diff
→ explicit transaction approval
→ execute once
→ verification READ
→ persist before/after evidence
```

## PHASE 8 — FULL KWORK ORDER E2E

**Status: BLOCKED.**

Target lifecycle:

```text
create work/<job_id>/
↓
RUN Wordstat → Finish
RUN Search → Finish
RUN Webmaster if available → Finish
RUN Metrika if available/needed → Finish
RUN Direct READ if available → Finish
↓
ChatGPT analysis + deliverables
↓
RUN Direct DRAFT_WRITE if required
↓
final verification and delivery
↓
customer accepts
↓
remove work/<job_id>/ from current tree
```

E2E must prove previously persisted paid evidence survives chat/browser/context loss and is reused instead of recollected.

## Regression gate after every phase

Minimum:

- source tests PASS;
- syntax/static PASS;
- exact packaged artifact PASS;
- source↔package identity evidence;
- Chromium extension load PASS;
- current production ChatGPT writing-block capture PASS;
- Manual/Autorun lifecycle PASS where supported;
- Pause/Resume/Finish PASS;
- duplicate-tab/owner protection PASS;
- conversation isolation PASS;
- missing-credential semantics PASS;
- disabled autorun semantics PASS;
- cost/quota guard PASS where relevant;
- result delivery PASS;
- paid/raw evidence persistence PASS where relevant;
- all previously accepted service regressions PASS.

## Current status summary

```text
PHASE 0  PASS
PHASE 1  PRE-LIVE PASS / PRODUCTION LIVE PENDING
PHASE 2  BLOCKED
PHASE 3  BLOCKED
PHASE 4  BLOCKED
PHASE 5  BLOCKED
PHASE 6  BLOCKED
PHASE 7  BLOCKED
PHASE 8  BLOCKED
```
