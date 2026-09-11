# KW-002 Blood & Sand — Main ChatGPT review of independent Step04 full-volume result audit

Date: 2026-09-11
Status: **AUDIT ACCEPTED / STEP04 REWORK REQUIRED / STEP05 REMAINS BLOCKED**

## Publication authority

Repository: `MaksimUnimax/Yandex_direct`  
Branch: `roadmap/kwork-productization-2026-08-28`  
Audit publication commit: `212a6fa7be66360317b3026541896669b8b019c6`  
Audit publication parent: `8a09e1610d68f61769b6a4d44d1382cab4dd37b7`

The owner-uploaded audit commit is exactly one commit above the audit execution release and changes exactly 16 expected job-root files. No unrelated paths were introduced in that upload.

## Main ChatGPT verdict

```text
STEP04_INDEPENDENT_RESULT_AUDIT = ACCEPTED
STEP04_CURRENT_RESULT = REWORK_REQUIRED
STEP05_ALLOWED = false
STEP06_ALLOWED = false
NEW_PROVIDER_CALLS = 0
```

The earlier operational acceptance of post-sanitation Step04 remains historical evidence that the artifact was mechanically complete and traceable. It is superseded as a semantic result verdict by this accepted independent full-volume audit.

The exact numeric Work score `67.69/100` is retained as a diagnostic audit score, not treated as an objective probability or percentage of truth. The rework decision does not depend on that score: three reproducible material rule/family defects are independently sufficient to block PASS.

## Remote readback

Verified from the published commit:

- artifact manifest present;
- audit report present;
- Work return present;
- local audit QA present;
- full-volume audit overlay published for 24,576 normalized identities;
- family coherence authority published for all 26 families;
- 26×26 symmetric family-boundary matrix published with 676 rows;
- queue/feedback audit published for all 13 queue rows and all 10 feedback rows plus 3 missing audit classes;
- 20 audit anti-regression controls published;
- independent audit materializer published;
- metrics authority published;
- `JOB_FLOW.md`, `JOB_MANIFEST.md`, current cursor and Work handoff log updated in the owner relay.

The large 13 MB audit overlay is exposed remotely as a Git blob. As with earlier large TSV readbacks, the connector does not provide a raw byte stream for an independent Main ChatGPT SHA-256 recomputation. Therefore this review does not falsely claim an independently recomputed remote SHA-256 for that file. The published manifest preserves the Work-local SHA-256 and row count.

## Full-volume accounting accepted

```text
NORMALIZED_IDENTITIES = 24576
ACTIVE_PLUS_HOLD_IDENTITIES = 18135
EXCLUDED_IDENTITIES_HISTORY = 6441
RAW_OCCURRENCES = 25979
UNIQUE_RAW_OCCURRENCE_IDS = 25979
RAW_LINEAGE_LOSS = 0
STEP03B_STATE_OR_REASON_MISMATCHES = 0
```

The audit did not re-triage Step03B, did not modify accepted Step04 artifacts and did not advance Step05/06.

## Material defect 1 — PSF019 game prefix collision

Accepted finding:

```text
AFFECTED_IDENTITIES = 8
CURRENT_FAMILY = PSF019
AUDIT_SIGNAL = TOY WITHOUT GAME
ROOT_CAUSE = broad `игр*` prefix
```

Main ChatGPT independently inspected the current Step04 materializer. `has_game_signal()` uses `has_token_prefix(text, ("игр", ...))`. This necessarily matches `игрушка/игрушки/...` as well as game morphology. The same game detector is evaluated before several other family routes, so the defect is an underlying rule defect rather than an isolated example error.

Required correction:

- remove broad `игр*` detection;
- use exact game morphology / bounded explicit game signals;
- model `игруш*` separately from GAME;
- rerun the complete frozen Step04 universe;
- do not patch only the eight currently observed identities.

## Material defect 2 — PSF014 early zodiac route hides explicit tasks

Accepted finding:

```text
AFFECTED_UNIQUE_IDENTITIES = 199
MEANING = 156
MEDIA = 38
TOY = 5
CURRENT_FAMILY = PSF014
ROOT_CAUSE = zodiac branch precedence / incomplete signal coverage
```

Main ChatGPT independently inspected `assign_family()`. The zodiac branch executes before later catalog/media/general semantic routes. Inside that branch it checks product/commerce/form, visual, a limited `ASTRO_INFO`, stone, then falls through to `PSF014`. It does not test the more informative general `MEANING`, `MEDIA`, or TOY task classes before the unqualified-zodiac fallback.

This conflicts with the PSF014 definition: the family says the phrase lacks enough task qualification, while the affected phrases contain explicit task signals.

Required correction:

- rework zodiac signal precedence and coverage;
- preserve zodiac as context but do not let it erase a stronger explicit task;
- route meaning/media/physical-toy cases according to their supported preliminary task, without claiming final intent or page ownership;
- rerun the whole frozen universe and audit the blast radius, not only the 199 rows.

## Material defect 3 — PSF001 hides explicit DIY task

Accepted finding:

```text
AFFECTED_IDENTITIES = 48
CURRENT_FAMILY = PSF001
SIGNALS = сделать / создать / изготовить / связать / сшить / сплести / своими руками and equivalents
ROOT_CAUSE = missing DIY/make/craft preliminary boundary before generic product fallback
```

Main ChatGPT inspected the current KEEP routing: after existing collision and semantic checks, a remaining product word falls through to `PSF001` (`SUPPORTED_GENERIC_PRODUCT_UNQUALIFIED`). There is no DIY task detector before that fallback.

Therefore these rows are not genuinely "without sufficient task qualification". They contain a coherent make/craft task.

Required correction:

- add an explicit preliminary DIY/make/craft task boundary or marker;
- do not infer final informational intent/page from that marker;
- rerun all active/HOLD identities so sibling rows are captured by the rule rather than a 48-row patch.

## Queue audit accepted

Current Step04 queue = 13 rows.

Accepted audit split:

```text
VALID_GAP = 2
OWNER_FACT_FIRST = 5
DUPLICATES_EXISTING_EVIDENCE = 5
DEFER_TO_LATER_INTENT_OR_SERP = 1
```

The five duplication findings are material to Step05 safety:

- PSQ005: combined Ом/Аум probe duplicates existing qualified Ом evidence in material part and must be narrowed if an Аум-only gap remains;
- PSQ006: Гунгнир/Копьё Одина already has qualified evidence;
- PSQ007: named catalog/entity set already has qualified evidence;
- PSQ008: Белобог/Чернобог/Мара already has qualified evidence;
- PSQ010: historical durable E013 `!чётки` evidence already exists and must not be replayed.

No provider call is authorized from the old queue.

## Sanitation-feedback audit accepted

Nine of ten existing feedback classes are justified. `PSFB003` is too broad because the PSF019 family contains the eight false toy/game assignments.

Three missing material feedback classes are accepted for the correction pass:

1. PSF001 DIY task hidden by generic fallback;
2. PSF014 explicit task hidden by zodiac route;
3. PSF019 toy/game prefix collision.

These remain Step04 findings. Step03B is not mutated by this acceptance.

## Independent diagnostic interpretation

The TF-IDF / 32-topic MiniBatchKMeans / centroid analysis is accepted as an auxiliary adversarial diagnostic, not as ground truth and not as final clustering. It usefully challenged large-family heterogeneity without substituting for later SERP/intent evidence.

The method boundary from the earlier external review still holds:

```text
STEP04 = PRELIMINARY FAMILY / TOPIC / TASK TRIAGE
STEP04 != FINAL SEO CLUSTERING
STEP04 != FINAL INTENT
STEP04 != QUERY->PAGE OWNERSHIP
STEP04 != SITE IA
```

## Supersession state

```text
STEP04_POST_SANITATION_OPERATIONAL_ACCEPTANCE = HISTORICAL / MECHANICAL-TRACEABILITY PASS
STEP04_EXTERNAL_METHOD_REVIEW = PASS FOR PRELIMINARY TRIAGE METHOD
STEP04_INDEPENDENT_RESULT_AUDIT = ACCEPTED / REWORK_REQUIRED
CURRENT_STEP04_SEMANTIC_AUTHORITY = NOT READY FOR DOWNSTREAM USE
```

Step05 W06 remains paused. Step06 remains not started.

## Required next action

Perform a rule-level full-volume corrective rerun of Step04 using:

- unchanged accepted Step03A;
- unchanged accepted corrected Step03B;
- frozen client/Ozon scope;
- original post-sanitation Step04 only as the superseded result being corrected;
- the accepted independent audit overlay/report/metrics as defect authority;
- the three new defect classes as blocking regressions;
- queue deduplication and feedback correction as part of the same rerun.

No Wordstat, ordinary Search, GenSearch, AI-search or Step05/06 execution is allowed during that corrective pass.
