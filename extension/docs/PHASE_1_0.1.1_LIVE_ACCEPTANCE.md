# PHASE 1 — 0.1.1 OWNER REAL-PROFILE LIVE ACCEPTANCE

Status: **PASS / CLOSED**  
Updated: 2026-08-19.

This document governs only the irreducible owner real-profile/current-production-ChatGPT acceptance that remains after the complete controlled Codex regression gate.

The owner explicitly narrowed the final live scope for this campaign to **functional Yandex tests only**. Standalone UI-only test cases are not required; UI behavior is observed naturally while the real Yandex functional path executes. Tests are given one at a time.

## 1. Exact candidate authority

Only this exact artifact was used for the final owner-live acceptance:

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
size 209505 bytes
files 45
ZIP entries 48
version 0.1.1
```

Production hashes:

```text
content_script.js ddf9ed51c60ab90dcdeb1fcd5a1b955c3dd88dfc53a0ddfd5842d66ebe9a02cc
popup.js ac87ad973e8b673bf0c235a43b3dc29dfb67865594ea62e085f943660f0a7ab2
service_worker.js 2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

The exact artifact had already received a complete controlled Codex pre-delivery PASS:

```text
PD-00..PD-17: ALL PASS
Manual-ON transaction addendum: PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source/package identity: PASS
real Yandex requests during controlled gate: 0
production modified during gate: NO
tests modified during gate: NO
verdict: PASS
```

## 2. Owner-live acceptance scope

Current explicit owner instruction supersedes older broader/manual UI-only acceptance wording for this campaign:

```text
only functional tests involving Yandex
UI observed naturally during those tests
give exactly one test at a time
state what is tested, exact command, exact click
freshly verify official pricing before each executable paid request
no blind retry
```

The required Phase-1 real-Yandex functional operations are:

```text
getRegionsTree
getTop
getDynamics
getRegionsDistribution
```

## 3. Owner-live results

### A. getRegionsTree — PASS

Observed real result:

```text
operation: getRegionsTree
status: OK
http_status: 200
request_executed: true
automatic_retry: false
estimated_rub: 0
charged: false
```

The real region tree was returned successfully.

### B. getTop — PASS

Observed real result:

```text
operation: getTop
status: OK
http_status: 200
request_executed: true
automatic_retry: false
estimated_rub: 0.02
charged: true
phrase: тест
numPhrases: 10
regions: [225]
devices: [DEVICE_ALL]
```

Ten real result rows plus associations and totalCount were returned.

### C. getDynamics — PASS after corrected operator test input

The first owner-live command used:

```text
toDate = 2026-08-01T00:00:00Z
```

Yandex returned HTTP 400 with:

```text
The to field value should be the last day of the month
```

Classification:

```text
layer: PROMPT/EXECUTION INSTRUCTION
product defect: NO
request_executed: true
automatic_retry: false
blind retry: NO
```

The test command was corrected using the established Yandex contract to:

```text
toDate = 2026-07-31T00:00:00Z
```

Corrected real result:

```text
operation: getDynamics
status: OK
http_status: 200
request_executed: true
automatic_retry: false
estimated_rub: 0.02
charged: true
period: PERIOD_MONTHLY
12 monthly result points returned
```

Therefore `getDynamics` owner-live verdict is PASS. The initial 400 is retained as test-instruction evidence, not hidden or reclassified as a product failure.

### D. getRegionsDistribution — PASS

Observed real result:

```text
operation: getRegionsDistribution
status: OK
http_status: 200
request_executed: true
automatic_retry: false
estimated_rub: 0.05
charged: true
region: REGION_REGIONS
```

A real multi-region distribution with count/share/affinityIndex values was returned successfully.

## 4. Live closure of issue #1 — external Yandex action usability

Across multiple sequential newly rendered command blocks in the owner's real production ChatGPT profile, the Bridge-owned `Яндекс` action was present and usable without requiring the native Copy control as the execution trigger. Each owner-authorized click executed exactly the intended Manual/Yandex path and returned the corresponding real result.

The exact candidate had already passed the complete controlled native-Copy lifecycle regression, including real popup Manual state and Copy independence. The final owner instruction did not require a standalone repeat of those already-controlled UI-only cases; naturally observed real-profile Yandex usability showed no live regression during the functional sequence.

Owner-live classification for issue #1:

```text
PASS / COMPLETED
```

## 5. Live closure of issue #2 — sequential Manual lock release

The owner executed multiple distinct Manual Yandex operations sequentially in the same live campaign:

```text
getRegionsTree
→ getTop
→ getDynamics error delivery
→ corrected getDynamics
→ getRegionsDistribution
```

Every subsequent operation was admitted after the prior result/error delivery. No stale `MANUAL_OPERATION_ACTIVE` blocked the next operation. The error-delivery path was followed by a new admitted operation without replaying the prior request automatically.

This directly proves the real-profile sequential Manual release behavior that issue #2 required.

Owner-live classification for issue #2:

```text
PASS / COMPLETED
```

## 6. Final Phase-1 verdict

```text
EXACT ARTIFACT: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
CONTROLLED FULL GATE: PASS
OWNER REAL-PROFILE YANDEX FUNCTIONAL ACCEPTANCE: PASS
ISSUE #1: COMPLETED
ISSUE #2: COMPLETED
PHASE 1 LIVE PASS: TRUE
PHASE 2 SEARCH: UNLOCKED
```

No further Phase-1 paid Wordstat request is required merely to repeat already-passed behavior.

After this PASS, current-state/roadmap authority must record Phase 1 closure and Phase 2 Search as the next allowed service stage.