# KW-002 / BLOOD & SAND — STEP08 PREPARATION RELEASE

Date: 2026-09-18
Status: **RELEASED TO CHATGPT WORK / PROVIDER EXECUTION NOT RELEASED**

## 1. Live authority

```text
PREPARATION_BASE_HEAD = 9933b714e09ecf22b5ff5891add036ea980c142d
PRE_RELEASE_HEAD = 1a57808fc55a046e764ff1aac3fcd96a2925c5a3
AUTHORITY_DRIFT = NONE
```

R10 remained current throughout preparation until this release.

## 2. Main Chat rule-read ledger

Current Main Chat action:

`STEP08 PREPARATION + WORK RELEASE`

Read in full from current live authority as applicable:

- `LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`
- `LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md`
- `LEVEL1/COMMON_RULES.md`
- `LEVEL1/INHERITED_KW001_UNIVERSAL_RULES.md`
- `LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md`
- `LEVEL1/CLIENT_INTAKE_AND_SCOPE_RULE.md`
- `LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`
- `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `LEVEL1/WORK_HANDOFF_RULE.md`
- `LEVEL1/YANDEX_MARKETING_BRIDGE_EXECUTION_RULE.md`
- `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`
- `LEVEL1/RESULT_QUALITY_SCORING_RULE.md`
- `LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md`
- `LEVEL2/STEP_RULES_INDEX.md`
- `LEVEL2/YANDEX_MARKETING_BRIDGE_PROVIDER_EXECUTION_GATE.md`
- `LEVEL2/STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md`
- `LEVEL2/STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md`
- `LEVEL2/STEP_05_TARGETED_EXPANSION_AND_PROVIDER_EXECUTION_GATE.md`
- current R10 flow/cursor;
- current Step07 acceptance;
- current Step00 scope freeze;
- current YMB job execution contract;
- relevant Step03/Step05 provider manifests and receipts;
- KW-001 MK03 competitor-gap Step04/Step05 authorities and actual reuse accounting.

```text
UNRESOLVED_AUTHORITY_CONFLICTS = 0
MAIN_CHAT_EXECUTION_ALLOWED = true
```

## 3. Fresh external research gate

Canonical trace:

`STEP_08_PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_TRACE_2026-09-18.md`

Verified on 2026-09-18:

- current Yandex Wordstat GetTop method/fields/depth;
- current operators;
- current Wordstat quotas/limits;
- current GetTop pricing;
- current Wordstat API mode;
- current Bridge Wordstat protocol identities/capabilities.

```text
PRE_STEP_EXTERNAL_RESEARCH = PASS
SOURCE_DISCLOSURE_REQUIRED_IN_OWNER_CHAT = PASS_ON_RELEASE_REPORT
SOURCE_TO_METHOD_TRACE = PASS
```

## 4. Frozen preparation artifacts

```text
STEP_08_PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_TRACE_2026-09-18.md
git_blob = ed3e6c7a6b4a49592ed9fdb6ae42a7e442de4856

STEP_08_PREPARATION_OUTPUT_SCHEMA_CONTRACT_2026-09-18.json
git_blob = 453d58cbc5fbd80a564ab62fd8f6d0572259af95

STEP_08_PREPARATION_METHOD_AND_EXECUTION_GATE_2026-09-18.md
git_blob = 1b0a64fa0c3e00e1c06c0fff78b0a7bbd11461c6

STEP_08_PRE_HANDOFF_MANIFEST_2026-09-18.json
git_blob = 14a2653a8f95c582ef4ce1556db865fae94bdadb

STEP_08_PRE_ACQUISITION_RECONCILIATION_WORK_PROMPT_2026-09-18.md
git_blob = 95ac7b2bd4fd57863d95c431d954e6408bcad47f
```

## 5. Released Work unit

```text
WORK_ID = KW002_STEP08_PRE_ACQUISITION_RECONCILIATION_2026-09-18
BOUNDED_INPUT = 794/794 Step07-eligible candidates
WORK_MODE = FULL_VOLUME
SAMPLING = FORBIDDEN
FRESH_WEB_RESEARCH_IN_WORK = FORBIDDEN
FULL_LEVEL1_REREAD_IN_WORK = FORBIDDEN
WORDSTAT_CALLS_IN_WORK = 0
YMB_SEARCH_CALLS_IN_WORK = 0
AI_SEARCH_CALLS_IN_WORK = 0
GENSEARCH_CALLS_IN_WORK = 0
```

Work performs only the narrow current-head/release/input-identity preflight defined in the prompt.

## 6. Required Work outputs

1. `STEP08_CANDIDATE_PRE_ACQUISITION_RECONCILIATION.csv` — exactly 794 rows.
2. `STEP08_EXISTING_EVIDENCE_REUSE_REGISTER.csv`.
3. `STEP08_PROVIDER_SEED_MANIFEST.csv`.
4. `STEP08_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX.csv`.
5. `STEP08_PRE_ACQUISITION_QA.md`.
6. `STEP08_PREPARATION_HANDOFF_MANIFEST.json`.
7. One transport ZIP containing those six files only.

Large artifacts use owner single-staging relay. Work does not publish canonical final paths.

## 7. Provider boundary

This release DOES NOT authorize provider execution.

```text
WORDSTAT_PROVIDER_EXECUTION_RELEASED = false
YMB_BATCH_START_RELEASED = false
YMB_BATCH_NEXT_RELEASED = false
STEP08_PROVIDER_EXECUTION_STARTED = false
```

After Work return, Main Chat must perform return QA and final provider-queue/depth/operator review before any command can be emitted.

## 8. Preparation quality score

This score evaluates the preparation/release, not Step08 analytical completion.

| Criterion | Score | Evidence |
|---|---:|---|
| Goal/output completeness | 10/10 | exact 794-row execution unit and required outputs frozen |
| Method/source support | 10/10 | fresh official Yandex + current repo + KW001 project-test trace |
| Input evidence/provenance integrity | 10/10 | exact blobs/trees frozen in manifest |
| Coverage/completeness | 10/10 | full-volume 794/794 requirement; sampling prohibited |
| Analytical correctness/claim boundaries | 10/10 | candidate != call; demand != final SEO; broad != qualified |
| Adversarial QA quality | 9.5/10 | hard regressions defined; execution QA still awaits Work |
| Persistence/readback/reproducibility | 10/10 | canonical prep artifacts committed and identity-addressed |
| Owner/client usability/plain language | 10/10 | owner-facing report and explicit boundaries prepared |
| Information gain/cost/execution efficiency | 10/10 | reuse-first; no blind 794-call plan |
| Downstream readiness | 9.5/10 | provider release deliberately awaits Work reconciliation |

```text
QUALITY_TOTAL = 99/100
QUALITY_SCORE = 9.9/10
HARD_PREPARATION_GATES = PASS
```

The 1 point withheld is intentional: provider queue/depth decisions are not yet evidenced until Work performs the 794-row reconciliation.

## 9. Transition

```text
STEP08_PREPARATION = PASS
STEP08_PRE_ACQUISITION_WORK = RELEASED
STEP08_PROVIDER_EXECUTION = NOT_STARTED
NEXT_ACTION = OWNER_RUNS_RELEASED_WORK_PROMPT
NEXT_STEP_ALLOWED = false
```

`NEXT_STEP_ALLOWED=false` means Step09 is not allowed and provider execution is not yet released. The only forward action is the released Step08 Work reconciliation.
