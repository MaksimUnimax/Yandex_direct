# KW-001 / OKNO-MSK — STEP 07B ROW-LEVEL CLEANUP PRE-STEP REVIEW

Date: 2026-08-29
Status: **PRE-STEP REVIEW COMPLETE / WAITING POST-REVIEW OWNER AUTHORIZATION**

This file is job-specific and disposable with the OKNO_MSK workspace. It does not modify universal KW-001 rules.

## 1. Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page-structure recommendation for Yandex ordinary human search plus selective Yandex AI-search evidence, with client-ready artifacts and final QA.

## 2. Genuinely completed work

1. Mock order/scope freeze — COMPLETE.
2. Existing-site discovery and merged business/page model — COMPLETE after cross-channel correction.
3. Frozen first-pass seed/query plan — COMPLETE.
4. Repaired Wordstat pass #1 — COMPLETE: 18/18 items, 2153 results + 262 associations = 2415 provider rows preserved and verified, 0 outcome_unknown, 0 failed_terminal.
5. Wordstat acquisition coverage revalidation — COMPLETE: four preserved targeted probes rechecked against repaired base; 483 results + 67 associations = 550 probe rows; acquisition breadth accepted as sufficient; no additional Wordstat request required now.
6. Dynamics observations — 4/4 completely preserved and reusable as later context; they do not replace cleanup/Search validation.

Historical Step-03 acceptance remains superseded by Step 03R. Historical family-level Step-04 triage is retained only as prior analyst evidence and is not treated as full cleanup.

## 3. Remaining whole-job work

1. Full row-level cleanup of all collected Wordstat evidence with reconciled accounting.
2. Freeze the final working semantic set for ordinary Search.
3. Ordinary Yandex Search/SERP validation for material query/page-boundary questions.
4. Search-intent/SERP clustering and manual business reconciliation.
5. Keyword/topic to existing/proposed page mapping and page-action decisions.
6. Selective AI-search evidence only for material unresolved decisions.
7. Search-vs-AI comparison.
8. Priority model and implementation order.
9. Client deliverables.
10. Final QA and revision gate.

## 4. Current step goal

Create one auditable row-level semantic classification covering the complete collected Wordstat source universe so every source row is accounted for and every unique retained/reviewed phrase has explicit provenance and a defensible decision reason.

## 5. What this step solves

The job currently has complete acquisition evidence but does not yet have a complete row-by-row semantic decision layer.

This step closes the gap between:

```text
RAW WORDSTAT EVIDENCE
→ accountable relevance/scope/mechanical cleanup
```

It does not yet decide final page ownership, cluster boundaries, cannibalization, new-page actions, or AI-search priorities.

## 6. Required output for this step

The step may pass only when all of the following exist and reconcile:

```text
source rows expected = 2965
= 2415 repaired first-pass rows
+ 550 targeted-probe rows

all 2965 source rows ingested/accounted for
exact/conservative normalized duplicate groups identified
all duplicate provenance preserved
unique phrase working set produced
every unique phrase assigned exactly one current decision state
explicit reason code / review note where applicable
KEEP count known
REVIEW count known
EXCLUDE_IRRELEVANT count known
EXCLUDE_SCOPE count known
EXCLUDE_MECHANICAL count known
source-row → unique-phrase mapping preserved
all before/after counts reconcile
no unresolved source row silently dropped
```

Planned job-specific artifacts:

```text
STEP_07B_SOURCE_UNION.tsv
STEP_07B_UNIQUE_PHRASE_DECISIONS.tsv
STEP_07B_REVIEW_QUEUE.tsv
STEP_07B_RECONCILIATION.md
```

The exact filenames may be adjusted only inside this job workspace without changing the declared output semantics.

## 7. Relevant prior errors / corrections freshly re-read

### Error A — provider technical success was mistaken for project completion

What failed before:
The historical Step-03 pass had successful provider calls but did not preserve complete reusable rows for every item, and downstream analysis progressed anyway.

Non-repeat control here:
The cleanup input is accepted only from the complete repaired 2415-row base plus the four complete 550-row probe datasets. All 2965 source rows must reconcile before classification can pass.

### Error B — family-level triage was called complete cleanup

What failed before:
The historical Step-04 review analyzed families/patterns and representative material but was described too strongly.

Non-repeat control here:
No `cleanup complete` verdict until every source row maps to a unique phrase record and every unique phrase has an explicit current decision.

### Error C — different exclusion reasons were mixed into `REJECT_OBVIOUS`

What failed before:
Irrelevance, frozen-scope exclusion and mechanical noise/duplication were conflated.

Non-repeat control here:
Use distinct current states:

```text
KEEP
REVIEW
EXCLUDE_IRRELEVANT
EXCLUDE_SCOPE
EXCLUDE_MECHANICAL
```

### Error D — low frequency could be overused as a rejection signal

Non-repeat control here:

```text
LOW_FREQUENCY_ALONE != PROOF_OF_IRRELEVANCE
```

Count may be preserved as evidence and used later for priority, but no row is excluded only because its count is small.

### Error E — associations could be over-promoted

Non-repeat control here:
`association` remains acquisition/vocabulary provenance. It is not automatically a final keyword, but it also is not automatically discarded. Its actual phrase is classified by relevance/scope; ambiguous useful association vocabulary can remain REVIEW.

### Error F — methodology was previously validated only after owner challenge

Non-repeat control here:
Current external source review was performed before execution and is recorded below.

## 8. Input evidence and scope truth

Frozen rehearsal scope:

```text
site = https://okno-msk.ru/
primary region = Moscow
primary test focus = residential B2C
all visible product families = provisionally active
standalone installation priority = UNKNOWN
repair/service acquisition priority = UNKNOWN
accessories standalone priority = UNKNOWN
finance acquisition priority = UNKNOWN
new pages = allowed when later evidence justifies them
merge/reassignment = allowed when later evidence justifies them
```

Unknown commercial-priority directions must not be silently excluded or promoted; material phrases in those areas remain REVIEW when relevance is real but business scope/priority is unresolved.

Primary row evidence:

```text
STEP_03R_S01..S18_RAW_NORMALIZED.tsv = 2415 rows
STEP_05_P2_01..P2_04_RAW_NORMALIZED.tsv = 550 rows
TOTAL SOURCE ROWS = 2965
```

## 9. Method origin

### OFFICIAL

Yandex Wordstat current documentation:
- https://yandex.ru/support2/wordstat/ru/interface/new
- https://yandex.ru/support2/wordstat/ru/

Current semantics support treating Wordstat top queries as recent popular queries containing the entered phrase plus similar queries, with region/device filtering. This is acquisition evidence, not a provider-defined final SEO core.

Yandex Webmaster targeting guidance:
- https://yandex.ru/support/webmaster/ru/recommendations/targeting?lang=ru
- https://yandex.ru/support/webmaster/ru/service/queries-selection

These support selecting queries that reflect real user needs and are appropriate for what the site/business can answer or offer.

### INDUSTRY_PRACTICE

Current external corroboration:
- https://ahrefs.com/blog/keyword-intent/ — current 2026 guidance treats intent as an early keyword-strategy filter and explicitly rejects high-volume keywords when the business/site cannot realistically serve the intent.
- https://ahrefs.com/blog/keyword-clustering/ — clustering is grouping same/similar intent, commonly informed by SERP similarity; clustering remains interpretation, not a perfect mechanical truth.
- https://ahrefs.com/blog/keyword-mapping/ — multiple closely related same-intent keywords can map to one page; not one-keyword-one-page.
- https://www.semrush.com/blog/keyword-clustering/ — current clustering guidance centers on shared search intent and notes that subtle wording differences can represent different intent.
- https://www.semrush.com/blog/keyword-mapping/ — current mapping guidance selects relevant topics according to site/business goals and intent, then maps clusters to appropriate pages.

### PROJECT_TEST_VALIDATED / OWNER-APPROVED

```text
complete-source-row accounting before full-cleanup claim
separate exclusion reasons
preserve REVIEW for ambiguity
low frequency alone is not irrelevance proof
associations are vocabulary evidence, not automatic final keywords
business-priority unknowns remain unresolved
```

### ANALYST_HEURISTIC / JOB-SPECIFIC MECHANICS

There is no external Yandex/industry standard requiring the exact five status names used here or one universal string-normalization formula.

For this job the conservative exact-deduplication key will be limited to mechanical normalization that does not intentionally change meaning:

```text
Unicode normalization
trim leading/trailing whitespace
collapse repeated internal whitespace
case-normalize for exact-comparison key
preserve punctuation/word content in display phrase
```

No stemming, lemmatization, word reordering or punctuation deletion is used to declare duplicates. Near-synonyms remain separate phrases until later semantic/SERP handling.

## 10. Practical classification procedure

1. Read all 22 normalized source TSV files.
2. Preserve source item, source section (`result`/`association`), phrase, count, request/probe provenance, region/device and origin batch.
3. Build the complete 2965-row source union.
4. Create the conservative normalized exact-comparison key.
5. Group exact mechanical duplicates while retaining every occurrence/provenance and observed counts separately.
6. For each unique phrase inspect semantic meaning against the frozen business/site model and mock scope.
7. Assign one state:
   - `KEEP`: clearly relevant, in frozen scope, useful candidate for later Search/semantic work.
   - `REVIEW`: plausibly valuable/relevant but intent, business priority, scope boundary or page ownership cannot be safely resolved without later evidence/client input.
   - `EXCLUDE_IRRELEVANT`: meaning/user job does not materially match the business/service universe.
   - `EXCLUDE_SCOPE`: semantically valid demand, but outside a frozen explicit scope boundary.
   - `EXCLUDE_MECHANICAL`: exact duplicate/noise or other purely mechanical non-semantic removal reason.
8. Preserve reason codes and notes; do not use frequency alone as a reason.
9. Produce the review queue separately so uncertain valuable phrases cannot disappear.
10. Reconcile source rows, duplicate groups and all decision counts before any COMPLETE verdict.

## 11. Adversarial self-audit findings

### Finding 1 — old runbook wording conflicts with the newer owner-approved lesson ledger

`WORKING_RUNBOOK_FOR_CHATGPT.md` still contains the historical Step-5 vocabulary:

```text
KEEP / REJECT_OBVIOUS / REVIEW
```

The newer owner-approved `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` explicitly corrected this into separated exclusion reasons.

Classification:

```text
UNIVERSAL_RULE_REVIEW_REQUESTED = true
```

For this concrete job, the newer owner-approved correction controls the classification schema. The permanent runbook is not silently edited during this job because Layer A is owner-locked.

This documentation inconsistency is reported, not hidden.

### Finding 2 — current evidence does support starting cleanup

The old `STEP_07_PRE_STEP_REVIEW.md` said row-level cleanup was blocked because the complete pass-1 payload had not been preserved.

That blocker is now historical/stale:

```text
Step 03R = COMPLETE
2415/2415 repaired pass-1 rows preserved/verified
coverage revalidation = COMPLETE
550/550 targeted probe rows preserved
ROW_LEVEL_CLEANUP_ALLOWED = true
```

Therefore the correct current method verdict is not CORRECTION_REQUIRED for missing raw data.

### Finding 3 — not all commercial ambiguities can be solved during cleanup

Installation, repair, accessories and finance standalone priority remain UNKNOWN in the frozen mock-client answers. Relevant phrases in these families must therefore not be deleted merely because commercial priority is unknown. Where that uncertainty matters, use REVIEW.

### Finding 4 — cleanup must not become premature clustering/page mapping

Industry methodology supports intent/SERP evidence for grouping/page boundaries. Therefore this step removes only defensible irrelevant/scope/mechanical material and records preliminary meaning; it does not decide page splits/merges from lexical similarity.

## 12. Risks / uncertainties

```text
some phrases can have mixed intent from wording alone
some commercial families are valid but client priority remains unknown
same phrase may occur with different counts/provenance across source observations
association rows can contain adjacent but potentially useful vocabulary
exact string dedupe will intentionally not merge semantic near-duplicates
```

These risks are handled by provenance preservation and REVIEW rather than forced certainty.

## 13. What will NOT be done in this step

```text
no new Wordstat calls
no YMB interaction
no ordinary Yandex Search calls
no SERP clustering
no final page ownership
no merge/delete/new-page recommendation
no cannibalization diagnosis
no GenSearch/Alice evidence
no final priority score
no universal-rule edit
```

## 14. Proposed pass gate

The step passes only if:

```text
source rows expected = 2965
source rows ingested = 2965
source rows mapped/accounted = 2965
all exact duplicate provenance preserved = true
unique phrase count = known
unique phrase decision count = unique phrase count
KEEP + REVIEW + EXCLUDE_IRRELEVANT + EXCLUDE_SCOPE + EXCLUDE_MECHANICAL = unique phrase count
all material REVIEW reasons preserved = true
low-frequency-only exclusions = 0
association-auto-promotions = 0
silent dropped rows = 0
quantitative reconciliation = PASS
artifacts readable for next step = true
```

If any count fails to reconcile:

```text
STEP_07B = INCOMPLETE
NEXT_STEP_ALLOWED = false
```

## 15. Review verdict and authorization state

```text
STEP_07B_METHOD_DIRECTION = SUPPORTED
STEP_07B_INPUT_READINESS = PASS
STEP_07B_EXTERNAL_METHOD_REVIEW = COMPLETE
STEP_07B_PRIOR_ERROR_REREAD = COMPLETE
STEP_07B_YMB_INTERACTION = false
STEP_07B_PRE_STEP_REVIEW = COMPLETE
STEP_07B_EXECUTION_STARTED = false
OWNER_POST_REVIEW_AUTHORIZATION_REQUIRED = true
NEXT_STEP_ALLOWED = false until owner authorization and successful execution
```

The owner's earlier instruction to proceed initiated this mandatory pre-step review. Under the active KW-001 gate, cleanup execution itself requires explicit authorization after this report has been shown.