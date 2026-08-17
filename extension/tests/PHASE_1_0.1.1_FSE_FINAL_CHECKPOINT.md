# Phase 1 0.1.1 — exhaustive full-system final controlled/package checkpoint

Date: 2026-08-17
Status: **CONTROLLED/PACKAGED PASS; REAL CURRENT-CHROME K-02 RERUN REQUIRED. PHASE 1 NOT LIVE PASS.**

## Test object and reason for campaign

The owner-installed K-02 generic-DOM patched candidate remained a real-current-Chrome FAIL: popup Manual was visibly ON while a supported `WORDSTAT_API_V1` local Copy remained ordinary/gray. The owner then ordered exhaustive whole-function testing with environment/input/output emulation rather than another selector guess.

Governed base candidate:

```text
yandex-marketing-bridge-0.1.1-phase1-k02-generic-dom-patch-candidate.zip
SHA-256: 46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c
files: 42
```

## Exhaustive discovery result

Formal positive controlled batches before patch:

```text
pure-module input/output matrix:               80/80 PASS
Chromium DOM/event matrix:                     34/34 PASS
worker/runtime/concurrency:                   112/112 PASS
popup/Manual/Start/reference UI:               41/41 PASS
transport/protocol/policy/security:            76/76 PASS
content/delivery/shared/source guards:         90/90 PASS
worker stale-content hard-gate targeted:        1/1 PASS
content authoritative sync targeted:            1/1 PASS
----------------------------------------------------------
formal positive controlled checks:            435 PASS
```

Base package supporting gate remained `319/319 PASS`, `37/37` syntax, `2/2` JSON, `42/42` fresh identity and Chromium pack exit `0`.

The assistant machine's real installed-MV3 gate is BLOCKED by managed Chromium policy (`ExtensionInstallBlocklist:["*"]`, `URLBlocklist:["*"]`); the policy was not bypassed.

## Demonstrated defects found by the exhaustive campaign

### FSE-DEF-07 — popup Manual desired state could diverge from active content state

The old popup committed `WS_SET_MANUAL_MODE` and then ignored the result of `WS_APPLY_MANUAL_MODE`. Two ON failure classes and two OFF failure classes were reproduced:

- tab transport failure;
- content returns `ok:true, applied:false`.

Old behavior could therefore show Manual ON success although the current content runtime had not armed Copy, or claim OFF cleanup although stale content remained armed.

Worker hard safety was independently proven intact: stale content click with authoritative worker Manual OFF returns `MANUAL_MODE_OFF` and produces zero mocked fetches. Content authoritative `WS_CONTENT_READY` pull/reload synchronization was also proven to reconcile ON/OFF correctly.

### FSE-DEF-08 — popup common async error boundary incomplete

`busy()` used `try/finally` without a common catch. Negative Send/Copy picker, Pause/Resume/Finish, Clear profile, Export/Import, diagnostic-clear and clipboard paths could escape as rejected async event handlers instead of controlled popup error status.

The complete demonstrated defect register is `PHASE_1_0.1.1_FULL_SYSTEM_EMULATION_DEFECT_REGISTER.md`.

## Final patch

Production scope: **only `popup.js`**.

Final Manual transaction order:

```text
ON:
  resolve exact current conversation
  → content APPLY ON must acknowledge ok:true + applied:true
  → only then commit worker hard gate ON
  → if worker ON commit fails, worker remains OFF and content is best-effort disarmed

OFF:
  commit worker hard gate OFF first
  → then content APPLY OFF
  → if cleanup is not acknowledged, keep worker/popup OFF but report explicit reconciliation error
```

Common popup `busy()` now catches otherwise-uncaught async action errors, renders controlled error status and still restores UI state.

No worker, content script, Manual-control adapter, Wordstat protocol, provider, pricing, request/result, delivery, credential, manifest permission or host-permission production code was changed by this patch.

Final production `popup.js` SHA-256:

```text
7286ea024033293110ad10ebc16856de0beacf512f6f86a229ac0271ac20c28c
```

## Final verification

```text
focused popup transaction/error matrix:        13/13 PASS
complete patched-tree suite:                  321/321 PASS
changed nonblank popup.js lines executed:       56/56
cross-layer safety/reconciliation rerun:        45/45 PASS
fresh ZIP complete suite:                     321/321 PASS
source ↔ fresh ZIP:                             42/42 byte-identical
JS/MJS syntax:                                  37/37 PASS
manifest/package JSON:                           2/2 PASS
manifest required entrypoints: all present
Chromium --pack-extension: exit 0
real/external Yandex requests during campaign:      0
```

The deterministic final ZIP was rebuilt twice byte-identically.

Final controlled/package candidate:

```text
yandex-marketing-bridge-0.1.1-phase1-fse-manual-popup-patch-candidate.zip
SHA-256: f06a16780bed8a1aedb6726c25baaa0667145d4adb14553868b294f95e807cc3
size: 180608 bytes
files: 42
```

Base-to-final changed files:

```text
popup.js
tests/popup_runtime_exhaustive.test.mjs
```

Only `popup.js` is production code. `manifest.json`, `service_worker.js`, `content_script.js`, `shared/manual_controls.js` and `shared/wordstat_protocol.js` are byte-identical to the governed base candidate.

Reproducible patch:

```text
extension/tests/patches/phase1-0.1.1-fse-manual-popup.patch.gz.b64
raw patch SHA-256: 77195780cdc7088cd763c636650c948895a2d62478d0111d051403aeedb04453
raw bytes: 21104
gzip SHA-256: ffff55adff96671e6336dd1879bede3a6bfb35b47f2c3bdc044d03763270feb0
gzip bytes: 4737
base64 SHA-256: f8d79faea01d1ab5284f06dbacb0b5075cb953cd4a19579190f1f3da4bb7c57b
base64 bytes: 6317
patch application to exact governed base reconstructs final tree: 42/42 exact files
```

Machine evidence:

```text
extension/tests/PHASE_1_0.1.1_FSE_MANUAL_POPUP_PATCH_EVIDENCE.json
schema: YMB_PHASE1_FSE_MANUAL_POPUP_PATCH_EVIDENCE_V1
```

## Effective K state

| ID | Effective status after this checkpoint |
|---|---|
| K-01 | NOT RUN on this final FSE candidate; all-four-method live closure still required. |
| K-02 | **REAL CURRENT-CHROME RERUN REQUIRED / previous candidate remains FAIL.** Controlled/package PASS does not override owner live evidence. On this candidate, Manual ON must either be positively acknowledged by content and visibly arm the supported Copy, or popup must remain/return OFF with an explicit error; false ON success is no longer accepted. |
| K-03 | NOT RUN; controlled Autorun regressions green. |
| K-04 | NOT RUN; controlled Debug/error regressions green. |
| K-05 | PASS controlled; final current-Chrome closure remains part of K campaign. |
| K-06 | PASS controlled; live result confirmation remains pending. |
| K-07 | **PASS on final FSE candidate** — 321/321 tree + 321/321 fresh ZIP + 56/56 changed lines + 42/42 identity + syntax/JSON/package gates green. |
| K-08 | NOT RUN / blocked until K-02 and remaining real-current-Chrome gates close. |

Phase 1 remains **NOT LIVE PASS**. Phase 2 Search remains blocked.
