# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH REOPENED — CONTEXT-RECOVERY FREEZE + WINDOWS TRANSPORT PASS / COMPLETE GATE AUTHORIZED**  
Updated: 2026-08-25

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_THIS_STATE_WRITE = d4202c4628943f85bee19e38ad5e21526f03c616
LAST_COMPLETE_ACCEPTED_PRODUCT_SOURCE = 10bb3aca67295e5e515ff2ade8914b23e8458ca7
LAST_COMPLETE_ACCEPTED_ARTIFACT = 0186b35d66cf1e7e20a522dc128b3fdd317cd660c665b8294120a1ab8affe91d / 171655 bytes / 66 files / 69 ZIP entries
LATEST_COMPLETE_GATE = PASS on exact 0186b35d... candidate; run 32730308190 / job 97440819536
CURRENT_FROZEN_PRODUCT_SOURCE = f4aee34c0a3455aa7199f6aa54bd581c71d97337
CURRENT_FROZEN_ARTIFACT = 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46 / 175971 bytes / 68 files / 71 ZIP entries
CURRENT_FROZEN_PAYLOAD_MANIFEST = bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478 / 11933 bytes
CURRENT_FREEZE_GATE = PASS; run 32799665340 / job 97657914686
WINDOWS_SAFE_TRANSPORT = PASS; transport commit 7c787eedd9856c3f91fbed85aeaea7f3405ad473; run 32800990879; Windows job 97661642103
FOCUSED_CONTEXT_RECOVERY_GATE = PASS; source 239/239; Chrome 151 real action popup; run 32799117004 / job 97656378411
PRODUCTION_BYTES_CHANGED_SINCE_CURRENT_FREEZE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_CURRENT_FREEZE = NO
OWNER_LIVE = BLOCKED
REAL_OWNER_LIVE_SEARCH_REQUESTS_SINCE_DEFECT = 0
OPEN_BLOCKERS = exact 739dd5d7... candidate has not yet completed one new full governed gate
AUTHORIZED_NEXT_STAGE = COMPLETE_GOVERNED_GATE
```

## Current candidate authority

```text
candidate branch: candidate/phase2-context-recovery-2026-08-25
source: f4aee34c0a3455aa7199f6aa54bd581c71d97337
artifact file: yandex-marketing-bridge-0.1.1-phase2-search-context-recovery-candidate.zip
artifact SHA-256: 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46
artifact bytes: 175971
files: 68
ZIP entries: 71
payload manifest SHA-256: bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478
payload manifest bytes: 11933
```

Relative to the previously accepted repaired baseline `10bb3aca...`, the clean candidate differs by exactly six files:

```text
extension/src/manifest.json
extension/src/popup.html
extension/src/popup_context_bootstrap.js
extension/tests/candidate_readiness_recovery.test.mjs
extension/tests/popup_context_bootstrap.test.mjs
extension/tests/popup_error_boundary_recovery.test.mjs
```

No focused browser harness/workflow bytes are part of the candidate source.

## Exact freeze PASS

Durable authority:

```text
extension/tests/PHASE_2_CONTEXT_RECOVERY_FREEZE_PASS_2026-08-25.md
workflow run: 32799665340
job: 97657914686
source suite: 239/239 PASS
source syntax: 22 PASS
source JSON: PASS
deterministic rebuild: PASS
packaged suite: 239/239 PASS
packaged syntax: 62 PASS
packaged JSON: 2 PASS
ZIP integrity: PASS
real Yandex requests: 0
```

## Windows-safe transport PASS

Durable authority:

```text
extension/tests/PHASE_2_CONTEXT_RECOVERY_WINDOWS_TRANSPORT_PASS_2026-08-25.md
transport branch: qa/phase2-context-recovery-final-b64-transport-f4aee34-2026-08-25
transport commit: 7c787eedd9856c3f91fbed85aeaea7f3405ad473
transport parent: f4aee34c0a3455aa7199f6aa54bd581c71d97337
transport format: YMB_PHASE2_CONTEXT_RECOVERY_EXACT_B64_TRANSPORT_V1
base64 length: 234628
artifact.b64 SHA-256: d72bce6d500582310bd1bda894ac5c57e023f03aa80f9b1ebd79427db4172398
workflow run: 32800990879
Ubuntu producer job: 97661608465 PASS
Windows consumer job: 97661642103 PASS
Windows core.autocrlf=true
exact ZIP roundtrip: PASS
payload manifest roundtrip: PASS
ZIP integrity: PASS
final cleanliness: PASS
real Yandex requests: 0
```

## Defect and focused Chrome authority

Owner-live previously failed before the provider boundary because an already-open ChatGPT page had no receiver after the extension became active. No paid Search request occurred.

The repair first tries the ordinary identity route, injects the exact manifest content bundle only on missing receiver, retries identity, and starts the normal popup runtime only after deterministic bootstrap. It does not intentionally change provider, budget, retry, Manual transaction, Autorun transaction, or delivery semantics.

Focused Chrome 151 proof:

```text
run: 32799117004
job: 97656378411
Windows Server 2025
Chrome for Testing 151.0.7922.47
Puppeteer 25.4.0
ChatGPT opened before extension: PASS
late unpacked install: PASS
real native action popup: PASS
missing receiver reproduced: PASS
bootstrap attempted=true/recovered=true
Bind: PASS
Manual ON: PASS
ChatGPT DOM remained open: PASS
source suite: 239/239 PASS
real Yandex requests: 0
```

## Phase-2 Search product boundary remains unchanged

Enabled only:

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

## Required complete gate

The next controlled campaign must consume exactly transport commit `7c787eed...` and reconstruct exactly artifact `739dd5d7...`.

Required coverage:

```text
- exact transport/source/package authority
- source suite 239/239
- packaged suite 239/239
- source/package syntax and JSON
- B-01 Project/Work browser
- B-02 mandatory Manual-ON real-popup transaction
- B-03 Search Autorun
- B-04 native Chrome-151 action popup geometry
- B-05 already-open-ChatGPT context recovery
- PD-00..PD-17 ALL PASS
- mandatory Manual-ON transaction gate PASS
- S-00..S-17 ALL PASS
- controlled Search provider stub exactly once where required
- real Yandex requests = 0
- real credentials = 0
- final exactness PASS
- final cleanliness PASS
```

Only a complete PASS on the exact `739dd5d7...` candidate may re-authorize exactly one owner-live synchronous Search acceptance.

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = RUN_COMPLETE_GOVERNED_GATE_ON_739DD5D7
OWNER_LIVE_SEARCH = BLOCKED
PHASE_3_WEBMASTER = BLOCKED
```
