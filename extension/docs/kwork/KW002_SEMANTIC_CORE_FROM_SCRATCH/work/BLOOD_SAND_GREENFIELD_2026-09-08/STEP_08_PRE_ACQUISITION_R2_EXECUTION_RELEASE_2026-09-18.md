# KW-002 / BLOOD & SAND — STEP08 PRE-ACQUISITION DEPENDENCY REWORK R2 EXECUTION RELEASE

Date: 2026-09-18
Status: **RELEASED TO CHATGPT WORK / PROVIDER EXECUTION BLOCKED**

## 1. Why R2 is released

The first Step08 Work pass completed 794/794 mechanically, but late Main Chat
semantic QA found a class-general provider-queue defect before any Wordstat
request was executed.

Current defect authority:

`STEP08_PRE_ACQUISITION_DUPLICATE_QUESTION_DEFECT_RECORD_2026-09-18.md`

The first Work result is therefore:

`REWORK_REQUIRED`

for provider-release purposes.

## 2. Full affected universe

R2 must process:

```text
STEP08_ELIGIBLE_CANDIDATES = 794/794
R1_PROVIDER_REQUIRED_CANDIDATES = 749/749
R1_PROVIDER_SEEDS = 386/386
R1_DUPLICATE_OPEN_QUESTION_GROUPS = 72/72
```

No representative-row patch is authorized.

## 3. Corrected method authority

Permanent controls now include:

- Level1 F05-18 parent/child provider-probe anti-regression;
- Step05 provider dependency gate;
- dedicated `STEP_08_COMPETITOR_DERIVED_WORDSTAT_VALIDATION.md`;
- corrected `STEP_RULES_INDEX.md`.

Core invariant:

```text
UNIQUE PHRASE != UNIQUE INFORMATION QUESTION
PARENT MAY ANSWER CHILD -> CHILD NOT UNCONDITIONALLY RELEASED
```

## 4. Frozen R2 release identities

```text
STEP_08_PRE_ACQUISITION_R2_PRE_HANDOFF_MANIFEST_2026-09-18.json
git_blob = 645cdc2bc52a3b487404b9ca116ce19132593d26

STEP_08_PRE_ACQUISITION_R2_OUTPUT_SCHEMA_CONTRACT_2026-09-18.json
git_blob = 622599b7bf366affb11df5a189fa995e3eae3a2f

STEP_08_PRE_ACQUISITION_DEPENDENCY_REWORK_R2_WORK_PROMPT_2026-09-18.md
git_blob = 76e97f58b527ae61d538484ee7d316413d73be35

STEP08_PRE_ACQUISITION_DUPLICATE_QUESTION_DEFECT_RECORD_2026-09-18.md
git_blob = fce5f8099d2fe1ad11bbf8f27bf10ea986c0737b

STEP_08_COMPETITOR_DERIVED_WORDSTAT_VALIDATION.md
git_blob = 0d3894dc2937a8c60add927a6f5d89491e2b2648
```

R2 preparation HEAD before this release:

`57965d3332c2cb4be41ce44d27a99477074b6cda`

## 5. Work role boundary

Work receives the already corrected execution contract.

It must NOT:

- redo Main Chat external research;
- redesign the roadmap;
- reread the full Level1 governance stack;
- execute Wordstat/Search/AI-search;
- start Step09.

It performs only the narrow remote/input-identity preflight in the R2 prompt,
then the full-volume dependency rework.

## 6. Required R2 outputs

1. `STEP08_CANDIDATE_PRE_ACQUISITION_RECONCILIATION_R2.csv`
2. `STEP08_EXISTING_EVIDENCE_REUSE_REGISTER_R2.csv`
3. `STEP08_PROVIDER_ACQUISITION_QUESTION_REGISTER_R2.csv`
4. `STEP08_PROVIDER_SEED_MANIFEST_R2.csv`
5. `STEP08_R1_SEED_DISPOSITION_R2.csv`
6. `STEP08_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX_R2.csv`
7. `STEP08_PRE_ACQUISITION_QA_R2.md`
8. `STEP08_PREPARATION_HANDOFF_MANIFEST_R2.json`

One transport ZIP contains exactly those eight files.

## 7. Provider boundary

```text
WORDSTAT_CALLS_ALLOWED_NOW = 0
WORDSTAT_BATCH_START_ALLOWED_NOW = false
WORDSTAT_BATCH_NEXT_ALLOWED_NOW = false
YMB_SEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
STEP08_PROVIDER_EXECUTION_STARTED = false
STEP09_STARTED = false
```

No R1 or R2 seed may be executed before Main Chat accepts R2 and creates a new
provider execution release.

## 8. Quality score for the R2 release contract

This score evaluates the corrected R2 method/release contract, not the future
R2 Work result.

| Criterion | Score | Basis |
|---|---:|---|
| Goal/output completeness | 10/10 | full 794/749/386 affected universes and eight outputs frozen |
| Method/source support | 10/10 | defect derived from actual full R1 queue plus current universal gates |
| Input evidence/provenance integrity | 10/10 | R1 frozen data authority inherited and exact R2 inputs pinned |
| Coverage/completeness | 10/10 | 794/794 + 386/386 + 72/72 required; no sample patch |
| Analytical correctness/claim boundaries | 10/10 | no naive 162 collapse; parent/child vs independent probes distinguished |
| Adversarial QA quality | 10/10 | F05-18 gates explicitly added and full blast radius frozen |
| Persistence/readback/reproducibility | 10/10 | canonical rules/schema/manifest/prompt released with Git identities |
| Owner/client usability/plain language | 9/10 | execution contract is precise; owner-facing explanation remains in Main Chat |
| Information gain/cost/execution efficiency | 10/10 | static over-acquisition blocked before any provider spend |
| Downstream readiness | 9/10 | provider execution deliberately remains blocked until R2 Work acceptance |

```text
QUALITY_TOTAL = 98/100
QUALITY_SCORE = 9.8/10
HARD_RELEASE_GATES = PASS
OPEN_CRITICAL_RELEASE_DEFECTS = 0
```

Points are withheld because R2 execution/return QA has not happened yet and
provider execution is intentionally not ready.

## 9. Quality / release decision

The R2 release closes the known method defect at contract level but does not
prejudge the R2 analytical result.

```text
R2_METHOD_CORRECTION = PASS
R2_FULL_VOLUME_WORK_TRIGGER = PASS
R2_PRE_HANDOFF_MANIFEST = PASS
R2_OUTPUT_SCHEMA = PASS
R2_WORK_PROMPT = PASS
PROVIDER_EXECUTION = BLOCKED
NEXT = OWNER_RUNS_R2_WORK_PROMPT
```
