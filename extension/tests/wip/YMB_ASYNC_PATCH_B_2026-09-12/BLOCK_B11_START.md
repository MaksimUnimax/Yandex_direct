# B11 — local repair and remaining invocation faults

Date: 2026-09-12. Live initial HEAD: `242f9e0f5133d4bf2e09059fe30d4aeb9cd72fc1`.
Status: IN_PROGRESS. RELEASE_ALLOWED = NO.

The existing source-snapshot workflow was reused, read-only, at the exact B10 ref. 124 saved files were checked against Git blob hashes. Exact owner014 ZIP SHA-256 is `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f` (53 files). The saved materializers restored B9 then B10 because those directories were absent in this runtime; no component was reimplemented. B10 tree: `191b3ed1222733cb9d3aed805b53084829740d10ad906c5246d2cf185fc9ae94`, 67 files.

Read current cursor, mandatory dependency/resource rule, pre-delivery gate and actual B10 invocation code/tests. Historical results remain attached to their exact targets, not relabelled as newly executed.

## Bounded scope

1. Add one explicit local-only normalizeSaved command for one preserved item. Reuse the existing runtime normalizer; no new POST/GET, no provider retry, no raw replacement from chat, no budget reset. Repeated successful normalization must be idempotent. Invalid/missing/cross-owner items and continued parse errors must fail honestly, preserving raw evidence.
2. Exercise full existing Search batch/Check failures with controlled network/storage fixtures, especially receipt/outcome truth, partial results and stop-required propagation. Change only dependencies for reproduced defects.
3. Reconcile final advertised provider request limits separately; do not enable the operation host or claim live auth proof merely to make synthetic tests pass.

## Required dependency evidence

- Async protocol -> Manual ingress -> actual store/runtime/normalizer -> existing outbox: local reparse scenarios, input boundaries, ownership, duplicate and error delivery.
- Legacy batch -> shared admission -> provider -> batch state/report/Autorun: injected admission/settlement/provider faults, partial progress, no hidden repeat.
- Check -> credential registry/provider admission: explicit consent, denied admission, HTTP/network failure and secret containment.
- Rerun impacted existing full-worker/module/export tests on final bytes; record syntax/tree identity.
- No new browser launch while known policy blocker remains, no policy bypass, no real credentials or provider calls. Node evidence is not Chrome/real-IDB/resource acceptance.

Persist source/test/evidence and cursor after each material block. Do not issue an installable ZIP.
