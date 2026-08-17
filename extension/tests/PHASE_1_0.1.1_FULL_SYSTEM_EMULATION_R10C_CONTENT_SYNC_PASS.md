# FSE R10C — authoritative Manual state pull/reload reconciliation

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **PASS**.

Corrected targeted test preserved the exact candidate package layout and used the same fake-style contract as the package's existing content tests.

Input 1 — content startup/content-ready with authoritative worker state:

```text
WS_CONTENT_READY → ok:true, manual_mode:true, matching conversation_key
```

Actual:

```text
content manualEnabled: true
eligible local Copy background-color: rgba(255, 204, 0, 0.22)
observer/decorate startup path active
```

Input 2 — subsequent authoritative resync:

```text
WS_CONTENT_READY → ok:true, manual_mode:false, same conversation_key
```

Actual:

```text
content manualEnabled: false
yellow Copy decoration removed
manual observer stopped
```

Conclusion:

- the content script can correctly reconcile authoritative persisted Manual state when it performs its `WS_CONTENT_READY`/`syncAllState` pull path;
- the R9B/R9C/R9D defect is therefore narrowed to the popup's immediate push/acknowledgement path after `WS_SET_MANUAL_MODE`, not to the content script's authoritative pull/reload reconciliation mechanism;
- together with R10B worker hard-gate PASS, stale content after a failed OFF push cannot cross the API boundary, and a later successful content sync repairs the stale visual/listener state.

No production patch was made. No real/external Yandex request occurred.
