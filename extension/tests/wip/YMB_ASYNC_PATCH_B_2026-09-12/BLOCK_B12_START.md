# B12 — final contract, permission and acceptance-coverage reconciliation

Date: 2026-09-12. Live input HEAD: `f52da796ca399c53c012902f04f49632d2ab6600`.

The current cursor and mandatory patch/resource plus full pre-delivery rules were read. Exact owner014 ZIP was verified: `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`. Saved B11 was recovered through the existing read-only Actions snapshot; 138 files matched Git blob identity. Saved materializers restored B9/B10/B11 because those directories were absent, not because the product was being rewritten. B11 target tree: `5fd8a55e980fa54fe5371a51070e9e899307319c8f1ee3255fdc0857b31ebd26`, 67 files.

## Bounded work

1. Check every public async action/alias against actual protocol, full worker and saved state behavior.
2. Re-read official Yandex query/result/grouping/Operation limits and Chrome permission documentation. Do not invent an undocumented server tokenizer, fixed retention expiry timestamp or guarantee of result count.
3. Exercise available boundary/permission tests without real network. If existing code already enforces a requirement, test it rather than duplicating the validator.
4. Write an honest capability contract separating current fail-closed WIP permissions, target provider behavior and local project limits.
5. Map PD-00..PD-17 and resource gates to executable evidence and explicit missing coverage. This block is NOT the independent Codex pre-delivery campaign.
6. Persist code if a proved defect needs fixing, plus tests/raw logs/results/cursor before proceeding.

## Protected behavior and dependencies

Baseline Search validator, normalizer, original sync/batch semantics, credentials Check, costs, per-item persistence, Manual ownership, Patch A binary/chunk delivery and existing manifest permissions stay unchanged unless a specific defect is demonstrated. If production changes, retest all affected callers. No scope expansion into other products or Kwork job data.

## Initial verified finding

The inherited `shared/search_protocol.js` already checks 400 Unicode code points and 40 whitespace-separated tokens. Do not claim that word-count validation is absent. GroupSpec allows 100 groups and 3 documents, but the service separately states no more than 250 returned results. Do not turn that into a promise of 300 results or silently change valid grouping parameters.

RELEASE_ALLOWED = NO
PROVIDER_CALLS = 0
BROWSER_TESTS = NOT_RUN
CURRENT_ACTION = executable contract and coverage audit
