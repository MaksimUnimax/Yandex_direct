# Codex final handoff — Phase 2 Search Stage 4 complete pre-delivery gate

Date: 2026-08-24  
Status: **AUTHORIZED FOR ONE COMPLETE QA CAMPAIGN / DO NOT PATCH PRODUCT OR TESTS**

## Role

You are the QA executor, not the developer. Execute the complete governed gate against the exact frozen candidate below. Do not design fixes, edit production code, edit package tests, weaken assertions, substitute another candidate, or use real Yandex credentials/requests.

If an assertion fails, classify it and continue unrelated safe sections when possible so the final report contains the complete failure set. A mandatory enabled `NOT_RUN` forbids PASS.

Allowed final verdicts only:

```text
PASS
FAIL_PRODUCT
FAIL_ARTIFACT
FAIL_HARNESS
```

## Repository

```text
MaksimUnimax/Yandex_direct
```

## Exact frozen authority

```text
source commit:
0ee1d38f8d28cfccceb5a07f9606fa715261bc27

artifact filename:
yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip

artifact SHA-256:
d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16

artifact bytes: 170734
files: 65
ZIP entries: 68

payload manifest SHA-256:
0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
payload manifest bytes: 11421
```

Do not use the superseded `1869d17... / 0f0b035c...` candidate.

## Exact artifact transport

Use only:

```text
branch: qa/phase2-stage4-final-b64-transport-0ee1d38-2026-08-24
commit: 9dedf7bf624174996fae7efa7a4bdbff6904d348
path: extension/tests/qa_transport/phase2-stage4-final-b64/
```

This transport was independently fresh-consumer verified before handoff:

```text
run 32715052351
job 97394394286
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FINAL_FROZEN_AUTHORITY_MATCH_PASS
REAL_YANDEX_REQUESTS=0
```

You must still establish your own consumed-byte identity before product PASS credit.

## Step 0 — read governing authority

Read these from current `main` before execution:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CURRENT_STATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
extension/docs/PHASE_2_STAGE_4_CODEX_EXECUTION_MAP_2026-08-24.md
extension/tests/PHASE_2_STAGE_4_PACKAGED_SUITE_ADAPTER_2026-08-24.md
extension/tests/PHASE_2_STAGE_4_REFROZEN_CANDIDATE_CHECKPOINT_2026-08-24.md
```

The execution map is mandatory. It maps every enabled PD/S requirement to a concrete source/integration/browser/package venue.

Search addendum `S-15` supersedes the generic parent `PD-16` Search lock only for governed synchronous text Search. Webmaster, Metrika, Direct and Search async/deferred, image and generative surfaces remain locked.

## Step 1 — consume exact transport and materialize exact ZIP

Fresh-checkout transport commit:

```text
git checkout 9dedf7bf624174996fae7efa7a4bdbff6904d348
python extension/tests/qa_transport/phase2-stage4-final-b64/verify_exact_b64_transport.py
```

Require:

```text
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
REAL_YANDEX_REQUESTS=0
```

Then materialize the exact ZIP into a QA temp directory using only the 16 published chunks. Equivalent Python is authorized:

```python
from pathlib import Path
import base64, hashlib, json

base = Path('extension/tests/qa_transport/phase2-stage4-final-b64')
t = json.loads((base/'TRANSPORT_MANIFEST_2026-08-24.json').read_text(encoding='utf-8'))
text = ''.join((base/r['path']).read_text(encoding='ascii') for r in t['chunks'])
data = base64.b64decode(text, validate=True)
assert len(data) == 170734
assert hashlib.sha256(data).hexdigest() == 'd58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16'
out = Path('<QA_TEMP>')
out.mkdir(parents=True, exist_ok=True)
(out/'yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip').write_bytes(data)
(out/'EXACT_CANDIDATE_MANIFEST_2026-08-24.json').write_bytes((base/'EXACT_CANDIDATE_MANIFEST_2026-08-24.json').read_bytes())
```

Record exact SHA/bytes. Do not rebuild another ZIP as a substitute.

## Step 2 — exact source suite

Checkout exact frozen source:

```text
git checkout 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
cd extension/src
npm test
```

Required:

```text
231 tests
231 PASS
0 fail
0 skipped
0 cancelled
```

Do not edit tests if a failure appears.

## Step 3 — static / syntax / manifest

Against exact frozen source and exact package bytes:

- parse/check every JS/MJS;
- parse `manifest.json` and `package.json`;
- verify manifest-declared entrypoints/resources exist;
- verify expected permission/host-permission surface;
- verify no accidental production entrypoint/file;
- retain exact candidate identity.

Use the mapped source tests in PD-02/PD-15 as additional evidence.

## Step 4 — exact packaged suite

Do **not** invoke `node --test tests/*.test.mjs` directly from the installable ZIP root. That is a known invalid test venue because repository tests resolve runtime through `../src`.

Use only the governed adapter from exact source `0ee1d38...`:

```text
python extension/tests/qa_transport/phase2-candidate/run_packaged_suite.py \
  --archive <QA_TEMP>/yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip \
  --manifest <QA_TEMP>/EXACT_CANDIDATE_MANIFEST_2026-08-24.json \
  --work-dir <FRESH_QA_TEMP>/packaged-suite-work
```

Required:

```text
PACKAGE_EXACT_IDENTITY_PASS
PACKAGED_SUITE_LAYOUT_IDENTITY_PASS
PACKAGED_SYNTAX_PASS count=59
PACKAGED_JSON_PASS count=2
231/231 packaged tests PASS
PACKAGED_SUITE_PASS files=38
PACKAGED_PREDELIVERY_PREFLIGHT_PASS
```

The adapter must not modify the ZIP or source/test bytes.

## Step 5 — browser-owned sections

Use qualified Chrome for Testing + Puppeteer, installed exact extracted `d58b5bd...` extension, isolated QA profile and controlled ChatGPT fixtures. No real provider traffic.

Known demonstrated browser baseline:

```text
Chrome for Testing 151.0.7922.47
Puppeteer 25.4.0
headful isolated QA profile
```

### B-01 Project/Work installed-extension baseline

Use the governed harness:

```text
extension/tests/qa_transport/phase2-candidate/browser_project_route_smoke.mjs
```

Require MV3 service worker, content identity on `/g/.../c/<uuid>`, popup initialization, enabled controls and zero Yandex provider requests.

### B-02 mandatory Manual-ON real-popup transaction

Execute all 12 steps from:

```text
CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
```

Must use the real extension popup control. Do not use internal `applyManualMode`, preseed content ON or replace the transaction with mocks.

Require worker ON before content apply, content remains ON after authoritative resync, exactly one external `Яндекс` action remains armed through ordinary mutation/resync and popup reopen, OFF removes it, second ON re-arms it, real Yandex requests 0.

### B-03 Search Autorun/operator lifecycle

Use real popup + exact installed package + controlled fixture/stub provider. Verify the complete B-03 scenario in the execution map: one Search RUN, WAITING_COMMAND, controlled Search pickup, at-most-once provider initiation, exactly-once delivery, popup reopen truth, Pause/Resume/Finish, owner/conversation isolation and safe worker lifecycle. Use deterministic integration for crash windows.

Browser-required assertions cannot be replaced with source inspection.

## Step 6 — execute the complete matrix

Execute every enabled section from the living gate plus both mandatory addenda:

```text
PD-00 through PD-17
Manual-ON transaction addendum
S-00 through S-17 Phase-2 Search addendum
```

Use `PHASE_2_STAGE_4_CODEX_EXECUTION_MAP_2026-08-24.md` for exact test/harness mapping.

Do not stop the entire campaign after one ordinary assertion failure when unrelated sections remain safe to execute. Collect the complete failure set.

### Search scope that must be positively tested

```text
SEARCH_API_V1
service search
method search
POST https://searchapi.api.cloud.yandex.net/v2/web/search
FORMAT_XML
SEARCH_RESULT_V1
synchronous text Search only
```

All provider traffic in QA must be controlled stub/fault injection only.

### Surfaces that must remain zero-provider locked

```text
Search async/deferred
Search image
Search generative
Webmaster
Metrika
Direct
arbitrary assistant-selected URLs/methods/headers
```

## Step 7 — final immutability / cleanliness

At the end:

- re-run final B64 verifier;
- re-hash exact ZIP and require `d58b5bd...` / 170734;
- re-check all 65 manifest rows;
- prove production files were not changed during gate;
- prove package test bytes were not changed during gate;
- record repository/test working state;
- require real Yandex requests exactly 0;
- require no credentials/secrets in evidence;
- every PD and S section must be explicit;
- no enabled `NOT_RUN` may be treated as PASS.

## Required output

Create one Markdown report and one JSON report in the QA workspace/evidence location. Return this complete summary to ChatGPT/owner:

```text
CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT
candidate:
  source_commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
  artifact: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
  artifact_sha256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
  artifact_bytes: 170734
  files: 65
  zip_entries: 68
  transport_commit: 9dedf7bf624174996fae7efa7a4bdbff6904d348
sections:
  PD-00: PASS|FAIL
  PD-01: PASS|FAIL
  PD-02: PASS|FAIL
  PD-03: PASS|FAIL
  PD-04: PASS|FAIL
  PD-05: PASS|FAIL
  PD-06: PASS|FAIL
  PD-07: PASS|FAIL
  PD-08: PASS|FAIL
  PD-09: PASS|FAIL
  PD-10: PASS|FAIL
  PD-11: PASS|FAIL
  PD-12: PASS|FAIL
  PD-13: PASS|FAIL
  PD-14: PASS|FAIL
  PD-15: PASS|FAIL
  PD-16: PASS|FAIL
  PD-17: PASS|FAIL
manual_on_transaction: PASS|FAIL
search_sections:
  S-00: PASS|FAIL
  S-01: PASS|FAIL
  S-02: PASS|FAIL
  S-03: PASS|FAIL
  S-04: PASS|FAIL
  S-05: PASS|FAIL
  S-06: PASS|FAIL
  S-07: PASS|FAIL
  S-08: PASS|FAIL
  S-09: PASS|FAIL
  S-10: PASS|FAIL
  S-11: PASS|FAIL
  S-12: PASS|FAIL
  S-13: PASS|FAIL
  S-14: PASS|FAIL
  S-15: PASS|FAIL
  S-16: PASS|FAIL
  S-17: PASS|FAIL
source_suite: <pass>/<total>
packaged_suite: <pass>/<total>
packaged_syntax: <pass>/<total>
packaged_json: <pass>/<total>
browser_project_work: PASS|FAIL
browser_manual_on_transaction: PASS|FAIL
browser_search_autorun: PASS|FAIL
real_yandex_requests: <integer>
real_credentials_used: YES|NO
production_modified_during_gate: YES|NO
tests_modified_during_gate: YES|NO
not_run_enabled_sections: <integer>
search_phase2:
  protocol_registry: PASS|FAIL
  parser_validation: PASS|FAIL
  provider_request_exactly_once: PASS|FAIL
  credential_policy: PASS|FAIL
  cost_guard: PASS|FAIL
  base64_xml_decode: PASS|FAIL
  xml_normalization: PASS|FAIL
  manual_path: PASS|FAIL
  autorun_path: PASS|FAIL
  wordstat_search_isolation: PASS|FAIL
  http_unknown_no_retry: PASS|FAIL
  future_search_modes_locked: PASS|FAIL
  real_yandex_requests: <integer>
  verdict: PASS|FAIL
verdict: PASS|FAIL_PRODUCT|FAIL_ARTIFACT|FAIL_HARNESS
```

`PASS` is valid only when every mandatory PD section, Manual-ON transaction and every mandatory S section passes, source/package suites pass, browser-owned assertions execute in the qualified browser, exact artifact identity remains unchanged, no enabled section is NOT_RUN, and real Yandex requests equal 0.

## After the result

- `PASS` → return evidence to ChatGPT. Owner-live paid Search acceptance may then be prepared, but is still a separate later step requiring a fresh official pricing check.
- `FAIL_PRODUCT` → return failing assertions/evidence. Do not patch them yourself.
- `FAIL_ARTIFACT` → identify exact identity/transport failure; do not substitute another candidate.
- `FAIL_HARNESS` → identify missing/broken qualified venue; do not weaken the assertion or mutate frozen product bytes.
