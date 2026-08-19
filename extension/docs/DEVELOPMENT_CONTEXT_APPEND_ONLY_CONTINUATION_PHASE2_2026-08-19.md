# DEVELOPMENT CONTEXT — APPEND-ONLY CONTINUATION — PHASE 2

Created: 2026-08-19.

This file continues the append-only project history. It records the exact Phase-2 checkpoint at the owner-requested pause boundary. Historical entries remain unchanged.

---

# ENTRY 0032 — 2026-08-19 — PHASE 1 CLOSED; PHASE 2 REQUIREMENTS/GATE READY

Phase 1 Wordstat is closed on exact accepted artifact:

```text
e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
209505 bytes
45 files
48 ZIP entries
```

Complete Codex pre-delivery gate on this artifact: PASS.
Owner real-profile functional Wordstat acceptance: PASS for `getRegionsTree`, `getTop`, corrected `getDynamics`, and `getRegionsDistribution`.
Issues #1 and #2: CLOSED / COMPLETED.

Phase 2 Search requirement/spec/gate authorities were created before product changes:

```text
extension/docs/PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
```

Current first Search slice:

```text
protocol: SEARCH_API_V1
service: search
method: search
mode: synchronous text web search
provider endpoint: /v2/web/search
canonical response format: FORMAT_XML
result signature: SEARCH_RESULT_V1
```

Deferred search, image search, generative search, HTML normalization and browser scraping of yandex.ru remain outside this first slice.

---

# ENTRY 0033 — 2026-08-19 — SEARCH FOUNDATION RESEARCH CHECKPOINT; NO PRODUCT CHANGE YET

Before implementing Phase 2, live `main` was re-read. At the pause boundary the latest observed live HEAD before this checkpoint documentation is:

```text
96749cf0a902455d0ca9df68f839651d0bf54d27
message: docs: authorize Phase 2 Search implementation foundation
```

No Phase-2 production source has been changed yet.

Existing Phase-1 product tree facts were re-established from GitHub, including:

```text
extension/src/shared/service_registry.js
extension/src/shared/wordstat_protocol.js
extension/src/shared/policy_model.js
extension/src/shared/credential_registry.js
extension/src/shared/autorun_model.js
extension/src/manifest.json
```

The accepted exact e13a target-tree manifest also confirms the combined installable source layout and production files, including root-level `service_worker.js`, `content_script.js`, `popup.js` and shared modules.

Official Yandex implementation facts were checked against current Yandex-owned SDK source rather than guessed:

1. `WebSearchRequest` construction uses `SearchQuery`, `GroupSpec`, `SortSpec`, `folder_id`, `region`, `l10n`, `max_passages`, response format and optional user agent/metadata.
2. Synchronous Web Search is the normal first-slice path; deferred uses a separate operation lifecycle.
3. Parsed XML results are built by UTF-8 XML parsing, finding `<response>`, iterating `<group>` and then `<doc>` entries.
4. Current official SDK's Web Search document parser treats `url`, `domain`, `title`, `modtime` and `lang` as optional and collects all `<passage>` elements.
5. `modtime` parsing uses provider form `YYYYMMDDTHHMMSS` when valid and tolerates invalid/missing values.

Primary current Yandex-owned code evidence inspected:

```text
yandex-cloud/yandex-ai-studio-sdk
src/yandex_ai_studio_sdk/_search_api/web/web.py
src/yandex_ai_studio_sdk/_search_api/web/config.py
src/yandex_ai_studio_sdk/_search_api/web/result.py
src/yandex_ai_studio_sdk/_search_api/types.py
```

This evidence is sufficient for the non-browser Search protocol/XML foundation and avoids inventing XML structure or provider request mapping.

Important engineering rule reaffirmed by owner:

```text
If a fact needed for implementation is unknown and is browser/DOM/runtime-state specific,
do not guess.
Ask Codex to measure the exact fact with a concrete executable QA/measurement prompt.
Use live GitHub for repository facts and official Yandex sources for public API facts.
```

No Codex measurement is currently required for the pure Search protocol/XML foundation because the needed facts are available from source/official API evidence. If later popup/current-ChatGPT DOM/browser behavior is uncertain, stop development at that uncertainty and request Codex measurement instead of inventing behavior.

---

# ENTRY 0034 — 2026-08-19 — OWNER-REQUESTED PAUSE

Owner explicitly ordered work to pause and wait for a continuation command.

State at pause:

```text
PHASE 1 = LIVE PASS / CLOSED
PHASE 2 requirements = COMPLETE
PHASE 2 spec addendum = READY
PHASE 2 gate addendum = READY
PHASE 2 production changes = NONE YET
old Phase-1 full-gate PASS remains valid only for the unchanged Phase-1 artifact
next production change will invalidate that artifact PASS for any new combined handoff
```

Planned resume point, and only after owner says to continue:

```text
1. re-fetch live main and CURRENT_STATE;
2. implement smallest non-browser Search foundation:
   - service registry registration for search/SEARCH_API_V1;
   - Search protocol/defaults/strict validation;
   - exact synchronous WebSearch request-body builder;
   - Base64 UTF-8 XML normalization with tolerant optional-field handling;
3. add focused tests for those modules;
4. run focused/source checks;
5. continue into worker/provider/policy integration only after the foundation is green;
6. whenever an unknown browser/DOM/runtime fact is encountered, request Codex measurement instead of guessing;
7. do not require owner intervention until an irreducible owner action or Codex execution is actually needed.
```

Until the owner explicitly commands continuation, no further product, test, QA-transport, Codex, or owner-live action is authorized.

---

# ENTRY 0035 — 2026-08-19 — RESUMED; SOURCE-AUTHORITY CHECK BEFORE FIRST PHASE-2 PRODUCT WRITE

The owner explicitly resumed work.

Live `main` at resume/reconstruction:

```text
5670de698c3d8c31015ae880e5dd4d0b38723172
message: docs: pause Phase 2 at recorded foundation checkpoint
```

Before editing production, repository/source authority was checked again rather than assuming `extension/src` was the complete accepted e13a installable tree.

New concrete repository finding:

```text
main: extension/src currently contains README.md, README.txt, manifest.json, package.json and shared/
main: extension/src does NOT contain root installable content_script.js, popup.js or service_worker.js
```

Therefore `main/extension/src` by itself is not a byte-complete editable representation of the accepted 45-file e13a artifact and must not be treated as the full Phase-2 product base.

Additional exact source-lineage evidence re-established:

```text
commit 794531d858b784ee5c6f09e99d87adce476bb863
message: fix: prevent Manual ON self-revert and add cross-layer regression
```

That commit records the repair that created the accepted e13a product bytes and the mandatory Manual-ON cross-layer regression. The successful QA transport remains:

```text
branch: qa/e13a-exact-reconstruction-v3
preimage: 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
raw patch SHA-256: 709234433bd446f52a18c95785675d0f5ca3450b82459ce2631d36bdb7269bc2
target manifest: extension/tests/qa_transport/e13a/target-tree-sha256.tsv
canonical packer: extension/tests/qa_transport/e13a/canonical_packer_exact.py
accepted target: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65 / 209505 / 45 files / 48 ZIP entries
```

The target-tree manifest confirms the accepted installable tree contains root-level `content_script.js`, `popup.js`, `service_worker.js`, shared modules and tests; it must be the byte-identity authority for the Phase-2 development base.

Search foundation source facts reconfirmed from live repository:

```text
shared/service_registry.js currently registers only WORDSTAT_API_V1 → wordstat
shared/wordstat_protocol.js provides the existing style for prefix parsing, strict validation, request construction, fingerprinting and result/error formatting
manifest host permissions already include https://searchapi.api.cloud.yandex.net/*
```

Current Yandex-owned SDK source was also checked for exact enum/field mapping instead of inventing values. Confirmed Search first-slice enum families include:

```text
SEARCH_TYPE_RU/TR/COM/KK/BE/UZ
FAMILY_MODE_NONE/MODERATE/STRICT
FIX_TYPO_MODE_ON/OFF
SORT_ORDER_ASC/DESC
SORT_MODE_BY_RELEVANCE/BY_TIME
GROUP_MODE_FLAT/DEEP
LOCALIZATION_RU/UK/BE/KK/TR/EN
FORMAT_XML/FORMAT_HTML
```

The current SDK's synchronous `WebSearchRequest` construction confirms the first-slice body structure around:

```text
query.queryText/searchType/familyMode/fixTypoMode/page
folderId
groupSpec.docsInGroup/groupsOnPage/groupMode
l10n
maxPassages
region
responseFormat
sortSpec.sortMode/sortOrder
optional userAgent/metadata
```

No browser/DOM/runtime unknown was encountered during this resumed research, so no Codex measurement was required.

Most important checkpoint decision:

```text
DO NOT WRITE PHASE-2 PRODUCT CODE INTO AN INCOMPLETE/STAGING SOURCE TREE.
FIRST RECONSTRUCT OR MATERIALIZE A BYTE-EXACT EDITABLE e13a WORKING TREE,
VERIFY IT 45/45 AGAINST target-tree-sha256.tsv,
THEN BRANCH/COMMIT THE FIRST SEARCH FOUNDATION CHANGES FROM THAT VERIFIED BASE.
```

State at this checkpoint:

```text
PHASE_2_PRODUCTION_CHANGES = NONE
PHASE_2_TEST_CHANGES = NONE
CODEX_MEASUREMENT_PENDING = NO
OWNER_ACTION_PENDING = NO
NEW_BLOCKER = exact editable e13a working-tree materialization/45-of-45 verification before first product write
NEXT_ENGINEERING_ACTION = reconstruct verified e13a development base, then implement Search foundation
```
