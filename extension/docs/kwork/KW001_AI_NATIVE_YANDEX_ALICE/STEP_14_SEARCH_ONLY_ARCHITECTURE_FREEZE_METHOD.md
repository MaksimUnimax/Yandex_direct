# KW-001 — STEP 14 SEARCH-ONLY ARCHITECTURE FREEZE METHOD

Updated: 2026-09-03  
Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-APPROVED**  
Stage: Step14 — freeze the classic-Search architecture before AI evidence.

Companion authorities:

- `RULES_ARCHITECTURE_CODEX_SITE_DISCOVERY_GATE_ADDENDUM_2026-09-02.md`
- `RULES_ARCHITECTURE_CODEX_EXECUTION_RELIABILITY_GATE_ADDENDUM_2026-09-02.md`
- `RULES_ARCHITECTURE_CODEX_EVIDENCE_CONFLICT_PRESERVATION_ADDENDUM_2026-09-02.md`
- `STEP_14_CODEX_BROWSER_FIRST_DISCOVERY_CORRECTION_2026-09-02.md`
- `STEP_14_CODEX_REPOSITORY_SYNC_GATE.md`
- `STEP_14_NO_RUN_SKIP_AND_CRAWLER_REMOVAL_RULE_2026-09-02.md`
- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`
- `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`

Concrete domains, URLs, phrase/page/link counts, action IDs, job artifact paths, commit SHAs and current step state belong in Level-2 evidence.

---

## 1. Step purpose

Step14 freezes the **Search-only** architecture before any AI/Alice/GenSearch evidence can influence the project.

It must reconcile two distinct layers:

```text
A. TARGET SEARCH ARCHITECTURE
   intended owner/responsibility for each accepted user/search task;
   supporting pages/relationships;
   supported structural actions;
   recommended internal links;
   preserved unresolved boundaries.

B. CURRENT AS-IS PUBLIC SITE TOPOLOGY
   current public pages actually discoverable/existing;
   current literal internal HTML/DOM links actually present;
   current reachability/discovery provenance;
   newly discovered pages that may change the accepted model.
```

Canonical rule:

```text
TARGET_SEARCH_ARCHITECTURE != CURRENT_AS_IS_TOPOLOGY
```

A complete Step14 baseline is semantically coherent **and** reconciled against a sufficiently independent current-site discovery/topology pass when completeness/topology is material.

---

## 2. Permanent failure history — what failed, root cause, control

### E14-01 — closed-list completeness fallacy

**Failure:** all known upstream implementation-relevant URLs were reread, and because the known set reconciled cleanly the process treated current architecture coverage as sufficiently complete.

**Root cause:**

```text
UPSTREAM CLOSED URL UNIVERSE
WAS ALLOWED TO
PROVE ITS OWN COMPLETENESS
```

The anti-speculation rule “do not change architecture without evidence” was overextended into “do not independently look beyond upstream URLs.”

**Control:** when acceptance materially depends on current-site completeness, run independent enumerable discovery using the strongest available approved native tool; reconcile every newly discovered relevant URL.

```text
KNOWN_URL_RECHECK != CURRENT_SITE_DISCOVERY
UPSTREAM_INPUT_UNIVERSE != CURRENT_SITE_UNIVERSE
```

### E14-02 — endpoint existence was conflated with literal link implementation

**Failure:** source page existed, target page existed and the relationship was semantically valid; that evidence was reported too close to proving that the current internal link already existed.

**Root cause:**

```text
SHOULD EXIST / RECOMMENDED
AND
DOES EXIST NOW
WERE NOT SEPARATE REQUIRED STATES
```

**Control:** extract/inspect literal current link evidence and store separately:

```text
RECOMMENDATION_STATE
AS_IS_TOPOLOGY_STATE
```

```text
SOURCE_LIVE + TARGET_LIVE + SEMANTIC_FIT != EDGE_IMPLEMENTED
```

### E14-03 — prior stronger project evidence mechanism was not reviewed before designing the step

**Failure:** a prior project stage had already demonstrated a more reproducible discovery/profile pattern, but the Step14 design did not explicitly inspect/reuse that precedent.

**Root cause:**

```text
PRE-STEP REVIEW FOCUSED ON IMMEDIATE UPSTREAM OUTPUTS
BUT NOT ON
EXISTING PROJECT EVIDENCE-ACQUISITION CAPABILITIES
```

**Control:** before inventing a new evidence mechanism ask whether a stronger prior-stage/project mechanism already exists; use it or document why it is unsuitable.

### E14-04 — deterministic requirement was overtranslated into “build a custom crawler”

**Failure:** work drifted from evidence acquisition into collection-infrastructure construction even though a current native browser/tool could satisfy the needed factual observation.

**Root cause:**

```text
MANUAL READING NOT EQUAL COMPLETENESS PROOF
WAS OVERGENERALIZED INTO
CUSTOM CRAWLER REQUIRED
```

**Control:** apply tool-capability-first selection. Define the fact, inspect current native capabilities, choose the simplest reproducible tool that meets coverage/termination/output needs, and use custom code only for a named gap.

### E14-05 — source reachability was mistaken for runner reliability

**Failure:** an isolated successful request was treated as enough confidence to start a broader deterministic run whose queue/parser/finalization behavior had not been qualified.

**Root cause:**

```text
SOURCE REACHABILITY
WAS TREATED AS
FULL RUNNER EXECUTABILITY
```

**Control:** staged qualification from construction/static smoke → one-item runner → bounded mini-run → alternate discovery probe → full run, with heartbeat, hard bounds and terminal state.

### E14-06 — branch name/local checkout was mistaken for current canonical authority

**Failure:** a correctly named local branch could be stale/diverged, causing locally missing files to appear absent from the project.

**Root cause:**

```text
LOCAL BRANCH IDENTITY
WAS TREATED AS
CURRENT REMOTE CONTENT
```

**Control:** fetch exact canonical remote, compare local/remote, preserve local-only evidence, synchronize safely, then perform mandatory authority reads.

### E14-07 — conflict severity was not separated from conflict meaning

**Failure:** all material repository conflicts were treated as one class even when some were losslessly preservable factual evidence and others represented competing project authority.

**Root cause:**

```text
MERGE CONFLICT
WAS TREATED AS
SEMANTIC AUTHORITY CONFLICT
```

**Control:** classify authority conflict, evidence-preservation conflict, byte-identical duplicate, or non-material mechanical conflict; preserve provenance without silently selecting one evidence version.

### E14-08 — obsolete runner lifecycle could be confused with evidence-history lifecycle

**Failure:** replacing/removing an unreliable collector could be mistaken for permission to omit its failed runs.

**Root cause:**

```text
ACTIVE IMPLEMENTATION STATE
WAS NOT SEPARATED FROM
APPEND-ONLY EVIDENCE HISTORY
```

**Control:** obsolete code may be removed/disabled as method requires; every run attempt remains durably recorded.

---

## 3. External method grounding

### Yandex

- site structure: https://yandex.ru/support/webmaster/ru/recommendations/site-structure
- canonical: https://yandex.ru/support/webmaster/ru/robot-workings/canonical
- changing site structure: https://www.yandex.ru/support/webmaster/ru/recommendations/changing-site-structure

Supports clear HTML link/reachability structure and cautious use of redirects/canonical. Overlap/new discovery alone does not justify destructive consolidation.

### Industry corroboration

- Semrush Site Audit crawled pages: https://www.semrush.com/kb/543-site-audit-crawled-pages
- Ahrefs Internal Links: https://ahrefs.com/blog/internal-links-for-seo/

Supports treating discovered URL universe, incoming/outgoing links and crawl depth/topology as distinct evidence dimensions.

The deterministic tool is an evidence mechanism, not an SEO authority.

---

## 4. Correct execution method

### Phase A — load accepted Search-only upstream authorities

Reconcile current accepted Steps 8–13 outputs that govern Search architecture:

```text
phrase/task accounting
page ownership
structural actions
unresolved boundaries
competing-page corrections/limitations
internal-link recommendations
later accepted overlays
```

Never resurrect superseded historical actions merely because they still exist in older files.

```text
LATEST ACCEPTED UPSTREAM STATE = INPUT BASELINE
!= CURRENT-SITE COMPLETENESS PROOF
```

### Phase B — determine whether completeness/topology is material

If final acceptance claims current public-site completeness, material current architecture coverage, exact as-is internal-link state or reconciliation against the actual live site, deterministic/enumerable discovery is required.

If the step only needs a named positive check, a smaller evidence route may be sufficient. The mode must be explicit.

### Phase C — select and qualify the collection tool

```text
FACT TO OBSERVE
→ AVAILABLE NATIVE TOOL
→ COVERAGE / REPEATABILITY / TERMINATION TEST
→ CUSTOM CODE ONLY FOR NAMED GAP
```

If custom/new deterministic code is needed, apply staged execution qualification before the full run.

### Phase D — synchronize repository authority before deterministic execution

Record local/remote state, fetch canonical branch, preserve local-only work, classify any evidence conflicts and only then read mandatory authorities/run current code.

### Phase E — independent current-site discovery

When material, discover through sufficient independent routes, for example:

```text
normal same-site HTML/browser navigation/crawl
public sitemap(s) as an additional route
known accepted URLs for seed/reconciliation
```

Preserve discovery provenance. Sitemap is a supplement, not proof of actual HTML reachability.

### Phase F — build current as-is topology

For fetched/current pages preserve as applicable:

```text
source_url
target_url
literal link/anchor evidence
fetch/final URL state
discovery provenance
crawl/navigation depth
incoming/outgoing internal links
redirect/broken/failure state
```

Do not turn a fetch failure into an absence claim without explicit bounded failure state.

### Phase G — reconcile newly discovered URLs

Every newly discovered URL absent from accepted upstream architecture receives one analytical classification:

```text
ARCHITECTURE_MATERIAL
NON_MATERIAL_WITH_REASON
OUT_OF_SCOPE_WITH_REASON
```

If material:

```text
REOPEN ONLY AFFECTED UNITS/CASES/OWNERSHIP/LINK DECISIONS
→ PRESERVE UNAFFECTED WORK
→ RE-RUN LOCAL QA
```

Discovery alone never authorizes new pages, redirects, canonical changes, merges or deletion.

### Phase H — verify recommended internal edges against current literal evidence

Store recommendation and current implementation separately.

Minimum as-is states:

```text
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
```

`AS_IS_PRESENT` requires literal normalized current link evidence. `AS_IS_ABSENT_PLANNED` means the recommendation survives but the current edge is absent; never report it as implemented.

### Phase I — semantic reconciliation

Deterministic enumeration proves existence/topology facts. The analytical layer checks semantic materiality/responsibility for material pages and edges.

```text
ENUMERATION / HTML FACT != SEMANTIC PAGE RESPONSIBILITY
```

### Phase J — preserve unresolved/destructive-action boundaries

No silent assignment/drop. New discovery does not authorize destructive actions without their qualifying evidence.

### Phase K — persist, read back, freeze

Persist raw/mechanical evidence, reconciliation, final Search-only semantic architecture, QA/report/state and read them back from GitHub before final PASS.

---

## 5. Required output classes

When completeness/topology is material, the current job should preserve equivalent artifacts for:

```text
CURRENT DISCOVERED URL UNIVERSE
CURRENT PAGE/FETCH PROFILE LEDGER
CURRENT INTERNAL LINK GRAPH
UPSTREAM-vs-CURRENT URL RECONCILIATION
REQUIRED/PLANNED EDGE VERIFICATION
UNRESOLVED / BOUNDARY LEDGER
FINAL SEARCH-ONLY SEMANTIC ARCHITECTURE FREEZE
RUN HISTORY / DETERMINISTIC QA when applicable
ANALYTICAL QA
REPORT
CURRENT STATE / JOB FLOW
FINAL GITHUB READBACK
```

Exact job filenames are configurable.

---

## 6. Pass gate

For completeness/topology-material mode:

```text
UPSTREAM_ACCOUNTING_RECONCILED = true
CURRENT AUTHORITY / SAFE SYNC = PASS when code/repo execution involved
DETERMINISTIC OR APPROVED ENUMERABLE DISCOVERY = PASS
REQUIRED OUTPUTS PERSISTED = true
GITHUB READBACK = PASS
CURRENT DISCOVERED URL UNIVERSE MATERIALIZED = true
DISCOVERY ORIGINS PRESERVED = true
NEW RELEVANT URLS RECONCILED = true
UNEXPLAINED RELEVANT DISCOVERED URLS = 0
CURRENT LITERAL INTERNAL LINK STATE MATERIALIZED = true
REQUIRED PLANNED EDGES AS-IS CLASSIFIED = 100%
TARGET ARCHITECTURE SEPARATE FROM CURRENT TOPOLOGY = true
MATERIAL AFFECTED UNITS REOPENED/RECHECKED = true when applicable
UNSUPPORTED NEW PAGE ACTIONS = 0
UNSUPPORTED DESTRUCTIVE ACTIONS = 0
SILENT DROPS = 0
FINAL SEARCH-ONLY FREEZE = PASS
AI EVIDENCE USED IN FREEZE = 0
```

If collection reliability or required current-site coverage is unresolved, Step14 remains blocked/reopened rather than substituting more manual reads and claiming equivalent completeness.

---

## 7. Step boundary

```text
STEP14_COMPLETE
= SEARCH-ONLY ARCHITECTURE FROZEN AGAINST CURRENT ACCEPTED SITE EVIDENCE

STEP14_COMPLETE
!= AI CASES SELECTED
!= AI EVIDENCE ACQUIRED
!= AI VISIBILITY/STABILITY PROVEN
```

Only after final readback may Step15 become the next allowed stage under its own rules.

---

## 8. Permanent markers

```text
KW001_STEP14_METHOD_ACTIVE = true
KW001_STEP14_JOB_SPECIFIC_RESULTS_FORBIDDEN_IN_PERMANENT_METHOD = true
KW001_STEP14_TARGET_ARCHITECTURE_NOT_EQUAL_CURRENT_TOPOLOGY = true
KW001_STEP14_CLOSED_LIST_CANNOT_PROVE_OWN_COMPLETENESS = true
KW001_STEP14_ENDPOINT_EXISTENCE_NOT_EQUAL_EDGE_EXISTENCE = true
KW001_STEP14_RECOMMENDATION_STATE_SEPARATE_FROM_AS_IS_LINK_STATE = true
KW001_STEP14_INDEPENDENT_CURRENT_SITE_DISCOVERY_REQUIRED_WHEN_MATERIAL = true
KW001_STEP14_NATIVE_TOOL_CAPABILITY_REVIEW_BEFORE_CUSTOM_CODE = true
KW001_STEP14_NEW_OR_CHANGED_RUNNER_REQUIRES_QUALIFICATION = true
KW001_STEP14_REMOTE_AUTHORITY_SYNC_REQUIRED_BEFORE_CODE_AUTHORITY_READ = true
KW001_STEP14_EVIDENCE_CONFLICTS_MUST_BE_CLASSIFIED = true
KW001_STEP14_FAILED_RUN_HISTORY_MUST_BE_PRESERVED = true
KW001_STEP14_NEW_DISCOVERY_REOPENS_ONLY_AFFECTED_UNITS = true
KW001_STEP14_NEW_DISCOVERY_DOES_NOT_AUTHORIZE_DESTRUCTIVE_ACTION = true
KW001_STEP14_AI_EVIDENCE_FORBIDDEN_BEFORE_SEARCH_ONLY_FREEZE = true
```

## ПРОСТЫМИ СЛОВАМИ

Step14 нужен, чтобы зафиксировать окончательную картину сайта для обычного поиска до любых AI-проверок. Нельзя считать сайт полностью проверенным только потому, что все уже известные страницы перечитаны, и нельзя считать внутреннюю ссылку установленной только потому, что обе страницы существуют и логично связаны. Поэтому отдельно проверяем реальный текущий сайт и реальные ссылки, сверяем новые находки с уже принятой архитектурой и только после этого замораживаем Search-базу.
