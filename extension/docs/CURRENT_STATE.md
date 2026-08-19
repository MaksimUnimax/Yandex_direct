# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY**  
Updated: 2026-08-19

This file applies **immediately in the current conversation** and is the first compact state record for every new/resumed conversation. It exists so workflow state is reconstructed from live GitHub rather than chat memory or stale historical candidate blocks.

## Live repository rule

Repository: `MaksimUnimax/Yandex_direct`  
Branch: `main`

**Always fetch live `main` HEAD before action.** Do not trust a remembered SHA. Because updating this file itself creates a new commit, the exact current HEAD is intentionally not hard-coded as permanent truth here.

The last live HEAD observed immediately before this reconciliation record was written was:

```text
143f920212d3cee12305a96a95bd05ba7d82bc78
```

When this file is read later, live GitHub wins over that historical observation.

## Current exact product candidate

Version:

```text
0.1.1
```

Exact frozen source used by the latest complete Codex gate:

```text
D:\codex\Yandex\work\ymb-full-gate-20260819-02\source
```

Critical frozen production hashes:

```text
content_script.js 6358418ff04de37a21368a28046c1109280a7a6b8d942972a319d4dc09dabd9e
service_worker.js 2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

Exact tested/handoff artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
bytes 209697
files 45
```

No production-byte change occurred during the documentation/governance reconciliation recorded below.

## Latest complete full regression gate

Codex result date: 2026-08-19  
Candidate/product-governance authority used by that campaign:

```text
07e0140d0a01a327d639e23bea8446a79818ceac
```

Complete result:

```text
PD-00..PD-17: ALL PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source/package identity: 45/45 PASS
real Yandex requests: 0
production modified during gate: NO
failures: NONE
verdict: PASS
```

Exact artifact accepted by that campaign is the `31cc5f…` artifact above.

## Documentation/governance reconciliation after the product PASS

After the complete product PASS, the following documentation/process corrections were made:

- `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` gained permanent QA transport/harness/gate-authoring failure-prevention rules;
- `WORKFLOW_OPERATING_RULES.md` was added and made effective immediately in the current conversation plus all future/resumed conversations;
- `README.md` gained mandatory workflow-transition reconstruction, authority precedence/conflict STOP rules and owner-correction canonicalization;
- `SPECIFICATION.md` was corrected to remove stale current wording and match the already-tested external Yandex action + Send→ready/Microphone Manual lifecycle;
- `ROADMAP.md` was synchronized from stale `3113…/4973…/358` checkpoints to current artifact `31cc…` and `361/361` full-gate PASS;
- `PHASE_1_0.1.1_LIVE_ACCEPTANCE.md` was updated to the exact `31cc…` artifact and reduced to irreducible owner real-profile checks;
- the old `PHASE_1_0.1.1_LIVE_TEST_PLAN_AND_RESULTS.md` is explicitly historical evidence, not current candidate/live-procedure authority.

### Classification of these post-gate documentation changes

Classification under `WORKFLOW_OPERATING_RULES.md`:

```text
PRODUCT_BYTES_CHANGED: NO
NEW_PRODUCT_BEHAVIOR_REQUIRED: NO
NEW_PRODUCT_ACCEPTANCE_ASSERTION_ADDED: NO
STALE_CURRENT_CONTRACT_TEXT_RECONCILED_TO_ALREADY-TESTED_BEHAVIOR: YES
QA/PROCESS FAILURE-PREVENTION RULES ADDED: YES
CURRENT/HISTORICAL AUTHORITY DISAMBIGUATED: YES
```

Therefore these changes are **process/governance clarification + stale-document reconciliation**, not a new product candidate.

The external Yandex action and Send→ready/Microphone assertions were already present in the living gate used for the successful `PD-00..PD-17` campaign. The reconciliation does not create an untested product requirement.

Accordingly, the exact complete product PASS for artifact `31cc5f…` remains applicable. Do **not** rerun the full product gate merely because of these documentation-only reconciliation commits.

If any later documentation change actually adds/changes a product contract or acceptance assertion, classify it again before handoff and refresh gate evidence as required.

## Owner live status

```text
Owner real-profile acceptance: PENDING
Issue #1: OPEN pending owner live acceptance
Issue #2: OPEN pending owner live acceptance
Phase 1 LIVE PASS: FALSE until owner acceptance
Search/Phase 2: BLOCKED until Phase 1 live PASS
```

Current owner-live authority:

```text
extension/docs/PHASE_1_0.1.1_LIVE_ACCEPTANCE.md
```

The owner-live step must use exact artifact SHA-256:

```text
31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
```

## Authorized next stage

```text
AUTHORIZED_NEXT_STAGE = OWNER_REAL_PROFILE_LIVE_ACCEPTANCE
```

Required behavior before starting that stage in the **current conversation or any later conversation**:

1. fetch live `main` HEAD;
2. read `README.md`, `WORKFLOW_OPERATING_RULES.md`, this file and `PHASE_1_0.1.1_LIVE_ACCEPTANCE.md`;
3. confirm no production bytes changed and no later contract/assertion change invalidated the classification above;
4. use only exact tested artifact `31cc5f…`;
5. perform only the irreducible owner-live checks; do not repeat controlled QA through the owner;
6. keep issues #1/#2 open and Search blocked until owner-live PASS.

Do not start Search. Do not close issues #1/#2 before owner real-profile PASS.
