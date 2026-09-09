# STEP 03 — RAW RECOVERY / LATE PERSISTENCE CORRECTION

Date: 2026-09-09
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Status: **RECOVERY IN PROGRESS / PROVIDER ACQUISITION 79/79 COMPLETE / DURABLE FEED-FORWARD RAW 60/79**

## Why this correction exists

A late Step-04 Work readback proved that the earlier Step-03 persistence PASS was too broad. All 79 canonical primary probes have current acquisition outcomes, but the full row-level `results[]` / `associations[]` payload cannot currently be reconstructed losslessly from GitHub for 19 canonical run orders.

This document overrides only the old persistence-completeness claim. It does not invalidate the factual fact that the 79 canonical primary probes were acquired.

```text
CANONICAL_PRIMARY_PROBES = 79
CURRENT_ACQUISITION_OUTCOME_PRESENT = 79/79
LOSSLESS_GITHUB_FEED_FORWARD_RAW = 60/79
AFFECTED_RUN_ORDERS = 32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51
STEP03_ACQUISITION = COMPLETE
STEP03_DURABLE_RAW = CORRECTION / REWORK REQUIRED
STEP04_SEMANTIC_EXECUTION_ALLOWED = false
```

## Broken carrier facts

### Block 032–041

Manifest authority: `STEP_03_WORDSTAT_RAW/MANUAL_BLOCK__032-041__2026-09-09__MANIFEST.md`.

Expected:

```text
gzip bytes = 73423
gzip sha256 = 77b25daef86d13840672d2564af1cf860c94e7625fe0b510f1d6a59f43f487fb
raw bytes = 782995
raw sha256 = 2c325758ec60314ba30ccf1c16116328d14d93cbea2d9a5f53ac93f1d6a03e37
```

Live GitHub carrier observations include:

```text
part01 expected 20000 / observed 14998
part02 expected 20000 / observed 16057
part03 expected 20000 / observed 4275
part04 expected 13423 / matched
```

The manifest's recorded Git blob SHAs do not provide a recovery path: the live Git objects at those SHAs themselves have the shortened sizes. Therefore reattaching those blobs is a no-op and does not restore the original bytes.

### Block 042–051

Manifest authority: `STEP_03_WORDSTAT_RAW/MANUAL_BLOCK__042-051__2026-09-09__MANIFEST.md`.

Expected:

```text
gzip bytes = 66784
gzip sha256 = ba220113f04060d60e717468ee9256bfd603630e2803bb05aa3fc29f85e4f194
raw bytes = 703355
raw sha256 = 98a4fa9966d95f0149f45a635ffe7c1737a63512c7a8946d4c8de8c826af5fed
```

Known broken parts from the Work/readback gate:

```text
part04 expected 10000 / observed 9999
part05 expected 10000 / SHA mismatch
```

Run 49 remains independently readable and is not part of the missing set. Runs 50 and 51 are canonical empty provider results `{}` but their original block carrier still belongs to the broken bundle and must be restored/re-materialized explicitly.

## Recovery source found without a new provider call

The original prior-dialogue uploads still exist in ChatGPT File Library and contain the full Wordstat delivery text:

```text
RECOVERY_SOURCE_A
name = Вставленная ​​уценка.md
created = 2026-09-09T07:20:47Z
content = original WORDSTAT_RESULT_V1 block for canonical run orders 32–41

RECOVERY_SOURCE_B
name = Вставленная ​​уценка.md
created = 2026-09-09T07:46:51Z
content = original WORDSTAT_RESULT_V1 block for canonical run orders 42–51
```

Spot readback from these sources confirms the original request IDs and complete row-level payload text are present. These File Library objects are recovery input, not final durable project evidence. Step03 cannot regain PASS until their complete source is materialized into GitHub and verified.

## Recovery order

```text
1. SOURCE_REHYDRATION_FROM_PRESERVED_FULL_UPLOADS
2. rebuild a durable text/raw representation that is safe for Git transport
3. verify all 19 affected request IDs
4. verify results-row / associations-row / totalCount against the two block manifests
5. verify 79/79 feed-forward readability
6. GitHub readback
7. only then restore STEP03_DURABLE_RAW = PASS
```

Do not recreate the failure by splitting gzip bytes through a text-only storage path. Prefer a text-safe durable representation (for example exact UTF-8 raw text plus checksums, or base64 with a deterministic decoder) if binary transport cannot be proven byte-safe.

## Provider replay fallback

Owner authorization in the active dialogue allows re-collection if recovery from preserved source is not sufficient.

Provider replay is a fallback, not the first choice, because original complete source has been located.

If replay becomes necessary:

```text
ACTIVE SERVICE = wordstat
METHOD = getTop
REGION = 225
DEVICES = DEVICE_ALL
NUM_PHRASES = 2000
REPLAY ONLY THE PROBES STILL NOT LOSSLESSLY RECOVERABLE
ONE USEFUL RESULT -> FULL DURABLE GITHUB WRITE -> READBACK -> COUNTS/FIELDS/PROVENANCE -> ONLY THEN NEXT PROVIDER REQUEST
```

Historical request IDs must never be overwritten by replay. Every replay is a new observation with a new request ID and explicit provenance.

```text
PROVIDER_REQUESTS_EXECUTED_DURING_THIS_RECOVERY_SO_FAR = 0
PROVIDER_COST_DURING_THIS_RECOVERY_SO_FAR = 0
```

## Current external execution limitation

The current ChatGPT session does not have a connected browser runtime for the local Yandex Marketing Bridge. Therefore no provider request has been fabricated or claimed. If source rehydration cannot be completed through the available File Library interface, provider replay remains pending until an actual Bridge runtime is available and its active service / Manual-Autorun state can be confirmed.

## Accidental empty write probes during recovery investigation

Three empty placeholder files were accidentally created while testing Git write mechanics and immediately deleted. They contained no project data. Cleanup commits are preserved in history; no placeholder file remains in the tree. No semantic, provider, assortment, or methodology file was changed by those probes.

## Gate

```text
STEP03_PROVIDER_ACQUISITION = COMPLETE_79_OF_79
STEP03_DURABLE_FEED_FORWARD = FAIL_60_OF_79
RECOVERY_SOURCE_FOUND = true
RECOVERY_MATERIALIZATION_COMPLETE = false
STEP04_ALLOWED = false
NEXT_ACTION = MATERIALIZE_AND_VERIFY_FULL_RAW_FOR_19_AFFECTED_PROBES
```
