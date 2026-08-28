# KW-001 / OKNO-MSK — STEP 05 WORDSTAT PASS #2 MANIFEST

Date: 2026-08-28  
Status: **FROZEN / OWNER AUTHORIZED / READY FOR PROVIDER EXECUTION**

This file is job-specific and disposable with the OKNO-MSK workspace.

## 1. Authority

Step-5 pre-step methodology review:

```text
STEP_05_PRE_STEP_REVIEW.md
```

Owner authorization received in chat after explanation of why the original candidate pool was reduced to a bounded second-pass manifest.

No universal KW-001 rule is changed by this manifest.

## 2. Purpose

Run a targeted second Wordstat acquisition pass only for probes expected to add material vocabulary or under-sampled user-job evidence beyond pass #1.

This is acquisition only. It is not final cleanup, clustering, page mapping or SERP validation.

## 3. Frozen provider controls

```text
job_id = kw001-okno-msk-wordstat-pass2-20260828
method = getTop
regions = ["213"]
devices = ["DEVICE_ALL"]
numPhrases = 200
operators = NONE
seed_count = 4
maxRequests = 4
estimated_max_provider_cost_rub = 0.08
```

Do not change the region, device, seed text, order, method or request ceiling during execution without a fresh owner-facing review.

## 4. Frozen probe manifest

### P2-01

```text
phrase = оконная фурнитура
reason = NEW_VOCABULARY
```

Why included:

```text
pass-1 literal seed `аксессуары для пластиковых окон` had root totalCount 29
Wordstat association `оконная фурнитура` had count 1458
```

Uncertainty tested: whether the literal accessory wording under-sampled the actual user vocabulary for fittings/components.

### P2-02

```text
phrase = панорамные окна
reason = NEW_VOCABULARY + DISTINCT_USER_JOB
```

Why included: pass #1 used `французские окна` and surfaced panoramic vocabulary, but the broader panoramic root was not independently sampled.

Uncertainty tested: whether broader panoramic-window wording exposes material application/design/use-case language missed by the French-window root.

### P2-03

```text
phrase = остекление балкона с выносом
reason = KNOWN_SUBFAMILY_GAP
```

Why included: broad balcony acquisition exposed the `с выносом` engineering branch but did not sample it deeply as its own root.

Uncertainty tested: whether this distinct engineering job has meaningful vocabulary around type, price, construction and house-series modifiers below the broad top-200 cutoff.

### P2-04

```text
phrase = окна для частного дома
reason = DISTINCT_USER_JOB
```

Why included: private-house wording appeared incidentally in pass #1 but had no direct broad acquisition seed.

Uncertainty tested: whether private-house demand exposes materially different profile/material/energy/design/price vocabulary from the predominantly apartment-oriented broad roots.

## 5. Explicitly deferred candidates

Do not execute in this pass:

```text
остекление террасы
панорамное остекление балкона
монтаж окон
регулировка окон пвх
москитные сетки на пластиковые окна
окна пвх
стеклопакет
оконный завод
```

Reasons are preserved in `STEP_05_PRE_STEP_REVIEW.md` and include redundancy, ambiguity, unresolved business scope, or a question better answered later by SERP rather than additional Wordstat acquisition.

Deferred does not mean semantically rejected.

## 6. Execution safety

```text
one batch.next <= one provider request
preserve exact provider result provenance
OUTCOME_UNKNOWN = STOP / NO BLIND REPLAY
pre-provider failure with request_executed=false may be repaired/replayed only after local cause is understood
no semantic/page decision during provider acquisition
final durable batch.status required before Step-5 acceptance
```

## 7. Step-5 pass gate

Step 5 can close only when:

```text
frozen 4-probe manifest executed unchanged
region 213 confirmed for every provider item
DEVICE_ALL confirmed for every provider item
all 4 items terminal
failed_terminal recorded if any
outcome_unknown recorded if any
requests_started recorded
estimated cost recorded
raw provider result provenance preserved
final batch.status captured
no final semantic/page decision made inside acquisition
```

Markers:

```text
KW001_OKNO_MSK_STEP05_MANIFEST_FROZEN = true
KW001_OKNO_MSK_STEP05_PROBE_COUNT = 4
KW001_OKNO_MSK_STEP05_PROVIDER_EXECUTION_STARTED = false
KW001_OKNO_MSK_STEP05_COMPLETE = false
```
