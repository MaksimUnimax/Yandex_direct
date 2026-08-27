# Freelance order capability matrix

Status: active product-discovery / workflow-design authority.
Started: 2026-08-27.

Purpose: derive future Yandex Marketing Bridge/product workflow from real freelance marketplace orders instead of inventing capabilities in isolation.

For every order card record:

```text
case id
marketplace / order type
required client inputs
required deliverable
current verdict = YES / PARTIAL / NO
what current Bridge can already do
what is missing in Bridge
what is missing outside Bridge
proposed concrete execution workflow
commercial/operational constraints
product priority
```

This document is planning/evidence only. It does not authorize product-byte changes by itself.

---

## F-001 — Rank tracking in Yandex and Google, up to 500 keywords

Source: Kwork card supplied by owner on 2026-08-27.

Service promise:

```text
input:
- client site URL/domain
- target region
- up to 500 keyword queries

measurement:
- Yandex organic position, depth up to 100
- Google organic position, depth up to 50

output:
- Excel summary
```

Owner supplied two example deliverables:

```text
pankovshop_ru - Сводка.xlsx
drovosekk.ru- Сводка.xlsx
```

Observed deliverable shape is simple and reproducible:

```text
sheet: Сводка
header: date/month + region
columns: search phrase + Google position + Yandex position
rank: integer when domain is found
not found within configured depth: "-"
```

The examples contain no complex formulas; the hard part of the order is reliable bulk SERP acquisition and rank extraction, not spreadsheet formatting.

### Current verdict

```text
PARTIAL
```

The exact advertised Kwork service cannot yet be sold as a fully automated Bridge workflow.

### What current Bridge can already do

Yandex Search first slice already supports synchronous organic SERP collection through official Yandex Search API:

```text
protocol = SEARCH_API_V1
method = search
provider = POST /v2/web/search
response = normalized organic results
region = supported for SEARCH_TYPE_RU
groupsOnPage = 1..100
normalized document includes rank, url and domain
```

Therefore one bounded Yandex request can request enough organic results to determine a domain position within the required top-100 depth for one keyword.

The Bridge/ChatGPT workflow can also construct the final XLSX once normalized per-keyword ranks exist.

### What is missing in Bridge

#### 1. Bulk rank-check orchestration

Current Search command is one query per command. There is no dedicated job operation such as:

```text
rankCheck(domain, region, keywords[], yandexDepth, googleDepth)
```

For a commercial 500-keyword order we need a durable batch workflow that:

- accepts/preserves the client's keyword list;
- normalizes the target domain (www/non-www, scheme, trailing slash, subdomain policy);
- executes one logical rank check per keyword/engine;
- matches returned result domains against the target domain;
- records first organic rank or `-`;
- checkpoints completed keywords;
- resumes safely after browser/session interruption without re-running completed provider requests blindly;
- enforces provider request rate/cost budgets;
- reports progress;
- produces a deterministic final table in original client order.

#### 2. Efficient high-volume Yandex path

The accepted Phase-2 Search slice is synchronous only. The project requirement snapshot records synchronous Search as a paid per-request path and explicitly defers `/v2/web/searchAsync`.

For up to 500 keywords, synchronous Search is technically possible but is not yet the preferred commercial execution path. A future bulk-ranking phase should research/implement Yandex deferred Search because it is designed for higher-volume work and has materially lower per-request pricing in the current project tariff snapshot.

Any async implementation requires its own durable operation/polling lifecycle and must preserve exactly-once/no-blind-retry rules.

#### 3. Google organic SERP provider

There is currently no Google Search rank provider in Yandex Marketing Bridge.

The official Google Custom Search JSON API is not automatically equivalent to normal Google organic SERP measurement and returns at most 10 results per request, with a maximum accessible result index of 100. Therefore it must not be assumed to reproduce the advertised `Google position` column without a separate provider/product decision.

Needed new work:

```text
research Google rank-data provider options
→ verify geographic targeting, organic-result fidelity, depth >= 50, quotas and price
→ choose provider contract
→ add separate credential/service adapter or governed rank-provider layer
→ add controlled QA + owner-live acceptance
```

A third-party SERP API may be the correct solution, but no provider is selected by this case record yet.

#### 4. Rank-report artifact workflow

Need a reusable deliverable builder that creates an XLSX matching the simple market format:

```text
A: Поисковая фраза
B: Google
C: Yandex
header metadata: measurement date + region
integer rank / "-"
```

Optional internal evidence (not necessarily delivered to client) should preserve request timestamp, provider, region/location, depth and execution status so disputed rows can be traced.

### External/client inputs required

```text
required:
- target site URL/domain
- target region
- keyword list

for Google provider after implementation:
- exact country/location/language/device policy if required by provider
```

No Webmaster, Metrika or Direct credential from the client is inherently required for this rank-tracking service because positions are measured from SERP data, not private site/account analytics.

### Concrete execution workflow after missing capabilities are implemented

```text
1. Receive client domain, region and keyword file/list.
2. Validate keyword count <= purchased quantity.
3. Normalize domain and preserve original keyword order.
4. Resolve region to governed Yandex region ID and Google provider location.
5. Create durable rank-check job/checkpoint.
6. For each keyword:
   a. acquire Yandex organic SERP to depth 100;
   b. find first organic result matching target domain;
   c. save numeric rank or "-";
   d. acquire Google organic SERP to depth 50 through selected provider;
   e. find first matching target-domain result;
   f. save numeric rank or "-";
   g. persist checkpoint before advancing.
7. Validate that every input keyword has exactly one Yandex and one Google outcome.
8. Produce XLSX summary matching client-facing sample structure.
9. Run final completeness/duplicate/order checks.
10. Deliver XLSX to client.
```

### Commercial/operational conclusion

This is a valuable recurring freelance workflow because the deliverable is standardized and the client inputs are small. Once bulk orchestration plus a Google SERP provider exist, most of the work can be deterministic and automated.

Current state:

```text
Yandex single-key rank acquisition = YES
Yandex 500-key commercial batch workflow = NOT YET PRODUCTIZED
Google rank acquisition = NO PROVIDER
XLSX generation = YES
exact advertised service end-to-end = PARTIAL
```

### Product priority generated by this order

```text
candidate next-product capability:
BULK SERP / RANK TRACKER

priority: HIGH
reason:
- directly maps to a real paid freelance deliverable;
- repeatable across clients;
- requires little client-side access;
- reuses existing Yandex Search investment;
- creates reusable batch/checkpoint/output infrastructure for many future SEO orders.
```
