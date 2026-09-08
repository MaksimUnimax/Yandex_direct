# STEP 05A — CLIENT-FACING COMPETITOR-GAP PREVIEW OWNER-REVIEW CORRECTION — WORK HANDOFF — 2026-09-08

## 0. Task type

This is a **FOCUSED EXECUTION task** for ChatGPT Work.

Do not rerun Step 5A.1–5A.8. Do not perform new research. Do not change the technical information-gain verdict. Correct only the owner-review client-facing materialization and the deterministic QA/readback artifacts that must remain consistent with it.

Repository:

`MaksimUnimax/Yandex_direct`

Branch:

`roadmap/kwork-productization-2026-08-28`

Current expected HEAD before this handoff is materialized:

`a078e6d52685ec6e2d919e57644440c7d7908cd7`

Current Step 5A execution workspace:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_05A_FIRST_EXECUTION_2026-09-08`

---

# 1. Why correction is required

The Step 5A.8 technical execution is accepted as technically consistent:

- deterministic technical gates 1–9 = PASS;
- information gain = material positive gain with strong filtering value;
- 16 accepted acquisition-delta phrases;
- 2 Search outcome-unknown directions remain HOLD;
- no automatic Level-1 promotion;
- `PROJECT_TEST_VALIDATED=false` pending explicit owner acceptance.

However the current client-facing preview is **too aggregated for owner acceptance under the project's recipient-ready standard**.

It says that 16 new phrases were prepared, but does not show the 16 phrases.

It says that selected competitors appeared in successful rechecks, but does not show the concrete relationship:

`tested query -> selected competitor -> observed TOP10 rank`.

This is a client-materialization gap only. It is not a research-data or methodology failure.

---

# 2. Mandatory authorities to read

Read the live remote versions from GitHub:

1. `STEP_05A_CLIENT_FACING_COMPETITOR_GAP_PREVIEW_RU.md`
2. `STEP_05A_FIRST_EXECUTION_VALIDATION_REPORT.md`
3. `STEP_05A_INFORMATION_GAIN_METRICS.json`
4. `STEP_05A_FIRST_EXECUTION_VALIDATION_GATE_REGISTER.tsv`
5. `STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv`
6. `STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv`
7. `STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv`
8. `STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv`
9. `STEP_05A_FIRST_EXECUTION_VALIDATION_QA.json`
10. `CHECKPOINT_10_INFORMATION_GAIN_VALIDATION_REMOTE_READBACK.md`
11. Level-1 `STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md`, especially the client-facing result boundary.

Do not use memory as authority when the live files can be read.

---

# 3. Required correction to the plain-Russian client preview

Update only:

`STEP_05A_CLIENT_FACING_COMPETITOR_GAP_PREVIEW_RU.md`

The revised preview must still be plain Russian and client-readable. No internal IDs, Stage/Step enums, raw filenames, QA labels or developer terminology.

The revised preview must make the result **materially inspectable**, not merely summarized.

## 3.1 Keep the understandable high-level explanation

Preserve clear sections that explain:

- why competitors were checked;
- 9 real search competitors;
- 44 inspected pages;
- 92 page-level observations -> 43 independent directions;
- filtering before provider work;
- Wordstat role;
- Search role;
- 7 confirmed directions;
- 2 unresolved directions;
- no automatic new-page implication;
- propagation required before next real release.

## 3.2 Show all 16 accepted new search phrases explicitly

Add a plain-Russian section such as:

`Какие 16 новых поисковых фраз подготовлены к включению в ядро`

List all 16 accepted phrases exactly, grouped under the seven confirmed directions.

Use the accepted semantic-pipeline delta / merge reconciliation as authority.

Do not list the three suppressed close variants as accepted.

Do not list the held storage phrase as accepted.

Do not invent a phrase for the totalCount-only old-housing direction.

## 3.3 Show concrete competitor/query visibility evidence

Add a plain-Russian section/table such as:

`Какие выбранные конкуренты реально появились по новым проверочным запросам`

For each of the seven successful exact Search rechecks show:

- tested exact query;
- selected competitor domains actually observed in TOP10;
- observed rank(s);
- if none of the nine selected competitors appeared, write that explicitly rather than leaving the cell blank.

Authority: successful raw Search evidence + `STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv`.

The materialized facts must reconcile to:

- 11 visible direction-domain cells;
- 12 selected-competitor ranking rows;
- 7/9 selected competitors visible across successful rechecks;
- two selected domains not observed in successful rechecks: `aluminarium.ru`, `okna-moskva.ru`;
- `гидроизоляция для открытого балкона`: zero selected competitors visible, while the direction still passed on combined Wordstat demand + current SERP intent/page mix + business fit + semantic novelty.

If one selected domain has two ranking URLs for the same tested query, make that understandable without inflating the number of different competitors.

## 3.4 Explain the inspected-page vs exact-query distinction in client language

The execution found zero exact matches between the 44 earlier inspected competitor URLs and the later exact-query ranking URLs, while same competitor domains still reappeared on different URLs.

Explain this simply, for example:

- the competitor page was used to discover a topic;
- later Yandex Search independently checked the new exact query;
- the same competitor could appear with another page;
- therefore page text was never treated as proof of ranking for the newly discovered phrase.

Do not leak internal methodological jargon.

## 3.5 Make filtering value materially clear

Do not merely say that noise was removed. Explain the measurable result in plain Russian:

- 22 of 43 discovered directions were already covered by the existing core;
- 3 were outside confirmed business scope;
- 4 were held before paid expansion;
- only 14/43 went to Wordstat;
- Wordstat returned 160 rows, but only 20 required Search recheck;
- after Search, 16 phrases were accepted, 3 close variants suppressed, 1 occurrence retained on hold.

This is important client value: the process prevented duplicates/noise/unsupported topics, not only added phrases.

## 3.6 Preserve the two unresolved topics honestly

Keep clearly visible:

- `окна для старого фонда`;
- `кладовая на балконе`.

Explain that current Search outcome was not safely obtained; no retry was performed in the bounded pass; the topics remain undecided rather than being called absent or unsuitable.

## 3.7 Preserve downstream boundary

State plainly:

- 16 phrases are prepared for the next semantic pipeline pass;
- they are not yet part of frozen truth;
- they do not automatically create seven or sixteen pages;
- before next real release they must go through normal cleanup/grouping/ownership/architecture checks.

---

# 4. Gate 10 / owner-review state

Do **not** self-certify Gate 10 as PASS.

After correction the stored state remains:

`CLIENT_FACING_USEFULNESS_GATE = OWNER_REVIEW_REQUIRED`

`PROJECT_TEST_VALIDATED = false`

`LEVEL1_METHOD_PROMOTION_STATE = NOT_PROMOTED`

The correction should make the preview ready for the human owner to decide PASS/REWORK_REQUIRED.

Do not infer owner approval from this correction task.

---

# 5. QA updates required

Update/re-run the Step 5A.8 deterministic QA so hashes/readback remain consistent with the modified preview.

Add/retain checks proving at minimum:

- preview contains exactly 16 accepted phrases, each traceable to delta rows;
- no suppressed/held phrase is presented as accepted;
- preview contains all seven successful tested directions;
- preview contains exactly two unresolved directions;
- all concrete selected-competitor rank claims trace to visibility/Search evidence;
- 11 visible direction-domain cells reconcile;
- 12 selected-competitor ranking rows reconcile;
- zero-selected-competitor visibility for open-balcony waterproofing is explicit;
- no claim that the 44 inspected URLs themselves ranked for the newly discovered exact queries;
- no internal IDs / filenames / enums / developer QA jargon leaked into client-facing prose;
- no page creation/ownership decision introduced;
- `PROJECT_TEST_VALIDATED=true` not persisted;
- Level-1 method not promoted;
- protected Stage-5/client-release/Documents 01–03/semantic-core XLSX unchanged;
- provider/substitute web calls = 0.

If the review workbook contains a client-preview/readiness sheet or hashes that depend on the preview, refresh it as required by the existing builder/validator contract.

Do not change technical information-gain metrics unless a genuine source contradiction is discovered.

---

# 6. Git lifecycle

Use:

`WORK -> SAVE -> COMMIT -> REMOTE GITHUB READBACK -> CONTINUE`

At completion:

1. working tree clean;
2. preview and all dependent QA/readback artifacts remotely present;
3. remote HEAD reported;
4. protected authorities verified unchanged;
5. no provider calls;
6. Gate 10 still `OWNER_REVIEW_REQUIRED` awaiting explicit owner decision.

---

# 7. Completion condition

This correction is complete only when the client preview lets a recipient directly see:

- what was checked;
- what was filtered;
- the seven confirmed demand directions;
- the exact 16 accepted phrases;
- the concrete selected-competitor/query/rank confirmations;
- the two unresolved topics;
- why no new page decision follows automatically;
- what must happen before the next real release.

Next action after PASS:

`OWNER_REVIEW_REVISED_STEP_5A_CLIENT_FACING_PREVIEW_AND_EXPLICITLY_ACCEPT_OR_REJECT_GATE_10`
