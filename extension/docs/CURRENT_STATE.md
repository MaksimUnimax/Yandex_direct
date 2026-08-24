# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH / STAGE 4 ACTIVE — FROZEN-CANDIDATE PREPARATION**  
Updated: 2026-08-24

Always fetch live `main` HEAD before any transition or control write.

## Current owner instruction

The owner explicitly requires focused development and forbids turning one engineering stage into an endless chain of micro-stages:

- ChatGPT is the developer and owns product/test changes;
- while product bytes are changing, run only focused tests for changed behavior, directly affected regressions and required syntax/static checks;
- do not rerun the complete historical PD/full-suite campaign after every development edit;
- do not keep searching adjacent edge cases after the current stage exit criteria are satisfied;
- the complete combined regression campaign belongs to the frozen pre-delivery candidate in Stage 4;
- no real Yandex request is permitted during controlled development/QA unless the owner explicitly enters owner-live acceptance.

## Transition reconstruction

```text
LIVE_MAIN_HEAD = c6ae089288a49077104d9a941d055889d2fe8985
PRODUCT_BRANCH = candidate/phase2-search-reconstruction-2026-08-23
STAGE3_PRODUCT_HEAD = 75d18291224069a6ae67c110498481ec7320d3c0
STAGE3_WORKER_BLOB = 87b90dcb0a1ecca8afc5587d8ab7f6ddfd2c241a
HANDOFF_ARTIFACT = NONE / NOT YET FROZEN
LATEST_FULL_GATE = Phase-1 historical PASS only; no Phase-2 frozen-candidate full gate yet
PRODUCTION_BYTES_CHANGED_SINCE_PHASE1_GATE = YES
OWNER_LIVE_SEARCH = PENDING
OPEN_PRODUCT_BLOCKERS = NONE PROVEN AT STAGE-3 CLOSURE
AUTHORIZED_NEXT_STAGE = PHASE 2 STAGE 4
```

`main` now contains a permanent read-only focused Phase-2 PR workflow at `.github/workflows/phase2-candidate-gate.yml`. Temporary write transports used during development were removed; the current focused workflow has `contents: read`.

## Repository pointers

```text
repo: MaksimUnimax/Yandex_direct
control branch: main
historical recovery branch: dev/phase2-recovery-work-2026-08-20
clean candidate branch: candidate/phase2-search-reconstruction-2026-08-23
PR: #5 Phase 2 Search reconstruction candidate
initial reconstructed snapshot: 07accfa96aeb1b38d4e882235163bdc136d16a01
Stage-3 production closure: 75d18291224069a6ae67c110498481ec7320d3c0
```

The current candidate is a functional reconstruction with new source bytes. The historical lost final patch was not recovered byte-identically and must not be represented as such.

## Accepted Phase 1 baseline

Phase 1 Wordstat remains LIVE PASS / CLOSED.

```text
accepted artifact SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes: 209505
files: 45
ZIP entries: 48
version: 0.1.1
historical complete full gate: PASS
owner-live Wordstat: PASS for all four supported operations
```

Phase-1 acceptance is historical authority for the accepted `e13a…` bytes, not a pre-delivery PASS for the new combined Wordstat+Search candidate.

## Phase 2 Search boundary

```text
protocol: SEARCH_API_V1
service: search
method: search
endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
mode: synchronous text web search only
response format: FORMAT_XML
normalized result: SEARCH_RESULT_V1
```

Out of scope for the current Search slice:

```text
/v2/web/searchAsync polling lifecycle
image Search
generative Search
HTML SERP normalization
yandex.ru scraping
Webmaster / Metrika / Direct implementation
```

## Stage 1 / Stage 2

```text
STAGE 1 — Search foundation = PASS / COMPLETED
STAGE 2 — worker/provider/credentials/policy = PASS / COMPLETED
```

Their historical evidence remains preserved in the Phase-2 requirement/control documents.

## Stage 3 closure

Stage 3 integrated Search into the common accepted user/runtime surfaces rather than creating a parallel Search-specific DOM/composer FSM.

Current reconstructed functionality includes:

- Search Manual execution through the external Bridge-owned `Яндекс` action;
- Search Autorun through the common RUN lifecycle;
- Project/Work nested ChatGPT route compatibility (`/g/.../c/<uuid>`);
- one immutable service per RUN and Wordstat/Search isolation;
- owner-tab and live-conversation fail-closed checks;
- Manual/Autorun lifecycle ownership controls;
- service-context locking while runtime state is active;
- Manual single-flight and active-operation Manual-mode lock;
- report-prefix owner/live-tab controls;
- future Autorun start-prompt live-tab mutation control;
- Search/Wordstat policy, request and cost guards;
- durable worker-owned outbox and occupied-composer protection;
- primary-runtime outbox reservation and admission blocking while delivery is occupied;
- durable content-error queue with owner and delivery ordering fences;
- committed Send at most once and watch-only committed recovery;
- Manual `REQUESTING` restart recovery with truthful UNKNOWN/no-retry outcome;
- Autorun abandoned `REQUESTING` restart recovery with UNKNOWN/no-retry outcome;
- Autorun `STARTING` restart recovery that recreates a missing `autorun_start` delivery without provider initiation and without duplicating an existing outbox;
- durable `YMB_ERROR_V1` error delivery and diagnostic redaction;
- settings export/import compatibility and runtime safety locks.

Final Stage-3 production fix:

```text
75d18291224069a6ae67c110498481ec7320d3c0
fix: recover missing Autorun start delivery
```

Commit audit proved the production diff touches only `extension/src/service_worker.js`, one recovery-loop hunk.

Final Stage-3 focused verification:

```text
workflow: phase2-focused-development
run: 32703002791
job: 97358197549
merge ref: ae41237a2babd9e2ce77f362bdd6d59551464702
focused tests: 77/77 PASS
fail: 0
service_worker.js syntax: PASS
popup.js syntax: PASS
workflow permission: contents: read
owner-live Search requests: 0
```

Durable evidence:

```text
extension/tests/PHASE_2_STAGE_3_FOCUSED_CHECKPOINT_2026-08-24.md
```

Verdict:

```text
STAGE 3 = PASS / COMPLETED
```

No additional Stage-3 edge-case audit is authorized merely because another hypothetical runtime window can be imagined. Stage 3 reopens only for a proven regression or a Stage-4 failure classified to the product layer.

## Stage 4 — current objective

Stage 4 is now **ACTIVE / AUTHORIZED**.

Required sequence:

```text
1. reconstruct exact current source authority from live GitHub;
2. freeze one exact combined Wordstat+Search candidate;
3. produce production/test hashes and full target manifest;
4. create the deterministic package and prove ZIP/source-package identity;
5. use CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md;
6. prove the Codex-consumed transport by round-trip/consumer-conformance;
7. run one complete combined Phase-1 + Phase-2 pre-delivery regression campaign;
8. if PASS and production bytes remain unchanged, prepare the exact owner artifact;
9. immediately before the paid owner-live Search command, freshly verify official Search pricing;
10. owner executes minimal real Search acceptance one command at a time, with no blind retry.
```

Do not initiate the owner-live paid Search request as a side effect of Stage-4 packaging or controlled QA.

## Current testing mode

Development-focused testing is complete for Stage 3. Stage 4 is the separate pre-delivery boundary. The next broad campaign is therefore not a repeated development gate; it is the one required regression firewall for the exact frozen handoff candidate.
