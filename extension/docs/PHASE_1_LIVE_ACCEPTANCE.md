# PHASE 1 — CONTROLLED LIVE ACCEPTANCE

Date: 2026-08-12
Product: `Yandex Marketing Bridge — ChatGPT ↔ Yandex`
Candidate version: `0.1.0`
Status before this procedure: PRE-LIVE PASS / PRODUCTION CHATGPT LIVE PENDING

## Authority artifact

Exact candidate ZIP:

```text
yandex-marketing-bridge-0.1.0-phase1-wordstat-candidate.zip
SHA-256 79c2bca5e2e65aaa1cb7cc38754589a0bf3b0b436c82f36416934cd175cafa2a
```

Do not substitute another rebuilt ZIP without generating new test evidence and a new hash.

## Purpose

This gate proves behavior that static/Node/Chromium-mock testing cannot prove:

- current production ChatGPT DOM;
- real local Copy ownership;
- real composer/send behavior;
- current user's Chrome timing;
- real Yandex Wordstat authorization/network path;
- actual operator UI usability;
- real ChatGPT → GitHub paid-evidence persistence workflow.

Search/Webmaster/Metrika/Direct development remains blocked until this gate passes.

## Required setup

1. Extract the exact candidate ZIP to a permanent local folder.
2. Open `chrome://extensions`.
3. Enable Developer mode.
4. Load the extracted candidate as unpacked extension.
5. Open a dedicated production ChatGPT conversation for this acceptance.
6. Open the extension popup.
7. Verify product/version visibly correspond to Yandex Marketing Bridge `0.1.0`.
8. Bind the current confirmed ChatGPT conversation explicitly.
9. Set a dedicated Job ID, recommended:

```text
acceptance-wordstat-0.1.0
```

10. Active service must be:

```text
wordstat
```

No other service must be selectable/executable in Phase 1.

## Gate A — missing credentials must not stop the run

Purpose: prove the owner's requirement that unavailable service credentials produce controlled SKIP, not a broken Job.

1. Ensure Wordstat API key is absent from extension storage for this subtest.
2. Keep the Job ID and bound conversation.
3. Enable Wordstat Autorun in operator policy with small hard limits.
4. Start Autorun.
5. Allow one valid Wordstat command to be emitted by ChatGPT.
6. Expected result:

```text
WORDSTAT_RESULT_V1
status = SKIPPED
reason = NO_CREDENTIALS
service = wordstat
job_id = acceptance-wordstat-0.1.0
run_id = <non-empty>
```

7. There must be **zero Yandex network initiation** for this command.
8. Run must remain controlled; Pause/Finish must still work.

No paid query is needed for Gate A.

## Gate B — operator-disabled Autorun

Purpose: prove credential presence does not imply autorun permission.

1. Finish any previous run.
2. Disable Wordstat Autorun in popup policy.
3. Attempt Start.
4. Expected: Start is refused before composer staging/API activity with an operator-visible policy reason.
5. Re-enable Autorun only for the remaining acceptance tests.

## Gate C — hard request/cost limits

Purpose: prove ChatGPT cannot override operator policy.

1. Configure a deliberately restrictive request or cost ceiling that would reject the next paid Wordstat operation.
2. Start a new Wordstat run.
3. ChatGPT may emit a valid Wordstat command.
4. Expected:

```text
status = SKIPPED
reason = REQUEST_LIMIT | COST_LIMIT | JOB_REQUEST_LIMIT | JOB_COST_LIMIT
```

5. There must be zero Yandex network initiation for the blocked command.
6. Changing numbers in assistant text must not change popup/operator policy.

Do not use an actual paid request merely to test the blocked path.

## Gate D — real free Wordstat request

Before any executable Wordstat command, ChatGPT must follow the existing working contract:

1. check current official Yandex Search API / Wordstat pricing on the official source;
2. explain the method, parameters and expected cost;
3. only then emit the executable command.

For the free-path network test, use the currently documented free Wordstat region-tree operation if official documentation still confirms it is free at test time.

Expected:

- exactly one real Yandex request;
- one `WORDSTAT_RESULT_V1`;
- `bridge = yandex-marketing-bridge`;
- `version = 0.1.0`;
- `service = wordstat`;
- correct Job ID and Run ID;
- no credential material in the result;
- after confirmed delivery, Autorun returns to waiting for the next command.

If the operation is no longer free according to current official pricing, do not assume the old price; update operator tariff policy and acceptance plan before execution.

## Gate E — one minimal paid Wordstat request

This is the only intentionally paid request required by the Phase 1 live gate.

Immediately before the command:

1. ChatGPT checks the **current official Wordstat tariff** on the official Yandex source;
2. ChatGPT states exact method/phrase/region/device/result-count parameters;
3. ChatGPT states estimated cost of this one initiation;
4. operator verifies popup request/cost ceilings allow exactly the intended request with safe remaining headroom.

Then execute one small useful `getTop` request.

Expected:

- exactly one paid Yandex initiation;
- no duplicate on double DOM events/duplicate tabs;
- one result delivery;
- correct `0.1.0` version provenance;
- `job_id`, `run_id`, method and cost estimate present;
- result usable by ChatGPT.

Do **not** repeat the request if browser/service-worker state becomes ambiguous after initiation. Preserve the reference `REQUEST_OUTCOME_UNKNOWN_NO_RETRY` rule.

## Gate F — immediate GitHub persistence of paid evidence

After Gate E result reaches ChatGPT and before intentionally collecting another paid result:

1. create/ensure:

```text
work/acceptance-wordstat-0.1.0/
```

2. persist the exact raw `WORDSTAT_RESULT_V1` under:

```text
work/acceptance-wordstat-0.1.0/raw/wordstat/
```

3. persist a run/cost record under:

```text
work/acceptance-wordstat-0.1.0/logs/runs/
work/acceptance-wordstat-0.1.0/logs/cost-ledger/
```

4. commit to GitHub;
5. verify the committed raw evidence can be fetched in a fresh ChatGPT context/after reload without repeating the paid Wordstat request.

This proves the owner's paid-evidence durability requirement.

## Gate G — Manual cost guard

Purpose: prove operator cannot bypass Job limits by switching from Autorun to Manual.

1. Finish/Pause Autorun according to normal mutual-exclusion rules.
2. Configure Job cost/request ceiling so another paid operation would exceed it.
3. Enable Manual mode.
4. Click local Copy on a valid paid Wordstat command.
5. Expected: durable `SKIPPED` result with Job-limit reason and **zero Yandex fetch**.
6. Restore policy only if a further intentional test is needed.

## Gate H — lifecycle and ownership

Verify in production ChatGPT:

- Pause from waiting state;
- Resume with fresh assistant baseline;
- Finish;
- duplicate tab cannot steal active owner;
- another ChatGPT conversation cannot execute this run;
- changing Job/service while run is active is blocked;
- generic `Copy response` never triggers Wordstat;
- non-Wordstat block local Copy performs ordinary copy only;
- occupied composer is never silently overwritten.

## PASS criteria

Phase 1 may be marked LIVE PASS only if all applicable gates above are confirmed and evidence is committed.

Minimum success chain:

```text
bind conversation
→ bind Job ID
→ missing-credential SKIP with zero fetch
→ operator-disabled/cost-limit guard with zero fetch
→ real free network request exactly once
→ one real paid request exactly once
→ result provenance 0.1.0 + Job/Run correct
→ paid raw evidence committed to GitHub
→ Pause/Resume/Finish/ownership controls PASS
```

## Failure / rollback

If any live path is ambiguous:

1. Pause/Finish if safe.
2. Do not repeat a paid operation whose initiation outcome is unknown.
3. Preserve diagnostic/result evidence.
4. Disable the candidate if necessary.
5. Append the observed failure to `DEVELOPMENT_CONTEXT_APPEND_ONLY.md`.
6. Fix under a new candidate artifact/hash.
7. Re-run source + exact ZIP gates before another live attempt.

## Gate status

At document creation:

```text
PHASE 1 PRE-LIVE: PASS
PHASE 1 PRODUCTION LIVE: PENDING OPERATOR TEST
PHASE 2 SEARCH: BLOCKED
```
