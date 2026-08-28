# Phase 9 — Google Search Console P9-05 controlled browser acceptance

Date: 2026-08-28
Status: **PASS / P9-05 CLOSED**

## Authority

```text
BRANCH = phase9/google-organic-provider-research-2026-08-28
TESTED_HEAD = 99aa6992a66fdf4e5995ceb9f59927dbc80ea58d
WORKFLOW = phase9-gsc-dev
RUN_ID = 33160562219
RUN_ATTEMPT = 1
RUN_CONCLUSION = success
PURE_JOB_ID = 98813735198
CONTROLLED_BROWSER_JOB_ID = 98813735491
REAL_GOOGLE_REQUESTS = 0
REAL_YANDEX_REQUESTS = 0
```

The workflow ran on the exact tested head and completed successfully. Both `pure-contract` and `controlled-browser` jobs reached terminal `success`.

## P9-05 source boundary

The accepted P9-05 worker overlay is loaded by `extension/src/phase3_service_worker_bootstrap.js` after the accepted Webmaster worker overlay and before Search Batch:

```text
shared/google_search_console_protocol.js
shared/google_search_console_runtime.js
google_search_console_worker_runtime.js
```

This preserves prior service routing while adding the explicit sixth service `google_search_console`.

## Node / worker gate

The successful pure job covered:

```text
PHASE9_GSC_PURE_SYNTAX_PASS
PHASE9_GSC_PURE_CONTRACT_PASS
PHASE9_GSC_INJECTED_RUNTIME_PASS
PHASE9_GSC_WORKER_ROUTING_PASS
PHASE9_GSC_PRIOR_SERVICE_REGRESSION_PASS
PHASE9_GSC_COMPLETE_NODE_REGRESSION_PASS
PHASE9_GSC_REAL_GOOGLE_REQUESTS=0
PHASE9_GSC_REAL_YANDEX_REQUESTS=0
```

The complete Node regression suite passed on the same tested head.

## Controlled installed-extension proof

`extension/tests/qa_browser/google_search_console_browser_runtime.mjs` copied the production extension source to an isolated temporary QA directory, added only a temporary QA public key to that copy, loaded the copy as a real MV3 Chrome extension through Puppeteer, attached to the real extension service worker, and exercised GSC only through explicit injected test adapters.

The browser gate required and observed:

```text
P9_GSC_BROWSER_BOOTSTRAP_ROUTE_PASS
P9_GSC_BROWSER_LIST_SITES_ONE_REQUEST_PASS
P9_GSC_BROWSER_SEARCH_ANALYTICS_ONE_REQUEST_PASS
P9_GSC_BROWSER_AUTORUN_NO_REQUEST_PASS
P9_GSC_BROWSER_TOKEN_REDACTION_PASS
P9_GSC_BROWSER_REAL_GOOGLE_REQUESTS=0
P9_GSC_BROWSER_REAL_YANDEX_REQUESTS=0
PHASE9_GSC_CONTROLLED_BROWSER_PASS
PHASE9_GSC_CONTROLLED_BROWSER_GATE_PASS
PHASE9_GSC_POST_BROWSER_PRODUCT_IDENTICAL
```

### Controlled `listSites`

The installed worker route executed exactly one injected business request:

```text
service = google_search_console
method = listSites
identity interactive = false
provider request count = 1
method = GET
url = https://www.googleapis.com/webmasters/v3/sites
request_executed = true
automatic_retry = false
```

The controlled provider response was normalized to `site_url` plus `permission_level` provenance and the injected bearer token was absent from the report.

### Controlled `searchAnalytics`

The installed worker route executed exactly one additional injected business request:

```text
service = google_search_console
method = searchAnalytics
identity interactive = false
provider request count for command = 1
method = POST
siteUrl = sc-domain:example.com
startDate = 2026-08-01
endDate = 2026-08-07
dimensions = query,page
rowLimit = 25
request_executed = true
automatic_retry = false
```

The controlled response preserved `clicks`, `impressions`, `ctr`, `average_position`, and `position_semantics = average_topmost_position_over_impressions`.

### Autorun / token safety

With default GSC policy, an Autorun `listSites` attempt was rejected as `AUTORUN_DISABLED` before identity acquisition and before fetch. The controlled bearer token was absent from report text, browser test logs, and `chrome.storage.local`.

## Product immutability

The browser workflow hashed every file under `extension/src` before and after the browser run and required byte-identical output. The post-browser identity step passed.

The temporary QA manifest key was never written into production source.

## P9-06 boundary remains closed

P9-05 does **not** authorize production OAuth manifest wiring.

The production manifest on the tested head still intentionally has no:

```text
identity permission
https://www.googleapis.com/* host permission
oauth2 block
manifest key
```

The Phase-9 architecture gate requires the existing installed/release extension identity to be resolved before any permanent `key` is introduced, because inventing a new identity for an already-used extension can orphan extension-local storage and bindings.

Therefore the next governed step is P9-06 identity/OAuth setup using the existing installed/release extension ID, followed by test-first manifest/UI authorization wiring. No live Google provider request is authorized by this evidence.

## Verdict

```text
PHASE9_GSC_P9_05 = PASS / CLOSED
P9_06_PRODUCTION_OAUTH = NOT YET AUTHORIZED
REAL_GOOGLE_REQUESTS = 0
REAL_YANDEX_REQUESTS = 0
```
