# Phase 1 — 0.1.1 real-profile live evidence — 2026-08-18

Authority before this evidence: `0d61b08177307d476542f9a317141e8469640566`.
Exact accepted artifact: `yandex-marketing-bridge-0.1.1-phase1-final-live-acceptance-candidate.zip`, SHA-256 `4973c5f87c3ad7d4c052e66c449c2afef412d20a6e4d767bbe761d62abf7cb84`.

## LIVE-RP-01 — Manual OFF/ON visual + marker-without-JSON safe error

Owner reported the requested real-profile visual checks as normal: Manual OFF left native Copy state, Manual ON armed the local block with the Yandex action, and generic whole-response Copy produced no Bridge action.

The clicked test block unintentionally contained the literal `WORDSTAT_API_V1` marker in explanatory prose, so this execution is classified as marker-without-JSON rather than a pure no-command case.

Actual automatic result:

- envelope: `YMB_MANUAL_BLOCK_RESULT_V1`
- bridge/version: `yandex-marketing-bridge` / `0.1.1`
- channel/service: `manual` / `wordstat`
- status: `ERROR`
- item stage/code: `COMMAND_DISCOVERY` / `MISSING_JSON`
- message: `После WORDSTAT_API_V1 должен идти JSON-объект.`
- `request_executed:false`
- `automatic_retry:false`
- `http_status:0`
- estimated cost: `0`
- no real Yandex provider request observed from this case.

Conclusion: real-profile Manual visual OFF/ON and generic-copy exclusion were reported normal; safe marker-without-JSON error delivery PASS. Pure no-command remains to be tested separately because the input accidentally contained the protocol marker.

Deferred UI issue for the next patch is tracked as GitHub issue #1: native Copy and Yandex action must become physically/action-independent sibling controls. No production patch was made during this live step.

## LIVE-RP-02 — stale Manual-operation lock after delivered result — FAIL / LIVE BLOCKER

After LIVE-RP-01 had already been automatically delivered into the bound ChatGPT conversation, several minutes and multiple subsequent conversation turns elapsed. Manual remained ON and Debug was enabled for the next safe malformed-command test.

The next Yandex action was captured by the real content script but the worker rejected it before malformed-command parsing.

Actual automatic result:

- envelope: `YMB_ERROR_V1`
- bridge/version: `yandex-marketing-bridge` / `0.1.1`
- service/channel: `wordstat` / `manual`
- stage: `WS_EXECUTE_MANUAL_BLOCK`
- code: `MANUAL_OPERATION_ACTIVE`
- message: `Bridge уже выполняет или доставляет другой ручной блок.`
- `recoverable:true`
- `request_executed:false`
- `automatic_retry:false`
- `run_id:null`
- no real Yandex provider request occurred.

Debug evidence also proved the real current ChatGPT DOM adapter remained bound and active (`chatgpt_pre_codemirror_v1`), `manual_enabled:true`, and the clicked block was captured by `MANUAL_BLOCK_CLICK_CAPTURED`. Therefore this was not a DOM-binding miss; admission was blocked by stale worker Manual-operation state.

Expected behavior: once a terminal Manual result/error has been automatically delivered and the delivery boundary is confirmed/reconciled, the single-flight Manual lock must be released so a later explicit Manual action can be admitted. The lock must remain only while a Manual transaction is genuinely active or an irreversible/delivery boundary remains unresolved.

Classification: **FAIL / PRODUCT LIVE BLOCKER**. Remaining Manual-command live tests on this exact candidate are blocked because they would hit the same stale lock rather than exercise their intended behavior.

Tracked as GitHub issue #2. The next product patch must both preserve the genuine in-flight fence and deterministically release it after completed Manual delivery, with focused positive/negative regressions and permanent coverage added to the pre-delivery regression gate.
