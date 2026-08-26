# Documentation index

Canonical documentation for Yandex Marketing Bridge.

## Read first in every current, new and resumed conversation

Before analysis, coding, QA planning, handoff, failure recovery or continuation, reconstruct governed state from live GitHub. Do not use chat memory as authority.

Read in this order:

1. `WORKFLOW_OPERATING_RULES.md` — mandatory ChatGPT/Codex/owner operating contract.
2. `CURRENT_STATE.md` — exact current product/artifact identity, latest gate verdict, owner-live state, blockers and authorized next action.
3. `PROJECT_PURPOSE.md` — product boundary and GitHub/runtime separation.
4. `SPECIFICATION.md` — base technical contract.
5. current phase-specific specification/addenda/implementation plan.
6. `ROADMAP.md` — phase/stage narrative; exact identities remain governed by `CURRENT_STATE.md`.
7. permanent Codex gate/runbook documents.
8. current phase-specific checkpoints/evidence listed in `CURRENT_STATE.md`.
9. append-only context chain when provenance can alter interpretation.

## Current status

Phase 2 synchronous Yandex Search first slice is **LIVE PASS / CLOSED**.

Accepted Phase-2 exact product:

```text
source commit: b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact: yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
artifact SHA-256: ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
artifact bytes: 179013
files: 69
ZIP entries: 72
```

The inter-phase lifecycle button gating patch is now **OWNER LIVE PASS / CLOSED** on:

```text
source commit: 939e880f820e52beae9dcbcedc86d5cd9e13b075
parent: b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact: yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
artifact SHA-256: 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
artifact bytes: 179877
files: 69
ZIP entries: 72
source suite: 247/247 PASS
packaged suite: 247/247 PASS
enabled_not_run_sections: 0
independent Codex verdict: PASS
owner real-profile lifecycle acceptance: PASS
real Yandex requests during controlled QA: 0
real Yandex requests during owner lifecycle acceptance: 0
```

Current transition:

```text
Lifecycle button patch = OWNER LIVE PASS / CLOSED
→ Phase 3 Webmaster = ACTIVE GOVERNED REQUIREMENT RECONSTRUCTION
```

Phase 3 must begin from current official Yandex Webmaster API documentation plus historical repository evidence. Webmaster production implementation is not authorized until its first-slice contract, specification, implementation plan and acceptance/gate requirements are written.

Durable current evidence:

```text
../tests/LIFECYCLE_BUTTON_GATING_FREEZE_2026-08-26.md
../tests/LIFECYCLE_BUTTON_GATING_EXACT_TRANSPORT_PASS_2026-08-26.md
../tests/LIFECYCLE_BUTTON_GATING_BROWSER_PREFLIGHT_2026-08-26.md
../tests/CODEX_LIFECYCLE_BUTTON_GATING_COMPLETE_GATE_HANDOFF_2026-08-26.md
../tests/LIFECYCLE_BUTTON_GATING_CODEX_COMPLETE_PASS_2026-08-26.md
../tests/LIFECYCLE_BUTTON_GATING_OWNER_LIVE_PASS_2026-08-26.md
```

## Authority precedence and conflict rule

1. explicit current owner instruction that intentionally changes workflow/requirement;
2. `WORKFLOW_OPERATING_RULES.md`;
3. `CURRENT_STATE.md`;
4. current living product/gate/live-acceptance contracts and mandatory addenda;
5. `ROADMAP.md`;
6. append-only context/historical evidence.

If current canonical documents materially conflict, stop, reconcile the documents, reconstruct state, then continue.

## Exact-artifact rule

The accepted lifecycle artifact remains the exact bytes that received complete independent gate PASS and owner real-profile PASS. Do not mutate or substitute it. Future product/package-test changes require a new governed candidate.

## Current architectural corrections

- no mandatory `job_id` in extension runtime;
- no GitHub API/workspace runtime dependency;
- all detected errors are delivered regardless of Debug Mode;
- Debug adds redacted diagnostics only;
- settings Export/Import uses integrity validation;
- active RUN/manual safety state survives import rules;
- no blind retry after uncertain provider outcome;
- Manual action is Bridge-owned and independent of native Copy;
- popup geometry is bounded at 430×560 for Chrome 151 native action host;
- factual real ChatGPT conversation ids are accepted without an invalid RFC UUID-version filter;
- identity recovery uses trusted location/canonical candidates and fails closed on conflict;
- Bind availability is separated from already-confirmed identity so context can recover;
- Manual ON follows content acknowledgement before worker authorization;
- lifecycle-blocked Manual action is disabled/non-clickable before user input and re-enabled only after positive lifecycle clear;
- accepted Phase-2 first slice enables only synchronous text `SEARCH_API_V1`.

## Source-of-truth rule

Before any development action or workflow transition: fetch current live `main`, read this index plus `WORKFLOW_OPERATING_RULES.md` and `CURRENT_STATE.md`, inspect applicable current gate/evidence, resolve any conflict, then proceed.
