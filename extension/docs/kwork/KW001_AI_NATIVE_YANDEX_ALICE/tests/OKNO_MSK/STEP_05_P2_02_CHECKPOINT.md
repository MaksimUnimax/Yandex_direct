# KW-001 / OKNO-MSK — STEP 05 P2-02 CHECKPOINT

Date: 2026-08-29  
Status: **SUCCEEDED / ACQUISITION EVIDENCE ONLY**

```text
job_id = kw001-okno-msk-wordstat-pass2-20260828
probe_id = P2-02
phrase = панорамные окна
method = getTop
regions = ["213"]
devices = ["DEVICE_ALL"]
numPhrases = 200
request_id = wordstat-batch-81c075ea-01bb-4ab0-83f3-c94f58041afe
http_status = 200
elapsed_ms = 737
request_executed = true
estimated_cost_rub = 0.02
item_status = SUCCEEDED
root_totalCount = 9273
```

Batch checkpoint after P2-02:

```text
total = 4
pending = 2
succeeded = 2
failed_terminal = 0
outcome_unknown = 0
terminal = 2
requests_started = 2
estimated_cost_rub = 0.04
next_safe_action = CLAIM_NEXT
```

## Acquisition observations

The probe added material vocabulary beyond the earlier `французские окна` seed.

Observed branches include:

```text
private / country house
apartment / residential-complex noise and adjacent real-estate intent
Moscow commercial purchase / price / turnkey / order
floor-to-ceiling / sliding / aluminium / plastic / corner / door combinations
balcony / loggia / terrace / veranda use cases
heating / convectors / dimensions / installation / insulation
```

Selected measured examples preserved from the provider response:

```text
панорамные окна = 9273
дом с панорамными окнами = 1103
квартира с панорамными окнами = 544
панорамные окна москва = 510
панорамные окна купить = 498
панорамные окна цена = 479
панорамные окна для загородного дома = 206
панорамные окна в частном доме = 162
панорамные окна на балконе = 140
раздвижные панорамные окна = 117
панорамные алюминиевые окна = 106
панорамные окна под ключ = 78
панорамные пластиковые окна = 77
установка панорамного окна = 69
панорамные окна на лоджии = 38
заказать панорамное окно = 38
```

Associations observed include:

```text
панорамное остекление = 1382
витражное остекление = 405
панорамное остекление балкона = 262
безрамочное остекление = 78
```

These associations remain vocabulary/acquisition evidence only. They are not automatically accepted keywords, new seeds, clusters or page decisions.

No cleanup, clustering, SERP or page-mapping decision is made in this checkpoint.
