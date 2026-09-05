# Step 12 — Final execution protocol

Updated: 2026-09-05  

Date: 2026-08-31  
Status: **APPROVED / ACTIVE / OWNER-REQUESTED / PERMANENT STEP-12 AUTHORITY**

This protocol is the shortest canonical execution order for future Step 12 runs. It exists so that future execution does not reconstruct the method from historical correction artifacts or repeat the false-PASS pattern where an action generated its own evidence.

It must be read together with:

- `STEP_12_STRUCTURAL_ACTION_METHOD.md`
- `STEP_12_EVIDENCE_INDEPENDENCE_AND_CURRENT_CONTENT_VALIDATION.md`
- `STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md`
- `STEP_12_THIRD_AUDIT_EXECUTION_ORDER_CLARIFICATION.md`
- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`

## 1. Step purpose

Step 12 converts accepted phrase/task/page-ownership evidence into a **structural candidate architecture**:

```text
PHRASE
→ COHERENT USER TASK / STRUCTURAL UNIT
→ CURRENT OWNER / NO OWNER
→ STRUCTURAL GAP STATE
→ CONTENT-ENHANCEMENT STATE
→ STRUCTURAL / CONTENT ACTION
→ IMPLEMENTABLE INTERNAL-LINK STATE
→ FULL PHRASE ACTION MAP
→ STEP-13 CANDIDATE-PAIR HANDOFF
```

Step 12 does **not** prove page performance, harmful cannibalization, or final Search architecture.

## 2. Causal order — mandatory

The order below is mandatory. Later states must not be used as evidence for earlier states.

### Stage 1 — freeze inputs and accounting

Read the accepted Step-11 phrase-level map, current job scope, current business/site model, current Wordstat/Search evidence and unresolved rows.

Predeclare:

```text
SOURCE_ACTIVE_PHRASES
EXPECTED_ASSIGNED_OR_EXPLICIT_UNRESOLVED
EXPECTED_OUTPUT_ROWS
```

No silent drops are allowed.

### Stage 2 — build or revalidate coherent structural units

For every unit inspect **all member phrases**, not examples.

Recompute from the phrases:

```text
PRIMARY_OBJECT
OBJECT_SCOPE
USER_ACTION_OR_GOAL
EXPECTED_TERMINAL_RESULT
INTENT_MODE
BUSINESS_SCOPE_STATE
```

A prior unit ID is provenance, not proof of coherence.

If a later content/page review exposes one member that violates the terminal task, reopen the complete materially affected member class. Do not validate only previously known regression literals.

Required control:

```text
KNOWN_REGRESSION_ZERO != GLOBAL_SEMANTIC_COHERENCE_PASS
```

### Stage 3 — refresh current site truth

Before content-changing or new-page actions, read the current first-party pages that could plausibly own the task, including relevant hubs, children, service pages and existing informational/supporting content.

For each material current-page judgment preserve:

```text
CURRENT_URL
CURRENT_PAGE_READ_DATE
CURRENT_PAGE_EVIDENCE
```

Absence in an old inventory is not current absence.

### Stage 4 — establish business truth and owner-goal evidence

Separate public-site evidence from client/internal truth.

Allowed evidence labels must preserve the distinction, for example:

```text
CLIENT_STATED
ANALYTICS_OBSERVED
SALES_SUPPORT_EVIDENCE
PUBLIC_SITE_EXPLICIT
PUBLIC_SITE_INFERRED
UNKNOWN
```

Never rewrite `PUBLIC_SITE_INFERRED` as client policy.

If the public site suggests a policy boundary but client/internal truth is unavailable, report it as **inferred current-site policy**, not as an owner instruction.

### Stage 5 — diagnose structural gap before choosing structural action

Use a structural state independent of the final action:

```text
STRUCTURAL_GAP_STATE =
  NONE
  TOPIC_GAP
  INTENT_GAP
  MIXED_STRUCTURAL_GAP
  STRUCTURAL_EVIDENCE_INSUFFICIENT
```

The selected action must never be an evidence source for the gap.

### Stage 6 — diagnose content enhancement separately

Content quality is a different axis from structural ownership:

```text
CONTENT_ENHANCEMENT_STATE =
  NONE
  QUALITY_GAP
  ORIGINALITY_GAP
  CONTENT_EVIDENCE_INSUFFICIENT
  NOT_ASSESSED
```

A `QUALITY_GAP` requires current-content evidence and explicit uncovered user needs:

```text
MEMBER_USER_NEEDS
NEEDS_ALREADY_COVERED
EXPLICIT_MISSING_NEEDS
WHY_MISSING_NEEDS_ARE_MATERIAL
```

Prohibited circular evidence:

```text
EXPAND was selected
SECTION was selected
current_page_fit = PARTIAL
the action requires fuller coverage
```

unless accompanied by independently observed current-page deficits.

`CONTENT_ENHANCEMENT_STATE = NONE` means only **no content gap was evidenced inside the Step-12 scope**. It does not certify complete originality, quality, conversions or performance.

### Stage 7 — compare existing-content alternatives before CREATE

Mandatory comparison order:

```text
KEEP STRUCTURAL OWNER
→ ROUTE TO EXISTING SPECIALIST / CHILD
→ ADD NARROW SECTION / FAQ
→ EXPAND EXISTING OWNER
→ REFRAME / CONSOLIDATE EXISTING CONTENT
→ ONLY THEN EVALUATE CREATE
```

`NO_SINGLE_OWNER != TOPIC_GAP`.

A new URL is allowed only when a distinct, useful and in-scope task remains after current-site and reuse review.

If any false CREATE is found, re-audit every surviving CREATE candidate in the same run.

### Stage 8 — choose the action from upstream evidence

Possible actions are project-configurable, but the current class includes:

```text
KEEP_STRUCTURAL_OWNER
ROUTE_TO_EXISTING_PAGE_AS_SUBTASK
ADD_SECTION_OR_FAQ_TO_EXISTING
EXPAND_EXISTING_PAGE
SPLIT_EXISTING_PAGE
MERGE_STRUCTURALLY_REDUNDANT_PAGES
NEW_COMMERCIAL_PAGE
NEW_INFORMATIONAL_PAGE
NO_STANDALONE_PAGE
DEFER_PENDING_EVIDENCE
OUTSIDE_SCOPE_NO_ACTION
```

Historical artifacts may retain `KEEP_EXISTING_STRUCTURE`, but its canonical meaning is `KEEP_STRUCTURAL_OWNER` / `KEEP_URL_ROLE`.

It never means:

```text
KEEP_AS_IS
NO_OPTIMIZATION_NEEDED
PERFORMANCE_GOOD
SEO_COMPLETE
```

without separate evidence.

### Stage 9 — preserve Search/SERP evidence boundaries

Where persisted direct Search evidence is material, preserve separately:

```text
INTENDED_TARGET_URL
CURRENT_YANDEX_RELEVANT_URL
RELEVANT_URL_MATCH_STATE
SERP_EXPECTED_CONTENT_TYPE
SERP_EXPECTED_FORMAT
SERP_EXPECTED_ANGLE
```

Do not fabricate format/angle/ranking data that was not observed.

For a structurally accepted content enhancement, fresh targeted SERP/competitor review may still be required later to write a precise implementation brief. Structural acceptance is not permission to invent the best article format or angle.

### Stage 10 — validate internal links from current content

A routing relationship is only a hypothesis.

`IMPLEMENT` requires:

```text
CURRENT SOURCE CONTEXT EXISTS
+ CURRENT TARGET SERVES THE NEXT TASK
+ THE LINK IS USEFUL TO THE USER JOURNEY
```

Preserve:

```text
SOURCE_URL
SOURCE_PAGE_READ_DATE
SOURCE_CONTEXT_EVIDENCE
TARGET_URL
TARGET_PAGE_READ_DATE
TARGET_TASK_FIT_EVIDENCE
USER_NEXT_STEP_HELPFUL
RELATION_TYPE
PLACEMENT_CONTEXT
ANCHOR_CONCEPT
```

Otherwise use an explicit fail-closed state such as:

```text
DEFER_SOURCE_CONTEXT_NOT_MATERIALIZED
DEFER_TARGET_CONTENT_GAP
NOT_APPLICABLE
```

### Stage 11 — distinguish browser-visible and search-visible content

When a recommendation depends on content that may be rendered through JS, images, filters, calculators, galleries or other dynamic surfaces, preserve a visibility state when material:

```text
SEARCH_VISIBLE_CONTENT_EVIDENCE_STATE =
  HTML_OR_SEARCH_ACCESSIBLE_CONFIRMED
  RENDERED_USER_VISIBLE_ONLY
  NOT_CHECKED
```

User-visible content is not automatically proof that the search crawler receives equivalent textual evidence.

This state does not create a technical SEO audit inside Step 12; it limits the strength of structural/content claims when visibility is material.

### Stage 12 — materialize the final canonical master and complete downstream outputs

Start from the accepted correction universe and the current canonical unit/action contracts. Do not patch only the canonical ID.

```text
CORRECTION / FINAL UNIT ID
-> TARGET UNIT CONTRACT
-> REBUILD TASK / INTENT / BUSINESS SCOPE / PAGE ROLE / OWNER / MATURITY
-> FINAL CANONICAL PHRASE→UNIT→PAGE/ACTION MASTER
-> FINAL STRUCTURAL UNITS
-> FINAL STRUCTURAL ACTIONS
-> INTERNAL-LINK ACTIONS
-> MATURITY / DEPENDENCY STATE
-> STEP-13 CANDIDATE-PAIR UNIVERSE
-> DECLARED LATER CONSUMERS
```

Fields independently sourced rather than unit-derived may be preserved only with explicit lineage. Declare the final canonical phrase/structural master and require downstream materializers to consume it; base assignments and overlays remain provenance.

Pair/cannibalization candidates are a **handoff**, not a Step-12 cannibalization verdict.

### Stage 13 — independent adversarial verification

The verifier must recompute upstream claims without using the final action as causal input.

Required adversarial checks include:

```text
FULL PHRASE ACCOUNTING
ALL CORRECTED ROWS MATCH THEIR TARGET UNIT CONTRACT
NO NEW UNIT ID RETAINS OLD UNIT-DERIVED METADATA
CORRECTION UNIVERSE RECONCILES THROUGH EVERY DECLARED CONSUMER
GLOBAL AFFECTED-CLASS SEMANTIC COHERENCE
QUALITY_GAP RECOMPUTATION FROM CURRENT CONTENT + MEMBER NEEDS
CREATE RECOMPUTATION FROM CURRENT SITE + REUSE ALTERNATIVES
IMPLEMENT LINK RECOMPUTATION FROM SOURCE + TARGET CONTENT
PAIR UNIVERSE RECOMPUTED FROM FINAL ROUTING GRAPH
NO CIRCULAR ACTION-DERIVED EVIDENCE
```

A verifier that cannot reject `QUALITY_GAP`, `EXPAND`, `SECTION`, `CREATE` or `IMPLEMENT` is not independent enough.

### Stage 14 — persist diagnostics before acceptance

```text
RUN GENERATOR / ANALYSIS
→ RUN INDEPENDENT QA
→ SAVE DIAGNOSTICS EVEN ON FAIL
→ GITHUB READBACK
→ ONLY THEN FINAL PASS/FAIL GATE
```

A transient log is not durable evidence.

### Stage 15 — closure-state readback

Do not set `STEP12_COMPLETE=true` in the same unverified state transition that creates the closure candidate.

Preferred closure:

```text
PERSIST CLOSURE CANDIDATE
→ READ BACK / PARSE
→ IF PASS, SET COMPLETE
→ PERSIST FINAL STATE
→ FINAL DURABLE READBACK
```

## 3. Reporting semantics

### KEEP

Report:

```text
CURRENT URL REMAINS STRUCTURAL OWNER
```

Do not report `keep as is` unless performance/content evidence separately proves it.

### CREATE = 0

Report:

```text
NO NEW URL IS JUSTIFIED BY THE CURRENT JOB'S AVAILABLE EVIDENCE SCOPE
```

Do not report:

```text
THE SITE HAS NO TOPIC GAPS
THE AUDIENCE HAS NO OTHER NEEDS
```

because CRM, sales calls, support tickets, interviews and private analytics may be absent.

### Performance boundary

Without Webmaster/Metrika/other performance evidence:

```text
STRUCTURAL OWNER CONFIRMED
!= PERFORMANCE OPTIMAL
!= CONTENT FULLY OPTIMIZED
```

### Step-13 boundary

```text
STEP12_COMPLETE
→ STRUCTURAL CANDIDATE ARCHITECTURE + CONFLICT HANDOFF READY

STEP12_COMPLETE
!= HARMFUL CANNIBALIZATION PROVEN
!= FINAL SEARCH ARCHITECTURE FROZEN
```

## 4. Direct external-method authorities

Current sources that constrain this protocol:

- Yandex Webmaster — user-task / quality framework (ЭПОС): https://yandex.ru/support/webmaster/ru/epos
- Yandex Webmaster — site structure: https://yandex.ru/support/webmaster/ru/recommendations/site-structure
- Yandex Webmaster — low-value / low-demand pages: https://yandex.ru/support/webmaster/ru/site-indexing/low-demand
- Yandex Webmaster — duplicate pages: https://yandex.ru/support/webmaster/ru/robot-workings/double
- Semrush — Keyword Mapping (2026): https://www.semrush.com/blog/keyword-mapping/
- Semrush — Content Gap Analysis (2026): https://www.semrush.com/blog/content-gap-analysis/
- Semrush — Content Audit: https://www.semrush.com/blog/content-audit/
- Ahrefs — Keyword Strategy (2026): https://ahrefs.com/blog/keyword-strategy/
- Ahrefs — Internal Links for SEO (2026): https://ahrefs.com/blog/internal-links-for-seo/
- Google Search Central — helpful, reliable, people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content

## 5. Permanent non-repeat markers

```text
KW001_STEP12_FINAL_EXECUTION_PROTOCOL_ACTIVE = true
KW001_STEP12_ACTION_CANNOT_PROVE_ITSELF = true
KW001_STEP12_PRIOR_UNIT_ID_CANNOT_PROVE_COHERENCE = true
KW001_STEP12_KNOWN_REGRESSION_ZERO_NOT_GLOBAL_QA = true
KW001_STEP12_CURRENT_PAGE_READ_REQUIRED_FOR_CONTENT_CHANGES = true
KW001_STEP12_STRUCTURAL_GAP_SEPARATE_FROM_CONTENT_GAP = true
KW001_STEP12_PUBLIC_SITE_INFERENCE_NOT_CLIENT_POLICY = true
KW001_STEP12_KEEP_MEANS_STRUCTURAL_OWNER = true
KW001_STEP12_ZERO_CREATE_IS_SCOPE_LIMITED_CLAIM = true
KW001_STEP12_ROUTING_EDGE_NOT_IMPLEMENTABLE_LINK = true
KW001_STEP12_SEARCH_VISIBLE_CONTENT_BOUNDARY_EXPLICIT_WHEN_MATERIAL = true
KW001_STEP12_INDEPENDENT_VERIFIER_MUST_FALSIFY_DECISIONS = true
KW001_STEP12_DIAGNOSTICS_PERSIST_BEFORE_FINAL_GATE = true
KW001_STEP12_FINAL_MASTER_MUST_JOIN_TARGET_UNIT_CONTRACT = true
KW001_STEP12_IDENTIFIER_ONLY_CORRECTION_FORBIDDEN = true
KW001_STEP12_CORRECTION_UNIVERSE_FORWARD_RECONCILIATION_REQUIRED = true
KW001_STEP12_TWO_PHASE_CLOSURE_READBACK_REQUIRED = true
KW001_STEP12_COMPLETE_NOT_EQUAL_FINAL_SEARCH_ARCHITECTURE = true
```
