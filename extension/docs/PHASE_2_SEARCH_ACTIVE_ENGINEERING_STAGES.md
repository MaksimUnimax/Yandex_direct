# PHASE 2 — SEARCH ACTIVE ENGINEERING STAGES

Status: **ACTIVE EXECUTION AUTHORITY**  
Adopted: 2026-08-20

This document fixes the remaining Phase-2 synchronous Search implementation work into four ordered engineering stages. These stages are not optional suggestions: they are the active execution plan and must be followed until owner/Codex intervention becomes genuinely necessary.

## Authority and already-completed foundation

Phase 1 Wordstat remains accepted on exact e13a.

Active development branch:

```text
dev/phase2-search-foundation-2026-08-19
```

The exact Phase-1 editable base was reconstructed and verified 45/45 before Search foundation changes.

Search foundation already completed before these four stages:

```text
SEARCH_API_V1 protocol/defaults/validation
Search XML Base64/UTF-8 normalization
search / SEARCH_API_V1 registration in shared service registry
focused Search tests
Phase-1 registry/test expectation corrections required by Search becoming a known service
```

Recorded verification evidence:

```text
extension/tests/phase2/search-foundation/FOUNDATION_EVIDENCE_2026-08-19.json
base identity: 45/45 PASS
focused Search: 32/32 PASS
affected tests: 86/86 PASS
full suite: 393/393 PASS
syntax: PASS
JSON: PASS
real Yandex requests: 0
```

Foundation production changes are limited to:

```text
shared/service_registry.js
shared/search_protocol.js
shared/search_xml.js
```

No owner action and no Codex browser measurement was required for foundation.

---

# STAGE 1 — SEARCH POLICY / COST / ADMISSION

Status: **NEXT / ACTIVE**

Goal: make Search an admitted paid service under the same fail-closed policy core as Wordstat, without initiating provider traffic in tests.

Required work:

```text
- Search Manual permission state
- Search Autorun permission state
- allowed Search method set (first slice: search only)
- per-RUN Search request limit
- per-RUN estimated RUB limit
- conservative synchronous Search cost reservation
- tariff snapshot/source metadata plumbing
- pre-network policy rejection with request_executed=false
- budget reservation before irreversible provider initiation
- one immutable service per Autorun RUN
- paused-RUN Manual Search uses the same RUN budget; no bypass
```

Required failure semantics:

```text
validation / policy / credential-capability rejection before provider initiation
→ request_executed=false
→ automatic_retry=false
→ provider initiations=0
```

Required tests include positive admission, each local rejection class, budget boundary, service isolation and no-network assertions.

Exit criterion:

```text
focused policy/admission tests PASS
existing Wordstat policy behavior remains PASS
no real Yandex request
```

---

# STAGE 2 — WORKER / PROVIDER EXECUTION INTEGRATION

Status: **QUEUED AFTER STAGE 1**

Goal: route an admitted Search command through the existing worker-owned exactly-once provider lifecycle.

Required work:

```text
- Search credential/folder capability resolution from operator-local settings
- build POST https://searchapi.api.cloud.yandex.net/v2/web/search
- Authorization remains local and never enters assistant command/result/debug/GitHub
- request body produced by SearchProtocol.buildRequest
- exactly one provider initiation for one admitted command
- HTTP 2xx → decode rawData → XML normalization → SEARCH_RESULT_V1
- HTTP 4xx/5xx after initiation → ERROR, request_executed=true, no automatic retry
- timeout/network/session ambiguity after initiation → truthful UNKNOWN semantics, no blind retry
- cost/request reservation retained conservatively across uncertain outcome
- Search result/error delivered through existing worker-owned outbox
- existing conversation binding / owner-tab / single-flight / irreversible fences reused
```

Do not fork a Search-specific composer or delivery subsystem.

Required tests include accepted request count=1, pre-network count=0, HTTP error count=1/no retry, UNKNOWN count<=1/no retry, Search result normalization and outbox delivery.

Exit criterion:

```text
focused worker/provider tests PASS
Wordstat worker regressions PASS
no real Yandex request
```

If a browser/DOM/runtime fact is unknown, stop only at that exact uncertainty and issue a concrete Codex measurement prompt. Do not guess.

---

# STAGE 3 — OPERATOR SETTINGS / POPUP / LOAD WIRING

Status: **QUEUED AFTER STAGE 2**

Goal: expose Search through the existing operator control plane without weakening Wordstat or leaking secrets.

Required work:

```text
- Search service availability in operator settings
- Search Manual allowed toggle/state
- Search Autorun allowed toggle/state
- Search method allowance
- Search request/RUB limits
- local folderId / credential capability wiring as required by the existing credential model
- public settings state excludes secrets
- Export/Import preserves governed Search settings under existing secret-handling rules
- manifest/script import order loads Search XML/protocol before consumers that require them
- popup state transitions preserve existing Manual ON transaction ordering
- no Search setting may silently mutate Wordstat settings
```

Required tests include popup reopen persistence, settings round-trip, export/import, redaction, load order and Wordstat non-regression.

Exit criterion:

```text
focused settings/popup/load tests PASS
existing popup/runtime tests PASS
no real Yandex request
```

Any unknown actual ChatGPT DOM/control behavior must be measured by Codex, not invented.

---

# STAGE 4 — MANUAL SEARCH END-TO-END INTEGRATION / LOCAL REGRESSION / FREEZE PREP

Status: **QUEUED AFTER STAGE 3**

Goal: prove the full controlled Search Manual path inside the extension architecture and prepare the exact candidate for independent Codex gate execution.

Required controlled path:

```text
SEARCH_API_V1 block
→ registered Search service
→ external Yandex action / accepted Manual path
→ worker admission
→ Search policy + budget + credential capability
→ exactly one mocked provider initiation
→ Search XML normalization
→ SEARCH_RESULT_V1
→ worker outbox
→ existing composer delivery lifecycle
```

Required controlled checks:

```text
- native Copy remains independent
- Manual ON final state remains ON when worker authority accepts it
- one click creates at most one provider initiation
- occupied composer protection remains intact
- committed Send remains at most once
- result and error both release Manual operation state
- sequential Wordstat ↔ Search commands remain service-isolated
- no blind retry
- YMB_ERROR_V1 behavior remains always-on for bound errors
- Debug remains redacted
- source full suite PASS
- syntax PASS
- JSON PASS
- exact target tree identity recorded
- real Yandex requests = 0 during development verification
```

After local development verification:

```text
1. freeze exact combined Wordstat+Search candidate source;
2. build deterministic candidate artifact;
3. execute mandatory artifact transport consumer-conformance runbook;
4. only after exact artifact transport proof prepare the Codex full-gate prompt;
5. Codex independently verifies the exact candidate and runs the complete Phase-1 + Phase-2 gate;
6. only after Codex PASS ask owner for the minimal paid real-Yandex Search acceptance.
```

Stage 4 is the first point at which Codex full-gate execution is mandatory. Codex measurement may be requested earlier only for a genuinely unknown browser/DOM/runtime fact.

Exit criterion:

```text
LOCAL DEVELOPMENT COMPLETE
EXACT CANDIDATE FROZEN
ARTIFACT TRANSPORT PROVEN
AUTHORIZED_NEXT_STAGE = CODEX_PHASE_2_COMPLETE_PRE_DELIVERY_FULL_GATE
```

---

# Execution rule

ChatGPT continues through these stages without stopping for micro-confirmations.

Stop and require outside intervention only when one of these is true:

```text
A. a browser/DOM/runtime fact is genuinely unknown → request concrete Codex measurement;
B. controlled implementation is complete and exact candidate is ready → request Codex complete pre-delivery gate;
C. Codex gate passes and a real paid Yandex Search call is required → request owner live action;
D. owner explicitly pauses/changes scope.
```

Never replace an unknown fact with a guess.
