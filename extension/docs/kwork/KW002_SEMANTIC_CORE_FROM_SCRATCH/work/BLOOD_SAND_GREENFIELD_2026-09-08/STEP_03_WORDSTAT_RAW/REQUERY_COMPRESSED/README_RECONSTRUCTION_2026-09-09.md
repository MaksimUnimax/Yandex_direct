# STEP 03 — Wordstat re-query data reconstruction manifest — 2026-09-09

Status: `DATA_PERSISTED / LOSSLESS_RECONSTRUCTION_ACCEPTED`

## 1. What this package is

This directory contains the complete current-provider re-query data supplied back to the main ChatGPT for the semantic probes that historically occupied M001–M011.

```text
DATA_CLASS = REQUERY_CURRENT_PROVIDER_RESULT
REQUERY_IDS = R001..R011
SOURCE_RESULT_ENVELOPES = 11
OK = 10
ERROR = 1
RESULT_ROWS_PRESERVED = 6599
ASSOCIATION_ROWS_PRESERVED = 187
CANONICAL_RESPONSE_TEXT_BYTES = 691717
NUM_PHRASES_REQUESTED = 2000 for all 11 calls
REGION = 225 / Russia
DEVICE = DEVICE_ALL
```

Critical provenance boundary:

```text
THESE ARE NOT THE ORIGINAL HISTORICAL M001–M011 RESPONSE BYTES.
THESE ARE NEW RE-QUERIES WITH NEW REQUEST IDS.
THE ORIGINAL M001–M011 REGISTER ROWS MUST NOT BE OVERWRITTEN OR RETROACTIVELY RE-LABELLED.
```

The supplied Markdown export escaped underscores (`\_`) and rendered the tariff URL as a Markdown link. For durable canonical response text, those presentation escapes were normalized back to ordinary response-envelope text. No Wordstat `results` row or `associations` row was removed, filtered, deduplicated, re-ranked, or analytically cleaned during persistence.

## 2. Re-query inventory

| Re-query | Phrase | Request ID | HTTP | Status | elapsed_ms | totalCount | results | associations | canonical text bytes | canonical Git blob SHA |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---|
| R001 | оберег | `wordstat-59d28ae6-a727-400c-8cb4-9a9e6ca352a0` | 200 | OK | 2818 | 310764 | 2000 | 20 | 203403 | `b4992bd8824f4103a1aeab8d811bfae4b6e0efa4` |
| R002 | талисман | `wordstat-7fa06c3d-a03c-4daa-a1ab-a33c7583d2e6` | 200 | OK | 808 | 491801 | 2000 | 20 | 212572 | `b47b678bcb16327a79c718bc13ed87fd6f29f839` |
| R003 | чётки | `wordstat-5f8ca245-591e-4eba-afa4-03d32a86a4cd` | 200 | OK | 491 | 494957 | 2000 | 19 | 193075 | `6afb06e475638c1751ab579e4eeb4bfd78aeb776` |
| R004 | талисман в машину | `wordstat-9abdd468-6be0-4488-87b0-1ef4e0c00eec` | 200 | OK | 407 | 206 | 2 | 17 | 2773 | `6a434ffdbc21691cc270f3561a8a92956cfe2bb0` |
| R005 | чётки в машину | `wordstat-98526ed9-70df-4187-ad22-5baed43c2505` | 200 | OK | 431 | 3680 | 121 | 18 | 16229 | `5f9121fa97aec761c69fc635eb764c648e462345` |
| R006 | амулет в машину | `wordstat-c13bc962-435f-431b-ae7d-7cb942ddd7ce` | 200 | OK | 400 | 419 | 9 | 15 | 3509 | `03105ca57f5202348a45c346280dbe12bd277ea5` |
| R007 | оберег в машину | `wordstat-d917ee75-b5a8-4a89-8dc6-a5abd3758a4f` | 200 | OK | 403 | 1327 | 48 | 19 | 8532 | `9d066040dbf59ff915918e27ccd7a3543606d1e0` |
| R008 | Шлем ужаса - Эгисхьяльм | `wordstat-231fd704-273c-4762-ba35-18166f618606` | 400 | ERROR | 345 | — | 0 | 0 | 946 | `2553e29ec42c19e146da16c881be3ba08def2c00` |
| R009 | Вегвизир | `wordstat-b0ca0b5a-d4a1-4532-8825-cfbd802c8c82` | 200 | OK | 436 | 5206 | 153 | 20 | 18826 | `7c4432a59094a71d75b96c48c2d61a2fb0f4b076` |
| R010 | Гунгнир | `wordstat-d5ee7054-c755-43d9-8cd2-8dc955b1d97c` | 200 | OK | 439 | 5247 | 134 | 19 | 15580 | `9db35ea72c373f53af1cdc17b2753dc6a2fd25be` |
| R011 | Валькнут | `wordstat-b11f01df-a3f3-4782-946c-b3a06152d596` | 200 | OK | 437 | 6196 | 132 | 20 | 16272 | `7726105cf1b4b897b28fe116a647224a2b27973a` |

R008 is deliberately retained as a real provider error. The hyphenated query is distinct from the later successful corrected query `Шлем ужаса Эгисхьяльм` already preserved as M012.

## 3. Why the data is encoded

The GitHub connector writes UTF-8 text content but does not accept an arbitrary local file path as an upload payload. The largest response envelopes are hundreds of kilobytes. To avoid chat/tool truncation changing the acquired evidence depth, the canonical response text was compressed and encoded for durable storage.

This is storage transport only. It does not change the semantic data.

## 4. R001 reconstruction

Canonical R001 response text:

```text
MANUAL__R001__obereg__wordstat-59d28ae6-a727-400c-8cb4-9a9e6ca352a0.txt
bytes = 203403
Git blob SHA = b4992bd8824f4103a1aeab8d811bfae4b6e0efa4
```

Deterministic gzip representation:

```text
gzip bytes = 22089
gzip SHA256 = 9432ab73675ba1c0f72fb21e6eee9a8164b98948f13eccc654f7094fdd0776ed
gzip Git blob SHA = 6d7a3f468b7019df07296caa17ba88fde81e10a0
```

Remote storage files:

1. `MANUAL__R001__obereg__wordstat-59d28ae6-a727-400c-8cb4-9a9e6ca352a0.txt.gz.part01.b64`
2. `MANUAL__R001__obereg__wordstat-59d28ae6-a727-400c-8cb4-9a9e6ca352a0.txt.gz.part02.b64`
3. `MANUAL__R001__obereg__parts03-04.bundle.txt`

Reconstruction:

```text
base64-decode part01
+ base64-decode part02
+ extract/base64-decode part03 from the bundle
+ extract/base64-decode part04 from the bundle
= 22089-byte gzip

gunzip
= 203403-byte canonical R001 response text
```

Remote storage-file identities verified against locally generated expected content:

```text
part01.b64: size 9336, blob 2ba0aef71193614f924e73212aed62b2bbc5dcf1
part02.b64: size 9336, blob a1063377cd61160cbaf0a87aa7cfd54fb981c417
parts03-04 bundle: size 10961, blob a0b9b789fb970a94eb5b8662584818cacdad9ff8
```

## 5. R002–R011 reconstruction

R002–R011 canonical response texts are packed in one deterministic tar.gz archive.

```text
archive = R002_R011_WORDSTAT_REQUERY.tar.gz
archive bytes = 55863
archive SHA256 = e14b6d009a6ccc0c1e794f4e4bba2f4b60aa9733441e8cd18e043b3a70c40807
archive Git blob SHA = 2dd867cc8a6a8ecd98d906392e167a8eecf120c1
```

The archive is split into `part00` … `part09`; parts 00–08 are 6000 raw bytes each, part09 is 1863 raw bytes.

Authoritative reconstruction sources:

```text
part00 + part01 -> R002_R011_WORDSTAT_REQUERY.tar.gz.parts00-01.bundle.txt
part02 + part03 -> R002_R011_WORDSTAT_REQUERY.tar.gz.parts02-03.bundle.txt
part04 -> R002_R011_WORDSTAT_REQUERY.tar.gz.part04.EXACT.b64
part05 -> R002_R011_WORDSTAT_REQUERY.tar.gz.part05.EXACT.b64
part06 + part07 -> R002_R011_WORDSTAT_REQUERY.tar.gz.parts06-07.bundle.txt
part08 + part09 -> R002_R011_WORDSTAT_REQUERY.tar.gz.parts08-09.bundle.txt
```

For bundle files, take only the base64 payload under the corresponding `### ...partNN` heading. Ignore surrounding heading text and harmless terminal whitespace. Decode each part and concatenate binary parts strictly in numerical order 00..09.

The earlier file `R002_R011_WORDSTAT_REQUERY.tar.gz.parts04-05.bundle.txt` is retained for forensic traceability but is **not authoritative for reconstruction**: its remote wrapper identity differed from the locally expected writer content. Exact independently verified part04 and part05 files were therefore persisted and are authoritative.

The `parts06-07.bundle.txt` remote file differs from the no-terminal-newline local wrapper only by one terminal newline; its payload sections remain the expected encoded data. Its accepted remote identity is size 16092 / blob `750690e92d704a681e5febd493fdab5259d565ad`.

Remote identities for the authoritative archive carriers:

```text
parts00-01 bundle: size 16091, blob ab3c30601190f91c57524263d4bcc5b23eff1f39
parts02-03 bundle: size 16091, blob d1e68120af80ddd3e5b5dfa1be3c6a591b5b4b94
part04.EXACT.b64: size 8000, blob 4d16bfebf0de4027939d3e2f7d45b038af2154a7
part05.EXACT.b64: size 8000, blob 4b69b5f8b7bde4644ce053981d38ed14c0bfff07
parts06-07 bundle: size 16092, blob 750690e92d704a681e5febd493fdab5259d565ad
parts08-09 bundle: size 10575, blob eaf850dfb97ff0180f79a51f48dc3f2e52d98b2f
```

After reconstruction, verify archive SHA256 exactly. Extraction must yield these ten canonical files and Git blob SHAs:

```text
R002  b47b678bcb16327a79c718bc13ed87fd6f29f839
R003  6afb06e475638c1751ab579e4eeb4bfd78aeb776
R004  6a434ffdbc21691cc270f3561a8a92956cfe2bb0
R005  5f9121fa97aec761c69fc635eb764c648e462345
R006  03105ca57f5202348a45c346280dbe12bd277ea5
R007  9d066040dbf59ff915918e27ccd7a3543606d1e0
R008  2553e29ec42c19e146da16c881be3ba08def2c00
R009  7c4432a59094a71d75b96c48c2d61a2fb0f4b076
R010  9db35ea72c373f53af1cdc17b2753dc6a2fd25be
R011  7726105cf1b4b897b28fe116a647224a2b27973a
```

## 6. Integrity acceptance performed before this manifest

Local reconstruction QA was executed against the canonical response texts used to build the storage package.

```text
R001_RECONSTRUCTED_GZIP_BYTES = 22089
R001_RECONSTRUCTED_RAW_BYTES = 203403
R001_RAW_EQUAL_TO_CANONICAL_SOURCE = true

R002_R011_RECONSTRUCTED_ARCHIVE_BYTES = 55863
R002_R011_RECONSTRUCTED_ARCHIVE_SHA256 = e14b6d009a6ccc0c1e794f4e4bba2f4b60aa9733441e8cd18e043b3a70c40807
R002_R011_ARCHIVE_EQUAL_TO_CANONICAL_SOURCE_ARCHIVE = true
R002_R011_EXTRACTED_FILES = 10
R002_R011_ALL_EXTRACTED_FILES_EQUAL_CANONICAL_SOURCE = true

REMOTE_STORAGE_IDENTITY_R001 = PASS
REMOTE_STORAGE_IDENTITY_R002_R003 = PASS
REMOTE_STORAGE_IDENTITY_R004_R005_EXACT_STANDALONES = PASS
REMOTE_STORAGE_IDENTITY_R006_R007 = PASS_WITH_TERMINAL_NEWLINE_WRAPPER_ONLY
REMOTE_STORAGE_IDENTITY_R008_R011 = PASS
```

The integrity test is about the re-query package actually supplied. It does not claim recovery of unavailable original historical M001–M011 bytes.

## 7. Analytical boundary

This package preserves evidence. It does not perform semantic cleaning.

Examples of noise and ambiguity visible in the Wordstat output — morphology around `чётки/чётко`, media/brand meanings around `талисман`, unrelated local/business/game meanings, etc. — are intentionally preserved unchanged. Filtering and classification belong to the later analytical steps, not raw persistence.

## 8. Acceptance

```text
REQUERY_ENVELOPES_ACCOUNTED = 11/11
PROVIDER_OK = 10
PROVIDER_ERROR_PRESERVED = 1
RESULT_ROWS_ACCOUNTED = 6599
ASSOCIATION_ROWS_ACCOUNTED = 187
CANONICAL_TEXT_BYTES_ACCOUNTED = 691717
REQUERY_DATA_DROPPED_DURING_PERSISTENCE = 0
ORIGINAL_HISTORICAL_REQUEST_IDS_OVERWRITTEN = 0
```
