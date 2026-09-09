# KW-002 Blood & Sand — STEP 03 PRE-STEP EXTERNAL RESEARCH AND SOURCE DISCLOSURE

Date checked: **2026-09-09**  
Status: **PASS / OWNER-FACING SOURCE DISCLOSURE REQUIRED BEFORE ANY BRIDGE COMMAND**  
Step: `STEP_03_PRIMARY_WORDSTAT_ACQUISITION`

This artifact is a mandatory companion to:

`STEP_03_PRE_STEP_PROVIDER_GATE_2026-09-09.md`

It implements Level-1:

`PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`

## 1. Exact questions researched before Step 03

Before executing Wordstat, current external research had to answer:

```text
1. What does current Yandex Wordstat / GetTop actually return?
2. What time window does it represent?
3. What result-depth limit is supported?
4. What do results and associations represent in the current API?
5. Are Wordstat operators () and | currently supported for Top queries?
6. Is region 225 Russia?
7. What does DEVICE_ALL mean?
8. What is the current official GetTop price?
9. Does official provider documentation prove our Bridge batch behavior? (No — Bridge capability must be proven separately by project acceptance evidence.)
```

## 2. Sources actually read

### S03-WEB-01 — Yandex Wordstat overview

Publisher / class: **Yandex / OFFICIAL_YANDEX**  
Checked: **2026-09-09**  
Link: [Яндекс Вордстат — Вордстат](https://yandex.ru/support2/wordstat/ru/)

Supports:

- Wordstat shows statistics of Yandex search queries;
- it can show top queries containing selected words;
- it can show what else users searched for on the same topic;
- demand can be viewed across regions and over time.

Step-03 application:

Use Wordstat as direct Yandex human-demand evidence rather than treating Ozon titles or analyst seed wording as search truth.

Claim boundary:

Wordstat demand evidence does not by itself prove business relevance, final intent, cluster or future page ownership.

---

### S03-WEB-02 — Yandex Search API: Wordstat.GetTop

Publisher / class: **Yandex AI Studio / OFFICIAL_PROVIDER**  
Checked: **2026-09-09**  
Link: [Wordstat.GetTop — REST API](https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop)

Supports:

- endpoint `POST /v2/wordstat/topRequests`;
- returns last-30-day popular queries containing the supplied keyword and similar queries;
- `phrase` is required and supports up to 400 characters;
- `numPhrases` supports values from 1 through 2000;
- request accepts regions and devices;
- current response model exposes the provider result for the supplied phrase.

Step-03 application:

- method = `getTop`;
- `numPhrases = 2000` to request the maximum documented result depth;
- persist full provider-returned result rather than a representative subset;
- explicitly record the provider depth boundary and never claim an unlimited hidden universe beyond the response limit.

Claim boundary:

`numPhrases=2000` means maximum documented requested depth; it does not prove Wordstat contains no additional hidden/unreturned universe beyond provider limits.

---

### S03-WEB-03 — Yandex Wordstat GetTop operation guide

Publisher / class: **Yandex AI Studio / OFFICIAL_PROVIDER**  
Checked: **2026-09-09**  
Link: [Getting top results by key phrase](https://aistudio.yandex.ru/en/docs/search-api/operations/wordstat-gettop)

Supports:

- request accepts device filters;
- `DEVICE_ALL` means all devices;
- response example includes `totalCount`, `results[]` and `associations[]`;
- associations are a distinct response section and must not be silently discarded.

Step-03 application:

For every executed item preserve:

```text
totalCount
results[]
associations[]
```

and record `DEVICE_ALL` in lineage.

Claim boundary:

The presence of an association does not automatically make that phrase business-relevant or a final semantic-core row.

---

### S03-WEB-04 — Yandex Wordstat operators

Publisher / class: **Yandex / OFFICIAL_YANDEX**  
Checked: **2026-09-09**  
Link: [Яндекс Вордстат — Операторы](https://yandex.ru/support2/wordstat/ru/content/operators)

Supports:

- Wordstat supports `-`, `!`, `+`, quotes, `[]`, `()` and `|`;
- `()` and `|` group alternatives in complex queries;
- operators are supported for Top queries / query-top surfaces.

Step-03 application:

The 19 V2 qualified OR probes are methodologically valid Wordstat expressions, but the first executed provider item must still test the actual end-to-end Bridge/provider route before mass continuation.

Claim boundary:

Official Wordstat operator support does **not** prove that the current Yandex Marketing Bridge implementation has already been live-tested with this exact grouped expression. Bridge behavior requires separate project capability evidence.

---

### S03-WEB-05 — Yandex search regions

Publisher / class: **Yandex AI Studio / OFFICIAL_PROVIDER**  
Checked: **2026-09-09**  
Link: [Search regions](https://aistudio.yandex.ru/en/docs/search-api/reference/regions)

Supports:

- region ID `225` = Russia.

Step-03 application:

Use:

```text
regions = ["225"]
```

because the frozen client market/search geography is Russia.

Claim boundary:

A country-wide acquisition does not describe city-level regional differences; separate regional analysis would require a named later question/information gain.

---

### S03-WEB-06 — Yandex Search API pricing

Publisher / class: **Yandex AI Studio / OFFICIAL_PROVIDER**  
Checked: **2026-09-09**  
Link: [Правила тарификации для Yandex Search API](https://aistudio.yandex.ru/ru/docs/search-api/pricing)

Supports:

- Wordstat `GetTop` current published price: **20 ₽ per 1000 requests, VAT included**.

Step-03 application:

For the current 79 primary requests:

```text
79 / 1000 × 20 RUB = 1.58 RUB
```

Use a 2 RUB batch hard ceiling as a safe execution bound for the planned 79-request primary set.

Claim boundary:

This is current direct Yandex published tariff truth. Actual Bridge/local accounting metadata must still be reconciled from the real execution results.

---

### S03-WEB-07 — Yandex Wordstat API structure / topRequests

Publisher / class: **Yandex / OFFICIAL_YANDEX**  
Checked: **2026-09-09**  
Link: [Yandex Wordstat — Structure of the API](https://yandex.ru/support2/wordstat/en/content/api-structure)

Supports:

- topRequests is explicitly an acquisition method for popular queries containing a phrase plus similar queries;
- region and device filters are part of the request model;
- requests consume service/request quotas.

Step-03 application:

Treat each seed as a measurement/acquisition input and preserve seed-to-returned-phrase provenance rather than collapsing all observations during acquisition.

Claim boundary:

This older Wordstat API documentation is corroborating conceptual provider behavior; the current Bridge uses the current Yandex Search API v2 contract, so v2 AI Studio documentation remains the current execution authority.

## 3. Source-to-method trace

| Method element | External support | Project-specific application | Executable control |
|---|---|---|---|
| Wordstat as Yandex demand evidence | S03-WEB-01, S03-WEB-02 | Use current Yandex data instead of seller vocabulary as demand truth | Step 03 runs GetTop |
| Maximum result depth | S03-WEB-02 | Request 2000 per seed | `numPhrases=2000` |
| Preserve associations separately | S03-WEB-03 | Do not drop association rows | receipt + raw payload + occurrence layer |
| OR operator semantics | S03-WEB-04 | Q-probes can use grouped alternatives | Q001 first; stop if end-to-end behavior fails |
| Russia region | S03-WEB-05 | Frozen market is Russia | `regions=["225"]` |
| All devices | S03-WEB-03 | No device split requested at primary stage | `devices=["DEVICE_ALL"]` |
| Current tariff | S03-WEB-06 | Estimate 79 calls at 1.58 RUB | `maxCostRub=2` |
| Seed is acquisition input, not final keyword | S03-WEB-01, S03-WEB-07 | preserve all observations for later triage | no KEEP/REJECT in Step 03 |

## 4. Separate Bridge/project evidence

External provider docs do not prove Yandex Marketing Bridge batch behavior.

Current project evidence separately proves:

```text
WORDSTAT_BATCH_API_V1 exists
start/status/pause/resume/cancel cause zero provider requests
one next causes at most one provider request
durable per-item state exists
pause/resume does not replay completed items
OUTCOME_UNKNOWN fails closed
```

Project authorities:

```text
extension/docs/CURRENT_STATE.md
extension/tests/PHASE6_WORDSTAT_BATCH_FINAL_ACCEPTANCE_2026-08-27.md
extension/src/shared/wordstat_batch_protocol.js
extension/src/shared/wordstat_protocol.js
```

This separation is mandatory:

```text
YANDEX DOCS = PROVIDER TRUTH
BRIDGE TESTS/CODE = CURRENT TOOL CAPABILITY TRUTH
JOB RAW RESULTS = CURRENT EXECUTION TRUTH
```

## 5. External-research verdict

```text
FRESH_INTERNET_RESEARCH_PERFORMED = true
OFFICIAL_CURRENT_YANDEX_SOURCES_READ = true
CLICKABLE_SOURCE_LINKS_MATERIALIZED = true
MATERIAL_PROVIDER_PARAMETERS_EXTERNALLY_CHECKED = true
SOURCE_TO_METHOD_TRACE = COMPLETE
PRE_STEP_EXTERNAL_RESEARCH_GATE = PASS
```

Execution still remains blocked until the same clickable source list and supported-claim explanation is shown to the owner in chat, per Level-1 rule.
