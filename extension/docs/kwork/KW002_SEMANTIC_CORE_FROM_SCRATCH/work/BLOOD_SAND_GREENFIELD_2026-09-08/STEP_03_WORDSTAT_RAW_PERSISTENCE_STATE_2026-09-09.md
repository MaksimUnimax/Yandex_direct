# STEP 03 — WORDSTAT RAW PERSISTENCE STATE

Date: 2026-09-09
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Status: **LATE CORRECTION / ACQUISITION COMPLETE / DURABLE RAW REWORK REQUIRED**

## Current authority

A later Step-04 Work readback invalidated the earlier statement `STEP03_ACQUISITION_PERSISTENCE = COMPLETE / PASS` as a combined claim.

The corrected distinction is mandatory:

```text
CANONICAL_PRIMARY_MANIFEST_ROWS = 79
CANONICAL_PRIMARY_RUN_ORDER = 1..79
CANONICAL_PRIMARY_PROBES_WITH_CURRENT_ACQUISITION_OUTCOME = 79
STEP03_PROVIDER_ACQUISITION = COMPLETE / 79 OF 79
LOSSLESS_GITHUB_FEED_FORWARD_RAW = 60 OF 79
STEP03_DURABLE_RAW = CORRECTION / REWORK REQUIRED
OLD_COMBINED_PERSISTENCE_PASS = OVERRIDDEN
```

Affected canonical run orders:

```text
32,33,34,35,36,37,38,39,40,41,
42,43,44,45,46,47,48,50,51
```

The complete late-correction record is:

`STEP_03_RAW_RECOVERY_2026-09-09.md`

## Preserved historical boundary

The original historical M001–M011 request-specific bodies were not durably persisted under their original request IDs. They remain historical missing-original evidence and are not relabelled or overwritten. Later current-provider re-query evidence for canonical probes remains preserved under its own request IDs.

The canonical run_order 1 current re-query remains valid:

```text
phrase = амулет
request_id = wordstat-86e7b86f-b118-4a08-b4bf-564b053de070
HTTP = 200
results[] = 2000
associations[] = 20
totalCount = 478857
request_executed = true
automatic_retry = false
raw path = STEP_03_WORDSTAT_RAW/MANUAL__001_CURRENT_REQUERY__wordstat-86e7b86f-b118-4a08-b4bf-564b053de070.raw.txt
```

This late correction does not alter that observation.

## Broken carrier correction

Two large manual delivery bundles were not safely persisted as lossless binary carriers:

```text
MANUAL_BLOCK__032-041__2026-09-09
MANUAL_BLOCK__042-051__2026-09-09
```

Their manifests preserve expected uncompressed/gzip checksums and row inventories, but the live Git binary parts do not reconstruct to those expected values. Therefore `FILE EXISTS`, recorded manifest blob SHA, or the earlier persistence PASS cannot be treated as proof of usable downstream evidence.

## Recovery source

The original full delivery text for both affected blocks has been located in preserved ChatGPT File Library uploads from the prior dialogue. This is sufficient to justify source rehydration before any paid replay, but File Library is not the final durable project store.

```text
RECOVERY_SOURCE_FOUND = true
RECOVERY_SOURCE_REHYDRATION_FIRST = true
PROVIDER_REQUERY = FALLBACK_ONLY_IF_NEEDED
PROVIDER_REQUESTS_DURING_RECOVERY_SO_FAR = 0
```

## PASS condition

Step03 durable feed-forward may return to PASS only after:

```text
all 19 affected probes have complete durable row-level payload
request IDs reconcile
results[] row counts reconcile
associations[] row counts reconcile
totalCount / exact empty-object outcomes reconcile
79/79 primary feed-forward is readable
GitHub remote readback passes
no source row is silently dropped
```

Until then:

```text
WORDSTAT_PRIMARY_ACQUISITION_COMPLETE = true
STEP03_DURABLE_RAW_COMPLETE = false
NEXT_STEP_ALLOWED = false
STEP04_ALLOWED = false
NEXT_ACTION = MATERIALIZE_AND_VERIFY_RECOVERED_RAW_19
```
