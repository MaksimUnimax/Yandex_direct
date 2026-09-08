# KW-002 Blood & Sand — STEP 00 ASSORTMENT SCOPE CORRECTION

Date: 2026-09-08  
Status: **CORRECTION APPLIED / STEP 00 PASS RESTORED**

## Owner correction

Latest owner instruction:

```text
USE ONLY OZON PRODUCT CARDS AS THE CLIENT ASSORTMENT INPUT
REASON = Ozon cards are more current for this test and do not duplicate the assortment input
```

## Superseded Step-00 facts

The earlier freeze admitted:

```text
88 WB in-scope rows
20 WB out-of-scope rows
76 Ozon rows
164 in-scope rows before cross-platform reconciliation
```

Those intake counts are superseded for current execution.

## Corrected current truth

```text
AUTHORITATIVE ASSORTMENT SOURCE = Ozon only
OZON PRODUCT/LISTING ROWS = 76
WB PRODUCT/LISTING ROWS ALLOWED IN STEP 01 = 0
CROSS_PLATFORM RECONCILIATION = NOT APPLICABLE
STEP 01 INPUT ROWS = 76
```

WB remains a stated sales channel but not an assortment evidence source for Step 01/02.

## Why Step 00 had to be reopened

The assortment source boundary is a material frozen job input. A later owner correction invalidates dependent Step-01 planning based on 164 rows and cross-platform joins.

```text
MATERIAL INPUT MUTATION
→ INVALIDATE DEPENDENT STEP01 PREVIOUS PLAN
→ UPDATE CLIENT BRIEF / ASSORTMENT MANIFEST / SOURCE WHITELIST
→ REBUILD STEP01 WORK HANDOFF
→ UPDATE JOB MANIFEST / FLOW
→ ONLY THEN RESTORE PASS
```

## QA

```text
client wording unchanged = PASS
ozon 76-row catalog remains preserved = PASS
WB removed from active Step01 source whitelist = PASS
cross-platform join removed from Step01 requirements = PASS
old SEO research remains sealed = PASS
provider calls caused by correction = 0
```

Verdict:

```text
STEP_00_CORRECTION = PASS
STEP_00_CURRENT_VERDICT = COMPLETE / PASS
STEP_01_PREVIOUS_164_ROW_WORK_PLAN = SUPERSEDED
STEP_01_MUST_USE_REBUILT_OZON_ONLY_CONTRACT = true
```