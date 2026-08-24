# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH REOPENED — OWNER-LIVE POPUP DEFECT UNDER FOCUSED REPAIR**  
Updated: 2026-08-24

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_CHECKPOINT = 23ec074f529b14659f918c36e9107604bf84f767
LAST_ACCEPTED_PRODUCT_SOURCE = 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
LAST_ACCEPTED_ARTIFACT = d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16 / 170734 bytes / 65 files / 68 ZIP entries
LATEST_COMPLETE_CODEX_GATE = PASS on exact d58b5bd... candidate
OWNER_LIVE = FAILED BEFORE PROVIDER BOUNDARY due unusable/jumping native action popup
REAL_OWNER_LIVE_SEARCH_REQUESTS = 0
PRODUCTION_BYTES_CHANGED_SINCE_LAST_FULL_GATE = YES on focused repair branch only; not yet refrozen
OPEN_BLOCKERS = Chrome 151 native action-popup geometry defect must pass focused browser regression, then new candidate must be frozen and fully re-gated
AUTHORIZED_NEXT_STAGE = FOCUSED_POPUP_REPAIR_AND_REFREEZE
```

## Owner-live defect authority

Read first:

```text
extension/docs/PHASE_2_OWNER_LIVE_POPUP_CHROME151_DEFECT_2026-08-24.md
```

Owner-live exposed an unstable/jumping extension toolbar popup before any paid Search provider request was executed.

Exact affected candidate CSS had a narrow `body` width but no root height bound/internal scroller, while `popup.html` is intrinsically far taller than the Chrome action-popup 600 px height limit.

Current Chromium issue:

```text
541684116 — [Extensions] Action popup expands from 316px to 800px when content height exceeds 600px
https://issues.chromium.org/issues/541684116
```

Chrome action-popup documented max size:

```text
800 x 600
https://developer.chrome.com/docs/extensions/reference/api/action
```

This is a real product/UI defect plus a previous browser-gate coverage blind spot.

## Why the previous Stage-4 browser PASS did not catch it

The previous harness helper called `openPopup()` but actually executed:

```js
chrome.tabs.create({ url: chrome.runtime.getURL('popup.html'), active:false })
```

so B-01/B-02/B-03 exercised real popup JavaScript and worker transactions in a normal extension tab, not the native toolbar action-popup host. It could not test Chromium action-popup autosizing.

The old complete Codex PASS remains valid evidence for all assertions actually executed, but it cannot authorize the known-bad `d58b5bd...` artifact for owner handoff after this live defect.

## Focused repair authority

```text
branch: fix/phase2-popup-chrome151-autosize-2026-08-24
PR: #11 Fix Chrome 151 action popup autosize regression
base exact product source: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
```

Current production change is intentionally limited to:

```text
extension/src/popup.css
```

New geometry contract:

```text
html/body = fixed 430 x 560
root overflow = hidden
main = 100% height
main overflow-y = auto
main overflow-x = hidden
```

No Search protocol/provider, service worker, content script, credential, policy, Manual/Autorun or delivery logic change is authorized by this defect.

Focused regression files:

```text
extension/tests/popup_chrome151_geometry_recovery.test.mjs
extension/tests/qa_browser/popup_chrome151_geometry_gate.mjs
```

The new browser gate must use the real:

```text
chrome.action.openPopup()
```

on Chrome for Testing `151.0.7922.47` and prove the native action-popup geometry, not a normal extension tab.

## Last complete controlled gate — historical PASS on superseded owner-handoff artifact

Exact old artifact:

```text
source: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
artifact SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
PD-00..PD-17: ALL PASS
Manual-ON: PASS
S-00..S-17: ALL PASS
source suite: 231/231 PASS
packaged suite: 231/231 PASS
browser B-01/B-02/B-03: PASS
real Yandex requests: 0
verdict: PASS
```

Durable old-gate evidence remains:

```text
extension/tests/PHASE_2_STAGE_4_CODEX_FULL_GATE_PASS_2026-08-24.md
```

It is no longer sufficient for owner handoff because product bytes are being repaired and the live defect is known.

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

## Required recovery path

```text
1. focused Chrome-151 native action-popup A/B regression PASS
2. complete affected/source tests PASS
3. freeze a NEW exact candidate because popup.css production bytes changed
4. prepare exact byte-safe Codex transport for the new artifact
5. run one NEW complete governed pre-delivery campaign from PD-00 through PD-17 + Manual-ON + S-00 through S-17 + native action-popup geometry regression
6. only complete PASS re-authorizes owner-live Search
7. then perform exactly one real synchronous Search acceptance
```

No paid owner-live Search is authorized while this defect is open.

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = FOCUSED_POPUP_REPAIR_AND_REFREEZE
OWNER_LIVE_SEARCH = BLOCKED
PHASE_3_WEBMASTER = BLOCKED
```
