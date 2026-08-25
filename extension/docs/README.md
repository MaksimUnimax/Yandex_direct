# Documentation index

Canonical documentation for Yandex Marketing Bridge.

## Read first in every current, new and resumed conversation

Before analysis, coding, QA planning, handoff, failure recovery or continuation, reconstruct governed state from live GitHub. Do not use chat memory as authority.

Read in this order:

1. `WORKFLOW_OPERATING_RULES.md` — mandatory ChatGPT/Codex/owner operating contract.
2. `CURRENT_STATE.md` — exact current product/artifact identity, latest gate verdict, owner-live state, blockers and authorized next action.
3. `PROJECT_PURPOSE.md` — product boundary and GitHub/runtime separation.
4. `SPECIFICATION.md` — base technical contract.
5. `SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md` — accepted Phase-2 Search companion.
6. `PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md` — Search requirements, pricing-policy and live-boundary authority.
7. `ROADMAP.md` — phase/stage narrative; exact identities remain governed by `CURRENT_STATE.md`.
8. permanent Codex gate/runbook documents for future candidate regression.
9. current phase-specific checkpoints/evidence listed in `CURRENT_STATE.md`.
10. append-only context chain when provenance can alter interpretation.

## Current status

Phase 2 synchronous Yandex Search first slice is **LIVE PASS / CLOSED**.

Accepted exact product:

```text
source commit: b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact: yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
artifact SHA-256: ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
artifact bytes: 179013
files: 69
ZIP entries: 72
payload manifest SHA-256: ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
```

Independent Codex complete rerun passed all enabled PD/Search/Manual/browser sections with zero real credentials/requests and zero tracked mutation.

Owner real-profile/live Search also passed on the same exact artifact:

```text
request_id: search-392c90df-7440-451b-8b09-d71cdce46720
status: OK
http_status: 200
request_executed: true
automatic_retry: false
response_format: FORMAT_XML
result_count: 5
```

Durable evidence:

```text
../tests/PHASE_2_REAL_PROFILE_BINDING_CODEX_COMPLETE_PASS_2026-08-25.md
../tests/PHASE_2_REAL_PROFILE_OWNER_LIVE_SEARCH_PASS_2026-08-25.md
```

Current transition:

```text
Phase 2 Search = LIVE PASS / CLOSED
→ Phase 3 Webmaster = UNBLOCKED / READY FOR GOVERNED REQUIREMENT RECONSTRUCTION
```

Additional optional owner functional checks against the accepted Phase-2 build may continue. If any exposes a real defect, preserve exact evidence and reopen the proven layer before product mutation.

## Withdrawn/historical candidates

The old `739dd5d7...`, `d58b5bd...` and `0186b35d...` candidates are historical only.

## Authority precedence and conflict rule

The governing order is:

1. explicit current owner instruction that intentionally changes workflow/requirement;
2. `WORKFLOW_OPERATING_RULES.md`;
3. `CURRENT_STATE.md`;
4. current living product/gate/live-acceptance contracts and mandatory addenda;
5. `ROADMAP.md`;
6. append-only context/historical evidence.

If current canonical documents materially conflict, stop, reconcile the documents, reconstruct state, then continue.

## Exact-artifact rule

The accepted Phase-2 artifact remains the exact bytes accepted by the complete independent gate and owner live boundary. Do not mutate or substitute it.

## Current architectural corrections

- no mandatory `job_id` in extension runtime;
- no GitHub API/workspace runtime dependency;
- all detected errors are delivered regardless of Debug Mode;
- Debug adds redacted diagnostics only;
- settings Export/Import uses integrity validation;
- active RUN/manual safety state survives import rules;
- no blind retry after uncertain provider outcome;
- Manual action is Bridge-owned and independent of native Copy;
- popup geometry is bounded for Chrome 151 native action host;
- current ChatGPT identity accepts factual real conversation ids without an invalid RFC UUID-version filter;
- identity recovery uses trusted location/canonical candidates and fails closed on conflict;
- Bind availability is separated from already-confirmed identity so context can be recovered;
- Manual ON follows content acknowledgement before worker authorization;
- accepted Phase-2 first slice enables only synchronous text `SEARCH_API_V1`.

## Source-of-truth rule

Before any development action or workflow transition: fetch current live `main`, read this index plus `WORKFLOW_OPERATING_RULES.md` and `CURRENT_STATE.md`, inspect applicable current gate/evidence, resolve any conflict, then proceed.