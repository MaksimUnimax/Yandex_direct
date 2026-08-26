# Mandatory gate addendum — lifecycle-blocked Manual action gating

Status: **MANDATORY / PART OF THE PRE-DELIVERY FULL REGRESSION GATE**  
Date: 2026-08-26  
Applies to the lifecycle-button patch candidate and remains a regression invariant for later candidates carrying this behavior.

This addendum is mandatory together with the living pre-delivery gate, Manual-ON transaction addendum, Search addendum, native popup geometry addendum and QA transport runbook.

## 1. Owner-visible defect / required behavior

During owner functional testing the Bridge backend correctly rejected new Manual activity with:

```text
MANUAL_OPERATION_ACTIVE
DELIVERY_IN_PROGRESS
```

and `request_executed=false`, but the Bridge-owned `Яндекс` action remained clickable.

Required product invariant:

```text
blocking lifecycle already active
-> existing Bridge-owned Yandex action remains present
-> action is disabled/non-clickable before owner interaction
-> blocked click cannot dispatch a new Manual block execution
-> backend admission guard remains fail-closed defense in depth
-> only positively observed lifecycle/outbox clear may re-enable action
```

The UI availability refresh must not reset Manual/Autorun worker timing, delivery state, provider state, binding, credentials, policy or unrelated runtime state.

## 2. Blocking states

At minimum the installed-extension regression must cover:

```text
active non-terminal manual_operation -> MANUAL_OPERATION_ACTIVE UI block
present conversation outbox delivery_id -> DELIVERY_IN_PROGRESS UI block
```

A local click-to-authoritative-refresh admission hold may additionally keep actions disabled while the just-started Manual operation has not yet appeared in the worker public state.

## 3. Deterministic source/package regression

The complete source and packaged suites must include assertions equivalent to:

- active non-terminal `manual_operation` maps to the Manual-operation blocker;
- active delivery hold maps to the delivery blocker;
- blocker evaluation occurs before `WS_EXECUTE_MANUAL_BLOCK` dispatch;
- action availability is refreshed from authoritative worker state/outbox observation;
- lifecycle completion re-enables the action;
- no unconditional `button.disabled=false` bypasses authoritative lifecycle state.

For the frozen lifecycle-button candidate the expected development source-suite count is `247/247`; Codex must report actual source and packaged counts rather than assuming that number.

## 4. Mandatory installed-extension browser regression

Independent Codex must execute the QA-only harness below against a fresh extraction of the **same exact transported frozen artifact**:

```text
branch = qa/lifecycle-button-gating-browser-harness-939e880-2026-08-26
commit = 1009b224d1cfe389f6f041a16cd2a8d53657284a
path = extension/tests/qa_browser/lifecycle_button_gating_gate.mjs
blob = 43739af40d50c35d910752c0cdb1371487393e9a
base product source = 939e880f820e52beae9dcbcedc86d5cd9e13b075
```

Verify the QA branch is exactly one commit above the product source and its entire delta is exactly the one harness file. Codex must not edit the harness.

Qualified browser dependency target:

```text
Chrome for Testing = 151.0.7922.47
puppeteer-core = 25.4.0
isolated temporary QA profile
```

Use the controlled historical ChatGPT TLS fixture certificate/key or an equivalent already-governed controlled fixture route. All Yandex provider host traffic must remain locally controlled/stubbed; no real credentials and no real Yandex request are permitted.

The harness exercises the real installed extension, real popup Manual ON transaction and the real content/worker storage lifecycle. It requires these markers:

```text
LIFECYCLE_BUTTON_INITIAL_ENABLED_PASS
LIFECYCLE_MANUAL_OPERATION_DISABLED_PASS
LIFECYCLE_MANUAL_OPERATION_BLOCKED_CLICK_NO_DISPATCH_PASS
LIFECYCLE_MANUAL_OPERATION_CLEAR_REENABLE_PASS
LIFECYCLE_DELIVERY_DISABLED_PASS
LIFECYCLE_DELIVERY_BLOCKED_CLICK_NO_DISPATCH_PASS
LIFECYCLE_DELIVERY_CLEAR_REENABLE_PASS
LIFECYCLE_GATE_PROVIDER_HITS=0
LIFECYCLE_GATE_REAL_YANDEX_REQUESTS=0
LIFECYCLE_BUTTON_GATING_BROWSER_GATE_PASS
```

Any missing marker, enabled action during a blocker, runtime mutation caused by a blocked click, failure to re-enable after positive clear, provider hit, or harness/product byte mutation is a gate failure.

## 5. ChatGPT preflight evidence is not independent gate credit

ChatGPT development preflight already executed this harness on the exact reassembled frozen artifact and observed all required markers. That proves the harness is executable and reduces QA-process risk, but it is **not** transferable independent Codex PASS credit.

Preflight reference:

```text
GitHub Actions run = 32920317520
job = 98032481002
Chrome = 151.0.7922.47
puppeteer-core = 25.4.0
exact artifact SHA-256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
result = PASS
```

Codex must rerun the lifecycle browser gate independently as part of the complete campaign.

## 6. Final PASS rule

The complete pre-delivery campaign cannot return PASS unless this lifecycle browser regression is PASS in addition to every other enabled living gate section.

Required final report field:

```text
lifecycle_button_gating_browser: PASS|FAIL|NOT_RUN
```

For overall PASS, this field must be `PASS`, real credentials must be `NO`, real Yandex requests must be `0`, relevant source/package/harness bytes must remain unchanged, and enabled `NOT_RUN` count must remain zero.
