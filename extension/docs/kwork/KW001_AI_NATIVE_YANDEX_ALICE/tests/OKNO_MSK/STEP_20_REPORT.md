# OKNO_MSK — Step20 Final QA report

Date: 2026-09-03  
Step: 20 — Final QA  
Execution status: **COMPLETE**  
Transition verdict: **CORRECTION_REQUIRED / STEP21 BLOCKED**

## Goal and result

Step20 was executed to answer one question: can the exact current Step19 package be handed over safely as the final current version?

Answer: **not yet**.

The mechanical/data/package foundation passed strongly, but the adversarial current-truth and contract checks found **three material defects** that make a final handoff unsafe without correction.

## What passed

### Deterministic package accounting

```text
LOGICAL DELIVERABLES = 9/9
PRIMARY DIRECTIONS = 15 / MAX 15
SEMANTIC ACTIVE ROWS = 2332/2332
UNIQUE PHRASE KEYS = 2332
PRESERVED SEARCH_REQUIRED = 19
AI CASES = 8/8
  CHANGE = 0
  DE_RISK = 4
  NO_CHANGE = 3
  INSUFFICIENT = 1
PAGE ACTIONS = 34/34
EXECUTION PACKAGES = 112/112
  EXACT ACTION = 31
  INTERNAL LINK = 15
  ROUTE TO EXISTING = 46
  HOLD/RECHECK = 20
NON-HOLD = 92
MEASUREMENT CLASSES = 7/7
```

All expected unique IDs/keys reconcile. The workbook's materialized non-README data sheets match the persisted Step19 materialized source files. No silent semantic drop was found.

### Priority and claim boundaries

The package still correctly preserves:

```text
EXPECTED IMPLEMENTATION PRIORITY = PENDING_CALIBRATION
FINAL SPRINT/CALENDAR SCHEDULE = NOT READY
SUPPORTED NEW PAGE ACTIONS = 0
SUPPORTED DESTRUCTIVE ACTIONS = 0
```

No client owner/effort/capacity values were fabricated. No sitewide/longitudinal AI claim, consumer-Alice equivalence, private Webmaster/Metrika observation, or ranking/traffic/lead/revenue guarantee was found.

### Physical identities

The exact persisted package identities match the Step19 manifest:

```text
XLSX = 457647 bytes
SHA-256 = 024966b5959deea16f1d46b3f0d2e89e437fe4bf5756081472b9f67845c910f3

DOCX = 43825 bytes
SHA-256 = 2754e7ba9e332c4cc73a733637e9678ff7bc86731ab8bad690f8f3c6643c61ca

PDF = 59491 bytes
SHA-256 = 0873f6c5f23f2b6d4a6345fde275d523d71df8238d1555cd44ca8b720bfb2145
```

No sensitive comments/tracked changes/external links/macros/embedded payload were found in the inspected Office package structures.

### Current URL/role recheck

Step20 mechanically materialized **48 unique implementation-critical URLs** from the current client/action/execution surfaces. All 48 obtained current public evidence of continued existence and expected page role.

That does not mean every content recommendation remained current: two content-action scopes failed the separate freshness/accuracy check below.

## Material defects

### D20-001 — missing TEST/DEMO identity

The frozen mock order states that this is a mock commercial rehearsal, not an actual paid client engagement, and requires derived portfolio artifacts to be clearly labelled test/demo.

The exact physical XLSX/DOCX/PDF package contains no such disclosure.

Impact: a recipient could mistake a rehearsal/demo package for a real paid-client result.

Required correction: reopen Step19 packaging, add clear test/demo identity to the XLSX README and standalone DOCX/PDF client report/delivery surfaces, rebuild, re-QA and read back the exact physical artifacts.

### D20-002 — S18-A012 door action is partly stale

Current public `https://okno-msk.ru/dveri-rehau/` already materially contains price/price-estimation guidance: price factors, an online-calculator estimate route, free measurer for exact estimates, and installation mention.

`S18-A012` still says to add both door-specific installation scope/process **and price/price-estimation guidance**.

Impact: the client could be instructed to recreate content that already exists.

Required correction: reopen Step18 for current-content calibration of S18-A012/S18-WP-A012. Narrow or close the already-satisfied price portion and preserve only the remaining evidence-supported installation/process gap. Then regenerate the affected Step19 surfaces.

### D20-003 — S18-A027 French definition action is partly stale

Current public `https://okno-msk.ru/okna-rehau/francuzskie-okna/` already gives a concise definition: French glazing in the floor, panoramic floor-to-ceiling construction, plus a dedicated features section.

`S18-A027` still says to add concise definition/naming guidance.

Impact: the recommendation can produce duplicate/low-value explanatory content.

Required correction: reopen Step18 current-content calibration for S18-A027, narrow the action to the remaining naming/distinction gap or merge it with S18-A009, then regenerate the affected Step19 surfaces.

## Minor defect

`D20-004`: DOCX has generic `python-docx` creator metadata and stale 2013 created/modified timestamps inherited from a template. No sensitive person identity is present. This does not block handoff by itself, but should be cleaned during the already-required Step19 rebuild.

## Provider / Bridge accounting

```text
WORDSTAT = 0
SEARCH = 0
GENSEARCH = 0
WEBMASTER = 0
METRIKA = 0
DIRECT = 0
NEW PAID COST = 0 RUB
```

No private provider evidence was acquired.

## Final decision

```text
STEP20 EXECUTION = COMPLETE
QA VERDICT = CORRECTION_REQUIRED
BLOCKING DEFECTS = 0
MATERIAL DEFECTS = 3
MINOR DEFECTS = 1
STEP21_ALLOWED = false
```

Step20 intentionally does not silently repair Step18 or Step19. The affected prior stages must be corrected under a separate owner instruction, then the corrected exact package must return through Final QA before handoff.

## Updated roadmap

| Step | Status |
|---|---|
| 0–17 | ✅ COMPLETE |
| 18 Prioritization/readiness | 🔁 CORRECTION REQUIRED — S18-A012 + S18-A027 current-content calibration |
| 19 Client-facing deliverables | 🔁 CORRECTION REQUIRED — demo/test identity + regenerate affected action/report/package surfaces + DOCX metadata hygiene |
| 20 Final QA | ✅ EXECUTED / VERDICT CORRECTION_REQUIRED |
| 21 Handoff/revisions | ⛔ BLOCKED |
| 22 Job close | ⬜ NOT STARTED |

## Next legal action

`OWNER_AUTHORIZATION_FOR_STEP18_STEP19_CORRECTION_FROM_STEP20_DEFECTS`
