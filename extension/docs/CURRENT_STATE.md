# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH — CONTROLLED PRE-DELIVERY PASS / OWNER LIVE SEARCH AUTHORIZED**  
Updated: 2026-08-25

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_THIS_STATE_WRITE = ec01d3d06dbf95032f7a565cd0b2cd671b8ecbe8
PRODUCT_SOURCE = f4aee34c0a3455aa7199f6aa54bd581c71d97337
HANDOFF_ARTIFACT = 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46 / 175971 bytes / 68 files / 71 ZIP entries
PAYLOAD_MANIFEST = bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478 / 11933 bytes
WINDOWS_SAFE_TRANSPORT = PASS at 7c787eedd9856c3f91fbed85aeaea7f3405ad473
LATEST_COMPLETE_GATE = PASS on exact 739dd5d7... candidate; run 32801788251 / job 97663951211
PRODUCTION_BYTES_CHANGED_SINCE_GATE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_GATE = NO
OWNER_LIVE = PENDING / AUTHORIZED
REAL_OWNER_LIVE_SEARCH_REQUESTS_SINCE_CONTEXT_RECOVERY_DEFECT = 0
OPEN_BLOCKERS = exactly one minimal real synchronous Search acceptance has not yet returned a usable SEARCH_RESULT_V1
AUTHORIZED_NEXT_STAGE = OWNER_LIVE_PHASE2_SEARCH
```

## Exact current candidate authority

```text
candidate branch: candidate/phase2-context-recovery-2026-08-25
product source: f4aee34c0a3455aa7199f6aa54bd581c71d97337
artifact: yandex-marketing-bridge-0.1.1-phase2-search-context-recovery-candidate.zip
artifact SHA-256: 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46
artifact bytes: 175971
files: 68
ZIP entries: 71
payload manifest SHA-256: bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478
payload manifest bytes: 11933
```

The current candidate was produced from the previously accepted popup-fix baseline `10bb3aca...` plus exactly the proven context-recovery production/package-test delta. The old `0186b35d...` and `d58b5bd...` artifacts are historical only and must not be used for owner-live acceptance.

## Exact freeze PASS

Durable authority:

```text
extension/tests/PHASE_2_CONTEXT_RECOVERY_FREEZE_PASS_2026-08-25.md
run: 32799665340
job: 97657914686
source suite: 239/239 PASS
source syntax: 22 PASS
source JSON: PASS
deterministic rebuild: PASS
packaged suite: 239/239 PASS
packaged syntax: 62 PASS
packaged JSON: 2 PASS
ZIP integrity: PASS
real Yandex requests: 0
```

## Windows-safe transport PASS

Durable authority:

```text
extension/tests/PHASE_2_CONTEXT_RECOVERY_WINDOWS_TRANSPORT_PASS_2026-08-25.md
transport branch: qa/phase2-context-recovery-final-b64-transport-f4aee34-2026-08-25
transport commit: 7c787eedd9856c3f91fbed85aeaea7f3405ad473
transport parent: f4aee34c0a3455aa7199f6aa54bd581c71d97337
transport format: YMB_PHASE2_CONTEXT_RECOVERY_EXACT_B64_TRANSPORT_V1
base64 length: 234628
artifact.b64 SHA-256: d72bce6d500582310bd1bda894ac5c57e023f03aa80f9b1ebd79427db4172398
run: 32800990879
Ubuntu producer job: 97661608465 PASS
Windows consumer job: 97661642103 PASS
Windows core.autocrlf=true
exact ZIP roundtrip: PASS
payload manifest roundtrip: PASS
ZIP integrity: PASS
cleanliness: PASS
real Yandex requests: 0
```

## Complete governed gate PASS

Durable authority:

```text
extension/tests/PHASE_2_CONTEXT_RECOVERY_COMPLETE_GATE_PASS_2026-08-25.md
workflow: phase2-context-recovery-complete-gate
QA executor head: fed2ea3dd84164ea91f68ba4bf57b29a4ec0c615
run: 32801788251
job: 97663951211
Windows Server 2025
Git: 2.55.0.windows.4
Chrome for Testing: 151.0.7922.47
Puppeteer: 25.4.0
```

Complete verdict:

```text
step-0 authority: PASS
transport: PASS
source suite: 239/239 PASS
source static: PASS
packaged suite: 239/239 PASS
packaged syntax: 62/62 PASS
packaged JSON: 2/2 PASS
B-01 Project/Work: PASS
B-02 mandatory Manual-ON transaction: PASS
B-03 Search Autorun: PASS
B-04 native Chrome-151 action popup geometry: PASS
B-05 already-open-ChatGPT context recovery: PASS
controlled Search stub requests: 1
real Yandex requests: 0
real credentials used: NO
production modified during gate: NO
tests modified during gate: NO
PD-00..PD-17: ALL PASS
mandatory Manual-ON transaction: PASS
S-00..S-17: ALL PASS
not-run enabled sections: 0
final exactness: PASS
final cleanliness: PASS
COMPLETE_GATE_VERDICT=PASS
PHASE2_CONTEXT_RECOVERY_COMPLETE_GATE_PASS
PHASE2_CONTEXT_RECOVERY_COMPLETE_GATE_ENFORCED_PASS
```

B-05 directly reproduced the owner defect ordering:

```text
ChatGPT opened first
→ unpacked extension installed afterwards
→ original ChatGPT page remained open
→ real extension action triggered
→ real popup opened
→ missing receiver reproduced
→ bootstrap attempted=true
→ bootstrap recovered=true
→ exact conversation identity recovered
→ Bind PASS
→ Manual ON PASS
→ real Yandex requests = 0
```

## Phase-2 Search product boundary remains unchanged

Enabled only:

```text
SEARCH_API_V1
service: search
method: search
POST https://searchapi.api.cloud.yandex.net/v2/web/search
synchronous text Search
FORMAT_XML
SEARCH_RESULT_V1
```

Still locked:

```text
Search async/deferred
Search image
Search generative
HTML SERP normalization
yandex.ru scraping
Webmaster
Metrika
Direct
```

## Owner-live Phase-2 Search acceptance

Exactly one irreducible live synchronous Search request is now authorized on the exact candidate `739dd5d7...`.

Canonical request:

```text
SEARCH_API_V1
{
  "method": "search",
  "queryText": "купить ноутбук",
  "searchType": "SEARCH_TYPE_RU",
  "region": "225",
  "page": 0,
  "groupsOnPage": 5,
  "familyMode": "FAMILY_MODE_MODERATE",
  "fixTypoMode": "FIX_TYPO_MODE_ON",
  "sortMode": "SORT_MODE_BY_RELEVANCE",
  "sortOrder": "SORT_ORDER_DESC",
  "groupMode": "GROUP_MODE_FLAT",
  "docsInGroup": 1,
  "maxPassages": 2,
  "l10n": "LOCALIZATION_RU"
}
```

The owner must click the external `Яндекс` action exactly once.

PASS criteria:

```text
signature: SEARCH_RESULT_V1
service: search
operation: search
status: OK
http_status: 200
request_executed: true
automatic_retry: false
response_format: FORMAT_XML
result.results: non-empty usable normalized result list
```

`url` is the essential document identity; optional title/snippet/domain/modtime may be null.

### No-blind-retry rule

If the result is any of:

```text
request_executed: "UNKNOWN"
timeout after possible provider initiation
session loss after possible provider initiation
ambiguous delivery after the irreversible provider boundary
```

do **not** click again and do **not** retry automatically. Preserve the exact evidence and classify it before any second live request.

A clear pre-network credential/access/policy rejection with `request_executed:false` must be classified as configuration/access versus product before another live request.

A clear provider HTTP error after one initiation with `request_executed:true` and `automatic_retry:false` also must not be retried automatically.

## Governance from here

```text
- do not refreeze or rebuild the candidate;
- do not change production/package-test bytes before owner-live acceptance;
- do not run another complete controlled gate unless new evidence invalidates the PASS;
- exactly one owner-live Search acceptance is the authorized next stage;
- Phase 3 Webmaster remains blocked until owner-live Phase-2 Search is PASS and closed.
```

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = OWNER_LIVE_PHASE2_SEARCH_EXACTLY_ONCE
OWNER_LIVE_SEARCH = PENDING / AUTHORIZED
PHASE_3_WEBMASTER = BLOCKED
```
