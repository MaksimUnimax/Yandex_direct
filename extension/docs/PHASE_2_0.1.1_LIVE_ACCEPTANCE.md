# Phase 2 Search — 0.1.1 owner live acceptance

Date: 2026-08-24  
Status: **AUTHORIZED / ONE MINIMAL REAL SYNCHRONOUS SEARCH REQUIRED**

## Exact accepted controlled-gate candidate

```text
source commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
artifact: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
bytes: 170734
files: 65
ZIP entries: 68
```

The complete Codex controlled pre-delivery campaign passed on these exact bytes:

```text
PD-00..PD-17: ALL PASS
Manual-ON transaction: PASS
S-00..S-17: ALL PASS
source: 231/231 PASS
packaged: 231/231 PASS
browser B-01/B-02/B-03: PASS
not_run_enabled_sections: 0
real Yandex requests during controlled gate: 0
verdict: PASS
```

Evidence checkpoint:

```text
extension/tests/PHASE_2_STAGE_4_CODEX_FULL_GATE_PASS_2026-08-24.md
```

## Fresh official pricing check

Checked immediately after complete Codex PASS on 2026-08-24 against the current official Yandex Search API pricing page:

```text
https://aistudio.yandex.ru/docs/ru/search-api/pricing.html
```

Current RUB prices, VAT included:

```text
daytime synchronous: 488 RUB / 1000 = 0.488 RUB/request
night synchronous:   366 RUB / 1000 = 0.366 RUB/request
night window:         00:00:00–07:59:59 UTC+3
```

The owner-live command prepared at this checkpoint falls in the daytime tariff class. Expected tariff reservation for exactly one accepted synchronous Search initiation:

```text
0.488 RUB
```

A provider-side internal server error or authentication error is documented as non-billable, but the Bridge must still report request initiation truthfully. Do not infer charge/no-charge from HTTP status beyond official billing rules.

## Owner-live scope

Do not repeat controlled browser/UI regression as a manual checklist. The owner performs only the irreducible real-profile/provider boundary:

1. exact `d58b5bd...` candidate is loaded in the owner's real Chrome profile;
2. the bound conversation uses Search as active service with Search Manual allowed;
3. valid local Yandex Search API credential/folder settings are present;
4. execute exactly one real synchronous Search command through the external `Яндекс` Manual action;
5. do not click twice and do not blind-retry an ambiguous provider outcome;
6. inspect the returned `SEARCH_RESULT_V1` for provider truth and usable normalized results.

## Exact first live command

Use exactly one block:

```text
SEARCH_API_V1
{
  "method": "search",
  "queryText": "купить ноутбук",
  "searchType": "SEARCH_TYPE_RU",
  "region": "225",
  "page": 0,
  "groupsOnPage": 5,
  "familyMode": "FAMILY_MODE_MODERATE",
  "fixTypoMode": "FIX_TYPO_MODE_ON",
  "sortMode": "SORT_MODE_BY_RELEVANCE",
  "sortOrder": "SORT_ORDER_DESC",
  "groupMode": "GROUP_MODE_FLAT",
  "docsInGroup": 1,
  "maxPassages": 2,
  "l10n": "LOCALIZATION_RU"
}
```

Expected external provider initiations for this acceptance:

```text
exactly 1 if locally admitted
```

Expected conservative cost reservation:

```text
0.488 RUB
```

## PASS criteria

Owner-live Phase 2 passes when the single command returns one truthful Bridge report with:

```text
signature: SEARCH_RESULT_V1
service: search
operation: search
status: OK
http_status: 200
request_executed: true
automatic_retry: false
response_format: FORMAT_XML
result.results: non-empty usable normalized result list
```

For returned documents, `url` is the essential identity; optional fields such as title/snippet/domain/modtime may legitimately be null according to the product contract and provider variability.

No duplicate report/provider initiation may appear from the one click.

## Controlled non-PASS outcomes

The following do not authorize a blind second click:

```text
request_executed: "UNKNOWN"
timeout/session loss after possible initiation
ambiguous delivery after irreversible provider boundary
```

Return that exact evidence to ChatGPT for reconciliation.

A clear pre-network rejection such as missing Search credentials/access/policy returns `request_executed:false` and is not evidence that Search provider execution was tested. ChatGPT must classify whether it is operator configuration/access or product behavior before any further live attempt.

A clear HTTP/provider error after one request returns `request_executed:true`, `automatic_retry:false`; return the report to ChatGPT and do not repeat automatically.

## Closure rule

```text
owner-live PASS
→ record exact report evidence
→ Phase 2 Search first slice = LIVE PASS / CLOSED
→ only then may Phase 3 Webmaster unlock
```

If owner-live proves a real product defect, Phase 2 reopens at the proven layer; any production or packaged-test byte change requires a new candidate and complete controlled gate.
