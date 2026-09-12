# B8 — bounded export, execution started

Date: 2026-09-12. Read-only live base: `b77c014d02e040679829ccb2c8d61710312b386a`.
Read current B7 continuation cursor and mandatory dependency/resource rule before this block. Exact owner 0.1.4 ZIP exists locally and SHA-256 was rechecked: `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`.

## Scope

Add explicit local `exportPage` to deferred Manual operations. Export contiguous item pages with query, parameters, status, saved raw response and normalized results. No representative sampling; continuation has exact revision and next item position. Revisions must not mix silently. Export does not submit, collect, retry, normalize or delete research evidence.

Reuse the unchanged Patch A `stageTextArtifact` and existing attachment descriptors/outbox. Do not introduce a second Base64 artifact map, content-side buffer path, or GitHub uploader.

The page builder will have a hard local byte budget checked BEFORE large JSON serialization, a bounded item count, and explicit next-page information. One page is materialized, not the entire job. This is bounded paging, not a claim of constant-memory streaming. An oversized single record must fail without truncation or advancing the continuation. Raw bytes/normalized records stay in source storage.

## Dependency matrix to complete

- B3 store: owned read-only export metadata/one-item revision checks; previous write/recovery behavior stays unchanged.
- New page builder -> unchanged Patch A staging/checksum/cleanup interface.
- B2 protocol: additive exportPage schema only.
- B7 Manual worker: trusted export authority, delivery ID, outbox descriptors, compact response, failure cleanup.
- Existing commands/owner/outbox: run relevant regression, no provider calls.
- Packaging/bootstrap: do not enable operation host or release ZIP during this block.

## Evidence boundary

Run actual executable Node tests and exact-byte checks available here. Do not repeat known blocked browser launch or bypass policies. Node/IDB doubles do not become Chrome memory or real IndexedDB proof. No source code is yet changed by this checkpoint.

RELEASE_ALLOWED = NO
B8_STATUS = IN_PROGRESS
NEXT = implement and persist bounded exporter plus executable tests before further integration.
