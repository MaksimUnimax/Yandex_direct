# KW-001 — VOLUME SCALING / EARLY SANITATION METHOD RESEARCH

Date: 2026-09-10  
Status: **METHOD RESEARCH COMPLETE / OWNER-APPROVED ROADMAP INPUT**  
Scope: universal KW-001 product; OKNO_MSK is only the current size reference, not a permanent method input.

## 1. Research question

Does the same scalability lesson exposed by KW-002 also apply to KW-001 when a site/catalog is much larger than the current rehearsal?

Answer: **yes for early normalization/sanitation and seed design; no for importing the KW-002 1500-phrase commercial ceiling.**

## 2. Current KW-001 architecture finding

KW-001 already has an important downstream scale control:

- Step7 performs row-level semantic cleanup before Step8 Search-stage freeze;
- Step9 ordinary Search is not conceptually required for every raw occurrence;
- Step15/16 use bounded AI diagnostic/control cases rather than bulk-running every phrase through Alice.

The scalability weakness exists earlier:

```text
Step3 RAW acquisition
-> Step4 family triage
-> Step5 targeted expansion
-> Step5A competitor expansion
-> only then Step7 deep cleanup
```

For a small corpus this is manageable. For a large catalog it can force Step4/5/5A and Work to carry tens or hundreds of thousands of duplicate/noisy occurrences before the first deep cleanup.

## 3. Official Yandex evidence

Source:
https://yandex.ru/support/webmaster/ru/service/queries-selection

Yandex Webmaster describes query selection across hundreds of millions of unique searches and explicitly provides:

- negative words to exclude non-target queries;
- automatic clusters for semantically/intent-similar queries;
- demand, clicks and competitiveness as selection signals;
- additional query discovery for non-obvious wording.

Method implication for KW-001:

```text
EARLY NON-TARGET EXCLUSION = NORMAL PRACTICE
QUERY SELECTION != KEEP EVERY DISCOVERED RAW ROW
VOLUME ALONE != KEYWORD VALUE
```

## 4. Progressive-cleaning evidence

Source:
https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/

Topvisor's 2025 methodology lists:

- implicit duplicates;
- non-target queries;
- wrong-intent queries;
- symbols/empty rows;
- optional frequency thresholds depending on strategy;
- cleanup before clustering when mass reduction is needed;
- final cleanup after clustering.

It explicitly recommends gradual cleanup: obvious junk first, then strategy-dependent filtering, then final review.

Method implication:

```text
ONE LATE CLEANUP STAGE IS NOT THE ONLY VALID MODEL
EARLY MASS SANITATION + LATE NUANCED CLEANUP = SUPPORTED PRACTICE
```

## 5. Tens-of-thousands evidence

Source:
https://journal.topvisor.com/ru/seo-kitchen/how-to-clean-queries/

Topvisor states that manually checking thousands/tens of thousands of queries is not practical and describes tool-assisted cleanup using negative words, frequency filters, implicit duplicates and later manual validation.

Method implication:

Large KW-001 jobs require machine-assisted compaction before expensive manual/LLM work.

## 6. Implicit duplicate evidence

Source:
https://www.key-collector.ru/docs/tools/implicit-duplicates/

Key Collector defines implicit duplicates as phrases made from the same words in different order and supports form-dependent/form-independent matching, synonyms/exceptions and automatic marking rules.

Method implication:

```text
RAW PROVIDER OCCURRENCES
MAY REMAIN LOSSLESS
WHILE
ANALYTICAL DUPLICATES ARE COLLAPSED
```

The duplicate operation must be conservative because word order can sometimes change meaning.

## 7. E-commerce category/subcategory evidence

Source:
https://ahrefs.com/blog/ecommerce-seo/

Ahrefs recommends using keyword research to align category and subcategory pages with how people search. It warns that not every possible term deserves its own subcategory and notes that product keyword research differs for branded versus unknown/unbranded products.

Method implication:

```text
CATALOG SKU COUNT != SEARCH-ENTITY COUNT
```

For a large store, search discovery should begin from meaningful category/subcategory/product-type/use/attribute and brand/model structures rather than one mandatory broad probe per SKU.

## 8. Large product-page research evidence

Source:
https://ahrefs.com/blog/ecommerce-product-page-seo/

Ahrefs gives the example that manually researching target keywords for 20,000 products would take weeks and recommends scraping product data and using bulk keyword-data workflows for large sites.

Method implication:

Large-catalog SEO requires bulk/machine processing and selective human analysis. A model that requires an LLM to reason manually over every raw product/query occurrence is not scalable.

## 9. What does NOT follow from the sources

The sources do not establish:

```text
one universal percentage that must be removed
one universal minimum frequency
one universal maximum number of active KW-001 phrases
one rule that every low-frequency phrase is bad
one rule that all word-order variants are always identical
```

Therefore the correction is structural, not an arbitrary threshold.

## 10. Corrected KW-001 architecture

```text
Step2 search-entity probe design
-> Step3 LOSSLESS RAW
-> Step3A normalization / exact + safe implicit dedup
-> Step3B high-confidence sanitation
-> Step4 family triage on compact candidates
-> Step5 expansion -> immediate 3A/3B
-> Step5A competitor expansion -> immediate 3A/3B
-> Step7 nuanced semantic cleanup
-> Step8 Search-stage freeze
-> bounded Search / clustering / Alice work downstream
```

## 11. Why the current ~2300 active phrases are not themselves a defect

A final active semantic core can legitimately contain more than 1500 phrases if they are relevant, traceable and grouped into coherent tasks/clusters.

The scalability problem is not `2300 > some magic number`.

The problem is:

```text
TENS/HUNDREDS OF THOUSANDS OF RAW OCCURRENCES
BEING TREATED AS
TENS/HUNDREDS OF THOUSANDS OF EXPENSIVE SEMANTIC DECISIONS
```

KW-001 therefore receives the early normalization/sanitation gate but no copied KW-002 commercial phrase ceiling.

## 12. Required future validation

The next materially large KW-001 catalog rehearsal should record a complete funnel:

```text
catalog/search-entity counts
seed count
RAW occurrences
normalized unique
sanitized candidates
Step7 active/reject/review
Search-stage set
Search observations
AI diagnostic cases
Work/analyst effort
```

This will show whether the permanent scalability correction is sufficient or whether another bounded selection layer is required for KW-001 commercial packaging.