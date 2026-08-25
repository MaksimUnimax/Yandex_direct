# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH REOPENED — CHATGPT CONTEXT RECOVERY FOCUSED PASS / NEW REFREEZE REQUIRED**  
Updated: 2026-08-25

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_THIS_STATE_WRITE = e6c0105f237f38670fce67c011cac20f6057205d
LAST_ACCEPTED_PRODUCT_SOURCE = 10bb3aca67295e5e515ff2ade8914b23e8458ca7
LAST_ACCEPTED_ARTIFACT = 0186b35d66cf1e7e20a522dc128b3fdd317cd660c665b8294120a1ab8affe91d / 171655 bytes / 66 files / 69 ZIP entries
LAST_ACCEPTED_PAYLOAD_MANIFEST = 447bf18e54ba4a728cc6255adff5e13996366b9bf54b2668114110d525501009 / 11601 bytes
LATEST_COMPLETE_GATE = PASS on exact 0186b35d... candidate; run 32730308190 / job 97440819536
OWNER_LIVE = FAILED BEFORE PROVIDER BOUNDARY due missing ChatGPT content-script receiver when extension becomes active after the ChatGPT tab is already open
REAL_OWNER_LIVE_SEARCH_REQUESTS = 0
PRODUCTION_BYTES_CHANGED_SINCE_LAST_FULL_GATE = YES on focused context-recovery branch only; not yet refrozen
FOCUSED_CONTEXT_RECOVERY_GATE = PASS; source 239/239; Chrome 151 real action popup; run 32799117004 / job 97656378411
OPEN_BLOCKERS = new context-recovery product candidate has not yet been frozen, transported, and completely re-gated
AUTHORIZED_NEXT_STAGE = CONTEXT_RECOVERY_REFREEZE
```

## Accepted repaired baseline — supersedes the original Stage-4 artifact

The Chrome-151 popup geometry repair was already refrozen and completely accepted before the current context-recovery defect was found.

Exact accepted baseline:

```text
source: 10bb3aca67295e5e515ff2ade8914b23e8458ca7
artifact: yandex-marketing-bridge-0.1.1-phase2-search-popup-fix-candidate.zip
artifact SHA-256: 0186b35d66cf1e7e20a522dc128b3fdd317cd660c665b8294120a1ab8affe91d
artifact bytes: 171655
files: 66
ZIP entries: 69
payload manifest SHA-256: 447bf18e54ba4a728cc6255adff5e13996366b9bf54b2668114110d525501009
payload manifest bytes: 11601
```

Durable complete-gate authority:

```text
extension/tests/PHASE_2_POPUP_FIX_COMPLETE_GATE_PASS_2026-08-24.md
workflow run: 32730308190
job: 97440819536
source suite: 234/234 PASS
packaged suite: 234/234 PASS
packaged syntax: 60/60 PASS
packaged JSON: 2/2 PASS
B-01/B-02/B-03: PASS
native action-popup geometry B-04: PASS
PD-00..PD-17: ALL PASS
mandatory Manual-ON: PASS
S-00..S-17: ALL PASS
controlled Search stub requests: 1
real Yandex requests: 0
final exactness: PASS
final cleanliness: PASS
verdict: PASS
```

The older `0ee1d38... / d58b5bd...` candidate remains revoked and must not be restored as the owner-handoff authority.

## Current owner-live defect authority — ChatGPT context recovery

Focused product branch:

```text
branch: fix/phase2-chat-context-self-recovery-2026-08-24
PR: #13 Fix popup ChatGPT context self-recovery after extension reload
accepted baseline source: 10bb3aca67295e5e515ff2ade8914b23e8458ca7
focused PASS product/QA head: f77e91fcff75b85290e012ffec79123aa7fc9f0e
```

Owner-live failure condition:

```text
1. ChatGPT conversation tab is already open.
2. The unpacked extension becomes active afterwards (install/reload/update lifecycle).
3. The already-open page has no live manifest content-script receiver for the new extension runtime.
4. The old popup path sends WS_GET_IDENTITY only to that missing receiver.
5. Popup falls back to `Текущий ChatGPT: не определён` and Bind/Manual/Send/Copy become unusable.
```

No paid Search provider request occurred before this defect.

Current production delta relative to accepted source `10bb3aca...` is limited to:

```text
extension/src/manifest.json
extension/src/popup.html
extension/src/popup_context_bootstrap.js
```

Current package-test delta is limited to:

```text
extension/tests/candidate_readiness_recovery.test.mjs
extension/tests/popup_context_bootstrap.test.mjs
extension/tests/popup_error_boundary_recovery.test.mjs
```

The separate focused workflow/browser harness is QA infrastructure and is not part of the production delta.

### Product behavior of the repair

On popup startup:

```text
- identify the active supported ChatGPT tab;
- try the ordinary WS_GET_IDENTITY path first;
- only when the receiver is missing, inject the exact manifest content bundle with chrome.scripting.executeScript;
- retry identity after deterministic injection;
- start the normal popup runtime only after bootstrap finishes;
- preserve a visible bootstrap failure instead of allowing a later false `Готово.` overwrite;
- publish only a sanitized attempted/recovered/reason/tab_id verification result, never credentials or the identity response payload.
```

No Search/Wordstat provider, service routing, cost policy, request retry, Manual transaction, Autorun transaction, or delivery semantics are intentionally changed.

## Focused Chrome-151 PASS — exact owner-live reproduction

Workflow:

```text
phase2-context-recovery-focused
run: 32799117004
job: 97656378411
Windows Server 2025
Chrome for Testing: 151.0.7922.47
Puppeteer: 25.4.0
```

The final browser venue reproduces the owner-live ordering directly:

```text
ChatGPT opens first
→ CDP Extensions.loadUnpacked installs the unpacked extension afterwards
→ original ChatGPT DOM marker remains unchanged
→ CDP selects the real Chrome target of type `tab`
→ Extensions.triggerAction runs the real extension default action
→ real popup.html opens
```

Required observed markers all passed:

```text
CONTEXT_RECOVERY_CHATGPT_OPEN_BEFORE_EXTENSION_PASS
CONTEXT_RECOVERY_CHATGPT_TAB_TARGET_PASS
CONTEXT_RECOVERY_LATE_UNPACKED_INSTALL_PASS
CONTEXT_RECOVERY_CHAT_PAGE_REMAINED_OPEN_PASS
CONTEXT_RECOVERY_NATIVE_ACTION_TRIGGER_PASS
CONTEXT_RECOVERY_NATIVE_ACTION_POPUP_OPEN_PASS
bootstrapResult.attempted = true
bootstrapResult.recovered = true
CONTEXT_RECOVERY_MISSING_RECEIVER_REPRODUCED_PASS
POPUP_CONTEXT_SELF_RECOVERY_PASS
CONTEXT_RECOVERY_BIND_PASS
CONTEXT_RECOVERY_MANUAL_ON_PASS
CONTEXT_RECOVERY_ALREADY_OPEN_CHATGPT_PASS
REAL_YANDEX_REQUESTS=0
CONTEXT_RECOVERY_FOCUSED_CLEAN_PASS
```

Complete source suite on the same focused head:

```text
239/239 PASS
```

Static recovery contract and manifest JSON checks also passed.

## Phase-2 Search boundary remains unchanged

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

## Required recovery path from here

```text
1. construct a clean new candidate source from accepted 10bb3aca... plus only the proven context-recovery product/package-test delta
2. freeze a NEW deterministic exact artifact
3. verify complete source and packaged suites plus syntax/JSON and exact source-package identity
4. publish a Windows-safe exact byte transport for the new artifact
5. run installed-extension browser coverage B-01/B-02/B-03
6. run native action-popup geometry B-04
7. run the new already-open-ChatGPT context-recovery browser acceptance B-05
8. run one NEW complete governed campaign PD-00..PD-17 + mandatory Manual-ON + S-00..S-17
9. require final exactness and cleanliness PASS with real Yandex requests = 0
10. only complete PASS re-authorizes exactly one owner-live synchronous Search acceptance
```

No old complete PASS can authorize the changed context-recovery production bytes without this new refreeze/full gate.

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = BUILD_CLEAN_CONTEXT_RECOVERY_CANDIDATE_AND_REFREEZE
OWNER_LIVE_SEARCH = BLOCKED
PHASE_3_WEBMASTER = BLOCKED
```
