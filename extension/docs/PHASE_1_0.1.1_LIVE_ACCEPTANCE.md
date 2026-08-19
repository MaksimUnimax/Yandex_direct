# PHASE 1 — 0.1.1 OWNER REAL-PROFILE LIVE ACCEPTANCE

Status: **MANDATORY FINAL OWNER-LIVE GATE / PENDING**  
Updated: 2026-08-19.

This document governs only the irreducible owner real-profile/current-production-ChatGPT acceptance that remains after the complete controlled Codex regression gate has already passed.

It does **not** repeat QA that Codex can reliably perform. The owner is not used as a repetitive manual QA runner.

## 1. Exact candidate authority

Only this exact artifact may be used for the current owner-live acceptance:

```text
yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
size 209697 bytes
files 45
```

The exact frozen product received a complete controlled Codex pre-delivery result:

```text
PD-00..PD-17: ALL PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
source/package identity: 45/45 PASS
real Yandex requests: 0
production modified during gate: NO
verdict: PASS
```

Historical artifacts including `311353…` and `4973c5…` are not current acceptance candidates.

Search remains blocked until this owner-live procedure passes.

## 2. Purpose of remaining owner-live acceptance

The remaining owner step exists only to prove behavior that depends on the owner's real Chrome/current production ChatGPT DOM/profile and therefore must not be fabricated from controlled fixtures.

The two open live blockers being closed are:

1. independent external Yandex action lifecycle versus native Copy;
2. Manual operation release after completed delivery so a subsequent Manual operation is admitted normally.

Issues #1 and #2 remain open until this exact artifact passes the checks below.

## 3. Installation / identity

The owner should receive the exact already-tested artifact. The owner must not reconstruct, patch or repackage it.

After installation/load, verify popup/runtime reports version `0.1.1`.

If migration of settings is required, use the product's normal Export/Import mechanism. Secret backup content remains private and must never be pasted into ChatGPT/GitHub.

## 4. Real-profile external Yandex action / native Copy independence

With Manual ON in the bound current conversation, use an eligible assistant code/writing block.

Required real-profile observations:

1. A newly rendered eligible block gets an enabled yellow `Яндекс` action even **before native Copy exists**, when that state is observable.
2. The Yandex action is visibly separate from native Copy and is not replacing/covering it.
3. When native Copy appears, the same Yandex action remains usable.
4. Trigger the native Copy/checkmark lifecycle if available: Copy appears → Copy state/checkmark changes → Copy disappears/re-renders/replacement appears.
5. The Yandex action remains present/usable through that lifecycle rather than disappearing with Copy.
6. Native Copy remains native Copy and does not execute a Bridge Manual operation.
7. Clicking the Yandex action performs one Manual admission for the bound block.
8. Manual OFF removes Bridge-owned Yandex controls and leaves the native ChatGPT surface intact.

A failure of any required observation is owner-live FAIL for issue #1.

## 5. Real-profile sequential Manual lock release

Use safe Manual operations that do not require a real Yandex request when practical, for example a controlled validation/no-command/error/result path that still exercises automatic report delivery.

Required sequence:

```text
first Manual admission
→ automatic result/error delivery completes
→ ChatGPT returns to ready/Microphone state
→ first Manual operation no longer blocks admission
→ second distinct Manual Yandex action is clicked
→ second Manual operation is admitted normally
```

Required observations:

- no stale `MANUAL_OPERATION_ACTIVE` after the first delivery has actually completed;
- no duplicate Send caused by recovery;
- no replay of the first block/provider operation;
- the second operation is genuinely admitted as a new operation.

A failure is owner-live FAIL for issue #2.

## 6. Real-profile plaques / composer safety

During the acceptance above, verify the visible Bridge status/reporting behavior that cannot be fully guaranteed by synthetic DOM alone:

- Bridge plaques appear in the expected top-right area rather than stacking over unrelated controls;
- repeated state updates do not visibly accumulate duplicate stale plaques;
- if the composer is already occupied when a Manual report is waiting, existing user text is not overwritten;
- where practical, clearing the composer allows the pending worker-owned report to resume once.

The occupied-composer branch need not be forced through unsafe manipulation if it cannot be produced naturally; controlled gate evidence remains authoritative for the internal branch. Any naturally observed violation is a live FAIL.

## 7. Real Yandex request policy during owner-live acceptance

The two current blocker closures above do **not** require a paid Yandex request.

Do not execute a real paid Yandex operation merely to repeat behavior already covered by the complete controlled gate.

If the owner explicitly chooses to perform a real Yandex command for additional live confidence, ChatGPT must freshly verify current official pricing immediately before the command, state the expected cost and preserve the no-blind-retry rule. This optional request is not required to close issues #1/#2 unless a later owner instruction changes the acceptance scope.

## 8. Acceptance verdict

PASS only if all mandatory real-profile observations above succeed on the exact artifact `31cc5f…`.

After PASS:

1. record owner-live evidence without secrets;
2. close issues #1/#2 as completed;
3. update `CURRENT_STATE.md` and `ROADMAP.md` to Phase 1 LIVE PASS;
4. only then unlock Phase 2 Search.

If any mandatory observation fails:

```text
owner-live FAIL
→ preserve exact evidence
→ keep issues/open phase blocked
→ ChatGPT performs root-cause analysis/fix
→ focused development tests
→ new frozen candidate if production bytes change
→ complete Codex pre-delivery gate again
→ repeat only the irreducible owner-live closure
```

The owner must not be asked to perform QA infrastructure setup, artifact transport or repetitive controlled test work.
