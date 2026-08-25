# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH REPAIR FROZEN — INDEPENDENT CODEX COMPLETE PASS / OWNER LIVE AUTHORIZED + PENDING / PHASE 3 BLOCKED**  
Updated: 2026-08-25

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_THIS_STATE_WRITE = bc42cd446cd6b2a3ab303f6646eea2abc5d31aa4
PRODUCT_SOURCE = b7869180c229356a6b3d51ac980ec3da5df4c23c
PRODUCT_PARENT = f4aee34c0a3455aa7199f6aa54bd581c71d97337
HANDOFF_ARTIFACT = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa / 179013 bytes / 69 files / 72 ZIP entries
PAYLOAD_MANIFEST = ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1 / 12125 bytes
FREEZE_RUN = 32805530317 / job 97674800575 PASS
WINDOWS_SAFE_TRANSPORT = 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
WINDOWS_TRANSPORT_PROOF = run 32805811476 / job 97675604279 PASS
REPAIR_BROWSER_HARNESS = 81625e073d507d70451f1457185a3e906c640c66 / blob 790539464d7f72214a3126c6585aac74e1afec39
CURRENT_STAGE4_WRAPPER = 1babfe66222251e2eb63e6e0d4e3eb726ed898e9 / blob e1763df3cec988c3bee93efcdd6369eb8c12d695
CURRENT_STAGE4_PREFLIGHT = run 32809552231 / job 97686152475 PASS
INDEPENDENT_CODEX_CAMPAIGN_1 = FAIL_HARNESS / PRODUCT FAILURE NO
INDEPENDENT_CODEX_CAMPAIGN_2 = COMPLETE_RERUN_AFTER_STAGE4_HARNESS_RECONCILIATION / PASS
LATEST_FULL_GATE = PASS ON EXACT CE824A9F ARTIFACT
PRODUCTION_BYTES_CHANGED_SINCE_GATE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_GATE = NO
OWNER_LIVE = AUTHORIZED / PENDING
REAL_YANDEX_REQUESTS_DURING_CONTROLLED_QA = 0
OPEN_BLOCKERS = owner real-profile/live acceptance only
AUTHORIZED_NEXT_STAGE = OWNER_REAL_PROFILE_LIVE_ACCEPTANCE_EXACT_CE824A9F
```

## Frozen repaired product

The owner-visible real-profile context failure was repaired before this freeze. Historical factual evidence used the real conversation id:

```text
6a82924e-5ed0-83eb-84a2-851ddad40c88
```

The repaired source restores:

```text
- factual ChatGPT conversation-id acceptance without the invalid UUID version 1-5 restriction;
- trusted location + canonical identity resolution with fail-closed conflict handling;
- delivered-but-invalid WS_GET_IDENTITY treated as failure/recovery, not success;
- supported ChatGPT page availability separated from confirmed conversation identity so Bind can recover;
- Manual ON transaction order: page/content acknowledgement before worker authorization;
- Manual OFF safety order: worker OFF before page cleanup.
```

Clean repair source `b786918...` is exactly one commit above `f4aee34...` and changes four production files plus two package-test files.

Current exact artifact:

```text
yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes = 179013
files = 69
ZIP entries = 72
payload manifest SHA-256 = ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
payload manifest bytes = 12125
```

The older `739dd5d7...` artifact remains withdrawn and must not be used.

## Freeze and exact transport

ChatGPT-owned freeze/transport evidence:

```text
source suite = 244/244 PASS
packaged suite = 244/244 PASS
deterministic byte-identical rebuild = PASS
source syntax = 22/22 PASS
packaged syntax = 63/63 PASS
source JSON = 2/2 PASS
packaged JSON = 2/2 PASS
Windows exact B64 reassembly / manifest / ZIP integrity = PASS
real Yandex requests = 0
```

The exact Actions artifact was downloaded back and round-trip verified. The Windows-safe B64 transport at `9fb1fcf...` reassembled the same exact `ce824a9f...` bytes on Windows Server 2025 with `core.autocrlf=true`.

## Independent Codex campaign #1 — historical FAIL_HARNESS

The first independent campaign returned `FAIL_HARNESS` in the historical Stage-4 popup lifecycle. Frozen product bytes were not implicated. ChatGPT reconciled only the external QA popup lifecycle and preserved historical B-01/B-02/B-03 assertions.

Durable evidence:

```text
extension/tests/PHASE_2_REAL_PROFILE_BINDING_STAGE4_HARNESS_RECONCILIATION_2026-08-25.md
```

## Independent Codex campaign #2 — COMPLETE PASS

The owner returned the complete second independent Codex report for the same exact frozen artifact after Stage-4 harness reconciliation.

Campaign:

```text
COMPLETE_RERUN_AFTER_STAGE4_HARNESS_RECONCILIATION
```

Observed independent result:

```text
step_0_authority = PASS
transport = PASS
source_suite = 244/244
packaged_suite = 244/244
source_syntax = 22/22
packaged_syntax = 63/63
source_json = 2/2
packaged_json = 2/2
B01_project_work = PASS
B02_manual_on_transaction_browser = PASS
B03_search_autorun = PASS
PD-00..PD-17 = ALL PASS
manual_on_transaction = PASS
S-00..S-17 = ALL PASS
repair_real_id_late_install = PASS
repair_canonical_live_receiver = PASS
controlled_search_stub_requests = 1
real_yandex_requests = 0
real_credentials_used = NO
production_modified_during_gate = NO
package_tests_modified_during_gate = NO
historical_stage4_harness_modified_during_gate = NO
current_stage4_wrapper_modified_during_gate = NO
repair_browser_harness_modified_during_gate = NO
final_cleanliness = PASS
enabled_not_run_sections = 0
failures = []
verdict = PASS
```

Durable PASS checkpoint:

```text
extension/tests/PHASE_2_REAL_PROFILE_BINDING_CODEX_COMPLETE_PASS_2026-08-25.md
```

No product or package-test bytes changed after freeze, so no refreeze is required. The exact tested `ce824a9f...` artifact is now the only eligible owner-live handoff artifact.

## Owner real-profile/live acceptance

Per `WORKFLOW_OPERATING_RULES.md`, the complete independent PASS authorizes handoff of the exact tested artifact to the owner for irreducible real-profile acceptance.

Owner-live must use only:

```text
yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
```

The first owner-visible check is the repaired real-profile path itself:

```text
current ChatGPT is detected
→ Bind is available and succeeds
→ Manual mode can turn ON
→ the Bridge-owned Yandex action becomes usable in the bound conversation
```

Only after that real-profile path is visibly healthy may the owner perform the single irreducible paid synchronous Search acceptance, after a fresh official Search tariff check. No blind retry is allowed after an ambiguous provider initiation/outcome.

```text
OWNER_LIVE_SEARCH = AUTHORIZED / PENDING
PHASE_3_WEBMASTER = BLOCKED until Phase-2 owner-live closes
```

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = HAND_OFF_EXACT_CE824A9F_TO_OWNER_AND_RUN_REAL_PROFILE_ACCEPTANCE
OWNER_LIVE_SEARCH = AUTHORIZED / PENDING
PHASE_3_WEBMASTER = BLOCKED
```

Do not rebuild or substitute another ZIP. If owner-live exposes a defect, preserve the exact evidence, classify the failing layer and reopen Phase 2. Any product/package-test byte change creates a new candidate and restarts freeze/transport/independent-Codex gating.