# Phase 2 Stage 4 — exact Stage-3 transport blocker

Date: 2026-08-20
Repository: `MaksimUnimax/Yandex_direct`
Development branch: `dev/phase2-search-foundation-2026-08-19`

## Classification

```text
layer: ARTIFACT / CHECKPOINT TRANSPORT
product defect: NOT ESTABLISHED
Stage-3 focused/full regression result: remains recorded PASS
Stage-4 freeze authorization: BLOCKED until exact Stage-3 bytes are recoverable from durable transport
real Yandex requests: 0
```

## Live GitHub finding

The Stage-3 evidence records an exact local patch/transport identity:

```text
raw patch SHA-256: d2338b7d1f233e3622fdc1da49038df0e96afe0785b2addfbab4f961fda9cee6
raw patch bytes: 81690
gzip SHA-256: 5c32e7a16f0102cc0c54cb59fb15a1b815795462822a8338692adef2d1487ec5
base64 SHA-256: edc73c040de67310a03c284728d45589b7a901721ff7b4b4df52d5f363b113de
base64 chars with wrapping: 26971
target manifest SHA-256: b9806e8f2a9ec172ad90ba343fa7183f7f01121fd1ddc3fb69db80b03dda423f
target files: 51
```

However, live GitHub comparison from the durable Stage-2 head
`0a59b41f48bc98a7d0c1aba7317dc61ba2f8d9b8`
to the current development branch shows only two Stage-3 commits/files beyond Stage 2:

```text
extension/tests/phase2/search-runtime-integration/STAGE3_EVIDENCE_2026-08-20.json
extension/tests/phase2/search-runtime-integration/target-tree-sha256.tsv
```

The Stage-3 patch itself is not present in the directory and repository code search does not find an expected Stage-3 patch transport file.

Therefore the Stage-3 target manifest proves the expected target identity but, by itself, does not provide byte-complete reconstruction of changed Stage-3 product/test files from the durable Stage-2 base.

## Why Stage 4 cannot freeze yet

`CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md` requires a producer/consumer-proven, byte-complete transport. GitHub upload/write success and prose/evidence-only identities are not proof of deliverability.

Freezing or packaging a Phase-2 candidate before recovering the exact Stage-3 patch would require inventing/reimplementing bytes and would break exact-candidate identity. That is forbidden.

The historical e13a QA branches were also inspected. They preserve the known successful model (Codex-side exact preimage plus text-safe patch/manifest/packer) but do not contain a byte-complete Stage-3 target or the missing Stage-3 patch.

## Required recovery measurement

Use Codex only as an independent measurement/artifact-recovery executor in the workspace where Stage 3 was produced. It must NOT modify product or test files.

Success condition is either:

1. locate the exact raw Stage-3 patch whose SHA-256 is `d2338b7d1f233e3622fdc1da49038df0e96afe0785b2addfbab4f961fda9cee6`; or
2. locate a gzip/base64 form matching the recorded hashes; or
3. locate the exact 51-file Stage-3 target and prove it matches `target-tree-sha256.tsv` 51/51, allowing a fresh exact diff against the canonical Stage-2 target to reproduce the recorded raw patch SHA.

Until one of those conditions is met:

```text
STAGE4_CANDIDATE_FREEZE = BLOCKED
CODEX_FULL_GATE = NOT AUTHORIZED
OWNER_LIVE = NOT AUTHORIZED
```
