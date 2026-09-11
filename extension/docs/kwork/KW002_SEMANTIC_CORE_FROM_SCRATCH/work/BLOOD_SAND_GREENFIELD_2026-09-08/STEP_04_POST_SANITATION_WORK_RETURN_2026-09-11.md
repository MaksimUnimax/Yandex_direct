# KW-002 Blood & Sand — post-sanitation Step04 Work return

Date: 2026-09-11
Status: **FULL-VOLUME EXECUTION COMPLETE / LOCAL QA PASS CANDIDATE / MAIN CHATGPT RETURN QA REQUIRED**

## Execution result

The corrected Step03B authority was used unchanged. All 18,135 KEEP+HOLD identities received one deterministic preliminary primary family; all 6,441 excluded identities were preserved as excluded history; all 25,979 RAW occurrences were materialized one-to-one.

```text
LIVE_BASE_HEAD = 640f1f3416319019fa362e7bb1b442532f6e1058
STEP03A_AUTHORITY = PASS / UNCHANGED
STEP03B_CORRECTED_AUTHORITY = ACCEPTED INPUT / UNCHANGED

TOTAL_NORMALIZED_IDENTITIES = 24576
TOTAL_RAW_OCCURRENCES = 25979
ACTIVE_PLUS_HOLD_IDENTITIES_TRIAGED = 18135
EXCLUDED_IDENTITIES_HISTORY = 6441

POST_SANITATION_FAMILY_COUNT = 26
POST_SANITATION_OBSERVED_FAMILY_COUNT = 24
POST_SANITATION_EXPANSION_QUEUE_ROWS = 13
SANITATION_FEEDBACK_ROWS = 10

OCCURRENCE_LEDGER_ROWS = 25979
UNIQUE_OCCURRENCE_IDS = 25979
UNASSIGNED_OCCURRENCE_IDS = 0
UNEXPECTED_DUPLICATE_OCCURRENCE_IDS = 0
RAW_LINEAGE_LOSS = 0

KNOWN_FAILURE_REGRESSION = PASS
F03B_COLLISION_REGRESSION = PASS
F04_OCCURRENCE_REPRODUCIBILITY = PASS
F04_RULE_LEVEL_RERUN = PASS
UPSTREAM_INVALIDATION_HANDLED = PASS

NEW_WORDSTAT_CALLS = 0
NEW_SEARCH_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_AI_SEARCH_CALLS = 0
SEALED_SOURCE_VIOLATIONS = 0
STEP05_STARTED = false

QUALITY_SCORE_100 = 97.20
QUALITY_SCORE_10 = 9.72
STEP04_POST_SANITATION_VERDICT = PASS_CANDIDATE
PUBLICATION = OWNER_RELAY_REQUIRED
REMOTE_READBACK = PENDING_OWNER_UPLOAD
STEP05_ALLOWED = false
```

## Frozen generated artifacts before publication-state documents

| file | bytes | SHA-256 |
|---|---:|---|
| `STEP_04_POST_SANITATION_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv` | 16281168 | `c053bcd1dccae5b2894cc7a316c84af72c2b0abfeb460624f138f1198a39a5ba` |
| `STEP_04_POST_SANITATION_FAMILY_TRIAGE_2026-09-11.tsv` | 33145 | `cb2a1259f596f1b97ea4eb662e8c8b315936aad2243c57389c290ea6d90a0b2c` |
| `STEP_04_POST_SANITATION_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv` | 12274 | `be46fd75e9b51354e14dfc3e862be69e8549fd67b708ecc7471bbfc3dcd63c73` |
| `STEP_04_POST_SANITATION_SANITATION_FEEDBACK_REGISTER_2026-09-11.tsv` | 8148 | `7a52efa3eb2e8eeebddecd61de4550acf33e98b8d357b463e815754f6af00903` |
| `STEP_04_POST_SANITATION_HISTORICAL_COMPARISON_2026-09-11.tsv` | 18855 | `e8c107ca8f277feb39e382fe8a21f013f17a477c215320edcdbc2f6b6c092909` |
| `STEP_04_POST_SANITATION_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-11.tsv` | 3186 | `824405b45304bc5120166f9c6aa3e886b954f40daea660307477271ca0d40109` |
| `STEP_04_POST_SANITATION_QA_2026-09-11.md` | 15048 | `23daeed34f724bfa8b86de4c5189d72793e0ba7e4955e37130b4d1b624b73429` |
| `STEP_04_POST_SANITATION_MATERIALIZER_2026-09-11.py` | 107955 | `3b80e56d81b02efa4e26c43d9caa92e22f4115738028f0e83a85218ce92f4ad2` |

The owner-relay transport package also includes this return, the artifact manifest and the three current-state documents. The ZIP is transport only and is not repository authority; extracted individual files must be uploaded before Main ChatGPT remote readback.

## What changed from historical Step04

- Historical family authority: 31 rows, 25 with observed occurrences.
- New authority: 26 family rows, 24 observed and 2 explicit zero-observation coverage gaps.
- New primary family assignment is based on corrected Step03B state/reason and phrase context; historical family IDs never enter the classifier.
- The three empty exact-name queue items are consolidated into one bounded multi-name item; all other accepted corrected queue concerns remain separately traceable.
- Possible remaining sanitation issues are routed to 10 non-destructive feedback rows rather than changing Step03B.

## ПРОСТЫМИ СЛОВАМИ

Историческая группировка устарела, потому что исправленная очистка изменила статус 1 710 фраз и затронула 23 из 25 прежних групп. Поэтому мы не подправляли старые итоговые строки, а заново разобрали весь актуальный и спорный массив.

Теперь все подходящие и неоднозначные фразы разложены по предварительным смысловым семьям: отдельно видны покупки, товары для машины, чётки, конкретные символы, знаки зодиака и зоны пересечения с астрологией, религией, медиа, играми, автомобилями и чужими сущностями. Неоднозначность не уничтожена: спорные строки не получили окончательный вердикт и ждут более поздних доказательств. Все исходные появления и их происхождение сохранены без потерь.

Локально Step04 выполнен полностью и проходит проверку с оценкой 97.20/100 (9.72/10). Для публикации подготовлен owner-relay: после загрузки извлечённых отдельных файлов Main ChatGPT должен сверить удалённые blob-версии. Step05 не запускался и остаётся закрыт до независимого принятия возврата Main ChatGPT.
