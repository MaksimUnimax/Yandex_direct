# Yandex Marketing Bridge — Webmaster v0.1.4 readiness + gzip addendum

Status: CURRENT VERSION-SPECIFIC CONTRACT / IMPLEMENTED CANDIDATE

This addendum supersedes the v0.1.3 Webmaster contract only where explicitly stated below. All accepted v0.1.3 non-destructive, request-boundary, quota, durable-task, secret-isolation and no-auto-retry guarantees remain in force.

## 1. New read-only method: `getHostInfo`

Command:

```text
WEBMASTER_API_V1
{"method":"getHostInfo","hostId":"https:example.com:443"}
```

Provider request:

```text
GET /v4/user/{user-id}/hosts/{host-id}
```

This is a single read-only OAuth GET. It does not add, verify, modify or delete a host.

Normalized stable fields:

- `host_id`
- `ascii_host_url`
- `unicode_host_url`
- `verified`
- `host_data_status`
- `webmaster_data_ready`
- `host_display_name` when the provider supplies it
- `main_mirror` stable host fields when present

`webmaster_data_ready` is `true` only when `host_data_status === "OK"`. Missing or non-OK provider state is never promoted to ready.

Known official data states include:

- `NOT_LOADED`
- `NOT_INDEXED`
- `OK`

The provider value is preserved. The Bridge must not reinterpret `HOST_NOT_LOADED` as an OAuth failure, wrong `hostId`, missing delegation, missing site, or unverified site.

## 2. Readiness is capability-aware

A non-OK `host_data_status` does not globally disable Webmaster.

Live v0.1.3 acceptance demonstrated that a verified host can return `HOST_NOT_LOADED` for summary/query/indexing methods while diagnostics and Enhanced Export discovery/lifecycle still work. Therefore the Bridge exposes host readiness evidence but does not synthesize a global service lock.

There is no hidden readiness probe before every command. `getHostInfo` is an explicit one-request command.

## 3. Enhanced Export collection is bytes-first

`collectQueryUrlExport` keeps the same durable-task and one-download-request contract but changes payload handling from text-first to bytes-first.

Flow:

1. load the durable export task locally;
2. require `download_status === "SUCCESS"` and an allowlisted stored URL;
3. issue at most one GET to the allowlisted storage URL;
4. validate the final response URL using the same allowlist;
5. read response bytes via `arrayBuffer()` when available;
6. hash/account the downloaded transport bytes;
7. detect gzip by magic bytes `1F 8B`;
8. if gzip, decompress locally with the browser-native `DecompressionStream("gzip")`;
9. decode the resulting CSV bytes as strict UTF-8;
10. parse/normalize CSV;
11. persist normalized rows plus decoded CSV and separate transport/CSV accounting.

No second storage request is introduced.

## 4. Gzip behavior

Compression values:

- `GZIP` — downloaded bytes begin with gzip magic `1F 8B` and are locally decompressed;
- `NONE` — downloaded bytes are treated as the CSV byte stream directly.

A corrupt gzip container fails explicitly with:

```text
WEBMASTER_EXPORT_GZIP_DECOMPRESSION_FAILED
```

The external storage request has already executed, therefore the error is fenced as:

- `request_executed = true`
- `automatic_retry = false`

There is no automatic redownload.

## 5. UTF-8 behavior

The decoded CSV byte stream is decoded with strict UTF-8 semantics.

Invalid UTF-8 fails explicitly with:

```text
WEBMASTER_EXPORT_INVALID_UTF8
```

Again:

- `request_executed = true`
- `automatic_retry = false`

## 6. Empty export behavior

A valid empty plain payload or a valid empty gzip member is a valid empty report, not a malformed-header report.

Normalized result:

```text
row_count = 0
columns = []
parse_warning = EMPTY_REPORT
```

No rows are fabricated.

## 7. Transport vs CSV accounting

Public durable manifest exposes separate accounting:

```text
downloaded_sha256
downloaded_bytes
compression
csv_sha256
csv_bytes
```

Semantics:

- `downloaded_*` hashes/counts the exact object returned by storage;
- `csv_*` hashes/counts the decoded CSV byte stream after optional gzip decompression.

Backward-compatibility fields are retained:

```text
raw_sha256 = csv_sha256
raw_bytes = csv_bytes
```

`raw_csv` means decoded UTF-8 CSV text only. Compressed gzip bytes are never stored in `raw_csv`.

The full compressed transport object does not need to be persisted; its SHA-256 and byte count are the durable transport evidence.

## 8. CSV parser behavior retained

Recognized stable columns remain:

```text
date
host
URL
query
region
clicks
impressions
position
```

The existing parser continues to support:

- UTF-8 BOM;
- CRLF/LF;
- comma/semicolon/TAB delimiter detection;
- quoted fields;
- escaped double quotes;
- stable Russian/English header aliases;
- nullable numeric fields.

If the decompressed text is non-empty but required headers cannot be mapped, the Bridge preserves explicit:

```text
UNRECOGNIZED_HEADER_MISSING:<fields>
```

If CSV quoted-field syntax is invalid:

```text
WEBMASTER_EXPORT_INVALID_CSV
```

## 9. Storage download security boundary retained

Accepted download URL must satisfy all of:

- scheme exactly `https`;
- hostname exactly `storage.mds.yandex.net`;
- pathname begins `/get-webmaster-download/`;
- no username;
- no password.

The final response URL must satisfy the same rule.

Storage request headers never contain Webmaster OAuth Authorization.

Manifest permission remains exactly:

```text
https://storage.mds.yandex.net/*
```

No `*.yandex.net` wildcard is added.

## 10. Async/export request boundaries retained

- `startQueryUrlExport` — exactly one explicit quota-bearing provider POST per command.
- `getQueryUrlExportStatus` — exactly one provider GET per command.
- `collectQueryUrlExport` — at most one storage GET per command, only after durable SUCCESS.
- `readQueryUrlExportChunk` — local storage only, zero network.
- no hidden status polling;
- no hidden download after a status command;
- no automatic retry of unknown-outcome external requests;
- unknown start POST outcome never fabricates a task ID and is never automatically replayed.

## 11. Quota/PRO guards retained

`startQueryUrlExport` still requires:

- `confirmQuota:true`;
- exact `expectedQuotaUnits = dates.length * paths.length`;
- valid `/`-prefixed paths;
- base-mode per-command projection <= 100 quota units;
- explicit independent `confirmProTariff:true` when `useProTariff:true`.

The Bridge never silently enables PRO.

## 12. Policy migration

Current default Webmaster allowlist contains 16 methods including `getHostInfo`.

Two historical default shapes are automatically migrated forward:

1. original four-method default:
   - `listHosts`
   - `getSummary`
   - `getDiagnostics`
   - `getPopularQueries`
2. exact v0.1.3 fifteen-method default.

Explicit/custom non-default allowlists remain restrictive and are not silently broadened.

## 13. Runtime dependency decision

Production gzip handling uses browser-native Web Platform APIs only:

- `Response.arrayBuffer()`
- `Uint8Array`
- `TextEncoder` / `TextDecoder`
- `crypto.subtle.digest`
- `Response` / Web Streams
- `DecompressionStream("gzip")`

No new third-party runtime/npm dependency is bundled into the extension for gzip handling.

If the runtime lacks native gzip decompression support, collection fails closed with `WEBMASTER_EXPORT_GZIP_DECOMPRESSION_FAILED`; it does not fetch an external decompression library.

## 14. Non-destructive site boundary retained

Still forbidden:

- add/delete host;
- verification mutation;
- recrawl submission;
- Sitemap mutation;
- important-URL mutation;
- original-text submission;
- owner/rights mutation;
- any other site/property state mutation.

The async Enhanced Export POST creates an analytics export task only; it does not mutate the client site/property.

## 15. Required acceptance coverage

The v0.1.4 release gate must prove at minimum:

- `getHostInfo` exact one-GET route and readiness normalization for `NOT_LOADED`, `NOT_INDEXED`, `OK`;
- plain CSV collect remains functional;
- gzip CSV collect with Cyrillic and quoted fields;
- valid empty gzip -> `EMPTY_REPORT`;
- corrupt gzip -> explicit fail-closed error;
- invalid UTF-8 -> explicit fail-closed error;
- separate downloaded-vs-CSV hashes/bytes;
- no OAuth on storage GET;
- one-collect/one-storage-GET boundary;
- old collect-before-ready local skip;
- full source and exact-packaged Node regression;
- installed exact-artifact browser runtime using real browser gzip primitives but controlled network;
- Direct/popup/manual lifecycle regression;
- Search Batch regression;
- GenSearch regression;
- Wordstat/Search delegation through the modified shared provider stack;
- no Kwork/job files in Bridge product work;
- deterministic exact candidate artifact with recorded SHA-256/bytes/entries.
