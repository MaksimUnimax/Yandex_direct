# Phase 5 Direct — final integration and closure plan

Date: 2026-08-27

Status: **PREPARED / OWNER-LIVE PENDING / NO MERGE AUTHORIZED YET**

This document prepares the exact sequence after Yandex approves production Direct API access. It does not grant owner-live PASS, does not close Phase 5, and does not authorize a merge before the live boundary succeeds.

## 1. Immutable accepted candidate authority

```text
live main before Phase 5 product integration = c2d5c59dc922ca82da55643cf94d7656339135b9
accepted Phase 5 source = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
accepted extension/src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
candidate branch = candidate/phase5-direct-first-slice-r2-2026-08-27
freeze run = 33037955943
freeze artifact id = 9632728199
artifact name = phase5-direct-r2-frozen-candidate-841a1e2
inner ZIP = yandex-marketing-bridge-0.1.1-phase5-direct-first-slice-r2-candidate.zip
ZIP SHA-256 = ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
ZIP bytes = 406656
ZIP files = 39
independent Codex complete gate = PASS
independent campaign = PHASE5_DIRECT_R2_COMPLETE_APPLICABLE_GATE_RERUN2
runner final marker = PHASE5_DIRECT_R2_INDEPENDENT_RUNNER_PASS
D-00..D-22 = PASS
NOT_RUN_COUNT = 0
PRODUCT_BYTES_POST_TEST = IDENTICAL
```

The candidate bytes are immutable. Any product-byte change before final integration invalidates this authority and requires a new candidate/freeze/independent campaign.

## 2. Current merge relationship already verified

At preparation time the accepted source is a clean descendant of the current `main`:

```text
base main = c2d5c59dc922ca82da55643cf94d7656339135b9
head = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
ahead = 54
behind = 0
merge base = c2d5c59dc922ca82da55643cf94d7656339135b9
```

This relationship MUST be re-fetched immediately before integration. Do not assume it remains true merely because this preparation check passed.

## 3. Hard gate before integration

No integration branch or PR may be treated as final until all of the following are true:

```text
[ ] Yandex Direct application production/full API access is approved
[ ] exact frozen ZIP above is loaded by owner
[ ] dedicated Direct OAuth token is used locally; no token is recorded in evidence
[ ] Direct Check exactly once = PASS
[ ] listCampaigns exactly once = PASS
[ ] listAdGroups = PASS or NOT_APPLICABLE_EMPTY_ACCOUNT
[ ] getCampaignPerformance = PASS or NOT_APPLICABLE_NO_REAL_DATA
[ ] no write/mutation request executed
[ ] no blind retry after provider initiation
[ ] owner-live evidence recorded as extension/tests/PHASE5_DIRECT_OWNER_LIVE_PASS_2026-08-27.md
```

If owner-live returns a product defect, STOP. Do not merge. Any product fix causes a new candidate/freeze/independent campaign.

## 4. Integration strategy

Do **not** merge the current independent-Codex QA branch wholesale into `main`.

The QA branch intentionally contains historical handoffs, superseded harness material and temporary preflight workflows. Final integration should be narrow and auditable.

### 4.1 Product/development source

The product/development authority is the accepted source commit:

```text
841a1e2c1a503c4a05572a957ba97c55b9b60c52
```

If live `main` is still exactly `c2d5c59...` and the accepted source remains `ahead / behind 0`, integration may use the accepted candidate lineage directly through a normal PR/merge.

If `main` has moved, create a fresh final integration branch from the new exact `main` and apply the accepted Phase-5 product/development delta without changing `extension/src`. Before opening/merging the PR require:

```text
git tree for extension/src = edf1c2d3494ebbc53ae778d23be1457eb885b605
no product blob differs from source 841a1e2...
```

No conflict resolution is allowed to silently alter product bytes. A real product-byte conflict requires stopping and requalification.

### 4.2 Permanent QA/evidence to carry into main

Carry these Phase-5 QA assets because they are required for durable verification or final acceptance history:

```text
extension/tests/credential_runtime_concurrency.test.mjs
extension/tests/direct_phase5_contract_closure.test.mjs
extension/tests/direct_phase5_selector_matrix.test.mjs
extension/tests/direct_phase5_ui_runtime_contract.test.mjs
extension/tests/phase5_prior_service_compatibility.test.mjs
extension/tests/helpers/phase5_runtime_harness.mjs
extension/tests/qa_browser/direct_browser_runtime.mjs
extension/tests/qa_browser/direct_manual_worker_lifecycle.mjs
extension/tests/qa_browser/direct_popup_d18.mjs
extension/tests/qa_browser/direct_codex_gate_addendum_v2.mjs
extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_compat_gate.mjs
extension/tests/qa_phase5_codex/direct_addendum_coverage.test.mjs
extension/tests/qa_phase5_codex/phase5_direct_r2_complete_gate_runner.py
extension/tests/qa_phase5_codex/phase5_direct_r2_complete_gate_runner_v2.py
extension/tests/PHASE5_DIRECT_R2_FROZEN_CANDIDATE_CHECKPOINT_2026-08-27.md
extension/tests/PHASE5_DIRECT_R2_CODEX_ATTEMPT1_FAIL_HARNESS_2026-08-27.md
extension/tests/PHASE5_DIRECT_R2_CODEX_ATTEMPT2_FAIL_HARNESS_2026-08-27.md
extension/tests/PHASE5_DIRECT_R2_CODEX_COMPLETE_PASS_2026-08-27.md
extension/tests/PHASE5_DIRECT_OWNER_LIVE_CHECKLIST_2026-08-27.md
extension/tests/PHASE5_DIRECT_OWNER_LIVE_PASS_2026-08-27.md
.github/workflows/phase5-direct-postmerge-final.yml
```

The first group already belongs to the accepted product/development lineage where applicable; the second group comes from the final QA/evidence lineage.

### 4.3 QA-only history that should remain off final main

Do not carry the following merely because they exist on the QA branch:

```text
extension/tests/qa_browser/direct_codex_gate_addendum.mjs
extension/tests/CODEX_PHASE5_DIRECT_R2_COMPLETE_GATE_HANDOFF_2026-08-27.md
extension/tests/CODEX_PHASE5_DIRECT_R2_COMPLETE_GATE_RERUN_HANDOFF_2026-08-27.md
extension/tests/CODEX_PHASE5_DIRECT_R2_COMPLETE_GATE_RERUN2_HANDOFF_2026-08-27.md
.github/workflows/phase5-direct-codex-harness-r2.yml
.github/workflows/phase5-direct-frozen-r2-gate.yml
.github/workflows/phase5-direct-independent-codex-runner-preflight.yml
.github/workflows/phase5-direct-independent-runner-v2-crossplatform.yml
```

These remain available in Git history/QA branch as traceable campaign evidence. `direct_codex_gate_addendum.mjs` is superseded by `direct_codex_gate_addendum_v2.mjs` and must not become the final governed browser authority.

The development workflows that are part of source commit `841a1e2...` may remain in the integrated history; they do not define production runtime behavior.

## 5. Final integration PR acceptance checks

Immediately before merge, verify:

```text
live main HEAD = freshly fetched
integration branch base = that exact live main HEAD
extension/src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
extension/src diff versus 841a1e2... = empty
owner-live PASS record exists and contains no secret
independent Codex PASS record exists
post-merge workflow file exists
no superseded direct_codex_gate_addendum.mjs introduced by the integration-only QA selection
```

The PR must not be merged if any product blob differs from the frozen accepted product.

## 6. Post-merge final gate

After the product/evidence integration lands on `main`, run exactly:

```text
.github/workflows/phase5-direct-postmerge-final.yml
```

using `workflow_dispatch` on `main`.

The workflow requires:

```text
main only
HEAD:extension/src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
extension/src diff versus 841a1e2... = empty
owner-live PASS evidence present
exact frozen artifact downloaded from run 33037955943
source suite = 34/34
packaged suite = 34/34
source syntax = 33/33
packaged syntax = 33/33
source JSON = 2/2
packaged JSON = 2/2
credential concurrency regression = PASS
all four installed-browser gates = PASS
D-00..D-22 = PASS
real credentials used = NO
real Yandex requests = 0
NOT_RUN_COUNT = 0
PRODUCT_BYTES_POST_TEST = IDENTICAL
PHASE5_DIRECT_POSTMERGE_FINAL_PASS
```

This gate is controlled QA only. It must not use the owner token and must not contact real Yandex endpoints.

## 7. Closure document update only after post-merge PASS

Only after the post-merge gate succeeds, create a docs-only closure commit updating `extension/docs/CURRENT_STATE.md` and `extension/docs/ROADMAP.md`.

The closure record must contain at minimum:

```text
ACCEPTED_PHASE5_SOURCE = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
ACCEPTED_PHASE5_SRC_TREE = edf1c2d3494ebbc53ae778d23be1457eb885b605
ACCEPTED_PHASE5_ZIP_SHA256 = ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
ACCEPTED_PHASE5_ZIP_BYTES = 406656
ACCEPTED_PHASE5_FREEZE_RUN = 33037955943
ACCEPTED_PHASE5_FREEZE_ARTIFACT_ID = 9632728199
ACCEPTED_PHASE5_CODEX_FINAL = PASS
ACCEPTED_PHASE5_OWNER_LIVE = PASS
ACCEPTED_PHASE5_MAIN_MERGE = <actual merge SHA>
ACCEPTED_PHASE5_POSTMERGE_RUN = <actual workflow run>
ACCEPTED_PHASE5_POSTMERGE = PASS
PHASE5_STATUS = LIVE PASS / CLOSED
```

`ROADMAP.md` must move Phase 5 from implementation/pending-live language to `LIVE PASS / CLOSED` and retain all deferred Direct write/bid/finance/offline surfaces as locked.

## 8. First product-cycle closure

`PROJECT_PURPOSE.md` currently defines the planned first service set as:

```text
Wordstat
Search / SERP
Webmaster
Metrika
Direct
```

After Phase 5 is `LIVE PASS / CLOSED`, that five-service implementation cycle is complete.

This does **not** mean the repository is finished forever. It means there is no sixth provider service already authorized by the current purpose/roadmap. Any next product stage must be explicitly reconstructed and authorized as a new roadmap decision rather than silently appended to Phase 5.

The final closure checkpoint should therefore state:

```text
PHASE_1_WORDSTAT = CLOSED
PHASE_2_SEARCH = CLOSED
LIFECYCLE_PATCH = CLOSED
PHASE_3_WEBMASTER = CLOSED
PHASE_4_METRIKA = CLOSED
PHASE_5_DIRECT = CLOSED
FIRST_PLANNED_FIVE_SERVICE_CYCLE = COMPLETE
AUTHORIZED_NEXT_STAGE = PRODUCT_RELEASE_DOCUMENTATION_OR_NEW_EXPLICIT_ROADMAP_DECISION
```

## 9. Current boundary while Yandex reviews the application

At the time of this plan:

```text
Direct production API application = submitted / pending provider approval
owner-live = NOT RUN
main product integration = BLOCKED
Phase 5 closure = BLOCKED
```

No user action is required for repository preparation. The next owner action is only when Yandex changes the Direct application access state to approved/full production access.
