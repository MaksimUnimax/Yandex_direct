# ROADMAP v0.9 — Yandex Marketing Bridge

Status: active roadmap.  
Updated: 2026-08-25.

## Governing rule

**One phase = one service = one controlled development closure + one final live acceptance boundary.**

Testing cadence:

```text
during development/change
→ focused tests for changed code + affected dependencies

working candidate frozen for handoff
→ exact artifact preparation through mandatory QA transport runbook
→ one complete independent Codex pre-delivery regression campaign
→ exact package/identity verification
→ owner real-profile/live acceptance only for irreducible live behavior
```

Exact current identities, blockers and authorized next action are authoritative in `CURRENT_STATE.md`.

---

# PHASE 0 — REPOSITORY / REFERENCE / CORE DESIGN

**Status: PASS / CLOSED.**

---

# PHASE 1 — WORDSTAT + UNIFIED CORE

**Status: LIVE PASS / CLOSED.**

Accepted Phase-1 artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes: 209505
files: 45
ZIP entries: 48
```

Controlled gate and owner real-profile functional Wordstat acceptance passed. Phase 1 remains the accepted baseline carried into later combined builds.

---

# PHASE 2 — YANDEX SEARCH / SERP

**Status: REAL-PROFILE BINDING REPAIR FROZEN / WINDOWS TRANSPORT PASS — INDEPENDENT CODEX GATE PENDING — OWNER LIVE BLOCKED.**

## Enabled first slice

```text
protocol: SEARCH_API_V1
service: search
method: search
mode: synchronous text WebSearch only
provider endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
response format: FORMAT_XML
normalized result: SEARCH_RESULT_V1
```

Still locked:

```text
Search async/deferred polling
Search image
Search generative
HTML SERP normalization
yandex.ru scraping
Webmaster
Metrika
Direct
```

## Stages 1–3 — implementation

**PASS / COMPLETED.**

Search protocol/validation, provider/credential/policy guard, exactly-once initiation/no-blind-retry behavior, XML normalization, Manual/Autorun integration, conversation ownership and durable delivery remain implemented and covered by the controlled suite.

## Stage 4 — reopened real-profile binding repair

The previous context-recovery candidate reached a ChatGPT-owned controlled PASS but then failed in the owner's real ChatGPT profile before the provider boundary. The old claim that this internal Actions run was the required independent Codex complete gate was invalid and has been revoked.

The repair restored factual real-conversation identity acceptance, trusted canonical fallback, delivered-invalid bootstrap handling, recoverable Bind availability and the proven Manual-ON transaction order.

Clean repaired product source:

```text
source branch: candidate/phase2-real-profile-binding-repair-2026-08-25
source commit: b7869180c229356a6b3d51ac980ec3da5df4c23c
parent: f4aee34c0a3455aa7199f6aa54bd581c71d97337
```

Exact delta: four production files plus two package-test files, one commit total.

Repair preflight:

```text
fail-first: 5 expected failures
focused affected suite after fix: 37/37 PASS
complete source suite after fix: 244/244 PASS
controlled factual-id/canonical Chrome 151 scenarios: PASS
real Yandex requests: 0
```

## Stage 4A — exact freeze

**PASS / COMPLETED (ChatGPT-owned packaging/preflight, not Codex).**

```text
freeze run: 32805530317
freeze job: 97674800575
artifact: yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256: ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes: 179013
files: 69
ZIP entries: 72
payload manifest SHA-256: ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
payload manifest bytes: 12125
source suite: 244/244 PASS
packaged suite: 244/244 PASS
deterministic rebuild: PASS
real Yandex requests: 0
```

The Actions artifact was downloaded back and the exact inner ZIP, manifest and archive integrity were independently round-trip verified.

## Stage 4B — exact Windows-safe transport

**PASS / COMPLETED (transport proof only).**

```text
transport commit: 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
transport run: 32805811476
Windows job: 97675604279
OS: Windows Server 2025
Git: 2.55.0.windows.4
core.autocrlf: true
exact B64 reassembly: PASS
exact ZIP identity: PASS
payload manifest identity: PASS
ZIP integrity: PASS
clean checkout: PASS
real Yandex requests: 0
```

Repair-specific browser harness is pinned externally at:

```text
commit: 81625e073d507d70451f1457185a3e906c640c66
blob: 790539464d7f72214a3126c6585aac74e1afec39
```

## Stage 4C — mandatory independent Codex complete gate

**READY / PENDING.**

Exact handoff:

```text
../tests/CODEX_PHASE_2_REAL_PROFILE_BINDING_REPAIR_FULL_GATE_HANDOFF_2026-08-25.md
```

Required outcome before owner-live can unlock:

```text
transport exactness = PASS
source + packaged complete suites = PASS
PD-00..PD-17 = ALL PASS
mandatory Manual-ON transaction = PASS
S-00..S-17 = ALL PASS
repair factual real-id late-install browser scenario = PASS
repair canonical live-receiver browser scenario = PASS
real Yandex requests = 0
real credentials used = NO
no product/test/harness mutation
no enabled NOT_RUN
verdict = PASS
```

Until Codex returns that complete PASS:

```text
OWNER LIVE SEARCH = BLOCKED
```

## Final Phase-2 live boundary

The live procedure remains `PHASE_2_0.1.1_LIVE_ACCEPTANCE.md`, but it is **not currently authorized**.

After independent Codex complete PASS, re-check the current official Yandex synchronous Search price/tariff window and authorize exactly one minimal real synchronous Search request.

On a truthful usable `SEARCH_RESULT_V1` PASS:

```text
PHASE 2 SEARCH FIRST SLICE = LIVE PASS / CLOSED
→ PHASE 3 WEBMASTER may unlock
```

If provider initiation may have happened but outcome is ambiguous, no blind retry is allowed.

The old `f4aee34... / 739dd5d7...` artifact remains withdrawn. Older `0ee1d38... / d58b5bd...` and `10bb3aca... / 0186b35d...` candidates are historical only.

---

# PHASE 3 — WEBMASTER

**Status: BLOCKED UNTIL PHASE 2 OWNER-LIVE PASS.**

---

# PHASE 4 — METRIKA

**Status: BLOCKED.**

---

# PHASE 5 — DIRECT READ

**Status: BLOCKED.**

---

# PHASE 6 — DIRECT DRAFT / PRE-LIVE WRITE

**Status: BLOCKED.**

---

# PHASE 7 — DIRECT LIVE WRITE

**Status: BLOCKED.**

---

# PHASE 8 — FULL ORDER E2E

**Status: BLOCKED.**

---

# Current status summary

```text
PHASE 0  PASS / CLOSED
PHASE 1  WORDSTAT LIVE PASS / CLOSED
PHASE 2  REPAIR FROZEN / WINDOWS TRANSPORT PASS / INDEPENDENT CODEX PENDING / OWNER LIVE BLOCKED
PHASE 3  BLOCKED UNTIL PHASE 2 LIVE PASS
PHASE 4  BLOCKED
PHASE 5  BLOCKED
PHASE 6  BLOCKED
PHASE 7  BLOCKED
PHASE 8  BLOCKED
```
