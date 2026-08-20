# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY / PHASE 2 STAGE 3 REOPENED — BLOCKED ON EXACT STAGE-2 BASE RECOVERY**  
Updated: 2026-08-20

Always fetch live `main` HEAD before any control-plane write.

## Repository

```text
repo: MaksimUnimax/Yandex_direct
control branch: main
Phase-2 development branch: dev/phase2-search-foundation-2026-08-19
current dev HEAD after latest evidence write: 2f5a32beba05dd7856d100509f20479d7c9114ce
```

## Mandatory workflow authorities

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
extension/docs/PHASE_2_FOUR_STAGE_EXECUTION_CONTROL.md
extension/docs/PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
```

Work continuously inside each four-stage boundary without micro-step chatter. At each stage PASS: preserve exact product/test/evidence in GitHub, update this file, report once to owner, then continue automatically unless owner action, Codex action, or a real blocker is required.

Unknown current browser/DOM/runtime facts MUST NOT be guessed. Exact artifact bytes/transport MUST NOT be guessed. GitHub write/upload success is not proof of exact consumer delivery.

## Phase 1 accepted authority

```text
artifact SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes: 209505
files: 45
ZIP entries: 48
version: 0.1.1
content_script.js: ddf9ed51c60ab90dcdeb1fcd5a1b955c3dd88dfc53a0ddfd5842d66ebe9a02cc
popup.js: ac87ad973e8b673bf0c235a43b3dc29dfb67865594ea62e085f943660f0a7ab2
service_worker.js: 2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

Latest complete Codex full gate remains exact Phase-1 e13a PASS: PD-00..PD-17 ALL PASS; source 361/361; packaged 361/361; syntax 40/40; JSON 2/2; source/package identity PASS; real Yandex requests 0. Owner real-profile Wordstat acceptance PASS for all four supported operations. Phase 1 is LIVE PASS / CLOSED.

## Phase 2 first Search slice

```text
protocol: SEARCH_API_V1
service: search
method: search
mode: synchronous text web search
endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
response format: FORMAT_XML
result signature: SEARCH_RESULT_V1
```

Outside first slice: async/polling, image search, generative search, HTML normalization, yandex.ru scraping.

## Four-stage execution status

### STAGE 1 — exact base + Search foundation

```text
STATUS = PASS / COMPLETED (historical accepted checkpoint)
base e13a: 45/45 exact
Stage-1 target files: 50
target manifest SHA-256: 62bd5846c8f7d6ade7f788d4394d79e02e802611144a4249761ccbb07397b98b
recorded focused: 32/32 PASS
recorded affected: 86/86 PASS
recorded full suite: 393/393 PASS
recorded syntax/JSON: PASS
recorded real Yandex requests: 0
```

Durable Stage-1 transport/evidence:

```text
extension/tests/phase2/search-foundation/FOUNDATION_EVIDENCE_2026-08-19.json
extension/tests/phase2/search-foundation/target-tree-sha256.tsv
extension/tests/phase2/search-foundation/phase2-search-foundation.patch.gz.b64
```

Stage-1 raw patch authority remains:

```text
raw patch SHA-256: 830e2ccba23a44bbaabb304f05e6c69a511b501c70d64963e8409a85bffd5f02
raw patch bytes: 41531
gzip SHA-256: d75da4c5619d6d0561616aba4c1cfbf733729bdd3e50ece058881f292fc713d5
base64 SHA-256: 0ad464225700a7179a815caa3f1cfd2ba63dfc8ca167c7ffbf9efb938297d578
```

Latest Codex materialization attempt independently re-established those Stage-1 patch identities but reported `git apply --check` failure. It then compared the still-unapplied e13a tree to the Stage-1 target and obtained exactly:

```text
42 matched
3 mismatched
5 missing
0 extras
```

This shape equals the recorded Stage-1 delta over the 45-file base: three existing files changed and five new files added. Therefore the Stage-1 patch is NOT classified corrupt from this result. Exact failing `git apply --check` diagnostics and working-directory/root assumptions were not returned. Current classification is `PROMPT/EXECUTION INSTRUCTION SUSPECTED`, not product defect.

### STAGE 2 — worker/provider/credential/policy execution

```text
STATUS = PASS / COMPLETED (historical accepted checkpoint)
target files: 51
target manifest SHA-256: a274600440461cc7ac4669e959d3b84ee6dfaa9dffb26219ee7e1dd0086f8236
recorded fresh apply identity: 51/51 PASS
recorded focused Search Stage 2: 10/10 PASS
recorded full suite: 377/377 PASS
recorded syntax: 46/46 PASS
recorded JSON: 2/2 PASS
recorded real Yandex requests: 0
```

Stage-2 product change identities recorded by accepted evidence:

```text
service_worker.js def73ebb44243b57d0be98ad21fec6ccf230cc2dfe1b29f8ee3588e17fe80282 / 190920
shared/credential_registry.js 506aafca071522c7dc110dd72feec4d7fbee36119849abac69158c9be232a311 / 1413
shared/policy_model.js c97c2b8dd600091f894d2c7c5c0fb91a6408d5cc848bc579ec3acc6cb59d99bf / 6086
tests/search_worker_stage2.test.mjs 1dcb99a40477846ffb93181ea0589fac194fca9f294b614990edc8a3f9cf0a3a / 13682
```

Durable Stage-2 evidence/manifest:

```text
extension/tests/phase2/search-worker-provider/STAGE2_EVIDENCE_2026-08-20.json
extension/tests/phase2/search-worker-provider/target-tree-sha256.tsv
```

The file currently published as:

```text
extension/tests/phase2/search-worker-provider/phase2-stage2-worker-provider.patch.gz.b64
```

is now independently proven NOT to reproduce the recorded Stage-2 gzip identity. Latest Codex result:

```text
Base64 decoded bytes: 8006
actual decoded SHA-256: 2ac4758d1fb0dec1a0cca144c19c6eb74c1d24634aa13b0024170bbc5b1afc05
expected gzip SHA-256: 4f9bac5de1e658c40e14305d9dbe6fca17b58718a562e6e546e26328a8285a54
gzip CRC/integrity: FAIL
raw Stage-2 patch: NOT SAFELY MATERIALIZED
```

Classification:

```text
failure layer = ARTIFACT / TRANSPORT
product defect = NOT ESTABLISHED
accepted Stage-2 behavioral evidence remains historical evidence
published Stage-2 patch transport is not currently usable as byte authority
```

Do NOT overwrite the corrupt historical transport file to make history look clean. Any recovered exact Stage-2 patch/component must be preserved as a new correction/recovery transport with its own evidence.

### STAGE 3 — Manual/Autorun/operator/delivery integration

```text
STATUS = REOPENED / BLOCKED BEFORE PRODUCT WRITE
REASON 1 = old Stage-3 exact bytes were not durable and exact recovery failed
REASON 2 = exact Stage-2 editable base cannot yet be reconstructed because the durable Stage-2 patch transport is corrupt
```

The old local Stage-3 verification/hashes remain historical behavioral evidence only and are not current editable byte authority.

Durable recovery/materialization evidence:

```text
extension/tests/phase2/search-runtime-integration/STAGE3_EXACT_RECOVERY_RESULT_V1_2026-08-20.json
extension/tests/phase2/search-runtime-integration/STAGE4_TRANSPORT_BLOCKER_2026-08-20.md
extension/tests/phase2/search-runtime-integration/STAGE3_REIMPLEMENTATION_BASE_MATERIALIZATION_BLOCKER_2026-08-20.md
extension/tests/phase2/search-runtime-integration/STAGE2_EXACT_MATERIALIZATION_RESULT_V1_2026-08-20.json
```

Next recovery must remain QA/measurement/artifact-only. No Stage-3 product/test implementation is authorized until exact Stage-2 target is established 51/51.

### STAGE 4 — frozen candidate / exact transport / Codex / owner live

```text
STATUS = PENDING REOPENED STAGE-3 DURABLE PASS
```

Not authorized:

```text
freeze combined Phase-2 candidate
build/declare final ZIP identity
issue Phase-2 Codex full-gate prompt
owner real-profile Search request
```

## Authorized narrow recovery action

Codex may perform only the following independent measurement/recovery work, with zero product/test edits and zero real Yandex requests:

1. rerun the exact Stage-1 patch from the exact e13a extracted ROOT directory, explicitly capture current working directory, patch path headers and complete `git apply --check` diagnostics; if the prior failure was only wrong invocation/root, prove Stage-1 target 50/50 exact;
2. search available Codex workspaces/artifact directories for the exact Stage-2 raw patch SHA `6b9c7f55...`, exact gzip SHA `4f9bac5d...`, or exact Stage-2 changed-file bytes listed above;
3. if exact Stage-2 changed files are found, construct a fresh Stage-2 target only by replacing the known Stage-2 delta over a verified 50/50 Stage-1 tree, then require full canonical Stage-2 manifest 51/51;
4. publish only after exact 51/51 target is proven and perform fresh remote consumer verification.

No logically equivalent reimplementation may substitute for exact recovery in this step.

## Current control-plane reconstruction

```text
LIVE_HEAD = fetch live main before every control-plane write
PRODUCT_SOURCE = exact accepted Stage-2 identity is recorded but byte-complete editable target not yet recovered
HANDOFF_ARTIFACT = NONE
LATEST_FULL_GATE = Phase-1 exact e13a PASS only; Phase-2 combined gate pending
PRODUCTION_BYTES_CHANGED_SINCE_GATE = YES
OWNER_LIVE = Phase 1 PASS; Phase 2 PENDING
OPEN_BLOCKERS = Stage-1 apply invocation diagnostics + exact Stage-2 transport/component recovery
AUTHORIZED_NEXT_ACTION = CODEX_STAGE1_APPLY_DIAGNOSTIC_AND_STAGE2_EXACT_COMPONENT_RECOVERY
CODEX_MEASUREMENT_PENDING = YES
OWNER_ACTION_PENDING = paste the supplied narrow Codex recovery prompt only
```

## Phase status

```text
PHASE 0 = PASS
PHASE 1 WORDSTAT = LIVE PASS / CLOSED
PHASE 2 SEARCH = ACTIVE / STAGE 1 HISTORICAL PASS / STAGE 2 HISTORICAL PASS / STAGE 3 REOPENED BLOCKED ON EXACT STAGE-2 BASE RECOVERY / STAGE 4 PENDING
PHASE 3 WEBMASTER = BLOCKED
PHASE 4 METRIKA = BLOCKED
PHASE 5 DIRECT READ = BLOCKED
PHASE 6 DIRECT DRAFT/PRE-LIVE WRITE = BLOCKED
PHASE 7 DIRECT LIVE WRITE = BLOCKED
PHASE 8 FULL ORDER E2E = BLOCKED
```
