# STEP 05A ACCEPTED DELTA PROPAGATION → STEP 7 CLEANUP → STEP 8 REFREEZE — WORK HANDOFF — 2026-09-08

## 0. Task type

This is an **EXECUTION task** for ChatGPT Work.

Do not stop after review, planning, inventory, or a prose-only impact report.
Execute the full bounded propagation of the owner-accepted Step 5A semantic delta back into the existing OKNO_MSK semantic pipeline through Step 7 and Step 8, materialize versioned post-Step5A authorities, run deterministic QA, commit checkpoints, and perform remote GitHub readback.

Repository:
`MaksimUnimax/Yandex_direct`

Branch:
`roadmap/kwork-productization-2026-08-28`

Level-1:
`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE`

Level-2 job:
`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK`

Expected live branch HEAD at handoff creation:
`ae93b11c6393bf47adc37a9353e834965bd65beb`

There is legitimate concurrent KW002 work on the same branch. Re-read the live branch before every write, preserve unrelated concurrent work, and do not reset/rebase/overwrite it.

---

## 1. Why this propagation is required

Step 5A is now permanently canonized and owner-accepted.

The completed competitor-semantic execution produced a union-compatible acquisition delta of exactly 16 accepted phrases. These phrases are **not yet frozen semantic truth** and must not simply be appended to the final XLSX or copied directly into a client release.

Correct causality:

```text
STEP5A ACCEPTED ACQUISITION DELTA
→ STEP7 ROW-LEVEL CLEANUP / STATE DECISION
→ STEP8 SEARCH-STAGE REFREEZE
→ DOWNSTREAM IMPACT REGISTER
→ only affected downstream stages are refreshed later
```

The two unresolved Step5A directions remain HOLD and are excluded from this propagation input:

- `окна для старого фонда`
- `кладовая на балконе`

Do not invent rows for them and do not perform new Search.

---

## 2. Mandatory Level-1 authorities

Read the live remote versions before processing:

1. `STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md`
2. `STEP_RULES_INDEX.md`
3. `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — Step 7 rules, including:
   - no default KEEP;
   - positive evidence required;
   - accounting QA != semantic QA;
   - uncertainty remains explicit.
4. `STEP_08_SEARCH_STAGE_FREEZE_METHOD.md` — Step 8 rules, including:
   - only executable evidence routes;
   - every preserved phrase must have deterministic complete demand/provenance joins;
   - silent field loss = 0.
5. relevant universal gates referenced by those authorities, especially provenance/durability and upstream-correction propagation rules.

Do not weaken the existing methods to make the 16 rows fit.

---

## 3. Mandatory Level-2 authorities

Read live remote files and resolve the exact historical Step 7 / Step 8 artifact names and schemas from the repository itself. Do not invent a competing schema if an established one already exists.

At minimum read:

### Step5A accepted source

- `STEP_05A_FIRST_EXECUTION_2026-09-08/STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv`
- `STEP_05A_FIRST_EXECUTION_2026-09-08/STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv`
- `STEP_05A_FIRST_EXECUTION_2026-09-08/STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv`
- `STEP_05A_OWNER_ACCEPTANCE_AND_PERMANENT_PROMOTION_2026-09-08.md`

### Existing frozen semantic baseline

Resolve and read the current completed OKNO_MSK authorities that establish:

```text
UNIQUE_PHRASES = 2840
ACTIVE = 2332
ASSIGNED = 2313
SEARCH_REQUIRED = 19
CANONICAL_STRUCTURAL_UNITS = 168
```

At minimum include the historical Stage-5 authorities:

- `RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv`
- `RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv`

and the existing Step 7 / Step 8 freeze artifacts that produced the known pre-Step5A freeze classes:

```text
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
TOTAL = 2840
```

If exact artifact names differ, discover them from live project references/state and record the resolved paths in the execution log.

### Preservation boundary

The corrected release dated 2026-09-05 and its existing client documents are historical accepted artifacts. Do not overwrite them in this task.

---

## 4. Exact propagation input

The Step5A delta contains exactly 16 accepted rows. Account for all 16 exactly once.

The phrases are:

1. `гидроизоляция для открытого балкона`
2. `гидроизоляция открытого балкона в частном доме`
3. `лучшая гидроизоляция для открытого балкона`
4. `как сделать гидроизоляцию на открытом балконе`
5. `гидроизоляция открытого деревянного балкона`
6. `гидроизоляция балконной плиты открытого балкона`
7. `солнцезащитный стеклопакет`
8. `солнцезащитное стекло в стеклопакете`
9. `солнцезащитный стеклопакет rehau`
10. `многофункциональный стеклопакет что это`
11. `ударопрочный стеклопакет`
12. `балконы под офис`
13. `шумоизоляция на крышу балкона`
14. `шумоизоляция крыши балкона от дождя`
15. `шумоизоляция крыши балкона изнутри от дождя`
16. `армирование оконного профиля`

Pre-cleanup arithmetic union size is exactly:

`2840 + 16 = 2856 candidate phrase rows`

This is only the input union. It is **not** a predetermined new active/frozen total.

---

## 5. Step 7 propagation execution

### 5.1 Build a union-compatible pre-cleanup input

Create a versioned post-Step5A union/input ledger that:

- preserves all 2,840 historical baseline phrase rows exactly once;
- adds all 16 accepted Step5A rows exactly once;
- preserves source lineage distinguishing historical baseline vs `COMPETITOR_DERIVED_STEP5A`;
- preserves actual Wordstat frequency evidence, region, device/operator context, competitor-page lineage, Search representative-query evidence and Step5A direction lineage for the 16 rows;
- does not fabricate fields not supported by evidence;
- produces zero normalized duplicate inflation.

If any of the 16 unexpectedly collides with a live baseline phrase under the actual Step7 normalization rules, stop treating the precomputed overlap=0 as authority: record the contradiction precisely and resolve it from live evidence rather than forcing addition.

### 5.2 Apply the existing Step 7 method to all 16 new rows

Do not default them to KEEP merely because Step5A said `ADD_TO_PIPELINE`.

`ADD_TO_PIPELINE` means “admit to normal semantic processing”, not “guaranteed active/final”.

For each of the 16 rows, apply the same row-level semantic cleanup logic used by the established OKNO_MSK Step7 authority.

Every new row must receive an evidence-backed Step7 state equivalent to the existing taxonomy, for example the established project states that feed Step8 (`CORE_CANDIDATE`, `REVIEW_SEARCH`, `REVIEW_DEFERRED`, `EXCLUDED_PRESERVED`) or the actual exact live taxonomy if different.

Preserve:

- phrase;
- normalized phrase;
- actual demand evidence;
- business/scope fit;
- semantic relevance;
- duplication/close-variant decision;
- uncertainty;
- reason;
- source/provenance;
- any search-required reason;
- lineage to Step5A direction.

Do not change historical Step7 decisions for the original 2,840 rows unless the addition of a new row creates an actual contradiction/duplicate relationship that requires an explicit, auditable correction. Any such changed historical row must be enumerated separately.

### 5.3 Reconcile Step7 counts

Report exactly:

- historical 2,840 rows carried unchanged;
- new 16 rows accounted;
- new rows by Step7 state;
- any historical rows whose Step7 state changed because of an actual new-row interaction;
- any duplicate/close-variant suppressions;
- any new SEARCH_REQUIRED/REVIEW_SEARCH need;
- any new deferred/hold/excluded state.

No silent drops.

---

## 6. Step 8 refreeze execution

Using the actual post-Step7 truth, create a **new versioned post-Step5A Step8 freeze**.

Do not overwrite the historical 2026-09-05 freeze.

The new freeze must:

- account for every union input row through an explicit frozen state;
- preserve deterministic joins to complete demand/provenance for all included/preserved rows;
- preserve Step5A provenance on the new rows;
- maintain zero silent field loss;
- maintain zero unexplained normalized duplicate inflation;
- distinguish historical evidence from new Step5A evidence;
- carry uncertainty/search-required states honestly;
- produce exact new totals for all Step8 classes;
- state whether the active/frozen core count changes and by how much.

Do not assume all 16 become active.

### 6.1 Rebuild/reconcile semantic authority inputs needed downstream

Materialize versioned post-Step5A semantic authority sufficient for downstream stages to consume the new truth.

Do **not** overwrite the old Stage-5 files or old corrected release.

If the existing architecture requires a versioned final semantic master / canonical join layer before Step9+, produce the new post-Step5A equivalent and document how it relates to the historical Stage5 authority.

Do not invent structural-unit/page ownership decisions at this stage. Where a new phrase can inherit only a parent semantic/business context but not final cluster/page ownership, keep downstream ownership unset/pending and let later stages resolve it.

---

## 7. Downstream impact register — REQUIRED

After refreeze, build an explicit impact register that answers what must be re-run and what can be reused.

For every surviving/new materially relevant phrase/direction, evaluate at least:

### Step 9 — ordinary Search validation

- Is existing preserved Step5A exact-query Search evidence sufficient for the downstream question?
- Is additional ordinary Search needed because Step9 asks a different clustering/page-ownership boundary?
- If new Search would be required, produce a **requirement only**; Work must not call a provider.

### Step 10 — clustering / user task

- existing cluster can absorb phrase with no cluster-boundary change;
- existing cluster needs member rebuild;
- new cluster candidate;
- unresolved pending Search.

### Step 11 — page ownership

- likely existing-page ownership needs recheck;
- supporting page relationship needs recheck;
- no ownership effect yet;
- unresolved.

Do not assign final ownership unless preserved evidence and current method make it deterministic without new Step9 work.

### Step 12 — structural/content actions

- possible content-block expansion;
- possible semantic mapping only;
- possible new structural action candidate;
- no action;
- unresolved.

Do not create a physical site action merely because a new phrase exists.

### Step 13 — competing-page diagnosis

State whether the new/changed direction triggers a competing-page check under the current method.

### Step 14 — Search-only architecture

State whether the Search-only architecture must be refreshed for that direction, or whether the existing architecture can be reused unchanged.

### Steps 15–17 — AI diagnostic / comparison impact

State whether each new/changed direction:

- is already represented by current AI diagnostic coverage;
- requires AI case-selection reconsideration;
- would require a new AI provider call only if later separately authorized;
- has no material AI-case impact.

Work must not perform Step16 provider calls.

### Steps 18–20

State which priority registers, implementation guides, client reports, semantic-core workbook and release QA will require regeneration **after** upstream downstream decisions are resolved.

The impact register must prevent a blind full rerun while also preventing stale downstream artifacts from surviving an upstream semantic change.

---

## 8. Required artifacts

Create a versioned propagation workspace under the current OKNO_MSK job, preferably:

`STEP_05A_POST_ACCEPTANCE_PROPAGATION_2026-09-08/`

At minimum materialize:

1. `STEP_05A_POST_ACCEPTANCE_UNION_INPUT.tsv`
2. `STEP_05A_DELTA_STEP07_CLEANUP_DECISIONS.tsv`
3. `STEP_05A_POST_ACCEPTANCE_STEP08_FREEZE.tsv` (or exact schema-equivalent)
4. `STEP_05A_POST_ACCEPTANCE_DEMAND_PROVENANCE_RECONCILIATION.tsv`
5. `STEP_05A_POST_ACCEPTANCE_SEMANTIC_AUTHORITY.tsv` if required by the current pipeline contract
6. `STEP_05A_POST_ACCEPTANCE_DOWNSTREAM_IMPACT_REGISTER.tsv`
7. `STEP_05A_POST_ACCEPTANCE_PROPAGATION_REPORT.md`
8. `STEP_05A_POST_ACCEPTANCE_PROPAGATION_QA.json`
9. execution/checkpoint/readback receipts sufficient to prove lifecycle.

You may add deterministic builders/validators.

Use actual existing schemas where stronger than these suggested filenames/fields.

---

## 9. Hard constraints

DO NOT:

- perform new Yandex Search;
- perform new Wordstat;
- perform Alice/GenSearch/Webmaster/Metrika/Direct calls;
- use substitute web search;
- inspect new competitor pages;
- retry the two Step5A unknown queries;
- append directly to the historical standalone semantic-core XLSX;
- overwrite the historical 2026-09-05 corrected release;
- overwrite historical Stage5/Step7/Step8 authorities merely to make the newest state look canonical;
- create final page ownership or page-creation decisions without the evidence required by Steps 9–12;
- change Level-1 methodology in this task;
- touch unrelated KW002 work.

Provider calls by Work must equal `0`.

---

## 10. Required QA

QA must fail if any of the following occurs:

- historical baseline not accounted exactly once;
- any of the 16 accepted delta rows missing or duplicated;
- either HOLD direction is inserted as an accepted row;
- pre-cleanup union does not reconcile to 2,856 absent a documented live-authority contradiction;
- any Step5A frequency/count is fabricated or replaced by totalCount invention;
- Step7 defaults all 16 to KEEP without row-level reasoning;
- silent field/provenance loss;
- normalized duplicate inflation;
- Step8 class totals do not reconcile to the complete union;
- any downstream impact is omitted for a surviving new direction;
- new page/ownership/action asserted without sufficient stage authority;
- new provider/web call performed;
- corrected client release changed;
- historical Stage5/freeze overwritten;
- Level1 changed;
- unrelated KW002 changed by this Work scope;
- remote readback fails.

Also explicitly report:

- union rows;
- new 16 rows by Step7 state;
- new Step8 totals;
- net active/frozen-core change vs 2,332 active / 2,840 total baseline as appropriate to the actual schema;
- count of downstream affected clusters/units/directions;
- number of additional Step9 Search requirements, if any;
- number of Step10/11/12/14/15–17 refresh requirements;
- protected artifact identities.

---

## 11. Git lifecycle

Use:

`WORK → SAVE → COMMIT → REMOTE GITHUB READBACK → CONTINUE`

Because concurrent KW002 work exists:

- fetch remote HEAD before every commit/push-equivalent operation;
- preserve legitimate concurrent commits;
- never force-update/reset the branch;
- if remote advances, integrate/preserve it before continuing.

Completion requires:

- all required propagation artifacts remotely present;
- deterministic QA PASS;
- protected historical release/authorities unchanged;
- provider calls = 0;
- working tree clean;
- remote readback PASS;
- final remote HEAD reported.

---

## 12. Completion / next action

This task stops after **Step7 cleanup + Step8 refreeze + downstream impact mapping**.

Do not execute Step9+ in this Work task.

After PASS, Main ChatGPT will read the new freeze and impact register directly from remote GitHub and authorize only the affected downstream work.

Expected next action class:

`EXECUTE_ONLY_TARGETED_DOWNSTREAM_REFRESH_REQUIRED_BY_POST_STEP5A_STEP8_IMPACT_REGISTER`
