# MK02 STEP 13 — SEARCH-ONLY TARGET ARCHITECTURE / CURRENT-TOPOLOGY RECONCILIATION

## PURPOSE
Freeze the final ordinary-Search architecture against the actual current public site before implementation specifications are prepared.

## WHY THIS STEP EXISTS
An analytically coherent target map can still be wrong if the current site contains pages missed by the upstream closed list, or if recommended page relationships are reported as already implemented without literal link evidence.

## INPUTS
Accepted Steps07–12 outputs; current ownership/actions; current known URL set; client structural constraints; strongest suitable site-discovery/topology mechanism.

## REQUIRED EVIDENCE
Current discovered URL universe sufficient for the architecture claim; current page/fetch profile; literal current internal-link evidence where implementation state matters; discovery provenance; upstream-vs-current reconciliation; newly discovered page classifications.

## METHOD
Keep two layers separate:

```text
TARGET SEARCH ARCHITECTURE
CURRENT AS-IS PUBLIC SITE TOPOLOGY
```

Because completeness/topology is material to MK02, the upstream known URL list cannot prove its own completeness. Review existing proven project tooling first, then choose the simplest reproducible current discovery method that can satisfy coverage/termination needs. Custom crawler/code is allowed only for a named capability gap and must be qualified before a full run.

Independently discover/reconcile current pages through appropriate routes such as current HTML navigation and sitemap as a supplement. Preserve discovery origin. Build literal internal-link state separately from recommended relationships:

```text
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
```

Every newly discovered relevant URL is classified as architecture-material, non-material with reason, or out-of-scope with reason. Material new evidence reopens only affected ownership/action decisions, not the whole project by default.

## OUTPUTS
Current discovered URL universe; current page/fetch profile; current internal-link graph; upstream-vs-current reconciliation; target architecture map; current-vs-target delta; unresolved topology ledger; final Search-only architecture freeze; QA/readback.

## SOURCE KW-001 AUTHORITY
`STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE_METHOD.md` and its discovery/reliability/repository-sync/conflict-preservation companion gates.

## KNOWN FAILURE CLASSES
E14-01 through E14-08 in `ERRORS_AND_LESSONS.md`.

## ROOT CAUSES
Known upstream lists, endpoint existence and one-off tool success were mistaken for current topology/completeness and implementation truth.

## NON-REPEAT CONTROLS
Independent discovery when completeness material; target/as-is separation; literal link evidence; native-tool capability review before custom code; staged runner qualification; current remote authority check; conflict classification; append-only failed-run history; local reopening of affected units when new pages discovered.

## CLAIM BOUNDARIES
```text
KNOWN URL RECHECK != CURRENT SITE DISCOVERY
UPSTREAM URL UNIVERSE != CURRENT SITE UNIVERSE
SOURCE LIVE + TARGET LIVE + SEMANTIC FIT != EDGE IMPLEMENTED
SITEMAP PRESENCE != HTML REACHABILITY
NEW DISCOVERY != PERMISSION FOR DESTRUCTIVE ACTION
TARGET ARCHITECTURE != CURRENT TOPOLOGY
```

AI/Alice/GenSearch evidence is forbidden in this architecture freeze.

## UNKNOWN / BLOCKER BEHAVIOR
If current-site coverage or collection reliability is insufficient for a material completeness/topology claim, Step13 remains blocked/reopened. Do not substitute a weaker manual sample and claim equivalent completeness.

## PASS GATE
Upstream accounting reconciled; independent current discovery PASS where material; current URL universe materialized; new relevant URLs reconciled; literal internal-link state materialized for required edges; target and as-is layers separate; affected units rechecked; unsupported new/destructive actions=0; silent drops=0; AI evidence used=0; final readback PASS.

## CLIENT-FACING MEANING
«Перед ТЗ сверяем целевую структуру с реальным сайтом: какие страницы существуют сейчас, какие связи между ними уже стоят, какие только рекомендуются и не пропустили ли мы важные страницы. Это защищает от ТЗ на создание того, что уже есть, или на ссылку, которая уже реализована иначе.»

---

## OWNER CORRECTION 2026-09-10 — TARGET ARCHITECTURE MUST EXIST BEFORE RECONCILIATION

Target architecture is no longer allowed to emerge mainly by relabelling the existing site.

Mandatory order inside Step13:

```text
1. TAKE ACCEPTED TARGET LANDING SPECS FROM STEP10/11
2. BUILD TARGET PAGE REGISTRY
3. BUILD TARGET HIERARCHY / TREE / PARENT-CHILD RELATIONS
4. FREEZE TARGET PAGE ROLES AND CLUSTER ROUTES
5. ONLY THEN RECONCILE TARGET PAGES WITH CURRENT PUBLIC URLs / TOPOLOGY
6. MATERIALIZE CURRENT→TARGET DELTA
```

The target page registry must contain one row per intended landing page and preserve at least:

```text
TARGET PAGE KEY
PAGE PURPOSE
PAGE TYPE
PRIMARY TASK / INTENT
PRIMARY / REPRESENTATIVE QUERY
MEMBER PHRASE COUNT
TARGET URL OR PROVISIONAL ROUTE
PARENT / SECTION
CHILD / SUPPORTING RELATIONS WHEN MATERIAL
CURRENT URL MATCH
CURRENT MATCH STATE
ACTION STATE
UNCERTAINTY / EVIDENCE BOUNDARY
```

Current-match states may use job-appropriate equivalents:

```text
EXISTING_MATCH
EXISTING_NEEDS_OPTIMIZATION
EXISTING_RELATIONSHIP_CHANGE
NEW_PAGE_CANDIDATE
NO_STANDALONE_PAGE_ROUTE_TO_PARENT
UNRESOLVED
```

A `NEW_PAGE_CANDIDATE` survives only if Step11/12 evidence permits it. This correction does not authorize fabrication of new pages.

The target architecture must also be renderable as a human-readable tree or hierarchical table. A flat list of current URLs with owner labels is not sufficient.

Permanent rules:

```text
CURRENT SITE AS-IS != TARGET ARCHITECTURE SOURCE OF TRUTH
TARGET TREE != CURRENT NAVIGATION TREE
TARGET PAGE REGISTRY != CHANGE-ONLY REGISTER
SMALL CURRENT→TARGET DELTA != SMALL TARGET ARCHITECTURE
```

Additional PASS requirements:

```text
TARGET PAGE REGISTRY COMPLETE FOR ALL MATERIAL STEP10 LANDING SPECS = true
TARGET HIERARCHY/PARENT ROUTE PRESENT FOR ALL MATERIAL TARGET PAGES = true
CURRENT MATCH STATE PRESENT FOR ALL TARGET PAGES = true
TARGET STRUCTURE CAN BE UNDERSTOOD WITHOUT OPENING CURRENT SITE = true
TARGET ARCHITECTURE DERIVED ONLY AS CURRENT-URL INVENTORY + DELTA = FAIL
```

Correct client-facing meaning:

«Сначала фиксируем, какие посадочные страницы и разделы должны существовать исходя из собранного спроса и кластеров. Затем накладываем эту целевую модель на текущий сайт: где нужная страница уже есть, где её нужно доработать, где достаточно оставить всё как есть, а где требуется отдельное решение.»