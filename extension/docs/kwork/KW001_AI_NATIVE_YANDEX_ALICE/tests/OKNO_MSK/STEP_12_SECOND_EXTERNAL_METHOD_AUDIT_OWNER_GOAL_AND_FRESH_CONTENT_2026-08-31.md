# Step 12 — second external method audit: owner goal + fresh existing-content check

Date: 2026-08-31  
Status: **EXTERNAL AUDIT / STEP 12 REOPENED / METHOD UPDATE REQUIRED BEFORE RECLOSE**

## Why this audit exists

The first external audit corrected major semantic and QA failures. A later owner challenge exposed another class of Step-12 error: the method could still produce a structurally/search-plausible recommendation that was wrong for the actual current site or wrong for the owner's desired commercial outcome.

The three concrete post-close findings are recorded in `STEP_12_POST_CLOSE_OWNER_CHALLENGE_2026-08-31.md` as D12-16..D12-18.

This second audit asks a narrower methodological question:

> What must Step 12 prove before recommending an existing page, a new page or informational content, when the website is a real business rather than an abstract semantic map?

## External sources reviewed

### Semrush — Keyword mapping for SEO, 2026-07-27
https://www.semrush.com/blog/keyword-mapping/

Material constraints:
- keyword maps become stale when pages are published, updated or removed;
- topic selection should reflect products/services, expertise, audience and business goals;
- clusters must be manually reviewed for common intent;
- before `To create`, check whether a suitable existing page already covers the topic and intent;
- open suggested existing URLs and confirm fit;
- optimize existing pages before investing in new content;
- new pages should fill real gaps and be prioritized by business relevance, search volume and realistic ranking difficulty.

### Semrush — Content audit, 2026-05-04
https://www.semrush.com/blog/content-audit/

Material constraints:
- an audit evaluates existing content against performance **and business goals**;
- the audit starts by defining the outcome to improve (traffic, conversions, AI visibility, etc.);
- existing content should be evaluated before creating more content.

### Semrush — Content marketing strategy, 2026-08-19
https://www.semrush.com/blog/content-marketing-strategy-guide/

Material constraints:
- every content decision should connect to a clear business goal;
- search demand should inform strategy, not dictate it;
- a topic should not automatically become an article merely because people search for it;
- content format/channel should be chosen based on the desired business outcome and audience journey.

### Ahrefs — Keyword strategy, updated 2026-03-13
https://ahrefs.com/blog/keyword-strategy/

Material constraints:
- SEO goal shapes the whole keyword strategy (rankings, traffic, revenue or authority lead to different priorities);
- each keyword/cluster should have a business-potential score;
- high-rankability/low-business-potential topics are only a `traffic play`, should not be overinvested in, and can attract the wrong audience;
- low-business-potential topics should be deprioritized unless there is an explicit strategic reason.

### Ahrefs — Keyword research / Business Potential
https://ahrefs.com/seo/keyword-research

Material constraints:
- traffic potential, difficulty and intent are not enough; the analyst must ask what ranking for the query is worth to the business;
- a topic can be related to the niche but still have near-zero business potential;
- prioritization must reflect the actual business context.

### Ahrefs — Product-led content
https://ahrefs.com/blog/product-led-content/

Material constraints:
- content should naturally connect the problem with the product/service where appropriate;
- prioritize topics where the product/service can genuinely help solve the problem;
- if existing high-value content already exists, update/rewrite it instead of creating unnecessary new content.

### Yandex Webmaster — low-value / low-demand pages
https://yandex.ru/support/webmaster/ru/site-indexing/low-demand

Material constraints:
- pages can be excluded when they duplicate known pages, contain insufficient value or fail to match real queries;
- similar pages can answer the same query and compete, with only the more relevant page retained;
- there is no arbitrary quota on useful pages, so the decision is about usefulness and distinct role, not page-count symmetry.

### Yandex Webmaster — site structure
https://yandex.ru/support/webmaster/ru/recommendations/site-structure

Material constraints:
- documents should belong to a clear logical section and be reachable by ordinary links;
- duplicate/technical pages waste crawl resources and provide no unique search value;
- navigation should help the user find the needed information quickly.

### Yandex Webmaster — duplicate pages
https://yandex.ru/support/webmaster/en/yandex-indexing/about-doubles

Material constraints:
- duplicate pages waste crawl resources;
- duplicate pages can compete in search;
- the crawler may retain the wrong duplicate instead of a strategically important landing page.

## Method finding 1 — `BUSINESS_TRUTH` is not the same as `OWNER_BUSINESS_GOAL`

The current reusable Step-12 method asks whether the target business can truthfully fulfil the product/service/content promise. That is necessary but insufficient.

Example failure: a professional installation company can truthfully publish a step-by-step self-installation guide. But if the owner's goal is qualified leads for installation, the guide may reduce the need for the paid service or attract a low-value audience. Search demand alone does not resolve this conflict.

The missing dimensions are:

```text
OWNER_PRIMARY_GOAL
DESIRED_USER_OUTCOME
BUSINESS_POTENTIAL
CONTENT_ROLE_IN_FUNNEL
COUNTERPRODUCTIVE_TO_CORE_OFFER?
```

Suggested states:

```text
OWNER_PRIMARY_GOAL = REVENUE | LEADS | AUTHORITY | TRAFFIC | SUPPORT_RETENTION | MIXED
CONTENT_ROLE = SELL | ASSIST_DECISION | EDUCATE_TO_CONVERT | SELF_SERVICE | AUTHORITY | TRAFFIC_PLAY | DEPRIORITIZE
BUSINESS_POTENTIAL = HIGH | MEDIUM | LOW | NEGATIVE_OR_COUNTERPRODUCTIVE | OWNER_POLICY_REQUIRED
```

Reason: Ahrefs and Semrush both explicitly make business goal/business potential part of keyword/content strategy. A high-demand query is not automatically a high-value structural opportunity.

Hard rule proposed:

```text
SEARCH_DEMAND != BUSINESS_VALUE
BUSINESS_TRUTH != BUSINESS_GOAL_ALIGNMENT
USER_WANTS_INFORMATION != OWNER_SHOULD_PUBLISH_NEUTRAL_ENABLEMENT
```

If the owner goal is unknown and it materially changes the structural action, Step 12 should defer rather than invent the business objective.

## Method finding 2 — a new-page candidate requires a fresh current-site existence check immediately before CREATE

The accepted Step-01 inventory is valuable evidence but not a timeless proof of absence. Semrush explicitly notes that page maps become stale as pages change and instructs analysts to check/open existing URLs before deciding `To create`.

D12-16 proved the failure concretely: Step 12 proposed `/panoramnye-okna/`, while a full current commercial landing already existed at `/okna-rehau/panoramnoe-osteklenie/`.

New mandatory sequence proposed:

```text
NEW_PAGE_CANDIDATE
→ FRESH CURRENT-SITE EXISTENCE CHECK
   - current navigation / internal links
   - current URL inventory / sitemap for discovery when useful
   - first-party site search / web discovery
   - synonyms, alternative slugs and neighboring page families
→ OPEN + READ EVERY PLAUSIBLE EXISTING PAGE
→ EXISTING-CONTENT GAP / OVERLAP AUDIT
→ ONLY THEN MAY CREATE REMAIN
```

Hard rules proposed:

```text
NOT_IN_OLD_INVENTORY != CURRENT_PAGE_ABSENT
NO_STEP11_OWNER != CURRENT_PAGE_DOES_NOT_EXIST
CREATE_WITHOUT_FRESH_EXISTING_PAGE_RECHECK = FAIL
```

Reason: the cost of a false CREATE recommendation is high: it can duplicate an existing landing page and create the exact search ambiguity that later steps are supposed to prevent.

## Method finding 3 — new informational pages require an existing-content reuse audit, not just a page-ownership gap

D12-18 exposed a separate issue. The proposed broad DIY repair/adjustment guide overlapped existing self-help content such as adjustment and seasonal-mode articles. A page gap at the structural-unit level does not prove a content gap on the current site.

Mandatory sequence proposed:

```text
NEW_INFORMATIONAL_PAGE_CANDIDATE
→ CURRENT CONTENT AUDIT
→ WHAT IS ALREADY COVERED?
→ CAN THE EXISTING ARTICLE/HUB BE EXPANDED OR REFRAMED?
→ IS THE REMAINING TASK DISTINCT ENOUGH FOR A NEW URL?
→ DOES THE NEW URL SUPPORT THE OWNER'S GOAL?
→ ONLY THEN CREATE
```

Hard rule proposed:

```text
PAGE_OWNERSHIP_GAP != CONTENT_GAP
NEW_INFORMATIONAL_PAGE != DEFAULT_FOR_INFORMATIONAL_INTENT
EXISTING_CONTENT_PARTIALLY_COVERS_TASK -> AUDIT_REUSE_BEFORE_CREATE
```

Reason: Semrush's keyword-mapping and content-audit guidance explicitly prioritize checking/optimizing existing content before creating additional pages; Yandex warns about similar/duplicate pages.

## What the previous Step-12 method still did well

The second audit does **not** invalidate the earlier improvements. External sources continue to support:
- phrase/task coherence before page decisions;
- demand from actual frequency rather than phrase count;
- current-page fit and open/read verification;
- explicit hierarchy and internal linking;
- avoiding page inflation;
- distinguishing target URL from currently relevant/ranking URL;
- separating candidate overlap from actual cannibalization diagnosis;
- evidence-derived confidence/maturity;
- independent QA rather than self-certification;
- durable persistence/readback.

The remaining issue is that the method was still too SEO-centric at the exact moment when a search opportunity must be converted into a business recommendation.

## Reassessment of the five previously proposed page concepts

### Panoramic windows

Previous action: CREATE `/panoramnye-okna/`.

Second-audit verdict: **withdraw CREATE** because a current commercial page already exists. Re-evaluate the existing `/okna-rehau/panoramnoe-osteklenie/` page for KEEP/EXPAND and later inspect its overlap with object/subtype panoramic pages.

### DIY installation

Previous action: CREATE a step-by-step self-installation article.

Second-audit verdict: **withdraw current neutral enabling concept**. The site's commercial positioning explicitly sells professional installation and discourages self-installation. Re-evaluate whether search demand should be handled by the existing service page or a business-aligned risk/requirements article. Owner goal must be explicit.

### DIY repair + adjustment

Previous action: CREATE one broad DIY repair/adjustment page.

Second-audit verdict: **withdraw current broad CREATE**. Existing DIY adjustment content already covers part of the need, while professional repair is a paid service. Re-audit for existing-content expansion/consolidation and a clear `safe self-help -> professional handoff` boundary.

### Window hardware guide

Second-audit verdict: remains **provisional**, not yet disproved. Must pass a fresh existing-content audit and explicit owner-goal/business-potential test before CREATE can be accepted.

### Window replacement service

Second-audit verdict: commercially aligned and therefore a stronger candidate, but still must pass the same fresh exact existing-page check and an `expand installation page vs separate replacement page` comparison before CREATE can be accepted.

## Revised Step-12 reasoning order proposed

```text
1. DEFINE OWNER BUSINESS GOAL / DESIRED USER OUTCOME
2. LOAD COMPLETE PHRASE-LEVEL INPUT
3. BUILD / VERIFY COHERENT USER-TASK STRUCTURAL UNITS
4. FRESHLY DISCOVER CURRENT SITE / CONTENT BEFORE STRUCTURAL CREATE DECISIONS
5. OPEN + READ CURRENT CANDIDATE PAGES
6. SCORE BUSINESS TRUTH + BUSINESS POTENTIAL + CONTENT ROLE
7. JOIN REAL DEMAND EVIDENCE (phrase count is accounting only)
8. USE SEARCH/SERP EVIDENCE WHEN PAGE BOUNDARY IS MATERIAL
9. TEST EXISTING PAGE: KEEP / EXPAND / SECTION / ROUTE
10. FOR INFO CONTENT, RUN EXISTING-CONTENT REUSE AUDIT
11. ONLY IF A REAL GAP REMAINS, EVALUATE NEW PAGE
12. NEW PAGE MUST PASS DISTINCT TASK + DEMAND + BUSINESS VALUE + TRUTHFUL EXPERTISE/OFFER + NO CURRENT EQUIVALENT + CORRECT CONTENT TYPE + HIERARCHY
13. MARK FINAL / PROVISIONAL / DEFERRED MATURITY
14. DERIVE COMPLETE STEP-13 CANDIDATE PAIR UNIVERSE
15. RUN INDEPENDENT QA + MANUAL OWNER-CHALLENGE CASES
16. SAVE TO GITHUB + STRUCTURED READBACK
17. GIVE A LAYMAN SUMMARY
18. ONLY THEN ALLOW STEP 13
```

The ordering matters. If business goal is introduced only after page ideas are generated, the process can spend effort proving an SEO opportunity that the owner should never implement. If fresh current-site discovery happens only at Step 1, a later CREATE recommendation can be based on stale absence evidence.

## Current job consequence

The current OKNO-MSK Step 12 is already reopened with D12-16..D12-18 and Step 13 blocked. Do not restore `STEP12_COMPLETE` until these three defects are corrected, the reusable method is updated, all five new-page concepts are re-evaluated under the new gates, and independent QA is rerun.
