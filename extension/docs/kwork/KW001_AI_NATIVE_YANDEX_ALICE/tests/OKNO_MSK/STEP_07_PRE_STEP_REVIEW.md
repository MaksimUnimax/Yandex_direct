# KW-001 / OKNO-MSK — STEP 07 PRE-STEP REVIEW

Date: 2026-08-29  
Status: **PRE-STEP REVIEW COMPLETE / CORRECTION REQUIRED BEFORE ROW-LEVEL CLEANUP / WAITING OWNER AUTHORIZATION**

This file is job-specific and disposable with the OKNO-MSK workspace.

## 1. Candidate next major step reviewed

The expected next analytical stage after Step 06 was:

```text
full row-level semantic cleanup
→ cleaned semantic set freeze
→ ordinary Yandex Search / SERP evidence
```

The review confirms that this is the correct analytical direction, but it cannot be executed honestly from the currently preserved Step-03 evidence.

Verdict:

```text
STEP_07_METHOD_DIRECTION = SUPPORTED
STEP_07_EXECUTION_READINESS = BLOCKED
STEP_07_BLOCKER = INCOMPLETE_PASS1_ROW_LEVEL_RAW_EVIDENCE
STEP_07_PRE_STEP_VERDICT = CORRECTION_REQUIRED
```

---

## 2. Why row-level cleanup is the next analytical direction

The current job has already completed:

```text
site/business discovery
first Wordstat acquisition pass
a family-level triage
bounded second Wordstat expansion
selective historical-demand diagnostics
```

Step 04's authoritative correction explicitly states that it did not perform a complete row-by-row classification and that full row-level cleanup remains incomplete.

The universal workflow also requires a cleaned semantic set before full ordinary-search/SERP work.

This ordering is methodologically reasonable because:

- Yandex recommends selecting search phrases that correspond to the user's real need and the site's answer/offer rather than treating raw query wording as sufficient targeting evidence.
- Yandex Wordstat top queries are acquisition evidence for queries containing the entered phrase and related queries; they are not themselves a final client semantic core.
- industry keyword-mapping/clustering practice separates relevance/intent filtering from later SERP-based page grouping: SERP overlap is valuable for deciding whether phrases belong to the same page, not for rescuing obviously irrelevant/off-scope raw phrases.

Current external sources checked:

OFFICIAL YANDEX:
- https://yandex.ru/support2/wordstat/ru/interface/new
- https://yandex.ru/support/webmaster/ru/recommendations/targeting?lang=ru
- https://yandex.ru/support/webmaster/ru/epos

INDUSTRY PRACTICE:
- https://ahrefs.com/blog/keyword-intent/
- https://ahrefs.com/blog/keyword-clustering/
- https://ahrefs.com/blog/keyword-mapping/
- https://www.semrush.com/blog/keyword-clustering/
- https://www.semrush.com/blog/keyword-mapping/

Method-origin classification:

```text
Wordstat top-query semantics = OFFICIAL
business/user-task relevance before targeting = OFFICIAL
row-level relevance filtering before SERP page grouping = INDUSTRY_PRACTICE + ANALYST_REASONING
SERP overlap for cluster/page-boundary validation = INDUSTRY_PRACTICE
exact OKNO-MSK row-state schema = owner-approved project workflow / job-specific application
```

---

## 3. Required row-level evidence for the intended cleanup

The corrected job discipline requires each candidate row to preserve enough provenance to answer at least:

```text
phrase
source seed/request provenance
provider count/observation
region/device
row source type (results vs associations where relevant)
decision state
reason code
family/cluster candidate
review note
```

Current row-state vocabulary for this job remains:

```text
KEEP
REVIEW
EXCLUDE_IRRELEVANT
EXCLUDE_SCOPE
EXCLUDE_MECHANICAL
```

Low frequency alone is not proof of irrelevance.

Associations remain vocabulary/acquisition evidence and are not automatically promoted to final semantic phrases.

---

## 4. Evidence audit of Step 03

Step 03 executed successfully:

```text
18/18 provider requests succeeded
0 failed_terminal
0 outcome_unknown
region = 213
DEVICE_ALL
numPhrases = 200
```

However, the current GitHub job workspace does not preserve every Step-03 provider phrase/count row.

Observed repository structure:

- `STEP_03_WORDSTAT_PASS1_EXECUTION_LOG.md` contains detailed execution evidence only through S04 and representative examples rather than complete result arrays.
- later S05-S18 checkpoint files preserve request metadata, branch summaries and representative examples.
- there is no Step-03 equivalent of the Step-05 `*_RAW_NORMALIZED.tsv` files.

Concrete example:

`STEP_03_WORDSTAT_PASS1_S15_CHECKPOINT.md` records:

```text
returned_results = 200
returned_associations = 11
```

but preserves only a short list of example phrases, not all 211 provider rows.

Therefore:

```text
STEP_03_ACQUISITION_SUCCESS = true
STEP_03_COMPLETE_ROW_DATA_IN_CURRENT_JOB_WORKSPACE = false
```

This is a data-preservation defect for the current rehearsal, not a provider-acquisition failure.

---

## 5. Why we must not proceed with "full cleanup" from summaries

If cleanup started now, the analyst would classify only the surviving examples and summaries while silently omitting many measured rows.

That would create false claims such as:

```text
full semantic cleanup complete
all raw Wordstat rows classified
cleaned core frozen from complete acquisition evidence
```

without the data needed to support them.

This would repeat the exact category of overstatement corrected in Step 04.

Therefore row-level cleanup is blocked until a complete working dataset exists.

---

## 6. Can the original Step-03 payload be recovered from the current YMB public batch contract?

Current accepted `WORDSTAT_BATCH_API_V1` actions are only:

```text
start
next
status
pause
resume
cancel
```

The current public command contract has no owner-facing action to export/retrieve all historical item payloads from a completed batch job.

Therefore this review does **not** assume that the original 2026-08-28 payload can be reconstructed from request IDs alone.

No hidden browser/local-storage manipulation is authorized as part of this job step.

---

## 7. Proposed correction: bounded pass-1 reacquisition for row-level working data

The cleanest available correction is to rerun the **same frozen 18 discovery seeds** under the same provider controls and preserve every returned row this time.

Important provenance rule:

```text
THIS IS NOT "RECOVERY OF THE ORIGINAL 2026-08-28 RAW PAYLOAD".
```

Wordstat `Top queries` represents the latest last-month/last-30-day window. A new request on 2026-08-29 is a new observation and may differ from the original 2026-08-28 results.

The reacquired rows must therefore be stored separately and labeled as:

```text
STEP_07_PASS1_REACQUISITION_CURRENT_OBSERVATION
```

Original Step-03 checkpoints remain untouched as historical execution evidence.

---

## 8. Frozen candidate correction manifest

Reuse exactly the original 18 Step-02 seeds:

```text
S01 пластиковые окна
S02 окна rehau
S03 французские окна
S04 окна п 44
S05 пластиковые двери
S06 остекление балконов
S07 остекление балкона с крышей
S08 остекление балкона п 46
S09 пластиковые окна митино
S10 остекление веранды
S11 алюминиевые окна
S12 аксессуары для пластиковых окон
S13 установка пластиковых окон
S14 ремонт пластиковых окон
S15 цены на пластиковые окна
S16 окна в рассрочку
S17 как выбрать пластиковые окна
S18 пластиковые окна от производителя
```

Proposed provider controls:

```text
method = getTop via durable WORDSTAT_BATCH_API_V1
regions = ["213"]
devices = ["DEVICE_ALL"]
numPhrases = 200
operators = NONE
seed_count = 18
maxRequests = 18
new_job_id = kw001-okno-msk-wordstat-pass1-reacquire-20260829
```

Estimated provider cost:

```text
18 × 0.02 RUB = 0.36 RUB
```

This is correction/reacquisition, not semantic expansion. No additional seeds are allowed in this correction batch.

---

## 9. Why not rerun only a subset

A subset would still leave the phrase universe incomplete for the families not reacquired.

Because the intended next claim is **full row-level cleanup across the acquired semantic universe**, the correction must either:

1. recover every original provider row, or
2. create a new complete bounded observation over the full frozen seed manifest.

The current public YMB contract does not expose option 1, so option 2 is the defensible route.

---

## 10. Why not combine reacquisition and cleanup in one step

They should remain separate gates.

Correction step:

```text
reacquire + preserve complete raw rows
```

Later analytical step:

```text
row-level KEEP/REVIEW/EXCLUDE classification
```

Separating them keeps acquisition facts immutable before subjective cleanup decisions and makes it possible to audit whether every row was actually considered.

---

## 11. What the correction will NOT do

```text
no new seed discovery
no third Wordstat expansion
no clustering
no page mapping
no SERP calls
no GenSearch calls
no final semantic decisions
no overwrite of original Step-03 checkpoints
no claim that reacquired rows equal the original 2026-08-28 rows
```

---

## 12. Adversarial review

### Objection: "Rerunning 18 requests duplicates work"

Correct. It duplicates provider acquisition because the original full row payload was not preserved in the job workspace.

Counterpoint: proceeding without complete data would make the next "full cleanup" unverifiable. The provider cost is small (`~0.36 RUB`), while the analytical consequence of missing hundreds/thousands of rows is large.

### Objection: "Could summaries be enough?"

No for a full row-level gate. They are enough for family-level reasoning, which Step 04 already completed, but not for a claim that every phrase was classified.

### Objection: "Will the rerun reproduce the original data?"

No guarantee. Official Wordstat top-query data is a rolling recent window. The new dataset is a fresh current observation and must be labeled accordingly.

---

## 13. Proposed next executable step

Do **not** begin row-level cleanup yet.

Next executable step after owner authorization:

```text
STEP 07A — PASS-1 RAW REACQUISITION / COMPLETE ROW PRESERVATION
```

Gate:

```text
18 frozen seeds submitted unchanged
18 terminal known outcomes
0 blind replay after uncertain outcomes
complete results + associations preserved per request
request provenance preserved
request count/cost recorded
no cleanup decisions during acquisition
original Step-03 evidence left intact
new observation clearly distinguished from original Step-03 observation
```

Only after Step 07A passes should a new pre-step review authorize:

```text
STEP 07B — FULL ROW-LEVEL SEMANTIC CLEANUP / CLEAN SET FREEZE FOR SERP
```

---

## 14. Pre-step verdict

```text
NEXT_ANALYTICAL_DIRECTION = SUPPORTED
ROW_LEVEL_CLEANUP_NOW = BLOCKED
CORRECTION_REQUIRED = true
CORRECTION = COMPLETE 18-SEED PASS1 REACQUISITION WITH FULL RAW PRESERVATION
PROPOSED_PROVIDER_REQUESTS = 18
ESTIMATED_PROVIDER_COST_RUB = 0.36
PROVIDER_REQUESTS_MADE_DURING_THIS_REVIEW = 0
OWNER_AUTHORIZATION_REQUIRED = true
```

No universal KW-001 methodology file was changed during this review.
