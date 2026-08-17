# Phase 1 0.1.1 — Manual Surface v2 changed-production coverage checkpoint

Date: 2026-08-17
Status: **SOURCE + CHANGED-PRODUCTION EXECUTION PASS; FRESH PACKAGE / REAL CHROME STILL PENDING.**

Base artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-fse-manual-popup-patch-candidate.zip
SHA-256: f06a16780bed8a1aedb6726c25baaa0667145d4adb14553868b294f95e807cc3
```

Authorities:

- `extension/docs/MANUAL_CODE_BLOCK_ACTION_CONTRACT_V2_2026-08-17.md`
- `extension/tests/PHASE_1_0.1.1_MANUAL_SURFACE_V2_PATCH_PLAN.md`
- `extension/tests/PHASE_1_0.1.1_LIVE_CHATGPT_DOM_EVIDENCE_2026-08-17.md`

## Cleanup before coverage closure

Coverage inspection identified four branches that were structurally unreachable/redundant rather than missing tests. They were removed instead of retained as untestable defensive clutter:

1. `block_command_discovery.extractBalancedObject()` `INVALID_JSON_BALANCE` branch after starting at `{`: depth cannot become negative because the function returns immediately when depth reaches zero.
2. `INVALID_JSON_ROOT` after a successfully balanced/parsed `{...}` object: a valid JSON text beginning with `{` cannot parse to a scalar/array root.
3. A second post-loop `stopAfterUnknown` sweep: the main serial loop already marks every later pending item `NOT_EXECUTED_AFTER_UNKNOWN_OUTCOME` after an UNKNOWN initiation.
4. A single-item `single_report_text || fallback` branch where the surrounding condition already requires `single_report_text` to be truthy.

No API/provider semantics were broadened by this cleanup.

## Added reachable safety coverage

Targeted tests now execute the remaining meaningful changed paths, including:

- direct missing/unterminated balanced-object extraction;
- current writing-block body missing/ambiguous and root-unsupported DOM reasons;
- runtime `WS_MANUAL_DELIVERY_AVAILABLE` mismatch + successful claimed delivery path;
- invalid Wordstat command validation in worker with zero fetch;
- known registry service without an enabled Phase-1 provider → `SERVICE_NOT_ENABLED`, zero fetch;
- missing/non-requesting durable Manual operation;
- paused RUN disappearing before a provider item → fail closed, zero fetch;
- unknown recovery with no operation id and with empty legacy batch items;
- recovery exception path;
- oversized Manual block rejection before durable claim/provider;
- active service mismatch before durable claim/provider;
- unexpected post-claim execution failure becoming one durable chat-visible error;
- successful `resumeManualBatchAndPush` provider completion + one delivery push.

## Full source regression after cleanup/tests

```text
tests:      358
pass:       358
fail:         0
skipped:      0
cancelled:    0
```

No real/external Yandex request was issued. Provider calls in these tests were controlled mocks.

## V8 changed-production execution result

A fresh full `358/358` run was executed with Node V8 precise coverage enabled. Coverage was aggregated across all test processes and compared only against nonblank lines added/replaced relative to the exact governed base artifact.

Result:

```text
content_script.js                     203 / 203
service_worker.js                     776 / 776
shared/block_command_discovery.js     218 / 218
shared/manual_controls.js               2 /   2
shared/wordstat_protocol.js            16 /  16
------------------------------------------------
TOTAL                                1215 / 1215
uncovered changed nonblank lines                 0
```

This is changed-production execution evidence, not a claim that every unchanged legacy line in the extension has 100% source coverage.

## Gate state

- Source regression: PASS (`358/358`).
- Changed-production nonblank execution: PASS (`1215/1215`).
- Real Yandex requests during patch/testing: 0.
- Fresh deterministic ZIP/package identity: PENDING.
- Fresh-ZIP complete regression: PENDING.
- Real-current-Chrome Manual visual K-02: PENDING and cannot be closed by this controlled result.

Phase 1 remains **NOT LIVE PASS**; Phase 2 remains blocked.
