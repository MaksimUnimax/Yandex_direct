# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY / PHASE 2 ACTIVE CHECKPOINT**  
Updated: 2026-08-19

This file applies immediately in the current conversation and every new/resumed conversation. Always fetch live `main` HEAD before action.

## Repository

```text
repo: MaksimUnimax/Yandex_direct
branch: main
```

## Mandatory QA transport runbook

Before preparing any future Codex pre-delivery prompt, ChatGPT must read and execute:

```text
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

Do not reconstruct QA transport from memory while the proven route remains applicable.

## Phase 1 accepted authority

Exact accepted artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505
files 45
ZIP entries 48
version 0.1.1
```

Critical production hashes:

```text
content_script.js ddf9ed51c60ab90dcdeb1fcd5a1b955c3dd88dfc53a0ddfd5842d66ebe9a02cc
popup.js ac87ad973e8b673bf0c235a43b3dc29dfb67865594ea62e085f943660f0a7ab2
service_worker.js 2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

Previous `31cc5f…` artifact is retired after the owner-live Manual-ON self-revert defect.

Successful exact QA transport authority:

```text
branch: qa/e13a-exact-reconstruction-v3
preimage SHA-256: 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
raw patch SHA-256: 709234433bd446f52a18c95785675d0f5ca3450b82459ce2631d36bdb7269bc2
target manifest: extension/tests/qa_transport/e13a/target-tree-sha256.tsv
canonical packer: extension/tests/qa_transport/e13a/canonical_packer_exact.py
```

Latest complete Codex gate on exact e13a:

```text
PD-00..PD-17: ALL PASS
Manual-ON transaction regression: PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source/package identity: PASS
real Yandex requests: 0
production modified during gate: NO
tests modified during gate: NO
failures: NONE
verdict: PASS
```

Owner real-profile Phase-1 functional acceptance:

```text
getRegionsTree            PASS
getTop                    PASS
getDynamics               PASS after corrected test-command toDate
getRegionsDistribution    PASS
```

Issues #1 and #2 are CLOSED / COMPLETED. Phase 1 Wordstat is LIVE PASS / CLOSED.

## Phase 2 Search authority

Requirements/spec/gate documents:

```text
extension/docs/PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
```

First implementation slice:

```text
protocol: SEARCH_API_V1
service: search
method: search
mode: synchronous text web search
REST endpoint: POST /v2/web/search
response format: FORMAT_XML
result signature: SEARCH_RESULT_V1
```

Explicitly outside first slice:

```text
searchAsync / Operation polling
image search
generative search
HTML normalization
browser scraping of yandex.ru
```

Current tariff snapshot remains documented in the Phase-2 requirement authority; any owner-live paid Search command requires a fresh official price check immediately before execution.

Search must reuse the accepted common Manual/Autorun/outbox/conversation/owner-tab/no-blind-retry core rather than fork delivery logic.

## Resumed Phase-2 foundation checkpoint

Append-only authority:

```text
extension/docs/DEVELOPMENT_CONTEXT_APPEND_ONLY_CONTINUATION_PHASE2_2026-08-19.md
ENTRY 0035
```

Owner resumed work after the earlier pause.

Repository/source authority was rechecked before the first Phase-2 product write. Important finding:

```text
main/extension/src is NOT the byte-complete accepted e13a installable source tree.
```

Current `main/extension/src` contains:

```text
README.md
README.txt
manifest.json
package.json
shared/
```

It does not contain root installable:

```text
content_script.js
popup.js
service_worker.js
```

Therefore Phase-2 code must not be written as though `main/extension/src` were the complete accepted product base.

Exact accepted product-tree authority remains the e13a target identity proven by:

```text
qa/e13a-exact-reconstruction-v3
extension/tests/qa_transport/e13a/target-tree-sha256.tsv
45/45 exact target files
```

Repair lineage evidence:

```text
794531d858b784ee5c6f09e99d87adce476bb863
fix: prevent Manual ON self-revert and add cross-layer regression
```

Search foundation facts reconfirmed from live repository/current Yandex-owned SDK source:

```text
shared/service_registry.js currently registers only WORDSTAT_API_V1 → wordstat
shared/wordstat_protocol.js is the existing protocol/validation/request/report style reference
manifest already permits https://searchapi.api.cloud.yandex.net/*
```

Current Yandex-owned SDK confirms synchronous WebSearch request structure and the enum families needed for strict first-slice validation, including SearchType, FamilyMode, FixTypoMode, SortOrder, SortMode, GroupMode, Localization and FORMAT_XML.

Current SDK XML parser evidence confirms:

```text
UTF-8 XML
<response> → <group> → <doc>
optional url/domain/title/modtime/lang
repeated passage values
invalid/missing optional modtime tolerated
```

No browser/DOM/runtime unknown has been encountered in this foundation work, so no Codex measurement is currently needed.

## Required next engineering action

Before any Phase-2 production change:

```text
1. materialize/reconstruct a byte-exact editable e13a working tree;
2. verify every file 45/45 against target-tree-sha256.tsv;
3. only then create/use the Phase-2 development lineage from that exact verified base;
4. implement smallest Search foundation:
   - service registry registration for search/SEARCH_API_V1;
   - Search protocol/defaults/strict validation;
   - exact synchronous WebSearch request-body builder;
   - Base64 UTF-8 XML normalization;
   - focused tests;
5. run focused/source checks;
6. continue into worker/provider/policy integration only after foundation is green.
```

If a browser/DOM/runtime-state fact becomes unknown:

```text
STOP at that uncertainty
→ do not guess
→ issue a concrete Codex measurement prompt
```

## Current control-plane reconstruction

```text
PRODUCT_SOURCE = accepted Phase-1 e13a bytes; exact editable Phase-2 base still must be materialized and verified 45/45 before editing
HANDOFF_ARTIFACT = e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65 / Phase-1 accepted artifact only
LATEST_FULL_GATE = PASS on exact Phase-1 e13a artifact
PRODUCTION_BYTES_CHANGED_SINCE_GATE = NO
OWNER_LIVE = Phase 1 PASS
OPEN_BLOCKERS = exact editable e13a working-tree materialization + 45/45 verification before first Phase-2 product write
AUTHORIZED_NEXT_STAGE = PHASE_2_EXACT_BASE_MATERIALIZATION_AND_VERIFICATION
CODEX_MEASUREMENT_PENDING = NO
OWNER_ACTION_PENDING = NO
```

## Phase status

```text
PHASE 0 = PASS
PHASE 1 WORDSTAT = LIVE PASS / CLOSED
PHASE 2 YANDEX SEARCH / SERP = REQUIREMENTS + SPEC + GATE READY; ACTIVE; NO PRODUCT CHANGES YET; EXACT BASE MATERIALIZATION NEXT
PHASE 3 WEBMASTER = BLOCKED
PHASE 4 METRIKA = BLOCKED
PHASE 5 DIRECT READ = BLOCKED
PHASE 6 DIRECT DRAFT/PRE-LIVE WRITE = BLOCKED
PHASE 7 DIRECT LIVE WRITE = BLOCKED
PHASE 8 FULL ORDER E2E = BLOCKED
```