# PHASE 2 — FOUR-STAGE EXECUTION CONTROL

Status: **ACTIVE / STAGE 4**  
Effective: 2026-08-20.  
Stage-3 transition recorded: 2026-08-24.

This document is the mandatory execution/checkpoint structure for Phase 2 Yandex Search / SERP. It exists to prevent long uncheckpointed work from being lost when the chat/tool session is interrupted.

## Operating rule

Phase 2 is split into exactly four engineering stages.

For every stage:

1. ChatGPT works continuously inside the stage without turning internal subtasks into new stages.
2. Unknown browser/DOM/runtime facts MUST NOT be guessed. If such a fact is required, stop at that uncertainty and request a concrete Codex measurement.
3. Product/test changes and exact verification evidence must be committed/preserved in GitHub during the stage.
4. When a stage reaches its exit criteria, ChatGPT MUST write a durable GitHub checkpoint/evidence record, update `extension/docs/CURRENT_STATE.md`, and send the owner one concise stage-completion report.
5. After the stage report, continue into the next stage automatically unless the owner pauses, owner-live action is required, Codex action is required, or a real external blocker prevents correct work.
6. Do not stop merely because a subtask or small group of tests completed.
7. Do not issue repeated micro-step status chatter between stage boundaries.

Current owner testing correction applies throughout this control document:

```text
while product bytes are changing
→ focused tests for changed behavior + directly affected regressions + required syntax/static checks

Stage 4 frozen handoff candidate
→ exact artifact preparation
→ one complete pre-delivery regression campaign
```

The older Stage-3 wording that implied a whole-product/full-source campaign during active development is superseded by this owner correction; broad combined regression belongs to Stage 4 after freeze.

Implementation lineage:

```text
repo: MaksimUnimax/Yandex_direct
Phase-1 accepted base: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
current candidate branch: candidate/phase2-search-reconstruction-2026-08-23
```

---

# STAGE 1 — EXACT BASE + SEARCH FOUNDATION

Status: **PASS / COMPLETED**

Purpose: establish a byte-authoritative Phase-2 base and implement provider-independent Search protocol foundation.

Completed evidence:

```text
base e13a materialization: 45/45 exact; mismatches 0; missing 0; extras 0
Stage-1 target files: 50
Stage-1 target manifest SHA-256: 62bd5846c8f7d6ade7f788d4394d79e02e802611144a4249761ccbb07397b98b

product foundation:
  shared/service_registry.js
  shared/search_protocol.js
  shared/search_xml.js

focused Search: 32/32 PASS
affected suite: 86/86 PASS
full suite: 393/393 PASS
syntax: PASS
JSON: PASS
real Yandex requests: 0
```

Durable evidence:

```text
extension/tests/phase2/search-foundation/FOUNDATION_EVIDENCE_2026-08-19.json
extension/tests/phase2/search-foundation/target-tree-sha256.tsv
extension/tests/phase2/search-foundation/phase2-search-foundation.patch.gz.b64
```

Known foundation commits include:

```text
6d0c1c2bdbfb9e2b18b32adb25a0c5885f932f2e
01f777c7a1e0e06efcb1338c403ea69c86e3d4e8
e52f6fae18b53cb90306a5dab643568bfaa00f27
69a92de2841a67bee05f347bc8389d81bc4e51eb
```

Stage-1 exit criteria are satisfied.

---

# STAGE 2 — WORKER / PROVIDER / CREDENTIAL / POLICY EXECUTION

Status: **PASS / COMPLETED**

Purpose: make one accepted Search command executable through worker/provider with correct credential, cost, policy, exactly-once and no-blind-retry semantics, with zero real Yandex traffic during development verification.

Completed product scope:

```text
Search protocol/XML runtime loading in worker
SEARCH_API_V1 -> search worker routing
Search credential capability using existing local API key + folderId
POST https://searchapi.api.cloud.yandex.net/v2/web/search
no credential/folderId exposure in assistant command/result command
Authorization/API-key redaction
one provider initiation exactly per accepted command
pre-provider validation/credential/policy rejection -> zero initiation
HTTP provider error -> ERROR / request_executed=true / automatic_retry=false
ambiguous initiated network failure -> request_executed=UNKNOWN / automatic_retry=false
response-normalization failure after HTTP success -> executed=true / no retry
conservative Search guard 0.488 RUB/request
request-count + RUB run-budget enforcement
cost/request reservation before provider initiation
Search/Wordstat routing isolation
```

Exact Stage-2 target:

```text
target files: 51
target manifest SHA-256: a274600440461cc7ac4669e959d3b84ee6dfaa9dffb26219ee7e1dd0086f8236
fresh git apply --check: PASS
fresh target identity: 51/51 exact; mismatches 0; missing 0; extras 0

service_worker.js:
  def73ebb44243b57d0be98ad21fec6ccf230cc2dfe1b29f8ee3588e17fe80282 / 190920
shared/credential_registry.js:
  506aafca071522c7dc110dd72feec4d7fbee36119849abac69158c9be232a311 / 1413
shared/policy_model.js:
  c97c2b8dd600091f894d2c7c5c0fb91a6408d5cc848bc579ec3acc6cb59d99bf / 6086
```

Verification:

```text
focused Search Stage 2: 10/10 PASS
full source suite: 377/377 PASS
syntax: 46/46 PASS
JSON: 2/2 PASS
real Yandex requests: 0
```

Durable evidence on the development branch:

```text
extension/tests/phase2/search-worker-provider/STAGE2_EVIDENCE_2026-08-20.json
```

Stage-2 exit criteria are satisfied.

---

# STAGE 3 — MANUAL / AUTORUN / OPERATOR / DELIVERY INTEGRATION

Status: **PASS / COMPLETED**

Purpose: integrate Search into the already accepted common user/runtime surfaces without creating a second DOM/composer/delivery implementation.

Required common-core integration is present and preserved:

```text
popup active-service handling for Search
Search Manual permission/control
Search Autorun permission/control
allowed Search methods
Search request and RUB limits
external `Яндекс` action on eligible SEARCH_API_V1 blocks
native Copy independence
real Manual state machine reuse
owner-tab fence
conversation binding
single-flight admission
one immutable service per Autorun RUN
Wordstat RUN cannot execute Search
Search RUN cannot execute Wordstat
worker-owned durable outbox
composer occupied protection
committed Send at most once
ready/Microphone completion
watch-only committed recovery
YMB_ERROR_V1 delivery
Debug redaction
Export/Import compatibility for Search settings/credentials
runtime crash recovery and no-blind-retry fences
```

Final focused development checkpoint:

```text
Stage-3 production HEAD: 75d18291224069a6ae67c110498481ec7320d3c0
service_worker.js blob: 87b90dcb0a1ecca8afc5587d8ab7f6ddfd2c241a
workflow: phase2-focused-development
run: 32703002791
job: 97358197549
focused Stage-3 tests: 77/77 PASS
fail: 0
service_worker.js syntax: PASS
popup.js syntax: PASS
workflow contents permission: read
owner-live Search requests: 0
```

The last proven Stage-3 defect was the worker-restart window after persisting an Autorun in `STARTING` but before persisting its `autorun_start` outbox. Commit `75d1829…` restores exactly one missing start delivery, preserves an existing matching outbox and performs no provider initiation.

Durable checkpoint:

```text
extension/tests/PHASE_2_STAGE_3_FOCUSED_CHECKPOINT_2026-08-24.md
```

Per the current owner testing rule, this focused development closure does not pretend to be the combined pre-delivery full regression certificate. The complete Wordstat+Search regression campaign is a Stage-4 requirement on the frozen exact candidate.

Stage-3 exit criteria are satisfied under the current focused-development authority.

---

# STAGE 4 — FROZEN CANDIDATE + EXACT TRANSPORT + CODEX FULL GATE + OWNER LIVE

Status: **ACTIVE / AUTHORIZED**

Purpose: freeze one exact combined candidate, prove exact artifact transport, run complete Codex regression, then perform only irreducible owner-live Search acceptance.

Required scope:

```text
freeze exact combined candidate source
production/test hashes + exact target manifest
deterministic package + ZIP integrity/source-package identity
mandatory QA transport runbook
consumer-conformance round trip before Codex prompt
exact SHA-256/bytes/files/entries from Codex-accessible transport
complete Phase-1 + Phase-2 Codex gate
zero real Yandex traffic during controlled gate
any production-byte change after gate invalidates the gate
```

After exact Codex PASS:

```text
prepare exact owner artifact
fresh official Search pricing check immediately before paid live command
owner tests one real Search command at a time
no blind retry
record owner-live PASS/FAIL
```

Stage-4 / Phase-2 exit criteria:

```text
exact candidate identity PASS
Codex full regression gate PASS
production bytes unchanged since gate
owner real-profile Search functional acceptance PASS
Phase 2 Search LIVE PASS / CLOSED
```

---

# Current execution pointer

```text
STAGE 1 = PASS / COMPLETED
STAGE 2 = PASS / COMPLETED
STAGE 3 = PASS / COMPLETED
STAGE 4 = ACTIVE / AUTHORIZED
```

The next work belongs to **Stage 4 only**. Do not reopen Stage 3 merely to search for additional adjacent edge cases; Stage 3 reopens only for a proven regression or a Stage-4 gate failure classified to the product layer.
