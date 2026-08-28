# KW-001 / OKNO-MSK — STEP REVIEW AND ERRORS LEDGER

Date created: 2026-08-28  
Status: **ACTIVE CASE MEMORY / READ BEFORE EVERY NEXT STEP**

Purpose: preserve concrete mistakes, corrections, good decisions and open risks discovered during this rehearsal so a future clean-context ChatGPT does not repeat them.

This file is case-specific. Universal reusable lessons live in `../../STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md`.

---

## Step 0 — mock order / scope freeze

### Correct

- Primary region was frozen before provider evidence.
- Public-site findings were not allowed to silently expand the mock client region.
- Unknown commercial priorities for standalone installation, repair, accessories and finance were explicitly retained as unknown.

### Error / correction

No material Step-0 defect currently recorded.

### Prevent repeat

Any later change to region, active offers or commercial priorities must be logged as mock-client revision, not silently substituted.

Status: **PASS / NO CURRENT CORRECTION REQUIRED**.

---

## Step 1 — site discovery + merged business/page model

### Correct

- Three discovery passes were compared rather than treating one pass as complete.
- `OPENED_READ` was separated from weaker discovery/inference states.
- Deep internal taxonomy and independent public/search-visible discovery were merged.
- GEO/public-subdomain findings and deep internal product/service families were both preserved.

### Error caught

The first single-pass discovery had been treated as sufficient too early. Later passes proved complementary blind spots.

### Correction made

`STEP_01_ACCEPTANCE.md` superseded the original single-pass acceptance and froze cross-channel discovery.

### Prevent repeat

Do not declare discovery saturation from a single non-trivial-site pass. Do not let a later deeper pass erase unique assets found by another channel.

Status: **PASS AFTER CORRECTION**.

---

## Step 2 — seed query plan

### Correct

- Seed manifest was frozen before Wordstat execution.
- All material merged business/search-job families had first-pass coverage.
- `numPhrases=200`, request caps and pass-2 caps were explicitly provisional productization controls.
- Second-pass reason codes were frozen before provider evidence.

### Error / communication defect caught

The diagnostic meaning of a seed was not explained strongly enough in live dialogue. The P-44 probe was challenged as something users supposedly would not search, and ChatGPT initially moved too close to accepting that intuition.

Provider evidence later showed real P-44 demand.

### Correction made

The governing distinction is now explicit:

```text
SEED = acquisition probe
SEED != final semantic keyword
```

### Prevent repeat

For every seed preserve the family/question it is testing. Do not remove a diagnostic probe merely because it sounds uncommon when measuring that uncertainty is the purpose.

Status: **PASS / EXPLANATION DISCIPLINE CORRECTED**.

---

## Step 3 — Wordstat pass #1

### Correct

- 18/18 frozen seeds executed unchanged.
- Region `213`, `DEVICE_ALL`, request count and cost truth were preserved.
- All provider items succeeded; no `OUTCOME_UNKNOWN` occurred.
- Final `batch.status` independently confirmed `COMPLETED` and itself made no provider request.
- Raw Wordstat was never declared final semantic core.
- Sparse P-46 payload was correctly treated as successful, not provider error.
- Associations such as stronger fitting/montage wording were kept only as later expansion signals.

### Concrete incidents/errors caught

1. Before batch start, active YMB service was wrong (`search` instead of `wordstat`). Bridge rejected with `SERVICE_NOT_ACTIVE`, `request_executed=false`.
2. During execution a send-button delivery failure occurred before provider execution. Safe replay was permitted only because execution truth was `request_executed=false`.

### Corrections made

- Permanent rule added: explicitly state active YMB service and execution mode immediately before every operator command.
- Replay decisions must be based on execution truth and accepted recovery policy, not on whether the UI looked like it failed.

### Prevent repeat

Never send a YMB command without explicit mode instructions. Never blindly replay `OUTCOME_UNKNOWN` or any attempt whose provider execution cannot be ruled out.

Status: **PASS / OPERATOR-DISCIPLINE LESSON RECORDED**.

---

## Step 4 — first post-Wordstat triage

### What was done correctly

- All 18 acquisition families were reviewed.
- Obvious semantic noise was separated from potentially valuable ambiguous demand.
- Repair, accessories, finance and standalone-installation demand were not silently promoted or deleted while client priority remained unknown.
- Associations were treated as vocabulary/expansion evidence rather than automatically accepted final keywords.
- No cluster/page decision was made before SERP.
- No new Wordstat/Search/GenSearch request was made.

### Defect 1 — output scope overstated

Original Step-4 status said `ANALYTICAL CLEANUP COMPLETE`.

This was too strong. The work reviewed seed families and recurring patterns, but did **not** create a complete row-level classification for every raw Wordstat phrase.

Correct status:

```text
FAMILY-LEVEL TRIAGE COMPLETE
CLEANUP RULES FROZEN
FULL ROW-LEVEL CLEANUP = NOT YET COMPLETE
```

### Defect 2 — `REJECT_OBVIOUS` conflated unrelated and out-of-scope

Example classes such as non-window meanings and valid queries naming locations outside the frozen Moscow scope were placed under the same rejection label.

Correct classification going forward:

```text
KEEP
REVIEW
EXCLUDE_IRRELEVANT
EXCLUDE_SCOPE
EXCLUDE_MECHANICAL
```

A valid query outside scope must remain distinguishable/recoverable if scope changes.

### Defect 3 — low-frequency statement was too absolute

Old wording: low frequency is never a rejection reason.

Correct wording:

```text
LOW_FREQUENCY_ALONE != PROOF_OF_IRRELEVANCE
```

Frequency can still contribute later to prioritization/page decisions together with business relevance, cluster size/traffic potential and regional SERP evidence.

### Defect 4 — some expansion candidates had excessive confidence

`монтаж окон` was called a strong candidate mainly because an association count was high. It is broader/ambiguous and can include other materials and employment/service meanings.

Correct status: `EXPANSION_PROBE_AMBIGUOUS`, not automatically a strong semantic candidate.

Other broad associations such as `стеклопакет` and `оконный завод` also remain probes/review candidates until business boundary and information gain are justified.

### External sources checked during retrospective audit

Official Yandex Wordstat semantics:
- https://aistudio.yandex.ru/docs/ru/search-api/api-ref/Wordstat/getTop
- https://aistudio.yandex.ru/docs/ru/search-api/operations/wordstat-gettop.html

Key provider facts used:
- GetTop returns popular queries containing the specified keyword plus queries similar to it.
- `associations` are similar queries, not an accepted semantic-core list.
- `regions` describes regions where queries were made; a phrase containing another location is not itself a provider error.

External methodology corroboration:
- https://www.semrush.com/blog/keyword-clustering/
- https://ahrefs.com/blog/keyword-mapping/
- https://ahrefs.com/blog/keyword-intent/

These sources support intent/topic grouping and business-value checks after collection; they do not prescribe our exact internal status labels.

### Corrected Step-4 authority

Use `STEP_04_METHOD_REVIEW_CORRECTION.md` and corrected `STEP_04_ACCEPTANCE.md` as authority over any conflicting wording in the original `STEP_04_PROGRESSIVE_CLEANUP_1.md`.

### Prevent repeat

- Do not call family-level triage full cleanup.
- Keep scope exclusions separate from semantic irrelevance.
- Do not use one frequency threshold as a universal semantic filter.
- Do not equate high association count with strong semantic candidacy.
- Before final semantic-core freeze, preserve row-level source + decision + reason.

Status: **CORRECTION_REQUIRED FOUND → CORRECTION IN PROGRESS / STEP 5 BLOCKED UNTIL RE-FREEZE**.

---

## Step 5 — Wordstat expansion pass #2

Status: **NOT STARTED**.

No Step-5 batch exists and no Step-5 provider request has been made.

Before authorization the pre-step report must prove for every proposed probe:

```text
source phrase/evidence
reason code
uncertainty tested
expected information gain
overlap/redundancy risk
business-scope status
why Wordstat is the right next evidence source instead of later SERP
```

The owner must explicitly authorize the frozen Step-5 manifest.

---

## Mandatory future-entry template

After every later major step append:

```text
## Step N — <name>

CORRECT
...

WRONG / DEFECT / INCIDENT
...

WHY IT HAPPENED
...

CORRECTION
...

PREVENT-REPEAT RULE
...

SOURCE/METHOD ORIGIN
...

STATUS
...
```

Do not remove historical mistakes after correction. Mark them superseded and preserve the lesson.

Markers:

```text
KW001_OKNO_MSK_STEP_ERROR_LEDGER_ACTIVE = true
KW001_OKNO_MSK_STEP4_RETRO_AUDIT_RECORDED = true
KW001_OKNO_MSK_STEP5_BLOCKED_UNTIL_STEP4_CORRECTION_REFROZEN = true
```
