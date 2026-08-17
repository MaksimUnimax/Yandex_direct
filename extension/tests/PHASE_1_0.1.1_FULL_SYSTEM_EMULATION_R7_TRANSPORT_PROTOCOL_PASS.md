# FSE R7 — transport / protocol / policy / envelope / security regression

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **PASS — 76/76**.

```text
76 tests
76 PASS
0 FAIL
```

Covered:

- exact Cyrillic/Unicode phrases preserved in UTF-8 JSON body and never placed in HTTP headers;
- invalid API keys containing Cyrillic, NBSP, zero-width characters, smart quotes, newlines or spaces rejected before fetch;
- settings save rejects invalid key and accepts ordinary ASCII key;
- all four Wordstat methods preserve Unicode phrase/body where applicable;
- exact product version and reference provenance checks;
- Phase-1 router exposes only Wordstat and future prefixes do not dispatch;
- no runtime Job/GitHub coupling;
- credential/operator-policy/request-limit/cost-limit separation;
- Autorun start without credentials remains possible but execution yields safe zero-fetch skip;
- missing credentials, disabled Autorun, request ceiling and cost ceiling all stop before fetch;
- paid allowed Manual/Autorun requests cross the mocked fetch boundary exactly once;
- active-service context immutable during RUN;
- paused RUN budget cannot be bypassed by Manual;
- export checksum/tamper/import/active-RUN preservation;
- Debug OFF compact error vs Debug ON additional redacted diagnostics;
- durable error claim → commit → confirm; duplicate commit has no second Send grant;
- recoverable Autorun error returns to waiting without blind retry;
- Test Connection missing credential: zero fetch + chat error;
- invalid-key Manual: one error queue, zero fetch;
- HTTP 403 Manual and HTTP 429 Autorun: one mocked fetch, error result, no retry;
- pending error recovery exposed through content-ready without Yandex replay;
- runtime Export/Import API and wrong-format rejection;
- PR-02 selective immediate toggle persistence without committing text/credentials;
- PR-04/PR-05 free-call `charged:false` and successful `request_executed:true`;
- PR-06 already-executed Manual result preserved across pre-commit delivery failure and post-commit replay fenced;
- protocol malformed JSON/prefix/method/phrase/date/device/region/size boundaries;
- folderId cannot be supplied by assistant command;
- result formatter does not invent credentials;
- deterministic command fingerprint;
- Auto Send remains Manual-only;
- optional Send/Copy picker/profile loading and permissions/recovery handshake source contracts.

No real/external Yandex request occurred; transport counts belong to controlled mocked fetch boundaries.
