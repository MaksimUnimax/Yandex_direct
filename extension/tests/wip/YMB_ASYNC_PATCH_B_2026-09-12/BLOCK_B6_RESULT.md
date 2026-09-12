# Patch B — B6: trusted worker/Manual/owner binding and shared guard activation

Date: 2026-09-12. Status: **B6 SOURCE + QA CHECKPOINT SAVED / NOT BROWSER-ACCEPTED / NOT RELEASED**.

`RELEASE_ALLOWED = NO`  
`OWNER_ZIP_HANDOFF = FORBIDDEN`  
`NEW_PROVIDER_CALLS = 0`

## 1. Continuation boundary

B6 continued from the saved B5 checkpoint. Patch A and B1–B5 were not rewritten. The exact owner baseline remains `yandex-marketing-bridge-0.1.4-webmaster-readiness-gzip(2).zip`, SHA-256 `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`.

B5 shared admission remains the input authority for this block. B6 adds the worker-owned context resolver and governed bootstrap load order only; it does not enable the deferred provider runtime yet.

## 2. Implemented B6 behavior

New `candidate/b6/search_admission_worker_binding.js` resolves Search authority from durable worker state rather than command/chat metadata.

Manual Search is accepted only when all relevant worker-owned facts agree:

- verified conversation binding exists;
- Manual mode is enabled;
- active service is `search`;
- durable Manual operation is in `requesting` or `search_batch_requesting`;
- operation conversation/service/run/tab match the bound conversation;
- live owner-tab conversation check succeeds;
- if the Manual operation belongs to a paused Autorun, that paused run must match run/service/tab.

Autorun Search is accepted only when:

- Manual mode is off;
- claimed run ID equals the durable run;
- active service is Search;
- run state is `requesting`;
- `request_worker_session_id` equals the current worker session;
- bound/live owner conversation matches.

Arbitrary `job_id`, batch item IDs, claimed channel or run metadata do not create authority. Credential Check is not granted through this resolver; the previously protected B5 credential-check path remains separate.

If B6 installation cannot establish the governed guard, Search receives a fail-closed guard. Other services remain loadable instead of treating guard initialization failure as permission to bypass admission.

## 3. Bootstrap boundary

`evidence/B6_BOOTSTRAP_DELTA.diff` inserts only:

- `shared/search_async_policy.js`
- `shared/search_legacy_admission.js`
- `search_admission_worker_binding.js`

immediately after `webmaster_worker_runtime.js` and before Search Batch imports.

B6 deliberately does **not** load `search_async_store.js`, `search_async_protocol.js`, `search_async_transport.js` or `search_async_runtime.js`. Deferred provider execution therefore remains disabled at this checkpoint.

Exact bootstrap baseline SHA-256: `d1fe374068c91d6d5ff2d677e31c4f018931a98d8311cead7f8c1f475ade5647`.  
B6 postimage SHA-256: `6bbd3d52d41d52e1f5d6c4f724dbbb9450dec2012ec99712b127a0d063a2c7b5`.

## 4. Tests actually executed

Node v22.16.0. No real provider traffic.

B6 source suite after final harness correction:

- 26 tests;
- 26 PASS;
- 0 FAIL / 0 skipped;
- TAP SHA-256 `a6d521e7a19cc6a3b06fb6ebc8b8bd2505d39a8768a6c20286c31d4a12ac7abe`.

Fresh exact reconstruction:

- 26 tests;
- 26 PASS;
- 0 FAIL / 0 skipped;
- TAP SHA-256 `76141553877cf64ebf93bef432541be01b17751d1a94597fb9cd6ee354691551`.

Preserved B5 regression on unchanged B5 bytes was also rerun:

- 85 tests;
- 85 PASS;
- TAP SHA-256 `87e4cb00cbb5cae3eeff378b6acd2a917719ba99eda4e4e1d1d49ae51bcdbeba`.

Fresh B6 QA candidate:

- 56 files;
- 50 production JavaScript files passed `node --check`;
- `manifest.json` and `package.json` parsed successfully;
- candidate tree manifest SHA-256 `3eaef3a5811928e63bd81907d90fdc270df8421c133efae7766ef34c1b16d715`.

Detailed evidence is in `evidence/B6_TEST_RESULTS.json`.

## 5. Dependency-impact result

| Changed surface | Verified now | Not yet proven |
|---|---|---|
| Manual ownership resolver | durable operation state, channel/run spoof rejection, tab/conversation binding | installed Chrome tab lifecycle |
| Autorun resolver | run/session/service/state ownership | MV3 restart with real worker state |
| B5 guard composition | one provider callback, duplicate request rejection, spoofed channel rejection | real network/provider and real IndexedDB |
| bootstrap load order | exact baseline→postimage diff and import ordering | installed-extension load in qualified browser |
| preserved B5 behavior | 85/85 existing B5 tests rerun | full A+B integrated regression |
| deferred runtime | intentionally not loaded | B7 command/runtime integration |

## 6. Harness incidents recorded, not hidden

Three QA-layer defects occurred before/around fresh reconstruction:

1. the first materializer expected repository-style B5 paths that were not present in the local QA layout;
2. a second materializer attempt passed byte content to `shutil.copyfile` instead of writing bytes;
3. the fresh composition test still contained absolute `/mnt/data/...` source paths, so it was not independently portable.

All three are classified `FAIL_HARNESS`, not product PASS and not product FAIL. No production bytes changed because of them. The third issue was corrected to relative QA paths, the expected hash in `prepare_b6.py` was updated, and the complete 26-case source and fresh suites were rerun from the beginning and passed.

Final portable test SHA-256: `cf84b1b3c9f02b82de311838b263cb6d671c8b3a22656eb51a11d65866a1a84c`.  
Final materializer SHA-256: `9e9aed2df167f60f6b6172f157c106cd1b973813f16ea696939a75d10c2405f3`.

## 7. Browser/resource boundary

No new browser PASS is claimed. The managed Chromium environment remains governed by the previously observed administrative restrictions, including `URLBlocklist=["*"]` and `ExtensionInstallBlocklist=["*"]`. Those policies were not modified or bypassed.

Therefore B6 Node/fresh-QA evidence does **not** prove:

- real IndexedDB scheduling/durability;
- installed MV3 restart/recovery;
- real Chrome memory behavior;
- real ChatGPT DOM ownership;
- complete combined A+B behavior.

The release gate remains closed.

## 8. Exact continuation point

Do not restart A/B1–B6.

Next block B7:

1. add the separate `SEARCH_ASYNC_BATCH_API_V1` Manual-only command ingress;
2. require `YMBSearchAdmissionBinding.ready === true` before deferred actions;
3. bind deferred job ownership to the verified Manual conversation, not chat-supplied identifiers;
4. keep Autorun deferred disabled in this first integration;
5. expose bounded `start / submitN / collectN / collectReady / status / itemsPage / pause / resume / cancelPending` actions;
6. keep polling manual—no alarms/background provider work;
7. return compact state only; no raw result arrays in chat;
8. keep provider Operation host permission disabled until the actual deferred transport is deliberately wired and its dependency tests are ready.

After B7: bounded file export through preserved Patch A, then exact A+B candidate and every testable non-browser dependency. Real browser/IndexedDB/resource gates remain mandatory before release.

## ПРОСТЫМИ СЛОВАМИ

B6 привязал общий Search-контроль к настоящему состоянию worker: какой диалог владелец, включён ли Manual, какой run сейчас действительно выполняет Search и тот ли это worker. Подделать эти факты параметрами команды нельзя в проверенных сценариях. Старый B5 набор также не сломан в Node-проверках. Но это ещё не установленное расширение и не проверка памяти Chrome. Поэтому ZIP по-прежнему запрещён, а следующая работа начинается с B7, а не заново.
