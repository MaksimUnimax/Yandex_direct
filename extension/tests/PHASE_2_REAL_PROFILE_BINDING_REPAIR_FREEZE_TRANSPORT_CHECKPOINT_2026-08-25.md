# Phase 2 real-profile binding repair — freeze + transport checkpoint

Status: **CHATGPT CONTROLLED PRE-CODEX PASS / INDEPENDENT CODEX PENDING / OWNER LIVE BLOCKED**  
Date: 2026-08-25

This checkpoint records the exact repaired Phase-2 candidate, its frozen artifact and the proven Windows-safe transport. It is not an independent Codex full-gate PASS and does not authorize owner-live Search.

## 1. Repair authority

Historical factual real-profile evidence proved that the working ChatGPT conversation id was:

```text
6a82924e-5ed0-83eb-84a2-851ddad40c88
```

The reconstructed Phase-2 identity/binding path had five proven regressions:

1. an RFC UUID-version `[1-5]` filter rejected the factual `...83eb...` conversation id;
2. trusted canonical `/c/<id>` fallback had been lost and content identity used only `location.href`;
3. a delivered `WS_GET_IDENTITY` response could be treated as bootstrap success even with `ok:false` / empty `conversation_key`;
4. Bind availability was circularly tied to already-confirmed conversation context;
5. Manual ON ordering had drifted from the proven transaction: content acknowledgement first, worker authorization second.

Fail-first focused verification before the repair produced the expected five failures. After the repair:

```text
focused affected suite = 37/37 PASS
complete source suite = 244/244 PASS
real Yandex requests = 0
```

Controlled Chrome 151 verification also passed both repair-specific cases: factual direct `/c/6a82924e-5ed0-83eb-84a2-851ddad40c88` with late extension installation, and a Project/root URL using a trusted canonical direct-conversation URL with an already-live receiver. Bind and Manual ON succeeded in both cases. This is ChatGPT-owned internal evidence only, not Codex evidence.

## 2. Clean repaired product source

```text
branch = candidate/phase2-real-profile-binding-repair-2026-08-25
source commit = b7869180c229356a6b3d51ac980ec3da5df4c23c
parent = f4aee34c0a3455aa7199f6aa54bd581c71d97337
```

The source delta is exactly one commit and exactly six files:

```text
extension/src/content_script.js
extension/src/popup.js
extension/src/popup_context_bootstrap.js
extension/src/shared/conversation_identity.js
extension/tests/popup_phase2_runtime.test.mjs
extension/tests/real_profile_binding_regression.test.mjs
```

Temporary QA workflows and browser harness files are not part of the product candidate.

## 3. Exact freeze

Freeze Actions authority:

```text
run = 32805530317
job = 97674800575
result = PASS
real Yandex requests = 0
```

The freeze gate established:

```text
exact six-file delta = PASS
source suite = 244/244 PASS
source JS syntax = 22 files PASS
source JSON = 2/2 PASS
deterministic first build = PASS
independent byte-identical rebuild = PASS
packaged suite = 244/244 PASS
packaged JS syntax = 63 files PASS
packaged JSON = 2/2 PASS
```

Frozen artifact:

```text
filename = yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes = 179013
files = 69
ZIP entries = 72
ZIP integrity = PASS
```

Payload manifest:

```text
filename = EXACT_REAL_PROFILE_BINDING_REPAIR_CANDIDATE_MANIFEST_2026-08-25.json
SHA-256 = ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
bytes = 12125
source_commit = b7869180c229356a6b3d51ac980ec3da5df4c23c
```

GitHub Actions artifact:

```text
artifact id = 9548000690
name = phase2-real-profile-binding-repair-frozen-candidate-b786918
```

ChatGPT downloaded the Actions artifact back and independently verified the outer archive, the exact inner ZIP SHA/byte count, the payload manifest SHA/byte count, `source_commit`, file/entry counts and both ZIP integrity checks. The returned inner ZIP remained exactly `ce824a9f...`.

## 4. Proven Windows-safe exact transport

Transport branch:

```text
qa/phase2-real-profile-binding-final-b64-transport-b786918-2026-08-25
```

Transport commit:

```text
9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
```

It is exactly one commit above `b786918...` and adds exactly five QA transport files under:

```text
extension/tests/qa_transport/phase2-real-profile-binding-final-b64/
```

Files:

```text
.gitattributes
EXACT_REAL_PROFILE_BINDING_REPAIR_CANDIDATE_MANIFEST_2026-08-25.json
TRANSPORT_MANIFEST_2026-08-25.json
artifact.b64
verify_exact_b64_transport.py
```

Transport identity:

```text
artifact.b64 bytes/chars = 238684
artifact.b64 SHA-256 = 0c0f2b19e1c630232c71cfd7d81c776693fce6b889482e9536d7c7b3ab38e803
raw-text policy = * -text
```

Windows consumer proof:

```text
run = 32805811476
job = 97675604279
OS = Microsoft Windows Server 2025
Git = 2.55.0.windows.4
core.autocrlf = true
result = PASS
```

Required markers all passed:

```text
WINDOWS_TRANSPORT_PARENT_PASS
WINDOWS_RAW_TEXT_POLICY_PASS
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
WINDOWS_SAFE_EXACT_TRANSPORT_PASS
WINDOWS_TRANSPORT_CLEAN_PASS
REAL_YANDEX_REQUESTS=0
```

The QA trigger PRs used only to run freeze/transport were closed without merge.

## 5. Repair-specific browser harness authority

A clean QA-only harness commit is pinned as one commit above the exact product source:

```text
branch = qa/phase2-real-profile-binding-browser-harness-b786918-2026-08-25
commit = 81625e073d507d70451f1457185a3e906c640c66
file = extension/tests/qa_browser/real_profile_binding_gate.mjs
blob = 790539464d7f72214a3126c6585aac74e1afec39
```

The diff from `b786918...` is exactly that one QA file. The harness must remain external to the frozen package and must be run by Codex against a fresh extraction of the exact `ce824a9f...` artifact.

Qualified environment already demonstrated by ChatGPT controlled QA:

```text
Chrome for Testing = 151.0.7922.47
puppeteer-core = 25.4.0
```

## 6. Boundary

```text
INDEPENDENT_CODEX_FULL_GATE = PENDING
OWNER_LIVE_SEARCH = BLOCKED / NOT AUTHORIZED
PHASE_3_WEBMASTER = BLOCKED
REAL_YANDEX_REQUESTS_DURING_REPAIR_FREEZE_TRANSPORT = 0
```

No refreeze is authorized unless product or package-test bytes change. ChatGPT Actions/browser results cannot substitute for the mandatory independent Codex campaign.
