# Yandex Marketing Bridge — Webmaster v0.1.4 live findings and implementation plan

Status: CURRENT IMPLEMENTATION CHECKPOINT
Base branch: `bridge/webmaster-full-read-surface-v0.1.3`
Base commit: `429321db7cab9ddd59dc56fdc082dbcce53aacf5`
Implementation branch: `bridge/webmaster-readiness-gzip-v0.1.4`
Scope: Bridge product under `extension/` only. Do not use Kwork/job files as a development base.

## Live acceptance evidence that triggered v0.1.4

Owner/delegated live site: `https://openscript.ru/`
Frozen provider `hostId`: `https:openscript.ru:443`

Confirmed working against real Yandex Webmaster API in v0.1.3:

- `listHosts` -> HTTP 200, host returned, `verified=true`.
- `getDiagnostics` -> HTTP 200.
- `getExportLimits` -> HTTP 200.
- `getExportDates` -> HTTP 200.
- `getExportRegions` -> HTTP 200.
- `startQueryUrlExport` -> HTTP 200, exactly one explicit POST.
- Base quota projection was 1 unit and provider confirmed exactly 1 unit used.
- Async export status remained explicit one-GET-per-command with no hidden polling.
- `collectQueryUrlExport` before SUCCESS returned local `SKIPPED / WEBMASTER_EXPORT_NOT_READY`, zero network.
- `readQueryUrlExportChunk` remained local-only, `request_executed=false`.
- Quota guards, bad-path guard, PRO confirmation guard and malformed task UUID guard all stopped before network.

Live provider-blocked methods on the same verified host:

- `getSummary`
- `getPopularQueries`
- `getAllQueryHistory`
- `getIndexingSamples`
- `getInSearchSamples`

They returned provider `HOST_NOT_LOADED`. This does **not** mean the site is absent or unverified: the same `hostId` is present in `listHosts`, is `verified=true`, and other host-specific APIs work. v0.1.3 lacks the official single-host read method needed to expose `host_data_status` directly.

Live Enhanced Export defect:

- Export task completed with `download_status=SUCCESS`.
- `collectQueryUrlExport` downloaded a real storage object with HTTP 200.
- The body began with gzip magic bytes `1F 8B`.
- v0.1.3 currently reads the download with `response.text()` and feeds that value directly into the CSV parser.
- Result: gzip bytes were misinterpreted as a CSV header, producing a false `UNRECOGNIZED_HEADER_MISSING:...` warning.
- The observed object was 22 bytes and is consistent with an empty gzip member, so a correct implementation may legitimately produce `row_count=0` with `EMPTY_REPORT` after decompression.

## Required v0.1.4 implementation

### 1. Add `getHostInfo`

Add a Bridge method for the official read endpoint:

`GET /v4/user/{user-id}/hosts/{host-id}`

Normalize and expose at minimum:

- `host_id`
- `ascii_host_url`
- `unicode_host_url`
- `verified`
- `host_data_status`
- `main_mirror` when present

`host_data_status` must preserve official provider values such as:

- `NOT_LOADED`
- `NOT_INDEXED`
- `OK`

No mutation endpoint is added.

### 2. Add normalized Webmaster readiness semantics

Public host-info result should expose provider status without turning it into an authentication/access error.

Recommended normalized fields:

- `host_data_status`
- `webmaster_data_ready` (`true` only when provider status is `OK`)

Readiness must be capability-aware, not a global "Webmaster unavailable" switch, because live acceptance proved that diagnostics and Enhanced Export can work while summary/query/indexing surfaces return `HOST_NOT_LOADED`.

### 3. Preserve `HOST_NOT_LOADED` as a provider data-readiness condition

Do not reinterpret `HOST_NOT_LOADED` as:

- OAuth failure
- wrong `hostId`
- delegation failure
- site absent
- site unverified

Preserve provider error mapping and `automatic_retry=false`. Do not add hidden retries.

### 4. Make Enhanced Export download binary-safe

Replace the current text-first transport flow with a bytes-first flow:

1. one allowlisted storage GET;
2. obtain response bytes (`ArrayBuffer` / `Uint8Array`);
3. validate final redirect URL with the existing strict storage allowlist;
4. identify transport compression;
5. if gzip, decompress locally;
6. decode decompressed CSV bytes as UTF-8;
7. feed decoded CSV text to the existing CSV normalizer.

No second storage request is permitted.

### 5. Add gzip detection and local decompression

At minimum detect gzip by magic bytes `0x1F 0x8B`.

Response headers may be used as supporting evidence but must not be the only detector.

Use a browser-native mechanism suitable for the extension runtime. Do not add a broad third-party dependency if the browser provides a reliable native decompression primitive.

On decompression failure return an explicit error such as:

- `WEBMASTER_EXPORT_GZIP_DECOMPRESSION_FAILED`

with `request_executed=true`, `automatic_retry=false`.

### 6. Correct empty-report semantics

A valid empty plain CSV payload or a valid empty gzip member must not become `UNRECOGNIZED_HEADER_MISSING`.

Expected normalized result:

- `row_count=0`
- `columns=[]`
- `parse_warning=EMPTY_REPORT`

### 7. Separate transport accounting from decoded CSV accounting

Do not hash already-corrupted text reconstructed from binary data.

Persist/report separate accounting for the downloaded transport object and decoded CSV, for example:

- `downloaded_sha256`
- `downloaded_bytes`
- `compression` = `GZIP` or `NONE`
- `csv_sha256`
- `csv_bytes`

Backward-compatibility fields may be retained only if their semantics are made unambiguous. `raw_csv` must mean decoded CSV text, not compressed bytes.

### 8. Keep compressed transport bytes out of `raw_csv`

`raw_csv` is decoded UTF-8 CSV only.

The compressed object does not need to be persisted in full. Hash + byte count are sufficient unless there is a concrete recovery requirement.

### 9. Improve collect diagnostics

Distinguish at least:

- `EMPTY_REPORT`
- `WEBMASTER_EXPORT_GZIP_DECOMPRESSION_FAILED`
- UTF-8 decode failure when detectable
- `UNRECOGNIZED_HEADER_MISSING:...`
- `WEBMASTER_EXPORT_INVALID_CSV`

Never report a gzip container itself as a CSV header.

### 10. Preserve security and request boundaries

Keep all existing accepted controls:

- storage host must be exactly `storage.mds.yandex.net`;
- path must begin `/get-webmaster-download/`;
- HTTPS only;
- no user/password in URL;
- final response URL must pass the same allowlist;
- no OAuth header on storage download;
- one `collectQueryUrlExport` command -> at most one storage GET;
- no hidden polling;
- no automatic replay of unknown-outcome POST;
- `automatic_retry=false` throughout these boundaries.

### 11. Add realistic gzip QA

Tests must cover at minimum:

- plain CSV;
- gzip CSV;
- empty gzip member;
- gzip CSV with Cyrillic UTF-8;
- quoted CSV field inside gzip;
- corrupt gzip;
- transport SHA/bytes;
- decoded CSV SHA/bytes;
- one-download-request invariant;
- no OAuth on storage GET.

### 12. Add `getHostInfo` protocol/runtime QA

Cover:

- `host_data_status=OK`;
- `NOT_LOADED`;
- `NOT_INDEXED`;
- `main_mirror` normalization;
- one OAuth GET;
- no mutation;
- public `webmaster_data_ready` normalization.

### 13. Preserve proven v0.1.3 contracts

The following are already accepted in live/controlled QA and must not regress:

- quota projection guard;
- explicit quota confirmation;
- explicit PRO confirmation;
- invalid export path guard;
- invalid task UUID guard;
- exact provider request boundaries;
- durable export task record;
- local-only chunk reads;
- collect-before-ready local skip;
- explicit async status checks;
- unknown POST outcome -> `UNKNOWN`, no retry, no fabricated task;
- Wordstat and Search delegation through the shared provider stack;
- no client-site/property mutation APIs.

## Product/version surfaces expected to move to v0.1.4

At minimum inspect/update as required:

- `extension/src/shared/webmaster_protocol.js`
- `extension/src/shared/phase3_provider_runtime.js`
- `extension/src/shared/policy_model.js` if default method allowlist migration needs the new method
- `extension/src/shared/product.js`
- `extension/src/manifest.json`
- `extension/src/package.json`
- `extension/src/webmaster_worker_runtime.js` if user-facing method guidance enumerates supported Webmaster methods
- `extension/src/popup.html` if version/method documentation is rendered there
- `extension/tests/webmaster_v013_protocol.test.mjs` or successor v0.1.4 tests
- `extension/tests/webmaster_v013_runtime.test.mjs` or successor v0.1.4 tests
- `extension/tests/webmaster_v013_dependency_regression.test.mjs` or successor
- Browser QA and deterministic packer/workflows if their version assumptions require v0.1.4.

## Release gate

Do not call v0.1.4 complete until:

1. source Node suite passes;
2. packaged Node suite passes;
3. installed exact-artifact Webmaster browser runtime passes;
4. Direct/popup common regression passes;
5. Manual lifecycle regression passes;
6. Search Batch regression passes;
7. GenSearch regression passes;
8. Wordstat/Search dependency delegation remains proved;
9. exact artifact is built and its SHA-256/bytes/entries are recorded;
10. no Kwork/job files are part of the product delta;
11. live follow-up can reuse the existing export task when practical instead of spending another quota unit.

## Live task to reuse after fix

Existing real task:

`3d18b4d1-a5e1-11f1-937d-c10593444139`

Host:

`https:openscript.ru:443`

Provider-confirmed quota accounting after the live test:

- limit: 100
- used: 1
- remaining: 99

Do not launch a new quota-bearing export merely to retest gzip if the existing successful task remains downloadable.
