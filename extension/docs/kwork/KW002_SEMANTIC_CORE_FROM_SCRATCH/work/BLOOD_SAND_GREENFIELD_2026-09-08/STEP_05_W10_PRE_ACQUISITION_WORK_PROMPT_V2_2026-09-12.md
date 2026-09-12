# KW-002 Blood & Sand — STEP05 W10 PRE-ACQUISITION WORK PROMPT V2

Date: 2026-09-12
Handoff ID: `KW002-BS-W10-V2`
Status: **CANONICAL CORRECTED WORK PROMPT / NO PROVIDER CALLS / EXECUTION ONLY AFTER OWNER-FACING PRE-STEP DISCLOSURE**

## 0. Mission

Continue the existing KW-002 Blood & Sand greenfield semantic-core rehearsal.

THIS IS AN EXECUTION TASK, but only for Step05 pre-acquisition reconciliation.

This is NOT a new project.
This is NOT Step04.
This is NOT Step06.
This is NOT provider execution.

Goal: reconcile the accepted W09 Step04 expansion queue against the complete durable acquisition history and owner-fact boundaries, then produce the smallest safe Step05 acquisition plan. Execute zero provider calls.

Repository: `MaksimUnimax/Yandex_direct`
Branch: `roadmap/kwork-productization-2026-08-28`
Job root: `extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

## 1. Start from current live remote, not a remembered SHA

Before reading job state:

```text
fetch current live remote branch
record WORK_START_REMOTE_HEAD
verify current prompt = this V2 file
verify current release = STEP_05_W10_PRE_ACQUISITION_EXECUTION_RELEASE_V2_2026-09-12.md
verify current pre-handoff manifest = STEP_05_W10_PRE_HANDOFF_MANIFEST_V2_2026-09-12.md
verify mandatory Level1/Level2 authorities exist
```

If the current remote branch cannot be fetched, fail closed.

Obey in full:

- `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`
- `LEVEL1/WORK_HANDOFF_RULE.md`
- `LEVEL1/WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md`
- `LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`
- `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`
- `LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md`
- `LEVEL2/STEP_RULES_INDEX.md`

Read in full before analysis:

- `STEP_05_W10_PREPARATION_RULE_VIOLATION_AND_CORRECTION_2026-09-12.md`
- `STEP_05_W10_PRE_ACQUISITION_EXTERNAL_RESEARCH_V2_2026-09-12.md`
- `STEP_05_W10_PRE_HANDOFF_MANIFEST_V2_2026-09-12.md`
- `STEP_05_W10_PRE_ACQUISITION_EXECUTION_RELEASE_V2_2026-09-12.md`

The older W10 V1 prompt/release/research files are historical and MUST NOT be executed as current authority.

## 2. Current upstream authority

Current Step04 authority is W09 accepted.

Read in full:

- `STEP_04_W09_MAIN_CHATGPT_REMOTE_READBACK_ACCEPTANCE_2026-09-12.md`
- `STEP_04_CURRENT_AUTHORITY_ARTIFACT_MANIFEST_2026-09-11.json`
- `STEP_04_CURRENT_AUTHORITY_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv`
- `STEP_04_CURRENT_AUTHORITY_FAMILY_TRIAGE_2026-09-11.tsv`
- `STEP_04_CURRENT_AUTHORITY_IDENTITY_SIGNAL_LEDGER_2026-09-11.tsv`
- `STEP_04_CURRENT_AUTHORITY_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv`
- `STEP_04_CURRENT_AUTHORITY_INDEPENDENT_TAXONOMY_AUDIT_2026-09-11.tsv`
- `STEP_04_CURRENT_AUTHORITY_SANITATION_FEEDBACK_REGISTER_2026-09-11.tsv`

Use current live `KW002_EXECUTION_CURSOR_2026-09-11.json` for execution state.

IMPORTANT: `JOB_FLOW.md` and `JOB_MANIFEST.md` contain stale W08-era status text. Do not use those stale status sections as current Step05 authority and do not overwrite them from a stale Work checkout. Main ChatGPT will reconcile mutable job-state summaries separately.

## 3. Current queue contract

Reconcile all 13 W09 rows exactly once.

### A. Search-gap candidates to challenge, not auto-authorize

```text
PSQ001
PSQ004
PSQ005
```

For each, prove or reject:

- exact unresolved search-demand question;
- no equivalent durable evidence;
- no literal duplicate;
- no semantic duplicate without real operator/scope gain;
- no unresolved owner-fact dependency;
- positive incremental information gain;
- useful negative-result value;
- explicit stop condition;
- bounded request design;
- current Bridge schema compatibility.

It is valid for all three to be rejected and for Step05 to require no new provider call.

### B. Owner-fact first/only

```text
PSQ002
PSQ003
PSQ009
PSQ012
PSQ013
```

Search demand cannot establish inventory, physical form, material or effect/audience claim truth. Do not convert these into provider candidates.

### C. Reuse existing durable evidence / no re-probe

```text
PSQ006
PSQ007
PSQ008
PSQ010
```

Map the existing evidence that closes each acquisition question.

PSQ010 must link to historical E013 `!чётки` evidence and record blind replay = false.

### D. Deferred

```text
PSQ011
```

Keep deferred to later row-level intent/SERP unless a concrete new current-authority collision genuinely changes that gate. Do not create a provider call merely to avoid a deferred state.

## 4. Mandatory historical evidence reconciliation

Read the complete relevant Step02/Step03 acquisition history and preserved Step05 evidence, including at minimum:

- `STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`;
- applicable Step02 probe maps/overlays;
- `STEP_03_WORDSTAT_EXECUTION_MANIFEST_V1.csv`;
- `STEP_03_WORDSTAT_ACQUISITION_RECEIPTS.csv`;
- complete relevant `STEP_03_WORDSTAT_RAW/` evidence;
- accepted Step03A authorities;
- accepted corrected Step03B authorities;
- historical Step05 E013 receipt and exact RAW carrier.

E013 known preserved evidence:

```text
phrase = !чётки
request_id = wordstat-132a43ff-7cf9-4544-a6e2-68da666c4813
results = 2000
associations = 19
raw_blob_sha = 550add6010ddbd10e0d807fd1a11046d2b782a4a
remote_readback = PASS
blind_replay = false
```

Mandatory principle:

```text
LOCAL STEP04 GAP != GLOBAL ACQUISITION GAP
CHAT/CONTEXT LOSS != EVIDENCE LOSS
```

## 5. Provider and Bridge contract

Use `STEP_05_W10_PRE_ACQUISITION_EXTERNAL_RESEARCH_V2_2026-09-12.md` as the current external source trace.

Read current repository implementation:

- `extension/src/shared/product.js`;
- `extension/src/shared/wordstat_protocol.js`;
- relevant Wordstat execution path in `extension/src/service_worker.js`;
- current Wordstat policy/cost model files.

Hard distinction:

```text
OFFICIAL YANDEX DOCS = provider/search meaning, operators, quotas, pricing
CURRENT BRIDGE CODE = executable envelope / accepted local fields
HISTORICAL REQUEST = project-tested historical evidence only
```

Do not present a Bridge-only field as official Yandex API semantics.

## 6. Zero provider-call boundary

Hard gate for this Work pass:

```text
WORDSTAT_CALLS = 0
ORDINARY_YANDEX_SEARCH_CALLS = 0
GENSEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
```

Do not output an executable provider command into a Bridge-consumable channel.

A future command specification may appear only as inert data with `execution_status = NOT_EXECUTED`.

## 7. New evidence feed-forward contract

If Main ChatGPT later releases a provider call after this Work return, any resulting RAW evidence must follow:

```text
persist complete RAW
→ remote readback
→ conservative normalization / dedup with full lineage
→ corrected Step03B sanitation
→ only then union into later candidate data
```

This V2 pass itself does not mutate Step03A/Step03B or W09 Step04 analytical payload.

## 8. Required outputs

Materialize exactly the V2 outputs defined by `STEP_05_W10_PRE_HANDOFF_MANIFEST_V2_2026-09-12.md`:

1. `STEP_05_W10_V2_QUEUE_RECONCILIATION_WORK_2026-09-12.tsv`
2. `STEP_05_W10_V2_EXISTING_EVIDENCE_REUSE_REGISTER_2026-09-12.tsv`
3. `STEP_05_W10_V2_PROVIDER_CANDIDATE_MANIFEST_V1_2026-09-12.tsv`
4. `STEP_05_W10_V2_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-12.tsv`
5. `STEP_05_W10_V2_PRE_ACQUISITION_QA_2026-09-12.md`
6. `STEP_05_W10_V2_PRE_ACQUISITION_WORK_RETURN_2026-09-12.md`
7. deterministic materializer/source if nontrivial programmatic reconciliation is used;
8. `STEP_05_W10_V2_ARTIFACT_MANIFEST_2026-09-12.json`.

Do not rename them into old V1 names.

## 9. Known-failure regression matrix

At minimum test:

```text
F03_PROVIDER_SUCCESS_NOT_DURABLE_COMPLETION
F03B1_OPERATOR_OR_LEXICAL_MATCH_NOT_SEMANTIC_TRUTH
F03B4_AMBIGUITY_PRESERVED
F04_3_CURRENT_UPSTREAM_AUTHORITY_PROPAGATED
F05_1_DUPLICATE_DURABLE_EVIDENCE_PREVENTED
F05_2_OWNER_FACT_NOT_SENT_TO_SEARCH_PROVIDER
F06_PRELIMINARY_FAMILY_NOT_FINAL_CLUSTER_OR_PAGE
WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT
```

Job-specific blocking regressions:

```text
PSQ006_REPROBE = false
PSQ007_REPROBE = false
PSQ008_REPROBE = false
PSQ010_REPROBE = false
E013_BLIND_REPLAY = false
OWNER_FACT_ROWS_PROVIDER_CANDIDATES = 0
PROVIDER_CALLS = 0
STEP06_STARTED = false
```

## 10. PASS conditions

PASS_CANDIDATE requires all hard gates, including:

```text
WORK_START_REMOTE_HEAD_RECORDED = true
CURRENT_V2_PROMPT_AND_RELEASE_CONFIRMED = true
CURRENT_W09_AUTHORITY_USED = true
QUEUE_RECONCILED = 13/13
MISSING_QUEUE_ROWS = 0
DUPLICATE_QUEUE_ROWS = 0
EQUIVALENT_DURABLE_EVIDENCE_REPROBES = 0
OWNER_FACT_BYPASSES = 0
SURVIVING_CANDIDATES_HAVE_INCREMENTAL_GAIN = true
SURVIVING_CANDIDATES_HAVE_NEGATIVE_RESULT_VALUE = true
SURVIVING_CANDIDATES_HAVE_STOP_CONDITION = true
FIRST_EXECUTION_CANDIDATES <= 1
PROVIDER_EXECUTION_STATUS = NOT_EXECUTED
PROVIDER_CALLS = 0
STEP06_STARTED = false
```

Quality score never overrides a failed hard gate.

## 11. Pre-publication freshness and publication

Immediately before native Git publication or owner-relay packaging:

```text
fetch current remote branch again
record WORK_PRE_PUBLICATION_REMOTE_HEAD
classify every changed path since Work start
if governing/current authority changed -> reconcile/revalidate before publication
STALE_BASE_MUTABLE_STATE_FILE_OVERWRITE = 0
```

Preferred artifact route:

```text
NORMAL AUTHENTICATED GIT IF ALREADY RELIABLE
ELSE OWNER RELAY WITHOUT WASTING TIME ON GIT AUTH
```

For owner relay:

- provide individual output files;
- provide transport ZIP when useful;
- provide direct GitHub upload link for the exact job root;
- exclude stale mutable state files unless freshly reconciled;
- return for Main ChatGPT remote readback.

Do not transport large artifact bytes through the model.

## 12. Work return

Return at minimum:

```text
HANDOFF_ID = KW002-BS-W10-V2
WORK_START_REMOTE_HEAD = <sha>
WORK_PRE_PUBLICATION_REMOTE_HEAD = <sha>
QUEUE_RECONCILED = 13/13
SURVIVING_NEW_PROVIDER_CANDIDATES = <integer>
FIRST_EXECUTION_CANDIDATE = <id or NONE>
E013_REPLAY_REQUIRED = false
OWNER_FACT_BYPASSES = 0
DUPLICATE_REPROBES = 0
PROVIDER_CALLS = 0
STEP06_STARTED = false
FINAL_WORK_VERDICT = PASS_CANDIDATE|REWORK_REQUIRED
```

Then provide `ПРОСТЫМИ СЛОВАМИ` explaining what gaps actually remain, which were closed by old evidence, whether any genuinely new provider request survives, and why execution stopped before any provider call.

## 13. STOP

STOP after materializing/QA/publication-preparing the V2 pre-acquisition authorities.

Do not execute Wordstat.
Do not execute Search.
Do not start Step06.
Return control to Main ChatGPT.
