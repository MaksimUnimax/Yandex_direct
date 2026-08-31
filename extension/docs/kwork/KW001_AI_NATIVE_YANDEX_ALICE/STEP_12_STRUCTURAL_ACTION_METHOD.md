# Step 12 — Structural action method

Status: **APPROVED / ACTIVE AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA**  
Scope: reusable Step-12 method for deciding what an existing site should keep, strengthen, add, create, split, merge or deliberately not create after phrase-level page ownership has been established.  
Step boundary: structural recommendations only. Real cannibalization diagnosis belongs to Step 13; final Search architecture freeze belongs to Step 14.

## 1. What Step 12 is actually for

Step 12 exists to convert an already cleaned and mapped semantic set into a practical answer to a client's real question:

> **What should be changed on the site, and why?**

The step does not exist merely to attach a label such as `KEEP`, `EXPAND` or `CREATE` to each cluster. A structural action is acceptable only when the analyst can explain the user task, current site state, demand/search evidence that matters, the business truth, the alternative considered, and why the selected structural form is better for the user than the alternatives.

The core relationship is:

```text
EXACT PHRASES
→ COHERENT USER TASK / STRUCTURAL UNIT
→ CURRENT PAGE OR EXPLICIT NO-PAGE STATE
→ DEMAND / SEARCH / BUSINESS EVIDENCE NEEDED FOR THIS DECISION
→ STRUCTURAL ACTION
→ IMPLEMENTATION POSITION IN THE SITE
```

The first OKNO-MSK Step-12 run got the broad idea right but implemented several shortcuts that made the final `PASS` stronger than the evidence justified. Those defects are preserved below because a future analyst must understand **why** the shortcuts failed, not merely memorize a replacement checklist.

---

## 2. External method grounding and what each source actually constrains

### Yandex Webmaster — answer the user's need
https://yandex.ru/support/webmaster/ru/recommendations/targeting

Yandex's guidance makes user need the central unit. This means lexical similarity is only a clue. A page should not become the target merely because its URL/title contains the same word; it must truthfully answer the user's task.

### Yandex Webmaster — site structure
https://yandex.ru/support/webmaster/ru/recommendations/site-structure

Yandex recommends a clear link structure in which each document belongs to a logical section and can be reached by ordinary links. Therefore a proposed new/split page is incomplete if Step 12 records only a slug. The analyst must also know where it belongs and how a user reaches it.

### Yandex Webmaster — presentation / logical splitting
https://yandex.ru/support/webmaster/ru/recommendations/presentation

Yandex recommends splitting information by major logical units rather than small fragments. Therefore a modifier, FAQ question or minor variant is not automatically a separate page. `SPLIT` is justified by a genuinely independent large task/logical unit, not by a convenient keyword token.

### Yandex Webmaster — low-value / low-demand pages
https://yandex.ru/support/webmaster/ru/site-indexing/low-demand

Yandex can exclude pages that duplicate known pages, contain insufficient useful content or do not correspond well to real user queries. Yandex also states there is no quota on useful pages. Therefore Step 12 must avoid both extremes: page inflation and arbitrary page-count caps.

### Yandex Webmaster — useful content
https://yandex.ru/support/webmaster/ru/threat/useless-content

Useful content must solve the user's task and add genuine value. Therefore a new page requires a real useful outcome, not merely a cluster label or a set of search phrases.

### Semrush — Keyword Mapping, 2026-07-27
https://www.semrush.com/blog/keyword-mapping/

The current Semrush workflow groups terms sharing intent, reviews assignments, considers demand/intent/difficulty, maps to a suitable existing page or planned page, and requires checking the suggested URL. This supports using demand and current page fit when deciding whether a standalone page is justified.

### Ahrefs — Keyword Mapping
https://ahrefs.com/blog/keyword-mapping/

Ahrefs groups same/similar-intent terms into one page/topic and distinguishes `Create`, `Optimize`, and `No action`. It also recommends traffic potential plus business potential when choosing topics worth covering. Therefore phrase count alone is not proof that a new page deserves to exist.

### Ahrefs — Keyword Clustering
https://ahrefs.com/blog/keyword-clustering/

SERP similarity can help infer whether queries belong on the same page, but clustering is imperfect. Therefore a mixed or ambiguous cluster must be re-audited rather than being accepted simply because it has an existing cluster ID.

### Rush Analytics — structure / relevant URL / clustering
https://www.rush-analytics.ru/faq/kak-sozdat-strukturu-sayta-na-osnove-semanticheskogo-yadra
https://www.rush-analytics.ru/faq/klasterizaciya-zaprosov-semanticheskogo-yadra-rukovodstvo
https://www.rush-analytics.ru/faq/klasterizaciya/opredelenie-relevantnyh-url-dlya-klasterov

Rush explicitly connects clustered queries, Wordstat frequency, search-result similarity and relevant URLs to the decision whether an existing page should be used or a new page should be created. This supports a structural-unit model rather than independent substring-based routing.

### Semrush — cannibalization, 2026-07-14
https://www.semrush.com/blog/keyword-cannibalization-guide/

Multiple pages ranking for related terms do not automatically constitute cannibalization. Harm must be shown separately. Therefore Step 12 may identify possible overlaps but must not diagnose harmful competition; that remains Step 13.

---

# 3. What the first Step-12 run did, why it seemed reasonable, and why it was insufficient

## Defect 1 — 191 phrase destinations were created as lexical overrides instead of explicit structural units

### What the first run did

After making cluster-level structural decisions, the implementation contained a function that routed individual phrases to already-known pages when certain substrings appeared. Examples included:

```text
"рассроч" / "кредит" -> credit/instalment page
"калькулятор" -> calculator
"частного дома" -> private-house page
"п44" -> P-44 page
"раздвиж" inside aluminium -> sliding aluminium page
"тепл" inside veranda -> warm-veranda page
REHAU model token -> model page
```

This produced 191 phrase-level overrides.

### Why this initially seemed reasonable

The site inventory already proved that those specific pages exist. Many tokens are strong hints: `Grazio` strongly suggests the Grazio product page, and `P-44` strongly suggests the existing P-44 solution page. Reusing an exact existing page is generally better than creating a duplicate page.

### Why this is not good enough

A word match does not prove the role of a page in the search journey. For example, a phrase containing `рассрочка` can still primarily mean "buy this specific product with instalments", where the product page may be the main landing and the finance page only supporting information. The first run silently turned a useful clue into a final primary-page decision.

It also created a maintenance problem: 191 hidden exceptions are not a coherent architecture. A future analyst cannot easily see which phrases form one independent subtask, why that subtask deserves a specific page, or whether the page is primary versus supporting.

### Correct understanding

When a subset of phrases clearly needs a different current page, that subset is evidence that the parent cluster contains a **structural subunit**. The subunit must be made explicit and reviewed as a group.

Correct sequence:

```text
POSSIBLE PHRASE OVERRIDE
→ GROUP SIMILAR OVERRIDES INTO AN EXPLICIT STRUCTURAL SUBUNIT
→ WRITE ITS USER TASK
→ MATERIALIZE ALL MEMBER PHRASES
→ READ / VERIFY THE CANDIDATE PAGE
→ DECIDE PRIMARY VS SUPPORTING ROLE
→ RECORD CONFIDENCE + EVIDENCE
→ THEN ROUTE ALL MEMBER PHRASES
```

Reason: the architecture should explain user tasks, not contain a bag of string rules.

---

## Defect 2 — the full phrase audit still accepted mixed clusters and, in some cases, created pages from them

### What the first run did

It created an audit file listing every phrase under every effective cluster and then selected a structural action at cluster level.

### Why this initially seemed reasonable

This was a major improvement over cluster-label-only reasoning. The analyst could finally see all members before deciding.

### Why it was still insufficient

The existence of a phrase list is not proof that the analyst actually challenged the cluster boundary strongly enough. Several mixed clusters survived the review:

- `WINDOW_INSTALLATION_DIY_INFO` contains PVC-window installation, PVC-door removal/installation, aluminium-window assembly/removal and French-window DIY phrases, yet all were routed to one PVC-window DIY article.
- `PANORAMIC_WINDOWS_COMMERCIAL` contains strong commercial phrases but also architecture/inspiration/object/command-like phrases, yet the complete 73-row set was described as one stable commercial task.
- `GLAZING_PERMISSION_INFO` correctly rejected one generic legal page but did not finish routing the distinct legal subtasks to their proper contexts.
- `WOOD_WINDOWS_COMMERCIAL` contains at least one phrase about **plastic windows in a wooden house**, which is not wooden-window product demand.

### Correct understanding

Phrase-level visibility is only the first half of semantic QA. The second half is asking whether every member truly shares the same terminal task/page expectation.

A mixed cluster cannot be "fixed" by a good structural recommendation. It must first be decomposed into explicit effective structural units or unresolved rows.

Correct sequence:

```text
READ ALL MEMBERS
→ IDENTIFY DISTINCT TERMINAL TASKS / OBJECTS / FORMATS
→ SPLIT INTO STRUCTURAL UNITS OR DEFER AMBIGUOUS ROWS
→ ONLY THEN DECIDE PAGE ACTION
```

Reason: page structure inherits semantic boundaries. If the boundary is wrong, every later `KEEP` or `CREATE` becomes less trustworthy.

---

## Defect 3 — five proposed new pages did not have a dedicated demand/Search evidence matrix

### What the first run did

New pages were mainly justified by phrase count, a narrative that the task was stable, absence of a current owner and the ability to describe useful content.

### Why this initially seemed reasonable

These are all relevant signals. A page should have a distinct task, business relevance and enough useful content. A cluster with dozens of phrases looks stronger than a single accidental query.

### Why it was insufficient

Phrase count is not demand. Forty phrases can be forty low-demand variants; thirteen phrases can represent a commercially important service. Also, a seemingly distinct task can still be served by the same page type in actual search results.

The project already owns Wordstat and ordinary Search evidence, but Step 12 did not materialize it next to each new-page decision. Therefore `HIGH` confidence was not auditable.

### Correct understanding

A new page is a structural investment. Before accepting it, use existing evidence to answer:

```text
What real demand supports the task?
Which phrases carry that demand?
What does ordinary Search show about the expected page/result type?
Does a standalone page pattern exist in the result set?
Can the target business truthfully fulfil the content/service promise?
Can an existing page satisfy the same need by expansion instead?
```

Only unresolved material gaps justify new provider calls; do not buy data merely to make the file look more complete.

---

## Defect 4 — confidence defaulted to HIGH instead of being earned

### What the first run did

The implementation helper had `confidence='HIGH'` as its default value. Unless the analyst manually overrode it, every decision became HIGH.

### Why this initially seemed reasonable

Most decisions were made after full phrase inspection and known page evidence, so it felt natural to treat them as decisive recommendations.

### Why it was wrong

Confidence is supposed to communicate evidence strength. A default value communicates nothing about evidence. It can also hide upstream uncertainty: a decision based on a `MEDIUM` ownership state or a mixed cluster can silently become `HIGH` after Step 12.

### Correct understanding

Confidence must be **derived**, not authored as decoration.

At minimum it must reflect separately observable dimensions:

```text
TASK_COHERENCE
BUSINESS_TRUTH
CURRENT_PAGE_FIT
DEMAND_SUPPORT
SEARCH/SERP_SUPPORT WHEN MATERIAL
STRUCTURAL_ROLE_CLARITY
```

The exact aggregation may be project-configurable, but the source dimensions and downgrade reasons must be visible. Missing evidence cannot produce HIGH merely because no error rule fired.

---

## Defect 5 — important QA checks were self-asserted or checked the wrong thing

### What the first run did

Several QA outputs were constants such as zero or true. Other checks merely verified that a rationale string existed. Most importantly, `split_without_major_logical_task_boundary` equalled the total number of `SPLIT` actions and `merge_based_only_on_suspected_cannibalization` equalled the total number of `MERGE` actions.

### Why this initially seemed reasonable

The script was intended to enforce strong invariants and to fail if forbidden shortcuts appeared.

### Why it was wrong

A QA check is evidence only when it computes or verifies the property it claims. A hard-coded `0` merely repeats the desired outcome. And counting every SPLIT/MERGE as an error makes legitimate SPLIT/MERGE impossible, biasing the result toward zero.

### Correct understanding

Every QA field must have one of three explicit origins:

```text
COMPUTED_FROM_DATA
VERIFIED_FROM_EXECUTION_RECEIPT / PROVENANCE
MANUAL_REVIEW_LEDGER WITH EXPLICIT ROWS
```

A pass gate cannot rely on `ASSUMED = 0` or `ASSUMED = true`.

For SPLIT/MERGE, QA must inspect the evidence attached to each action and count only unsupported actions as failures.

Reason: quality assurance must be independent of the desired result; otherwise it merely certifies the script that created the result.

---

## Defect 6 — Step-13 handoff was manually selected instead of derived from the actual page routing graph

### What the first run did

It marked selected clusters with `step13_followup_required=true` based on analyst judgment.

### Why this initially seemed reasonable

The most obvious overlap families were known: homepage vs REHAU/PVC, broad aluminium vs object pages, broad balcony vs children, etc.

### Why it was insufficient

After the 191 phrase overrides, many source themes were actually distributed across parent, child, utility and model pages. That complete routing graph is the real universe from which Step 13 should select potential overlap checks. A manually curated list can miss less obvious pairs.

### Correct understanding

Step 12 must generate a complete **candidate pair ledger**, not a cannibalization verdict:

```text
semantic/structural unit
page A
page B
why their responsibilities are adjacent/overlapping
phrases/units routed to each
why the overlap may be perfectly normal
whether direct Step-13 Search evidence is needed
```

Reason: Step 13 should begin from a complete candidate universe and then prove or reject harmful competition.

---

## Defect 7 — new-page hierarchy was only partially implementation-ready

### What the first run did

It recorded a proposed slug and a broad `parent_page_or_section` value.

### Why this initially seemed reasonable

The immediate goal was to decide whether the page should exist, not design detailed navigation.

### Why it was insufficient

A page without a clear place in the site's navigation is not a complete structural recommendation. Yandex explicitly stresses link structure and logical sections. Also, informational pages need a clear route back to the relevant commercial action; otherwise they can become isolated content.

### Correct understanding

For each accepted new page, Step 12 must specify:

```text
PARENT URL / SECTION
INBOUND LINK SOURCE(S)
ANCHOR / LINK CONCEPT
OUTBOUND SUPPORT / CHILD LINKS
COMMERCIAL CONVERSION LINK WHEN INFORMATIONAL
BREADCRUMB / NAVIGATION ROLE
```

Reason: architecture is about relationships among pages, not merely URLs.

---

## Defect 8 — mixed `NO_STANDALONE_PAGE` groups were rejected as one page but their useful subparts were not always re-routed

### What the first run did

For groups such as legal/permission queries, it correctly concluded that one generic page would combine unrelated questions. It then wrote prose saying the useful parts should be distributed to relevant contexts.

### Why this initially seemed reasonable

Rejecting a bad combined page was the main structural decision, and the report explained the intended direction.

### Why it was incomplete

A recommendation saying "distribute these later" still leaves phrase-level architecture unfinished. The output must tell us what happens to each usable phrase/subtask now, or explicitly defer it with a reason.

### Correct understanding

`NO_STANDALONE_PAGE` is not the end of analysis when the phrases remain valuable. It branches into:

```text
ROUTE_TO_EXISTING_SECTION/PAGE
CREATE EXPLICIT SUBUNIT FOR LATER EVALUATION
DEFER BECAUSE BUSINESS/LEGAL EVIDENCE IS MISSING
EXCLUDE/OUTSIDE ONLY IF TRULY OUTSIDE
```

Reason: deciding not to create a page does not answer where the user's need will be served.

---

## Defect 9 — some misassigned useful phrases remained trapped inside a rejected cluster

### What the first run did

It correctly rejected a wooden-window commercial page because the product is not verified, but the cluster contained `пластиковые окна в деревянном доме`, which belongs to a different valid task.

### Why this initially seemed reasonable

The overall cluster was clearly unsafe for a new wooden-window page, and the business-truth guard prevented an invented product landing.

### Why it was incomplete

The correct cluster-level rejection hid a valid phrase that should have been rescued into a real existing task/page.

### Correct understanding

Whenever a cluster receives `NO_STANDALONE_PAGE` or `OUTSIDE`, the analyst must still scan for **salvageable in-scope rows** that belong elsewhere.

Reason: "this cluster should not become a page" and "every phrase in this cluster has no valid destination" are different statements.

---

## Defect 10 — the first run used phrase count as a strong narrative signal without materializing frequency/traffic potential

### What the first run did

Descriptions such as "large, stable commercial task" relied partly on the number of member phrases.

### Why this initially seemed reasonable

Many independent phrase variants often signal a real broad topic.

### Why it was insufficient

Phrase count can be inflated by morphology, local variants, repeated price/geo formulations or noisy acquisition patterns. External methods from Semrush, Ahrefs and Rush explicitly use demand/frequency/traffic potential as an additional dimension.

### Correct understanding

Use phrase count for **coverage**, not as a proxy for demand. Demand evidence must come from actual frequency/traffic/search data already acquired for the job.

Reason: architecture should respond to user demand and task distinctness, not vocabulary size alone.

---

## Defect 11 — the output separated Step 12 from Step 13 correctly, but did not make Step-12 uncertainty explicit enough

### What the first run did

It correctly refused to call page overlap cannibalization and deferred conflict diagnosis.

### Why this initially seemed sufficient

The roadmap boundary was respected.

### Why it was still incomplete

Some Step-12 actions depended on unresolved page-boundary questions that were merely marked `step13_followup_required=true` while the structural action itself remained HIGH. This can make a provisional architecture look final before Step 13 checks it.

### Correct understanding

A Step-12 structural recommendation can be:

```text
FINAL_WITHIN_STEP12_EVIDENCE
PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK
DEFERRED_PENDING_MISSING_EVIDENCE
```

These are not three new evidence routes; they are statement-of-certainty/status fields about the recommendation. A provisional action must not be presented as an implementation-ready final action until its named downstream dependency is resolved.

Reason: respecting a later step means preserving the uncertainty that the later step exists to resolve.


## Defect 12 — upstream OUTSIDE/NO-PAGE state can be contradicted by later verified site evidence

### What exposed the failure

During the OKNO-MSK correction, full phrase review found a historical outside-scope family that contained a product for which the current site already had a verified public page. Other rejected/outside groups also contained individual phrases that belonged to valid in-scope tasks.

### Why the old behavior seemed reasonable

Step 12 is downstream from semantic cleanup/clustering/page ownership, so accepted upstream states normally deserve strong deference. Reopening every prior decision without cause would create endless instability.

### Why blind inheritance is wrong

Upstream authority is not stronger than contradictory later evidence. A later step often sees more complete phrase membership, page inventory and structural relationships than the earlier step did. If current first-party evidence proves that the business really offers the product/service, preserving an old `OUTSIDE` label merely because it is historical converts provenance into a correctness claim.

### Correct understanding

```text
UPSTREAM STATE
= accepted input until contradicted

LATER MATERIAL CONTRADICTION
→ preserve original history
→ create explicit correction overlay
→ re-evaluate affected phrase/task
→ verify downstream impact
```

Do **not** reverse every outside/no-page state just because a relevant word appears. The same correction run also demonstrated the opposite case: a window-related phrase can actually target another brand/company and therefore remain outside after disambiguation.

### Non-repeat control

Every Step-12 `OUTSIDE_SCOPE` / `NO_STANDALONE_PAGE` family must receive a salvage/contradiction pass before final acceptance:

```text
CURRENT SITE/OFFER CONTRADICTS OLD OUTSIDE?
USEFUL IN-SCOPE PHRASE TRAPPED IN REJECTED UNIT?
OTHER-BRAND / NAVIGATIONAL PHRASE CORRECTLY OUTSIDE?
UNVERIFIED PRODUCT/SERVICE STILL UNVERIFIED?
```

The result must be explicit per phrase or structural subunit: `SALVAGED`, `DEFERRED`, `OUTSIDE_CONFIRMED`, or `NO_STANDALONE_CONFIRMED`.

Why: the goal is neither to protect old labels nor to rescue everything; it is to preserve the user's real task and the business truth under the newest reliable evidence.

---

# 4. Correct Step-12 working model

A structural action is not chosen directly from `cluster_id` or `ownership_state`.

Correct reasoning chain:

```text
FULL PHRASE SET
→ COHERENT STRUCTURAL UNIT(S)
→ USER TASK AND EXPECTED RESULT
→ BUSINESS TRUTH
→ CURRENT EXISTING PAGE FIT
→ DEMAND EVIDENCE
→ SEARCH/SERP EVIDENCE WHEN IT CAN CHANGE THE PAGE BOUNDARY
→ ALTERNATIVE STRUCTURAL OPTIONS
→ ACTION
→ CONFIDENCE / PROVISIONAL STATUS
→ SITE-HIERARCHY IMPLEMENTATION
→ COMPLETE PHRASE MAP
→ INDEPENDENT QA
```

### Why this order matters

- If coherence is not established first, demand and page evidence are aggregated across different tasks.
- If business truth is not checked before creating a commercial page, the method can recommend products/services the company does not offer.
- If current page fit is not checked before creation, the method creates duplicates.
- If demand/Search evidence is not attached to new-page decisions, a page can be justified by vocabulary size rather than real search behaviour.
- If alternatives are not compared, `CREATE` or `KEEP` can become analyst preference.
- If confidence is chosen before evidence is assembled, confidence becomes cosmetic.
- If hierarchy is added only at the end, a proposed page can become an orphan or duplicate path.
- If full phrase mapping and independent QA are omitted, mixed groups and silent losses remain hidden.

---

# 5. Correct structural action semantics

The exact labels are project mechanics; the principles below are the method.

## KEEP_EXISTING_STRUCTURE

Use when the existing page already serves the coherent task and no material content/structural gap requires a change.

Why not automatic: `OWNER_EXISTING` from Step 11 only means an owner exists, not that its current content is already sufficient for every member need.

## EXPAND_EXISTING_PAGE

Use when the owner is correct but meaningful same-task needs are under-covered.

Why preferable to CREATE: same-task content belongs together unless a distinct page boundary is demonstrated.

## ADD_SECTION_OR_FAQ_TO_EXISTING

Use for a subordinate question/subtask that helps the parent task but lacks independent standalone value.

Why: a useful answer can exist without a new URL; this avoids thin page inflation.

## NEW_COMMERCIAL_PAGE / NEW_INFORMATIONAL_PAGE

Use only when the structural unit is coherent and standalone, the business can truthfully fulfil it, no current page can adequately own it, real demand/search evidence supports the boundary at the confidence claimed, and its site placement is explicit.

Why: `NO_SUITABLE_EXISTING_PAGE` is a gap observation, not proof that filling the gap with a new URL is the best solution.

## SPLIT_EXISTING_PAGE

Use when a current page carries two or more large independent tasks/logical units that should have distinct pages.

Why: users should not have to navigate one page that conflates separate outcomes; however, small modifiers/FAQ fragments are insufficient.

## MERGE_STRUCTURALLY_REDUNDANT_PAGES

Use when current pages are structurally redundant for the same task and one page can truthfully replace them based on content/task evidence. Do not claim search harm unless Step 13 proves it.

Why: redundancy is a structural question; cannibalization is a search-performance diagnosis.

## NO_STANDALONE_PAGE

Use only to say "do not make a separate URL for this unit." Then separately route each useful subtask or explicitly defer it.

Why: absence of a standalone page does not mean absence of a user need.

---

# 6. Correct confidence model

No default HIGH is allowed.

Every action must expose at least:

```text
TASK_COHERENCE = STRONG / PARTIAL / WEAK
BUSINESS_TRUTH = VERIFIED / CONDITIONAL / UNVERIFIED
CURRENT_PAGE_FIT = STRONG / PARTIAL / NONE / NOT_APPLICABLE
DEMAND_SUPPORT = STRONG / PARTIAL / WEAK / NOT_AVAILABLE
SEARCH_BOUNDARY_SUPPORT = STRONG / PARTIAL / WEAK / NOT_NEEDED / NOT_AVAILABLE
HIERARCHY_CLARITY = STRONG / PARTIAL / WEAK
```

Final confidence must be derived from those fields and downgrade reasons must be visible.

Example principle:

```text
UNVERIFIED_BUSINESS_TRUTH -> cannot become HIGH commercial CREATE
WEAK_TASK_COHERENCE -> cannot become HIGH page action
MATERIAL_SEARCH_BOUNDARY_UNKNOWN -> provisional, not final HIGH
```

Do not invent a universal numeric threshold without separate validation. The important rule is evidence-derived confidence, not a cosmetic scoring formula.

---

# 7. Correct QA model

Every QA claim must identify its evidence source.

### Computable accounting checks

```text
ALL_ACTIVE_PHRASES_ACCOUNTED
NO_DUPLICATE_FINAL_PHRASE_ROWS
NO_SILENT_DROPS
EVERY_ASSIGNED_PHRASE_HAS_ONE_FINAL_STRUCTURAL_UNIT
UNRESOLVED_PHRASES_HAVE_NO STRUCTURAL TARGET
```

### Computable structural checks

```text
NEW_PAGE_ROWS_HAVE_EXPLICIT_EVIDENCE MATRIX
NEW_PAGE_ROWS_HAVE_BUSINESS_TRUTH STATE
NEW_PAGE_ROWS_HAVE_HIERARCHY PLAN
OVERRIDE/SUBUNIT PHRASES ARE MATERIALIZED AS UNITS, NOT HIDDEN STRING RULES
```

### Review-led checks

```text
KNOWN_MIXED_UNITS_LEFT_UNCORRECTED
MODIFIER_ONLY_NEW_PAGES
UNSUPPORTED_SPLITS
UNSUPPORTED_MERGES
USEFUL_PHRASES_STRANDED_BY NO_STANDALONE_PAGE
```

These require an explicit review ledger with the rows/cases inspected. They cannot be hard-coded as zero.

### Step-boundary checks

Verify from artifact provenance and fields that no Step-13 harm verdict, Step-14 freeze or AI evidence was introduced. A constant boolean is not evidence.

---

# 8. Correct Step-12 execution order — and why each stage comes next

## Stage 1 — Freeze accepted upstream inputs

Read the final Step-11 phrase map, ownership ledger, corrections, unresolved rows, current site inventory, Wordstat evidence and available ordinary Search evidence.

**Why first:** later structural reasoning is meaningless if it uses stale or superseded inputs.

## Stage 2 — Materialize all current phrase memberships

Build one working view containing every active phrase, current effective cluster, current owner/no-owner state and existing evidence references.

**Why:** the cluster name cannot substitute for its members.

## Stage 3 — Coherence audit before any structural action

For every unit, identify mixed terminal tasks, objects, page formats and obvious misassignments. Create explicit correction/subunit rows; preserve old history rather than rewriting it silently.

**Why before page decisions:** a wrong semantic boundary produces a wrong architecture even if the chosen page looks plausible.

## Stage 4 — Build explicit structural subunits for specialized existing pages

When phrases clearly belong to an existing child/utility/model page, group them into a named subunit with its own task and evidence. Do not route them one-by-one by substring.

**Why:** this converts lexical clues into auditable architecture.

## Stage 5 — Verify business truth

For each proposed commercial/service action, confirm the public site or authorized client evidence shows the product/service is actually offered. Record uncertainty explicitly.

**Why before CREATE:** search demand cannot create a product the business does not sell.

## Stage 6 — Review current page fit

For each structural unit, compare plausible current pages. Decide whether one already serves the task fully, partially or not at all.

**Why before new page evidence:** duplication should be avoided before evaluating creation.

## Stage 7 — Attach demand evidence

Use already collected Wordstat/frequency evidence to show which units have real demand and which phrases drive it. Phrase count remains coverage only.

**Why:** standalone pages are an investment and should not be justified by vocabulary size alone.

## Stage 8 — Attach ordinary Search/SERP evidence where the page boundary is material

Use existing Step-9/Step-11 Search evidence first. If it does not cover a structural boundary that could change a decision, mark a named gap. Only then consider an authorized Bridge request.

**Why:** Search evidence is valuable when it can distinguish one-page vs separate-page expectations; indiscriminate calls waste cost and do not improve every decision.

## Stage 9 — Compare structural alternatives

For each unit explicitly compare viable choices: keep, expand, section, create, split, merge, no standalone page. Record why the selected option beats the alternatives.

**Why:** otherwise action labels become analyst preference.

## Stage 10 — Derive confidence and provisional/final status

Calculate confidence from the evidence dimensions. Mark decisions dependent on Step 13 as provisional rather than final implementation instructions.

**Why:** certainty must reflect what is known now and what is deliberately left for later.

## Stage 11 — Define hierarchy and internal-link role

For each accepted new/split page, specify parent URL/section, inbound link source/concept, relevant outbound links and commercial handoff for informational pages.

**Why:** a page proposal without relationships is not a complete site-structure proposal.

## Stage 12 — Materialize the full phrase→structural-unit→page/action map

Every active phrase must inherit exactly one final structural unit/action or explicit unresolved state. No useful phrase may be stranded because its original cluster was rejected.

**Why:** this is where semantic completeness and structural completeness meet.

## Stage 13 — Generate the complete Step-13 candidate-pair universe

Derive page pairs from the final routing graph. Do not diagnose cannibalization yet.

**Why:** the next step should start from complete possible overlaps, not analyst memory.

## Stage 14 — Independent QA

Compute accounting checks from data, review mixed/action risks through explicit QA ledgers, verify evidence matrices and hierarchy plans, and ensure every claimed pass property has a real derivation.

**Why:** the creator of the recommendation must not be able to pass QA merely by setting expected constants.

## Stage 15 — Persist, read back, then accept

Save all final artifacts to canonical GitHub, read them back, parse/check counts, update job flow/manifest and only then mark Step 12 complete.

**Why:** a correct result that is not durably preserved is not a reusable project result.

---

# 9. Required corrected artifacts

A corrected Step 12 should contain at minimum:

```text
STEP_12_STRUCTURAL_UNIT_CORRECTIONS.tsv
STEP_12_STRUCTURAL_UNITS.tsv
STEP_12_STRUCTURAL_ACTIONS.tsv
STEP_12_NEW_PAGE_EVIDENCE.tsv
STEP_12_PHRASE_ACTION_MAP.tsv
STEP_12_PAGE_ACTION_ROLLUP.tsv
STEP_12_HIERARCHY_PLAN.tsv
STEP_12_STEP13_CANDIDATE_PAIRS.tsv
STEP_12_SEARCH_REQUIRED_HANDOFF.tsv
STEP_12_QA_REVIEW_LEDGER.tsv
STEP_12_QA.json
STEP_12_REPORT.md
```

Historical first-pass artifacts must remain traceable. Corrections should not erase how the first result was produced.

---

# 10. Correct acceptance gate

Step 12 may pass only when:

```text
ALL_ACTIVE_PHRASES_ACCOUNTED = true
ALL_FINAL_STRUCTURAL_UNITS_EXPLICIT = true
HIDDEN_LEXICAL_OVERRIDE_RULES_IN_FINAL_ARCHITECTURE = 0
KNOWN_MIXED_UNITS_LEFT_UNCORRECTED = 0
NEW_PAGE_CANDIDATES_WITHOUT_DEMAND_EVIDENCE = 0 unless DEMAND_NOT_AVAILABLE is explicitly justified
NEW_PAGE_CANDIDATES_WITH_MATERIAL_SEARCH_BOUNDARY_GAP_AND_FINAL_HIGH = 0
COMMERCIAL_CREATE_WITH_UNVERIFIED_BUSINESS_TRUTH = 0
DEFAULT_HIGH_CONFIDENCE = false
CONFIDENCE_WITHOUT_EVIDENCE_DIMENSIONS = 0
QA_SELF_ASSERTED_PASS_FIELDS = 0
UNSUPPORTED_SPLIT = 0
UNSUPPORTED_MERGE = 0
USEFUL_PHRASES_STRANDED_BY_NO_STANDALONE_PAGE = 0
ACCEPTED_NEW_PAGES_WITHOUT_HIERARCHY_PLAN = 0
STEP13_CANDIDATE_UNIVERSE_DERIVED = true
PREMATURE_CANNIBALIZATION_VERDICTS = 0
PREMATURE_SEARCH_ARCHITECTURE_FREEZE = 0
AI_EVIDENCE_USED_EARLY = 0
FINAL_GITHUB_SAVE_AND_READBACK = PASS
```

If an evidence gap prevents a material structural boundary from being resolved, the correct result is not a fabricated PASS. Preserve the provisional/deferred state and execute the named evidence route when authorized.

---

# 11. Plain-language meaning of the method

**Why this step exists:** after collecting and cleaning search demand, we need to turn it into a real plan for the website: what pages stay, what gets improved, what new pages are truly useful, and what pages should not be made at all.

**Why the corrected method is stricter:** the first run sometimes used a matching word as if it proved the right page, treated the number of phrases as if it proved demand, and let the same script both create and certify its own decisions. Those shortcuts can produce a tidy table that looks more certain than the evidence really is.

**How the corrected work should feel:** first understand what people actually mean, then confirm the business really serves that need, then look at the current pages and real search demand, compare the possible website changes, and only after that choose the action. Finally, a separate check tries to find mistakes instead of proving that the chosen answer is correct.


---

# 12. Post-audit defects discovered by fail-closed correction — permanent non-repeat controls

The correction itself exposed additional reusable failure classes after the original external audit. They are part of the final approved Step-12 method because they concern structural integrity and QA mechanics, not one site's vocabulary.

## A. NEW_* action target must be the canonical proposed page

A structural action can change from "best current fallback" to `NEW_COMMERCIAL_PAGE` / `NEW_INFORMATIONAL_PAGE`. When that happens, the primary target must also change to the canonical proposed page. The old current page may remain only as a supporting/current-alternative route.

```text
NEW_PAGE_ACTION
→ CANONICAL_PROPOSED_PRIMARY_TARGET
→ HIERARCHY_OWNER_EXISTS

NEW_PAGE_ACTION
!= EXISTING_FALLBACK_AS_PRIMARY_TARGET
```

Why: otherwise the action label, implementation target and hierarchy describe different pages and downstream graph derivation becomes incomplete.

## B. Implementable page actions require a reviewed primary destination

Any action that tells the implementer to keep, expand, add a section, route a subtask, create a page, or include content in a proposed page must identify the primary destination.

```text
IMPLEMENTABLE_PAGE_ACTION
→ NON_EMPTY_REVIEWED_PRIMARY_TARGET
```

A blank target is not repaired by copying a supporting page or the lexically nearest URL. Re-evaluate exact phrases and page-fit evidence. If no truthful owner exists, change the action to an explicit deferred/no-standalone state instead of inventing a destination.

## C. Human-readable confidence reasons must be regenerated after evidence-state overlays

Hierarchy, Search-boundary state and downstream dependency can change after an initial confidence pass. When structured evidence fields change, the explanation must be regenerated from the **current** state.

```text
CURRENT_EVIDENCE_DIMENSIONS
→ CURRENT_MATURITY
→ CURRENT_CONFIDENCE
→ CURRENT_CONFIDENCE_REASON
```

Resolved evidence must not remain in the downgrade reason. Removing stale wording must not silently strengthen confidence when a real Search/business/Step-13 dependency remains.

## D. QA must use the correct unit of analysis

A QA metric must measure the property it names. Examples of prohibited shortcuts:

```text
UNIQUE_PAGES_CHECKED_BY_COUNTING_OWNER_ROWS
STRUCTURED_JSON_VALIDATED_BY_LITERAL_GREP_OCCURRENCE_COUNT
PAIR_UNIVERSE_VALIDATED_BY_HISTORICAL_LITERAL_PAIR_COUNT
```

Correct controls:

```text
UNIQUE PAGE PROPERTY → UNIQUE NORMALIZED PAGE SET
STRUCTURED STATE → PARSE STRUCTURE AND ASSERT FIELDS
PAIR UNIVERSE → INDEPENDENTLY RECOMPUTE EXPECTED SET AND COMPARE MISSING/EXTRA/DUPLICATE
```

## E. Persist diagnostics before the final PASS/FAIL gate

A failed validator is often the most useful evidence in the correction loop. Therefore diagnostic artifacts must be saved/read back before the workflow exits on the final acceptance gate when doing so is safe and does not falsely mark acceptance.

```text
RUN INDEPENDENT QA
→ SAVE DIAGNOSTIC ARTIFACTS
→ GITHUB READBACK / STRUCTURED PARSE
→ THEN FINAL PASS/FAIL GATE
```

Why: a failure reason that exists only in transient logs/chat can be lost and force paid or analyst work to be repeated.

## F. SPLIT/MERGE QA validates evidence, not action-name presence

The evaluator must be able to accept a supported SPLIT/MERGE and reject an unsupported one. A current job having zero such final actions does not prove the evaluator works. Positive and negative regression controls are required when this failure class is material.

---

# 13. Final reusable Step-12 pass meaning

`STEP12_COMPLETE` means all required structural outputs are durably materialized and independently checked **within Step-12 evidence**. It does not mean Step 13 has validated overlap/cannibalization or Step 14 has frozen final Search architecture.

Canonical boundary:

```text
STEP12_COMPLETE
→ STEP13_MAY_BECOME_NEXT_ALLOWED

STEP12_COMPLETE
!= STEP13_EXECUTED
!= CANNIBALIZATION_PROVEN
!= SEARCH_ARCHITECTURE_FROZEN
```

Markers:

```text
KW001_STEP12_CAUSAL_METHOD_REWRITE_ACTIVE = false
KW001_STEP12_FIRST_PASS_SHORTCUTS_DOCUMENTED = true
KW001_STEP12_HIDDEN_LEXICAL_OVERRIDES_FORBIDDEN = true
KW001_STEP12_STRUCTURAL_UNITS_REQUIRED = true
KW001_STEP12_NEW_PAGE_DEMAND_EVIDENCE_REQUIRED = true
KW001_STEP12_CONFIDENCE_MUST_BE_EVIDENCE_DERIVED = true
KW001_STEP12_QA_MUST_BE_INDEPENDENTLY_DERIVED = true
KW001_STEP12_SPLIT_MERGE_MUST_BE_EVIDENCE_VALIDATED_NOT_ZERO_FORCED = true
KW001_STEP12_NO_STANDALONE_PAGE_REQUIRES_SUBTASK_ROUTING = true
KW001_STEP12_HIERARCHY_PLAN_REQUIRED_FOR_NEW_PAGES = true
KW001_STEP12_STEP13_CANDIDATE_UNIVERSE_MUST_BE_DERIVED = true
KW001_STEP12_FINAL_ACCEPTANCE_PENDING_CORRECTION = false
KW001_STEP12_METHOD_APPROVED_AFTER_INDEPENDENT_QA = true
KW001_STEP12_DIAGNOSTICS_PERSIST_BEFORE_FINAL_GATE = true
KW001_STEP12_DYNAMIC_PAIR_UNIVERSE_QA_REQUIRED = true
KW001_STEP12_IMPLEMENTABLE_ACTION_REQUIRES_PRIMARY_TARGET = true
KW001_STEP12_CONFIDENCE_REASON_MUST_MATCH_CURRENT_STATE = true
```
