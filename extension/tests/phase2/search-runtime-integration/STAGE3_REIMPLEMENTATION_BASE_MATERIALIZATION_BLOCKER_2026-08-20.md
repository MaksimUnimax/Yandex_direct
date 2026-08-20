# Phase 2 Stage 3 reopened — exact Stage-2 editable-base materialization blocker

Date: 2026-08-20
Repository: `MaksimUnimax/Yandex_direct`
Development branch: `dev/phase2-search-foundation-2026-08-19`

## Classification

```text
layer: ARTIFACT / SOURCE MATERIALIZATION / ENVIRONMENT BOUNDARY
product defect: NOT ESTABLISHED
Stage-2 durable target identity: ESTABLISHED
Stage-3 product write authorization: BLOCKED until exact Stage-2 target is materialized as a byte-complete editable tree
real Yandex requests: 0
```

## Established authority

Canonical durable Stage-2 target:

```text
target files: 51
target manifest SHA-256: a274600440461cc7ac4669e959d3b84ee6dfaa9dffb26219ee7e1dd0086f8236
Stage-2 raw patch SHA-256: 6b9c7f55fd736261ce794f818f66ea066dc1256c3ae05e849c97373c7b4ccedc
Stage-2 raw patch bytes: 32357
Stage-2 gzip SHA-256: 4f9bac5de1e658c40e14305d9dbe6fca17b58718a562e6e546e26328a8285a54
Stage-2 base64 SHA-256: 717d8b1c76450949053c33bfeff1921401f433076f0f8b0c9c3c78f5539f662d
```

Durable transport/evidence:

```text
extension/tests/phase2/search-worker-provider/STAGE2_EVIDENCE_2026-08-20.json
extension/tests/phase2/search-worker-provider/target-tree-sha256.tsv
extension/tests/phase2/search-worker-provider/phase2-stage2-worker-provider.patch.gz.b64
```

The Stage-2 target was previously fresh-consumer verified 51/51.

## Why ChatGPT must not write Stage 3 yet

Live development branch `extension/src` is still not the complete installable Stage-2 target. It contains the staging/shared source layout and does not contain root installable `content_script.js`, `popup.js`, `popup.html`, or `service_worker.js` as a byte-complete target tree.

The exact Stage-2 target is reconstructable through the canonical Phase-1 e13a + Stage-1 + Stage-2 transport chain, but the exact e13a preimage used by the proven route lives in the Codex QA/workspace environment rather than the current ChatGPT tool/container environment.

Environment capabilities do not inherit. ChatGPT must not infer or fabricate the missing target bytes and must not write Stage-3 product code against the incomplete staging tree.

## Required next measurement/materialization

Codex may be used only as an artifact/materialization executor, not a developer:

1. locate/verify the exact governed e13a/preimage route already demonstrated in the Codex workspace;
2. reconstruct the exact Stage-2 51-file target using only canonical published transports;
3. require the durable Stage-2 target manifest 51/51 exact;
4. do not modify any reconstructed product/test byte;
5. publish the exact reconstructed Stage-2 target to a dedicated GitHub artifact/materialization branch/root without changing the control development branch product/test bytes;
6. return the branch/root/manifest plus consumer-verifiable identities.

Preferred publication is a normal UTF-8 file tree under a dedicated transport root so ChatGPT can independently read it back and materialize an editable working tree. Publication itself is artifact transport, not product development.

Until this succeeds:

```text
STAGE3_PRODUCT_WRITE = BLOCKED
CODEX_ROLE = ARTIFACT MATERIALIZATION ONLY
OWNER_FILE_HANDLING = NONE
REAL_YANDEX_REQUESTS = 0
```
