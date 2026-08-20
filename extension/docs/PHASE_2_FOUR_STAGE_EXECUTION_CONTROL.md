# PHASE 2 — FOUR-STAGE EXECUTION CONTROL

Status: **ACTIVE / OWNER-ORDERED EXECUTION CONTROL**  
Effective: 2026-08-20.

This document is the mandatory execution/checkpoint structure for Phase 2 Yandex Search / SERP.

It exists to prevent long uncheckpointed work from being lost when the chat/tool session is interrupted.

## Operating rule

Phase 2 is split into exactly four engineering stages.

For every stage:

1. ChatGPT works continuously inside the stage without sending micro-step progress messages.
2. Unknown browser/DOM/runtime facts MUST NOT be guessed. If such a fact is required, stop at that uncertainty and request a concrete Codex measurement.
3. Product/test changes and exact verification evidence must be committed/preserved in GitHub during the stage.
4. When a stage reaches its exit criteria, ChatGPT MUST:
   - write a durable GitHub checkpoint/evidence record;
   - update `extension/docs/CURRENT_STATE.md` with the completed stage and exact next stage;
   - send the owner one concise stage-completion report.
5. After the stage report, continue into the next stage automatically unless:
   - the owner explicitly pauses/stops work;
   - owner live action is required;
   - Codex measurement or Codex gate execution is required;
   - a real external blocker prevents further correct work.
6. Do not stop merely because a subtask or small group of tests completed.
7. Do not issue repeated status chatter between stage boundaries.

The current implementation lineage is:

```text
repo: MaksimUnimax/Yandex_direct
Phase-1 accepted base: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
development branch: dev/phase2-search-foundation-2026-08-19
```

---

# STAGE 1 — EXACT BASE + SEARCH FOUNDATION

Status: **PASS / COMPLETED**

Purpose: establish a byte-authoritative Phase-2 base and implement the provider-independent Search protocol foundation before touching worker/provider/runtime integration.

Required scope:

```text
exact editable e13a base materialization
45/45 base identity verification
SEARCH_API_V1 service registration
strict Search command parse/validation/defaults
synchronous /v2/web/search request-body builder
Base64 UTF-8 FORMAT_XML normalization
stable SEARCH_RESULT_V1 envelope helpers
focused Search tests
Phase-1 test corrections required by Search registration
full source regression
syntax + JSON validation
zero real Yandex traffic
```

Completed evidence:

```text
base artifact SHA-256:
  e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65

base materialization:
  45/45 exact
  identity mismatches: 0
  missing: 0
  extras: 0

new/changed foundation product surfaces:
  shared/service_registry.js
  shared/search_protocol.js
  shared/search_xml.js

verification:
  focused Search: 32/32 PASS
  affected after registry-test correction: 86/86 PASS
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

Foundation commits already present in the Phase-2 development lineage include:

```text
6d0c1c2bdbfb9e2b18b32adb25a0c5885f932f2e  phase2: add SEARCH_API_V1 protocol foundation
01f777c7a1e0e06efcb1338c403ea69c86e3d4e8  phase2: add Search XML normalization foundation
e52f6fae18b53cb90306a5dab643568bfaa00f27  phase2: register Search protocol in service registry
69a92de2841a67bee05f347bc8389d81bc4e51eb  phase2: add exact Search foundation patch transport
```

Stage-1 exit criteria are satisfied.

---

# STAGE 2 — WORKER / PROVIDER / CREDENTIAL / POLICY EXECUTION

Status: **ACTIVE / NEXT ENGINEERING STAGE**

Purpose: make one accepted Search command execute through the worker/provider layer with correct credential, cost, policy, exactly-once and no-blind-retry semantics, while still avoiding real Yandex traffic in development tests.

Required scope:

```text
load Search protocol/XML modules in the installable runtime
worker router: SEARCH_API_V1 -> search service
Search credential capability + local folderId usage
no credentials/folderId in assistant command or result
POST https://searchapi.api.cloud.yandex.net/v2/web/search
Authorization redaction
exactly one provider initiation per accepted command
validation/policy/credential rejection -> zero provider initiation
HTTP 4xx/5xx -> truthful ERROR, request_executed=true, automatic_retry=false
ambiguous timeout/network/session-loss outcome -> UNKNOWN semantics, no retry
Search conservative cost reservation before provider initiation
Search request-count and RUB budget enforcement
Wordstat/Search routing isolation
focused worker/provider/policy tests
full regression after integration
zero real Yandex traffic
```

Stage-2 exit criteria:

```text
all focused Search worker/provider/policy tests PASS
exactly-once and no-blind-retry contours PASS
credential and secret-redaction tests PASS
budget/cost reservation tests PASS
Wordstat regressions PASS
full source suite PASS
syntax/JSON PASS
real Yandex requests = 0
GitHub stage checkpoint written
CURRENT_STATE advanced to Stage 3
owner receives concise Stage-2 completion report
```

---

# STAGE 3 — MANUAL / AUTORUN / OPERATOR / DELIVERY INTEGRATION

Status: **PENDING STAGE 2 PASS**

Purpose: integrate Search into the already accepted common user/runtime surfaces without creating a second DOM/composer/delivery implementation.

Required reuse and integration:

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
```

Browser/DOM rule for this stage:

```text
if an integration decision depends on an unknown current ChatGPT DOM/browser fact:
  DO NOT GUESS
  preserve the exact uncertainty
  issue a concrete Codex measurement prompt
  resume only from measured evidence
```

Stage-3 exit criteria:

```text
Search Manual integration tests PASS
Search Autorun integration tests PASS
Search result/error delivery tests PASS
Search/Wordstat service isolation PASS
popup/settings/export/import regressions PASS
existing Phase-1 Copy/Manual/outbox/conversation regressions PASS
full source suite PASS
syntax/JSON PASS
real Yandex requests = 0
GitHub stage checkpoint written
CURRENT_STATE advanced to Stage 4
owner receives concise Stage-3 completion report
```

---

# STAGE 4 — FROZEN CANDIDATE + EXACT TRANSPORT + CODEX FULL GATE + OWNER LIVE

Status: **PENDING STAGE 3 PASS**

Purpose: convert the completed combined Wordstat+Search source into one exact candidate, prove exact artifact transport to Codex, run the complete regression gate, then perform only irreducible owner-live Search acceptance.

Required scope:

```text
freeze exact combined candidate source
production/test hashes and exact target manifest
package candidate deterministically
verify archive readability/file count/source-package identity
execute mandatory QA transport runbook
consumer-conformance round-trip before Codex prompt
prove exact SHA-256 + bytes + file/entry counts from Codex-accessible transport
issue Codex full-gate prompt only after transport proof
Codex runs complete Phase-1 + Phase-2 gate
Search gate additions include protocol, credential, policy/cost, exactly-once, HTTP/UNKNOWN no-retry, XML, Manual, Autorun, service isolation and packaged behavior
zero real Yandex traffic during controlled Codex gate
any production-byte change after gate invalidates that gate
```

After exact Codex PASS:

```text
prepare exact owner handoff artifact
freshly verify official Yandex Search pricing immediately before each paid live command
owner tests one real Search functional command at a time
no blind retry
classify evidence before any second request
record owner-live PASS/FAIL in GitHub
```

Stage-4 / Phase-2 exit criteria:

```text
exact candidate identity PASS
Codex full regression gate PASS
production bytes unchanged since gate
owner real-profile Search functional acceptance PASS
Phase 2 Search marked LIVE PASS / CLOSED
next service phase may then be unlocked by governance
```

---

# Current execution pointer

```text
STAGE 1 = PASS / COMPLETED
STAGE 2 = ACTIVE / IN WORK
STAGE 3 = PENDING
STAGE 4 = PENDING
```

The next engineering work belongs to **Stage 2 only**. Do not skip directly to popup/live/Codex work before Stage-2 exit criteria are satisfied.