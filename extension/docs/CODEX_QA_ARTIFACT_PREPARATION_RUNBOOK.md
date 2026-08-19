# Codex QA artifact preparation runbook — Yandex Marketing Bridge

Status: **MANDATORY / PRE-CODEX / COMPANION TO THE LIVING FULL GATE**  
Adopted: 2026-08-19  
Scope: every future attempt to prepare a frozen Yandex Marketing Bridge candidate for Codex pre-delivery QA.

This document converts the permanent prohibitions in `WORKFLOW_OPERATING_RULES.md` and `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` into an executable preparation procedure.

It exists because two `FAIL_ARTIFACT` campaigns were caused by QA preparation mistakes before product testing started, while the third preparation path reached exact artifact identity and a complete Codex PASS.

The procedure below is therefore the **default proven preparation route** until a newer route is independently demonstrated and deliberately replaces it.

---

## 1. Golden rule

Codex is the **QA executor**, not the transport debugger.

Before the owner receives any Codex prompt, ChatGPT must already have proved that the exact QA input contract Codex will consume is sufficient to produce or obtain the exact frozen candidate.

The required chain is:

```text
freeze candidate
→ record exact target identity
→ prepare Codex-accessible transport
→ read the published transport back
→ execute the handoff contract from a fresh consumer state
→ reproduce/obtain exact target SHA + bytes + archive integrity + tree identity
→ only then issue Codex prompt
→ Codex independently repeats identity checks
→ only then product PD-00..PD-17 begins
```

A successful upload, Git commit, Git blob creation, file listing or API response is **not** completion of this chain.

---

## 2. Required preparation outputs

Every Codex campaign must have these prepared **before** the Codex prompt is issued:

```text
A. exact frozen target identity
B. Codex-accessible transport identity
C. complete source/postimage identity
D. byte-complete executable package authority when reconstruction is used
E. fresh consumer-conformance proof
F. full-gate test authority and any mandatory addenda
G. qualified browser/harness coordinates when browser assertions are enabled
H. final report schema
```

Minimum target identity record:

```text
filename
version
SHA-256
byte count
file count
ZIP entry count if governed
critical production-file hashes
```

Never prepare a Codex prompt from only a filename or a source commit.

---

## 3. Transport route selection — mandatory order

Use this order and do not skip directly to a newly invented mechanism:

```text
1. proven direct exact-ZIP route already demonstrated in Codex;
2. another machine-safe direct exact-ZIP route, but only after round-trip proof;
3. machine-safe text encoding of the exact ZIP bytes, followed by exact reassembly proof;
4. exact reconstruction fallback using a governed preimage + exact patch + full tree manifest + executable packer;
5. if none of the above can be proved before the prompt: STOP / transport not ready.
```

A new route is not preferred merely because it looks simpler from ChatGPT's current tool environment.

Capabilities are environment-specific. A route must be judged by whether **Codex can consume it and ChatGPT can prove it before prompt handoff**.

---

## 4. What worked for the successful `e13a…` campaign

The successful campaign used an exact reconstruction fallback because the available GitHub connector could safely carry the reconstruction text inputs while the direct binary-object attempt had already failed.

The working chain was:

```text
Codex-proven exact old ZIP preimage
→ exact raw patch represented as gzip+base64 text chunks in GitHub
→ exact per-layer hashes
→ fresh extraction of preimage
→ byte-safe patch application
→ full 45/45 target-tree manifest verification
→ published executable canonical ZIP packer
→ exact e13a ZIP reproduction
→ ZIP integrity + file/entry verification
→ complete Codex PD-00..PD-17 + mandatory browser addendum
→ PASS
```

This is the concrete route to copy when the same class of reconstruction is needed again.

---

## 5. Step-by-step preparation procedure

### STEP 0 — reconstruct live authority

Before preparing QA inputs:

1. fetch live `main` HEAD;
2. read `README.md`;
3. read `WORKFLOW_OPERATING_RULES.md`;
4. read `CURRENT_STATE.md`;
5. read the current full gate and relevant addenda;
6. establish the exact authorized stage;
7. confirm whether production bytes changed since the previous complete gate.

Do not continue from remembered candidate names or hashes.

### STEP 1 — freeze and verify the exact target

Build/freeze the candidate intended for owner handoff.

Record:

```text
TARGET_FILENAME
TARGET_SHA256
TARGET_BYTES
TARGET_FILE_COUNT
TARGET_ZIP_ENTRY_COUNT
TARGET_VERSION
CRITICAL_PRODUCTION_HASHES
```

Verify locally/in the producer environment:

```text
SHA-256 == recorded target
bytes == recorded target
ZIP opens
ZIP test/integrity == PASS
fresh extraction succeeds
file/path count == recorded target
```

The frozen target must not change while artifact/transport preparation is repaired.

### STEP 2 — identify a proven Codex-side preimage when reconstruction is needed

If reconstruction is the selected fallback, prefer a preimage that Codex already possessed and independently verified in a previous successful campaign.

Record:

```text
PREIMAGE_FILENAME
PREIMAGE_SHA256
PREIMAGE_BYTES
PREIMAGE_FILES
KNOWN_CODEX_PATH or proven retrieval route
```

Codex must verify the preimage by SHA, bytes and archive integrity before using it.

A filename match is not enough.

If the exact preimage is unavailable to Codex, do not pretend reconstruction is ready. Fix transport or choose another governed route before prompt handoff.

### STEP 3 — produce the exact raw patch

Create the exact byte patch from governed preimage source to frozen target source.

The patch must represent only the intended changed files.

Before transport, record:

```text
RAW_PATCH_BYTES
RAW_PATCH_SHA256
EXPECTED_CHANGED_PATHS
```

Require the patch to apply cleanly to a fresh exact preimage:

```text
git apply --check equivalent == PASS
```

No EOL normalization or text rewriting is allowed.

### STEP 4 — encode the patch as machine-safe GitHub text transport

The route that worked used:

```text
raw patch bytes
→ gzip
→ base64 ASCII
→ deterministic text chunks
```

For **every** layer record identity:

```text
raw patch bytes + SHA-256
gzip bytes + SHA-256
concatenated base64 chars + SHA-256
for each chunk:
  repository path
  character count
  SHA-256
  Git blob SHA-1 when available
```

Chunk concatenation must be explicitly defined:

```text
part00 bytes + part01 bytes + ...
NO separator
NO inserted newline
NO trimming
NO CRLF conversion
NO whitespace normalization
```

After publication, read each chunk back from GitHub and independently re-check these identities.

### STEP 5 — publish a complete target-tree manifest

Generate a manifest covering **every target file**, not selected production files only.

Recommended governed form:

```text
path<TAB>bytes<TAB>sha256
```

Record:

```text
TARGET_TREE_MANIFEST_PATH
TARGET_TREE_MANIFEST_SHA256
TARGET_TREE_MANIFEST_GIT_BLOB
TARGET_TREE_FILE_COUNT
```

After patch application, require:

```text
path set == exact
file count == exact
byte count for every file == exact
SHA-256 for every file == exact
```

For the successful `e13a…` campaign this gate was `45/45` exact.

A `45/45` target-tree PASS is necessary but **not sufficient** to prove the ZIP bytes.

### STEP 6 — publish executable canonical packer authority

When the final exact ZIP must be reconstructed, publish the **actual executable packer** in the QA transport branch.

Do not give Codex a prose reimplementation recipe when exact package SHA matters.

The packer must fix all byte-affecting ZIP behavior, including where applicable:

```text
canonical archive root
entry order
explicit directory entries
timestamps
create_system / host metadata
S_IFDIR / S_IFREG file-type bits
permission bits
external_attr
DOS directory flag
compression method
compression level
extra fields
entry comments
archive comment
filename/path separators
encoding/flags
creator/extract version if relevant
```

The packer should self-verify the expected target and exit non-zero on mismatch.

For the successful `e13a…` packer the critical metadata included:

```text
create_system = 3
root + explicit directory entries
directories: ZIP_STORED
directory external_attr = ((S_IFDIR | 0755) << 16) | 0x10
files: ZIP_DEFLATED level 9
regular-file external_attr = ((S_IFREG | 0644) << 16)
fixed timestamp = 2025-12-31 19:00:00
extra = empty
comments = empty
forward-slash paths
```

The old incomplete prose `dirs 0755 / files 0644` was not sufficient and produced the wrong package SHA even from an exact target tree.

### STEP 7 — publish one transport manifest

Create a machine-readable manifest that references every QA preparation input and expected identity.

It must include at minimum:

```text
schema/version
transport branch/ref
purpose
preimage identity
patch chunk identities
concatenated base64 identity
gzip identity
raw patch identity
target-tree manifest identity
canonical packer path
target artifact identity
mandatory consumer sequence
fail-closed behavior
```

Codex should be able to read this manifest and know exactly what objects to verify before product testing begins.

### STEP 8 — perform producer-side round-trip / consumer-conformance

This step is mandatory and is the one that would have prevented both earlier artifact failures.

Use a **fresh directory/process** and only:

```text
published GitHub transport objects
+ explicitly governed preimage already intended for Codex
```

Do not use:

```text
hidden local target files
unpublished packer state
remembered metadata
producer-only helper variables
manual corrections after download
```

Execute the same sequence Codex will execute:

```text
1. verify preimage SHA/bytes/ZIP/files;
2. read published chunks back from GitHub;
3. verify each chunk;
4. concatenate exactly;
5. verify concatenated base64;
6. decode and verify gzip;
7. decompress and verify raw patch;
8. fresh-extract preimage;
9. patch byte-safely;
10. verify complete target tree against manifest;
11. fetch/read published canonical packer;
12. execute it unmodified;
13. require exact target ZIP SHA/bytes/files/entries;
14. run ZIP integrity test;
15. fresh-extract final ZIP and verify governed identity.
```

Only a complete PASS authorizes the Codex prompt.

### STEP 9 — prepare the QA execution map

Artifact identity alone is not enough. Before prompt handoff, map every enabled gate section to a concrete Codex-capable venue.

At minimum classify each assertion as one of:

```text
source/static
Node/VM/unit
content↔worker deterministic integration
network stub/fault injection
qualified CfT/Puppeteer browser
package/extraction identity
```

For browser-owned assertions, publish the known harness coordinates rather than asking Codex to rediscover them.

For the successful current campaign:

```text
Chrome for Testing:
D:\codex\Test\qa-harness\puppeteer-extension-qa\chrome\win64-151.0.7922.47\chrome-win64\chrome.exe
Chrome 151.0.7922.47
Puppeteer 25.4.0
headful isolated QA profile
```

### STEP 10 — prepare the Codex prompt only after authorization checklist PASS

Before giving the prompt, ChatGPT must be able to answer YES to all applicable lines:

```text
LIVE_AUTHORITY_RECONSTRUCTED = YES
EXACT_TARGET_FROZEN = YES
PRODUCT_BYTES_UNCHANGED_DURING_QA_PREP = YES
PROVEN_ROUTE_REUSED_OR_PROVEN_INAPPLICABLE = YES
CODEX_INPUT_ACCESSIBLE = YES
PREIMAGE_IDENTITY_GOVERNED = YES                # reconstruction only
PATCH_ALL_LAYERS_HASHED = YES                    # reconstruction only
TARGET_TREE_FULL_MANIFEST = YES                  # reconstruction only
EXECUTABLE_PACKER_PUBLISHED = YES                # exact ZIP reconstruction only
PUBLISHED_INPUTS_READ_BACK = YES
FRESH_CONSUMER_CONFORMANCE = YES
FINAL_SHA_MATCH = YES
FINAL_BYTES_MATCH = YES
FINAL_ARCHIVE_OPEN = YES
FINAL_TREE_IDENTITY = YES
PD00_PD17_EXECUTION_MAP_READY = YES
MANDATORY_ADDENDA_INCLUDED = YES
BROWSER_HARNESS_COORDINATES_INCLUDED = YES       # if browser assertions enabled
OWNER_FILE_HANDLING_REQUIRED = NO
```

Any `NO` means: **do not issue the Codex prompt yet**.

### STEP 11 — Codex must independently repeat identity before product tests

The prompt must require Codex to repeat the exact identity sequence itself.

Product QA may begin only after Codex obtains/reproduces the exact target:

```text
SHA == expected
bytes == expected
file count == expected
ZIP integrity == PASS
source/package identity == governed expected
```

If exact identity fails:

```text
verdict = FAIL_ARTIFACT
product PD campaign does not receive PASS credit
production/tests remain untouched
```

### STEP 12 — one complete campaign

After exact identity PASS, Codex executes the complete current living gate plus every mandatory addendum.

Requirements:

```text
PD-00..PD-17 all enabled sections executed
no enabled NOT_RUN on PASS
browser-owned assertions executed in browser
zero real Yandex requests unless a future gate explicitly changes this
production_modified_during_gate = NO
tests_modified_during_gate = NO
```

Only a complete `PASS` authorizes owner handoff of that exact artifact.

---

## 6. Permanent DO NOT list

The following preparation mistakes are forbidden:

1. **Do not treat `create_blob`, upload, commit or API success as byte-identity proof.**
2. **Do not give Codex a prompt before producer-side round-trip/consumer-conformance PASS.**
3. **Do not use Codex as the experiment that tells ChatGPT whether a newly invented transport works.**
4. **Do not transport a logical/source equivalent and call it the exact frozen artifact without exact package SHA proof.**
5. **Do not use a prose ZIP recipe when an exact SHA is required; publish executable packer authority.**
6. **Do not accept complete source-tree identity as substitute for package-byte identity.**
7. **Do not allow CRLF/LF conversion, trimming, newline insertion or text-mode rewrite in exact-byte inputs.**
8. **Do not reconstruct from a stale or merely similarly named preimage; verify SHA/bytes/archive first.**
9. **Do not ask the owner to download/upload/move/stage QA files.**
10. **Do not change production bytes because artifact/transport preparation failed.**
11. **Do not patch tests during independent Codex QA.**
12. **Do not substitute another candidate after the campaign starts.**
13. **Do not leave enabled PD sections `NOT_RUN` and call the campaign complete.**
14. **Do not replace browser-owned assertions with source inspection or direct internal calls.**
15. **Do not manually copy a giant base64 payload through model/tool arguments and assume it remained byte-exact; only use a machine-verified path with read-back identity.**
16. **Do not invent another route while a proven applicable route exists.**

---

## 7. Exact successful reference — `e13a…`

This section is a factual worked example, not a template value for future releases.

### Frozen target

```text
filename:
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip

SHA-256:
e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65

bytes:
209505

files:
45

ZIP entries:
48
```

### Proven preimage already present in Codex

```text
filename:
yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip

SHA-256:
31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14

bytes:
209697

files:
45

known Codex workspace path:
D:\codex\Yandex\qa-evidence-ymb-full-gate-20260819-04\yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
```

### Successful QA transport branch

```text
qa/e13a-exact-reconstruction-v3
```

### Transport manifest

```text
extension/tests/qa_transport/e13a/transport-manifest-v2.json
schema: YMB_QA_EXACT_RECONSTRUCTION_TRANSPORT_V2
```

### Patch chunks

```text
part00:
extension/tests/qa_transport/e13a/patch.gz.b64.part00
chars 3500
SHA-256 16ae23212f2b136fa9b408e36a37918105976c195adf005978721655f78d0a07
Git blob eecddec70dd896a324fb7fc2db64810cf404c66f

part01:
extension/tests/qa_transport/e13a/patch.gz.b64.part01
chars 2484
SHA-256 197d4a39ca45b69002ab40b39e2d63dcb41abf22714b67fd97ae7edf2704b54a
Git blob 8584db901f65be77cc3cd520692e4d222d049cd6
```

### Exact patch-layer identities

```text
concatenated base64 chars:
5984

concatenated base64 SHA-256:
ddd6e3357441297e0d6980ff45615e31d047d8335c6344f57d0ea0f68d47492d

gzip bytes:
4488

gzip SHA-256:
f575398d19351625c69b1bdb3be3ad69968e364b3b1fda7f488e5e22edd75002

raw patch bytes:
21532

raw patch SHA-256:
709234433bd446f52a18c95785675d0f5ca3450b82459ce2631d36bdb7269bc2
```

### Target-tree authority

```text
extension/tests/qa_transport/e13a/target-tree-sha256.tsv
files 45
SHA-256 7c7234e184403de6a02e843b92bfd5f2fa12ed2391c054f4fa221d690f5b44b7
Git blob 16c626dae276def8870c0a40c0f64a276cd3df1a
```

### Executable packer authority

```text
extension/tests/qa_transport/e13a/canonical_packer_exact.py
branch qa/e13a-exact-reconstruction-v3
```

Codex executed the published packer unmodified and obtained the exact expected `e13a…` ZIP.

### Final independent Codex result

```text
artifact SHA: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
artifact bytes: 209505
files: 45
ZIP entries: 48
ZIP integrity: PASS
target tree identity: PASS
PD-00..PD-17: ALL PASS
Manual-ON real-popup transaction regression: PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source/package identity: PASS
real Yandex requests: 0
production modified during gate: 0
tests modified during gate: 0
verdict: PASS
```

This is the proof that the concrete procedure above reaches real Codex execution and complete QA, rather than merely looking valid in the producer environment.

---

## 8. Failure handling during preparation

If any preparation identity fails:

```text
preserve evidence
→ classify ARTIFACT/PACKAGING or TRANSPORT
→ keep production frozen
→ fix only preparation layer
→ rerun fresh consumer-conformance
→ no Codex prompt until exact PASS
```

If Codex later reports `FAIL_ARTIFACT`, do not automatically create a new product candidate. First determine whether the frozen product bytes ever failed a product assertion. If they did not, keep them frozen and repair only the preparation/transport contract.

---

## 9. Future-release template

For a future artifact replace values, not the procedure:

```text
TARGET_FILENAME = ...
TARGET_SHA256 = ...
TARGET_BYTES = ...
TARGET_FILES = ...
TARGET_ZIP_ENTRIES = ...

PROVEN_TRANSPORT_ROUTE = ...

PREIMAGE_SHA256 = ...          # only if reconstruction is used
PATCH_SHA256 = ...             # only if reconstruction is used
TARGET_TREE_MANIFEST = ...     # only if reconstruction is used
CANONICAL_PACKER = ...         # only if exact ZIP reconstruction is used

CONSUMER_CONFORMANCE = PASS
CODEX_ACCESS = PASS
OWNER_FILE_HANDLING = NO
```

Do not copy the `e13a…` numeric values into another release unless they genuinely remain the exact governed identities.
