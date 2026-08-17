# FSE R9A — Manual apply consistency fault-injection attempt

Date: 2026-08-17
Status: **TEST ERROR — superseded by corrected selective fault injection.**

Purpose: verify that popup/worker cannot claim Manual ON if the content-side `WS_APPLY_MANUAL_MODE` acknowledgement fails.

Initial fault injection incorrectly forced `chrome.tabs.sendMessage` to fail for every tab message. That also broke the earlier `WS_PAGE_CONTEXT` lookup, so the Manual handler never reached `WS_SET_MANUAL_MODE` or `WS_APPLY_MANUAL_MODE`. The resulting assertion therefore tested the wrong stage and is not extension evidence.

Observed runner summary including unchanged popup regressions:

```text
12 tests
11 PASS
1 TEST ERROR
```

No production file was changed. Corrected rerun must allow `WS_PAGE_CONTEXT` normally and fail only the subsequent `WS_APPLY_MANUAL_MODE` delivery/acknowledgement.

No real/external Yandex request occurred.
