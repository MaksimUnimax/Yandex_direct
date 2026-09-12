# B4A — guarded deferred Search XML normalization

2026-09-12. Continues WIP HEAD `7000398d82ffddf4ff0b91d68d4ca9d6229ba2c3`. NO RELEASE / no installable artifact.

## Exact inputs and saved outputs

Owner 0.1.4 ZIP rechecked locally: `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f` (53 files). Existing B3 runtime read at the exact remote commit. Patch A and B1/B2/B3 source not rewritten. Old normalizer is reused unchanged: `shared/search_xml.js` SHA-256 `790d14469db165795c84c34a6b6e8bf68a259e477d01fb648ff3101244cecffd`.

New `candidate/shared/search_async_normalizer.js` SHA-256 `7c4fda899456696b1bbcb8ce096def228eded161f5a1f457edc2aaaf129f3415`.
Test `qa/b4_normalizer.test.mjs` SHA-256 `8e9365938f88cc2a58abc9a07045fb017192a036a51a0af5c89acf22550a05f9`.

The guard runs before the existing XML-to-result mapper. It validates Base64/padding, UTF-8, local byte/character/depth/node budgets and a documented unnamespaced XML 1.0 envelope. It is deliberately NOT advertised as a full generic XML implementation. DTDs, namespaces, unsupported declarations and quoted literal greater-than attributes fail closed; raw data stays in B3 storage for later inspection instead of re-purchasing Search. The literal greater-than attribute restriction protects the unchanged legacy tokenizer.

Documented XML error 15 is an empty-result observation. Other error codes, contradictory empty evidence, unexpected/missing response and truncated XML cannot become successful empty search. Optional missing URL/title/domain remain null without invented replacements. Missing/unsafe URL ranks are retained and mark results unusable for URL comparison. Existing rank/title/snippet/modtime projection is byte-semantics compatible on tested valid fixtures; its existing snippet limit is unchanged. No raw XML is returned inside normalized data.

## Actual checks executed

Node v22.16.0; real baseline mapper + new guard, no mocked parser. Syntax PASS. First 58 checks PASS. Two further adversarial assertions initially FAIL: quoted `>` in attribute reached the permissive legacy mapper; error 15 with positive found total was accepted as empty. Both corrections added before publishing. Same complete 60-case suite rerun: 60 PASS, 0 FAIL, 0 skipped, exit 0 (146.528 ms TAP total). These are new-module RED/GREEN cases, not claimed reproductions of the owner's Chrome memory incident.

Run in QA subtree with exact baseline at `baseline/shared/search_xml.js`:

`node --test qa/b4_normalizer.test.mjs`

Tests cover fixed baseline identity, full 300-row accounting, Unicode/entities/CDATAs, missing optional fields, unsafe URL preservation, provider error classification, zero/contradictory results, malformed envelopes/tags/attributes/entities, depth/node/byte guards, noncanonical Base64, invalid UTF-8, BOM and unsupported encodings. Original production manifest, ordinary Search, GenSearch and credentials have not been modified.

## Dependency / resource boundaries

Changed path: new guard -> existing XML mapper -> B3 normalizeRaw injection. Existing mapper exact hashes unchanged; projection parity tested. B3 runtime has not yet been bound to this guard in an installed extension. Full integration, browser memory, real IndexedDB and global policy remain required. B3 existing catch records a failed normalization and retains raw bytes; richer typed XML-error state may be added explicitly later, not asserted here.

No browser PASS or complete resource PASS is claimed. Earlier managed-browser blocker is retained. Local raw GitHub downloads were DNS-blocked, so source was read/persisted via the connected GitHub tool; no network policy bypass was attempted.

## Sources checked now

- https://aistudio.yandex.ru/ru/docs/search-api/api-ref/WebSearchAsync/search — Operation and XML output setting.
- https://aistudio.yandex.ru/ru/docs/search-api/api-ref/Operation/get — completed operation response/error distinction.
- https://aistudio.yandex.ru/en/docs/search-api/reference/error-codes — XML error 15 is no results; other errors are not empty success.
- https://aistudio.yandex.ru/ru/docs/search-api/concepts/web-search — optional response fields and Base64 UTF-8 XML.

## Next action

Continue real Search policy adapter work using unchanged YMBPolicyModel and durable per-attempt accounting. Do not restart B4A. Preserve code/tests after each material block.

RELEASE_ALLOWED = NO
PROVIDER_CALLS = 0

## Простыми словами

Разбор выдачи теперь отличает настоящую пустую выдачу от ошибок и повреждённого ответа. Проверки этой части выполнены, код и тесты уже сохранены. Работа продолжается с учётом расходов; до браузерной и общей приёмки сборку для установки не выдавать.
