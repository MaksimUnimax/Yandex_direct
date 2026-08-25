# Phase 2 real-profile binding repair — Stage-4 browser harness reconciliation

Status: **HARNESS RECONCILED / SAME FROZEN ARTIFACT / INDEPENDENT CODEX COMPLETE RERUN REQUIRED**  
Date: 2026-08-25

## 1. Independent Codex campaign result that triggered this reconciliation

The first independent Codex campaign on the exact repaired artifact returned:

```text
verdict = FAIL_HARNESS
candidate_source = b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact_sha256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
artifact_bytes = 179013
artifact_files = 69
artifact_zip_entries = 72
transport = PASS
source_suite = 244/244
packaged_suite = 244/244
source_syntax = 22/22
packaged_syntax = 63/63
source_json = 2/2
packaged_json = 2/2
repair_real_id_late_install = PASS
repair_canonical_live_receiver = PASS
real_yandex_requests = 0
real_credentials_used = NO
production_modified_during_gate = NO
package_tests_modified_during_gate = NO
repair_browser_harness_modified_during_gate = NO
```

The blocking failure was the historical Stage-4 Search/Manual/Autorun browser venue:

```text
gate = B-03 / PD-10 / S-11
classification = FAIL_HARNESS
error = TimeoutError: Waiting failed: 10000ms exceeded
evidence = browser_phase2_stage4_gate.mjs:109
```

The old harness opened `popup.html` as an inactive extension tab and immediately waited for `#conversationMeta`. That venue predates `popup_context_bootstrap.js` and did not preserve the repaired popup's active ChatGPT page-context contract. Codex correctly classified this as a harness failure; no frozen product bytes were implicated.

The propagated PD/S failures and final cleanliness FAIL from that campaign are not product verdicts. The campaign remains a complete independent `FAIL_HARNESS` and cannot be resumed piecemeal.

## 2. Frozen product remains unchanged

No product or package-test byte changed during reconciliation.

```text
PRODUCT_SOURCE = b7869180c229356a6b3d51ac980ec3da5df4c23c
ARTIFACT_SHA256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
ARTIFACT_BYTES = 179013
FILES = 69
ZIP_ENTRIES = 72
PAYLOAD_MANIFEST_SHA256 = ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
TRANSPORT_COMMIT = 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
```

Therefore **no refreeze is required or authorized**.

## 3. Historical assertion authority preserved

The original Stage-4 browser assertions remain authoritative and unchanged:

```text
HISTORICAL_STAGE4_COMMIT = 667fda2f9a0e4197c4873ea96f27862c8453f2f0
HARNESS_PATH = extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_gate.mjs
HARNESS_BLOB = 127e6042037ac0cbb044e81b2a9c554f24b5aa6b
TLS_KEY_BLOB = 2d0ab1f091b119d964a7ebdcd15720f6cd9728ad
TLS_CERT_BLOB = d91cb127e8d8f6cfa5a95723a15612fd03478af6
```

The compatibility repair does not edit that file. It wraps the historical harness and replaces only the obsolete `openPopup` / `closePopup` lifecycle functions in a temporary QA copy. B-01/B-02/B-03 assertions, provider stub, Manual assertions, Autorun assertions and result markers remain the historical body.

## 4. Current compatible wrapper authority

```text
branch = qa/phase2-current-stage4-browser-harness-b786918-2026-08-25
commit = 1babfe66222251e2eb63e6e0d4e3eb726ed898e9
product base = b7869180c229356a6b3d51ac980ec3da5df4c23c
path = extension/tests/qa_browser/phase2-stage4-current/run_current_stage4_gate.mjs
blob = e1763df3cec988c3bee93efcdd6369eb8c12d695
```

The branch delta relative to the frozen product is exactly that one QA file.

The reconciled popup lifecycle:

1. confirms the active owner ChatGPT tab and its exact identity before opening the test popup;
2. creates an inactive `about:blank` tab;
3. explicitly restores the owner ChatGPT tab as active before navigating the test tab to `popup.html`;
4. identifies the popup by exact `chrome.tabs.getCurrent()` tab id rather than a racy new-target event;
5. waits for the current `popup_context_bootstrap` outcome;
6. requires `attempted:true` and requires bootstrap `tab_id` to equal the owner ChatGPT tab id;
7. then requires the historical exact `conversationMeta` and normal `Готово.` state;
8. closes by tab id and waits until tab removal is confirmed.

Windows CRLF is normalized only in the temporary QA copy used to apply the function-level wrapper. The historical Git blob is independently pinned before execution. The temporary patched harness is deleted after execution.

## 5. ChatGPT-owned preflight of the reconciled harness

Preflight authority:

```text
run = 32809552231
job = 97686152475
OS = Windows Server 2025
Chrome for Testing = 151.0.7922.47
puppeteer-core = 25.4.0
artifact under test = exact ce824a9f... transported ZIP
result = PASS
```

Required observed markers:

```text
CURRENT_STAGE4_HARNESS_AUTHORITY_PASS
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
EXACT_CE824A9F_MATERIALIZED_PASS
HISTORICAL_STAGE4_ASSERTIONS_PRESERVED
CURRENT_STAGE4_POPUP_LIFECYCLE_PATCH_READY
CURRENT_POPUP_BOOTSTRAP_VENUE_PASS
B01_PROJECT_WORK_PASS
BROWSER_STEP_BIND_PASS
BROWSER_STEP_SEARCH_SETTINGS_PASS
BROWSER_STEP_MANUAL_FIRST_ON_PASS
BROWSER_STEP_NATIVE_COPY_PASS
B02_MANUAL_ON_TRANSACTION_PASS
BROWSER_STEP_AUTORUN_START_PASS
BROWSER_STEP_SEARCH_DELIVERY_PASS
B03_SEARCH_AUTORUN_PASS
BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1
BROWSER_GATE_REAL_YANDEX_REQUESTS=0
PHASE2_STAGE4_BROWSER_GATE_PASS
CURRENT_STAGE4_BROWSER_PREFLIGHT_PASS
CURRENT_STAGE4_PREFLIGHT_CLEAN_PASS
REAL_YANDEX_REQUESTS=0
```

This preflight proves the harness repair is executable against the exact artifact. It is **not** independent Codex evidence and does not authorize owner-live.

## 6. Required next transition

The first Codex campaign cannot be partially resumed. The independent Codex gate must restart from Step 0 / PD-00 against the same exact artifact, using the current wrapper for the Stage-4 B-01/B-02/B-03 browser venue and the already-pinned repair-specific browser harness for the factual real-id/canonical cases.

```text
AUTHORIZED_NEXT_STAGE = INDEPENDENT_CODEX_COMPLETE_RERUN_SAME_EXACT_CE824A9F
OWNER_LIVE_SEARCH = BLOCKED
PHASE_3_WEBMASTER = BLOCKED
```

Any production or package-test byte change would invalidate this reconciliation and require a new freeze. No such change has occurred.