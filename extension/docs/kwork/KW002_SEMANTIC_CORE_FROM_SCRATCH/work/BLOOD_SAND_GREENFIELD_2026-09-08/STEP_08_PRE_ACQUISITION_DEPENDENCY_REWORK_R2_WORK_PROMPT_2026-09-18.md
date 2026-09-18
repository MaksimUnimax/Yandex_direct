# KW-002 / BLOOD & SAND — STEP08 PRE-ACQUISITION DEPENDENCY REWORK R2 — CHATGPT WORK EXECUTION PROMPT

WORK_ID: `KW002_STEP08_PRE_ACQUISITION_DEPENDENCY_REWORK_R2_2026-09-18`

CONTINUE THE EXISTING KW-002 BLOOD & SAND GREENFIELD SEMANTIC-CORE REHEARSAL.

THIS IS A FULL-VOLUME STEP08 PRE-ACQUISITION REWORK.

THIS IS NOT A NEW PROJECT.
THIS IS NOT FRESH METHODOLOGY RESEARCH.
THIS IS NOT WORDSTAT EXECUTION.
THIS IS NOT STEP09.
THIS IS NOT FINAL INTENT.
THIS IS NOT FINAL CLUSTERING.
THIS IS NOT QUERY→PAGE OWNERSHIP.
THIS IS NOT SITE ARCHITECTURE.

Repository:

`MaksimUnimax/Yandex_direct`

Branch:

`roadmap/kwork-productization-2026-08-28`

Job root:

`extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

# ======================================================================
# 0. NARROW TECHNICAL PREFLIGHT
# ======================================================================

Fetch/read the CURRENT LIVE remote branch.

Do NOT redo Main Chat governance.
Do NOT reread all Level1 rules.
Do NOT redo external web research.

Read and obey exactly:

- `STEP_08_PRE_ACQUISITION_R2_PRE_HANDOFF_MANIFEST_2026-09-18.json`
- `STEP_08_PRE_ACQUISITION_R2_OUTPUT_SCHEMA_CONTRACT_2026-09-18.json`
- `STEP08_PRE_ACQUISITION_DUPLICATE_QUESTION_DEFECT_RECORD_2026-09-18.md`
- `LEVEL2/STEP_08_COMPETITOR_DERIVED_WORDSTAT_VALIDATION.md`
- the current R2 execution release record.

Also use the R1 preparation artifacts named by the manifest as historical/input
authority for the rework.

Verify:

1. the R2 manifest identities;
2. the R1 pre-handoff manifest identity;
3. all 21 frozen data/input identities inherited through that R1 manifest;
4. the R1 canonical Step08 output identities named by the R2 manifest.

A later live HEAD caused only by Main Chat publishing R2 control/release files is
expected.

If a frozen DATA input materially differs:

`AUTHORITY_DRIFT`

and stop.

# ======================================================================
# 1. WHY R2 EXISTS
# ======================================================================

R1 completed mechanical full-volume accounting correctly:

```text
STEP08_ELIGIBLE = 794/794
PROVIDER_REQUIRED_CANDIDATES = 749
R1_PROVIDER_SEEDS = 386
UNIQUE_LITERAL_PROVIDER_PHRASES = 386
WORDSTAT_CALLS = 0
```

But late Main Chat semantic QA found:

```text
UNIQUE_DECLARED_OPEN_INFORMATION_QUESTIONS = 162
DUPLICATE_OPEN_QUESTION_GROUPS = 72
SEEDS_INSIDE_DUPLICATE_QUESTION_GROUPS = 296
```

These counts demonstrate a systematic risk but DO NOT imply that the correct
queue contains exactly 162 provider probes.

The defect is:

```text
UNIQUE QUERY STRING
WAS TREATED TOO CLOSE TO
UNIQUE INFORMATION QUESTION
```

and broad/parent plus narrower/child probes could all be made future provider
candidates at once without a dependency model.

R2 must correct the mechanism across the complete affected universe.

# ======================================================================
# 2. FULL-VOLUME BOUNDARY
# ======================================================================

Process all:

```text
STEP08_ELIGIBLE_CANDIDATES = 794/794
R1_PROVIDER_REQUIRED_CANDIDATES = 749/749
R1_PROVIDER_SEEDS = 386/386
R1_DUPLICATE_OPEN_QUESTION_GROUPS = 72/72
```

Hard rule:

```text
REPRESENTATIVE DEFECT EXAMPLE != PATCH TARGET
REPRESENTATIVE DEFECT EXAMPLE = REGRESSION TEST
```

Do NOT patch only Om/Aum, Kres, amulet, obereg, talisman or rune examples.

Do NOT sample.

# ======================================================================
# 3. DO NOT NAIVELY COLLAPSE TO 162 QUESTIONS
# ======================================================================

Identical or similar R1 `unresolved_question` text is a diagnostic signal only.

Two probes with the same high-level wording may legitimately be distinct when
they have materially different:

- referent;
- qualification scope;
- broad-recall vs precision purpose;
- operator question;
- collision question;
- product vs informational scope;
- evidence boundary.

Therefore R2 must decide for every relationship:

```text
ONE PROBE SUFFICIENT
OR
MULTIPLE INDEPENDENT PROBES JUSTIFIED
OR
PARENT WITH CONDITIONAL CHILDREN
OR
QUESTION MUST BE SPLIT INTO DISTINCT QUESTION IDENTITIES
OR
NO PROVIDER PROBE NEEDED AFTER EVIDENCE REUSE
```

Do not optimize toward a predetermined number of R2 probes.

# ======================================================================
# 4. ACQUISITION-QUESTION MODEL
# ======================================================================

Create stable R2 acquisition-question identities:

`S08AQ0001...`

Each acquisition question must state the actual evidence need, not a generic
topic sentence.

A question identity must distinguish materially different evidence questions.

Example conceptual distinction:

```text
broad topic vocabulary around X
!=
physical-product-qualified demand around X
!=
exact-form collision between X and Y
```

But do not split merely because literal candidate wording differs.

For every provider-needed candidate, map it to an acquisition question.

# ======================================================================
# 5. PROVIDER PROBE RELEASE STATES
# ======================================================================

Every surviving R2 provider probe receives exactly one:

```text
INITIAL_REQUIRED
INDEPENDENT_REQUIRED
CONDITIONAL_AFTER_PARENT
HOLD_NOT_RELEASED
```

All rows must also have:

`provider_execution_released = false`

## INITIAL_REQUIRED

Use when the probe is the first/broadest safe observation required for its
question and later evidence may determine whether children are still needed.

## INDEPENDENT_REQUIRED

Use only when the probe answers a materially distinct evidence scope that a
parent/sibling cannot answer.

If several nonconditional probes share one acquisition question, each must have
a specific nonblank:

`distinct_information_gain_within_same_question`

explaining why all must run independently.

## CONDITIONAL_AFTER_PARENT

Use when a narrower probe may become unnecessary after another probe.

It MUST have:

- `parent_seed_id`;
- `conditional_trigger`.

Canonical trigger semantics:

```text
PARENT ACTUAL RESULT
-> COMPLETE RAW PERSISTENCE
-> REMOTE READBACK
-> RECONCILE AGAINST CHILD QUESTION
-> CHILD STILL UNANSWERED
=> ONLY THEN CHILD MAY RECEIVE A LATER MAIN CHAT RELEASE
```

A conditional child is NOT provider-ready now.

## HOLD_NOT_RELEASED

Use for unresolved cases that should not be executed until another authority
resolves the uncertainty.

# ======================================================================
# 6. PARENT / CHILD GRAPH QA
# ======================================================================

The R2 dependency graph must satisfy:

```text
ALL CONDITIONAL PARENTS EXIST = true
DEPENDENCY_CYCLES = 0
SELF_PARENT = 0
ORPHAN_CONDITIONAL_CHILD = 0
CONDITIONAL_CHILD_WITHOUT_TRIGGER = 0
```

Prefer the smallest dependency depth necessary.

Do not build dependency chains merely for elegance.

# ======================================================================
# 7. EXISTING EVIDENCE REUSE REMAINS FIRST
# ======================================================================

R2 may correct R1 reuse/provider decisions when evidence supports it.

Before retaining any provider question, re-evaluate current durable evidence
under the same strict scope rule:

```text
BROAD EVIDENCE != QUALIFIED QUESTION ANSWER
RELATED EVIDENCE != CLOSURE
```

Reuse requires durable evidence provenance.

Do not invent provider observations from derived labels.

If R1 incorrectly required a provider call even though durable evidence already
answers the same question, correct it in R2 and record the R1→R2 transition.

# ======================================================================
# 8. R1 SEED DISPOSITION — 386/386
# ======================================================================

Every R1 seed ID must appear exactly once in:

`STEP08_R1_SEED_DISPOSITION_R2.csv`

Allowed dispositions:

```text
RETAINED_AS_INITIAL
RETAINED_AS_INDEPENDENT
RETAINED_AS_CONDITIONAL
MERGED_INTO_R2_SEED
CANCELLED_AS_REDUNDANT
CANCELLED_BY_REUSE
HOLD
```

No R1 seed may disappear silently.

A merged/cancelled seed must retain an explicit reason and the relevant R2
question/seed identity where applicable.

# ======================================================================
# 9. PROVIDER SEED DESIGN
# ======================================================================

Use the frozen current provider facts from Main Chat's R1 source trace; do not
redo web research.

Current planning authority remains:

```text
provider = Yandex Wordstat GetTop
region = 225 / Russia
devices = DEVICE_ALL
numPhrases supported = 1..2000
estimated direct price = 0.02 RUB per GetTop request at frozen snapshot
```

Research modes:

```text
DISCOVERY_RECALL_FIRST
PRECISION_VALIDATION
EXACT_FORM_TEST
COLLISION_DIAGNOSTIC
```

Operators and depth must follow the actual question.

Do not downgrade depth to fit context.

Do not select 2000 just because it is maximum.

Do not use OR merely to reduce request count.

# ======================================================================
# 10. REQUIRED OUTPUT 1 — CANDIDATE R2
# ======================================================================

Create:

`STEP08_CANDIDATE_PRE_ACQUISITION_RECONCILIATION_R2.csv`

Exactly:

```text
ROWS = 794
DISTINCT candidate_id = 794
INPUT ID SET MATCH = EXACT
SILENT_SKIP = 0
```

Use the R2 schema exactly.

# ======================================================================
# 11. REQUIRED OUTPUT 2 — REUSE R2
# ======================================================================

Create:

`STEP08_EXISTING_EVIDENCE_REUSE_REGISTER_R2.csv`

Preserve all materially used durable evidence and record whether each row is
unchanged from or corrected relative to R1.

# ======================================================================
# 12. REQUIRED OUTPUT 3 — ACQUISITION QUESTIONS
# ======================================================================

Create:

`STEP08_PROVIDER_ACQUISITION_QUESTION_REGISTER_R2.csv`

One row per R2 acquisition-question identity.

Report:

- question scope;
- referent/qualification scope;
- member candidates;
- current evidence state;
- provider requirement state;
- root probe IDs;
- conditional child IDs;
- one-probe / parent-child / multiple-independent policy;
- why neighboring questions were not merged.

# ======================================================================
# 13. REQUIRED OUTPUT 4 — PROVIDER SEEDS R2
# ======================================================================

Create:

`STEP08_PROVIDER_SEED_MANIFEST_R2.csv`

This is the corrected dependency-aware future provider queue.

No R2 provider seed is authorized for execution by Work.

```text
provider_execution_released = false FOR ALL
```

# ======================================================================
# 14. REQUIRED OUTPUT 5 — R1 DISPOSITION
# ======================================================================

Create exactly 386 rows in:

`STEP08_R1_SEED_DISPOSITION_R2.csv`

Hard gates:

```text
R1_SEEDS_ACCOUNTED = 386/386
DISTINCT_R1_SEED_ID = 386
SILENT_R1_SEED_DROP = 0
```

# ======================================================================
# 15. REQUIRED OUTPUT 6 — REGRESSION MATRIX R2
# ======================================================================

Create:

`STEP08_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX_R2.csv`

It must include the new F05-18 regression and applicable older failures.

F05-18 must explicitly test:

```text
PROVIDER_SEEDS_WITHOUT_ACQUISITION_QUESTION_ID = 0
DUPLICATE_INFORMATION_QUESTIONS_WITHOUT_MERGE_OR_JUSTIFICATION = 0
UNCONDITIONAL_CHILD_PROBES_WHERE_PARENT_MAY_ANSWER = 0
CONDITIONAL_CHILD_WITHOUT_VALID_PARENT = 0
CONDITIONAL_CHILD_WITHOUT_TRIGGER = 0
DEPENDENCY_CYCLES = 0
MULTIPLE_ROOT_PROBES_SAME_QUESTION_WITHOUT_DISTINCT_INFO_GAIN = 0
```

# ======================================================================
# 16. REQUIRED OUTPUT 7 — QA R2
# ======================================================================

Create:

`STEP08_PRE_ACQUISITION_QA_R2.md`

Report at least:

```text
WORK_START_REMOTE_HEAD
WORK_PRE_HANDOFF_REMOTE_HEAD
AUTHORITY_DRIFT_STATUS

STEP08_ELIGIBLE_ACCOUNTED = 794/794
R1_PROVIDER_REQUIRED_CANDIDATES_ACCOUNTED = 749/749
R1_PROVIDER_SEEDS_ACCOUNTED = 386/386
R1_DUPLICATE_OPEN_QUESTION_GROUPS_REVIEWED = 72/72

R2_ACQUISITION_QUESTIONS = n
R2_PROVIDER_SEEDS_TOTAL = n
R2_INITIAL_REQUIRED = n
R2_INDEPENDENT_REQUIRED = n
R2_CONDITIONAL_AFTER_PARENT = n
R2_HOLD_NOT_RELEASED = n

R1_RETAINED_AS_INITIAL = n
R1_RETAINED_AS_INDEPENDENT = n
R1_RETAINED_AS_CONDITIONAL = n
R1_MERGED_INTO_R2_SEED = n
R1_CANCELLED_AS_REDUNDANT = n
R1_CANCELLED_BY_REUSE = n
R1_HOLD = n

INITIAL_WAVE_PROVIDER_REQUESTS = n
MAX_FUTURE_REQUESTS_IF_ALL_CONDITIONAL_CHILDREN_TRIGGER = n
CURRENT_INITIAL_WAVE_ESTIMATED_COST_RUB = n
MAX_FUTURE_ESTIMATED_COST_RUB = n

DEPENDENCY_CYCLES = 0
ORPHAN_CONDITIONAL_CHILDREN = 0
DUPLICATE_INFORMATION_QUESTIONS_WITHOUT_MERGE_OR_JUSTIFICATION = 0
UNCONDITIONAL_CHILD_PROBES_WHERE_PARENT_MAY_ANSWER = 0
MULTIPLE_ROOT_PROBES_SAME_QUESTION_WITHOUT_DISTINCT_INFO_GAIN = 0

WORDSTAT_CALLS = 0
YMB_SEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
GENSEARCH_CALLS = 0
STEP08_PROVIDER_EXECUTION_STARTED = false
STEP09_STARTED = false
```

Also report the largest R2 acquisition-question groups and their dependency
shape for adversarial review.

Score all ten KW-002 quality dimensions 0..10.

# ======================================================================
# 17. REQUIRED OUTPUT 8 — R2 HANDOFF MANIFEST
# ======================================================================

Create:

`STEP08_PREPARATION_HANDOFF_MANIFEST_R2.json`

Include:

- Work ID;
- start/pre-handoff HEAD;
- frozen input identities;
- all eight output files;
- row counts;
- SHA-256 values;
- R2 question/probe/release-state counts;
- R1 disposition counts;
- zero-provider-call declaration;
- staging target;
- ZIP hash reported externally after packaging;
- Main Chat acceptance = PENDING.

# ======================================================================
# 18. HARD QA
# ======================================================================

R2 completion requires all gates from the R2 schema, including:

```text
STEP08_ELIGIBLE_ACCOUNTED = 794/794
R1_PROVIDER_SEEDS_ACCOUNTED = 386/386
R1_DUPLICATE_OPEN_QUESTION_GROUPS_REVIEWED = 72/72
SILENT_SKIP = 0

PROVIDER_SEEDS_WITHOUT_ACQUISITION_QUESTION_ID = 0
DUPLICATE_INFORMATION_QUESTIONS_WITHOUT_MERGE_OR_JUSTIFICATION = 0
UNCONDITIONAL_CHILD_PROBES_WHERE_PARENT_MAY_ANSWER = 0
CONDITIONAL_CHILD_WITHOUT_VALID_PARENT = 0
CONDITIONAL_CHILD_WITHOUT_TRIGGER = 0
DEPENDENCY_CYCLES = 0
MULTIPLE_ROOT_PROBES_SAME_QUESTION_WITHOUT_DISTINCT_INFO_GAIN = 0
PROVIDER_REQUIRED_QUESTION_WITHOUT_ROOT_PROBE = 0

PROVIDER_EXECUTION_RELEASED_ROWS = 0
WORDSTAT_CALLS = 0
YMB_SEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
GENSEARCH_CALLS = 0
STEP08_PROVIDER_EXECUTION_STARTED = false
STEP09_STARTED = false
```

A high quality score does not override any failed hard gate.

# ======================================================================
# 19. OWNER RELAY / PUBLICATION
# ======================================================================

Do NOT commit/push these eight outputs directly to canonical final paths.

Package exactly the eight R2 outputs into one transport ZIP.

ZIP is transport only.

Owner single staging target:

`extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08/_work_staging/STEP08_PRE_ACQUISITION_R2_2026-09-18`

Work must give direct links for all eight outputs + one ZIP + the one staging
upload link.

Main Chat performs final placement/readback/acceptance.

# ======================================================================
# 20. STOP BOUNDARY
# ======================================================================

STOP after complete R2 artifacts and local QA/handoff.

Do NOT issue a Wordstat command.
Do NOT start a YMB batch.
Do NOT execute any provider request.
Do NOT start Step09.
Do NOT make final intent/cluster/page decisions.

Final status must be one of:

```text
STEP08_PRE_ACQUISITION_R2_COMPLETE
STEP08_PRE_ACQUISITION_R2_REWORK_REQUIRED
AUTHORITY_DRIFT
```

Main Chat owns final acceptance.
