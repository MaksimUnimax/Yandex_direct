# B19 — independent Codex pre-delivery gate prompt for exact 0.1.6

Use this prompt only for the final independent QA campaign. Codex is the independent QA executor, not the developer.

---

Continue independent pre-delivery QA for Yandex Marketing Bridge.

THIS IS A QA EXECUTION TASK.
THIS IS NOT A DEVELOPMENT TASK.

DO NOT EDIT PRODUCTION CODE.
DO NOT FIX FAILURES.
DO NOT CHANGE OR WEAKEN TEST ASSERTIONS.
DO NOT SUBSTITUTE OR REBUILD A DIFFERENT PRODUCT CANDIDATE.
DO NOT SILENTLY ACCEPT HISTORICAL PASS AS YOUR OWN VERDICT.
DO NOT MAKE LIVE/PAID YANDEX PROVIDER CALLS.
DO NOT USE OWNER CREDENTIALS OR OWNER BROWSER PROFILE.

Repository:
`MaksimUnimax/Yandex_direct`

Evidence / working branch:
`wip/ymb-file-delivery-patch-a-2026-09-12`

Read IN FULL before execution:

1. `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`
2. `extension/docs/YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md`
3. `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/BLOCK_B18_RESULT.md`
4. `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/B19_NODE_GATE_CHECKPOINT.md`
5. `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/B19_NETWORK_GATE_CHECKPOINT.md`
6. `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/B19_FINAL_PACKAGE_GATE_CHECKPOINT.md`
7. `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/B19_PRE_CODEX_TRANSPORT_READBACK_2026-09-13.md`
8. `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/B19_FINAL_PD_EXECUTION_MAP.md`
9. current `extension/tests/wip/YMB_FILE_DELIVERY_PATCH_A_2026-09-12/CONTINUATION_CURSOR_2026-09-12.json`

## B19 authority override — mandatory

For this exact `0.1.6` candidate, `B19_FINAL_PD_EXECUTION_MAP.md` is the mandatory execution authority for mapping `PD-00..PD-17` to concrete runners/harnesses.

Historical B18 material remains provenance only where it conflicts with the final B19 enabled phase. In particular, the old B18 requirement that `operation.api.cloud.yandex.net` remain disabled is **SUPERSEDED FOR B19** and MUST NOT be applied to 0.1.6.

B19 intentionally enables deferred Search provider networking in **Manual-only** mode. The expected product boundary is therefore:

- Search host permission enabled;
- Operation host permission enabled;
- `chrome.alarms` absent;
- no hidden/background deferred poller;
- explicit Manual `start -> submit/submitN -> searchAsync POST -> persist operation_id -> WAITING -> explicit collect/collectN/collectReady -> Operation GET -> persist raw -> normalize -> export/delivery`;
- injected provider URL, API key or folder values fail closed and cannot override governed settings;
- uncertain submit becomes `UNKNOWN` and is never automatically resubmitted.

Do **not** edit production or QA assertions to restore the obsolete disabled-operation-host state.

The exact artifact transport/readback has already been independently re-consumed through the GitHub Actions artifact route and recorded in `B19_PRE_CODEX_TRANSPORT_READBACK_2026-09-13.md`. Use that same direct artifact route; do not ask the owner to download, upload, copy, rename, extract or otherwise transport QA artifacts.

QA/document commits made on the working branch after the frozen candidate was produced do not change the exact product ZIP or its extracted product tree. Do not compare later QA-only branch commits with the candidate and misclassify expected documentation drift as product drift.

If a governed runner requires product bytes at `extension/src`, use a disposable QA workspace only: fresh-extract the exact install ZIP, verify the exact 67-file tree SHA first, stage those exact bytes into the disposable runner path, and verify the product tree again after the campaign. That staging is not authorization to edit production.

Historical B17/B18/B19 artifacts may be used only as qualified fixture/harness inputs exactly as specified by `B19_FINAL_PD_EXECUTION_MAP.md`. They are not the 0.1.6 candidate and none of their historical PASS results transfers into the independent verdict.

Execute the complete B19 map. No enabled `PD-00..PD-17` section may remain `NOT_RUN` if overall verdict is `PASS`.

## Exact artifact under test — immutable

You MUST test this exact installable ZIP and no other product bytes:

Filename:
`Yandex-Marketing-Bridge-0.1.6.zip`

SHA-256:
`81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2`

Bytes:
`220045`

Extracted product tree SHA-256:
`b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86`

Product files:
`67`

Primary GitHub Actions artifact containing the exact ZIP and package evidence:

- run id: `34737506830`
- artifact id: `10311695957`
- artifact name: `ymb-0.1.6-final-owner-candidate`
- artifact SHA-256: `07d9b9e70181983172b7af448e07e087ec9551144905562e506053670c40b059`
- artifact bytes: `225323`

The artifact contains `Yandex-Marketing-Bridge-0.1.6.zip`, `PACKAGE_RESULT.json`, `FINAL_PACKAGE_GATE.json`, source hashes and fresh-extracted browser evidence.

Download the existing exact artifact. Do not rebuild the product if the exact artifact is available. If you cannot obtain and verify the exact ZIP SHA/size, stop with `FAIL_ARTIFACT` rather than substituting another build.

## Final product boundary

This is the **network-enabled** deferred Search release candidate.

Manifest must contain both Yandex Search origins exactly as expected:

- `https://searchapi.api.cloud.yandex.net/*`
- `https://operation.api.cloud.yandex.net/*`

`chrome.alarms` must remain absent.

Deferred Search is Manual-only. There must be no hidden/background deferred poller.

Expected deferred lifecycle:

`start -> submit/submitN -> POST /v2/web/searchAsync -> persist operation_id -> WAITING -> explicit collect/collectN/collectReady -> GET /operations/<id> -> persist raw result -> normalize -> export/delivery`

An uncertain submit outcome must become `UNKNOWN` and MUST NOT be automatically resubmitted.

## Provider safety boundary for this independent gate

Real provider calls: **0**.

Use only synthetic credentials and controlled provider/network fixtures.

The purpose is to independently validate the release code's routing, authorization-boundary handling, request lifecycle, persistence, recovery, delivery and resource behavior without spending owner quota or using owner secrets.

Do not use a real Yandex key merely to make the gate more realistic. A live-provider canary is a separate owner-authorized action and is not part of this independent regression campaign.

## Mandatory independent campaign

Execute every enabled `PD-00` through `PD-17` from `B19_FINAL_PD_EXECUTION_MAP.md` and the authoritative permanent gate in one governed campaign against the exact ZIP above.

Historical B13–B19 results are provenance and known test venues only. They do not count as your independent result.

Browser-owned assertions must run in a qualified real Chrome/Puppeteer venue on a fresh extraction of the exact ZIP.

Internal deterministic/state assertions may use the qualified Node/VM/IndexedDB/network-fixture venues defined by the authorities, but they must run again independently on the exact 0.1.6 bytes.

At minimum, independently exercise and classify:

- package identity, CRC, path safety, 67-file fresh extraction and exact tree identity;
- JS/JSON/manifest/load-order/static checks;
- MV3 install, worker lifecycle/restart, popup/content initialization;
- Wordstat existing methods and error delivery;
- ordinary Search and GenSearch regression;
- Webmaster, Metrika and Direct existing read paths;
- shared admission/cost/accounting behavior;
- Manual ownership and conversation/tab isolation;
- deferred Search start/submit/collect/state transitions on controlled provider responses;
- fixed provider origins and credential/folder containment;
- operation ID persistence before subsequent paid work;
- UNKNOWN/no-auto-retry behavior;
- recovery after worker/browser interruption;
- raw-result-before-normalization persistence and local `normalizeSaved` repair;
- exportPage paging/revision fence;
- bounded file staging and attachment delivery;
- duplicate-Send protection;
- wrong-chat/navigation isolation;
- pause/resume and persisted delivery pause;
- corrupted-chunk failure behavior;
- 10/100/500/1500 IndexedDB item contours where required;
- 1/10/32/64 MiB and repeated 64 MiB file/resource contours where required;
- backup/import/migration and active-work guards;
- Debug/error redaction and no credential leakage;
- final browser process cleanup and resource thresholds.

Do not stop at the first ordinary product failure if unrelated mandatory sections can still be executed safely. Return the complete failure set.

## Resource safety

The historical catastrophic RAM failure is release-critical. Independently measure the qualified Chrome process tree and enforce the gate's resource requirements.

Development reference only — NOT your PASS:

- fresh-extracted package resource gate had 16 browser cases, zero failures;
- peak owned Chrome RSS observed: `1811652 KiB`;
- emergency development limit: `2097152 KiB`;
- remaining processes after cleanup: `0`.

You must measure independently. Do not copy these numbers as your own result.

## Required final classification

For every enabled PD section return the exact allowed PASS/FAIL state required by `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` and `B19_FINAL_PD_EXECUTION_MAP.md`.

Overall verdict must be exactly one of:

- `PASS`
- `FAIL_PRODUCT`
- `FAIL_ARTIFACT`
- `FAIL_HARNESS`

Overall PASS is forbidden if any enabled mandatory section is NOT_RUN.

If a product assertion fails:

- preserve exact evidence;
- do NOT patch the product;
- do NOT design the fix;
- continue unrelated safe checks;
- return the complete failure set to main ChatGPT.

If artifact or harness fails:

- preserve exact evidence;
- do NOT modify production bytes;
- classify the failure accurately.

## Required evidence output

Produce one durable independent acceptance packet containing at minimum:

1. exact input artifact/ZIP SHA-256, bytes and filename;
2. fresh extraction file count and exact product-tree identity;
3. Node/Chrome/Puppeteer/platform versions;
4. exact commands/test entry points used;
5. full machine-readable `PD-00..PD-17` matrix;
6. all FAIL and NOT_RUN details;
7. full resource measurements and process-cleanup results;
8. network boundary proof: controlled provider only, real provider calls = 0;
9. confirmation that owner credentials/profile were not used;
10. confirmation that production bytes stayed unchanged during QA;
11. exact final ZIP identity at the end of the campaign;
12. one overall verdict.

The exact ZIP that receives independent PASS is the only package that main ChatGPT may hand to the owner.

Do not implement fixes.

---

Expected pre-gate state:

```text
PRODUCT_VERSION = 0.1.6
PRODUCT_TREE_SHA256 = b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86
INSTALL_ZIP_SHA256 = 81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2
INSTALL_ZIP_BYTES = 220045
DEFERRED_NETWORK = ENABLED_MANUAL_ONLY
OPERATION_HOST_EXPECTED = ENABLED
B18_DISABLED_OPERATION_HOST_EXPECTATION = SUPERSEDED_FOR_B19
PRE_CODEX_TRANSPORT_READBACK = PASS
B19_FINAL_PD_EXECUTION_MAP = READY
DEVELOPMENT_NODE_GATE = PASS
DEVELOPMENT_RESOURCE_CHROME_GATE = PASS
DEVELOPMENT_DEFERRED_NETWORK_CHROME_GATE = PASS
DETERMINISTIC_PACKAGE_GATE = PASS
FRESH_EXTRACTION_GATE = PASS
REAL_PROVIDER_CALLS_AUTHORIZED = 0
OWNER_CREDENTIALS_ALLOWED = NO
INDEPENDENT_CODEX_GATE = NOT_RUN
RELEASE_ALLOWED = NO
```
