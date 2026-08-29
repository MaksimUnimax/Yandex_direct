# KW-001 / OKNO-MSK — STEP 05 P2-03 CHECKPOINT

Date: 2026-08-29
Status: **SUCCEEDED / PROVIDER EVIDENCE PRESERVED**

Job:

```text
job_id = kw001-okno-msk-wordstat-pass2-20260828
probe_id = P2-03
phrase = остекление балкона с выносом
method = getTop
regions = ["213"]
devices = ["DEVICE_ALL"]
numPhrases = 200
```

Provider truth:

```text
request_id = wordstat-batch-d6dd358c-4a35-4387-a0ac-a1053dd87238
status = SUCCEEDED
http_status = 200
request_executed = true
automatic_retry = false
elapsed_ms = 459
estimated_cost_rub = 0.02
root_totalCount = 95
```

Direct returned results were sparse but valid. The returned result family contained 5 direct phrases, including:

```text
остекление балкона с выносом = 95
остекление балкона с выносом подоконника = 20
остекление балкона в москве с выносом = 13
сварка выноса на балконе с последующим остеклением = 11
вынос на балконе с остеклением providal = 5
```

Interpretation at acquisition stage only:

```text
the subfamily is real but lexically narrow in this probe;
P2-03 did not expose a large new direct-query universe;
associations are mostly adjacent/noisy and are not promoted automatically;
no page/cluster decision is made here;
no further Wordstat expansion is justified solely from this result.
```

Batch progress after P2-03:

```text
total = 4
pending = 1
succeeded = 3
failed_terminal = 0
outcome_unknown = 0
requests_started = 3
estimated_cost_rub = 0.06
next_safe_action = CLAIM_NEXT
```
