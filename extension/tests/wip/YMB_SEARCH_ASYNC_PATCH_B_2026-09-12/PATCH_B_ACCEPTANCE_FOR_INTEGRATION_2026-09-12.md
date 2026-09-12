# YMB Deferred Search Patch B — acceptance for later integration

Date: 2026-09-12
Branch: `wip/ymb-search-async-patch-b-2026-09-12`
Status: **PATCH_B_ACCEPTED_FOR_INTEGRATION / NOT A RELEASE / NO OWNER ZIP**

Patch B is the bounded deferred ordinary Yandex Search correction built independently from the exact owner-provided 0.1.4 baseline.

## Accepted evidence

- exact 0.1.4 baseline identity preserved;
- exactly 8 Patch-B production paths differ from baseline;
- standalone Patch-B protocol/runtime/state/recovery tests = PASS;
- 1500 command contract and 1501 rejection = PASS;
- no giant mutable item list in job record = PASS;
- provider operation IDs persisted per item = PASS;
- stale/unknown submit outcome blocks blind replay = PASS;
- malformed provider XML fails closed = PASS;
- pause/cancel/expiry semantics = PASS;
- Node scale `10/100/500/1500` = PASS;
- browser IndexedDB 1500 submit/collect across fresh MV3/browser lifecycles = PASS;
- final browser state `COMPLETED / SUCCEEDED=1500` = PASS;
- no submit replay across restart = PASS;
- submit/collect bounded pacing = PASS;
- cost/admission reservation and rollback = PASS;
- exact async submit/Operation provider hosts, methods and Api-Key auth = PASS;
- ordinary sync Search endpoint remains `/v2/web/search` = PASS;
- global policy blocks before second fetch = PASS;
- async Autorun is locally rejected in standalone Patch B = PASS;
- wrapper-chain delegation for ordinary Search, Search Batch and Wordstat Batch = PASS;
- wrong-service/manual-disabled async requests remain local = PASS;
- settings backup/import does not serialize or erase async IndexedDB state = PASS;
- content isolated-world recognition = PASS;
- popup and all five existing service protocol/runtime surfaces load = PASS;
- full candidate identity `59/59 SHA` = PASS;
- JavaScript syntax `53/53` = PASS;
- durable WIP postimage transport remote readback `6/6` = PASS.

## Scope boundary

Standalone Patch B intentionally does not implement large-file export. Export/delivery of large async result sets belongs to the A+B integration, where the already accepted Patch-A bounded IndexedDB file-delivery contour must be reused rather than another transport invented.

## Verdict

```text
PATCH_B_ACCEPTANCE = PASS
PATCH_B_STATUS = ACCEPTED_FOR_INTEGRATION
PATCH_B_PRODUCTION_RELEASE = NO
OWNER_HANDOFF = FORBIDDEN
PATCH_A_PLUS_B_INTEGRATION = REQUIRED
FINAL_CROSS_LAYER_RESOURCE_GATE = NOT_RUN
FINAL_PRE_DELIVERY_GATE = NOT_RUN
FRESH_FINAL_PACKAGE = NOT_BUILT
RELEASE_ALLOWED = NO
```
