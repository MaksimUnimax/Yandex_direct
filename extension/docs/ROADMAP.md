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

**Status: INDEPENDENT CODEX COMPLETE PASS — OWNER REAL-PROFILE/LIVE ACCEPTANCE AUTHORIZED + PENDING.**

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

## Stage 4 — real-profile binding repair

The previous context-recovery candidate failed in the owner's real ChatGPT profile before the provider boundary. The repaired source restored factual real-conversation identity acceptance, trusted canonical fallback, delivered-invalid bootstrap handling, recoverable Bind availability and the proven Manual-ON transaction order.

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

**PASS / COMPLETED.**

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

**PASS / COMPLETED.**

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

## Stage 4C — independent Codex complete gate

The first campaign returned `FAIL_HARNESS` in the obsolete historical Stage-4 popup-open lifecycle. Frozen product bytes were not implicated. ChatGPT reconciled only the QA lifecycle while preserving historical assertions.

Codex then executed a new complete rerun from Step 0 on the **same exact `ce824a9f...` artifact**.

**PASS / COMPLETED.**

```text
campaign: COMPLETE_RERUN_AFTER_STAGE4_HARNESS_RECONCILIATION
transport: PASS
source suite: 244/244 PASS
packaged suite: 244/244 PASS
source syntax: 22/22 PASS
packaged syntax: 63/63 PASS
source JSON: 2/2 PASS
packaged JSON: 2/2 PASS
B-01 Project/Work: PASS
B-02 Manual-ON browser transaction: PASS
B-03 Search Autorun: PASS
PD-00..PD-17: ALL PASS
mandatory Manual-ON transaction: PASS
S-00..S-17: ALL PASS
repair factual real-id late-install: PASS
repair canonical live-receiver: PASS
controlled Search stub requests: 1
real Yandex requests: 0
real credentials used: NO
tracked mutation: NO
final cleanliness: PASS
enabled NOT_RUN: 0
verdict: PASS
```

Durable evidence:

```text
../tests/PHASE_2_REAL_PROFILE_BINDING_CODEX_COMPLETE_PASS_2026-08-25.md
```

No refreeze is required because production/package-test bytes did not change after freeze.

## Final Phase-2 live boundary

**AUTHORIZED / PENDING.**

Current procedure:

```text
PHASE_2_0.1.1_LIVE_ACCEPTANCE.md
```

Owner must use only exact artifact:

```text
yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256: ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
```

Owner acceptance order:

```text
1. verify repaired real-profile ChatGPT detection / Bind / Manual path;
2. if healthy, freshly verify official Yandex Search price/tariff;
3. execute exactly one minimal real synchronous Search request;
4. no blind retry after ambiguous initiation/outcome.
```

On a truthful usable `SEARCH_RESULT_V1` PASS:

```text
PHASE 2 SEARCH FIRST SLICE = LIVE PASS / CLOSED
→ PHASE 3 WEBMASTER may unlock
```

The old `f4aee34... / 739dd5d7...` artifact remains withdrawn. Older `0ee1d38... / d58b5bd...` and `10bb3aca... / 0186b35d...` candidates are historical only.

---

# PHASE 3 — WEBMASTER

**Status: BLOCKED UNTIL PHASE 2 OWNER-LIVE PASS.**

---

# PHASE 4 — METRIKA

**Status: BLOCKED.**