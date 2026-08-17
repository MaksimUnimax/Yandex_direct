# Phase 1 0.1.1 — final FSE candidate real-current-Chrome K-02 result

Date: 2026-08-17
Candidate: `yandex-marketing-bridge-0.1.1-phase1-fse-manual-popup-patch-candidate.zip`
SHA-256: `f06a16780bed8a1aedb6726c25baaa0667145d4adb14553868b294f95e807cc3`

Status: **K-02 / C-01 FAIL in owner real current Chrome.**

## Procedure

The owner installed/reloaded the exact final FSE candidate, refreshed the current ChatGPT conversation and performed the zero-Yandex-request visual Manual Copy test. Four code blocks were displayed:

1. supported `WORDSTAT_API_V1` + `{"method":"getRegionsTree"}`;
2. non-command control text;
3. bare JSON without the protocol marker;
4. plain Wordstat visual-control text.

The owner was instructed not to click Copy. Therefore this test executed **zero Yandex requests**.

## Actual

- The supported `WORDSTAT_API_V1` block local Copy remained ordinary/gray instead of receiving the governed Yandex-yellow Manual action decoration.
- All three negative controls also remained ordinary/gray, which is correct for those controls.
- Supplied diagnostics contained `CONTENT_RUNTIME_STARTED`, `CONVERSATION_BOUND`, and `SETTINGS_IMPORTED` for the current confirmed conversation/runtime `0.1.1`.
- The supplied diagnostics did not contain a Manual apply/readiness/decorated-count event capable of proving which content-side branch rejected or failed to decorate the supported block.

## Expected

With Manual enabled for the current conversation, the supported command's unique local code-block Copy must visibly enter the governed Yandex Manual-ready state before any API execution. Negative controls and generic assistant-level Copy must remain native/non-trigger controls.

## Classification

This is a real-current-Chrome K-02/C-01 FAIL on the final FSE candidate. The prior controlled/package PASS does not override it.

The current diagnostic schema is also insufficient to localize the live failure because it does not record the complete Manual activation/admission chain (popup request -> worker state -> content apply -> content Manual/readiness state -> supported binding count -> local Copy candidate count -> decorated button count / fail-closed reason). This diagnostic limitation is an implementation/testability gap; it is not missing operator evidence.

No new DOM/provider patch is authorized solely from this observation. Root-cause work must compare the proven Ozon Manual/Copy admission architecture and the final Yandex product contract before changing production code.
