# KW-002 Blood & Sand — Step04 external methodology review by Main ChatGPT

Date: 2026-09-11
Status: METHOD REVIEW COMPLETE / FULL-VOLUME DATA AUDIT DELEGATED TO WORK

## Scope

This review evaluates the METHOD of the accepted post-sanitation Step04 family triage against current external SEO/search-engine guidance. It does NOT independently reclassify all 18,135 active/HOLD identities or all 25,979 RAW occurrences. Full-volume result quality is delegated to a separate adversarial Work audit.

## External sources checked

1. Yandex Webmaster — Query selection and market analysis
   https://yandex.ru/support/webmaster/ru/service/queries-selection
   - Yandex defines query clustering as automatic grouping of queries similar in meaning or user intent.
   - The tool exposes additional/non-obvious queries and popular sites/pages.

2. Yandex Webmaster — Search quality / Proxima / Proficit
   https://yandex.com/support/webmaster/en/search-quality
   - Search quality is tied to relevance, usefulness and probability of solving the user's objective.

3. Yandex Webmaster — Low-value / low-demand pages
   https://yandex.ru/support/webmaster/en/site-indexing/low-demand
   - Duplicate/low-demand pages can be excluded; pages should correspond to user queries and interests.

4. Yandex Webmaster — Site structure
   https://yandex.ru/support/webmaster/en/recommendations/site-structure
   - Site structure should be clear; documents belong to sections and unique URLs.

5. Topvisor — Clustering by SERP Top-10
   https://topvisor.com/ru/support/clustering/
   - Final keyword clustering can be based on overlap in Yandex/Google Top-10 and is used for site structure.

6. Ahrefs — How To Do Keyword Clustering the Easy Way
   https://ahrefs.com/blog/keyword-clustering/
   - Final keyword clusters should reflect same/similar intent, commonly validated by similar search results.
   - Term clustering (common words/phrases) is useful for understanding trends and niches, but is not the same as final SERP clustering.
   - Clustering is inherently imperfect and requires interpretation.

7. Ahrefs — Search Intent
   https://ahrefs.com/blog/search-intent/
   - Queries can have multiple intents; SERPs reveal content type/format/angle.

8. Semrush — How to Do Keyword Clustering & Why It Helps SEO
   https://www.semrush.com/blog/keyword-clustering/
   - Manual clustering should consider SERP similarity, content quality and user journey.
   - Manual analysis becomes expensive on large lists; tooling is appropriate at scale.

9. Semrush — Methods for keyword clustering and topic modeling
   https://www.semrush.com/blog/what-are-methods-for-keyword-clustering-and-topic-modeling/
   - Common methods combine search intent, SERP overlap, semantic similarity and manual review.

10. Yandex Wordstat operators
    https://yandex.ru/support2/wordstat/ru/content/operators
    - Operators refine acquisition; they are not semantic relevance or page-ownership rules.

## Method verdict

The Step04 architecture is fundamentally sound IF its output is treated strictly as preliminary topical/family triage and NOT as final SEO clustering or query-to-page mapping.

### Strong methodological decisions

1. Stage separation — PASS / strong
   Step04 explicitly avoids final row cleanup, final intent, SERP clustering, query-to-page mapping and IA. This matches external practice: term/topic grouping can be used earlier, while page-level clusters require intent/SERP evidence later.

2. User-task/intent awareness — PASS
   The family authority contains `primary_user_task_hypothesis` and `intent_hint_not_final`, and the method preserves mixed intent. This is aligned with Yandex's user-objective framing and Ahrefs/Semrush intent guidance.

3. Ambiguity preservation — PASS / strong
   HOLD identities remain unresolved instead of being forced into business/out-of-scope decisions. This is methodologically safer than lexical over-classification because many queries have mixed or unclear intent.

4. Business relevance separated from final page ownership — PASS
   Catalog support is used as business lineage but the method explicitly says catalog presence does not prove final user intent/page mapping.

5. Frequency is descriptive, not a relevance rule — PASS
   Yandex exposes demand as a useful prioritization metric, but meaning/intent is the grouping criterion. Step04 correctly avoids using frequency as a semantic assignment rule.

6. Coverage-gap queue — PASS
   Explicit coverage gaps and targeted-expansion queue are methodologically justified. Yandex recommends looking for additional/non-obvious formulations; competitor/content-gap work later in the roadmap is also consistent with standard practice.

7. Reproducibility / lineage — PASS / excellent
   Deterministic rules plus occurrence-level lineage are stronger than ordinary manual SEO workflows because every result can be traced back to provider evidence.

### Method risks / weaknesses

1. Hand-built lexical taxonomy bias — MATERIAL RISK
   Family assignment relies heavily on curated token/prefix/phrase dictionaries and ordered deterministic rules. This is acceptable for pre-triage but can impose the analyst's taxonomy onto the data. External methods emphasize intent, semantic similarity and eventually SERP similarity; therefore lexicon families must never become page clusters without later independent evidence.

2. Very large coarse families — MATERIAL RISK
   Examples: PSF001 (~2,953 identities), PSF006 (~2,109) and PSF014 (~6,540). A coarse family is acceptable as a holding bucket, but it can hide multiple user tasks or missing subfamilies. A full-volume heterogeneity audit is required before trusting family coherence.

3. `STRONG_IN_SCOPE` can be misread downstream — GOVERNANCE RISK
   It means business relevance confidence, not final SEO/page confidence. Recommended future schema separation:
   - business_relevance_confidence
   - family_coherence_confidence
   - final_intent_status
   - serp_cluster_status
   This prevents later steps from treating Step04 family labels as final clusters.

4. Self-QA is not sufficient — MATERIAL RISK
   The same deterministic rules generate families and many regression assertions. Full-volume independent audit should challenge family boundaries with a second method rather than only rerunning the same classifier.

5. Missing independent lexical/semantic cross-check — IMPROVEMENT
   An independent term/subtopic diagnostic should be run over each large family to surface hidden heterogeneity. It must remain diagnostic and must not perform final SERP/page clustering.

6. Family-count quality is not a meaningful KPI — GOVERNANCE RISK
   26 families is neither good nor bad by itself. Quality depends on coherence, boundary precision, preserved ambiguity and downstream usefulness.

## Main ChatGPT method score

This is intentionally independent from Work's prior self-score of 97.20/100.

- Stage design / separation: 10.0/10
- User-task and intent framing: 9.2/10
- Ambiguity handling: 9.7/10
- Traceability / reproducibility: 10.0/10
- Business-boundary discipline: 9.4/10
- Coverage-gap method: 9.2/10
- Resistance to lexical-taxonomy bias: 7.8/10
- Independent semantic validation design: 8.1/10
- Downstream safety: 9.8/10

METHOD_SCORE = 92/100 = 9.2/10

## Interpretation

The method is GOOD and suitable for the role assigned to Step04. It would be methodologically wrong to call the 26 Step04 families final SEO clusters or site pages. The current roadmap avoids that error by postponing final intent/SERP clustering/page ownership.

The biggest unresolved question is not method design but RESULT QUALITY: whether all 18,135 identities were actually assigned to coherent preliminary families without systematic hidden heterogeneity or rule-order leakage. That requires full-volume independent Work audit.

## Required full-volume audit before relying on result quality

Work must independently audit:
- all 18,135 active/HOLD identities;
- all 25,979 occurrence ledger rows for lineage/accounting;
- all 26 family definitions and boundaries;
- all 13 expansion queue rows;
- all 10 sanitation feedback rows;
- family-level heterogeneity, especially PSF001, PSF006, PSF014, PSF018, PSF024;
- classifier rule-order / lexicon bias;
- cases where the same user task is split across families or multiple user tasks are hidden inside one family;
- whether zero-observation coverage gaps are evidence-based;
- whether any Step04 label improperly implies final intent or page ownership.

No provider calls and no Step05/06 execution are allowed in that audit.
