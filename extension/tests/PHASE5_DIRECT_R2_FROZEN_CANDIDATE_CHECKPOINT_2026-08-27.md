# Phase 5 Direct R2 frozen candidate checkpoint — 2026-08-27

Status: **FROZEN CANDIDATE + FROZEN-ARTIFACT PREFLIGHT PASS — INDEPENDENT CODEX REQUIRED — OWNER-LIVE BLOCKED**

## Authority

- Corrected source branch: `fix/phase5-credential-runtime-concurrency-2026-08-27`
- Exact source commit: `841a1e2c1a503c4a05572a957ba97c55b9b60c52`
- Exact `extension/src` tree: `edf1c2d3494ebbc53ae778d23be1457eb885b605`
- Pre-freeze full QA run: `33037727189` — PASS
- Candidate branch: `candidate/phase5-direct-first-slice-r2-2026-08-27`
- Candidate branch freeze-trigger commit: `389084290635fbf2ac305098adc3aae17f967c83`

The prior Phase 5 candidate branch `candidate/phase5-direct-first-slice-2026-08-27` and prior ZIP beginning with SHA-256 prefix `fcfb19c7` are superseded and must not be used for release, Codex QA, or owner-live.

## Corrected defect

The superseded candidate had a real credential-store concurrency defect:

1. a stale credential migration write could erase a concurrently saved Direct credential;
2. concurrent saves for different services could overwrite each other.

The corrected product serializes credential-store mutations and re-reads the current store inside the mutation transaction. Backup credential import participates in the same mutation lock.

Credential architecture remains intentionally separate:

`Wordstat != Search != Webmaster != Metrika != Direct`

No credential/token consolidation was introduced.

## Exact frozen artifact

Freeze workflow run: `33037955943`

Artifact:

- GitHub artifact name: `phase5-direct-r2-frozen-candidate-841a1e2`
- GitHub artifact ID: `9632728199`
- GitHub artifact wrapper digest: `sha256:ef8c7acd127d3f37820843e6a4f27379d7c8668d812022949739b7a0d598887c`
- GitHub artifact wrapper size: `414023` bytes
- Inner candidate ZIP: `yandex-marketing-bridge-0.1.1-phase5-direct-first-slice-r2-candidate.zip`
- **Inner candidate ZIP SHA-256: `ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b`**
- Inner candidate ZIP size: `406656` bytes
- Product files: `39`
- Manifest: `PHASE5_DIRECT_R2_EXACT_CANDIDATE_MANIFEST_2026-08-27.json`

Freeze assertions passed:

- exact pinned source commit;
- exact product tree;
- complete source Node suite;
- deterministic ZIP build;
- independent deterministic rebuild byte-equal to the first ZIP;
- ZIP integrity test;
- extracted file set and per-file SHA identity with source;
- consumer JS syntax check from exact frozen ZIP bytes;
- real Yandex requests = `0`.

## Frozen-artifact pre-Codex gate

Frozen-artifact QA branch: `qa/phase5-direct-frozen-r2-gate-2026-08-27`

GitHub Actions pre-Codex gate workflow run: `33038048376` — **PASS**

This run is a qualified frozen-artifact preflight and transport proof. It is **not** the mandatory independent Codex campaign and must not be cited as an independent Codex PASS.

The gate downloaded GitHub artifact ID `9632728199`, verified the GitHub artifact digest, verified the inner ZIP SHA-256, independently reconstructed the deterministic inner ZIP byte-for-byte, extracted that ZIP over `extension/src`, and executed Node/browser QA against those exact frozen product bytes.

Pre-Codex matrix result:

```text
D-00: PASS
D-01: PASS
D-02: PASS
D-03: PASS
D-04: PASS
D-05: PASS
D-06: PASS
D-07: PASS
D-08: PASS
D-09: PASS
D-10: PASS
D-11: PASS
D-12: PASS
D-13: PASS
D-14: PASS
D-15: PASS
D-16: PASS
D-17: PASS
D-18: PASS
D-19: PASS
D-20: PASS
D-21: PASS
D-22: PASS
direct_controlled_provider_requests: 2
direct_real_yandex_requests: 0
direct_real_credentials_used: NO
NOT_RUN_COUNT=0
PRODUCT_BYTES_POST_TEST=IDENTICAL
PHASE5_DIRECT_R2_FROZEN_GATE_PASS
```

Additional final cleanliness assertions:

```text
production_modified_during_gate = NO
package_tests_modified_during_gate = NO
direct_harness_modified_during_gate = NO
source_workspace_clean = PASS
transport_workspace_clean = PASS
enabled_not_run_sections = 0
PRODUCT_BYTES_POST_TEST = IDENTICAL
```

Permanent Phase-2/Stage-4 compatibility lifecycle regression also passed on the exact frozen bytes, including binding, Manual resync/remount/no-replay, owner-tab fencing, Search Autorun, one controlled Search provider request, and zero real Yandex requests.

## Mandatory next stage — independent Codex

Before owner-live, run one new independent Codex campaign against the exact frozen ZIP identified above.

Codex must act as an independent QA executor only and must not edit production, package tests, governed harnesses, candidate bytes, artifact bytes, or acceptance criteria.

Required final verdicts are limited to:

```text
PASS
FAIL_PRODUCT
FAIL_ARTIFACT
FAIL_HARNESS
```

A Codex PASS requires every enabled `D-00..D-22` section plus all still-applicable permanent/core/Phase-1/2/3/4 regressions to execute with zero enabled `NOT_RUN`, zero real Yandex requests and `PRODUCT_BYTES_POST_TEST=IDENTICAL`.

## Owner-live boundary — BLOCKED until independent Codex PASS

Only after a genuine independent Codex PASS may owner-live begin. The narrow owner-live Direct check is then:

1. confirm the OAuth application has `direct:api` permission;
2. confirm the application/account has approved full Yandex Direct API access for production testing;
3. install/load the **exact frozen candidate identified above**;
4. save one dedicated real Direct OAuth token in the Direct credential record only;
5. save `Client-Login` only when an agency-client context is actually required;
6. run Direct `Check` exactly once;
7. run `listCampaigns` exactly once;
8. only if a real campaign exists, perform at most one bounded downstream object read if needed;
9. run `getCampaignPerformance` exactly once for a short period only if real report data exists and online generation succeeds.

Owner-live must not exercise mutations, bids, finance/payment operations, quota/concurrency/error testing, offline reports, report polling, or automatic replay of an unknown-result POST.

## Integration lock

Do not merge/integrate Phase 5 into `main` before both:

1. independent Codex PASS is recorded;
2. owner-live result is recorded.

The frozen candidate bytes identified by SHA-256 above are immutable for Codex and owner-live; any product-byte change requires a new candidate, new freeze, new frozen-artifact preflight and a new independent Codex campaign.
