# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH / CONTROLLED PRE-DELIVERY PASS — OWNER LIVE SEARCH AUTHORIZED**  
Updated: 2026-08-24

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_CHECKPOINT = aad239ce02ee5f88a2922ac0d2c8f7636dfd0a98
PRODUCT_SOURCE = 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
HANDOFF_ARTIFACT = d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16 / 170734 bytes / 65 files / 68 ZIP entries
LATEST_COMPLETE_CODEX_GATE = PASS on exact d58b5bd... candidate
PRODUCTION_BYTES_CHANGED_SINCE_GATE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_GATE = NO
OWNER_LIVE = PENDING / AUTHORIZED
OPEN_BLOCKERS = exactly one minimal real synchronous Search acceptance has not yet returned a usable SEARCH_RESULT_V1
AUTHORIZED_NEXT_STAGE = OWNER_LIVE_PHASE2_SEARCH
```

The live `main` HEAD may legitimately be newer than the checkpoint because documentation/evidence commits advance `main`; always read current metadata before acting.

## Exact frozen product authority

```text
repo: MaksimUnimax/Yandex_direct
product branch: candidate/phase2-search-reconstruction-2026-08-23
product PR: #5
source commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
artifact: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
artifact SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
artifact bytes: 170734
files: 65
ZIP entries: 68
payload manifest bytes: 11421
payload manifest SHA-256: 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
```

No transport, browser-harness, documentation or gate-evidence repair changed frozen product or package-test bytes. No refreeze is required.

## Complete controlled pre-delivery gate — PASS

Durable checkpoint:

```text
extension/tests/PHASE_2_STAGE_4_CODEX_FULL_GATE_PASS_2026-08-24.md
```

Codex returned:

```text
live_main_head_at_gate_start: c1cde115d7ba5c17ab9edf5e8803e77b1d96b8c9
step_0_authority: PASS
transport: PASS
source_suite: 231/231 PASS
packaged_suite: 231/231 PASS
packaged_syntax: 59/59 PASS
packaged_json: 2/2 PASS
browser_project_work: PASS
browser_manual_on_transaction: PASS
browser_search_autorun: PASS
controlled_search_stub_requests: 1
real_yandex_requests: 0
real_credentials_used: NO
production_modified_during_gate: NO
tests_modified_during_gate: NO
final_cleanliness: PASS
not_run_enabled_sections: 0
PD-00..PD-17: ALL PASS
mandatory Manual-ON transaction: PASS
S-00..S-17: ALL PASS
search_phase2 verdict: PASS
failures: []
FINAL VERDICT: PASS
```

This supersedes the earlier Stage-4 stopped attempts as current gate authority. Those attempts remain historical QA-process evidence only.

## Exact QA transport / browser evidence retained

Windows-safe exact transport:

```text
branch: qa/phase2-stage4-final-b64-transport-0ee1d38-2026-08-24
commit: bc7754cff6416ff59942ff6f1052d450792888d5
.gitattributes: * -text
Windows consumer run: 32717179084
job: 97400791303
```

Browser harness:

```text
harness commit: 667fda2f9a0e4197c4873ea96f27862c8453f2f0
Chrome for Testing: 151.0.7922.47
Puppeteer: 25.4.0
independent Windows browser run: 32720334374
job: 97410193364
B-01 PASS
B-02 PASS
B-03 PASS
controlled Search stub requests: 1
real Yandex requests: 0
```

These are retained evidence; the next authorized stage is not another controlled rerun unless new evidence invalidates the PASS.

## Current Phase-2 Search boundary

Enabled first slice:

```text
SEARCH_API_V1
service: search
method: search
POST https://searchapi.api.cloud.yandex.net/v2/web/search
mode: synchronous text WebSearch only
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

## Fresh official pricing check before live acceptance

Freshly checked on 2026-08-24 against the official Yandex Search API pricing page:

```text
https://aistudio.yandex.ru/docs/ru/search-api/pricing.html
```

Current RUB prices, VAT included:

```text
daytime synchronous: 488 RUB / 1000 = 0.488 RUB/request
night synchronous:   366 RUB / 1000 = 0.366 RUB/request
night window:         00:00:00–07:59:59 UTC+3
```

The prepared owner-live request is in the daytime tariff class, so the conservative expected reservation is exactly:

```text
0.488 RUB
```

Requests ending in an internal server error or authentication error are documented as non-billable, but the Bridge must still report `request_executed` truthfully and no ambiguous initiation may be blindly retried.

## Owner-live authority

Canonical procedure:

```text
extension/docs/PHASE_2_0.1.1_LIVE_ACCEPTANCE.md
```

Owner action is intentionally minimal. Controlled UI/runtime regressions are already covered and are not repeated manually.

Required live boundary:

```text
1 real synchronous Search command
→ one external Яндекс action
→ at most one provider initiation
→ one truthful SEARCH_RESULT_V1
→ usable non-empty normalized result list
→ automatic_retry:false
```

Exact prepared query is recorded in `PHASE_2_0.1.1_LIVE_ACCEPTANCE.md`.

If outcome after possible provider initiation is ambiguous (`request_executed:"UNKNOWN"`, timeout/session loss, uncertain delivery), do not click again. Return evidence to ChatGPT for reconciliation.

If a clear pre-network credential/access/policy rejection occurs, classify configuration/access before another live request.

## Stage status

```text
STAGE 1 — Search foundation = PASS / COMPLETED
STAGE 2 — provider/credentials/policy = PASS / COMPLETED
STAGE 3 — Manual/Autorun/operator/delivery integration = PASS / COMPLETED
STAGE 4 — exact refrozen candidate = PASS
STAGE 4 — complete controlled Codex pre-delivery gate = PASS
PHASE 2 — owner-live real Search acceptance = PENDING / AUTHORIZED
PHASE 3 — Webmaster = BLOCKED UNTIL PHASE 2 LIVE PASS
```

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = OWNER_LIVE_PHASE2_SEARCH
```

Do not start Phase 3, refreeze, rebuild, rerun the complete controlled gate, or change product bytes unless owner-live evidence establishes a concrete need.
