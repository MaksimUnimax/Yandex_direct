# KW-002 / BLOOD & SAND — STEP07 POST-EXTERNAL-METHOD AUDIT — 2026-09-18

Status: **REWORK_REQUIRED / STEP08 BLOCKED**

## Scope

This audit re-evaluates the accepted Step07 result against fresh external methodology and the actual published Step07 candidate/provenance corpus.

No new provider, browser, Wordstat, Search, AI Search or GenSearch calls were made.

## Fresh external sources

1. Yandex Webmaster — Query selection and market analysis  
   https://yandex.ru/support/webmaster/ru/service/queries-selection  
   Supports: competitor/market analysis, non-obvious query discovery, explicit exclusion of non-target queries, and later demand/click/competition evaluation.

2. Semrush — How to find competitor keywords and close visibility gaps (2026-06-16)  
   https://www.semrush.com/blog/competitor-keywords/  
   Supports: manual review of titles/headings/navigation/product/blog pages as seed discovery; manual review does not prove search demand; competitor topics unrelated to the business must be filtered by what the business actually sells.

3. Ahrefs — Keyword Competitive Analysis  
   https://ahrefs.com/blog/keyword-competitive-analysis/  
   Supports: search competitors may differ from business competitors; candidate topics still require business-value/relevance judgment.

4. Ahrefs — Content Gap Analysis  
   https://ahrefs.com/blog/content-gap-analysis/  
   Supports: irrelevant topics should be excluded; multi-competitor intersection may be used as a confidence/prioritization signal; keyword gaps are based on actual ranking keywords rather than arbitrary page text.

## Current Step07 external-audit findings

Published Step07 current corpus:
- candidate identities = 2172
- provenance rows = 3948
- current Step08-eligible = 1548
- NEW_CANDIDATE = 1540
- POSSIBLE_VARIANT = 8

Evidence concentration among 1548 eligible:
- single competitor source = 1502
- multi-source = 46
- top source contribution:
  - livemaster.ru = 400
  - kartaslov.ru = 268
  - avito.ru = 254

Main Chat bounded diagnostic surfaced 121 / 1548 eligible candidates with obvious adjacent/off-scope lexical signals requiring full-volume review. This 121 set is NOT the rework scope and MUST NOT become a patch list. It is evidence of a producer-level business-scope defect.

Concrete regression examples currently still eligible include:
- Винтажная настольная лампа в форме Будды на одну светоточку
- Настольная лампа с фигурой Будды
- Картхолдер Молот Тора Руна Одал ручной работы из кожи
- Латунный состаренный ваджрный пестик и ступка латунный брелок золотой кулон
- Картина Подкова
- Подсвечник Молот Тора

Page-wrapper/listing-noise examples currently still eligible include:
- Ассоциации к слову «амулет»
- Ассоциации к слову «оберег»
- Ассоциации к словосочетанию «рунические знаки»
- Джапа — это повторение любой мантры или имени Бога
- Амулет с руной Феху — привлекает богатство и благополучие

## External-audit verdict

Step07 collection/coverage/provenance work remains accepted.

The defect is limited to the semantic handoff into Step08:
COMPETITOR PAGE / PRODUCT / TITLE TEXT
must not become Step08 candidate merely because it contains an in-scope symbol/token.

Required second limited rework:
- no new crawl/browser/provider work;
- full-volume review of ALL 1548 currently Step08-eligible candidates;
- use full provenance/source context;
- enforce frozen client business scope;
- separate page/title/listing wrappers from underlying semantic concepts;
- derive a compact candidate only when transformation is reproducible and business-relevant;
- otherwise route OUT_OF_SCOPE or AMBIGUOUS;
- multi-source evidence is confidence/prioritization, not automatic acceptance;
- single-source evidence remains allowable if independently valid and business-relevant.

External audit score:
QUALITY_TOTAL = 86/100
QUALITY_SCORE = 8.6/10
VERDICT = REWORK_REQUIRED
STEP08 = BLOCKED
