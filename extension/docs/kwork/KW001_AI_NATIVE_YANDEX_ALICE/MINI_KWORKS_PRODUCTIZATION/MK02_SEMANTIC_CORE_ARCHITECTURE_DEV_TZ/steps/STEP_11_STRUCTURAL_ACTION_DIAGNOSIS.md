# MK02 STEP 11 — STRUCTURAL / CONTENT-ROUTING ACTION DIAGNOSIS

## PURPOSE
Convert accepted page-ownership evidence into supported structural/content-routing decisions: what should stay as structural owner, what should be strengthened/routed/split/merged/created, what requires no physical site change, and what remains unresolved.

## WHY THIS STEP EXISTS
`NO_SUITABLE_EXISTING_PAGE`, a large cluster, or a convenient action label can easily become an unsupported CREATE/SPLIT/MERGE recommendation. MK02 must compare alternatives and prove why a real site change is required before handing anything to implementation.

## INPUTS
Step10 phrase→page map; task/cluster authority; current page/content evidence; demand evidence; Search evidence where material; client business/change constraints; current link/page relationships.

## REQUIRED EVIDENCE
Current owner/page fit; current content coverage/reuse evidence; demand/user-task evidence; Search result type/format/angle when material; owner/business-goal evidence source; alternative-action comparison; contradiction review.

## METHOD
For each effective task/unit separate diagnosis from prescription:

```text
STRUCTURAL GAP STATE
CONTENT ENHANCEMENT STATE
CURRENT OWNER / COVERAGE STATE
REAL SITE CHANGE REQUIRED = YES | NO | UNRESOLVED
```

Compare viable alternatives before selecting action. Before surviving CREATE, perform a fresh current-site existence/content-reuse audit. Before rejecting a unit, salvage any in-scope member/subtask. Preserve owner-goal evidence strength. A correct current owner may still need content improvement, but `KEEP_STRUCTURAL_OWNER` is not a performance claim. Every material later contradiction reopens all affected members and downstream consumers.

Allowed equivalent outcomes include:

```text
KEEP CURRENT STRUCTURAL OWNER
STRENGTHEN / EXPAND CURRENT PAGE
ROUTE SUPPORTING TASK
SPLIT MATERIAL TASKS
MERGE / CONSOLIDATION CANDIDATE
CREATE NEW PAGE
NAVIGATION / INTERNAL-LINK CHANGE
SEMANTIC MAPPING ONLY / NO SITE CHANGE
DEFER / NEEDS EVIDENCE
```

Action wording never acts as its own evidence.

## OUTPUTS
Structural/content diagnosis ledger; evidence-backed action authority; no-change/mapping-only states; dependencies/relationships; unresolved/deferred items; correction impact map; QA.

## SOURCE KW-001 AUTHORITY
`STEP_12_STRUCTURAL_ACTION_METHOD.md` plus evidence-independence, global-coherence and correction companion gates.

## KNOWN FAILURE CLASSES
M12-01 through M12-25 in `ERRORS_AND_LESSONS.md`.

## ROOT CAUSES
Lexical clues, cluster size, historical inventories, action labels and existing unit IDs were repeatedly treated as stronger than current user-task/page/business evidence.

## NON-REPEAT CONTROLS
Explicit diagnosis before action; no default HIGH confidence; current-content reuse before CREATE; owner-goal source field; alternative comparison; full-member salvage; action-evidence independence; atomic propagation after correction; independent global-coherence review.

## CLAIM BOUNDARIES
```text
PHRASE COUNT != NEW PAGE VALUE
NO EXACT OWNER != CONTENT GAP
NO SUITABLE OWNER != CREATE
KEEP OWNER != PAGE OPTIMIZATION PASS
ACTION LABEL != DIAGNOSIS
ACTION DESCRIPTION != EVIDENCE
```

No destructive action is considered final merely because it is structurally plausible; Step12 competing-page safety may still bound or reopen it.

## UNKNOWN / BLOCKER BEHAVIOR
Missing material current-page/business/Search evidence produces provisional/deferred state. Missing company-specific facts are not invented. If later evidence contradicts the unit boundary, reopen all affected members and rebuild impacted outputs.

## PASS GATE
Every action traces to independent evidence; all surviving CREATE candidates pass current existence/reuse audit; no rejected unit strands valid in-scope phrases; action confidence earned; `REAL SITE CHANGE REQUIRED` explicit; correction impact propagated; known-defect regression + global coherence QA PASS.

## CLIENT-FACING MEANING
«После распределения тем по страницам отдельно проверяем, действительно ли сайт нужно менять. Где текущая страница уже подходит — это фиксируется как нормальный результат; новую страницу, разделение или объединение рекомендуем только когда это подтверждено, а не потому что так удобнее разложить ключи.»

---

## OWNER CORRECTION 2026-09-10 — ACTION DELTA MAY NOT REPLACE THE TARGET PAGE SPEC

Step11 now consumes the target-first landing map from corrected Step10.

For every target landing page/task, Step11 must preserve two independent outputs:

```text
A. TARGET PAGE SPECIFICATION STATE
what page should own the demand and what role it has in the intended structure

B. CURRENT→TARGET ACTION STATE
what, if anything, must physically change on the current site
```

A small action delta is allowed. A small **deliverable** is not.

Mandatory action-state equivalents:

```text
CREATE
OPTIMIZE / STRENGTHEN
ROUTE / INTERNAL-LINK CHANGE
KEEP / LOCK AS TARGET OWNER
NO_STANDALONE_PAGE — INCLUDE WITHIN PARENT
RECHECK / NEEDS EVIDENCE
```

`KEEP / LOCK AS TARGET OWNER` means the current page matches the independently designed target role. It must retain the target-page specification and remain visible to the client even though `REAL SITE CHANGE REQUIRED = NO`.

`NO_STANDALONE_PAGE` is also a positive routing decision: the cluster/task remains mapped to the parent/owner page and must not disappear from the target architecture.

Permanent rules:

```text
NO SITE CHANGE != OMIT PAGE FROM TARGET SPEC
KEEP != NOTHING TO DELIVER
ACTION DELTA != FULL PRODUCT RESULT
TARGET PAGE ROLE != IMPLEMENTATION CHANGE TICKET
```

Additional PASS requirements:

```text
EVERY TARGET LANDING SPEC FROM STEP10 HAS STEP11 ACTION STATE = true
KEEP/NO_CHANGE TARGET PAGES DROPPED FROM DOWNSTREAM = 0
NO_STANDALONE CLUSTERS WITHOUT EXPLICIT PARENT ROUTE = 0
ACTION REGISTER CAN BE SMALL; TARGET PAGE REGISTER MUST REMAIN COMPLETE
```

Correct client-facing meaning:

«Сначала фиксируем полную целевую рассадку. Затем для каждой целевой страницы определяем, что делать с текущим сайтом: создать страницу, доработать существующую, изменить связи, оставить её как правильную посадочную или включить тему в более широкую страницу. Даже когда менять ничего не нужно, клиент всё равно получает зафиксированное назначение страницы и её семантику.»