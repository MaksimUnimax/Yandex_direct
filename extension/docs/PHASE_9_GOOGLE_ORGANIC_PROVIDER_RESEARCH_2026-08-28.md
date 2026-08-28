# PHASE 9 — Google organic provider research

Date: 2026-08-28

Status: **PROVIDER RESEARCH COMPLETE / ARCHITECTURE GATE REQUIRED BEFORE IMPLEMENTATION**

## 1. Question

Phase 9 must determine whether Yandex Marketing Bridge can add useful Google organic evidence without pretending that an unofficial scraper is an official Google API and without collapsing unlike evidence surfaces into one misleading `rank` concept.

Required evidence jobs:

```text
A. first-party Google performance for a site we are authorized to inspect
B. arbitrary keyword Google SERP / TOP-domain competition
C. cross-engine Yandex-vs-Google comparison
D. future longitudinal Google rank evidence
```

The research must keep these jobs separate because Google exposes different official surfaces for different purposes.

## 2. Official Google surfaces reviewed

### 2.1 Search Console API — ACCEPTABLE FOR FIRST-PARTY SITE PERFORMANCE

Official docs:

- https://developers.google.com/webmaster-tools/
- https://developers.google.com/webmaster-tools/v1/searchanalytics/query
- https://developers.google.com/webmaster-tools/v1/how-tos/all-your-data
- https://developers.google.com/webmaster-tools/limits
- https://developers.google.com/webmaster-tools/pricing
- https://support.google.com/webmasters/answer/7042828

What it provides for Search Console properties to which the caller has access:

```text
query
page
country
device
date/hour where supported
clicks
impressions
ctr
average position
search type / appearance filters
```

Key constraints:

```text
authorization required for a managed Search Console property
rowLimit <= 25,000 per request
Search Analytics exposes at most 50,000 rows/day/search-type
some query/page detail may be omitted
results are not an exhaustive arbitrary Google SERP
position is an average over impressions, not a deterministic live rank
```

Google explicitly defines Search Console position as a relative/average metric and warns that an observed manual search can differ because location, history and other factors vary.

Pricing:

```text
Search Console API = free of charge
subject to quotas/load limits
```

Decision:

```text
GOOGLE_SEARCH_CONSOLE_FIRST_PARTY_EVIDENCE = TECHNICALLY_AND_POLICY_ACCEPTABLE
```

This is the strongest official Google first slice.

### 2.2 Custom Search JSON API — REJECT FOR NEW PRODUCTION WORK

Official docs:

- https://developers.google.com/custom-search/v1/overview
- https://developers.google.com/custom-search/v1/introduction

Current Google notice:

```text
closed to new customers
existing customers must transition by 2027-01-01
```

The API searches through a configured Programmable Search Engine and is not a durable new production dependency for this project.

Decision:

```text
CUSTOM_SEARCH_JSON_API = REJECT
reason = closed_to_new_customers + scheduled_discontinuation
```

### 2.3 Vertex AI Search — REJECT FOR GENERAL GOOGLE SERP/RANK

Google recommends Vertex AI Search as an alternative for searching a bounded set of domains/data sources. That is useful for owned/curated retrieval but not a consumer Google organic SERP or generic competitor rank surface.

Decision:

```text
VERTEX_AI_SEARCH = NOT_A_GENERAL_GOOGLE_SERP_REPLACEMENT
```

### 2.4 Grounding with Google Search — USEFUL AI EVIDENCE, NOT ORGANIC RANK

Official docs:

- https://ai.google.dev/gemini-api/docs/google-search
- https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/grounding-with-google-search

The response can expose model search calls, search suggestions and cited source URLs for a grounded generative answer.

It does **not** provide a stable deterministic list that can safely be labeled:

```text
Google organic position 1..N
consumer SERP TOP-N
historical organic rank
```

Decision:

```text
GOOGLE_SEARCH_GROUNDING = DISTINCT_AI_SEARCH_EVIDENCE_ONLY
```

If ever used, provenance must remain separate from ordinary Google organic evidence just as Yandex GenSearch remains separate from ordinary Yandex Search.

## 3. Direct Google consumer-SERP scraping

Google Terms prohibit automated access that violates machine-readable instructions. More importantly for this project, a self-hosted Google scraper would create unstable parser/proxy/CAPTCHA maintenance and a legal/ToS surface that is unrelated to the Bridge's core value.

Decision:

```text
SELF_HOSTED_GOOGLE_SERP_SCRAPER = REJECT
```

The Bridge must not implement direct consumer Google scraping.

## 4. Third-party SERP providers reviewed

Third-party providers can technically supply arbitrary Google SERP evidence, but they are not official Google APIs. Their collection/legal posture therefore must remain explicit.

### 4.1 DataForSEO Google Organic SERP API

Docs / pricing / terms:

- https://docs.dataforseo.com/v3/serp-google-organic-overview/
- https://docs.dataforseo.com/v3/serp-google-overview/
- https://dataforseo.com/pricing/serp/google-organic-serp-api
- https://dataforseo.com/terms-of-service
- https://dataforseo.com/blog/is-scraping-google-serps-legal

Technical capabilities include:

```text
keyword
location
language
device / OS
organic result positions
rank_group / rank_absolute
SERP features
10+ result depth
Standard queue / Priority / Live modes
```

Current published base pricing observed on 2026-08-28:

```text
Standard: $0.0006 per 10-result SERP
Priority: $0.0012 per 10-result SERP
Live: $0.002 per 10-result SERP
```

For the Phase-8-like 500-key / TOP-10 class this is technically cheap:

```text
500 x TOP-10 Standard ~= $0.30 base provider cost
```

Important boundary:

DataForSEO itself describes the underlying process as Google SERP scraping. Its older legal explainer states that automated Google queries violate Google's ToS while arguing that API customers are not themselves making those queries. That is provider-supplied legal interpretation, not a Google authorization and not legal advice.

Decision:

```text
DATAFORSEO = TECHNICAL_FRONT_RUNNER_FOR_EXTERNAL_SERP
production_contract = NOT_YET_AUTHORIZED
```

### 4.2 SerpApi Google Search API

Docs / pricing / legal:

- https://serpapi.com/search-api
- https://serpapi.com/organic-results
- https://serpapi.com/pricing
- https://serpapi.com/legal

Technical fit is strong: location/device controls, structured organic positions and rich SERP elements.

However, Google filed Google LLC v. SerpApi LLC in 2025 over scraping/circumvention allegations. A first complaint was dismissed in July 2026, but Google filed an amended complaint in August 2026 and the dispute remains active. SerpApi separately advertises a U.S. Legal Shield on qualifying plans.

Decision:

```text
SERPAPI = TECHNICALLY_VALID_BUT_CURRENTLY_HIGHER_LEGAL_EVENT_RISK
production_contract = NOT_AUTHORIZED_DURING_ACTIVE_GOOGLE_LITIGATION
```

This is not a finding that SerpApi is unlawful. It is a product-risk decision: there is no reason to freeze a new production dependency while its exact collection model is the subject of active litigation and a cheaper technical alternative exists.

## 5. Research conclusion

There is no single current official Google API that provides both:

```text
first-party Search Console performance
AND
arbitrary competitor Google organic TOP/rank
```

Therefore Phase 9 must be split instead of pretending one provider solves both jobs.

Recommended architecture:

```text
P9-A OFFICIAL FIRST-PARTY GOOGLE EVIDENCE
provider = Google Search Console API
purpose = owned/authorized site performance
metrics = query/page/clicks/impressions/ctr/average_position
status = architecture/test-first work may proceed

P9-B EXTERNAL GOOGLE SERP EVIDENCE
provider candidate = DataForSEO
purpose = arbitrary keyword TOP/rank/domain competition
status = technical candidate only; separate legal/commercial/provider gate required

P9-C GOOGLE AI SEARCH EVIDENCE
provider candidate = Google Search grounding
purpose = AI answer/source evidence only
status = out of ordinary-organic Phase-9 first slice
```

## 6. Provenance rules

Permanent distinctions:

```text
GSC_AVERAGE_POSITION != LIVE_GOOGLE_SERP_RANK
GSC_QUERY_OBSERVATION != ARBITRARY_KEYWORD_SERP
THIRD_PARTY_GOOGLE_SERP != OFFICIAL_GOOGLE_API
GOOGLE_SEARCH_GROUNDING_SOURCE != GOOGLE_ORGANIC_RANK
YANDEX_SERP_RANK != GOOGLE_SERP_RANK
```

Any future cross-engine report must label provider, market/location, device, timestamp and metric semantics.

## 7. Service-registry architecture consequence

Current production registry is intentionally exactly five Yandex services:

```text
wordstat
search
webmaster
metrika
direct
```

Google Search Console must **not** be smuggled into `webmaster` or `search` merely to preserve the number five. It has different provider identity, OAuth ownership, authorization scope and evidence semantics.

Therefore implementation requires one explicit architecture decision before product bytes change:

```text
Option A — introduce a sixth provider service: google_search_console
Option B — introduce a provider-neutral evidence registry above existing Yandex services
Option C — keep Google as import-only/out-of-extension evidence
```

Research recommendation:

```text
preferred = Option A for the first slice
service = google_search_console
protocol = GOOGLE_SEARCH_CONSOLE_API_V1
credential = dedicated Google OAuth / never reused from Yandex
writes = disabled
```

Reason: the smallest truthful design is better than over-generalizing a provider-neutral framework before a second non-Yandex provider exists.

This recommendation intentionally changes the previous five-service invariant and therefore must be accepted through a dedicated architecture gate/test contract rather than silently coded.

## 8. Proposed P9-A first slice

Read-only methods only:

```text
listSites
searchAnalytics
```

Potential later method after first slice:

```text
inspectUrl
```

Not in first slice:

```text
sitemap writes
property writes
indexing requests
Google Ads
arbitrary Google SERP scraping
DataForSEO
SerpApi
Google Search grounding
```

Minimal Search Analytics request contract should bound:

```text
siteUrl
startDate / endDate
search type = web first
optional dimensions: query,page,country,device,date
optional exact/contains filters
rowLimit <= 25,000
bounded pagination
read-only OAuth scope
```

## 9. Next gate

Authorized next engineering sequence after this research record:

```text
P9-00 freeze exact main and service-registry baseline
P9-01 architecture audit of provider registry / credentials / popup / policy / OAuth patterns
P9-02 freeze explicit decision to add google_search_console as sixth service or reject it
P9-03 test-first GOOGLE_SEARCH_CONSOLE_API_V1 protocol
P9-04 read-only listSites/searchAnalytics runtime with local stub only
P9-05 pagination/quota/provenance/fail-closed tests
P9-06 all prior Yandex service regressions
P9-07 controlled browser gate with zero real Google/Yandex requests
P9-08 only then consider owner OAuth/live acceptance
```

No paid Google or third-party request is authorized by this research document.

## 10. Verdict

```text
PHASE9_GOOGLE_PROVIDER_RESEARCH_PASS
OFFICIAL_FIRST_PARTY_PROVIDER = GOOGLE_SEARCH_CONSOLE_API
EXTERNAL_SERP_PROVIDER = UNFROZEN
TECHNICAL_EXTERNAL_SERP_FRONT_RUNNER = DATAFORSEO
SELF_HOSTED_GOOGLE_SCRAPING = REJECTED
CUSTOM_SEARCH_JSON_API = REJECTED
GOOGLE_GROUNDING_AS_ORGANIC_RANK = REJECTED
NEXT = ARCHITECTURE_GATE_FOR_GOOGLE_SEARCH_CONSOLE
```
