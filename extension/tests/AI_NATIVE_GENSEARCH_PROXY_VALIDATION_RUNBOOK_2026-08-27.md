# AI-native — bounded GenSearch vs canonical consumer-Alice proxy validation

Date: 2026-08-27

Status: **READY FOR OWNER-LIVE BOUNDED VALIDATION / NO PRODUCT SOURCE CHANGE**

## Authority

```text
repository = MaksimUnimax/Yandex_direct
branch = ai-native/gensearch-proxy-validation-2026-08-27
baseline_main = ca422ac5b1635bb42984d6076f3143780e1d72f6
methodology_verdict = AI_NATIVE_COMPARATIVE_GATE_PASS
canonical_consumer_alice_source_commit = 0da1fdfa65155fe0b22d67838d366e7d214ccbbe
```

Canonical methodology comparison:

`extension/tests/AI_NATIVE_BLOOD_SAND_COMPARISON_2026-08-27.md`

Provider research:

`extension/docs/AI_NATIVE_YANDEX_GENSEARCH_PROVIDER_RESEARCH_2026-08-27.md`

## Why this is a validation-only probe

Do not alter or freeze the production Bridge GenSearch protocol before this comparison establishes what GenSearch means for the product.

The current extension already has:

- Search/Yandex Cloud credential stored locally under the `search` service record;
- host permission for `https://searchapi.api.cloud.yandex.net/*`;
- a service worker extension context capable of direct `fetch` to the provider;
- explicit fail-closed/no-auto-retry discipline for paid Search requests.

Therefore this one-time proxy test uses a DevTools service-worker console probe and changes **zero** `extension/src` bytes.

The probe prefix below is evidence-only and is **not a production protocol contract**:

```text
GEN_SEARCH_PROXY_RESULT_V1
```

## Official request shape used

Endpoint:

```text
POST https://searchapi.api.cloud.yandex.net/v2/gen/search
```

Body for each isolated root:

```json
{
  "messages": [
    {
      "content": "<ROOT>",
      "role": "ROLE_USER"
    }
  ],
  "folderId": "<stored Search folder ID>",
  "searchType": "SEARCH_TYPE_RU",
  "fixMisspell": true,
  "getPartialResults": false,
  "enableRichStructuredAnswer": true
}
```

No previous-turn message is supplied. Every root is a fresh single-message request so conversational contamination cannot carry between roots.

## Fixed representative set

Execute in this order, one result inspected before the next request:

```text
G01 = печать велеса
G02 = оберег в машину
G03 = вегвизир
G04 = алатырь оберег
G05 = подарок мужчине в машину
```

Purpose:

- G01 — transactional ordinary Search vs meaning/history/use-first consumer Alice;
- G02 — hybrid choice/use-case + shopping;
- G03 — provenance-sensitive history/meaning/correction;
- G04 — commercial Search vs mythology/meaning/suitability consumer Alice;
- G05 — clean contamination-control comparator.

At the recorded pricing snapshot (~5.08 RUB/request), maximum planned provider cost for all five successful explicit calls is approximately 25.40 RUB.

## Hard safety rules

1. One console invocation = at most one GenSearch request.
2. No loop, retry, recursion, timer or batch execution is allowed.
3. Never print or copy `api_key` or `folder_id`.
4. HTTP response, including HTTP error, is a known outcome and may be recorded.
5. A thrown `fetch` / network exception is `OUTCOME_UNKNOWN`; **do not repeat that root** until explicitly reconciled.
6. Do not proceed to the next root until the previous result has been inspected and recorded.
7. `searchQueries[]` provenance is `GEN_SEARCH_QUERY_OBSERVED`, never `ALICE_FANOUT_OBSERVED`.
8. No claim of consumer-Alice equivalence is permitted from this test.

## Validation-only one-request probe

Change only the `QUERY` literal for the currently authorized root. Do not edit any other line.

```js
(async () => {
  "use strict";

  const QUERY = "печать велеса";
  const ENDPOINT = "https://searchapi.api.cloud.yandex.net/v2/gen/search";
  const startedAt = new Date().toISOString();
  const startedMs = performance.now();

  const stored = await chrome.storage.local.get("ymb_service_credentials");
  const searchCredential = stored?.ymb_service_credentials?.search || {};
  const apiKey = String(searchCredential.api_key || "").trim();
  const folderId = String(searchCredential.folder_id || "").trim();

  if (!apiKey || !folderId) {
    console.log("GEN_SEARCH_PROXY_RESULT_V1\n" + JSON.stringify({
      validation_only: true,
      query: QUERY,
      status: "ERROR",
      reason: !apiKey ? "SEARCH_API_KEY_MISSING" : "SEARCH_FOLDER_ID_MISSING",
      request_executed: false,
      automatic_retry: false,
      started_at: startedAt
    }, null, 2));
    return;
  }

  const body = {
    messages: [{ content: QUERY, role: "ROLE_USER" }],
    folderId,
    searchType: "SEARCH_TYPE_RU",
    fixMisspell: true,
    getPartialResults: false,
    enableRichStructuredAnswer: true
  };

  let response;
  try {
    response = await fetch(ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Api-Key ${apiKey}`
      },
      body: JSON.stringify(body)
    });
  } catch (error) {
    console.log("GEN_SEARCH_PROXY_RESULT_V1\n" + JSON.stringify({
      validation_only: true,
      query: QUERY,
      status: "OUTCOME_UNKNOWN",
      reason: "NETWORK_OUTCOME_UNKNOWN_NO_RETRY",
      request_executed: "UNKNOWN",
      automatic_retry: false,
      started_at: startedAt,
      elapsed_ms: Math.max(0, Math.round(performance.now() - startedMs)),
      error_name: String(error?.name || "Error"),
      error_message: String(error?.message || error || "network error").slice(0, 500)
    }, null, 2));
    return;
  }

  const rawText = await response.text();
  let parsed = null;
  try { parsed = JSON.parse(rawText); } catch {}

  const providerResult = parsed ?? { non_json_body: rawText.slice(0, 4000) };
  console.log("GEN_SEARCH_PROXY_RESULT_V1\n" + JSON.stringify({
    validation_only: true,
    query: QUERY,
    status: response.ok ? "OK" : "ERROR",
    reason: response.ok ? null : String(parsed?.code || parsed?.error?.code || parsed?.message || `HTTP_${response.status}`).slice(0, 300),
    http_status: response.status,
    request_executed: true,
    automatic_retry: false,
    started_at: startedAt,
    elapsed_ms: Math.max(0, Math.round(performance.now() - startedMs)),
    provider_result: providerResult
  }, null, 2));
})();
```

The output contains no credential values unless the provider itself unexpectedly echoes them. Before copying a result out of DevTools, visually verify there is no API key, Authorization header, or secret material in the output. Normal GenSearch response fields should contain answer/source/query evidence only.

## Per-root comparison record

For each G01–G05 record:

```text
query
provider_request_executed
HTTP/status
GenSearch answer job
GenSearch answer summary
GenSearch sources[] domains/types
GenSearch sources[].used
GenSearch searchQueries[] themes
canonical consumer-Alice job
canonical consumer-Alice source themes/domains
canonical consumer-Alice observed fan-out where present
alignment classification
material page-job implication same/different
notes / limitations
```

Classification must be one of:

```text
SAME_OR_STRONGLY_ALIGNED
PARTIALLY_ALIGNED
MATERIALLY_DIFFERENT
NOT_COMPARABLE
```

## Acceptance logic

GenSearch may be promoted to a repeatable structured AI-search hand if the five-root bounded set has no unexplained systematic recommendation-level contradiction and the structured evidence is sufficient for audit.

Partial alignment is allowed if provenance remains explicit. Exact wording/source equality is not required.

If several roots are materially different in ways that would change semantic/page recommendations, do not call GenSearch a consumer-Alice proxy. Keep it as a separate AI-search evidence surface and revise the product contract before implementation.

## Durable outputs after execution

Planned evidence file:

`extension/tests/AI_NATIVE_GENSEARCH_PROXY_VALIDATION_RESULTS_2026-08-27.md`

Final output must state:

```text
provider_requests_planned = 5
provider_requests_executed = <actual>
unknown_outcomes = <actual>
proxy_verdict = <verdict>
production_protocol_authorized = true|false
```

No production source change is authorized merely by creating this runbook.
