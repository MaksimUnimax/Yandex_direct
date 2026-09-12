# YMB Patch A — browser recovery / owner-isolation block 3

Date: 2026-09-12
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Candidate: exact candidate2; production bytes unchanged during this block.
Browser: Chrome/Chromium 144 controlled QA profile.
Real provider traffic: 0.

## Harness correction

The first attempt reused assertions from an older integrated candidate and expected symbols/state helpers not present in candidate2 (`attachment_claimed`, `patchOutboxEntry`, old file-delivery global names).

This was classified as `FAIL_HARNESS`, not product failure. Production was not edited. A candidate2-specific browser harness was written against the actual public/current worker contract and the entire block was rerun from the beginning.

## Final results

```text
small_text_legacy_path = PASS
text_file_threshold = PASS
occupied_composer_no_commit = PASS
committed_recovery_no_reattach = PASS
ready_reload_fail_closed = PASS
multi_file_attach_send_cleanup = PASS
wrong_owner_rejected = PASS
BLOCK3_BROWSER_RECOVERY_OWNER_ISOLATION = PASS
```

## Important assertions

- ordinary 100k-character text still uses the legacy text send path, with no file mutation;
- exact ChatGPT threshold remains 1,048,000 Unicode characters: threshold stays text, threshold+1 stages an attachment;
- occupied composer preserves user draft, does not attach, does not commit and does not click Send;
- worker-committed attachment with no existing DOM preview is not automatically reattached and not sent;
- an `attachment_ready` delivery whose preview disappears after page reload fails closed and does not send a file-less marker;
- two governed artifacts (`one.txt` and `two.csv`) attach together in one file set, produce one Send click, and are removed from IndexedDB after completion;
- wrong-owner delivery is rejected with `AUTO_NON_OWNER_TAB`;
- Chromium managed-policy bytes were restored exactly after the run.

## Release status

```text
BLOCK3 = PASS
PRODUCTION_BYTES_CHANGED_IN_BLOCK = NO
RELEASE_ALLOWED = NO
```

This is partial Patch-A evidence. Remaining shared-service regressions / exact candidate gate still apply.
