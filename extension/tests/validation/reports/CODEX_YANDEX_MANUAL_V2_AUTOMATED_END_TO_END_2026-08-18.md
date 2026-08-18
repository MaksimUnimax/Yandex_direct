# CODEX_YANDEX_MANUAL_V2_AUTOMATED_END_TO_END

Date: 2026-08-18  
Verdict: `AUTOMATED_CONTROLLED_PASS`

The bounded external adapter was corrected and the synthetic end-to-end run completed on Chrome for Testing 151.0.7922.47 with Puppeteer 25.4.0. The MV3 worker installed and the popup bound to the canonical synthetic conversation identity while the visible URL remained `/c/yandex-qa-manual-v2`.

Manual surface results:

- OFF converged to 0 decorated buttons.
- ON converged to 7/7 eligible local PRE/CodeMirror Copy buttons decorated yellow with an explicit `Яндекс` label.
- Generic whole-response Copy was excluded.
- Ambiguous local Copy locality failed closed with `LOCAL_COPY_AMBIGUOUS_INSIDE_ROOT`.
- A dynamically appended block was decorated by the observer.
- OFF restored the surface to zero; re-enable restored 7 authored decorations plus the dynamic block.

The representative click matrix covered an ordinary block, an explicit double-click probe, generic whole-response Copy, and ambiguous local Copy. Diagnostics reached `MANUAL_OPERATION_COMPLETED`; the fixture’s send lifecycle was made realistic so the worker could observe composer emptying and user-turn confirmation. Provider traffic remained zero.

Production source was not changed. The exact authority SHA and origin/main are `3ceb9607c8b35da3204db4182ea1599c15f2b111`; the final source suite passed 358/358 and the five audited source hashes remained unchanged. The adapter regression test passed 2/2.

No GitHub branch or commit was created. Real current-Chrome K-02 and live Phase-1 Yandex search were not run; the latter remains blocked by the no-real-request/no-credential boundary.
