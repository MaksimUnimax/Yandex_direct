# KW-002 — LEVEL 2 STEP RULES INDEX

Status: **OWNER-APPROVED METHODOLOGY REVISION / ACTIVE FOR KW-002**  
Product: from-scratch semantic core + clustering + planned site architecture for modern Yandex.
Revision authority: owner instruction 2026-09-10 after Blood & Sand Step04 volume/audit findings.

Level 2 contains universal rules for each execution step. Concrete Blood & Sand data belongs only in `work/BLOOD_SAND_GREENFIELD_2026-09-08/`.

Mandatory Level-1 volume rule:

`LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`

## Global execution order

```text
00 scope + purchased delivery cap freeze
01 business/assortment model
02 seed map
03 primary Wordstat acquisition -> LOSSLESS RAW
03A RAW normalization + exact/safe implicit deduplication
03B high-confidence sanitation + candidate/reserve preparation
04 first family triage on SANITIZED CANDIDATES, not RAW occurrences
05 targeted expansion / coverage control -> immediate 03A/03B sanitation for new rows
06 current Yandex competitor discovery
07 competitor semantic expansion
08 competitor-derived Wordstat expansion -> immediate 03A/03B sanitation for new rows
09 candidate semantic master + valid reserve freeze
10 nuanced row-level relevance + intent + user job + priority
11 delivery-scope selection + Search-stage semantic freeze
12 ordinary Yandex Search batch acquisition for DELIVERY-SELECTED set
13 SERP + task-first clustering
14 query→page ownership + Search-only IA freeze
15 AI-search diagnostic selection
16 AI-search evidence acquisition
17 Search-vs-AI reconciliation
18 final semantic core + site IA + Page Jobs + internal-link model
19 client deliverables
20 final QA / recipient acceptance
21 revision rehearsal + Kwork productization measurement
22 job close
```

No step may be silently skipped because a later step appears to contain similar data.

Hard data-flow rule:

```text
RAW_OCCURRENCE_POOL
-> NORMALIZED_UNIQUE_POOL
-> SANITIZED_CANDIDATE_POOL
-> CANDIDATE_SEMANTIC_MASTER + VALID_RESERVE_SET
-> DELIVERY_SELECTED_SET
-> SEARCH/SERP/CLUSTERING
-> FINAL_DELIVERED_CORE
```

The expensive analyst/LLM/Search/SERP stages must never default to the complete RAW occurrence universe.

---

# STEP 00 — order / scope / source / delivery-cap freeze

### Purpose

Make the order reproducible before research can influence the brief and freeze the commercial size of the promised client result.

### Inherited KW-001 rule

`scope freeze before evidence acquisition`.

### Required actions

Freeze:

```text
business description
region
actual assortment/services
commercial goal
business exclusions
site state
allowed input sources
sealed/prohibited sources
order-specific deliverable scope
DELIVERY_KEYWORD_CAP
purchased add-on increments, if any
```

### Delivery-cap rule

`DELIVERY_KEYWORD_CAP` applies to the final client-delivered phrase rows, not to RAW acquisition.

Current standard productization ceiling:

```text
STANDARD_KWORK_DELIVERY_CEILING = 1500
>1500 = custom / separately owner-approved scope
```

Do not promise that a package of `up to N` will be padded to exactly N if fewer relevant phrases survive evidence-based cleaning.

### Output

`JOB_MANIFEST.md` + frozen brief/source whitelist + frozen delivery cap.

### PASS

No unresolved ambiguity that would change what business/geography is researched or how many final phrase rows were purchased.

---

# STEP 01 — business and assortment model

### Purpose

Understand what can genuinely be sold/represented before inventing search vocabulary.

### Method

Build a neutral model:

```text
products/services
families/categories
attributes
uses/problems solved
selection dimensions
commercial actions
known exclusions
```

Do not use prior SEO research as a shortcut in a greenfield rehearsal.

### Output

`BUSINESS_AND_ASSORTMENT_MODEL`.

### PASS

Every seed family in Step 02 can trace to an actual offer/use/business boundary.

---

# STEP 02 — seed / acquisition probe map

### Purpose

Create probes for discovering demand, not a fake final keyword list.

### Inherited KW-001 rule

```text
SEED != FINAL KEYWORD
SEED != FINAL PAGE TARGET
```

A seed may be broad or diagnostic if it is useful for discovering a real demand family.

### Required seed dimensions

Where relevant:

```text
head product/service terms
synonyms / common naming variants
category/family terms
use-case terms
selection/comparison terms
commercial modifiers
problem/question terms
attribute/material/form-factor terms
brand terms only as a separate class
```

### Output

`SEED_MAP` with purpose and business lineage for each seed.

### PASS

Coverage is broad enough to probe the business without claiming completeness.

---

# STEP 03 — primary Wordstat acquisition

### Purpose

Acquire current Yandex human-demand evidence from the seed map as a lossless RAW evidence layer.

### Inherited KW-001 rules

```text
provider success != collection completion
preserve complete result required by the step
preserve seed/region/provenance for every occurrence
one returned phrase may occur under multiple seeds; do not destroy provenance early
RAW OCCURRENCE != FINAL KEYWORD CANDIDATE
```

### Official source

`https://yandex.ru/support2/wordstat/ru/`

Operators, when deliberately needed:

`https://yandex.ru/support2/wordstat/ru/content/operators`

### Bridge

Use durable Wordstat batch/provider jobs. Technical batch size is not a product limit.

### Output

Complete raw primary Wordstat occurrence table(s): `RAW_OCCURRENCE_POOL`.

### PASS

Every authorized seed has known terminal/acquisition status and complete preserved required payload.

### Mandatory next gate

Step03 completion NEVER sends the complete RAW occurrence universe directly to Step04 semantic triage.

It must pass through Step03A and Step03B first.

---

# STEP 03A — RAW normalization + deduplication

### Purpose

Convert lossless provider occurrences into a compact analytical phrase layer without destroying provenance.

### Method

For the complete RAW occurrence set:

```text
preserve every raw occurrence and provider identity
canonicalize whitespace/case/technical punctuation conservatively
create one stable normalized phrase identity
collapse exact duplicates analytically while retaining all occurrence lineage
detect safe implicit duplicate groups (word-order / inflection variants)
select canonical representative only where equivalence is high-confidence
never delete the underlying RAW evidence
```

### Required distinction

```text
25 occurrences of the same phrase under different runs
= 25 RAW evidence occurrences
= potentially 1 normalized analytical phrase with 25 provenance links
```

### Frequency handling

Where duplicate variants are genuinely equivalent, frequency may help choose the canonical representative. It must not be used to decide business relevance.

### External corroboration

- Topvisor implicit duplicates: `https://topvisor.com/ru/support/implicit-duplicates/`
- Key Collector implicit duplicates: `https://www.key-collector.ru/docs/tools/implicit-duplicates/`

### Output

`NORMALIZED_UNIQUE_POOL` + `NORMALIZATION_LEDGER` preserving RAW lineage.

Minimum fields:

```text
normalized_phrase_id
canonical_phrase
all_raw_occurrence_ids
all_seed/run/provider provenance
exact_duplicate_count
implicit_duplicate_group_id if applicable
canonicalization_reason
```

### PASS

```text
RAW occurrence count fully reconciled
no provenance loss
all normalized rows trace to RAW
all collapsed duplicates explain why they were collapsed
```

---

# STEP 03B — high-confidence sanitation / pre-filter

### Purpose

Remove obvious machine-detectable noise and foreign meanings before expensive semantic family triage while preserving uncertainty.

### Method

Apply the frozen business scope and conservative filters to `NORMALIZED_UNIQUE_POOL`.

Allowed high-confidence sanitation classes include:

```text
explicit frozen business exclusions
explicit foreign brands/entities where context proves foreign referent
explicit media/game/book/person/place/organization/vehicle-model contexts
obvious morphology/lexical garbage
technical noise / empty strings / malformed rows
safe implicit duplicates already identified at 03A
high-confidence stop-topic patterns derived from observed evidence
```

### Asymmetric rule

```text
CLEAR OFF-TOPIC -> AUTO_EXCLUDED with reason + lineage
CLEAR DUPLICATE -> COLLAPSED_TO canonical row
UNCERTAIN / MULTI-MEANING -> HOLD / AMBIGUOUS
DIRECT BUSINESS-SUPPORTED -> KEEP_CANDIDATE
LOW FREQUENCY ALONE -> NEVER AUTO_EXCLUDE
HIGH FREQUENCY ALONE -> NEVER KEEP
```

A stop-word/token blacklist alone is insufficient for ambiguous entity boundaries. Context/referent rules are required.

### Official/industry support

- Yandex Webmaster query selection: `https://yandex.ru/support/webmaster/ru/service/queries-selection`
- Topvisor progressive cleaning: `https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/`

### Output

```text
SANITIZED_CANDIDATE_POOL
AUTO_EXCLUDED_REGISTER
HOLD_AMBIGUOUS_REGISTER
SANITATION_QA
```

### Mandatory accounting

Report:

```text
raw_occurrence_rows
normalized_unique_rows
implicit_duplicate_groups
collapsed_duplicate_rows
auto_excluded_rows by reason
hold_ambiguous_rows
sanitized_candidate_rows
```

### PASS

No silent row loss; every normalized phrase is candidate, excluded, collapsed or HOLD with a deterministic reason and RAW lineage.

---

# STEP 04 — first family triage

### Purpose

Understand what demand families exist and where the **sanitized candidate pool** is still ambiguous or incomplete before nuanced row-level review.

### Input rule

Step04 reads:

```text
SANITIZED_CANDIDATE_POOL
+ HOLD_AMBIGUOUS_REGISTER where family context is needed
+ aggregate RAW provenance locators
```

It does NOT require the LLM/analyst to semantically classify every RAW occurrence independently.

The RAW occurrence ledger remains machine/audit evidence only.

### Inherited KW-001 rules

```text
FAMILY TRIAGE != FINAL ROW CLEANUP
LOW FREQUENCY ALONE != IRRELEVANCE
FAMILY TRIAGE != RAW OCCURRENCE PARTITION
```

### Actions

Classify preliminary candidate families approximately as:

```text
strong in-scope
plausible in-scope
mixed/ambiguous
obvious out-of-scope missed by sanitation
coverage gap / requires expansion
```

Any obvious out-of-scope family found here is a feedback signal to improve Step03B rules, not justification to keep feeding the same noise downstream forever.

### Output

`FAMILY_TRIAGE` + targeted-expansion queue + sanitation feedback register.

### PASS

No family is permanently rejected solely on a superficial token/frequency rule; the working semantic dataset is materially smaller than RAW and remains fully traceable.

---

# STEP 05 — targeted expansion / coverage control

### Purpose

Close material vocabulary holes created by initial seed choice or revealed by Step04.

### Inherited KW-001 boundary

A second acquisition must use the same union-compatible evidence/provenance model as primary acquisition.

### Possible evidence routes

```text
new synonyms/naming variants discovered in Wordstat
promising related-query branches
missing business families
regional/dynamics checks when they affect scope/priority
owner/client clarification when a business boundary is unclear
```

### Mandatory volume rule

Every NEW Step05 provider result must immediately pass through the same Step03A normalization and Step03B sanitation before union with the working candidate set.

Do not append raw Step05 occurrences directly to Step04/09 semantic working tables.

### Stopping rule

Stop when another acquisition branch has low expected information gain, not because an arbitrary fixed number of seeds was reached and not because the final delivery cap is not yet numerically full.

### Output

```text
new RAW evidence preserved
normalized/sanitized Step05 additions
updated candidate pool
updated valid reserve
```

---

# STEP 06 — current Yandex competitor discovery

### Purpose

Find actual search competitors for retained candidate families, not merely businesses the client calls competitors.

### Input volume rule

Use representative high-value sanitized families/queries. Do not run competitor discovery over the complete RAW universe.

### Method

Use representative in-scope query families in current ordinary Yandex Search and record:

```text
query
region/time
ranked domains/URLs
page/result type
recurrence of domains across families
```

### Rule

```text
BUSINESS RIVAL != SEARCH COMPETITOR
```

### Output

`SEARCH_COMPETITOR_REGISTRY` with reasons each domain was selected for semantic inspection.

---

# STEP 07 — competitor semantic expansion

### Purpose

Discover vocabulary/topics missed by our own starting language.

### Transferred KW-001 Step 5A rules

```text
COMPETITOR PAGE TOPIC != EXACT QUERY RANKING
COMPETITOR RANKING != AUTOMATIC KEYWORD ACCEPTANCE
COMPETITOR-DERIVED SEED != FINAL KEYWORD
TESTED QUERY VISIBILITY != FULL COMPETITOR KEYWORD UNIVERSE
```

### Method

```text
real recurring Yandex competitor
→ inspect evidence-bearing relevant public pages
→ extract candidate missed topics/seeds
→ compare against already sanitized semantic universe
→ only genuinely new candidates continue
```

This is semantic coverage research, not a full competitor SEO audit and not a substitute for a reverse-domain database.

### Output

`COMPETITOR_DERIVED_SEED_CANDIDATES` with source URL and topic evidence.

---

# STEP 08 — competitor-derived Wordstat expansion

### Purpose

Test whether competitor-derived topics correspond to real Yandex demand.

### Rule

```text
PUBLIC PAGE TOPIC
MUST RETURN TO DEMAND EVIDENCE
BEFORE IT CAN ENTER THE FINAL CORE AS SEARCH DEMAND
```

### Method

Run new candidate seeds through Wordstat under the same persistence/provenance rules as Step03.

Immediately after acquisition:

```text
Step08 RAW
-> Step03A normalization
-> Step03B sanitation
-> union only sanitized new candidates
```

### Output

Competitor-derived RAW evidence + normalized/sanitized candidate decisions:

```text
NEW_DEMAND
ALREADY_COVERED
NO_USEFUL_DEMAND
OUT_OF_SCOPE
HOLD
```

Do not let competitor expansion inflate the working semantic set with raw duplicates/noise.

---

# STEP 09 — candidate semantic master + reserve freeze

### Purpose

Create one auditable **post-sanitation** candidate universe before expensive nuanced row-level decisions.

### Inherited KW-001 rule

Do not silently lose demand/provenance fields at semantic freeze boundaries.

### Master must preserve

```text
normalized phrase
all acquisition sources/seeds
region
provider demand fields
RAW occurrence lineage
competitor-derived lineage if applicable
sanitation state/reason
family state
status/errors
```

### Separate sets

Step09 must distinguish:

```text
ACTIVE_CANDIDATES
HOLD_AMBIGUOUS
VALID_RESERVE_CANDIDATES
AUTO_EXCLUDED_HISTORY
```

`VALID_RESERVE_CANDIDATES` are not rejects. They are cleaned potential phrases that may later fall outside the purchased delivery cap.

### Output

`CANDIDATE_SEMANTIC_MASTER` + preliminary `VALID_RESERVE_SET`.

### PASS

The candidate master is substantially smaller than cumulative RAW and no candidate exists only because the same phrase was repeated across provider runs.

---

# STEP 10 — nuanced row relevance + intent + user job + priority

### Purpose

Perform the expensive semantic review only on the sanitized candidate universe: decide which phrases genuinely belong to the client business, what users are trying to do, and how strongly each phrase deserves scarce delivery/Search budget.

### Transferred KW-001 rules

```text
NO DEFAULT KEEP
POSITIVE IN-SCOPE EVIDENCE REQUIRED
ACCOUNTING QA != SEMANTIC QA
UNCERTAINTY STAYS EXPLICIT
FREQUENCY ALONE != PRIORITY
```

### Every candidate row receives

```text
KEEP / REJECT / HOLD
relevance reason
user task/job
intent class or mixed intent
commercial/informational role
business-fit state
frequency/demand evidence
clicks where available
competition/rankability where available
redundancy/canonicality state
family/cluster coverage role
delivery_priority_tier
```

### Priority method

Do not sort only by frequency.

Use, in order:

```text
business/assortment fit
coverage of commercially important families
intent/user-job fit and ambiguity
Yandex demand/frequency + clicks where available
competition/rankability where available
redundancy/canonicality
incremental topic/cluster coverage value
```

### Important

Intent is not determined mechanically only by words such as `купить`, `цена`, `что такое`. Current SERP evidence in later steps can refine the judgment.

### Output

`CLEANED_PRIORITIZED_SEMANTIC_MASTER`.

---

# STEP 11 — delivery-scope selection + Search-stage semantic freeze

### Purpose

Freeze the exact retained semantic set that will receive expensive structural/Search evidence while respecting the purchased result size.

### Required commercial rule

```text
DELIVERY_SELECTED_SET <= DELIVERY_KEYWORD_CAP
FINAL standard KW-002 delivery <= 1500 unless custom owner-approved scope
```

### Selection rule

When valid cleaned phrases exceed the purchased cap:

```text
1. guarantee reasonable coverage of all commercially material business families;
2. avoid spending the cap on redundant variants of one family;
3. select highest coverage-aware priority phrases;
4. move remaining valid phrases to VALID_RESERVE_SET;
5. reserve != reject;
6. preserve reasons/rank for future +N expansion.
```

When fewer valid phrases exist than the cap, do not pad the set with junk.

### Paid +N rule

A paid additional tranche (for example +500) normally promotes the next highest-priority valid reserve phrases while preserving family/cluster coverage.

It is NOT defined as the next N phrases by raw Wordstat frequency.

Only if the valid reserve is insufficient and the purchased expansion requires broader legitimate coverage may new acquisition be considered.

### Inherited KW-001 rule

Every retained phrase must have deterministic lineage back to demand/provenance evidence. Silent field loss = FAIL.

### Output

```text
DELIVERY_SELECTED_SET
VALID_RESERVE_SET
DELIVERY_SELECTION_LEDGER
SEARCH_STAGE_SEMANTIC_SET
```

This is not yet final clustering or IA.

### PASS

```text
selected rows <= purchased cap
all selected rows are cleaned and prioritized
all overflow valid rows are explicit reserve
no frequency-only selection
no artificial padding to cap
```

---

# STEP 12 — ordinary Yandex Search batch acquisition

### Purpose

Acquire current SERP evidence needed for clustering and page-boundary decisions **only for the delivery-selected/Search-stage semantic set**.

### Bridge capability

Use the accepted ordinary Search batch hand and split the selected set across multiple jobs when a technical job limit is reached.

### Product/batch rule

```text
SEARCH_BATCH_JOB_LIMIT != DELIVERY_KEYWORD_CAP
RAW_OCCURRENCE_POOL != SEARCH_INPUT
VALID_RESERVE_SET != SEARCH_INPUT by default
```

The purchased delivery cap was enforced at Step11. Step12 must not silently expand back to the raw universe.

### Preserve for each query

```text
query
region/time
ranked URLs/domains/titles
result/page types where analytically derived
provider/job provenance
```

### Output

Complete persisted Search evidence for the selected set.

---

# STEP 13 — SERP + task-first clustering

### Purpose

Determine which retained delivery-selected phrases should be served by the same page and which require separate page jobs.

### Transferred KW-001 clustering rules

```text
TASK-FIRST CORE
SERP OVERLAP = EVIDENCE, NOT AUTOMATIC VERDICT
NO UNIVERSAL MAGIC OVERLAP THRESHOLD
MIXED INTENT MUST REMAIN VISIBLE
```

### External corroboration

- Ahrefs: `https://ahrefs.com/blog/keyword-clustering/`
- Semrush: `https://www.semrush.com/blog/keyword-clustering/`

### Inputs

```text
semantic meaning
user job
intent
current ranked URLs/domains/page types
SERP overlap/jaccard/containment projections
business/assortment boundaries
```

### Work rule

Large pairwise/cluster analysis may use Work, but only over the already delivery-selected set. Do not load full RAW occurrence ledgers into Work merely because they exist.

Machine-generated similarity matrices may remain machine artifacts; Work/analyst receives compact cluster candidates and targeted evidence.

### Output

`CLUSTER_MASTER` with member coherence and split/merge reasoning.

---

# STEP 14 — query→page ownership + Search-only IA freeze

### Purpose

Turn clusters into a planned site architecture before AI-search evidence can influence it.

### Transferred KW-001 rules

```text
one cluster must have an explicit primary page owner
cluster ownership != merely mentioning the phrase on many pages
target page != observed competitor/current relevant URL
SEARCH-ONLY ARCHITECTURE MUST BE FROZEN BEFORE AI COMPARISON
```

### For a greenfield site assign

```text
planned page/unit ID
page type
working URL/slug candidate
parent section
primary cluster
secondary clusters/queries
user job
commercial/informational/hybrid role
supporting-page relationships
```

### Output

`SEARCH_ONLY_QUERY_PAGE_MAP` + `SEARCH_ONLY_IA`.

---

# STEP 15 — AI-search diagnostic selection

### Purpose

Select the smallest sufficient set of cases that can reveal whether generative Yandex changes or de-risks Search-only page decisions.

### Transferred KW-001 rules

```text
DIAGNOSTIC SET != REPRESENTATIVE OF EVERY QUERY BY DEFAULT
SELECT FOR DECISION VALUE, NOT DECORATION
STABILITY/CONTROL CASES SEPARATE FROM CHANGE-CANDIDATE CASES
```

Select cases across material boundaries such as:

```text
commercial vs informational
broad root vs explanatory query
mixed-intent family
cluster split/merge boundary
source-quality-sensitive topic
selection/comparison task
```

### Output

`AI_SEARCH_CASE_REGISTER` with explicit reason for each case.

---

# STEP 16 — AI-search evidence acquisition

### Purpose

Observe the generative Yandex search surface relevant to the selected cases.

### Claim boundary

```text
GENSEARCH/STRUCTURED AI-SEARCH EVIDENCE != GUARANTEED CONSUMER ALICE STATE FOREVER
ONE AI ANSWER != STABLE UNIVERSAL TRUTH
SOURCE ORDER != RANKING
```

Preserve:

```text
query/case
observation surface/provider mode
answer/user-job orientation
source domains/types
used-source truth where exposed
search-query expansion themes where exposed
commercial vs explanatory orientation
raw/durable evidence reference
```

### Output

`AI_SEARCH_EVIDENCE_REGISTER`.

---

# STEP 17 — Search-vs-AI reconciliation

### Purpose

Measure whether AI-search evidence changes the Search-only semantic/page architecture.

### Transferred KW-001 rule

Every case preserves:

```text
selection reason
frozen Search-only baseline
evidence comparison
verdict
downstream effect
```

Allowed verdicts:

```text
NO_CHANGE
DE_RISK
ENRICH_PAGE_JOB
SPLIT_SUPPORTED
MERGE_SUPPORTED
PRIORITY_CHANGE
HOLD / INSUFFICIENT
```

### Rule

Do not force an AI delta. Supported `NO_CHANGE` is a valid client-visible result.

### Output

`SEARCH_AI_RECONCILIATION` and explicit mutation list against Search-only IA.

---

# STEP 18 — final semantic core + IA + Page Jobs + internal-link model

### Purpose

Materialize the final site-ready semantic architecture after reconciliation.

### Final phrase count rule

```text
FINAL_DELIVERED_CORE <= DELIVERY_KEYWORD_CAP
STANDARD ordinary KW-002 <= 1500 final phrase rows
VALID_RESERVE_SET is not silently appended to client deliverables
```

If a later evidence step invalidates a selected phrase, replace it from the highest-priority compatible reserve only when doing so preserves evidence quality and purchased scope. Do not pad mechanically.

### Final page/unit record should include

```text
page/unit ID
working URL/slug candidate
parent/section
page type
Page Job in plain language
primary cluster/query
secondary queries
intent mix
supporting pages
internal-link relationships
required product/category content scope
important evidence/uncertainty notes
semantic priority (analytical, not implementation schedule)
```

### Final phrase record should include

```text
phrase
frequency/demand evidence
cluster
primary page owner
intent/user job
source/provenance
Search evidence status
AI-search relevance/delta state where applicable
KEEP/HOLD state
delivery priority/order-scope state
notes
```

### Rule

Do not create thin pages merely because a micro-query exists. Do not merge materially different user jobs merely to reduce page count.

### Output

Canonical final truth feeding all client artifacts.

---

# STEP 19 — client deliverables

### Purpose

Turn canonical truth into artifacts the commissioner can use without reading internal evidence logs.

### Transferred KW-001 packaging rules

```text
ONE CURRENT TRUTH FEEDS ALL VIEWS
CORRECT DATABASE != CLIENT-USABLE WORKBOOK
INTERNAL TRACEABILITY != CLIENT NARRATIVE
RAW INTERNAL EVIDENCE != CLIENT KEYWORD COUNT
```

Expected artifact classes for the first rehearsal:

```text
1. standalone semantic core workbook limited to purchased final scope
2. clusters + query→page map
3. planned site structure / IA
4. Page Jobs + internal-link map
5. competitor semantic-gap evidence summary
6. Search-vs-AI decision summary
7. plain-Russian client report / handoff
```

Do not dump `RAW_OCCURRENCE_POOL` or `VALID_RESERVE_SET` into the ordinary client workbook unless that is an explicit purchased/custom artifact.

---

# STEP 20 — final QA / recipient acceptance

### Purpose

Verify both data correctness and usefulness of each promised artifact.

### Transferred KW-001 rules

```text
PACKAGE PASS != EVERY ARTIFACT PASS
DATA QA != WORKBOOK QA != RECIPIENT-USABILITY QA
RENDER/OPEN PASS != CONTENT COMPLETENESS
```

Check at minimum:

```text
final delivered phrase count <= DELIVERY_KEYWORD_CAP
no artificial padding to cap
no silent missing retained rows
no unexplained duplicate rows
region/provenance correct
all important clusters have page owners
no unexplained competing page owners
all planned pages have Page Jobs
Search/AI claim scopes correct
competitor-derived phrases have demand lineage
HOLD/uncertainty visible
reserve vs reject distinction preserved internally
workbooks open and are understandable
client-facing language explains completed work and result
```

### Output

`FINAL_QA` with per-artifact verdicts.

---

# STEP 21 — revision rehearsal + Kwork productization measurement

### Purpose

Prove the service can handle a realistic client correction without restarting unrelated paid work and measure whether the product is sellable.

### Revision test examples

```text
client removes one product family
client corrects geography
client says an assumed service/product is not offered
client changes a real commercial priority
client buys +N additional phrase capacity
```

For a paid +N expansion:

```text
first promote from VALID_RESERVE_SET by coverage-aware priority
re-run only affected Search/SERP/downstream evidence
new acquisition only if reserve is insufficient for legitimate scope
```

Recompute only affected downstream truth while preserving history.

Measure separately from client SEO result:

```text
RAW acquisition size
normalized unique size
sanitized candidate size
selected delivery size
reserve size
analyst/Work execution burden
provider request counts/cost
owner/operator actions
large-data handoffs
elapsed constraints
revision-sensitive stages
artifact-generation burden
```

This is Kwork productization economics, not the economics of the client website.

---

# STEP 22 — job close

Close only when:

```text
final deliverables complete
final delivered size reconciles to purchased scope
final QA passed or accepted exceptions recorded
revision test/real revision closed
no pending provider/Work/operator action
productization measurements recorded for a rehearsal
owner handoff complete
```

A job close does not automatically modify Level 1 or Level 2 methodology.

---

# Blood & Sand test-only migration gate — NOT A UNIVERSAL CLIENT STEP

The current Blood & Sand rehearsal began before the 2026-09-10 volume-pipeline revision.

Before its Step05 may resume, the job must backfill the new universal gates using already acquired evidence:

```text
existing Step03 RAW 79/79
-> Step03A normalization/dedup
-> Step03B sanitation
-> reconcile corrected Step04 family/queue authority against sanitized candidate layer
-> freeze explicit candidate/reserve counts
-> only then decide whether Step05 resumes
```

Do not replay Step03 provider calls solely because the pipeline changed.
Do not use the already executed Step05 E013 result to contaminate the historical Step04 correction; apply it only after the migration baseline is frozen.

After Step20 final result is frozen, the Blood & Sand rehearsal may open its sealed previous research for a separate regression comparison.

This comparison belongs in that `work/<JOB_ID>/` only and must not alter the already frozen from-scratch result before the comparison is recorded.

It asks:

```text
what KW-002 independently reproduced
what it newly discovered
what it missed
where it disagreed and why
whether the product methodology requires owner-approved correction before sale
```