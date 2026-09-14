# B22 — Stage B popup memory hotfix final qualification — 2026-09-14

## Verdict

- `REVOKED_STAGE_B = 404dd03874e5df80a95bc6cec1e6967bb71de405`
- `REVOKED_ZIP_SHA256 = 51491db92e1ea7c8e3c9555e95ba236cada5a4890b66e6c6134779550856c036`
- `HOTFIX_PRODUCT_SHA = 1adc113945a6c4ca63f78788980b2c68b0acfd08`
- `HOTFIX_BRANCH = hotfix/ymb-popup-memory-bounded-2026-09-13`
- `HOTFIX_EXTENSION_SRC_TREE_SHA256 = 4b06abdf0eafe951a0758b55ac3a811599a296e3b382a7d64e4f178b1e9a8a30`
- `HOTFIX_FILES = 68`
- `AUTOMATED_QUALIFICATION = PASS`
- `OWNER_LIVE_SMOKE = PENDING`
- `FINAL_RECIPIENT_ACCEPTANCE = OPEN`

The revoked Stage-B ZIP MUST NOT be used again.

## Root cause

The revoked popup monitor performed periodic IndexedDB refresh every 5 seconds and cursor-scanned complete `items` and complete `results` stores. Reading `results` materialized result records containing large `raw_text` and normalized SERP payloads into the popup process. The previous automated qualification used small synthetic jobs and therefore did not cover this large-evidence RAM failure class.

The hotfix changes only `extension/src/popup_search_async_monitor.js` relative to revoked Stage B. It:

- removes the automatic 5-second IndexedDB refresh;
- keeps only one lightweight UI/countdown interval and clears it on `pagehide`;
- refreshes database state only on popup bootstrap, conversation change, explicit refresh, or after explicit popup action;
- replaces full `items` cursor scans with IndexedDB `count()` / index queries;
- replaces full `results` cursor scan with `results.count(itemRange)`;
- never reads `raw_text` or `normalized.results` for popup metrics;
- exposes unknown SERP-row total as `— (без чтения payload)` instead of reading heavy payloads.

No Search runtime, transport, admission, file-delivery, Send, manifest, or Stage-B content ingress was changed by this memory hotfix.

## Memory reproduction and stress evidence

### V6 — max-job 100 explicit refreshes

Run: `34795447327`
Artifact: `10329995260` (`ymb-popup-memory-bounded-evidence-v6`)

Revoked Stage B reproduced periodic heavy result reads: `result_open_cursor` increased from `1` to `4` while the popup remained open.

Hotfix max-job stress:

- items: `1500`;
- per-result raw payload: `32768` bytes;
- approximate raw payload: `49,119,232` bytes plus normalized data;
- 100 real explicit refreshes completed;
- `result_open_cursor = 0` throughout;
- result count reads increased from `2` to `103`, proving the refreshes actually executed;
- IndexedDB job revision/item/result counts unchanged;
- provider calls: `0`;
- measured RSS `1,218,964 -> 1,320,340 KiB`, delta `101,376 KiB`, below the hard 192 MiB refresh-drift bound.

The V6 aggregate result remained RED only because a synthetic `browser.newPage()` 100-tab churn later exceeded an absolute Chrome process-tree RSS bound. That synthetic tab model was independently controlled in V8 below and was not used as proof of extension leakage.

### V8 — long-lived heavy popup + neutral-control lifecycle differential

Run: `34795757733`
Artifact: `10329299127` (`ymb-popup-memory-lifecycle-v8`)
Artifact SHA-256: `497c66f827b0f5190fe479144b42492b92c447e87d4c4bb67683e7448261f801`
Verdict: `PASS`
Provider calls: `0`

Long-lived heavy popup for 60 seconds on the 1500-item / ~49.1 MiB raw dataset:

- start counters: `result_open_cursor=0`, `result_count=3`, `item_open_cursor=0`, `item_count=3`;
- end counters identical after 60 seconds: no automatic database read loop remained;
- database unchanged;
- base RSS `1,231,976 KiB`;
- final RSS `1,181,796 KiB`;
- RSS delta `-50,180 KiB`;
- peak RSS `1,320,940 KiB`;
- provider calls `0`.

100 synthetic `browser.newPage() -> popup.html -> close()` cycles were also compared against a QA-only neutral control in which the popup monitor script was replaced by a no-op:

Neutral control:
- residual RSS growth `904,608 KiB`;
- peak RSS `2,328,904 KiB`;
- processes `11 -> 19`, max `21`.

Hotfix:
- residual RSS growth `1,007,796 KiB`;
- peak RSS `2,456,296 KiB`;
- processes `11 -> 19`, max `21`.

Differential hotfix overhead over neutral Chrome churn:
- residual `103,188 KiB`;
- peak-growth difference `132,964 KiB`;
- extra processes `0`;
- all within the 256 MiB differential bound.

Therefore the ~1 GiB accumulation in the 100-`newPage()` model is Chrome/Puppeteer renderer-pool behavior, not a monitor-specific leak. The realistic long-lived popup gate is stable.

## Node / behavioral regression

Workflow: `YMB popup memory hotfix Node final`
Run: `34795960371`
QA commit: `0dd39bc025689298f44c2b6cfd3c63fc9e11d609`
Artifact: `10329069520`
Artifact SHA-256: `49497872840ea39faa0c764e4451a9dc526abfa638627268e5886e80e9bfd7ed`
Verdict: `PASS`

Accepted Stage A (`341c847089e1207dd23bf876f5ba3ac537b65a10`) and the hotfix product were run through the same B19 campaign. `suite_delta = {}`.

Preserved suite signatures:
- ORIGINAL: `132/132`;
- MISSING: `78/78`;
- MODULE: `254/254`;
- EXPORT: `84/84`;
- FULL: `98/99` on both accepted Stage A and hotfix (known stale pre-current-confirmation file-delivery assertion);
- DELIVERY: `56/69` on both accepted Stage A and hotfix (known stale pre-current-confirmation assertions).

The current Stage-B popup contract test passed and provider calls were `0`.

## Final exact package / real-Chrome requalification

Workflow: `YMB popup memory hotfix package final`
Run: `34795995153`
QA commit: `93aa43eb50f23352ff27b94ba192641bd53c29db`
Artifact: `10329359167` (`ymb-0.1.6-stage-b-memory-hotfix-final`)
Outer artifact SHA-256: `f5fde7703e868fc8d305f36f5b023ae1cad24efd9d6713ae84239bb0d84016e9`

Installable ZIP:
- filename: `Yandex-Marketing-Bridge-0.1.6-stage-b-memory-hotfix.zip`;
- SHA-256: `781ef6ec1a98ee7fe86c0ee34e94eee05fb12e0a3c2fd58cf629e6630125c108`;
- bytes: `232604`;
- files: `68`;
- extension/src tree SHA-256: `4b06abdf0eafe951a0758b55ac3a811599a296e3b382a7d64e4f178b1e9a8a30`;
- deterministic dual build identity: `PASS`;
- fresh-extraction identity: `PASS`;
- ZIP integrity: `PASS`;
- per-file `SOURCE_SHA256SUMS`: `68/68 MATCH` on independent downloaded-artifact readback.

Final gates on the exact fresh-extracted package:

- memory 100-refresh evidence: `PASS`;
- memory lifecycle evidence: `PASS`;
- TEST-15 exactly-once: `PASS`, all four required cases, provider calls `0`;
- popup real Chrome: `PASS`, 6 cases, failures `0`, provider fetch calls `0`;
- B19 resource matrix: `16/16 PASS`, cleanup remaining processes `[]`;
- B19 deferred-network matrix: `9/9 PASS`, cleanup remaining processes `[]`;
- real provider calls: `0`;
- final aggregate gate: `PASS`.

Resource-gate peak owned RSS was `1,920,608 KiB`, below its existing 2 GiB emergency bound. Network-gate peak was `1,299,928 KiB`.

## Remote readback / scope

Hotfix product branch remote HEAD read back as:

`1adc113945a6c4ca63f78788980b2c68b0acfd08`

Final production diff from accepted Stage A is still exactly two files:

1. `extension/src/content_script.js` — Stage-B action ingress;
2. `extension/src/popup_search_async_monitor.js` — Stage-B popup monitor/actions plus bounded-memory hotfix.

No other `extension/src` files differ from accepted Stage A.

## Gate state

`AUTOMATED_QUALIFICATION = PASS`

`OWNER_LIVE_SMOKE = PENDING`

`FINAL_RECIPIENT_ACCEPTANCE = OPEN`

Do not claim final owner/browser acceptance until the owner installs the exact ZIP SHA above and completes a minimal live smoke. Do not use the revoked Stage-B ZIP.