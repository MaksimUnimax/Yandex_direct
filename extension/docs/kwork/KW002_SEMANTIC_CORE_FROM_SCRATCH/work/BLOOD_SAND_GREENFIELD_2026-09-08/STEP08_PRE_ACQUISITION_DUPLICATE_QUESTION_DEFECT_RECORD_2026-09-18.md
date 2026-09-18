# KW-002 / BLOOD & SAND — STEP08 PRE-ACQUISITION DUPLICATE-QUESTION DEFECT RECORD

Date: 2026-09-18
Status: **CURRENT / BLOCKING / FULL-VOLUME REWORK REQUIRED**

## 1. Why this record exists

ChatGPT Work completed the first Step08 pre-acquisition reconciliation with full
mechanical accounting:

```text
STEP08_ELIGIBLE = 794/794
LINKED_STEP07_PROVENANCE = 1060/1060
SILENT_SKIP = 0
PROVIDER_REQUIRED_CANDIDATES = 749
PROVIDER_SEEDS = 386
PROVIDER_SEED_MEMBER_LINKS = 749
WORDSTAT_CALLS = 0
```

The result passed Work QA and was staged/published canonically. During Main Chat
return QA the first mechanical checks also passed.

Before any Wordstat command was released, a later semantic audit examined the
actual seed-level information questions and found a systematic provider-queue
design defect.

The earlier Main Chat PASS was immediately invalidated. No provider traffic had
started.

## 2. Defect

The R1 producer treated literal provider-query uniqueness as too close to
information-question uniqueness.

Full queue diagnostic:

```text
PROVIDER_SEEDS = 386
UNIQUE_LITERAL_PROVIDER_PHRASES = 386

UNIQUE_DECLARED_OPEN_INFORMATION_QUESTIONS = 162
DUPLICATE_OPEN_QUESTION_GROUPS = 72
SEEDS_INSIDE_DUPLICATE_QUESTION_GROUPS = 296
RAW_EXCESS_IF_NAIVELY_ONE_SEED_PER_QUESTION = 224
```

The number `224` is only a diagnostic. It is NOT permission to collapse the
queue blindly to 162 seeds.

Some probes sharing a high-level topic may legitimately require different:

- referent scope;
- product qualification;
- recall vs precision mode;
- operator shape;
- collision diagnostic;
- evidence boundary.

The blocking defect is narrower and more precise:

> multiple literal seed rows were made unconditional future provider candidates
> under the same declared acquisition question without a dependency model and
> without proving why each child must execute even after the broader/parent
> observation becomes available.

## 3. Representative regressions

Representative examples are regression tests, not manual patch targets.

### Kres branch

Two separate seeds were generated while both declared the same demand question
for `Крес`.

One broad qualified Kres probe may make the second product-title-shaped probe
unnecessary.

### Om/Aum branch

Twenty separate D500 collision-diagnostic seeds declared the same information
question for `символ Ом / Аум`.

The phrases differed, but the R1 contract did not establish a parent/child
execution order or prove why every child had to execute independently after a
parent result.

### Other full-queue concentrations

The same mechanism appears in groups labelled around:

- `обереги`;
- `амулеты`;
- `талисманы`;
- `руны`;
- `подкова`;
- Muslim amulet/obereg topics;
- Alatyr;
- automobile amulet topics;
- Zvezda Lada;
- luck/vезение topics;
- several rune/name families.

Do not patch these labels specially. Re-run the complete provider-required
universe under the corrected dependency rule.

## 4. Root cause

The R1 Step08 preparation had:

- candidate-level information gain;
- reuse-first logic;
- unique literal provider phrases;
- operator/depth/outcome contracts;

but did not require:

```text
ACQUISITION_QUESTION_ID
PARENT_SEED_ID
RELEASE_STATE
CONDITIONAL_TRIGGER
DISTINCT_INFORMATION_GAIN_WITHIN_SAME_QUESTION
```

Therefore the producer could create several different phrases for one declared
question and still pass mechanical duplicate checks.

```text
UNIQUE QUERY STRING != UNIQUE INFORMATION QUESTION
PROVIDER-SEED UNIQUENESS != PROVIDER-QUEUE EFFICIENCY
```

## 5. Permanent method correction

Universal corrections are now recorded in:

- `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md` as F05-18;
- `LEVEL2/STEP_05_TARGETED_EXPANSION_AND_PROVIDER_EXECUTION_GATE.md`;
- `LEVEL2/STEP_08_COMPETITOR_DERIVED_WORDSTAT_VALIDATION.md`;
- `LEVEL2/STEP_RULES_INDEX.md`.

Required provider release states include:

```text
INITIAL_REQUIRED
INDEPENDENT_REQUIRED
CONDITIONAL_AFTER_PARENT
REUSE_EXISTING_EVIDENCE
HOLD
```

A narrower child may be released only after the parent result is durably
persisted/read back and a new reconciliation proves the child question remains
unanswered.

## 6. Affected artifacts

Current R1 artifacts are preserved as historical evidence but are superseded for
provider release:

- `STEP08_CANDIDATE_PRE_ACQUISITION_RECONCILIATION.csv`
- `STEP08_PROVIDER_SEED_MANIFEST.csv`
- `STEP08_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX.csv`
- `STEP08_PRE_ACQUISITION_QA.md`
- `STEP08_PREPARATION_HANDOFF_MANIFEST.json`
- historical Main Chat return QA;
- historical provider execution plan.

The existing-evidence reuse register remains evidence input for R2 but does not
self-certify final R2 closure.

## 7. Rework scope

R2 must process:

```text
STEP08_ELIGIBLE_CANDIDATES = 794/794
PROVIDER_REQUIRED_R1_CANDIDATES = 749/749
R1_PROVIDER_SEEDS = 386/386
R1_DUPLICATE_OPEN_QUESTION_GROUPS = 72/72
```

R2 must NOT simply deduplicate identical `unresolved_question` text.

For each question/probe relationship, decide:

1. is one broader safe probe sufficient?
2. are separate probes truly independent because they ask different
   referent/operator/scope questions?
3. should a narrower probe become `CONDITIONAL_AFTER_PARENT`?
4. was the question itself too broad and should be split into distinct
   acquisition-question identities?
5. can existing durable evidence remove the question entirely?

## 8. Provider boundary

```text
WORDSTAT_CALLS = 0
YMB_SEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
GENSEARCH_CALLS = 0
STEP08_PROVIDER_EXECUTION_STARTED = false
STEP09_STARTED = false
```

No R1 provider seed is currently authorized for execution.

## 9. Current gate

```text
STEP08_PRE_ACQUISITION_R1 = REWORK_REQUIRED
STEP08_PROVIDER_EXECUTION = BLOCKED_NOT_STARTED
NEXT = STEP08_PRE_ACQUISITION_DEPENDENCY_REWORK_R2_IN_WORK
```
