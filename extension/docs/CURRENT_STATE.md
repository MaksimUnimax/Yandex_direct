# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH REOPENED — CONTEXT-RECOVERY EXACT FREEZE PASS / WINDOWS TRANSPORT REQUIRED**  
Updated: 2026-08-25

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_THIS_STATE_WRITE = bef10dcc4c379d2e9247af4dc14365443b7f59f7
LAST_COMPLETE_ACCEPTED_PRODUCT_SOURCE = 10bb3aca67295e5e515ff2ade8914b23e8458ca7
LAST_COMPLETE_ACCEPTED_ARTIFACT = 0186b35d66cf1e7e20a522dc128b3fdd317cd660c665b8294120a1ab8affe91d / 171655 bytes / 66 files / 69 ZIP entries
LATEST_COMPLETE_GATE = PASS on exact 0186b35d... candidate; run 32730308190 / job 97440819536
CURRENT_FROZEN_PRODUCT_SOURCE = f4aee34c0a3455aa7199f6aa54bd581c71d97337
CURRENT_FROZEN_ARTIFACT = 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46 / 175971 bytes / 68 files / 71 ZIP entries
CURRENT_FROZEN_PAYLOAD_MANIFEST = bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478 / 11933 bytes
CURRENT_FREEZE_GATE = PASS; run 32799665340 / job 97657914686
FOCUSED_CONTEXT_RECOVERY_GATE = PASS; source 239/239; Chrome 151 real action popup; run 32799117004 / job 97656378411
PRODUCTION_BYTES_CHANGED_SINCE_CURRENT_FREEZE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_CURRENT_FREEZE = NO
OWNER_LIVE = BLOCKED
REAL_OWNER_LIVE_SEARCH_REQUESTS_SINCE_DEFECT = 0
OPEN_BLOCKERS = exact current artifact has not yet received Windows-safe transport and one new complete governed gate
AUTHORIZED_NEXT_STAGE = WINDOWS_SAFE_EXACT_TRANSPORT
```

## Previous accepted repaired baseline

The Chrome-151 popup geometry repair was fully accepted before the current context-recovery defect was found.

```text
source: 10bb3aca67295e5e515ff2ade8914b23e8458ca7
artifact: yandex-marketing-bridge-0.1.1-phase2-search-popup-fix-candidate.zip
artifact SHA-256: 0186b35d66cf1e7e20a522dc128b3fdd317cd660c665b8294120a1ab8affe91d
artifact bytes: 171655
files: 66
ZIP entries: 69
payload manifest SHA-256: 447bf18e54ba4a728cc6255adff5e13996366b9bf54b2668114110d525501009
payload manifest bytes: 11601
complete-gate run: 32730308190
complete-gate job: 97440819536
```

That artifact is historical baseline evidence only and cannot authorize owner-live after the context-recovery production change.

The still older `0ee1d38... / d58b5bd...` candidate remains revoked.

## Owner-live defect authority — ChatGPT context recovery

Owner-live failed before the Search provider boundary when the unpacked extension became active after a ChatGPT conversation tab was already open. The existing page had no receiver for the new extension runtime, so the popup could not identify the conversation and Bind/Manual became unusable. No paid Search request occurred.

Focused product branch:

```text
branch: fix/phase2-chat-context-self-recovery-2026-08-24
PR: #13
focused PASS product/QA head: f77e91fcff75b85290e012ffec79123aa7fc9f0e
accepted baseline source: 10bb3aca67295e5e515ff2ade8914b23e8458ca7
```

Repair behavior:

```text
- identify the active supported ChatGPT tab;
- try ordinary WS_GET_IDENTITY first;
- only on missing receiver, inject the exact manifest content bundle with chrome.scripting.executeScript;
- retry identity after deterministic injection;
- start normal popup runtime only after bootstrap finishes;
- keep bootstrap failure visible instead of allowing a later false ready state;
- expose only sanitized recovery diagnostics;
- do not change Search/Wordstat provider, routing, budget, retry, Manual transaction, Autorun transaction, or delivery semantics.
```

## Focused Chrome-151 PASS

```text
workflow: phase2-context-recovery-focused
run: 32799117004
job: 97656378411
Windows Server 2025
Chrome for Testing: 151.0.7922.47
Puppeteer: 25.4.0
source suite: 239/239 PASS
real Yandex requests: 0
```

The browser venue reproduced the real ordering directly:

```text
ChatGPT opens first
→ unpacked extension loads afterwards through CDP Extensions.loadUnpacked
→ original ChatGPT DOM remains open and unchanged
→ Chrome tab target selected
→ Extensions.triggerAction invokes the real extension action
→ real popup opens
→ missing receiver reproduced
→ bootstrapResult.attempted=true
→ bootstrapResult.recovered=true
→ Bind PASS
→ Manual ON PASS
```

## Current clean candidate source

Candidate branch:

```text
candidate/phase2-context-recovery-2026-08-25
source: f4aee34c0a3455aa7199f6aa54bd581c71d97337
```

Relative to accepted repaired baseline `10bb3aca...`, the clean candidate differs by exactly six files:

```text
extension/src/manifest.json
extension/src/popup.html
extension/src/popup_context_bootstrap.js
extension/tests/candidate_readiness_recovery.test.mjs
extension/tests/popup_context_bootstrap.test.mjs
extension/tests/popup_error_boundary_recovery.test.mjs
```

No focused workflow/browser harness bytes are part of the clean candidate.

## Exact context-recovery freeze PASS

Durable authority:

```text
extension/tests/PHASE_2_CONTEXT_RECOVERY_FREEZE_PASS_2026-08-25.md
workflow: phase2-context-recovery-freeze
run: 32799665340
job: 97657914686
QA-only PR: #14
```

Freeze gates:

```text
exact six-file source authority: PASS
source suite: 239/239 PASS
source syntax files: 22 PASS
source JSON: PASS
deterministic double build: PASS
packaged suite: 239/239 PASS
packaged syntax: 62 PASS
packaged JSON: 2 PASS
ZIP integrity: PASS
real Yandex requests: 0
```

Current exact frozen artifact:

```text
file: yandex-marketing-bridge-0.1.1-phase2-search-context-recovery-candidate.zip
SHA-256: 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46
bytes: 175971
files: 68
ZIP entries: 71
```

Payload manifest:

```text
file: EXACT_CONTEXT_RECOVERY_CANDIDATE_MANIFEST_2026-08-25.json
SHA-256: bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478
bytes: 11933
```

GitHub Actions transport source:

```text
artifact name: phase2-context-recovery-frozen-candidate-f4aee34
artifact ID: 9546054918
outer artifact size: 188372 bytes
outer artifact digest: sha256:c41907f7c9f1f16c2a1c80f4b806f8d73e0cb60fcab040507764fae84ce0858c
expires: 2026-09-24T01:59:53Z
```

Do not confuse the outer Actions artifact digest with the inner exact candidate SHA-256.

## Phase-2 Search product boundary remains unchanged

Enabled first slice only:

```text
SEARCH_API_V1
service: search
method: search
POST https://searchapi.api.cloud.yandex.net/v2/web/search
synchronous text Search
FORMAT_XML
SEARCH_RESULT_V1
```

Still locked:

```text
Search async/deferred
Search image
Search generative
HTML SERP normalization
yandex.ru scraping
Webmaster
Metrika
Direct
```

## Required path from here

```text
1. publish a Windows-safe byte-exact transport for artifact 739dd5d7...
2. prove Windows consumer reassembly equals exact frozen SHA-256, size, files, entries and payload manifest
3. run one NEW complete governed gate on exactly 739dd5d7...
4. include installed-extension B-01/B-02/B-03
5. include native action-popup geometry B-04
6. include already-open-ChatGPT context-recovery acceptance B-05
7. include PD-00..PD-17
8. include mandatory Manual-ON transaction gate
9. include S-00..S-17
10. require final exactness and cleanliness PASS and real Yandex requests = 0
11. only then re-authorize exactly one owner-live synchronous Search acceptance
```

No previous complete PASS can authorize the changed context-recovery production bytes.

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = WINDOWS_SAFE_EXACT_TRANSPORT_FOR_739DD5D7
OWNER_LIVE_SEARCH = BLOCKED
PHASE_3_WEBMASTER = BLOCKED
```
