# FSE Manual/popup patch R6 — changed-line execution coverage

Date: 2026-08-17
Base candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`
Final revision-2 `popup.js` SHA-256 at this checkpoint: `7286ea024033293110ad10ebc16856de0beacf512f6f86a229ac0271ac20c28c`

Status: **PASS — 56/56 changed nonblank production lines executed, uncovered 0.**

Method:

- exact base `popup.js` from the governed candidate was diffed against the revision-2 patched `popup.js`;
- V8 coverage was collected while the real patched `popup.js` was executed by the popup runtime harness;
- coverage source URL was the production `popup.js` itself;
- every nonblank line on the patched side of every non-equal diff hunk was mapped to an executed V8 range.

```text
changed/new lines including blanks: 61
changed/new nonblank production lines: 56
executed changed nonblank lines: 56
uncovered changed nonblank lines: 0
```

The focused popup execution used for this coverage remained 13/13 PASS.

This supersedes the intermediate revision-1 26/28 coverage checkpoint. The previously uncovered rollback branch was removed by the safer ON content-first / worker-commit-second transaction ordering rather than merely adding a test around an inferior ordering.

No real/external Yandex request occurred.
