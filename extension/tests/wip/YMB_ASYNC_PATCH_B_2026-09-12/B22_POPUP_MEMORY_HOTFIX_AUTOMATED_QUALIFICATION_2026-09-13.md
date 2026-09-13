# B22 — Popup memory hotfix automated qualification — 2026-09-13

## Incident and revocation

The Stage-B candidate rooted at:

- product commit `404dd03874e5df80a95bc6cec1e6967bb71de405`
- install ZIP SHA-256 `51491db92e1ea7c8e3c9555e95ba236cada5a4890b66e6c6134779550856c036`

is **REVOKED** for owner installation.

Root cause found after owner RAM failure:

- `popup_search_async_monitor.js` performed an automatic IndexedDB refresh every 5 seconds;
- every refresh cursor-scanned all job `items`;
- every refresh cursor-scanned all job `results`;
- reading each result materialized the full record, including `raw_text` and `normalized.results`, inside the popup process;
- the previous popup qualification used small jobs and did not exercise a realistic large deferred-result store.

This is the second memory-safety miss in the same extension family and is treated as a P0 resource-regression incident, not as an accepted owner candidate.

## Hotfix product identity

Product branch:

`hotfix/ymb-popup-memory-bounded-2026-09-13`

Exact product commit:

`1adc113945a6c4ca63f78788980b2c68b0acfd08`

Diff from revoked Stage B:

- only `extension/src/popup_search_async_monitor.js`
- no changes to Search runtime/transport/admission;
- no changes to `content_script.js` popup ingress;
- no changes to file delivery / Send;
- no manifest changes.

Qualified `extension/src` identity:

- files: `68`
- tree SHA-256: `4b06abdf0eafe951a0758b55ac3a811599a296e3b382a7d64e4f178b1e9a8a30`

Install ZIP:

- file: `Yandex-Marketing-Bridge-0.1.6-stage-b-memory-hotfix.zip`
- SHA-256: `781ef6ec1a98ee7fe86c0ee34e94eee05fb12e0a3c2fd58cf629e6630125c108`
- bytes: `232604`
- deterministic dual build: PASS
- fresh extraction identity: PASS
- ZIP integrity/readback: PASS

## Production memory fix

The popup monitor now:

1. does **not** run a 5-second IndexedDB refresh loop;
2. refreshes persisted state only on popup open, conversation change, explicit action, or explicit `Обновить статус`;
3. uses IndexedDB `count()` and indexed `get()` for lightweight counts/next-due lookup;
4. never opens a cursor over the `results` store;
5. never materializes `raw_text` or `normalized.results` merely to render popup progress;
6. renders total SERP-row count as `— (без чтения payload)` because there is no safe persisted aggregate for that field yet;
7. retains only a local 1-second UI/countdown timer and clears it on `pagehide`;
8. keeps the existing popup → content script → `WS_EXECUTE_MANUAL_BLOCK` execution path unchanged.

## Memory-specific real-Chrome gate

Passing workflow run:

- run: `34763043359`
- artifact: `10319562586`
- artifact digest: `sha256:cd4d7675493b383468a9d9fa28fedd38067a918376f640b361e6f78ef6a0b4fc`

Revoked Stage B reproduction:

- old candidate under a heavy persisted result store detached/crashed the popup/browser frame during the reproduction contour;
- old source statically contains both `results.openCursor` and `REFRESH_MS = 5000`.

Fixed candidate large-job contour:

- job items: `1500`
- persisted result records: `1499`
- raw bytes per result: `65536`
- approximate raw result payload: `98238464` bytes
- explicit refreshes: `100`
- `results.openCursor` calls: `0`
- bounded `results.count` observations: `103`
- bounded `items.count` observations: `103`
- job/items/results state unchanged: PASS
- process-tree RSS before refresh loop: `1216568 KiB`
- process-tree RSS after refresh loop: `1319176 KiB`
- delta: `102608 KiB`

100 popup-document lifecycle contour:

- baseline process-tree RSS: `1311720 KiB`
- final process-tree RSS: `1462324 KiB`
- delta: `150604 KiB`
- peak: `1495804 KiB`
- emergency limit: `2097152 KiB`
- verdict: PASS

Provider calls during the memory gate: `0`.

Historical RED attempts are preserved and MUST NOT be relabelled as PASS:

- `34762467410` — first memory harness / initial hotfix UI-null defect;
- `34762617246` — QA refresh-count race;
- `34762704817` — QA owner/refresh observability race;
- `34762920436` — proved 1500-item/100-refresh memory safety; RED remained only because 100 full browser tabs were an invalid proxy for action-popup lifecycle.

## Exact-package / browser regression

Passing browser/package job is inside workflow run:

- run: `34763247778`
- job: `exact-package-browser` — PASS
- artifact: `10319971703`
- artifact digest: `sha256:cf5bb00bdb5755df7d8fffef0029a9e46de50597ca6adba224cf1fec99a873af`

Final exact-package gate:

- package identity/static: PASS
- fresh-extracted JS syntax: PASS
- targeted TEST-15 exactly-once: PASS
- popup real Chrome: PASS
- B19 resource matrix: `16/16 PASS`
- B19 deferred-network matrix: `9/9 PASS`
- browser failures: `0`
- remaining owned Chrome processes: `0`
- resource peak RSS: `1880272 KiB` < `2097152 KiB`
- network peak RSS: `1292668 KiB`
- embedded memory gate: PASS
- real provider calls: `0`
- aggregate `FINAL_GATE.pass`: `true`

The workflow run overall is red only because its first Node job contained a QA output-directory collision. The browser/package job itself is PASS and its passing artifact is retained. That Node harness defect did not execute a product assertion.

## Node / contract regression

Corrected Node workflow:

- run: `34763353171`
- artifact: `10319902223`
- artifact digest: `sha256:9bc236d30c42d00933567e0261ca4792458334761c5a3f7a1856d0d0a15fdf90`
- workflow conclusion: PASS

Results:

- Stage-B popup contract: PASS
- baseline product: revoked `404dd038...`
- hotfix product: `1adc113...`
- B19 suite delta: `{}`
- static pass: true
- real provider calls: `0`

Known stale frozen B19 failures remain byte-for-byte/suite-for-suite identical on baseline and hotfix:

- `FULL_99`: `98/99`
- `DELIVERY_69`: `56/69`

They belong to the older frozen pre-current-confirmation file-delivery expectations and are not new hotfix regressions. Current controlled TEST-15, resource, and network gates all pass on the exact hotfix ZIP.

## Gate state

```text
REVOKED_STAGE_B_404DD = DO_NOT_INSTALL
REVOKED_ZIP_51491D = DO_NOT_INSTALL

HOTFIX_PRODUCT = 1adc113945a6c4ca63f78788980b2c68b0acfd08
HOTFIX_ALLOWLIST = PASS (popup_search_async_monitor.js only)
MEMORY_LARGE_JOB = PASS
MEMORY_100_REFRESH = PASS
MEMORY_100_POPUP_LIFECYCLES = PASS
STAGE_B_CONTRACT = PASS
NODE_DIFFERENTIAL = PASS / suite_delta={}
DETERMINISTIC_ZIP = PASS
FRESH_EXTRACTION = PASS
TEST15 = PASS
POPUP_REAL_CHROME = PASS
RESOURCE = 16/16 PASS
NETWORK = 9/9 PASS
PROVIDER_CALLS = 0
AUTOMATED_QUALIFICATION = PASS
OWNER_LIVE_SMOKE = PENDING
FINAL_RECIPIENT_ACCEPTANCE = OPEN
```

Do not claim final owner acceptance until the exact ZIP SHA-256 `781ef6ec1a98ee7fe86c0ee34e94eee05fb12e0a3c2fd58cf629e6630125c108` is installed in the owner's real Chrome profile and the live popup/action/file-delivery smoke is completed.
