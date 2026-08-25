# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH REOPENED — REAL-PROFILE CONTEXT/BINDING DEFECT / OWNER LIVE BLOCKED**  
Updated: 2026-08-25

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_THIS_STATE_WRITE = c2a3eb60be9fe52c631d499b8a8a5e90b50a4765
LAST_FROZEN_PRODUCT_SOURCE = f4aee34c0a3455aa7199f6aa54bd581c71d97337
WITHDRAWN_HANDOFF_ARTIFACT = 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46 / 175971 bytes / 68 files / 71 ZIP entries
LAST_PAYLOAD_MANIFEST = bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478 / 11933 bytes
WINDOWS_SAFE_TRANSPORT = 7c787eedd9856c3f91fbed85aeaea7f3405ad473
CHATGPT_INTERNAL_ACTIONS_GATE = PASS on 739dd5d7... but is NOT the mandatory independent Codex gate
INDEPENDENT_CODEX_FULL_GATE_ON_739DD5D7 = NOT RUN
OWNER_LIVE = FAIL / BLOCKED BEFORE PROVIDER BOUNDARY
REAL_YANDEX_REQUESTS_FROM_FAILURE = 0
PRODUCTION_BYTES_CHANGED_SINCE_LAST_FREEZE = NO YET; PRODUCT REPAIR REQUIRED
OPEN_BLOCKERS = current real ChatGPT conversation cannot be confirmed, so Bind and Manual remain disabled; previous handoff skipped independent Codex QA
AUTHORIZED_NEXT_STAGE = PRODUCT_CONTEXT_BINDING_REPAIR
```

## Withdrawal of previous handoff

The exact `739dd5d7...` ZIP is withdrawn from owner-live use. Do not retry Search with it.

The repository Actions run `32801788251 / 97663951211` remains useful ChatGPT-owned internal QA evidence, but it was incorrectly treated as the independent Codex pre-delivery gate. The mandatory Codex campaign was not run. Therefore the previous owner-live authorization was invalid under `WORKFLOW_OPERATING_RULES.md`.

## Real-profile product defect

The owner's current real ChatGPT profile shows:

```text
Текущий ChatGPT = не определён
Привязать диалог = disabled
Ручной режим Yandex = disabled
```

No Yandex provider request was initiated.

Root-cause evidence already established:

1. `popup_context_bootstrap.js` treats any delivered `WS_GET_IDENTITY` response as bootstrap success even when `ok:false` or `conversation_key` is empty.
2. `popup.js` then requires `page.ok && conversation_key`, so the popup falls back to unavailable context and disables Bind/Manual.
3. reconstructed `shared/conversation_identity.js` restricts `/c/<id>` to RFC UUID version nibbles 1-5.
4. factual owner real-profile Phase-1 DOM evidence contains working ChatGPT URL `https://chatgpt.com/c/6a82924e-5ed0-83eb-84a2-851ddad40c88`; the current `[1-5]` UUID-version restriction rejects this proven real conversation id.
5. historical Phase-1 candidate manifest proves `shared/conversation_identity.js` had a different accepted byte identity before reconstruction (`e56a9f352c4668f47a0f72c2044a943a88457024c4400fa878a974551518114a`).
6. current content identity refresh uses only `location.href`; historical controlled/live DOM fixtures preserved canonical ChatGPT conversation URL evidence and the reconstructed path lost that fallback semantics.

## Required product repair

The authorized repair is limited to the proven context/binding/Manual layers:

```text
- restore conversation-id acceptance compatible with factual real ChatGPT ids without weakening trusted-origin fences;
- restore location + trusted canonical conversation identity resolution/fail-closed mismatch handling;
- make delivered-but-invalid WS_GET_IDENTITY an explicit failure/recovery case, never a bootstrap success;
- distinguish supported ChatGPT page context from confirmed conversation/binding as the older working popup did;
- surface a truthful context error instead of silent `не определён` plus false-ready state;
- restore the proven Manual transaction semantics after confirmed binding;
- add fail-first regression using factual id 6a82924e-5ed0-83eb-84a2-851ddad40c88 and live-receiver-invalid-identity case;
- zero Yandex requests during focused repair QA.
```

## Historical working authority being used for repair

```text
controlled accepted Phase-1 source: 653adb63a68f98f03f21534658f3397fd389e0c6
accepted artifact: 4973c5f87c3ad7d4c052e66c449c2afef412d20a6e4d767bbe761d62abf7cb84
real-profile evidence: extension/tests/PHASE_1_0.1.1_REAL_PROFILE_LIVE_EVIDENCE_2026-08-18.md
factual real ChatGPT DOM/URL: extension/tests/PHASE_1_0.1.1_LIVE_CHATGPT_DOM_EVIDENCE_2026-08-17.md
Manual transaction authority: extension/tests/PHASE_1_0.1.1_FSE_MANUAL_POPUP_PATCH_R4_TRANSACTION_PASS.md
```

The old real-profile evidence proves Manual OFF/ON and current ChatGPT block binding worked before the later stale-manual-operation defect.

## Workflow boundary after repair

During repair ChatGPT runs focused tests only. If production bytes change, a new exact candidate is required. Before any future owner handoff, the exact new frozen artifact must go through the mandatory independent Codex pre-delivery campaign. ChatGPT's own Actions/preflight cannot substitute for Codex.

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = REPAIR_CONTEXT_BINDING_AGAINST_HISTORICAL_REAL_PROFILE_AUTHORITY
OWNER_LIVE_SEARCH = BLOCKED
PHASE_3_WEBMASTER = BLOCKED
```
