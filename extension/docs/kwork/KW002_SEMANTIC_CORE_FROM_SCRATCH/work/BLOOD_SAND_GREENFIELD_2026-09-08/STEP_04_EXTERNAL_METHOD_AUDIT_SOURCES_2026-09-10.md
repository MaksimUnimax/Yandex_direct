# STEP 04 — EXTERNAL METHOD AUDIT SOURCES

Date checked: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Purpose: external-method authority for a retrospective quality audit of the **first completed Step04 family triage**, not a new execution of Step04 and not Step05.

## Audit question

Assess whether the completed Step04 correctly performed a preliminary family-level demand triage from the full Step03 Wordstat corpus, using concrete published methodology rather than model intuition.

The audit must distinguish two layers:

1. **Step04 family triage / topic boundary screening** — preliminary grouping, business-fit screening, ambiguity/entity collision handling, obvious noise identification, coverage-gap detection.
2. **Later final keyword clustering / page decisions** — intent + SERP similarity/overlap + page/user-journey evidence, which belongs to later roadmap steps and must NOT be demanded from Step04.

## Source hierarchy

Use sources in this order of authority for the audit:

1. Official Yandex / Yandex Webmaster / Wordstat sources for Yandex-demand interpretation and Yandex terminology.
2. Current professional SEO methodology from Ahrefs and Semrush as corroborative industry practice.
3. Foundational information-retrieval literature only for general intent concepts.

Industry sources are not allowed to override explicit Yandex behavior or the frozen Blood & Sand business facts.

## External sources and method elements

### S04-AUD-01 — Yandex Webmaster training: demand research

Title: `Обучение — Как работать со спросом в поиске Яндекса`
Publisher: Yandex Webmaster
URL: https://yandex.ru/support/webmaster/ru/training
Checked: 2026-09-10

Method elements supported:
- demand research includes **structuring demand and understanding what the niche consists of**;
- finding **relevant** search queries is a separate task;
- checking whether search queries are **suitable for promotion of the site** is a separate task;
- landing-page construction comes after those research tasks.

Audit application:
- Step04 should be judged as a demand-structuring and suitability-screening layer, not as final page construction;
- a family being observed in Wordstat is not enough by itself to make it business-relevant.

Claim boundary:
- this source does not prescribe the exact five project triage labels or a numeric scoring rubric.

### S04-AUD-02 — Yandex Webmaster: query selection and market analysis

Title: `Подбор поисковых запросов и анализ рынка β`
Publisher: Yandex Webmaster
URL: https://yandex.ru/support/webmaster/ru/service/queries-selection
Checked: 2026-09-10

Method elements supported:
- select queries that are **suitable** for the site;
- discover additional queries with **non-obvious wording**;
- analyze query potential rather than assuming every discovered query should be targeted.

Audit application:
- unfamiliar/non-obvious vocabulary should not be automatically rejected;
- coverage gaps and targeted-expansion candidates are legitimate outputs of preliminary triage;
- business suitability must remain distinct from raw discovery.

### S04-AUD-03 — Yandex Webmaster: official clustering definition

Title: `Добавили кластеризацию в «Подбор запросов и анализ рынка β»`
Publisher: Yandex Webmaster Blog
Published: 2025-12-19
URL: https://webmaster.yandex.ru/blog/wordcraft-clusterization
Checked: 2026-09-10

Method elements supported:
- Yandex describes clustering as grouping queries close by **meaning or user intent**;
- clusters characterize a particular niche;
- informational and commercial meanings can require separation;
- clusters can reveal themes already covered and themes that are missing.

Audit application:
- semantic meaning / user-purpose signals are stronger family boundaries than token coincidence alone;
- the audit should test whether Step04 families mix materially different referents/intent signals without marking ambiguity;
- missing-topic/coverage-gap decisions are legitimate when grounded in observed evidence.

Critical boundary:
- this source discusses a downstream clustering product. The current roadmap deliberately reserves final SERP-backed keyword clustering and page ownership for later steps. Therefore **do not penalize Step04 merely because it did not produce final page-level clusters**.

### S04-AUD-04 — Yandex Webmaster: understand how users formulate needs

Title: `На какие вопросы отвечает ваш сайт`
Publisher: Yandex Webmaster
URL: https://yandex.ru/support/webmaster/ru/recommendations/targeting?lang=ru
Checked: 2026-09-10

Method elements supported:
- understand how users formulate their needs as search queries;
- Wordstat related queries can expose synonyms and words that clarify or extend the seed;
- query popularity can fluctuate because of seasonality/events.

Audit application:
- associations/related branches are discovery evidence, not automatic acceptance;
- raw count alone is insufficient for a business-fit verdict;
- synonyms and non-obvious related wording should survive long enough to be evaluated semantically.

### S04-AUD-05 — Yandex Wordstat operators / refinement

Title: `Операторы`
Publisher: Yandex Wordstat
URL: https://yandex.ru/support2/wordstat/ru/content/operators
Checked: 2026-09-10

Method elements supported:
- Wordstat supports refinement with `-`, `!`, `+`, quotes, `[]`, `()` and `|`;
- operators can narrow morphology, word count, order and alternative branches.

Audit application:
- when Step04 identifies a coverage/noise boundary that can be tested by a qualified acquisition later, routing it to targeted expansion is methodologically legitimate;
- Step04 itself should not have to solve every ambiguity by guessing.

Claim boundary:
- operators refine acquisition; they do not determine business relevance or final cluster membership.

### S04-AUD-06 — Ahrefs: keyword intent as an early research filter

Title: `Keyword Intent: What It Is and How to Use It in Your SEO Strategy`
Publisher: Ahrefs
Published: 2026-03-13
URL: https://ahrefs.com/blog/keyword-intent/
Checked: 2026-09-10

Method elements supported:
- intent is the reason behind a query;
- intent/business usefulness can be applied **during keyword research**, before content planning;
- if the query cannot realistically be served by the site/product, attractive volume does not make it strategically suitable;
- branded/entity-like terms can carry different intents;
- mixed intent exists and should not be forced into an oversimplified bucket.

Audit application:
- Step04 should be rewarded for preserving real ambiguity rather than forcing keep/reject;
- volume must not rescue an obviously wrong entity/referent;
- business/assortment fit must be explicit.

Claim boundary:
- Ahrefs is Google-oriented industry practice, not an official Yandex rule. Use it as corroboration.

### S04-AUD-07 — Ahrefs: ambiguous topic boundaries

Title: `How to Focus on Topics (Not Keywords) in Your SEO Strategy`
Publisher: Ahrefs
Published: 2026-03-04
URL: https://ahrefs.com/blog/topics-not-keywords/
Checked: 2026-09-10

Method elements supported:
- a topic is a conceptual space around meaning, intent and related ideas, not one lexical token;
- ambiguous topics can use exactly the same words while referring to different meanings/entities;
- entity/brand context can be the main differentiator;
- ambiguous topic membership needs **better signals than keyword volume**;
- success requires clear topic boundaries and removal/holding of off-topic/ambiguous terms.

Audit application:
- directly test Blood & Sand collision handling such as Chery Amulet vs amulet product demand, Om/Aum, Gungnir/game meanings, media/book/game/person/place collisions, zodiac product demand vs generic astrology;
- token similarity must not be treated as enough to join a family.

Claim boundary:
- industry methodology; use as external corroboration, not as a substitute for client truth.

### S04-AUD-08 — Ahrefs: term clustering vs intent/SERP clustering

Title: `Keyword Clustering in Seconds: Save Time With Keywords Explorer Tool`
Publisher: Ahrefs
URL: https://ahrefs.com/blog/keyword-clustering-tools/
Checked: 2026-09-10

Method elements supported:
- **term clustering** groups by words/phrases and is useful for trends, niches and preliminary topical buckets;
- page-oriented keyword clustering aims to group keywords with the same/similar intent.

Audit application:
- preliminary Step04 family buckets are legitimate as an exploratory layer;
- they must not be mislabeled or treated as final page clusters.

### S04-AUD-09 — Ahrefs: final keyword clustering generally needs SERP evidence

Title: `How To Do Keyword Clustering the Easy Way`
Publisher: Ahrefs
URL: https://ahrefs.com/blog/keyword-clustering/
Checked: 2026-09-10

Method elements supported:
- page-oriented keyword clustering groups keywords with the same/similar intent;
- a common practical signal is same/similar search results;
- clustering output is not perfect and remains open to interpretation.

Audit application:
- do not demand final page-level clustering from Step04 because the KW-002 roadmap deliberately obtains ordinary Yandex Search evidence later;
- flag any Step04 row only if it **prematurely claims** final page/cluster truth, not because final SERP clustering is absent.

### S04-AUD-10 — Semrush: intent, SERP similarity, user journey and low-volume aggregation

Title: `How to Do Keyword Clustering & Why It Helps SEO`
Publisher: Semrush
Published: 2025-10-29
URL: https://www.semrush.com/blog/keyword-clustering/
Checked: 2026-09-10

Method elements supported:
- clustering is centered on same search intent;
- subtle wording differences can indicate different goals;
- manual grouping considers SERP similarity, content coherence and user journey;
- low-volume queries can have meaningful combined potential;
- business/industry relevance is a separate input to keyword selection.

Audit application:
- low frequency alone must never be a Step04 reject reason;
- audit whether grouped family members have coherent meaning/user-purpose at the preliminary level;
- final same-page decisions remain downstream because SERP similarity is not yet available at Step04.

### S04-AUD-11 — Semrush: multiple valid clustering signals

Title: `What are methods for keyword clustering and topic modeling?`
Publisher: Semrush
Published: 2025-09-25
URL: https://www.semrush.com/blog/what-are-methods-for-keyword-clustering-and-topic-modeling/
Checked: 2026-09-10

Method elements supported:
- grouping can use search intent, SERP overlap, semantic similarity or manual review.

Audit application:
- a preliminary semantic/manual family triage is a legitimate pre-SERP organization step;
- final cluster assertions need stronger evidence than lexical similarity alone.

### S04-AUD-12 — Foundational information-retrieval intent taxonomy

Title: `A taxonomy of web search`
Author: Andrei Z. Broder
Publication: SIGIR Forum 36 (2002), pp. 3–10
URL: https://research.google/pubs/a-taxonomy-of-web-search/
Checked: 2026-09-10

Method element supported:
- web search needs are not one-dimensional; informational, navigational/entity and transactional goals are materially different classes of user need.

Audit application:
- use only as foundational support for the principle that identical/similar terms can represent different user goals.

Claim boundary:
- historical foundational literature; not a current Yandex implementation specification.

## Source-to-method synthesis for the Step04 audit

The external sources support the following audit method:

```text
M01 FULL INPUT BEFORE JUDGMENT
    Evaluate the complete observed corpus, not a convenience sample.

M02 BUSINESS FIT IS SEPARATE FROM DEMAND
    Wordstat occurrence/frequency proves observed demand context, not that the client should target it.

M03 SEMANTIC / USER-PURPOSE BOUNDARIES BEAT TOKEN MATCHING
    Group by meaning/topic/use/referent and user-purpose signals; identical tokens can belong to different entities.

M04 AMBIGUITY MUST STAY EXPLICIT
    If the available Step04 evidence cannot reliably resolve a referent or intent boundary, HOLD/mixed/coverage-gap is preferable to invented certainty.

M05 VOLUME IS NOT A RELEVANCE VERDICT
    High volume cannot rescue an off-topic entity; low volume alone cannot justify rejection.

M06 RELATED / NON-OBVIOUS WORDING IS COVERAGE EVIDENCE
    Preserve plausible synonyms/related branches when business-supported; route unresolved gaps to targeted expansion.

M07 PRELIMINARY TOPICAL BUCKETS != FINAL SEO CLUSTERS
    Family triage can organize a large corpus semantically before SERP evidence exists.

M08 FINAL PAGE CLUSTERING IS DOWNSTREAM
    Same-page/page-owner decisions need intent + ordinary search/SERP evidence; their absence at Step04 is not a defect.

M09 PROVENANCE MUST SURVIVE SUMMARIZATION
    Every family/gap conclusion must remain traceable to observed data and client/business authority.

M10 NO POST-HOC JUSTIFICATION
    Score the first Step04 result using only evidence available by the end of Step04. Later Step05 `!чётки` evidence must not increase or rescue the Step04 score.
```

## Hard audit boundaries

The audit MUST NOT:
- use later Step05 provider evidence to justify the original Step04 score;
- make new Wordstat, Yandex Search, GenSearch, Alice or AI-search evidence calls;
- use sealed prior Blood & Sand SEO research;
- penalize Step04 for not doing Step10 row cleanup, Step12 Search acquisition, Step13 SERP clustering or Step14 page ownership;
- silently edit the existing Step04 output during the audit.

The audit MAY:
- browse/read the public methodology URLs above to verify claims;
- programmatically re-read the complete current Step03 feed-forward corpus;
- independently reconstruct a reference family/boundary map from the same end-of-Step04 evidence;
- compare that independent reference against every one of the original 32 family rows and 17 expansion-queue rows;
- recommend corrections, but must keep them separate from the original artifacts until owner review.

## Scoring convention

The exact historical text of the earlier 10-point rubric was not preserved as a durable authority. The repository does preserve the previous scoring presentation convention, e.g. `93/100 = 9.3/10` for Step02. For this audit, use the explicit weighted 100-point rubric in the companion Work prompt and convert directly:

```text
QUALITY_SCORE_10 = QUALITY_SCORE_100 / 10
```

Do not invent another scoring system.