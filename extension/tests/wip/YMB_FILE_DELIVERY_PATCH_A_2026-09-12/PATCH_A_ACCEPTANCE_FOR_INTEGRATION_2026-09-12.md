# YMB Patch A — acceptance for later integration

Date: 2026-09-12
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Status: **PATCH_A_ACCEPTED_FOR_INTEGRATION / NOT A RELEASE / NO OWNER ZIP**

Patch A is the bounded ChatGPT file-delivery correction built from the exact owner-provided 0.1.4 baseline.

## Accepted evidence

- exact baseline and exact candidate2 SHA manifests preserved;
- exactly 7 production paths changed; 50 other production files remain byte-identical to 0.1.4;
- JS syntax + manifest/package JSON = PASS;
- static negative-regression assertions for 0.1.5 memory anti-pattern = PASS;
- worker bootstrap/load = PASS;
- artifact stage failure cleanup = PASS;
- small legacy text outbox = PASS;
- large outbox artifact staging/compaction = PASS;
- outbox failure cleanup = PASS;
- per-chunk worker contract and no whole-store read = PASS;
- browser worker/content/popup load order = PASS;
- Search Batch local regression = PASS;
- Wordstat Batch local regression = PASS;
- browser occupied-composer preservation = PASS;
- committed recovery no automatic reattach = PASS;
- ready-after-reload fail-closed = PASS;
- multi-file `.txt` + `.csv` attach/send/cleanup = PASS;
- wrong-owner rejection = PASS;
- settings backup/import compatibility = PASS;
- Wordstat/Search/Webmaster/Metrika/Direct credentials preserved = PASS;
- store stress `1/10/32/64/64/64 MB` = PASS;
- browser file memory `1/10/32/64/64/64 MB` = PASS;
- repeated 64 MB cleanup trend = PASS for recorded exact candidate2 bytes;
- candidate2 full SHA manifest after tests = 57/57 PASS.

## Scope boundary

Patch A does **not** contain deferred Search. It is accepted only as a component that may be integrated later with an independently accepted Patch B.

## Verdict

```text
PATCH_A_ACCEPTANCE = PASS
PATCH_A_STATUS = ACCEPTED_FOR_INTEGRATION
PATCH_A_PRODUCTION_RELEASE = NO
OWNER_HANDOFF = FORBIDDEN
DEFERRED_SEARCH_PATCH_B = REQUIRED_SEPARATELY
INTEGRATED_A_PLUS_B_GATE = NOT_RUN
FINAL_PRE_DELIVERY_GATE = NOT_RUN
FRESH_FINAL_PACKAGE = NOT_BUILT
RELEASE_ALLOWED = NO
```
