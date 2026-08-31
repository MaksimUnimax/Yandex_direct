# Step 12 — Structural action method

Status: **CLOSURE CANDIDATE AFTER D12-28..D12-30 EVIDENCE-INDEPENDENCE + GLOBAL-COHERENCE CORRECTION — FINAL STATE READBACK PENDING**  
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

## 1.1 Second-audit lesson: reading the right material is not enough unless it becomes an executable gate

The owner challenge after the first corrected Step-12 closure exposed a deeper process failure. Before Step 12, the analyst had already read external material saying to review existing pages, use business relevance and avoid unnecessary new content. The work still produced false CREATE recommendations.

### Why this happened despite correct research

The research was treated as **background guidance**, while the implementation/QA only enforced the controls that had been translated into explicit fields and fail-closed checks. Two critical ideas remained narrative instead of executable gates:

```text
FRESH CURRENT-SITE EXISTENCE CHECK IMMEDIATELY BEFORE CREATE
OWNER BUSINESS GOAL / DESIRED USER OUTCOME BEFORE CONTENT-STRATEGY ACTION
```

Therefore the process could honestly say "we considered current page fit" while still inheriting an old inventory absence, and could honestly say "business truth verified" while still recommending content that helps users avoid a paid core service.

Permanent lesson:

```text
CORRECT RESEARCH != EXECUTABLE CONTROL
METHOD PRINCIPLE WITHOUT FIELD/GATE/FAIL CONDITION = EASY TO SKIP
```

Every material external-method conclusion must be converted into one or more of:

- an explicit evidence field;
- a mandatory execution stage;
- a fail-closed QA check;
- a named manual owner-challenge case.

For current-site freshness, the universal authority is `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`.

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


### Second external audit — business goal, content reuse and freshness

Additional current sources after the owner challenge:

- Semrush, *Keyword Mapping*, 2026-07-27 — page maps become stale; check/open existing URLs; optimize existing pages before creating new ones; prioritize business relevance + demand.  
  https://www.semrush.com/blog/keyword-mapping/
- Semrush, *Content Audit*, 2026-05-04 — evaluate current content against explicit business goals before creating more content.  
  https://www.semrush.com/blog/content-audit/
- Semrush, *Content Marketing Strategy*, 2026-08-19 — search demand informs strategy but does not dictate that every searched topic should become an article; content must connect to a business objective.  
  https://www.semrush.com/blog/content-marketing-strategy-guide/
- Ahrefs, *Keyword Strategy*, updated 2026-03-13 — SEO goals shape prioritization; business potential is independent of rankability/traffic; low-business-potential topics may attract the wrong audience.  
  https://ahrefs.com/blog/keyword-strategy/
- Ahrefs, *Keyword Research / Business Potential* — traffic potential and intent are insufficient without asking what ranking is worth to the business.  
  https://ahrefs.com/seo/keyword-research
- Ahrefs, *Product-led Content* — useful informational content should naturally connect the user's problem with the product/service when that supports the strategy; reuse/update strong existing content instead of unnecessary duplication.  
  https://ahrefs.com/blog/product-led-content/
- Yandex Webmaster duplicate/low-demand guidance — duplicate or insufficiently distinct pages can waste crawl resources and create search ambiguity.  
  https://yandex.ru/support/webmaster/ru/site-indexing/low-demand  
  https://yandex.ru/support/webmaster/en/yandex-indexing/about-doubles

These sources add three mandatory distinctions:

```text
BUSINESS_TRUTH != OWNER_BUSINESS_GOAL_ALIGNMENT
PAGE_OWNERSHIP_GAP != CURRENT_CONTENT_GAP
OLD_INVENTORY_ABSENCE != CURRENT_PAGE_ABSENCE
```

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


## Defect 16 — false panoramic CREATE because old absence was treated as current absence

### What the corrected run did

It proposed `PROPOSED_NEW:/panoramnye-okna/` after Step 11 had not verified a broad panoramic owner.

### Why it seemed reasonable

The accepted inventory contained panoramic balcony pages, a panoramic article and related object pages, but not a broad commercial panoramic landing. Strong Wordstat demand and a coherent commercial core made a new page look like a legitimate gap fill.

### Why it was wrong

Fresh current-site discovery later found `https://okno-msk.ru/okna-rehau/panoramnoe-osteklenie/`, a full commercial page with price, order/measurement CTA, product options, installation and warranty. CREATE would have manufactured a duplicate.

### Why the earlier research did not prevent it

The method said "review current page fit", but QA did not require a **fresh timestamped existence search immediately before every CREATE**. The analyst inherited Step-1/Step-11 absence as if it were a current fact.

### Permanent correction

```text
NEW_PAGE_CANDIDATE
→ FRESH CURRENT-SITE DISCOVERY
→ SYNONYM / ALTERNATIVE SLUG / FAMILY CHECK
→ OPEN + READ PLAUSIBLE EXISTING PAGES
→ ONLY THEN CREATE CAN SURVIVE
```

Reason: a false CREATE can create the duplicate/overlap problem that later steps are supposed to diagnose.

---

## Defect 17 — installation DIY search opportunity conflicted with the owner's commercial outcome

### What the corrected run did

It proposed a step-by-step self-installation article because demand was strong and observed Search results were informational guides.

### Why it seemed reasonable

The user task was real, demand was strong, the company has installation expertise, and informational SERPs supported the format. Under an SEO-only model, the evidence looked strong.

### Why it was wrong

The live site sells professional installation, explicitly discourages self-installation and explains technical/safety risks. A neutral enabling tutorial could help the user avoid the paid service the site is built to sell.

### Why the earlier research did not prevent it

`BUSINESS_TRUTH` was interpreted as "the company can truthfully/expertly discuss this topic". That is not the same as "ranking for this topic in this format advances the owner's goal". No explicit `OWNER_PRIMARY_GOAL`, `DESIRED_USER_OUTCOME`, `BUSINESS_POTENTIAL` or `COUNTERPRODUCTIVE_TO_CORE_OFFER` field existed.

### Permanent correction

Before content action:

```text
OWNER_PRIMARY_GOAL
DESIRED_USER_OUTCOME
BUSINESS_POTENTIAL
CONTENT_ROLE_IN_FUNNEL
COUNTERPRODUCTIVE_TO_CORE_OFFER?
```

If the goal is unknown and can materially change the action, do not invent it: DEFER / OWNER_POLICY_REQUIRED.

---

## Defect 18 — broad DIY repair page confused an ownership gap with a content gap

### What the corrected run did

It proposed one broad page for DIY repair + adjustment.

### Why it seemed reasonable

The professional repair page was transactional and did not own the whole informational task; the broad structural unit had real demand.

### Why it was wrong

The current site already has substantial self-help content for adjustment, seasonal mode, stuck/opening problems and insulation. At the same time complex repair is a paid service. A broad new article would duplicate existing self-help and blur the safe-self-help / professional-repair boundary.

### Why the earlier research did not prevent it

Step 12 checked for **one page owner**, not for **distributed current content coverage**. `NO_SINGLE_OWNER` was silently promoted to `CONTENT_GAP`.

### Permanent correction

Every `NEW_INFORMATIONAL_PAGE` candidate must run a current-content reuse audit first:

```text
WHAT CURRENT CONTENT ALREADY COVERS THE TASK?
CAN EXISTING ARTICLE/HUB BE EXPANDED?
CAN EXISTING MATERIALS BE REFRAMED/CONSOLIDATED?
WHAT DISTINCT TASK REMAINS?
DOES THAT REMAINING TASK SUPPORT THE OWNER GOAL?
```

---

## Defect 19 — replacement service was a second false CREATE

### What happened

Step 12 proposed `PROPOSED_NEW:/uslugi/zamena-okon/`. Fresh current-site discovery found `https://okno-msk.ru/okna-rehau/po-tipu-doma/zamena-okon-v-kvartire/`, a commercial replacement page with price, CTA, reasons for replacement, product options and installation workflow.

### Why this matters

This proves Defect 16 was systemic. The process had no reliable negative-existence gate for CREATE.

### Permanent correction

All CREATE candidates, commercial and informational, must be rechecked in one batch under `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`. A single discovered false CREATE triggers re-audit of **all** surviving CREATE candidates before the step can close.

---

## Defect 20 — hardware guide CREATE ignored existing-content reuse

### What happened

A new broad guide for window hardware was proposed. Fresh current-site review shows that `https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna/` already has a substantial hardware-selection section and the site has specific hardware/accessory pages.

### Why the previous method still failed

The method looked for a dedicated broad owner and treated fragmentation as evidence for a new guide. It did not ask whether **expanding a strong existing high-level selection article** was the better business/content architecture.

### Permanent correction

For informational CREATE candidates, `EXPAND EXISTING` and `ROUTE TO EXISTING SPECIALISTS` are mandatory alternatives that must be explicitly tested before CREATE.

---


# 3A. Third external audit — six additional defects that must not be hidden by a technically clean V3

The third external literature review compared the current V3 method against current Yandex, Semrush, Ahrefs, Topvisor and Rush guidance. V3 fixed false CREATE decisions and business-goal mistakes, but six evidence layers were still too compressed. These are tracked as D12-21..D12-26.

## Defect 21 — content-gap type was implicit instead of explicit

### What V3 did
V3 stored `current_page_fit`, `existing_content_reuse` and the final structural action. The analyst could often infer why an action existed.

### Why that seemed sufficient
If the action is `EXPAND`, the page is presumably incomplete; if it is `CREATE`, something is presumably missing. The action appeared to encode the diagnosis.

### Why it is insufficient
Current content-gap methodology distinguishes fundamentally different failures: missing topic, wrong intent, weak/incomplete quality, lack of original value, or mixed/uncertain evidence. Those causes can produce different implementation even when the high-level action label looks similar. An ownership gap is also not automatically a content gap.

### Permanent rule
Every structural unit must state:

```text
GAP_TYPE =
  NONE
  TOPIC_GAP
  INTENT_GAP
  QUALITY_GAP
  ORIGINALITY_GAP
  MIXED_GAP
  EVIDENCE_INSUFFICIENT

GAP_EVIDENCE = why this diagnosis follows from current evidence
```

`CREATE` is allowed only after a verified `TOPIC_GAP` survives current-site, reuse, business-goal, demand and Search-boundary gates.

**Why:** the method must diagnose the problem before prescribing the page action.

## Defect 22 — structural KEEP could be misread as "do nothing" without performance evidence

### What V3 did
`KEEP_EXISTING_STRUCTURE` correctly meant the current URL is the best structural owner. In human reporting it could still sound like the page itself needs no improvement.

### Why that seemed reasonable
Step 12 is primarily structural. A strong task/page fit is enough to avoid unnecessary CREATE/SPLIT/MERGE.

### Why it is insufficient
Content-audit methods use traffic, visibility trends, conversions and business outcomes when deciding whether content is actually performing well enough to keep unchanged. The base Kwork order explicitly does not include Yandex Webmaster/Metrika account access, so Step 12 cannot honestly certify page performance.

### Permanent rule
Separate:

```text
STRUCTURAL_OWNER_DECISION
!=
OPTIMIZATION/PERFORMANCE_STATE
```

Required fields:

```text
PERFORMANCE_EVIDENCE_STATE
OPTIMIZATION_READINESS
```

When analytics are outside scope:

```text
PERFORMANCE_EVIDENCE_STATE = NOT_AVAILABLE_IN_BASE_SCOPE_NO_WEBMASTER_METRIKA
KEEP_EXISTING_STRUCTURE = KEEP THE URL/ROLE, NOT "NO OPTIMIZATION NEEDED"
```

**Why:** absence of analytics must constrain the claim, not be silently treated as good performance.

## Defect 23 — intended target and Yandex-selected relevant URL were not materialized together

### What V3 did
It stored the intended primary page plus a compressed `search_boundary_support` state.

### Why that seemed reasonable
Step 11 had already documented that target URL means intended owner, and ordinary Search evidence was sampled rather than exhaustive.

### Why it is insufficient
The page an analyst wants to rank and the page Yandex actually selects are different facts. A mismatch or non-observation can change confidence and determine what Step 13 must inspect.

### Permanent rule
For every unit preserve:

```text
INTENDED_TARGET_URL
CURRENT_YANDEX_RELEVANT_URL
RELEVANT_URL_MATCH_STATE =
  MATCH
  MISMATCH
  SITE_NOT_OBSERVED
  NOT_DIRECTLY_CHECKED
```

Only persisted ordinary-Search evidence may populate the observed URL. Never infer a ranking URL from page semantics.

**Why:** target ownership is a recommendation; relevant URL is observed search behaviour.

## Defect 24 — broad intent/support fields hid SERP content type / format / angle

### What V3 did
It stored broad intent and Search support strength.

### Why that seemed reasonable
For many commercial pages, broad intent plus obvious page fit is enough for structural ownership.

### Why it is insufficient
When page boundary is disputed, "informational" does not distinguish a how-to, comparison, list, calculator, review/forum result, product/category page or service landing. Current Search methodology uses the actual SERP to understand content type, format and angle.

### Permanent rule
For direct material Search evidence preserve separately:

```text
SERP_EXPECTED_CONTENT_TYPE
SERP_EXPECTED_FORMAT
SERP_EXPECTED_ANGLE
SERP_FORMAT_EVIDENCE_STATE
```

If the persisted evidence did not record a dimension, write `NOT_SEPARATELY_OBSERVED_IN_PERSISTED_EVIDENCE`; do not fabricate it from broad intent.

**Why:** evidence incompleteness is information and must remain visible.

## Defect 25 — owner-goal evidence source strength was not explicit enough

### What V3 did
It added owner goal, desired user outcome, business potential and content role. Many goals were inferred from the public commercial site.

### Why that seemed reasonable
A commercial site often makes its lead/sales objective obvious, and the base order does not include client interviews or CRM/support research.

### Why it is insufficient
A public-site inference is not the same evidence as an explicit client instruction, analytics, sales calls or support evidence. Some businesses deliberately publish low-direct-conversion content for authority/top-of-funnel strategy.

### Permanent rule
Add:

```text
OWNER_GOAL_EVIDENCE_SOURCE =
  CLIENT_STATED
  ANALYTICS_OBSERVED
  SALES_SUPPORT_EVIDENCE
  PUBLIC_SITE_EXPLICIT
  PUBLIC_SITE_INFERRED
  UNKNOWN

OWNER_POLICY_MATERIALITY = HIGH / MEDIUM / LOW / NOT_APPLICABLE
```

If a policy-sensitive action depends on an inferred/unknown goal, preserve that uncertainty. Never label inference as client-stated truth.

**Why:** business strategy is evidence, not a model assumption.

## Defect 26 — internal linking was treated mainly as a new-page hierarchy problem

### What V3 did
It had detailed hierarchy plans for proposed new pages, but most `ROUTE`, `SECTION` and `EXPAND` actions among existing pages were represented only by primary/supporting URLs.

### Why that seemed reasonable
The page relationship was conceptually visible and the initial hierarchy concern was orphaned new pages.

### Why it is insufficient
After all five CREATE concepts were withdrawn, the implementation value of Step 12 sits largely in relationships between existing pages. A route is not fully implementable if the client cannot see source, destination and purpose.

### Permanent rule
Material existing-page relationships must be written to an internal-link action ledger with:

```text
structural_unit_id
source_url
target_url
link_action_state
relation_type
placement_context
anchor_concept
user_journey_purpose
business_handoff
evidence_origin
```

When no distinct source/target link is justified, record an explicit `NOT_APPLICABLE` or `DEFER_SOURCE_CONTEXT_NOT_MATERIALIZED` rather than inventing a link.

**Why:** internal linking is part of implementing a routing decision, not decorative SEO after the architecture is finished.

## Third-audit source-derived execution overlay

The following order is mandatory because each stage constrains the next one:

```text
1. OWNER GOAL + EVIDENCE SOURCE
2. FULL PHRASE SET / COHERENT STRUCTURAL UNIT
3. FRESH CURRENT-SITE + CONTENT-REUSE CHECK
4. GAP TYPE DIAGNOSIS
5. STRUCTURAL OWNER FIT
6. PERFORMANCE EVIDENCE STATE (AVAILABLE / OUT OF SCOPE / MISSING)
7. REAL DEMAND
8. INTENDED TARGET vs OBSERVED YANDEX RELEVANT URL
9. SERP CONTENT TYPE / FORMAT / ANGLE WHEN MATERIAL
10. KEEP/EXPAND/SECTION/ROUTE/REUSE BEFORE CREATE
11. ACTION + STRUCTURAL-ONLY vs OPTIMIZATION-READY MEANING
12. EVIDENCE-DERIVED CONFIDENCE / MATURITY
13. INTERNAL-LINK IMPLEMENTATION FOR MATERIAL EXISTING-PAGE RELATIONS
14. FULL PHRASE MAP
15. DERIVED STEP-13 PAIR UNIVERSE
16. INDEPENDENT QA + OWNER CHALLENGE
17. GITHUB SAVE + STRUCTURED READBACK
18. PLAIN-LANGUAGE OWNER REPORT
```

### Third-audit fail-closed checks

```text
STRUCTURAL_UNITS_WITHOUT_GAP_TYPE = 0
CREATE_WITHOUT_VERIFIED_TOPIC_GAP = 0
KEEP_PRESENTED_AS_NO_OPTIMIZATION_NEEDED_WITHOUT_PERFORMANCE_EVIDENCE = 0
STRUCTURAL_UNITS_WITHOUT_PERFORMANCE_EVIDENCE_STATE = 0
STRUCTURAL_UNITS_WITHOUT_RELEVANT_URL_MATCH_STATE = 0
OBSERVED_RELEVANT_URL_WITHOUT_PERSISTED_SEARCH_EVIDENCE = 0
DIRECT_SERP_EVIDENCE_WITHOUT_EXPLICIT_TYPE_FORMAT_ANGLE_STATE = 0
STRUCTURAL_UNITS_WITHOUT_OWNER_GOAL_EVIDENCE_SOURCE = 0
POLICY_SENSITIVE_UNKNOWN_OWNER_GOAL_PRESENTED_AS_FINAL = 0
MATERIAL_ROUTE_WITHOUT_LINK_ACTION_OR_EXPLICIT_NA_DEFER = 0
INTERNAL_LINK_TO_WITHDRAWN_PROPOSED_NEW_PAGE = 0
```



## Defect 27 — evidence-first page recheck exposed residual mixed structural units

### What happened
After D12-21 introduced explicit gap diagnosis, evidence-first review of strong current-page fits exposed that `FRENCH_WINDOWS_COMMERCIAL` and `WINDOW_ACCESSORIES_GENERAL` still mixed different terminal user tasks. The French unit combined genuine commercial demand with inspiration, concept, DIY and hardware phrases. The general-accessories unit mixed generic accessory shopping with aftermarket hardware and aluminium-specific component/frame tasks.

### Why it seemed reasonable
The phrases shared strong lexical/product-family similarity, and earlier correction rounds had already removed several obvious outliers. Once a unit had survived repeated QA, it was easy to treat the unit ID itself as evidence that the remaining members were coherent.

### Why that is wrong
A structural unit is an analytical hypothesis, not permanent truth. Fresh page/gap evidence can expose a contradiction that was invisible under an earlier coarse boundary. If the unit mixes terminal tasks, every later gap type, page-fit and structural action aggregates incompatible evidence.

### Permanent correction
Whenever a fresh current-page, gap-type, owner-goal or Search-boundary review materially changes the understanding of a structural unit, re-open **all member phrases of that unit** before retaining the unit as a final boundary.

```text
MATERIAL LATER EVIDENCE CONTRADICTS OR NARROWS A STRUCTURAL UNIT
→ EXTRACT ALL MEMBER PHRASES
→ REVIEW EACH PHRASE AGAINST TERMINAL USER TASK / PAGE EXPECTATION
→ REASSIGN TO EXISTING VALID UNIT OR EXPLICIT NEW/DEFERRED UNIT
→ RECOMPUTE UNIT COUNTS / ACTIONS / PHRASE MAP / INTERNAL LINKS / PAIR GRAPH
→ INDEPENDENT EXACT-PHRASE REGRESSION
```

Do not review only the phrase that exposed the problem. One contradiction is evidence that the unit boundary itself must be challenged.

**Why:** later evidence must be allowed to falsify an earlier cluster/unit. Otherwise the methodology becomes self-sealing.

### OKNO-MSK regression evidence
The D12-27 review explicitly inspected 65 phrases. Twenty were reassigned; the French commercial core retained 42 true commercial phrases and the generic-accessory core retained 3 true generic phrases. The final V5/V6 independent verifier checks all 65 exact resolutions and recomputes the downstream graph.

---


# 4. Correct Step-12 working model

A structural action is not chosen directly from `cluster_id` or `ownership_state`.

Correct reasoning chain:

```text
OWNER PRIMARY GOAL / DESIRED USER OUTCOME
→ FULL PHRASE SET
→ COHERENT STRUCTURAL UNIT(S)
→ USER TASK AND EXPECTED RESULT
→ FRESH CURRENT-SITE / CURRENT-CONTENT DISCOVERY
→ BUSINESS TRUTH + BUSINESS POTENTIAL + CONTENT ROLE
→ CURRENT EXISTING PAGE FIT / CONTENT REUSE FIT
→ DEMAND EVIDENCE
→ SEARCH/SERP EVIDENCE WHEN IT CAN CHANGE THE PAGE BOUNDARY
→ ALTERNATIVE STRUCTURAL OPTIONS (KEEP/EXPAND/SECTION/ROUTE/REUSE BEFORE CREATE)
→ ACTION
→ CONFIDENCE / PROVISIONAL STATUS
→ SITE-HIERARCHY IMPLEMENTATION
→ COMPLETE PHRASE MAP
→ DERIVED NEXT-STEP PAIRS
→ INDEPENDENT QA + OWNER-CHALLENGE CASES
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

Use only when the structural unit is coherent and standalone, the owner/business goal supports attracting and satisfying this demand in the proposed format, the business can truthfully fulfil the promise, a fresh current-site and content-reuse audit proves no adequate current page/content path exists, real demand/search evidence supports the boundary at the confidence claimed, and its site placement is explicit.

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
OWNER_GOAL_ALIGNMENT = STRONG / PARTIAL / WEAK / OWNER_POLICY_REQUIRED
BUSINESS_POTENTIAL = HIGH / MEDIUM / LOW / NEGATIVE_OR_COUNTERPRODUCTIVE / OWNER_POLICY_REQUIRED
CONTENT_ROLE = SELL / ASSIST_DECISION / EDUCATE_TO_CONVERT / SELF_SERVICE / AUTHORITY / TRAFFIC_PLAY / DEPRIORITIZE
FRESH_SITE_CHECK = CURRENT_VERIFIED / MULTI_ROUTE_ABSENCE_VERIFIED / INCOMPLETE
EXISTING_CONTENT_REUSE = NOT_APPLICABLE / REUSE_PREFERRED / EXPAND_PREFERRED / DISTINCT_GAP_VERIFIED
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


### Fresh-site / owner-goal checks added after second audit

```text
EVERY_CREATE_HAS_FRESH_CURRENT_SITE_CHECK = true
EVERY_CREATE_HAS_EXISTING_CONTENT_REUSE_AUDIT = true
EVERY_CREATE_HAS_OWNER_GOAL_ALIGNMENT = true
EVERY_CREATE_HAS_BUSINESS_POTENTIAL = true
CREATE_WITH_CURRENT_EQUIVALENT_PAGE = 0
NEUTRAL_ENABLEMENT_COUNTERPRODUCTIVE_TO_CORE_PAID_OFFER = 0 unless owner explicitly approves that strategy
OLD_INVENTORY_USED_AS_SOLE_ABSENCE_PROOF = 0
```

These checks must be computed from persisted freshness/business ledgers or explicit manual owner-policy rows, not hard-coded booleans.

---

# 8. Correct Step-12 execution order — revised after owner challenge

This order supersedes every earlier Step-12 ordering when there is a conflict. The ordering is causal: each stage prevents a specific failure class before later evidence is allowed to harden the wrong recommendation.

## Stage 1 — Define the owner's business goal and desired user outcome

Record the best available owner/client goal evidence: leads, direct sales, authority, support/retention, traffic or mixed. If public-site behaviour is used as a proxy, label it `PUBLIC_BUSINESS_GOAL_INFERRED`, not owner-confirmed.

**Why first:** without the goal, the process can spend time proving an SEO opportunity that the owner should not implement.

## Stage 2 — Freeze accepted upstream phrase-level inputs

Read final Step-11 phrase map, ownership/corrections/unresolved rows, Wordstat and available Search evidence.

**Why:** later corrections must preserve provenance and exact accounting.

## Stage 3 — Materialize every phrase and audit semantic coherence

Inspect all member phrases; split mixed tasks into explicit structural units or defer ambiguity.

**Why:** page architecture cannot repair a wrong task boundary.

## Stage 4 — Refresh the current public site before structural actions

Use `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`. Broad negative claims use Codex/browser discovery plus targeted web read when available; small named positive checks can use targeted ChatGPT web. Persist the timestamped result.

**Why here:** old inventory absence is not current absence.

## Stage 5 — Build current candidate-page and current-content reuse views

Open/read plausible owners, related articles, hubs, children, services and utilities. For informational candidates, map distributed existing coverage, not only one exact owner.

**Why:** `NO_SINGLE_OWNER != CONTENT_GAP`.

## Stage 6 — Evaluate business truth, owner-goal alignment and business potential

For every material unit record:

```text
BUSINESS_TRUTH
OWNER_PRIMARY_GOAL
DESIRED_USER_OUTCOME
BUSINESS_POTENTIAL
CONTENT_ROLE
COUNTERPRODUCTIVE_TO_CORE_OFFER?
```

**Why before demand:** high demand does not make a low/negative-value topic strategically correct.

## Stage 7 — Attach real demand evidence

Use Wordstat/frequency evidence. Phrase count is coverage only.

**Why:** demand strength and vocabulary size are different facts.

## Stage 8 — Attach Search/SERP evidence only where it can change the page boundary

Use existing evidence first; name any material gap.

**Why:** Search tells us what result type is expected, not whether the business should pursue the topic.

## Stage 9 — Compare existing-content alternatives before CREATE

Mandatory comparison order:

```text
KEEP
→ EXPAND
→ ADD SECTION / FAQ
→ ROUTE TO EXISTING CHILD/SPECIALIST PAGE
→ REFRAME / CONSOLIDATE EXISTING CONTENT
→ ONLY THEN EVALUATE CREATE
```

This is not a ban on CREATE. It is proof that CREATE fills a real remaining gap.

## Stage 10 — Fresh CREATE gate

Every surviving CREATE candidate must pass **again immediately before acceptance**:

```text
CURRENT-SITE EXISTENCE CHECK
+ EXISTING-CONTENT REUSE AUDIT
+ DISTINCT USER TASK
+ REAL DEMAND
+ BUSINESS GOAL / BUSINESS POTENTIAL
+ TRUTHFUL EXPERTISE/OFFER
+ SEARCH BOUNDARY WHEN MATERIAL
+ NO CURRENT EQUIVALENT
+ IMPLEMENTABLE HIERARCHY
```

If one false CREATE is found, re-audit all CREATE candidates in that run.

## Stage 11 — Choose action and derive evidence-based confidence/maturity

No default HIGH. A material fresh-site gap, owner-policy gap or Step-13 dependency prevents final HIGH.

## Stage 12 — Define hierarchy/internal links for accepted new/split pages

Only pages that survived Stage 10 receive new-page hierarchy.

## Stage 13 — Materialize the full phrase→unit→page/action map

Every active phrase receives exactly one final action or explicit unresolved/deferred state.

## Stage 14 — Derive the complete Step-13 candidate-pair universe

Use the final current routing graph. Do not diagnose cannibalization yet.

## Stage 15 — Independent QA plus owner-challenge review

Machine QA recomputes accounting/current-site/create/business fields from persisted artifacts. Manual owner-challenge ledger must include at least:

```text
WHY DOES THE OWNER WANT THIS PAGE?
WHAT SHOULD THE USER DO AFTER IT?
DOES IT HELP OR SUBSTITUTE FOR A CORE PAID OFFER?
WAS A CURRENT EQUIVALENT PAGE/CONTENT RECHECKED?
CAN EXISTING CONTENT BE EXPANDED INSTEAD?
```

**Why:** 46 perfect technical checks cannot compensate for a missing strategic question.

## Stage 16 — Persist to GitHub and structured readback

Save method evidence, freshness ledger, actions, phrase map, QA and report; read them back before acceptance.

## Stage 17 — Plain-language owner report

Always explain:
- why the step exists;
- what changed on the site recommendation;
- what was rejected and why;
- what remains provisional;
- what the owner should actually implement.

Only after this may Step 13 become allowed.

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


---

# 14. Post-PASS D12-28..D12-30 correction — why the method failed again

The prior D12-27 closure was later withdrawn after a new external-method audit proved that Step 12 could still pass while material claims were circular or insufficiently falsified. This was **not a lack-of-research failure**. The sources had already identified the right concepts. The failure was translating those concepts into fields and then verifying the fields instead of independently verifying the real-world claim.

Canonical failure chain:

```text
EXTERNAL PRINCIPLE
→ ADD FIELD / STATE
→ GENERATOR POPULATES FIELD FROM ITS OWN ACTION LOGIC
→ VERIFIER CHECKS FIELD PRESENCE / ACTION CONSISTENCY
→ FALSE PASS
```

Concrete failures:

```text
EXPAND / SECTION
→ generator wrote QUALITY_GAP
→ generic gap_evidence restated that fuller coverage was needed
→ verifier checked that gap_type existed and matched action
→ current page was not independently required to prove the missing need

ROUTING GRAPH EDGE
→ generator wrote IMPLEMENT internal link
→ verifier checked source/target fields and coverage
→ current source context + current target task fit were not independently required

KNOWN D12-27 PHRASES FIXED
→ exact regression set became zero
→ verifier treated that as enough
→ later review found other mixed units outside the known regression set
```

Permanent root-cause rules:

```text
SCHEMA COMPLETENESS != EVIDENCE COMPLETENESS
ACTION CONSISTENCY != CAUSAL VALIDATION
ACTION MUST NEVER BE AN EVIDENCE SOURCE FOR ITSELF
KNOWN URL != PAGE FIT
ROUTING EDGE != IMPLEMENTABLE LINK
KNOWN_REGRESSION_ZERO != GLOBAL_SEMANTIC_COHERENCE_PASS
```

Therefore every future Step 12 must also read and obey:

- `STEP_12_EVIDENCE_INDEPENDENCE_AND_CURRENT_CONTENT_VALIDATION.md`;
- `STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md`;
- `STEP_12_THIRD_AUDIT_EXECUTION_ORDER_CLARIFICATION.md`;
- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`.

Current OKNO-MSK correction proof before final state readback:

```text
20 historical QUALITY_GAP units re-read from current content
322/322 affected member phrases re-reviewed
49 exact phrase reassignments
8 QUALITY_GAP remain, each with explicit missing need
28/28 historical IMPLEMENT links revalidated
15 IMPLEMENT retained; 13 downgraded to explicit DEFER states
2332/2332 final phrase map
168 structural units
195 candidate pairs independently reconciled
independent findings = 0
new page actions = 0
Step13 executed = false
```

The final reusable PASS still requires durable readback of the closure state itself.
