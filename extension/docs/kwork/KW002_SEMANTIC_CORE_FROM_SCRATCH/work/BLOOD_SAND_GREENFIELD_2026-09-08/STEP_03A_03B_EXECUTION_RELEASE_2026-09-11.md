# KW-002 Blood & Sand — STEP 03A/03B EXECUTION RELEASE

Date: 2026-09-11  
Status: **EXECUTION RELEASED / OWNER CONTINUE INSTRUCTION RECEIVED / WORK MAY START**  
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`

## 1. Purpose

This file supersedes only the old execution blocker recorded in `STEP_03A_03B_PREPARATION_RECEIPT_2026-09-11.md`.

The Step03A/03B method, pre-step research, manifest and canonical Work prompt remain authoritative.

The owner explicitly instructed the project to continue work on 2026-09-11.

## 2. Step04 publication blocker is closed

The corrected Step04 five-file bundle was published to the shared branch and remotely verified.

Publication commit:

`7ff8d7362d40477a45c38385fe417d224f8085ef`

Required corrected authority is present on remote, including:

- `STEP_04_OCCURRENCE_FAMILY_LEDGER_CORRECTED_2026-09-10.tsv`
- `STEP_04_FAMILY_TRIAGE_CORRECTED_2026-09-10.tsv`
- `STEP_04_TARGETED_EXPANSION_QUEUE_CORRECTED_2026-09-10.tsv`
- `STEP_04_LIMITED_REWORK_QA_2026-09-10.md`
- `STEP_04_LIMITED_REWORK_WORK_RETURN_2026-09-10.md`

Remote publication/readback was independently confirmed as 5/5 exact artifact identity before this release.

Corrected QA remains:

```text
TOTAL_OCCURRENCES = 25979
RESULT_OCCURRENCES = 24722
ASSOCIATION_OCCURRENCES = 1257
UNIQUE_OCCURRENCE_IDS = 25979
UNASSIGNED_OCCURRENCES = 0
DUPLICATE_OCCURRENCE_IDS = 0
FAMILY_ROWS_CORRECTED = 31
CORRECTED_QUEUE_ROWS = 15
OWNER_OR_CLIENT_FACT_ROWS = 5
PROVIDER_RELEVANT_QUEUE_ROWS = 13
KNOWN_AUDITED_DEFECTS_REMAINING = 0
```

The historical Work-return wording `REMOTE READBACK PENDING` is superseded by the later completed publication/readback; do not treat that historical wording as a current blocker.

## 3. Current execution unit

Run the complete mandatory migration:

```text
RAW_OCCURRENCE_POOL (25979)
-> STEP03A NORMALIZED_UNIQUE_POOL + NORMALIZATION_LEDGER
-> STEP03B SANITIZED_CANDIDATE_POOL + EXCLUDED/HOLD REGISTER
-> DATA FUNNEL
-> RECONCILIATION-READY SUMMARY FOR CORRECTED STEP04
```

Use the complete dataset. No sampling, first-N fallback or truncation.

## 4. Canonical Work contract

Primary execution prompt:

`STEP_03A_03B_CANONICAL_WORK_PROMPT_2026-09-11.md`

Pre-step authority:

`STEP_03A_03B_PRE_STEP_REVIEW_AND_WORK_HANDOFF_2026-09-11.md`

Preparation receipt:

`STEP_03A_03B_PREPARATION_RECEIPT_2026-09-11.md`

This release changes execution authorization/blocker state only, plus the artifact-publication amendment below.

## 5. Mandatory new cross-Kwork publication rule

Before execution, Work must also read in full:

`extension/docs/kwork/KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md`

and current:

`LEVEL1/WORK_HANDOFF_RULE.md`

Where an older section of the canonical Work prompt assumes that Work itself must push every large output, the newer owner-locked cross-Kwork publication rule supersedes that transport assumption.

Required policy:

```text
NATIVE AUTHENTICATED GIT PUSH
only if it already works reliably and cheaply

ELSE

OWNER-RELAY WEB PUBLICATION
= Work freezes + QA's exact files
+ provides downloadable files and optional transport ZIP
+ provides direct GitHub upload-files page for exact repo/branch/directory
+ owner uploads exact files in authenticated browser
+ Work/Main ChatGPT performs mandatory remote readback
```

Forbidden by default for large completed artifacts:

```text
base64 through model
full-file chat paste
giant connector arguments
many text chunks used as byte transport
recompute/regenerate only because Git authentication failed
hours of repeated Git-auth debugging when owner relay is available
```

## 6. Checkpoint rule for this execution

This is a large-data Work run. Do not keep all completed work only in local scratch memory until the end.

Use semantic checkpoints.

At minimum:

```text
CHECKPOINT A = STEP03A outputs + QA complete
CHECKPOINT B = STEP03B outputs + QA complete
CHECKPOINT C = data funnel + reconciliation-ready summary + quality score complete
```

At each completed material checkpoint:

```text
save exact artifacts locally
-> run local mechanical QA
-> freeze exact file set / hashes / counts
-> publish with approved transport when practical
-> remote readback before relying on checkpoint as durable authority
```

If native Git authentication is unavailable, immediately use owner-relay rather than spending substantial time/tokens recovering Git authentication.

## 7. Provider and scope boundary

```text
NEW_WORDSTAT_CALLS = 0
NEW_SEARCH_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_AI_SEARCH_CALLS = 0
SEALED_SOURCE_VIOLATIONS = 0
STEP05_ADVANCED = false
STEP06_PLUS_STARTED = false
```

Do not use historical Step05 E013 as an input to the Step03A/03B backfill.

## 8. Delivery cap boundary

Do not invent an order-specific delivery cap.

```text
DELIVERY_KEYWORD_CAP = OWNER_DECISION_REQUIRED
```

This does not block Step03A/03B execution. It blocks final delivery-selection/migration-baseline decisions that require a frozen cap.

## 9. Work return

After completing the execution, return the artifacts/counts/quality score required by the canonical Work prompt.

Do not mark Main ChatGPT acceptance yourself.

Do not continue into Step05.

## 10. Current release state

```text
STEP04_CORRECTED_REMOTE_PUBLICATION = PASS
STEP04_CORRECTED_REMOTE_READBACK = PASS
STEP03A_03B_PRE_STEP = PASS
STEP03A_03B_WORK_TRIGGER = PASS
STEP03A_03B_EXECUTION_AUTHORIZED = true
STEP03A_03B_EXECUTION = READY_TO_START
STEP05 = PAUSED
```

## ПРОСТЫМИ СЛОВАМИ

Проблема с пятью исправленными файлами Step04 закрыта: они уже лежат в GitHub и проверены. Поэтому подготовленный ранее большой этап наконец можно запускать.

Work должен взять все 25 979 сохранённых строк Wordstat целиком, сначала аккуратно схлопнуть повторы без потери происхождения каждой строки, затем убрать только очевидный мусор и отдельно оставить спорные запросы. Никаких новых запросов к Яндексу на этом этапе не нужно.

Если Work создаст большие файлы и не сможет быстро загрузить их обычным Git, он не должен снова тратить часы на авторизацию. Он отдаёт готовые файлы владельцу для обычной загрузки через GitHub, после чего результат проверяется на GitHub. После Step03A/03B работа останавливается для проверки главным ChatGPT; Step05 автоматически не продолжается.
