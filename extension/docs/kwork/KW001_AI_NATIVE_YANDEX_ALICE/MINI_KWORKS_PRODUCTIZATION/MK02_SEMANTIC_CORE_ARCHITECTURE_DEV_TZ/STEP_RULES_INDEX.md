# MK02 — STEP RULES INDEX

Status: **ACTIVE / RULE LEVEL B INDEX / PER-STEP FILES REQUIRED**

MK02 uses product-local step numbers. Source KW-001 step numbers and MK01 method files are traceability/origin only; the executable MK02 method must be fully materialized in this directory.

## 1. Autonomous execution sequence

| MK02 step | Purpose | Primary source authority | Mode | Required output |
|---|---|---|---|---|
| 00 | Order / scope / structural-constraint freeze | KW-001 Step0 + MK01 Step00 + MK02 `CLIENT_INPUT_CONTRACT.md` | REQUIRED | frozen client/order contract |
| 01 | Current site + business model | KW-001 Step1 + current-site freshness gate + MK01 Step01 | REQUIRED | current scoped business/page vocabulary profile |
| 02 | Wordstat acquisition plan | KW-001 Step2 + MK01 Step02 | REQUIRED | bounded seed/probe manifest |
| 03 | Wordstat acquisition + durable persistence | KW-001 Step3 + persistence/cost gates + MK01 Step03 | REQUIRED | complete occurrence/demand/provenance layer |
| 04 | First conservative triage | KW-001 Step4 + MK01 Step04 | REQUIRED | preliminary scope/noise screening |
| 05 | Targeted second acquisition | KW-001 Step5 + MK01 Step05 | CONDITIONAL | union-compatible evidence for named gaps |
| 06 | Row-level semantic cleanup | KW-001 Step7 corrected method + MK01 Step06 | REQUIRED | explicit state/reason for governed phrases |
| 07 | Semantic freeze / uncertainty routing | KW-001 Step8 + MK01 Step07 | REQUIRED | preserved semantic universe + executable unresolved routes |
| 08 | Targeted ordinary Yandex Search for semantic boundaries | KW-001 Step9 narrow controls + MK01 Step08 | CONDITIONAL | exact observations resolving material semantic ambiguity |
| 09 | Task/intent-first clustering | KW-001 Step10 + MK01 Step09 | REQUIRED | coherent cluster contracts + assignments + semantic QA |
| 10 | Current page ownership / phrase→page mapping | `STEP_11_PAGE_OWNERSHIP_METHOD.md` | REQUIRED | complete phrase/task→page ownership map + unresolved handoff |
| 11 | Structural / content-routing action diagnosis | `STEP_12_STRUCTURAL_ACTION_METHOD.md` + companion gates | REQUIRED | evidence-backed structural actions, no-change states and unresolved actions |
| 12 | Competing-page safety diagnosis | `STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md` | REQUIRED TO MATERIAL CASES | distinct-task/overlap/conflict evidence states sufficient to protect architecture |
| 13 | Search-only target architecture + current-topology reconciliation | `STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE_METHOD.md` + discovery/reliability gates | REQUIRED | current-vs-target architecture freeze + literal-link/topology state |
| 14 | Implementation specification / analytical priority | `STEP_18_PRIORITIZATION_AND_IMPLEMENTATION_READINESS_METHOD.md` + `STEP_18_EXECUTION_TICKET_COMPLETENESS_GATE.md` | REQUIRED | READY / clarification / mapping-only / no-change / hold work packages |
| 15 | Client materialization + final QA / readback | Step19 packaging + Step20 report/workbook/recipient gates | REQUIRED | recipient-ready package + QA/readback |

## 2. Explicit exclusions from base MK02

```text
KW-001 Step5A competitor semantic expansion = MK03 / not base MK02
KW-001 Step6/6A seasonality/coverage extensions = not base unless later versioned decision
KW-001 Steps15–17 AI/Alice/GenSearch = MK06/MK07 / excluded
Google research/tooling = excluded
full standalone historical cannibalization audit = MK04 / not base MK02
website implementation/coding itself = excluded
production schedule with invented owner/effort/capacity = forbidden
```

## 3. Step-boundary invariants

```text
STEP 09 COMPLETE != PAGE OWNER COMPLETE
STEP 10 OWNER DECISION != STRUCTURAL ACTION
STEP 11 ACTION != CANNIBALIZATION PROOF
STEP 12 CURRENT WARNING != HISTORICAL HARM
STEP 13 TARGET ARCHITECTURE != CURRENT TOPOLOGY
STEP 14 IMPLEMENTATION SPEC != PRODUCTION SCHEDULE
STEP 15 MATERIALIZATION != NEW RESEARCH
```

No later step may silently repair a missing upstream evidence decision by invention.

## 4. Mandatory cross-step authorities

Every step also obeys:

- `../YANDEX_ONLY_SCOPE.md`;
- `PRODUCT_SCOPE.md`;
- `CLIENT_INPUT_CONTRACT.md`;
- `GENERAL_RULES.md`;
- `ERRORS_AND_LESSONS.md`;
- parent KW-001 `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`;
- parent persistence/cost/source-to-method/research-to-execution gates as applicable;
- private Yandex access policy where first-party history is considered.

## 5. Required schema of every per-step file

Every `steps/STEP_XX_*.md` must contain equivalent sections:

```text
PURPOSE
WHY THIS STEP EXISTS
INPUTS
REQUIRED EVIDENCE
METHOD
OUTPUTS
SOURCE KW-001 AUTHORITY
KNOWN FAILURE CLASSES
ROOT CAUSES
NON-REPEAT CONTROLS
CLAIM BOUNDARIES
UNKNOWN / BLOCKER BEHAVIOR
PASS GATE
CLIENT-FACING MEANING
```

A line saying only “use KW-001 Step N” is not sufficient.

## 6. Data-work boundary during productization

Until Phase 5 starts, this Level-1 method build must not execute or transform OKNO_MSK semantic/page/action datasets.

```text
PHASE 3–4 = METHOD / RULES / ROADMAP ONLY
PHASE 5 = DATA REHEARSAL IN WORK MODE
```

No Wordstat/Search/provider calls are needed to build the Level-1 method.

## 7. Final MK02 execution meaning

MK02 PASS will mean:

```text
CURRENT YANDEX DEMAND
+ CLEAN TASK CLUSTERS
+ COMPLETE PAGE OWNERSHIP
+ EVIDENCE-BACKED STRUCTURAL DECISIONS
+ COMPETING-PAGE SAFETY BOUNDARIES
+ CURRENT-vs-TARGET ARCHITECTURE RECONCILIATION
+ IMPLEMENTATION-READY SPECIFICATIONS WHERE EVIDENCE IS SUFFICIENT
+ EXPLICIT CLARIFICATION / NO-CHANGE / HOLD WHERE IT IS NOT
+ RECIPIENT-READY CLIENT PACKAGE
```

It will **not** mean that the website changes were implemented, Google was researched, AI/Alice was researched, competitors were exhaustively mined, or a production schedule was calibrated without real implementation inputs.
