# KW-002 — VOLUME PIPELINE / KWORK PACKAGE / KEYWORD SELECTION RESEARCH

Date: 2026-09-10
Status: **METHOD RESEARCH COMPLETE / OWNER-APPROVED ROADMAP INPUT**
Scope: universal KW-002 product design; Blood & Sand is only the first rehearsal that exposed the scaling defect.

## 1. Research questions

1. Is it normal for raw keyword acquisition to produce tens of thousands of rows while a client Kwork delivers hundreds or ~1000–1500 phrases?
2. When should most junk/duplicates disappear?
3. What does an extra `+500 keywords` package mean in real Kwork offers?
4. Should the next 500 be selected purely by frequency?
5. How should KW-002 separate machine evidence from expensive analyst/LLM/Search work?

## 2. Current Kwork market evidence

### Example A — base 100, expansion to 500 and 1500

Kwork:
https://kwork.ru/keywords/53185723/soberu-semanticheskoe-yadro-dlya-sayta-sbor-i-klasterizatsiya-klyuchey

Observed offer:
- base service volume: 100 keywords;
- paid option: expanded core up to 500;
- paid option: large core up to 1500;
- output promises Wordstat frequency, junk/non-target cleaning, clustering, page grouping and intent marking.

Interpretation:
The package number is clearly a client-result scope, not a raw Wordstat scrape limit.

### Example B — 500 grouped phrases after manual cleaning

Kwork:
https://kwork.ru/keywords/51997366/semanticheskoe-yadro

Observed offer:
- up to 500 grouped phrases;
- high/mid/low-frequency mix;
- base + exact frequency;
- manual cleaning of junk/non-thematic phrases.

Interpretation:
The final set is deliberately mixed across demand tiers and cleaned before delivery; it is not `top 500 raw phrases by volume`.

### Example C — 1000 cleaned/clustered phrases

Kwork:
https://kwork.ru/keywords/45633833/sbor-chistka-i-klasterizatsiya-semanticheskogo-yadra-pod-klyuch

Observed offer:
- service volume: 1000 keywords;
- process includes niche analysis, collection from several sources, duplicate/junk/non-relevant/stop-word cleaning, clustering and manual control.

Interpretation:
Again the commercial count applies after cleaning and structuring.

### Example D — current Kwork category pricing is expressed per 100 delivered keywords

Kwork landing:
https://kwork.ru/land/semanticheskoe-yadro-s-wordstat

Observed examples include:
- services priced per 100 keywords;
- a listing explicitly titled `до 500 сгруппированных ключевых фраз`;
- multiple sellers with different client-facing phrase volumes.

Interpretation:
Keyword count is a commercial unit of delivered scope in this market.

### Example E — technical collection can be larger than final core

Kwork:
https://kwork.ru/keywords/53663932/semanticheskoe-yadro-pod-klyuch-seo-struktura-polniy-aeo

Observed wording:
- deep final core around 1200+ requests;
- technical additional collection up to 2400.

Interpretation:
This is direct market evidence for separating `technical/raw candidate volume` from `final delivered core`.

### Example F — final quantity depends on project

Kwork:
https://kwork.ru/keywords/37043902/sbor-semanticheskogo-yadra-dlya-kontekstnoy-reklamy-yandeks-direkt

Observed offer:
- up to 500 keys;
- junk cleaning + negative keywords + clustering;
- seller explicitly states that actual final keyword count is individual to the project.

Interpretation:
`up to N` is a ceiling, not a promise to manufacture exactly N phrases.

## 3. Professional cleaning evidence

### Yandex Webmaster — select suitable queries, minus words and potential

https://yandex.ru/support/webmaster/ru/service/queries-selection

Yandex states that its tool can:
- choose suitable target queries;
- find additional non-obvious wording;
- analyze query potential and choose promising formulations;
- use minus words to remove non-target requests;
- use demand, clicks and competition to help choose keywords.

Implication:
Early exclusion of clearly non-target branches is normal; selection is multi-factor and not raw-volume-only.

### Topvisor — progressive cleaning

https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/

Method points:
- remove implicit duplicates, non-target phrases, symbols/empty junk;
- cleaning before clustering is appropriate when the goal is mass reduction for later analysis;
- clean progressively: obvious junk first, then optional frequency-based filtering, then final check after clustering.

Implication:
KW-002 should not postpone all cleaning until late Step10.

### Topvisor implicit duplicate normalization

https://topvisor.com/ru/support/implicit-duplicates/

Method points:
- normalize word forms/order/stop words;
- keep the strongest/canonical variant where safe;
- remove semantic repeats without manual row-by-row reading.

### Key Collector implicit duplicates

https://www.key-collector.ru/docs/tools/implicit-duplicates/

Method points:
- detects same-word-set permutations;
- supports form-dependent/form-independent modes, synonyms/exceptions;
- automatic rule-based marking can keep stronger variants.

Implication:
Machine-assisted compaction is standard for large lists.

## 4. Keyword priority is NOT frequency-only

### Yandex

https://yandex.ru/support/webmaster/ru/service/queries-selection

Yandex explicitly surfaces demand, clicks and competitiveness as selection signals and says they help choose keywords for optimization/promotion.

### Ahrefs — intent as early filter

https://ahrefs.com/blog/keyword-intent/

Keyword intent is described as an early research filter for deciding whether a keyword belongs in the strategy at all.

### Ahrefs — strategy/prioritization

https://ahrefs.com/blog/keyword-strategy/

Ahrefs recommends prioritizing clusters using business potential and rankability, grouping related terms rather than treating each variation as an isolated target.

### Ahrefs — keyword analysis

https://ahrefs.com/blog/keyword-analysis-for-seo/

The decision whether to target a keyword considers:
- traffic potential;
- whether the searcher need can be served;
- business value;
- ability to rank.

It explicitly warns against choosing by search volume alone.

## 5. Answer: where do the extra +500 come from?

In a product with a delivery cap, the proper model is:

```text
large RAW/candidate acquisition
-> normalization/deduplication
-> sanitation
-> relevance/intent/business-value review
-> prioritized valid pool
-> first purchased tranche
-> VALID RESERVE
```

The paid `+500` primarily promotes the next 500 valid phrases from the reserve according to coverage-aware priority.

They are not automatically the next 500 by raw frequency.

Good expansion candidates can include:
- deeper long-tail variants in already important commercial clusters;
- secondary product/use families that did not fit the base cap;
- informational support queries with real business value;
- additional regional/attribute/selection formulations;
- valid competitor-derived demand discovered later.

If the reserve contains fewer than 500 worthwhile phrases, `up to +500` should not be padded with junk. New acquisition is justified only when the paid scope requires legitimate additional coverage and the current reserve is insufficient.

## 6. Required KW-002 architecture correction

Old weak model:

```text
RAW 25k+
-> semantic family triage of almost every occurrence
-> more acquisition
-> more acquisition
-> cleanup only late
-> expensive Search/clustering
```

Corrected model:

```text
RAW evidence (unlimited by delivery cap)
-> Step03A normalization / exact + safe implicit dedup
-> Step03B conservative sanitation
-> compact candidate pool
-> Step04 family triage
-> each expansion immediately passes 03A/03B
-> Step09 cleaned candidate master + reserve
-> Step10 nuanced relevance/intent/priority
-> Step11 enforce purchased delivery cap
-> Search/SERP/clustering only for selected set
-> final client core <= purchased cap
```

## 7. Product policy conclusion

For ordinary KW-002:

```text
STANDARD_KWORK_DELIVERY_CEILING = 1500 final phrases
RAW may be much larger
CUSTOM >1500 only by explicit owner-approved scope
```

This 1500 ceiling is a current commercial/productization safety policy informed by the observed Kwork market, not a claim that SEO methodology universally forbids larger cores.

The base package size remains a separate pricing/product decision. The roadmap only requires that the purchased cap be frozen before acquisition and enforced before expensive Search/SERP processing.

## 8. Blood & Sand implication

Blood & Sand's 25,979 Step03 occurrences remain valid lossless evidence.

They must no longer be treated as 25,979 equally expensive semantic candidates.

Before Step05 resumes:

```text
existing Step03 RAW
-> backfill Step03A normalization
-> backfill Step03B sanitation
-> reconcile corrected Step04 against the compact candidate layer
-> record candidate/reserve counts
-> only then resume targeted expansion
```

No provider replay is required merely because the universal pipeline changed.