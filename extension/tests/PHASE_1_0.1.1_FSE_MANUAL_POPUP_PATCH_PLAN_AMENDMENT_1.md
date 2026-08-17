# Phase 1 0.1.1 — FSE Manual/popup patch plan amendment 1

Date: 2026-08-17
Status: PLAN AMENDMENT — committed before revision-2 implementation.
Base plan: `PHASE_1_0.1.1_FSE_MANUAL_POPUP_PATCH_PLAN.md`.
Trigger: revision-1 changed-line coverage reached 26/28 changed nonblank `popup.js` lines and exposed an avoidable second-order worker-rollback-failure branch.

## Transaction-order refinement

The production scope remains **only `popup.js`**. No worker/content/provider/transport/permission change is authorized.

### Manual ON — content acknowledgement before worker authorization

Required order:

1. current ChatGPT tab/conversation is resolved and confirmed;
2. while authoritative worker Manual remains OFF, send `WS_APPLY_MANUAL_MODE {enabled:true}` to that exact content runtime;
3. proceed only if acknowledgement has `ok === true && applied === true`;
4. only then commit worker desired/hard-gate state ON with `WS_SET_MANUAL_MODE`;
5. if content apply fails or reports `applied:false`, worker is never committed ON; popup remains/returns OFF and shows an explicit error;
6. if content apply succeeds but worker ON commit fails, worker remains OFF and popup must best-effort disarm content with `WS_APPLY_MANUAL_MODE {enabled:false}`; popup stays OFF and reports the commit failure;
7. success is reported only after both content apply and worker ON commit succeed.

Safety invariant: no transient worker authorization may exist before the current content runtime has positively acknowledged Manual activation.

### Manual OFF — worker hard gate before content cleanup

Required order remains safety-first:

1. commit worker desired/hard-gate state OFF first;
2. then send `WS_APPLY_MANUAL_MODE {enabled:false}` to current content;
3. if content cleanup succeeds, report normal OFF success;
4. if transport fails or content reports `applied:false`, keep worker OFF and popup OFF but report explicit incomplete-reconciliation error; never claim observer/listeners/yellow decoration were removed;
5. later `WS_CONTENT_READY`/authoritative pull remains the recovery path and must still reconcile stale content OFF.

## New mandatory focused cases before final acceptance

- ON + content transport failure: worker receives no ON commit; popup OFF/error.
- ON + content `applied:false`: worker receives no ON commit; popup OFF/error.
- ON + content apply success + worker ON commit success: worker/content/popup ON.
- ON + content apply success + worker ON commit failure: worker remains OFF; best-effort content OFF attempted; popup OFF/error.
- ON + worker commit failure + cleanup content OFF failure: worker still OFF; popup OFF/error; no false success.
- OFF + worker OFF commit failure: do not claim OFF success; content is not relied on as authoritative safety gate.
- OFF + worker OFF success + content cleanup transport failure: worker/popup OFF + reconciliation error.
- OFF + worker OFF success + content `applied:false`: same safe/error state.
- OFF + both succeed: normal OFF success.
- stale content click while worker OFF remains zero-fetch `MANUAL_MODE_OFF`.
- content authoritative startup/resync ON→OFF remains green.

Every changed nonblank `popup.js` line must execute in controlled tests before packaging. No real/external Yandex request is permitted.
