# B19 — final independent PD-00..PD-17 execution map for exact 0.1.6

Date: 2026-09-13
Status: **MANDATORY QA AUTHORITY FOR THE INDEPENDENT PRE-DELIVERY CAMPAIGN**
Scope: exact frozen Yandex Marketing Bridge 0.1.6 candidate only

This map is QA/process authority only. It does not change production bytes, does not inherit historical PASS, and does not unlock owner handoff by itself.

## 1. Exact immutable candidate

The independent campaign MUST test the existing exact installable ZIP and no substitute:

- filename: `Yandex-Marketing-Bridge-0.1.6.zip`
- SHA-256: `81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2`
- bytes: `220045`
- extracted product tree SHA-256: `b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86`
- product files: `67`

Primary exact-artifact source:

- GitHub Actions run: `34737506830`
- artifact id: `10311695957`
- artifact name: `ymb-0.1.6-final-owner-candidate`
- outer artifact SHA-256: `07d9b9e70181983172b7af448e07e087ec9551144905562e506053670c40b059`
- outer artifact bytes: `225323`

Pre-Codex consumer readback is recorded in `B19_PRE_CODEX_TRANSPORT_READBACK_2026-09-13.md`: outer artifact hash/size, ZIP CRC, 14/14 published SHA entries, inner ZIP hash/size, 67-file extraction, path safety and tree identity all passed without reconstruction.

The exact ZIP is the primary product input. Rebuilding or substituting a logically equivalent ZIP is forbidden. A disposable QA workspace may copy the already-verified fresh extraction into that workspace's `extension/src` only when a runner requires that path. Such a copy is test staging, not a production edit, and MUST be preceded and followed by exact 67-file tree identity checks.

Current branch QA/document commits after candidate freeze are NOT product-byte drift. Do not compare the candidate to a later branch tree containing QA-only documents and call that a product failure. Product identity is the exact ZIP/tree above.

## 2. B19 supersession of obsolete B18 Search lock

`B18_FINAL_PD_EXECUTION_MAP.md` was written while deferred Search provider networking was intentionally disabled. Its PD-16 requirement that `operation.api.cloud.yandex.net` remain disabled is obsolete for B19 and MUST NOT be applied to 0.1.6.

The permanent gate explicitly requires a disabled future phase to remain locked **until explicitly enabled**, and once enabled to replace the lock with full functional coverage. B19 explicitly enables deferred Search in **Manual-only** mode.

Therefore B19 PD-16 requires full enabled-phase coverage:

- `https://searchapi.api.cloud.yandex.net/*` present exactly as authorized;
- `https://operation.api.cloud.yandex.net/*` present exactly as authorized;
- no `chrome.alarms` permission;
- no hidden/background deferred poller;
- lifecycle is explicit Manual `start -> submit/submitN -> POST /v2/web/searchAsync -> persist operation_id -> WAITING -> explicit collect/collectN/collectReady -> GET /operations/<id> -> persist raw -> normalize -> export/delivery`;
- assistant/user payload cannot override provider origins, API key source or folder containment;
- uncertain submit becomes `UNKNOWN` and is never auto-resubmitted;
- Manual disabled means zero deferred-provider network;
- existing ordinary Search/GenSearch/Webmaster/Metrika/Direct paths remain under their normal regression coverage;
- any still-unsupported operation must fail before provider network.

Do not restore the old disabled-operation-host assertion and do not edit production to satisfy it.

## 3. Qualified reusable QA inputs

Historical evidence is provenance only; all mandatory assertions are executed again independently.

### Node/classification harness input

- run: `34734894636`
- artifact id: `10310577071`
- artifact name: `ymb-b19-node-classification`
- artifact digest: `sha256:2df3ef02bb9107f11c7434efe0464f633139a7065a54c10c961965d2bae9cb4e`

Canonical runner:

```bash
python3 extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/qa/b19_final_node_campaign_v2.py \
  "$QA_REPO" "$CLASSIFICATION_DIR" "$QA_OUT/b19-final-node"
```

The disposable `$QA_REPO/extension/src` MUST first be replaced only in the disposable QA workspace with the verified fresh extraction of the exact install ZIP, then rehashed to the exact B19 tree. The classification artifact supplies harness/test inputs, not product bytes.

Expected independent result shape from this runner:

- original source tests: `132`
- Wordstat/Debug/backup coverage: `78`
- full network/contract suite: `99`
- async/modules: `254`
- export: `84`
- delivery/recovery: `69`
- JS syntax files: `61`
- failed/skipped/cancelled: `0`

These counts are acceptance expectations, not inherited PASS.

### Reusable browser harness input

Historical B17 ready evidence may be reused only for qualified fixture/harness files:

- run: `34699125356`
- artifact id: `10299402884`
- artifact name: `ymb-b17-pause-internal-evidence`
- artifact digest: `sha256:0a6b938c6d39392ed1f61f072bfc1ed5e590e99c207bc0bb2d9defebce1e5c3c`

It is NEVER the B19 product candidate. Browser runs load the exact fresh-extracted B19 0.1.6 tree.

Canonical B19 browser entry points:

```bash
xvfb-run -a node extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/qa/b19_network_browser.mjs
```

Resource/delivery campaign uses QA-only adaptation of the preserved B17 browser harness:

```bash
python3 extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/qa/b19_resource_browser_adapt.py \
  "$QA_REPO" "$B17_READY_DIR" "$QA_OUT/resource-tests"

xvfb-run -a node "$QA_OUT/resource-tests/b15_browser_qualification.mjs"
xvfb-run -a node "$QA_OUT/resource-tests/b15_browser_faults.mjs"
xvfb-run -a node "$QA_OUT/resource-tests/b17_browser_b19.mjs"
```

The adaptation script is QA-only and tree-guarded. Product bytes remain unchanged.

Additional governed browser/reload entry points available on the branch and reusable against exact B19 bytes include:

- `.github/workflows/ymb-b16-browser-remaining.yml`
- `.github/workflows/ymb-b17-pause-validation.yml`
- `.github/workflows/ymb-b17-cleanup-recheck.yml`
- `.github/workflows/ymb-b18-missing-qualification.yml`
- `.github/workflows/ymb-b18-reload-qualification.yml`
- `.github/workflows/ymb-b18-cli-reload-qualification.yml`

Their product input MUST be rebound to the exact B19 fresh extraction. Any obsolete assertion that the operation host/provider is disabled is excluded by this B19 map; no other assertion may be weakened.

## 4. Provider and owner-safety boundary

Independent campaign requirements:

- real Yandex provider calls: `0`;
- real owner credentials: forbidden;
- owner browser/profile: forbidden;
- synthetic/controlled network fixtures only;
- no owner file transport;
- no background deferred polling;
- no production edits;
- no weakening or deletion of a failing assertion.

A normal product failure does not justify stopping unrelated safe PD sections. Collect the complete failure set.

## 5. PD-00..PD-17 executable map

### PD-00 — authority, freeze, exact candidate identity

**Venue:** package/static + fresh consumer readback.

**Execute:** download artifact `10311695957` from run `34737506830`; verify outer SHA/bytes and CRC; extract exact nested `Yandex-Marketing-Bridge-0.1.6.zip`; verify inner SHA/bytes/CRC; fresh-extract; verify 67 files, single safe root and tree SHA.

**Assertions:** candidate exactly matches the identities in section 1; no substituted/rebuilt product; production bytes unchanged throughout campaign.

**Evidence:** input source, hashes, byte counts, CRC, file count, path-safety result, tree hash, start/end candidate identity.

### PD-01 — complete source regression

**Venue:** Node/VM/integration.

**Runner:** `qa/b19_final_node_campaign_v2.py` with classification artifact `10310577071` in a disposable exact-B19 workspace.

**Assertions:** independently obtain 132 / 78 / 99 / 254 / 84 / 69 with zero failed/skipped/cancelled; ordinary Search, GenSearch, Webmaster, Metrika, Direct, Wordstat, export and delivery regressions remain passing.

**Evidence:** exact command, Node version, per-suite stdout/stderr, counts, exit status.

### PD-02 — static, syntax, manifest and load-order integrity

**Venue:** Node/static/manifest.

**Runner:** same B19 Node runner plus direct manifest inspection and `node --check` over all 61 JS files.

**Assertions:** version 0.1.6; 61 JS syntax PASS; both Search provider origins present exactly once; `alarms` absent; expected service worker/content scripts/load order preserved; no command-controlled provider endpoint or credential source introduced.

**Evidence:** manifest snapshot, JS file count, syntax log, static assertions.

### PD-03 — exact package, extraction and reproducibility boundary

**Venue:** package/extraction identity.

**Execute:** PD-00 exact ZIP is primary. Validate archive integrity/path safety/fresh extraction and exact 67-file tree. The existing deterministic packer/`ymb-b19-final-package-qualification.yml` may be rerun only as additional reproducibility evidence; a rebuilt ZIP never replaces the exact handoff ZIP.

**Assertions:** exact ZIP remains `81d47...34e2`, 220045 bytes before and after campaign; extracted tree remains `b87246...8b86`; no extra files inside package.

**Evidence:** hashes before/after, archive listing, extraction manifest, optional reproducibility comparison.

### PD-04 — MV3 runtime and lifecycle

**Venue:** qualified Chrome for Testing/Puppeteer + deterministic integration.

**Runners:** B19 resource campaign (`b15_browser_qualification.mjs`, `b15_browser_faults.mjs`, `b17_browser_b19.mjs`), plus B18 reload/CLI-reload workflows rebound to exact B19 bytes.

**Assertions:** extension installs from fresh extraction; worker/content/popup initialize; worker restart and full browser/profile close-reopen recover safely; no orphan owned Chrome processes remain.

**Evidence:** Chrome/Puppeteer versions, extension id/runtime logs, restart/reload traces, cleanup process table.

### PD-05 — popup/settings/settings-window behavior

**Venue:** qualified Chrome/Puppeteer + source regression.

**Runners:** B16/B18 browser cases rebound to exact B19 bytes plus PD-01 source regression.

**Assertions:** settings UI opens and persists governed settings; Manual/Autorun controls remain correct; no hidden deferred activation is introduced; UI state recovers after reload/restart.

**Evidence:** browser case matrix, persisted setting state before/after reload, console errors.

### PD-06 — Manual action and ChatGPT DOM binding

**Venue:** qualified Chrome/Puppeteer.

**Runners:** B16 remaining-browser coverage + B18 missing browser cases + B19 resource fixture, all on exact B19 product.

**Assertions:** Manual binding to the intended ChatGPT conversation/tab; native Copy/CodeMirror/plain-content behavior; command boundary detection; visible delivery plaques/state; no cross-chat action.

**Evidence:** browser case names, DOM fixture state, ownership identifiers, action counts.

### PD-07 — Manual full-block discovery and content→worker routing

**Venue:** Chrome/Puppeteer + deterministic content↔worker integration.

**Runners:** `qa/b19_network_browser.mjs`, `qa/b9_full_worker.test.mjs`/harness through the B19 Node campaign, and governed B18 browser full-block/source-order cases.

**Assertions:** one complete assistant envelope maps to one intended worker action; malformed/non-command content is ignored/fails closed; deferred lifecycle routes `start/submit/collect` correctly; duplicate discovery does not duplicate paid work.

**Evidence:** discovered block ids, worker messages, request counts, state transitions.

### PD-08 — Wordstat complete regression

**Venue:** Node/VM/integration.

**Runner:** B19 Node campaign, especially the 78 Wordstat/Debug/backup cases plus original protocol tests.

**Assertions:** all Wordstat methods preserve request accounting, credential selection, malformed-JSON error behavior and no unauthorized automatic retry.

**Evidence:** 78-suite result and Wordstat-specific error/accounting traces.

### PD-09 — policy, credentials, cost and accounting

**Venue:** Node/integration + controlled browser network.

**Runners:** 99 full network/contract suite; `b10_deferred.test.mjs`, `b11_batch_faults.test.mjs`, `b11_reparse.test.mjs`; `b19_network_browser.mjs`.

**Assertions:** admission/cost/accounting are consistent; operation_id is persisted before subsequent paid work; interrupted/unknown outcomes do not trigger duplicate paid requests; `UNKNOWN` means one submit attempt and no auto-resubmit; credentials/folder come only from governed settings.

**Evidence:** request ledger/state snapshots, operation id persistence order, network call counts, synthetic credential proof.

### PD-10 — Autorun lifecycle and recovery

**Venue:** Node + Chrome/Puppeteer.

**Runners:** legacy/deferred batch coverage from PD-01 plus B17/B18 reload and pause/recovery browser cases.

**Assertions:** existing Autorun functionality remains stable; deferred Search remains Manual-only and cannot start from hidden/background polling; stop/pause/reload/restart state is deterministic; no extra Yandex request is made on recovery.

**Evidence:** mode flags, state transitions, reload/restart traces, zero unexpected network calls.

### PD-11 — Manual delivery FSM, durability, duplicate prevention and resources

**Venue:** Chrome/Puppeteer + IndexedDB + deterministic delivery integration.

**Runners:** B19 resource campaign three commands from section 3 plus 69 delivery/recovery Node cases.

**Assertions:** 1/10/32/64 MiB and repeated 64 MiB delivery contours; bounded staging; duplicate-Send prevention; corrupted chunk stops before attach/send; pause/resume persists; wrong-chat navigation isolation; late chunk after pause cannot attach/send; 10/100/500/1500 IndexedDB contours; worker restart during large job; final cleanup.

**Resource gate:** measure owned Chrome process-tree RSS independently; emergency limit `2097152 KiB`; remaining owned browser processes after cleanup must be `0`.

**Evidence:** per-case result, peak RSS, item counts, chunk counts, attach/send counts, recovery state, final process list.

### PD-12 — Debug and error delivery/redaction

**Venue:** Node + browser/error fixture where required.

**Runners:** 78 Wordstat/Debug/backup suite + 99 full contract suite + delivery failure cases.

**Assertions:** Debug off/on semantics remain governed; error surfaces preserve already-executed accounting; API keys/tokens/folder secrets never leak into reports, logs, export or backup; malformed provider results become explicit errors rather than false success.

**Evidence:** redaction scans, representative error records, zero-secret findings.

### PD-13 — conversation/tab ownership isolation

**Venue:** Chrome/Puppeteer + deterministic binding integration.

**Runners:** B16 browser remaining, B17 foreign-tab/pause cases, B19 resource fault/isolation campaign.

**Assertions:** a result/file prepared for conversation A cannot attach/send in B; foreign tab cannot stop/resume another owner; navigation between chats before final attach is rechecked; stale ownership fails closed.

**Evidence:** tab/conversation ids, blocked-action records, attach/send counters.

### PD-14 — export/import/migration/persistence

**Venue:** Node + IndexedDB browser contours.

**Runners:** 84 export suite, original/full Node suites, 78 backup suite, B19 resource large IndexedDB/restart cases.

**Assertions:** export paging/revision fence; backup/import/migration guards; active-work guards; persistent request/result/delivery state across worker/browser interruption; `normalizeSaved` reparses stored raw results without a new paid request.

**Evidence:** export page counts/revisions, migration/backup results, IndexedDB counts, before/after persisted records, provider-call count remains zero for normalizeSaved.

### PD-15 — security and provider containment

**Venue:** static + Node + controlled Chrome network.

**Runners:** `b12_contract.test.mjs`, B19 99 contract suite, `b19_network_browser.mjs`, Debug/backup containment tests.

**Assertions:** assistant content cannot inject URL, provider host, API key, folder id or permission; only fixed Search POST and Operation GET origins are reachable by deferred Search; Manual-disabled path is pre-network; owner secrets absent; no unexpected host permission added.

**Evidence:** blocked injection cases, observed controlled URLs, request headers with synthetic-only credential, manifest host list, redaction results.

### PD-16 — enabled-phase coverage and remaining phase locks

**Venue:** static + Node + controlled Chrome network.

**This section supersedes the obsolete B18 disabled-operation-host expectation.**

**Runners:** B19 Node campaign + `b19_network_browser.mjs` + manifest/static checks.

**Required B19 Search coverage:**

1. exact Search host permission present;
2. exact Operation host permission present;
3. `chrome.alarms` absent;
4. no background deferred poller;
5. `start` causes zero provider network;
6. explicit submit makes exactly the fixed `POST https://searchapi.api.cloud.yandex.net/v2/web/searchAsync` request under controlled fixture;
7. returned `operation_id` is durably persisted before later paid work;
8. explicit collect makes the fixed `GET https://operation.api.cloud.yandex.net/operations/<id>` request;
9. raw result is persisted before normalization;
10. normalization/export/delivery operate on the saved result;
11. injected URL/api_key/folder values cannot redirect/override governed provider configuration;
12. Manual disabled produces zero deferred network;
13. uncertain submit becomes `UNKNOWN`, one attempt, no automatic resubmit;
14. worker/browser recovery never invents a second paid submit;
15. ordinary Search/GenSearch and existing Webmaster/Metrika/Direct read paths still pass their normal full regression;
16. any operation still unsupported by the release fails before provider network.

**Evidence:** exact manifest, controlled request log, persisted operation/raw records, mode/poller proof, ordinary-service regression results.

### PD-17 — final exact-artifact cleanliness and complete evidence packet

**Venue:** package/static/reporting.

**Execute after every other PD:** rehash the original exact install ZIP; re-open/CRC it; fresh-extract again; recompute 67-file tree identity; compare against PD-00. Produce machine-readable PD-00..PD-17 matrix.

**Assertions:** no production mutation; no extra package files; no enabled `NOT_RUN`; real provider calls `0`; owner credentials/profile unused; exact final ZIP remains SHA `81d47...34e2`, 220045 bytes; all mandatory sections have explicit PASS/FAIL.

**Evidence:** final hashes/tree/file count, environment versions, command ledger, full matrix, all failures/NOT_RUN details, resource measurements, network boundary proof, one overall verdict.

## 6. Required classification

Each enabled PD section: explicit `PASS` or `FAIL` with evidence. `NOT_RUN` is allowed only as an intermediate state and forbids overall PASS.

Overall verdict MUST be exactly one of:

- `PASS`
- `FAIL_PRODUCT`
- `FAIL_ARTIFACT`
- `FAIL_HARNESS`

Classification rules:

- exact candidate established + product assertion fails → `FAIL_PRODUCT`;
- exact ZIP/tree/transport identity cannot be established → `FAIL_ARTIFACT`;
- exact candidate valid but qualified governed harness cannot execute a mandatory assertion → `FAIL_HARNESS`;
- every enabled PD-00..PD-17 independently PASS on the exact candidate → `PASS`.

Historical B13–B19 results are provenance only. They do not count as the independent verdict.

## 7. Release boundary after campaign

Until independent overall `PASS` is persisted for this exact ZIP:

```text
INDEPENDENT_CODEX_GATE = NOT_RUN / NOT_PASS
RELEASE_ALLOWED = NO
OWNER_INSTALLABLE_HANDOFF = FORBIDDEN
```

Only an independent PASS on exact SHA `81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2` may unlock owner handoff. Any production-byte correction creates a new candidate and restarts the complete independent campaign from PD-00.
