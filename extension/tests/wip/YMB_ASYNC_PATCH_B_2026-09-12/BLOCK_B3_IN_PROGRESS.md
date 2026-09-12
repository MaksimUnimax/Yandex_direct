# B3 — orchestration continuation checkpoint

Date: 2026-09-12. State: IN PROGRESS. Not an installable release.

Owner authorized continuation with checkpoints during work. Live starting branch HEAD: `5e464f44f7e2990850130cbe62e8b791d54b30dc`. Existing Patch A source is not rewritten. Existing B1 store, B2 protocol and transport are the inputs, not a new implementation from memory.

Local original 0.1.4 ZIP verified in this continuation: SHA-256 `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`, 53 archive files. Baseline SearchProtocol SHA-256: `48cb17f0a846f87e2057d65945dce23788e5c3c90810b7542557d762c2f301b7`.

## Bounded scope

Connect the saved store and transport using an internal runtime with explicit one-item submit/collect, durable command identities, recovery and raw-before-parse handling. Do not enable it in the production manifest or existing UI in this block. Preserve provider/cost and owner admission requirements as explicit injected dependencies. No new provider calls.

## Impact and required assertions

- Store -> atomic settlement, interrupted work, owner checks, duplicate identities; test all touched state transitions.
- Transport -> exactly one admitted fetch, no retry, cancellation/unknown outcome; test together with store.
- Operation response -> preserve immediate result/error and operation ID; no extra paid request or unnecessary GET.
- Raw persistence -> failure must stop progression; parse failure must retain bytes and allow local retry.
- Runtime -> bounded work, no automatic restart execution, no giant returned payload, no accumulated timers.
- Old extension and Patch A -> production files remain byte-identical; integration regression is still required before enabling this runtime.

Browser resource/real IndexedDB evidence remains unproven for Patch B. Previously recorded administrative block is not converted into PASS. No policy bypass, no installable ZIP, no release in this block.

Next durable outputs: exact runtime source, executable tests with raw results and hashes, any minimal store correction with RED/GREEN evidence, updated continuation cursor.
