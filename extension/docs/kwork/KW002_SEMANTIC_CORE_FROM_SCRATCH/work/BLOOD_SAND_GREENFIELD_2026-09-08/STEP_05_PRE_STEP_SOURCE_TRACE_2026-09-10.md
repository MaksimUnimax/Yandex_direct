# STEP 05 — PRE-STEP SOURCE TRACE

Date checked: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Step: `05 — targeted expansion / coverage control`
Status: **PREPARED / FRESH SOURCE RESEARCH PASS / EXECUTION NOT YET AUTHORIZED**

## Step goal

Use the Step04 family triage and targeted-expansion queue to close material vocabulary/coverage holes without restarting primary acquisition, without turning Step05 into row cleanup, and without using arbitrary fixed seed counts.

## Fresh external sources

| source_id | source_title | publisher | class | url | checked_at | supports | claim boundary |
|---|---|---|---|---|---|---|---|
| S05-WEB-01 | WordstatService.GetTop | Yandex AI Studio / Yandex Search API | OFFICIAL_PROVIDER | https://aistudio.yandex.ru/en/docs/search-api/api-ref/grpc/Wordstat/getTop | 2026-09-10 | GetTop returns last-30-day popular queries containing the phrase plus similar queries; `num_phrases` accepts 1..2000; region/device fields and results/associations are explicit | provider response does not itself prove client relevance or final clustering |
| S05-WEB-02 | Getting top results by key phrase | Yandex AI Studio / Yandex Search API | OFFICIAL_PROVIDER | https://aistudio.yandex.ru/en/docs/search-api/operations/wordstat-gettop | 2026-09-10 | GetTop `phrase` supports search operators; `numPhrases` max 2000 | operator support does not mean every complicated expression is analytically optimal |
| S05-WEB-03 | Операторы | Яндекс Вордстат | OFFICIAL_PROVIDER | https://yandex.ru/support2/wordstat/ru/content/operators | 2026-09-10 | `-`, `!`, `+`, quotes, `[]`, `()` and `|` are supported and combinable; `!` fixes word form; quotes fix word count; brackets fix order; parentheses/pipe group alternatives | operators refine acquisition; they are not relevance rules |
| S05-WEB-04 | Вордстат — Топы запросов | Яндекс | OFFICIAL_PROVIDER | https://yandex.ru/support2/wordstat/ru/interface/new | 2026-09-10 | top-query data covers the last month and includes queries containing the phrase plus similar queries; region/device filters are available | observed association is discovery evidence, not automatic keyword acceptance |
| S05-WEB-05 | Подбор поисковых запросов и анализ рынка β | Яндекс Вебмастер | OFFICIAL_SEARCH_ENGINE | https://yandex.ru/support/webmaster/ru/service/queries-selection | 2026-09-10 | additional/non-obvious query formulations are a legitimate discovery route; word-form fixing and negative terms are supported in query selection | does not define Blood & Sand business boundaries or final page ownership |
| S05-WEB-06 | Квоты и лимиты Yandex Search API | Yandex AI Studio | OFFICIAL_PROVIDER | https://aistudio.yandex.ru/ru/docs/search-api/concepts/limits | 2026-09-10 | Wordstat statistics quota: 10 requests/second and 100/hour; associations max 20 | project persistence rule is stricter and remains sequential |
| S05-WEB-07 | Правила тарификации Yandex Search API | Yandex AI Studio | OFFICIAL_PROVIDER | https://aistudio.yandex.ru/ru/docs/search-api/pricing | 2026-09-10 | Wordstat GetTop = 20 RUB per 1000 requests, i.e. 0.02 RUB/request at current RUB tariff | actual billing still depends on provider/account conditions and request success |

## Current project capability evidence

Current project evidence independently proves that the active `yandex-marketing-bridge` v0.1.4 path can execute Wordstat `getTop` with:

```text
phrase
numPhrases = 2000
regions = ["225"]
devices = ["DEVICE_ALL"]
results[]
associations[]
totalCount
request_executed
automatic_retry
```

The Step03 recovery executed 17 sequential current GetTop requests at envelope estimate 0.02 RUB each, persisting every useful result before the next request. Authority: `STEP_03_RAW_RECOVERY_FINAL_RECEIPT_2026-09-10.md` plus the individual recovery receipts/raw carriers.

## Source-to-method conclusion

Fresh sources confirm the Step05 method and narrow it as follows:

```text
TARGETED EXPANSION != RESTART PRIMARY COLLECTION
TARGETED EXPANSION != FINAL CLEANUP
TARGETED EXPANSION != FINAL CLUSTERING
USE QUALIFIED PHRASES / OPERATORS WHEN THEY DIRECTLY ADDRESS OBSERVED NOISE
DO NOT USE LOW FREQUENCY AS A STOP/REJECT RULE
DO NOT FAN OUT VARIANTS AUTOMATICALLY
AFTER EACH USEFUL PROBE: PERSIST -> REMOTE READBACK -> REASSESS INFORMATION GAIN
```

Because Step04 already produced an evidence queue, Step05 must start from that queue rather than inventing a new seed universe.

## Current queue split

Step04 queue = 17 rows.

Ready for provider evidence after explicit Step05 authorization and without new client facts:

```text
E001,E002,E003,E006,E007,E008,E009,E010,E011,E013,E014
COUNT = 11
```

Blocked on client/owner fact before or alongside provider work:

```text
E004,E005,E012,E015,E016,E017
COUNT = 6
```

Provider evidence is eventually relevant to 15/17 queue rows; E015 and E016 are fact-only boundaries and must not be "solved" with Wordstat.

## First-probe rationale

The safest first Step05 acquisition after authorization is queue `E013`, using the Wordstat word-form operator to isolate the noun `чётки` from observed morphology noise `чётко/чёткий`.

Candidate first request:

```text
phrase = !чётки
numPhrases = 2000
region = 225
device = DEVICE_ALL
expected provider requests now = 1
current tariff estimate = 0.02 RUB
```

This request does not claim final relevance. It is a controlled coverage/noise diagnostic. No second provider request is allowed until the complete result is durably persisted and read back.

## Execution gate

```text
PRE_STEP_EXTERNAL_RESEARCH = PASS
SOURCE_TO_METHOD_TRACE = PASS
STEP04_INPUT_QUEUE = 17/17 READ
STEP05_PROVIDER_CALLS_EXECUTED = 0
STEP05_PROVIDER_CALLS_AUTHORIZED = false
STEP05_EXECUTION = HOLD_PENDING_EXPLICIT_PROVIDER_AUTHORIZATION
```
