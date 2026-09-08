# STEP 05A.5 WORDSTAT CLEAN / RECONCILE / SEARCH-RECHECK PACKAGE — WORK HANDOFF — 2026-09-08

## 0. Task type

This is an **EXECUTION task** for ChatGPT Work.

Do not stop after review, diagnosis, planning, or sample analysis.
Execute the complete Step 5A.5 scope, materialize durable artifacts, run deterministic QA, commit every completed checkpoint, and perform remote GitHub readback before reporting completion.

Repository:

`MaksimUnimax/Yandex_direct`

Branch:

`roadmap/kwork-productization-2026-08-28`

Level-1 methodology workspace:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE`

Current Level-2 job workspace:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK`

Step 5A execution workspace:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_05A_FIRST_EXECUTION_2026-09-08`

Expected acquisition-summary base commit before this handoff materialization:

`23fa91b38dcf5f55374d33d8b72bd7a67f1fe0af`

The launch prompt from Main ChatGPT will provide the actual current handoff commit. Verify the live branch before substantive work.

---

# 1. Current state — already complete

Step 5A.1 is complete:

- 75 preserved Search probes accounted for;
- 750 preserved TOP10 ranking rows accounted for;
- domain recurrence/classification completed;
- bounded 9-competitor selection completed.

Step 5A.2 and 5A.3 are complete:

- all 9 selected competitor domains accounted for;
- all 44 authorized preserved ranking URLs inspected;
- page-level evidence persisted;
- candidate directions derived only from observed competitor-page evidence;
- candidate directions reconciled against existing OKNO_MSK semantic authority;
- 14 `POTENTIALLY_NEW_WORDSTAT_SEED` directions materialized for Main ChatGPT.

Step 5A.4 is complete:

- Main ChatGPT executed the exact 14-seed Wordstat package through Yandex Bridge;
- all 14 requests succeeded;
- final job state = `COMPLETED`;
- `failed_terminal = 0`;
- `outcome_unknown = 0`;
- `pending = 0`;
- `requests_started = 14`;
- final estimated cost = `0.28 RUB`;
- final `next_safe_action = NONE`.

No further Wordstat provider calls are authorized in this Work task.

---

# 2. Mandatory authorities to read before processing

Read the current live versions from GitHub, not stale local assumptions.

At minimum read:

1. Level-1 method:
   - `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md`

2. Step 5A execution authorities:
   - `STEP_05A_FIRST_EXECUTION_REPORT.md`
   - `STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv`
   - `STEP_05A_COMPETITOR_PAGE_OBSERVATIONS.json`
   - `STEP_05A_DERIVED_SEED_CANDIDATES.tsv`
   - `STEP_05A_SEED_DECISIONS.json`
   - `STEP_05A_WORDSTAT_REQUIREMENT_PACKAGE.tsv`
   - `STEP_05A_WORDSTAT_ACQUISITION_SUMMARY_2026-09-08.md`
   - `STEP_05A_WORDSTAT_BATCH_START_RAW.json`
   - all fourteen raw provider envelopes:
     - `STEP_05A_WORDSTAT_ITEM_01_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_02_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_03_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_04_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_05_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_06_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_07_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_08_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_09_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_10_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_11_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_12_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_13_RAW.json`
     - `STEP_05A_WORDSTAT_ITEM_14_RAW.json`

3. Current OKNO_MSK semantic authority used by Step 5A.3, including the current Stage-5 semantic master and canonical structural-unit authority. Resolve the exact live files from existing Step 5A references/current project state; do not substitute an older semantic snapshot.

4. Existing preserved Search evidence may be used only as prior evidence/reference. Do not perform new Search in Work.

---

# 3. Hard evidence rules

These rules are mandatory.

## 3.1 Provider payload truth

The raw Wordstat envelopes are the authority.

- Extract only rows actually present in `provider_result.result.results` or `provider_result.result.associations`.
- Never invent a missing `results` list.
- Never infer unreturned rows from `totalCount`.
- Preserve the exact phrase and count supplied by Wordstat.

## 3.2 Empty provider result

`result = {}` means **empty provider result**.

It does **not** mean a proven numeric demand value of zero.

Keep a distinct evidence state such as:

`EMPTY_PROVIDER_RESULT`

Do not fabricate `totalCount=0`.

## 3.3 `totalCount`-only result

If a raw envelope contains `totalCount` but no `results` rows, preserve that distinction.

Do not invent phrase-level rows.

## 3.4 Associations

Associations are discovery evidence only.

An association is **not** accepted merely because Wordstat returned it.

Every association must be classified independently as one of at least:

- materially relevant candidate;
- already covered / close existing semantic direction;
- generic/off-scope noise;
- ambiguous / hold.

Examples visible in the acquisition include obvious noise such as unrelated entertainment, finance-app, medical, or generic roofing phrases. They must not enter the Search recheck package merely because their counts are high.

## 3.5 Search ownership boundary

Wordstat validates/discovers demand.

Wordstat does **not** determine:

- SERP intent;
- exact-query landing-page owner;
- split/merge decision;
- page creation;
- physical site change.

Any genuinely new material candidate surviving this step must be returned to Main ChatGPT for ordinary Yandex Search validation in Step 5A.6.

## 3.6 Competitor causality boundary

Preserve:

`competitor page evidence -> candidate seed -> Wordstat seed -> Wordstat returned phrase -> semantic reconciliation -> Search recheck requirement`

Do not collapse this into `competitor ranks for returned phrase`.

The competitor page only supplied the observed topic/seed unless exact ranking evidence already exists independently.

---

# 4. Required Step 5A.5 execution scope

## 4.1 Account for all 14 seed executions

Build a normalized seed acquisition ledger that accounts for every one of the 14 authorized seeds exactly once.

For every seed include at minimum:

- seed priority/order;
- exact seed text;
- raw item file;
- request ID;
- HTTP status;
- request executed state;
- provider result shape;
- totalCount if actually supplied;
- number of direct `results` rows actually supplied;
- number of associations actually supplied;
- empty-result flag;
- evidence limitation note where applicable.

No seed may silently disappear.

## 4.2 Materialize every returned Wordstat phrase row

Create a row-level ledger containing every actually returned direct `results` phrase and every actually returned association from items 01–14.

Each row must preserve at minimum:

- source seed priority/order;
- source seed;
- source raw item file;
- Wordstat row class: `DIRECT_RESULT` or `ASSOCIATION`;
- returned phrase exactly as supplied;
- returned count exactly as supplied;
- source request ID;
- source totalCount if supplied;
- candidate relevance classification;
- reason/evidence note.

Do not deduplicate before preserving raw row-level lineage.

## 4.3 Join back to competitor-page lineage

For every seed, join the existing Step 5A.3 lineage back to the source competitor evidence.

Preserve where available:

- competitor domain;
- competitor ranking URL / inspected URL;
- page evidence row/identifier;
- observed page phrase/topic evidence that generated the seed;
- Step 5A.3 candidate direction / decision record.

If a seed has multiple legitimate page-evidence origins, preserve all lineage rather than selecting one arbitrarily.

## 4.4 Reconcile every returned phrase against current semantic authority

Reconcile all materially relevant direct results and associations against the current OKNO_MSK semantic authority.

Use exact/normalized/close-semantic matching with auditable evidence.

For each materially relevant phrase classify into one of at least:

- `ALREADY_COVERED_EXACT_OR_CLOSE`
- `POTENTIALLY_NEW_SEARCH_RECHECK`
- `OFF_SCOPE_BUSINESS`
- `NOISE_IRRELEVANT`
- `HOLD_EVIDENCE`

Do not treat lexical novelty as semantic novelty.

A phrase is `POTENTIALLY_NEW_SEARCH_RECHECK` only if it represents a materially new business/search direction not already adequately captured by the current semantic authority and is sufficiently evidenced to justify paid/new Search validation.

## 4.5 Deduplicate genuinely new directions

Deduplicate surviving `POTENTIALLY_NEW_SEARCH_RECHECK` rows at the direction/query-family level while preserving all underlying Wordstat and competitor-page lineage.

Do not suppress materially distinct intents merely because wording overlaps.

Do not create multiple Search calls for trivial grammatical variants if one representative query can validate the same unresolved direction.

For each deduped direction choose the best representative Search query and explain why it is representative.

## 4.6 Build exact ordinary Yandex Search recheck package

Materialize the exact bounded Search package for Main ChatGPT / Yandex Bridge.

Each required Search row must include at minimum:

- search priority;
- representative query exactly to execute;
- region = `213` unless preserved project evidence requires otherwise;
- requested TOP results = `10` unless the current ordinary-Search bridge contract requires an equivalent current field;
- originating Wordstat seed(s);
- originating returned Wordstat phrase(s) and counts;
- competitor-page lineage;
- current semantic reconciliation result;
- unresolved question that Search must answer;
- why existing preserved Search evidence does not already resolve it;
- expected downstream decision gate after Search.

This package is a **requirement package only**.

Work must not execute Yandex Search.

---

# 5. Required artifacts

Create, at minimum, in:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_05A_FIRST_EXECUTION_2026-09-08/`

1. `STEP_05A_WORDSTAT_SEED_ACQUISITION_LEDGER.tsv`
2. `STEP_05A_WORDSTAT_RETURNED_PHRASE_LEDGER.tsv`
3. `STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv`
4. `STEP_05A_SEARCH_RECHECK_REQUIREMENT_PACKAGE.tsv`
5. `STEP_05A_WORDSTAT_RECONCILIATION_REPORT.md`
6. `STEP_05A_WORDSTAT_RECONCILIATION_QA.json`
7. an execution/readback log or checkpoint files sufficient to prove the Work lifecycle and remote readback.

You may add builder/validator scripts when useful for deterministic reproducibility.

Do not overwrite the raw provider envelopes.

---

# 6. Required QA

QA must fail if any of the following occurs:

- fewer or more than 14 seed acquisition rows;
- any authorized seed missing;
- duplicate seed-accounting inflation;
- any raw direct `results` row silently dropped;
- any raw association row silently dropped from the raw returned-phrase ledger;
- fabricated phrase rows;
- fabricated zero demand for `result={}`;
- fabricated phrase list from `totalCount` only;
- materially relevant candidate without semantic-authority reconciliation;
- `POTENTIALLY_NEW_SEARCH_RECHECK` without competitor/seed/Wordstat lineage;
- Search requirement without explicit unresolved Search question;
- duplicate Search requirements that test the same unresolved direction without justification;
- obvious off-topic Wordstat association promoted to Search recheck;
- new Yandex provider call performed by Work;
- mutation of current client deliverables;
- automatic promotion of Step 5A to permanent Level-1 methodology.

Also report explicit counts for:

- 14 seeds accounted for;
- seed results by shape (`RESULT_ROWS`, `TOTALCOUNT_ONLY`, `EMPTY_PROVIDER_RESULT`, etc.);
- total direct Wordstat rows extracted;
- total association rows extracted;
- rows classified already covered;
- rows classified new Search recheck;
- rows classified off-scope/noise;
- rows classified hold;
- deduped genuinely new directions;
- final Search recheck calls required.

---

# 7. No-provider / no-client-doc constraints

DO NOT:

- perform new Yandex Search;
- perform new Wordstat;
- perform Alice/GenSearch/Webmaster/Metrika/Direct calls;
- use web search as a substitute for Yandex provider evidence;
- alter the 14 raw provider envelopes;
- mutate Report 01, Report 02, Report 03, Report 04, their DOCX/PDF derivatives, or corrected client release contents;
- rewrite current Stage-5 authority merely to make new candidates fit;
- create pages, page owners, split/merge decisions, or implementation actions from Wordstat alone;
- promote Step 5A to permanent Level-1 methodology.

If a genuine authority contradiction is discovered, preserve it as a blocker/HOLD with exact evidence rather than silently correcting upstream truth.

---

# 8. Git lifecycle

Use the project discipline:

`WORK -> SAVE -> COMMIT -> REMOTE GITHUB READBACK -> CONTINUE`

Commit completed checkpoints rather than leaving the entire execution uncommitted until the end.

At completion:

1. verify working tree clean;
2. verify all required artifacts exist on the remote branch;
3. remote-read back the final artifacts from GitHub;
4. verify remote/local tree identity for the produced scope;
5. persist a final remote-readback receipt/checkpoint;
6. report final HEAD and the exact count of Search recheck requirements returned to Main ChatGPT.

---

# 9. Completion condition

This Work task is complete only when all 14 Wordstat seed executions and every actually returned Wordstat row are accounted for, relevant candidates are reconciled against the current semantic authority with full lineage, genuinely new directions are deduplicated, and an exact bounded ordinary-Yandex-Search requirement package is materialized and remotely read back.

The next stage after PASS is:

`MAIN_CHATGPT_STEP_5A_6_EXECUTE_ONLY_THE_MATERIALIZED_SEARCH_RECHECK_PACKAGE_VIA_YANDEX_BRIDGE`

Do not execute that next stage in Work.
