# Phase 2 Search — 0.1.1 owner live acceptance

Date: 2026-08-25  
Status: **AUTHORIZED / ONE MINIMAL REAL SYNCHRONOUS SEARCH REQUIRED**

## Exact accepted controlled-gate candidate

```text
source commit: f4aee34c0a3455aa7199f6aa54bd581c71d97337
artifact: yandex-marketing-bridge-0.1.1-phase2-search-context-recovery-candidate.zip
SHA-256: 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46
bytes: 175971
files: 68
ZIP entries: 71
payload manifest SHA-256: bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478
payload manifest bytes: 11933
Windows-safe transport commit: 7c787eedd9856c3f91fbed85aeaea7f3405ad473
```

The complete controlled pre-delivery campaign passed on these exact bytes:

```text
run: 32801788251
job: 97663951211
Windows Server 2025
Chrome for Testing: 151.0.7922.47
source: 239/239 PASS
packaged: 239/239 PASS
packaged syntax: 62/62 PASS
packaged JSON: 2/2 PASS
browser B-01 Project/Work: PASS
browser B-02 mandatory Manual-ON: PASS
browser B-03 Search Autorun: PASS
browser B-04 native Chrome-151 popup geometry: PASS
browser B-05 already-open-ChatGPT context recovery: PASS
PD-00..PD-17: ALL PASS
mandatory Manual-ON transaction: PASS
S-00..S-17: ALL PASS
controlled Search stub requests: 1
not_run_enabled_sections: 0
real Yandex requests during controlled gate: 0
real credentials used: NO
final exactness: PASS
final cleanliness: PASS
verdict: PASS
```

Evidence checkpoints:

```text
extension/tests/PHASE_2_CONTEXT_RECOVERY_FREEZE_PASS_2026-08-25.md
extension/tests/PHASE_2_CONTEXT_RECOVERY_WINDOWS_TRANSPORT_PASS_2026-08-25.md
extension/tests/PHASE_2_CONTEXT_RECOVERY_COMPLETE_GATE_PASS_2026-08-25.md
```

Older `d58b5bd...` and `0186b35d...` artifacts are historical only and must not be used for this acceptance.

## Fresh official pricing check

Rechecked on 2026-08-25 against the current official Yandex Search API pricing page:

```text
https://aistudio.yandex.ru/docs/ru/search-api/pricing.html
```

Current RUB prices, VAT included:

```text
daytime synchronous: 488 RUB / 1000 = 0.488 RUB/request
night synchronous:   366 RUB / 1000 = 0.366 RUB/request
night window:         00:00:00–07:59:59 UTC+3
```

At the latest pre-handoff check (about 05:39 UTC+3 on 2026-08-25), the request was in the night tariff window, so the expected price for one accepted synchronous initiation at that moment was:

```text
0.366 RUB
```

If the owner executes at or after 08:00:00 UTC+3, re-check the tariff classification immediately before the click; the daytime price under the current published tariff is 0.488 RUB/request.

A provider-side internal server error or authentication error is documented as non-billable, but the Bridge must still report request initiation truthfully. Do not infer charge/no-charge from HTTP status beyond official billing rules.

## Owner-live scope

Do not repeat controlled browser/UI regression as a manual checklist. The owner performs only the irreducible real-profile/provider boundary:

1. load the exact `739dd5d7...` candidate in the owner's real Chrome profile;
2. open or keep open the target ChatGPT conversation — the already-open-tab recovery path has been controlled-tested and no page reload should be required merely because the extension was loaded;
3. bind the target conversation if it is not already bound;
4. select Search as active service, enable Search Manual permission, and enable conversation Manual mode;
5. valid local Yandex Search API credential/folder settings must be present;
6. execute exactly one real synchronous Search command through the external `Яндекс` Manual action;
7. do not click twice and do not blind-retry an ambiguous provider outcome;
8. inspect the returned `SEARCH_RESULT_V1` for provider truth and usable normalized results.

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

Expected request price is determined by the official tariff window at the actual click time. At the latest 05:39 UTC+3 pre-handoff check it was 0.366 RUB; at/after 08:00 UTC+3 under the currently published tariff it is 0.488 RUB.

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
