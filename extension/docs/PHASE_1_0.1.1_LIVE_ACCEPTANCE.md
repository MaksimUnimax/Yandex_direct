# PHASE 1 — 0.1.1 PRODUCTION LIVE ACCEPTANCE

Status: mandatory owner Chrome/current production ChatGPT gate.
Date: 2026-08-12.

Exact candidate:

```text
yandex-marketing-bridge-0.1.1-phase1-repair-candidate.zip
SHA-256 311353e2671052b7170e12db3e1318dfed4f59ccf945c7eda6ec59152ee3abfb
```

Search remains blocked until this procedure passes.

## 1. Installation / migration

Preferred in-place upgrade test:

1. Export settings from the currently installed old extension if available.
2. Keep the secret JSON private; do not commit it.
3. Replace files in the same unpacked folder with 0.1.1 and Reload, or load 0.1.1 from a new folder.
4. Verify popup shows `0.1.1`.
5. If same-folder upgrade: verify existing Wordstat key/folder settings remain present.
6. If new-folder installation: use Import settings and verify checksum/import succeeds.
7. Verify import does not alter a deliberately active safety RUN if testing that branch.

## 2. Conversation binding

Bind exactly the current ChatGPT conversation.

Verify another conversation/duplicate tab cannot take ownership or execute the same operation without proper binding/owner semantics.

## 3. Debug OFF mandatory error delivery

Keep Debug Mode OFF.

Trigger a zero-network error, preferably a validation/missing-credential path.

Expected:

```text
local visible error/toast
→ YMB_ERROR_V1 automatically arrives in this ChatGPT conversation
→ no credential secret in text
→ no unintended Yandex fetch
```

The operator must not need to open diagnostics or manually copy logs for the error to reach ChatGPT.

## 4. Debug ON additional logs

Enable Debug Mode and trigger another safe zero-network error.

Expected:

```text
YMB_ERROR_V1 automatically arrives
+ debug_logs present
```

Verify no API key, Authorization header or credential secret is present.

Debug Mode must not change whether an error is delivered; only detail level changes.

## 5. Recoverable Autorun continuation

Start Wordstat Autorun with valid conversation binding and policy.

Trigger a recoverable validation/watcher/policy error.

Expected:

```text
error → automatically delivered to ChatGPT
→ RUN remains controlled
→ returns to waiting for next command when safe
```

No silent terminal stop.

## 6. Free real Wordstat path

Immediately before issuing the command, ChatGPT must freshly verify the official Yandex Wordstat tariff.

Use `getRegionsTree` only if the official current pricing still marks it non-billable.

Expected sequence:

```text
ChatGPT explains method/current cost
→ WORDSTAT_API_V1 block
→ local request-start feedback
→ exactly one Yandex request
→ response feedback
→ WORDSTAT_RESULT_V1 delivered to this conversation
```

Verify:

- bridge/version = yandex-marketing-bridge / 0.1.1;
- service = wordstat;
- operation = getRegionsTree;
- no `job_id` field;
- no secret credential;
- no duplicate request/delivery.

## 7. HTTP error path

Use a safe account/access condition if available or a controlled test route.

For a real HTTP 4xx/429 response from one request:

- deliver the ERROR result/evidence to ChatGPT;
- do not automatically repeat the request;
- Autorun should remain controllable and continue when safe.

## 8. Pause / Manual shared budget

Configure a restrictive RUN cost/request limit.

Start Autorun and Pause it.

Use Manual Copy for a command that would exceed the remaining RUN budget.

Expected:

```text
SKIPPED / COST_LIMIT or REQUEST_LIMIT
zero Yandex request
same run_id / RUN accounting
```

Manual must not bypass the paused RUN ceiling.

## 9. Unknown request outcome no-retry

This test should be performed only with a safe emulator/fault injection unless the operator explicitly accepts the risk.

Simulate service-worker loss during REQUESTING after the irreversible boundary.

Expected:

```text
YMB_ERROR_V1
request_executed = UNKNOWN
automatic_retry = false
```

The identical command is fenced; no blind repeat.

## 10. Export / Import end-to-end

Export settings from one installation identity.

Verify the file explicitly warns/behaves as secret-bearing.

Load another unpacked installation identity and Import.

Expected:

- checksum accepted for untouched backup;
- credentials/settings restored;
- tampered JSON rejected;
- no secret appears in ChatGPT/GitHub;
- active execution state from the backup is not imported.

## 11. One minimal paid Wordstat request

Only after all previous gates pass:

1. freshly check current official Yandex pricing immediately before the command;
2. choose one minimal paid method/phrase/result count;
3. state exact estimated cost;
4. verify RUN limit has room;
5. issue exactly one command;
6. no retry if outcome becomes ambiguous.

## 12. Acceptance verdict

PASS only if all required live paths above succeed in the owner's real Chrome/current production ChatGPT.

After PASS:

- append live evidence to the append-only context chain;
- update ROADMAP Phase 1 to LIVE PASS;
- only then unlock Phase 2 Search.
