# YMB 0.1.8 durable deferred Search ownership — feature acceptance

Date: 2026-09-16

Feature branch: `hotfix/ymb-durable-search-job-scope-2026-09-16`
Accepted feature HEAD before merge: `617833e7134062d42a38db2f2393d0cc82f27612`
Base production HEAD: `d5554a3155259b67a8e8a8abef90420ebd29f59e`

## Architectural invariant

Deferred Search job data is owned by the active Search credential scope (`search-folder:<folder_id>`), not by a ChatGPT conversation key. ChatGPT conversation identity remains live execution authority only.

A newly bound ChatGPT dialogue using the same Search `folder_id` can continue the same durable job through status, items page, export, local controls, normalization, submit, collect and interrupted-operation recovery. A different Search folder fails closed through the existing owner/folder guards.

Paused Autorun accounting remains conversation-owned separately through the policy `run_owner` field.

`search_async_export.js` contains no cross-owner recovery or terminal-export bypass; it is the ordinary strict owner-guarded exporter.

Jobs created by the older conversation-owned deferred schema are intentionally not migrated. Recreate them under 0.1.8.

## Feature-branch evidence

GitHub Actions run `35059444571` (`YMB File Delivery P0 Qualification`) on exact HEAD `617833e7134062d42a38db2f2393d0cc82f27612`: SUCCESS.

- preserved async admission/state modules: 254/254 PASS;
- export/file modules: 84/84 PASS;
- durable Search handoff scope: 9/9 PASS;
- candidate full-worker: 100 tests / 94 pass / 6 historical known failures;
- base full-worker: 100 tests / 94 pass / same 6 failures;
- candidate delivery: 41 tests / 36 pass / 5 historical known failures;
- base delivery: 41 tests / 36 pass / same 5 failures;
- `new_full_failures_vs_1adc = []`;
- `new_delivery_failures_vs_1adc = []`;
- differential status: `PASS_NO_NEW_REGRESSION`;
- provider calls: 0;
- production source unchanged by tests.

GitHub Actions run `35059444553` (`YMB verify and package`) on exact same HEAD: SUCCESS.

- production shape/version/permissions: PASS;
- all production JavaScript syntax: PASS;
- legacy exporter + durable-scope regression: PASS;
- deterministic YMB 0.1.8 package build: PASS.

Qualification evidence SHA256 manifest was independently verified after download.
