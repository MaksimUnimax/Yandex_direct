# Codex QA artifact transport and full-gate runbook — Yandex Marketing Bridge

Status: **CURRENT / MANDATORY TEST-OPERATIONS RUNBOOK**  
Adopted: 2026-08-19  
Scope: every future ChatGPT → Codex pre-delivery QA handoff for Yandex Marketing Bridge.

This document is the concrete execution companion to:

- `extension/docs/WORKFLOW_OPERATING_RULES.md`
- `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`
- `extension/docs/CURRENT_STATE.md`

It exists because abstract rules such as “verify SHA” were not sufficient to prevent repeated `FAIL_ARTIFACT` mistakes. This runbook records the **actual sequence that reached a complete Codex execution and PASS** for the repaired 0.1.1 candidate.

The rule is simple:

> **Do not invent a QA transport procedure from scratch when a proven one exists. Prepare the transport exactly, prove it independently before the Codex prompt, and only then start the gate.**

---

## 1. Permanent anti-patterns — DO NOT DO THESE

The following are explicitly forbidden.

### 1.1 Do not treat an upload/write API success as transport proof

Forbidden evidence:

```text
GitHub create_blob/create_file/update_file returned success
branch/commit exists
filename appears in repository
blob SHA was returned
HTTP/API call returned 200/201
```

None of those proves that Codex can recover the intended exact artifact bytes.

Permanent negative example:

```text
expected artifact:
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505

bad GitHub object received by Codex:
SHA-256 37d896fb8c1542509abfb33780fee6ca802b0d76238b39d76ec78c309b22cf6d
bytes 14999
not a ZIP
```

That attempt was `FAIL_ARTIFACT` before product testing.

### 1.2 Do not give Codex a packaging recipe in prose and expect exact bytes

Forbidden:

```text
“dirs 0755”
“files 0644”
“ZIP_DEFLATED level 9”
“fixed timestamp”
```

without complete executable byte-affecting metadata.

Permanent negative example:

```text
source tree: 45/45 exact
ZIP bytes: 209505
ZIP integrity: PASS
actual SHA-256: 8359c6cf46ed9ca107675d56aec0d37b9615a009fa007b7f68abcddba3a96400
expected SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
```

The source was correct but ZIP metadata was not fully specified. In particular, UNIX file-type bits in `external_attr` were missing from the prose recipe.

### 1.3 Do not let Codex discover whether a new transport works

Transport is ChatGPT QA-engineering responsibility.

Wrong sequence:

```text
invent transport
→ write prompt
→ Codex discovers transport is broken
```

Required sequence:

```text
invent/reuse transport
→ publish inputs
→ fresh consumer reads the published inputs back
→ consumer reproduces exact target
→ SHA/bytes/ZIP/source identity PASS
→ only then issue Codex prompt
```

### 1.4 Do not mutate product bytes to repair transport/packaging

`FAIL_ARTIFACT`, `FAIL_HARNESS`, transport failure, or prompt failure does not authorize production changes.

Keep the exact frozen candidate unless separate evidence proves a product defect.

### 1.5 Do not use the owner as a file courier or QA operator

The owner must not be asked to:

- download/upload files for Codex;
- move/rename/extract QA artifacts;
- run shell commands;
- install Codex QA dependencies;
- reconstruct packages.

### 1.6 Do not substitute a logically equivalent package

If the target artifact identity is frozen, a different ZIP with the same extracted files is not the same artifact.

Exact SHA-256 and byte count are authoritative.

---

## 2. Proven successful pattern — exact 0.1.1 e13a campaign

The following sequence is the canonical worked example because it actually reached:

```text
artifact exact identity PASS
Manual-ON browser regression PASS
PD-00..PD-17 ALL PASS
source suite 361/361 PASS
packaged suite 361/361 PASS
syntax 40/40 PASS
JSON 2/2 PASS
real Yandex requests 0
verdict PASS
```

### 2.1 Frozen target

```text
filename:
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip

SHA-256:
e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65

bytes:
209505

files:
45

ZIP entries including directories:
48
```

Production hashes:

```text
content_script.js
ddf9ed51c60ab90dcdeb1fcd5a1b955c3dd88dfc53a0ddfd5842d66ebe9a02cc

popup.js
ac87ad973e8b673bf0c235a43b3dc29dfb67865594ea62e085f943660f0a7ab2

service_worker.js
2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

### 2.2 Exact preimage already available in Codex

The successful procedure reused the exact previous artifact already present in the Codex QA workspace:

```text
D:\codex\Yandex\qa-evidence-ymb-full-gate-20260819-04\yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
```

Required identity:

```text
SHA-256:
31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14

bytes:
209697

files:
45

ZIP integrity:
PASS
```

Codex did not trust the filename. It independently recalculated identity first.

### 2.3 Patch transport inputs

The exact patch transport was text-safe and small enough to survive GitHub transport reliably.

Canonical inputs:

```text
branch:
qa/e13a-exact-reconstruction-v3

extension/tests/qa_transport/e13a/patch.gz.b64.part00
extension/tests/qa_transport/e13a/patch.gz.b64.part01
extension/tests/qa_transport/e13a/target-tree-sha256.tsv
extension/tests/qa_transport/e13a/canonical_packer_exact.py
```

Patch chunk identities:

```text
part00 chars: 3500
part00 SHA-256:
16ae23212f2b136fa9b408e36a37918105976c195adf005978721655f78d0a07

part01 chars: 2484
part01 SHA-256:
197d4a39ca45b69002ab40b39e2d63dcb41abf22714b67fd97ae7edf2704b54a
```

Concatenate exact bytes:

```text
part00 + part01
```

Do not insert a newline. Do not trim. Do not convert CRLF/LF. Do not normalize whitespace.

Expected concatenated base64:

```text
chars: 5984
SHA-256:
ddd6e3357441297e0d6980ff45615e31d047d8335c6344f57d0ea0f68d47492d
```

Base64-decode:

```text
gzip bytes: 4488
SHA-256:
f575398d19351625c69b1bdb3be3ad69968e364b3b1fda7f488e5e22edd75002
```

Gzip-decompress:

```text
raw patch bytes: 21532
SHA-256:
709234433bd446f52a18c95785675d0f5ca3450b82459ce2631d36bdb7269bc2
```

If any of those identities differ, stop with `FAIL_ARTIFACT`; do not begin product QA.

---

## 3. Exact source reconstruction steps that worked

Use a fresh directory every time.

### Step 1 — verify preimage

Before extraction, verify:

```text
SHA-256 == 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
bytes == 209697
ZIP opens
45 files
```

### Step 2 — fresh-extract preimage

Do not reuse a previously modified/extracted QA tree.

### Step 3 — verify exact patch inputs

Verify part00, part01, concatenated base64, decoded gzip, and raw patch identities from section 2.3.

### Step 4 — run patch dry check

Run the equivalent of:

```text
git apply --check <raw-patch>
```

Required:

```text
PASS
```

### Step 5 — apply patch byte-safely

Apply the exact raw patch.

Do not:

- edit files manually;
- normalize line endings;
- rewrite text through a platform-dependent editor;
- modify tests;
- modify production beyond what the exact patch contains.

### Step 6 — verify entire postimage tree

Use:

```text
extension/tests/qa_transport/e13a/target-tree-sha256.tsv
```

Manifest identity used by the successful campaign:

```text
SHA-256:
7c7234e184403de6a02e843b92bfd5f2fa12ed2391c054f4fa221d690f5b44b7

files:
45
```

Require for all 45 files:

```text
exact path set
exact byte count
exact SHA-256
```

Result must be:

```text
45/45 PASS
```

This check is mandatory before packaging.

---

## 4. Exact executable packer — use the code, not prose

Canonical executable packaging authority used by the successful campaign:

```text
branch:
qa/e13a-exact-reconstruction-v3

path:
extension/tests/qa_transport/e13a/canonical_packer_exact.py
```

Do not rewrite the algorithm in the Codex prompt. Do not ask Codex to imitate it. Tell Codex to execute the published file unchanged.

The successful packer fixed, among other fields:

```text
archive root:
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate

fixed timestamp:
2025-12-31 19:00:00

create_system:
3 (UNIX)

directory external_attr:
((S_IFDIR | 0755) << 16) | 0x10

regular file external_attr:
((S_IFREG | 0644) << 16)

directories:
ZIP_STORED

files:
ZIP_DEFLATED
compression level 9

extra:
empty

comments:
empty

paths:
forward slashes

entry order:
root dir first
then directories lexicographically
then files lexicographically
```

The important permanent rule is not to memorize these fields and rewrite them. The executable packer file is the authority.

---

## 5. Mandatory pre-Codex consumer-conformance test

Before issuing a Codex prompt, ChatGPT must act as a fresh consumer of the published handoff contract.

### Required fresh-consumer inputs

Use only:

- exact governed preimage;
- files freshly read back from the published GitHub QA branch;
- published target-tree manifest;
- published executable packer.

Do not use hidden local variables or an unpublished packer.

### Required consumer sequence

```text
1. read patch chunks back from GitHub
2. verify chunk hashes
3. concatenate/decode/decompress
4. verify raw patch SHA
5. fresh-extract exact preimage
6. git apply --check
7. apply patch
8. verify target tree 45/45
9. read canonical_packer_exact.py back from GitHub
10. execute that downloaded packer unchanged
11. verify output SHA/bytes
12. open/test ZIP
13. verify 45 files / 48 entries
14. compare output bytes with frozen target when local frozen target is available
```

For the successful e13a campaign, the mandatory result was:

```text
output SHA-256:
e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65

output bytes:
209505

files:
45

ZIP entries:
48

ZIP integrity:
PASS

output byte-identical to frozen target:
YES
```

Only after this result may ChatGPT set:

```text
AUTHORIZED_NEXT_STAGE = CODEX_COMPLETE_PRE_DELIVERY_FULL_GATE
```

and issue the Codex prompt.

---

## 6. Codex prompt preparation — exact order

The prompt must not start with “run tests” and leave artifact preparation implicit.

Use this order:

### Phase A — authority

Codex fetches live `main` and reads:

```text
WORKFLOW_OPERATING_RULES.md
CURRENT_STATE.md
CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
this runbook
other current product/spec authority required by CURRENT_STATE
```

### Phase B — preimage identity

Codex independently verifies the old exact preimage SHA/bytes/files/ZIP.

### Phase C — transport identity

Codex independently verifies:

- patch chunk identities;
- concatenated base64;
- gzip;
- raw patch;
- target tree manifest;
- executable packer file.

### Phase D — source postimage

Codex fresh-extracts, runs `git apply --check`, applies exact patch, and requires `45/45` target tree.

### Phase E — exact package

Codex executes the published executable packer **unmodified** and requires:

```text
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505
files 45
entries 48
ZIP integrity PASS
```

### Phase F — product gate

Only after Phase E PASS may Codex execute:

```text
PD-00..PD-17
mandatory Manual-ON transaction addendum
real installed-extension popup scenario
source suite
packaged suite
syntax
JSON
source/package identity
```

### Phase G — immutability/reporting

Require:

```text
production_modified_during_gate = 0
tests_modified_during_gate = 0
real_yandex_requests = 0
```

Allowed verdicts:

```text
PASS
FAIL_PRODUCT
FAIL_ARTIFACT
FAIL_HARNESS
```

---

## 7. Known qualified browser harness used in the successful campaign

The successful real-popup regression used the qualified Codex browser environment:

```text
Chrome executable:
D:\codex\Test\qa-harness\puppeteer-extension-qa\chrome\win64-151.0.7922.47\chrome-win64\chrome.exe

Chrome:
151.0.7922.47

Puppeteer:
25.4.0

mode:
headful
isolated QA profile
real extension installed
```

Do not claim browser QA is unavailable merely because a higher-level UI browser button is absent. Use the demonstrated executable harness unless evidence proves it is no longer available.

---

## 8. Mandatory Manual-ON regression that must remain in every relevant gate

Initial state:

```text
worker Manual OFF
content Manual OFF
eligible ChatGPT command block present
```

Use the real installed extension popup.

Required transaction:

```text
real popup Manual ON
→ WS_SET_MANUAL_MODE(true) committed to worker first
→ WS_APPLY_MANUAL_MODE(true) to content second
→ worker remains ON
→ content remains ON
→ exactly one external Yandex action exists and is enabled
→ ordinary resync/mutation does not revert it OFF
→ popup close/reopen still ON
→ real popup OFF removes action
→ second real popup ON remains armed after resync
```

Forbidden substitutes:

- direct internal `applyManualMode(true)`;
- preseed content ON;
- popup mock;
- synthetic success response;
- bypassing popup→worker→content ordering.

Any ON→OFF self-revert is `FAIL_PRODUCT`.

---

## 9. Successful campaign reference result

The procedure above produced the following actual Codex result on 2026-08-19:

```text
artifact SHA-256:
e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65

artifact bytes:
209505

artifact files:
45

ZIP entries:
48

ZIP integrity:
PASS

Manual-ON transaction regression:
PASS

on_to_off_self_revert_observed:
NO

PD-00..PD-17:
ALL PASS

source suite:
361/361 PASS

packaged suite:
361/361 PASS

syntax:
40/40 PASS

JSON:
2/2 PASS

source/package identity:
PASS

real Yandex requests:
0

production modified during gate:
0

tests modified during gate:
0

verdict:
PASS
```

Codex evidence workspace:

```text
D:\codex\Yandex\qa-evidence-ymb-full-gate-20260819-06\
```

This result is the proof that the runbook sequence is executable, not theoretical.

---

## 10. Checklist ChatGPT must complete before every future Codex prompt

Every applicable item must be YES:

```text
[ ] live main authority fetched
[ ] CURRENT_STATE read
[ ] exact candidate frozen
[ ] product bytes unchanged during QA transport preparation
[ ] latest proven transport procedure reviewed first
[ ] exact preimage/input independently verified where reconstruction is used
[ ] all transport components freshly read back from Codex-accessible GitHub path
[ ] all transport component hashes verified
[ ] fresh source reconstruction performed where applicable
[ ] git apply --check PASS where applicable
[ ] complete target tree identity PASS
[ ] executable packer published
[ ] executable packer freshly read back from GitHub
[ ] fresh consumer executed published packer unchanged
[ ] consumer artifact SHA equals frozen target SHA
[ ] consumer artifact byte count equals frozen target byte count
[ ] ZIP integrity PASS
[ ] file count PASS
[ ] source/package identity PASS
[ ] known qualified browser harness path included when needed
[ ] every enabled PD section has an executable venue
[ ] no owner file handling required
[ ] Codex prompt instructs QA-only / no code or test edits
```

If any applicable box is not satisfied, do not issue the Codex prompt.

---

## 11. Rule for future candidates

The exact hashes/filenames in this document are the worked 0.1.1 example. Future candidates will have different artifact/source hashes.

The reusable procedure is:

```text
freeze exact target
→ choose proven transport
→ publish exact transport inputs
→ read them back
→ fresh consumer reconstructs/reassembles target
→ complete source identity
→ execute published byte-complete packer if reconstruction is needed
→ exact target SHA/bytes/ZIP PASS
→ Codex independently repeats identity phase
→ only then full product gate
```

Do not copy old expected hashes onto a new candidate. Do copy the **execution discipline**.
