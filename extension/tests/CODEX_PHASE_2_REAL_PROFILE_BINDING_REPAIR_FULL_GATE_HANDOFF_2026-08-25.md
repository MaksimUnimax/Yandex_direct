# Codex handoff — Phase 2 real-profile binding repair complete pre-delivery gate

Status: **READY FOR INDEPENDENT CODEX EXECUTION / OWNER LIVE BLOCKED**  
Date: 2026-08-25

This is an execution handoff, not permission to change the product. Codex is the independent QA executor. ChatGPT remains the product/test/harness owner.

## 0. Non-negotiable role and safety boundary

Codex MUST NOT:

- edit production code;
- edit package tests;
- edit the pinned browser harness;
- weaken, skip or reinterpret an assertion to obtain PASS;
- substitute a rebuilt/logically-equivalent package for the exact frozen package under test;
- use real Yandex credentials;
- make any real Yandex provider request;
- ask the owner to transport, download, extract or repair QA files;
- repair an artifact/harness/product failure itself.

If a failure occurs, classify the failing layer and report it to ChatGPT. Product/test/harness bytes must remain unchanged during this campaign.

## 1. Exact authority

```text
PRODUCT_BRANCH = candidate/phase2-real-profile-binding-repair-2026-08-25
PRODUCT_SOURCE = b7869180c229356a6b3d51ac980ec3da5df4c23c
PRODUCT_PARENT = f4aee34c0a3455aa7199f6aa54bd581c71d97337

TRANSPORT_BRANCH = qa/phase2-real-profile-binding-final-b64-transport-b786918-2026-08-25
TRANSPORT_COMMIT = 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
TRANSPORT_DIR = extension/tests/qa_transport/phase2-real-profile-binding-final-b64

ARTIFACT_FILENAME = yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
ARTIFACT_SHA256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
ARTIFACT_BYTES = 179013
FILES = 69
ZIP_ENTRIES = 72

PAYLOAD_MANIFEST = EXACT_REAL_PROFILE_BINDING_REPAIR_CANDIDATE_MANIFEST_2026-08-25.json
PAYLOAD_MANIFEST_SHA256 = ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
PAYLOAD_MANIFEST_BYTES = 12125
PACKAGE_ROOT_NAME = yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate

REPAIR_BROWSER_HARNESS_BRANCH = qa/phase2-real-profile-binding-browser-harness-b786918-2026-08-25
REPAIR_BROWSER_HARNESS_COMMIT = 81625e073d507d70451f1457185a3e906c640c66
REPAIR_BROWSER_HARNESS_PATH = extension/tests/qa_browser/real_profile_binding_gate.mjs
REPAIR_BROWSER_HARNESS_BLOB = 790539464d7f72214a3126c6585aac74e1afec39
```

Historical artifact `739dd5d7...` is withdrawn and MUST NOT be tested or used for owner handoff.

## 2. Governing gate documents

Execute the complete currently enabled requirements from:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
extension/tests/PHASE_2_REAL_PROFILE_BINDING_REPAIR_FREEZE_TRANSPORT_CHECKPOINT_2026-08-25.md
```

All enabled `PD-00..PD-17` and `S-00..S-17` sections must receive explicit results. No enabled `NOT_RUN` may appear in a PASS campaign.

## 3. Step 0 — reconstruct live authority before testing

Use a fresh workspace. Fetch live repository refs first. Record:

```text
LIVE_MAIN_HEAD
PRODUCT_SOURCE
HANDOFF_ARTIFACT
LATEST_COMPLETE_INDEPENDENT_CODEX_GATE
PRODUCTION_BYTES_CHANGED_SINCE_FREEZE
OWNER_LIVE
OPEN_BLOCKERS
AUTHORIZED_NEXT_STAGE
```

Required precondition at campaign start:

```text
PRODUCT_SOURCE == b7869180c229356a6b3d51ac980ec3da5df4c23c
HANDOFF_ARTIFACT == ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa / 179013 bytes / 69 files / 72 entries
PRODUCTION_BYTES_CHANGED_SINCE_FREEZE == NO
OWNER_LIVE == BLOCKED
AUTHORIZED_NEXT_STAGE == INDEPENDENT_CODEX_FULL_GATE_EXACT_CE824A9F
```

Also verify `PRODUCT_PARENT..PRODUCT_SOURCE` is exactly one commit with exactly these six changed files:

```text
extension/src/content_script.js
extension/src/popup.js
extension/src/popup_context_bootstrap.js
extension/src/shared/conversation_identity.js
extension/tests/popup_phase2_runtime.test.mjs
extension/tests/real_profile_binding_regression.test.mjs
```

If authority differs, stop and return `FAIL_ARTIFACT`/`FAIL_HARNESS` as appropriate. Do not guess and do not patch.

## 4. Exact artifact acquisition — use published B64 transport only

Check out the exact `TRANSPORT_COMMIT` in a fresh transport workspace. Verify:

```text
git rev-parse HEAD == 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
git rev-parse HEAD^ == b7869180c229356a6b3d51ac980ec3da5df4c23c
```

The commit delta must be exactly the five files in `TRANSPORT_DIR` and no others.

Run:

```text
python extension/tests/qa_transport/phase2-real-profile-binding-final-b64/verify_exact_b64_transport.py
```

Required output:

```text
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
REAL_YANDEX_REQUESTS=0
```

Then persist the exact decoded ZIP in a fresh QA output directory using only `artifact.b64` and `TRANSPORT_MANIFEST_2026-08-25.json`. Recalculate and require:

```text
SHA-256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes = 179013
ZIP integrity = PASS
files = 69
ZIP entries = 72
```

Do not regenerate the package as a substitute for the transported ZIP. A deterministic rebuild may be performed only as additional PD-03 reproducibility evidence.

If any identity fails: `FAIL_ARTIFACT`, stop product testing, make zero product/test edits.

## 5. Fresh extraction and payload identity

Fresh-extract the exact transported ZIP. The package root directory name from the payload manifest is:

```text
yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate
```

Verify every extracted payload path/byte count/SHA-256 against the exact payload manifest. Any mismatch is `FAIL_ARTIFACT`.

## 6. Exact source and packaged regression suites

In a separate clean source workspace at exact `PRODUCT_SOURCE`, run the complete source suite:

```text
cd extension/src
npm test
```

Expected current count:

```text
244/244 PASS
```

Run syntax/JSON checks required by the canonical gate. Current frozen preflight established:

```text
source JS syntax = 22/22 PASS
source JSON = 2/2 PASS
```

Against the fresh extraction of the exact artifact, run the complete packaged suite using the canonical package-suite adapter from the exact product source. Current frozen preflight established:

```text
packaged tests = 244/244 PASS
packaged JS syntax = 63/63 PASS
packaged JSON = 2/2 PASS
```

Codex must report actual observed counts. The expected counts above are not permission to suppress a discrepancy.

## 7. Complete canonical browser/integration matrix

Execute every enabled browser/integration requirement from the permanent gate and both current addenda. This includes the existing Phase-2 Search controlled browser scenarios and the Manual-ON transaction regression. Keep all provider activity stubbed/intercepted. Real Yandex request count must remain zero.

The canonical result must explicitly cover:

```text
PD-00..PD-17 = each PASS
Manual-ON transaction = PASS
S-00..S-17 = each PASS
```

Search protocol, validation, credential/policy pre-network rejection, exact-one controlled provider initiation, cost ledger, Base64/XML normalization, Manual, Autorun, service isolation, HTTP no-retry, UNKNOWN/no-blind-retry and future-feature locks must remain covered exactly as governed by the gate documents.

## 8. Mandatory repair-specific Chrome regression

This new repair changes browser-owned identity/binding/Manual behavior, so the independent campaign MUST additionally execute the pinned external harness. Do not copy it into or modify the frozen package.

In a separate clean harness workspace:

```text
git checkout 81625e073d507d70451f1457185a3e906c640c66
git rev-parse HEAD^ == b7869180c229356a6b3d51ac980ec3da5df4c23c
git rev-parse 81625e073d507d70451f1457185a3e906c640c66:extension/tests/qa_browser/real_profile_binding_gate.mjs == 790539464d7f72214a3126c6585aac74e1afec39
```

The diff from product source must be exactly one file: `extension/tests/qa_browser/real_profile_binding_gate.mjs`.

Qualified environment:

```text
Chrome for Testing = 151.0.7922.47
puppeteer-core = 25.4.0
```

Install only the browser QA dependency in the harness workspace, not inside the extracted extension package:

```text
npm install --no-save --package-lock=false puppeteer-core@25.4.0
```

Run:

```text
node extension/tests/qa_browser/real_profile_binding_gate.mjs <CHROME_151_EXECUTABLE> <FRESH_EXTRACTED_PACKAGE_ROOT>
```

Required repair-specific assertions:

1. factual direct conversation URL `https://chatgpt.com/c/6a82924e-5ed0-83eb-84a2-851ddad40c88` is confirmed even though its UUID version nibble is outside the reconstructed `[1-5]` filter;
2. late extension installation into an already-open ChatGPT direct conversation self-recovers identity;
3. Project/root visible URL can use the trusted canonical direct-conversation URL when the content receiver is already live;
4. popup resolves exact key `https://chatgpt.com|6a82924e-5ed0-83eb-84a2-851ddad40c88`;
5. Bind is enabled and succeeds;
6. Manual is enabled and Manual ON succeeds only after page acknowledgement;
7. exactly one Bridge-owned external Yandex action appears in the controlled assistant block;
8. the visible ChatGPT page/DOM remains stable;
9. real Yandex requests = 0.

Required final marker:

```text
REAL_PROFILE_BINDING_BROWSER_GATE_PASS
REAL_YANDEX_REQUESTS=0
```

Any harness execution/environment failure on an otherwise exact package is `FAIL_HARNESS`, not `FAIL_ARTIFACT`. Any product assertion failure on the exact package is `FAIL_PRODUCT`.

## 9. Cleanliness and mutation audit

Before final verdict, prove:

```text
real credentials used = NO
real Yandex requests = 0
production modified during gate = NO
package tests modified during gate = NO
repair browser harness modified during gate = NO
exact artifact bytes modified = NO
final source workspace clean = PASS
final harness workspace clean = PASS
no enabled NOT_RUN sections = PASS
```

## 10. Required final report

Return one complete machine-readable/plain-text report headed exactly:

```text
CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT
```

It must include at least:

```text
candidate_source: b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact_sha256: ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
artifact_bytes: 179013
artifact_files: 69
artifact_zip_entries: 72
payload_manifest_sha256: ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
payload_manifest_bytes: 12125
transport_commit: 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
repair_browser_harness_commit: 81625e073d507d70451f1457185a3e906c640c66
repair_browser_harness_blob: 790539464d7f72214a3126c6585aac74e1afec39
step_0_authority: PASS|FAIL
transport: PASS|FAIL
source_suite: <actual pass>/<actual total>
packaged_suite: <actual pass>/<actual total>
source_syntax: <actual pass>/<actual total>
packaged_syntax: <actual pass>/<actual total>
source_json: <actual pass>/<actual total>
packaged_json: <actual pass>/<actual total>
PD-00: PASS|FAIL|NOT_RUN
...
PD-17: PASS|FAIL|NOT_RUN
manual_on_transaction: PASS|FAIL|NOT_RUN
S-00: PASS|FAIL|NOT_RUN
...
S-17: PASS|FAIL|NOT_RUN
repair_real_id_late_install: PASS|FAIL|NOT_RUN
repair_canonical_live_receiver: PASS|FAIL|NOT_RUN
controlled_search_stub_requests: <integer>
real_yandex_requests: 0
real_credentials_used: NO
production_modified_during_gate: NO
package_tests_modified_during_gate: NO
repair_browser_harness_modified_during_gate: NO
final_cleanliness: PASS|FAIL
enabled_not_run_sections: <integer>
failures: [] | [exact failures]
verdict: PASS|FAIL_PRODUCT|FAIL_ARTIFACT|FAIL_HARNESS
```

`PASS` is valid only if every enabled section passed, both repair browser scenarios passed, failures are empty, no relevant bytes were modified, no real credentials were used, and real Yandex requests remained zero.

On any non-PASS verdict, return the exact evidence and stop. Do not patch anything.
