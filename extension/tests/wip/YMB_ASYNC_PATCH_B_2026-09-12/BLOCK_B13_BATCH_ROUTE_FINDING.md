# B13 — actual batch caller bypasses unified Wordstat provider

Date: 2026-09-12. Product under inspection: exact B12 and original owner014. Both fail the same two complete-worker assertions.

The live Wordstat batch adapter (`wordstat_batch_worker_transport.js`, not the unused similarly named integration module) calls `executeWordstatCommand` directly. That is the legacy Phase-2 provider, which reads legacy settings.apiKey/settings.folderId. The accepted later `webmaster_worker_runtime.js` replaces `executeServiceCommand` with the unified provider but does not replace this direct legacy function.

Consequences reproduced with synthetic credentials/fetch:

1. A saved dedicated Wordstat credential without the old wsmb keys passes the capability check but batch then fails API_KEY_MISSING before fetch.
2. When a different obsolete legacy cloud key also exists, batch actually sends that obsolete key/folder instead of the current dedicated Wordstat credential. The test captures only synthetic keys; no real credentials or external requests are used.

The exact two assertions fail on untouched owner014 too (0/2), so this is an inherited route defect, not an async-patch regression or RAM reproduction. It also means that testing the new response guard only through ordinary Manual/Check misses the real batch caller.

Bounded scope extension: change the single actual batch call to `executeServiceCommand(WORDSTAT, command, metadata)` so it uses the same current credentials/provider/error handling as ordinary Wordstat. Retain existing batch admission, pre-request checkpoint, price checks, counters, request IDs, metadata, ownership and no-retry model. No new provider implementation or fallback credential path is introduced. Required regression includes full Wordstat batch Manual and Autorun, malformed/success/error outcomes, all existing original suites and shared Search/service regressions.

A separate test-draft error was found: searching the whole JSON error report for the strings 'null' or 'true' incorrectly treated legitimate metadata as raw response leakage. Those two test assertions were corrected to check the exact fixed safe error message. The prior failing draft log is preserved, not counted as product failure.

This checkpoint precedes the single-line batch routing edit. The separate Wordstat response-envelope guard is already local; no installable archive has been produced. RELEASE_ALLOWED = NO.
