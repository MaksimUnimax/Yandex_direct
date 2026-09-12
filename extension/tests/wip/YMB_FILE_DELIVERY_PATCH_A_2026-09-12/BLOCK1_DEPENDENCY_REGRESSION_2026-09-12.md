# YMB Patch A — dependency regression block 1

Date: 2026-09-12
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Candidate: exact `candidate2` reconstructed from owner 0.1.4 baseline; production bytes unchanged during this block.

## Scope

This block validates syntax/load/static/storage/outbox/attachment paths directly affected by Patch A.

## Harness incident

Initial run stopped before a product assertion because local QA helper `worker_vm_harness.mjs` referenced `fileURLToPath` without importing it from `node:url`.

Classification:

```text
FAIL_HARNESS = YES
FAIL_PRODUCT = NO
PRODUCTION_MODIFICATIONS = 0
```

Only the local QA harness was corrected. The candidate production tree was not edited. The entire block was then rerun from the beginning.

## Rerun results

```text
JS_SYNTAX_PASS = 51 production JS files
JSON_PARSE_PASS = manifest.json + package.json
STATIC_RESOURCE_REGRESSION = PASS
WORKER_BOOTSTRAP_SMOKE = PASS
ARTIFACT_STAGE_FAILURE_CLEANUP = PASS
WORKER_SMALL_OUTBOX_REGRESSION = PASS
WORKER_LARGE_OUTBOX_CONTRACT = PASS
WORKER_OUTBOX_FAILURE_CLEANUP = PASS
WORKER_ATTACHMENT_CONTRACT = PASS
BLOCK1 = PASS
```

Important assertions reached:

- modular artifact store loaded as `ymb_delivery_artifacts_v2`;
- worker bootstrap loaded without real network;
- stage failure leaves artifact metadata/chunks empty;
- ordinary small outbox stays textual and performs one provider request in the synthetic harness;
- large outbox path stages the large payload as an artifact instead of inflating the outbox;
- outbox failure cleanup removes artifact state;
- wrong-owner chunk request is rejected before artifact-store access;
- one chunk request performs one indexed record `get` and no `getAll`;
- attachment lifecycle reaches committed -> ready -> send committed -> complete;
- artifact metadata/chunks are deleted after completion.

## Release status

```text
BLOCK1_DEPENDENCY_REGRESSION = PASS
PRODUCTION_BYTES_CHANGED_IN_BLOCK = NO
RELEASE_ALLOWED = NO
```

This PASS is partial evidence only. Later dependency blocks, resource/browser evidence, Patch B and the final pre-delivery gate remain required.
