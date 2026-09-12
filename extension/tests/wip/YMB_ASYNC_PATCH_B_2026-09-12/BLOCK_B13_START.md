# B13 — original extension suite inventory and feasible missing coverage

Started 2026-09-12 from live WIP HEAD `1aafee85d8534ab08848c217efa517a8a2cbec23`. The B12 continuation is the input, not a new patch project.

Exact owner014 ZIP is present in this session: 159963 bytes, SHA-256 `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`. Ready B12 directories are not present; reconstruct with preserved scripts, not manual rewriting. Expected B12 tree: `73e6ed85bfd843bf2590a2d1a44a9d04224ce5f63563d127bcd35c2ad092eeec`, 67 files.

Use the existing read-only source snapshot workflow to retrieve the complete original extension/tests inventory, source/reference fixtures and documentation at that exact ref. Archive creation is transport only, not test evidence or a release.

## Work now

1. Inventory every tracked original test/harness file, separate WIP patch tests from original extension tests, inspect executable entry points and dependencies before running.
2. Read the full PD-00..PD-17 gate, B12 coverage map, resource rule and saved successful harness evidence.
3. Run only safely executable original suites on exact B12 bytes with bounded time/resources and zero real provider traffic. Do not execute browser/profile or live-provider scripts blindly.
4. Keep product assertions intact; classify old test/fixture incompatibility separately from product failure. A product finding must be reproduced and recorded before any fix; no silent product changes during the frozen inspection.
5. Persist inventory, runner, complete logs, classifications, report and cursor during work. Unavailable Chrome/DOM/real-IDB checks remain open without repeated blocked launches.

Production changes in this start checkpoint: 0. New provider calls: 0. Installable ZIP: not created.
RELEASE_ALLOWED = NO.
