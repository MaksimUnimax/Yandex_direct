# KW-002 Blood & Sand — Step05 post-Step04 pre-step external research

Date checked: 2026-09-11
Status: **PRE-STEP RESEARCH PASS / PROVIDER EXECUTION NOT YET RELEASED**

## Current scope

Current Step05 authority must start from the accepted post-sanitation Step04 queue:

`STEP_04_POST_SANITATION_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv`

Current queue rows: **13**.

The historical 2026-09-10 Step05 trace was based on a superseded 17-row Step04 queue. Its methodology/provider facts remain useful only where revalidated; its queue accounting is superseded.

Historical durable provider evidence must not be discarded or blindly replayed. In particular, preserved E013 `!чётки` evidence is a candidate for reuse after mapping to the current queue.

## Current Level-2 Step05 method

Current Level-2 purpose:

- close material vocabulary holes created by initial seeds or revealed by Step04;
- use owner/client clarification when business boundaries are unclear;
- preserve all new RAW evidence and provenance;
- immediately route any new provider rows through Step03A normalization and corrected Step03B sanitation;
- stop when another acquisition branch has low expected information gain;
- never expand merely to fill a commercial delivery cap.

## Fresh external sources

### S05-20260911-01 — Yandex Wordstat / main help

URL: https://yandex.ru/support2/wordstat/ru/

Publisher/class: Yandex / OFFICIAL_PROVIDER

Checked: 2026-09-11

Supports:
- Wordstat provides statistics on Yandex search queries;
- it can show top queries containing selected words and other queries searched on the same topic;
- it supports regional comparison and demand exploration.

Boundary:
- Wordstat observation is demand/discovery evidence, not proof of client relevance, final intent, final cluster or page ownership.

### S05-20260911-02 — Yandex Wordstat / Top queries interface

URL: https://yandex.ru/support2/wordstat/ru/interface/new

Publisher/class: Yandex / OFFICIAL_PROVIDER

Checked: 2026-09-11

Supports:
- Top queries reports last-month popular queries containing a phrase and similar queries;
- region and device filters are available.

Boundary:
- similar-query association is discovery evidence and may contain noise/foreign meanings.

### S05-20260911-03 — Yandex Wordstat operators

URL: https://yandex.ru/support2/wordstat/ru/content/operators

Publisher/class: Yandex / OFFICIAL_PROVIDER

Checked: 2026-09-11

Supports:
- operators can refine acquisition;
- `-` excludes words;
- `!` fixes word form;
- quotes fix word count;
- `[]` fixes word order;
- `()` and `|` group alternatives.

Boundary:
- operator support is not a semantic relevance rule; operators are only justified when they answer a specific observed coverage/noise question.

### S05-20260911-04 — Yandex Search API Wordstat.GetTop

URL: https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop

Publisher/class: Yandex AI Studio / OFFICIAL_PROVIDER

Checked: 2026-09-11

Supports current provider contract:

```text
GetTop period = last 30 days
phrase max length = 400 characters
numPhrases = 1..2000
regions max elements = 100
devices include DEVICE_ALL/DESKTOP/PHONE/TABLET
response = totalCount + results[] + associations[]
```

Boundary:
- provider response does not prove final business fit or downstream SEO architecture.

### S05-20260911-05 — Getting top results by key phrase

URL: https://aistudio.yandex.ru/en/docs/search-api/operations/wordstat-gettop

Publisher/class: Yandex AI Studio / OFFICIAL_PROVIDER

Checked: 2026-09-11

Supports:
- `phrase` supports search operators;
- `numPhrases` max is 2000;
- region/device parameters are explicit.

Boundary:
- a technically valid operator expression is not automatically the best analytical probe.

### S05-20260911-06 — Yandex Search API quotas and limits

URL: https://aistudio.yandex.ru/en/docs/search-api/concepts/limits

Publisher/class: Yandex AI Studio / OFFICIAL_PROVIDER

Checked: 2026-09-11

Current Wordstat limits relevant here:

```text
statistics requests per second = 10
statistics requests per hour = 100
maximum associations = 20
```

Project anti-regression boundary is stricter: Step05 remains sequential and persistence/readback/information-gain reassessment occurs before the next probe.

### S05-20260911-07 — Yandex Search API pricing

URL: https://aistudio.yandex.ru/ru/docs/search-api/pricing

Publisher/class: Yandex AI Studio / OFFICIAL_PROVIDER

Checked: 2026-09-11

Current RUB rate:

```text
Wordstat GetTop = 20 RUB / 1000 requests = 0.02 RUB/request
```

Boundary:
- actual account billing may depend on provider/account conditions; cost never justifies skipping persistence or semantic QA.

### S05-20260911-08 — Yandex Webmaster query selection and market analysis

URL: https://yandex.ru/support/webmaster/ru/service/queries-selection

Publisher/class: Yandex / OFFICIAL_SEARCH_ENGINE

Checked: 2026-09-11

Supports:
- discovery of additional/non-obvious formulations;
- demand/click/competition analysis;
- refinement by word form, negative words, region and device;
- additional query vocabulary is a legitimate discovery route.

Boundary:
- Webmaster discovery does not define Blood & Sand business boundaries or final query→page ownership.

### S05-20260911-09 — Ahrefs seed keywords

URL: https://ahrefs.com/blog/seed-keywords/

Publisher/class: Ahrefs / INDUSTRY_METHOD

Checked: 2026-09-11

Supports:
- seed choice strongly affects discovered vocabulary;
- additional seed/modifier vocabulary can expose subtopics missed by the initial seed list.

Boundary:
- this is industry corroboration, not a Yandex rule.

### S05-20260911-10 — Semrush current keyword research workflow

URL: https://www.semrush.com/blog/how-to-use-semrush-keyword-research/

Publisher/class: Semrush / INDUSTRY_METHOD

Checked: 2026-09-11

Supports:
- expand from known terms into new related search terms;
- gap discovery must remain relevant to core topics;
- expansion and later clustering are distinct activities.

Boundary:
- this is industry practice, not current Yandex provider behavior.

## Provider/Bridge evidence from this project

Current project evidence already proves `yandex-marketing-bridge` can execute the saved `WORDSTAT_BATCH_API_V1` contract with:

```text
phrases[]
numPhrases = 2000
regions = ["225"]
devices = ["DEVICE_ALL"]
maxRequests
maxCostRub
```

The canonical historical command syntax is preserved in:
`STEP_03_WORDSTAT_BATCH_START_COMMAND_2026-09-09.txt`.

A preserved Step05 provider request already exists:

```text
historical queue item = E013
phrase = !чётки
request_id = wordstat-132a43ff-7cf9-4544-a6e2-68da666c4813
results = 2000
associations = 19
remote readback = PASS
raw blob = 550add6010ddbd10e0d807fd1a11046d2b782a4a
```

Authority:
`STEP_05_E013_WORDSTAT_EVIDENCE_RECEIPT_2026-09-10.md`.

This durable evidence must be mapped to the new queue before any replay. `PROVIDER_SUCCESS != COLLECTION_COMPLETION` remains active, and `DURABLE_EXISTING_EVIDENCE != REPLAY_REQUIRED` is added as the current anti-regression rule.

## Method conclusion

```text
STEP05 != RESTART STEP03
STEP05 != EXECUTE EVERY QUEUE ROW
STEP05 != FINAL CLEANUP
STEP05 != FINAL INTENT
STEP05 != SERP CLUSTERING
STEP05 != FILL DELIVERY CAP

CURRENT QUEUE -> FACT/REUSE/DEFER/NEW-PROBE GATE
NEW PROBE -> ONE MATERIAL QUESTION
NEW PROVIDER RESULT -> DURABLE RAW -> READBACK -> 03A -> CORRECTED 03B -> UNION
NEXT PROBE -> ONLY AFTER INFORMATION-GAIN REASSESSMENT
```

## Execution gate

Fresh research is complete, but provider execution is not released by this file.

Before the first new provider call, a full current-queue reconciliation must:

1. map all 13 current queue rows;
2. reuse durable E013 evidence where applicable;
3. check candidate probes against Step02/Step03 acquisition history to prevent duplicate collection;
4. freeze exact probe intent, phrase/operator expression, max request count, max cost and stop condition;
5. select only the first justified probe;
6. materialize a pre-acquisition QA/manifest;
7. return for Main ChatGPT verification.

```text
PRE_STEP_EXTERNAL_RESEARCH = PASS
CURRENT_QUEUE_ROWS = 13
NEW_PROVIDER_CALLS_IN_THIS_GATE = 0
STEP05_PROVIDER_EXECUTION_RELEASED = false
```
