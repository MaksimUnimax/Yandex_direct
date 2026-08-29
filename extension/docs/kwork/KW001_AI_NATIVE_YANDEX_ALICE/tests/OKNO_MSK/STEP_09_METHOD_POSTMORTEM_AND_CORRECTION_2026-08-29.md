# KW-001 / OKNO-MSK — Step 09 method postmortem and correction

Date: 2026-08-29  
Status: **ACTIVE CORRECTION AUTHORITY FOR STEP 09**

This document records not only what must be done differently, but the causal chain explaining why the first Step-09 manifest model was wrong and which controls now block the same failure class.

## 1. Step-09 purpose remains unchanged

Step 09 exists to collect bounded, reproducible **ordinary Yandex Search** evidence for material intent, result-type and page-boundary questions before Step 10 clustering and Step 11 page ownership.

Step 09 is not final clustering and is not one paid Search request per keyword by definition. It may use bounded evidence tranches, but any inference from a direct Search probe to a non-probed phrase must be separately justified after observing SERP evidence.

## 2. What failed in the first Step-09 manifest model

The first builder created 40 REVIEW_SEARCH "evidence questions" by grouping rows primarily by `corrected_reason`, and for the broad reason `RETAINED_BUSINESS_BOUNDARY_NEEDS_SEARCH` by `corrected_reason + primary acquisition source`. It then chose one phrase from each such group with a lexical/source-centrality heuristic.

That design produced a numerically tidy first manifest:

```text
REVIEW_SEARCH rows = 944
cleanup reasons = 23
constructed review groups = 40
active duplicate groups = 8
total probes = 75
```

The machine QA then reported `coverage_complete=true` because every one of the 944 rows had been assigned to one of those constructed groups.

### Why this was wrong

`corrected_reason` is a **cleanup uncertainty reason**. It answers: "why did Step 07 refuse to make a final semantic decision here?"

It does **not** answer:

```text
what exact user task this phrase represents;
whether two phrases have the same search intent;
whether Yandex returns the same result type;
whether two queries can be targeted by one page;
whether evidence from one phrase transfers to another.
```

Likewise, `source_id` is **Wordstat acquisition provenance**. It records which discovery seed produced an occurrence. It is not a user-intent family and is not a page-boundary authority.

Therefore:

```text
same corrected_reason != same search intent
same source_id != same search intent
same lexical root != same SERP family
one direct probe != evidence for every row sharing those fields
```

## 3. False assumption that caused the error

The false assumption was:

> If a set of REVIEW rows share the same cleanup uncertainty code, and especially the same acquisition source, one lexically central phrase can act as a representative Search marker for that entire set.

This looked operationally attractive because it reduced 944 rows to 40 direct REVIEW probes while keeping perfect accounting traceability. The problem is that **accounting compression was silently treated as semantic representativeness**.

This repeats the previously known failure class:

```text
ACCOUNTING_QA != SEMANTIC_QA
```

The manifest was machine-complete, but its evidence-transfer premise had not been semantically validated.

## 4. External research that contradicts the failed premise

### 4.1 Yandex: clusters are about meaning / user intent

Direct source:

https://yandex.ru/support/webmaster/ru/service/queries-selection

Yandex describes clustering as automatic grouping of search queries that are close **by meaning or by user intent**. It does not say that acquisition provenance or an analyst's cleanup-reason code defines a Search cluster.

Supported method consequence:

```text
cleanup metadata may help organize review;
it cannot by itself establish a Search-intent/page cluster.
```

### 4.2 Rush Analytics: marker-query selection is not fully automatic

Direct source:

https://www.rush-analytics.ru/faq/kak-nayti-markernye-zaprosy

Rush explicitly states that marker queries for a site cannot currently be obtained **fully automatically** for sites of arbitrary size and calls this a major area of manual work in semantic selection.

Supported method consequence:

```text
automatic lexical/source centrality may propose or diversify samples;
it cannot self-approve a phrase as the authoritative marker for an intent family.
```

### 4.3 Ahrefs: intent clustering and term clustering are different things

Direct sources:

https://ahrefs.com/blog/keyword-clustering/
https://ahrefs.com/blog/keyword-clustering-tools/

Ahrefs defines keyword clustering as grouping keywords with the same or similar intent, commonly using the similarity of actual search results. It separately describes **term clustering** as grouping by common words/phrases and notes that term clustering is useful for trends/topics rather than proving same-page intent.

Supported method consequence:

```text
lexical similarity is not enough to prove same-page compatibility;
actual SERP evidence is the stronger boundary evidence.
```

### 4.4 Semrush: page-level clustering depends on intent and SERP similarity

Direct sources:

https://www.semrush.com/blog/keyword-clustering/
https://www.semrush.com/blog/keyword-manager-clustering-tool/
https://www.semrush.com/blog/what-are-methods-for-keyword-clustering-and-topic-modeling/

Semrush describes keyword clustering around common search intent and explains that SERP overlap is evidence that one content asset may serve multiple queries. It also explicitly distinguishes search-result logic from simple word similarity.

Supported method consequence:

```text
word similarity / cleanup class / acquisition source may assist review,
but cannot independently authorize evidence transfer or one-page treatment.
```

## 5. Concrete examples showing why the old grouping was unsafe

The failed builder produced examples such as:

```text
DIY_OR_PROCEDURAL_INTENT_NEEDS_CONTENT_FIT
69 rows
selected sample: `пластиковые двери видео`
```

A query about a door video cannot pre-authorize conclusions for every installation/manual/procedural phrase merely because Step 07 gave them the same uncertainty code.

Another example:

```text
RETAINED_BUSINESS_BOUNDARY_NEEDS_SEARCH + P2-01
190 rows
selected sample: `оконная фурнитура отзывы`
```

The phrase contains a review/comparison angle. Other fitting-related phrases may be transactional, component-specific, brand/entity, repair/replacement or informational. Wordstat provenance `P2-01` does not make those intents identical.

Another example:

```text
RETAINED_BUSINESS_BOUNDARY_NEEDS_SEARCH + S15
64 rows
selected sample: `шторы на пластиковые окна фото цены`
```

The fact that rows came from a price-oriented discovery seed does not mean they form one Search job.

These examples demonstrate the causal defect: **provenance/cleanup strata were promoted into semantic evidence families without SERP proof**.

## 6. Corrected meaning of the 75-query first tranche

The 75-query set is retained only as an **INITIAL_BOUNDED_SERP_TRANCHE**.

It is composed of three roles:

```text
REVIEW_STRATIFIED_SAMPLE
= a direct diagnostic Search query selected to diversify the first tranche across known uncertainty strata;
  it does not represent the other rows in that stratum.

NONEXACT_DUPLICATE_VARIANT
= a mandatory direct query used in an explicit pairwise duplicate-candidate comparison.

STEP1_BOUNDARY_OR_CORE_ANCHOR
= a direct control/contrast query for a declared architecture or core-intent question.
```

The semantic QA for the exact 75-query list is stored in:

`STEP_09_INITIAL_TRANCHE_SEMANTIC_QA.json`

Its exact ordered query-list fingerprint is frozen. A changed machine-generated list cannot silently inherit the old semantic approval.

## 7. Corrected 944-row coverage model

The old meaning of `coverage_complete=true` is withdrawn.

Correct states before provider Search are only:

```text
DIRECT_PROBE
= this exact REVIEW_SEARCH phrase is present in the paid initial tranche.

UNRESOLVED_UNPROBED
= this exact REVIEW_SEARCH phrase is not directly probed in the current tranche and remains unresolved.
```

Before SERP evidence:

```text
PRE_SERP_TRANSFER_ALLOWED = false
PRE_SERP_TRANSFER_LINKS = 0
FULL_SERP_EVIDENCE_COVERAGE = false
```

`TRACEABILITY_COMPLETE = true` means only that all 944 REVIEW_SEARCH rows remain present in the ledger and none disappeared. It must never be presented as proof that all 944 have Search evidence.

## 8. When evidence transfer is allowed after Search

A non-probed phrase may receive transferred evidence only through a separate explicit analytical decision after observed SERP data exists.

At minimum the transfer record must state:

```text
source probe/query;
target phrase;
observed source SERP evidence;
semantic reason the target is compatible;
why material modifiers do not change the user task;
whether direct target SERP is still required;
confidence;
reversible status before Step 10.
```

No rule of the form below is permitted:

```text
same corrected_reason => transfer
same source_id => transfer
same lexical tokens => transfer
same Wordstat family => transfer
no contradiction observed => transfer
```

## 9. Allowed use of cleanup reason, source and lexical similarity

They are not banned. Their role is narrowed to what they can actually support.

### `corrected_reason`

Allowed:
- sampling-stratum diversity;
- QA that every known uncertainty class is touched by the first tranche;
- analyst navigation.

Not allowed:
- automatic intent cluster;
- automatic SERP-family assignment;
- automatic evidence transfer.

### `source_id`

Allowed:
- provenance;
- sampling diversity;
- diagnosing which acquisition roots produced uncertainty.

Not allowed:
- page ownership;
- same-intent proof;
- same-page proof.

### lexical similarity / token overlap

Allowed:
- candidate discovery;
- sampling/tie-breaking;
- flags for later comparison.

Not allowed:
- same-intent proof;
- same-page proof;
- non-exact duplicate merge;
- pre-SERP evidence transfer.

## 10. Second failure: the attempted one-block `start + 75 next` execution plan

After freezing the first manifest, a single Manual block was prepared containing:

```text
start
next x75
status
```

The generic Search batch runtime can execute commands serially and durably store each provider payload. However, the accepted **Step-09 project gate is stricter** than generic transport safety.

Step 09 requires:

```text
one paid next
-> known governed outcome
-> complete raw payload saved
-> normalized ranked rows readable
-> observed row count reconciled
-> project-level completeness check
-> only then another paid next
```

The false assumption here was:

> Durable worker persistence is equivalent to Step-09 analytical completeness verification.

It is not.

This repeats the Step-03 causal lesson:

```text
REQUEST_SUCCEEDED != PROJECT_RESULT_COMPLETE
TRANSPORT_PERSISTED != ANALYTICALLY_VERIFIED
```

Therefore the one-block 75-next execution plan is rejected for Step 09 even though generic multi-command transport is serial.

No such provider run was executed; provider requests and cost remain zero.

## 11. Correct provider execution model

The current Step-09 execution contract is:

```text
START
= creates the bounded job; expected provider requests = 0.

NEXT
= admits at most one ordinary Search provider request.

AFTER EACH NEXT
= inspect result envelope and durable payload;
= verify request_executed/outcome;
= verify raw Search evidence is present;
= verify normalized ranked rows and observed count;
= persist job-specific evidence reference;
= stop on incomplete or OUTCOME_UNKNOWN;
= only then issue the next NEXT.

STATUS / PROJECTION / OVERLAP
= non-provider inspection actions only.
```

A future product-level feature may automate the project completeness check, but until that feature itself is validated, Step 09 remains interaction-gated per paid `next`.

## 12. Corrected machine gates

The builder/workflow now enforce:

```text
TRACEABILITY_ROWS = 944
TRACEABILITY_COMPLETE = true
FULL_SERP_EVIDENCE_COVERAGE = false
PRE_SERP_TRANSFER_LINKS = 0
SEMANTIC_SAMPLE_QA_PASS = true
PROVIDER_EXECUTION_SCOPE = INITIAL_BOUNDED_TRANCHE_ONLY
REQUEST_CAP_OK = true
BUDGET_CAP_OK = true
```

The machine gate is intentionally prevented from claiming semantic resolution of all 944 rows.

## 13. Why the correction keeps the 75 direct queries instead of discarding them

The problem was not that every chosen query was useless. The problem was the **scope of inference attached to them**.

The same direct query set remains useful for a first diagnostic tranche because it:

- samples every known Step-07 uncertainty stratum;
- directly checks all eight active non-exact duplicate groups;
- includes declared Step-01/core comparison anchors;
- fits inside the authorized 80-request / 39.04-RUB safety ceiling;
- can reveal which uncertainty areas require deeper second-tranche Search.

But it no longer claims to be sufficient evidence for all 944 REVIEW_SEARCH rows.

## 14. New non-repeat controls

### Control A — metadata is not an intent cluster

Before any grouping field is allowed to transfer SERP evidence, ask:

```text
Does this field describe the user's search task / observed SERP compatibility?
Or does it merely describe our acquisition/cleanup process?
```

If it is process metadata, it cannot authorize evidence transfer.

### Control B — sample selection and cluster authority are separate

A machine may propose/diversify a first-tranche sample. It cannot self-approve that sample as a marker for non-probed phrases.

### Control C — traceability and evidence coverage use different names

```text
TRACEABILITY_COMPLETE
!=
FULL_SERP_EVIDENCE_COVERAGE
```

The second may become true only after direct Search evidence and governed transfer/direct-probe decisions actually cover the intended scope.

### Control D — semantic QA is independent of accounting QA

Provider/query count/cost/row-accounting PASS cannot self-accept sample representativeness or intent conclusions.

### Control E — no pre-SERP transfer

`PRE_SERP_TRANSFER_LINKS` must equal zero.

### Control F — project completeness before next paid request

One `next` is followed by one project completeness check. Generic serial runtime behavior is necessary but not sufficient.

### Control G — new failure class triggers causal correction

If a later QA finds another false inference class, do not patch only the affected phrase. Record the causal assumption, fix the method/class, rerun all affected artifacts, and preserve the lesson here.

## 15. Current corrected Step-09 state

```text
owner authorization for Step 09 = received
initial direct query list = 75
initial tranche semantic QA = PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY
REVIEW_SEARCH total = 944
direct REVIEW_SEARCH rows in current 75-query tranche = determined by corrected builder
non-probed REVIEW_SEARCH rows = remain UNRESOLVED_UNPROBED
full SERP evidence coverage = false
pre-SERP transfer links = 0
provider Search requests executed = 0
provider cost incurred = 0 RUB
Step 09 complete = false
Step 10 allowed = false
```

## 16. Canonical lesson

```text
A CLEANUP REASON IS NOT A SEARCH-INTENT CLUSTER.
ACQUISITION PROVENANCE IS NOT A SEARCH-INTENT CLUSTER.
LEXICAL CENTRALITY IS NOT SERP COMPATIBILITY.
TRACEABILITY IS NOT EVIDENCE COVERAGE.
DURABLE PROVIDER PERSISTENCE IS NOT PROJECT COMPLETENESS QA.
```

The corrected method does not prohibit automation. It prohibits automation from claiming evidence authority that its inputs do not causally support.
