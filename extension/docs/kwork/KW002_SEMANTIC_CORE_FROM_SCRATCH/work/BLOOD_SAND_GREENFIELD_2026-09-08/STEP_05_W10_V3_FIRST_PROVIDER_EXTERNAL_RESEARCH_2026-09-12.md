# Step05 W10 V3 — fresh provider source trace

Date: 2026-09-12
Status: PASS FOR GATE PREPARATION / NO PROVIDER CALL
Base HEAD: `f8306e84c612f96d74a639f5f130a1f1d4376b4e`
Candidate: `W10C001`.

## Official provider facts rechecked

Sources:
- https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop
- https://aistudio.yandex.ru/ru/docs/search-api/operations/wordstat-gettop
- https://aistudio.yandex.ru/ru/docs/search-api/concepts/limits
- https://aistudio.yandex.ru/ru/docs/search-api/pricing
- https://aistudio.yandex.ru/ru/docs/search-api/reference/regions
- https://aistudio.yandex.ru/en/docs/search-api/operations/wordstat-getregiontree
- https://yandex.com/support2/wordstat/en/content/operators

Current facts:
```text
GETTOP_ENDPOINT = /v2/wordstat/topRequests
EVIDENCE_WINDOW = last 30 days
NUM_PHRASES = 1..2000
PHRASE_MAX_LENGTH = 400
REGIONS_MAX = 100
DEVICES_MAX = 3
DEVICE_ALL = supported
REGION_225 = Russia
WORDSTAT_QUOTA = 10 requests/second; 100 requests/hour
GETTOP_PRICE = 20 RUB / 1000 requests, VAT included
DERIVED_ONE_REQUEST_ESTIMATE = 0.02 RUB
SUPPORTED_TOP_OPERATORS = ! + quotes [] () |
! = fixes word form
() and | = grouping / OR
```

Provider maximum is a technical ceiling, not semantic-completeness proof.

## Bridge recheck

Live branch files checked:
- `extension/src/shared/wordstat_protocol.js`
- `extension/src/shared/service_registry.js`
- `extension/src/shared/wordstat_batch_protocol.js`
- `extension/src/shared/wordstat_batch_runtime.js`
- `extension/src/shared/policy_model.js`

Current Bridge contract:
```text
PREFIX = WORDSTAT_API_V1
METHOD = getTop
ENDPOINT = /v2/wordstat/topRequests
NUM_PHRASES = 1..2000
DEFAULT_REGIONS = ["225"]
DEFAULT_DEVICES = ["DEVICE_ALL"]
OUTCOME_UNKNOWN -> automatic_retry:false
DEFAULT_GETTOP_COST_RUB = 0.02
```

Bridge numeric GetTop cost matches the current official price. Bridge's default tariff-check metadata is dated 2026-08-12, so that historical timestamp is not used as current pricing evidence; this 2026-09-12 source trace is the current price authority for this gate.

## Operator decision

Candidate phrase remains:
`(амулет|оберег|талисман) Аум`

```text
MODE = DISCOVERY_RECALL_FIRST
MORPHOLOGY_FIXATION = NO
AUTO_SWITCH_TO_!Аум = NO
```

This is a project-method decision, not a provider fact. Product-class qualifiers already narrow context, while premature `!` fixation can reduce recall. A precision-form test would require separate evidence and a separate release.

## Depth decision

Options considered: 500 / 1000 / 2000.
Selected: `2000` for this one bounded request because shallower limits can truncate lower-frequency qualified vocabulary while request count/cost remains one request. Current provider and Bridge both support 2000.

Hard interpretation:
```text
RETURNED_ROWS == 2000
=> DEPTH_BOUNDARY_REACHED = true
=> SEMANTIC_UNIVERSE_COMPLETE = false
```

## Outcome contract

```text
SUCCESS_WITH_ROWS -> bounded positive evidence; persist/readback; then 03A/03B; reconcile
SUCCESS_WITH_ZERO_ROWS -> bounded zero for current request/snapshot only
SUCCESS_BUT_EVIDENCE_INCOMPLETE -> UNRESOLVED
VALIDATION_FAILURE -> UNRESOLVED
PROVIDER_FAILURE -> UNRESOLVED
OUTCOME_UNKNOWN -> UNRESOLVED; blind retry forbidden
NO_RETRY != NEGATIVE_EVIDENCE
```

## Verdict

```text
CURRENT_PROVIDER_DOCS = PASS
CURRENT_PRICE = PASS
CURRENT_LIMITS_QUOTAS = PASS
CURRENT_BRIDGE_SCHEMA = PASS
REGION = PASS
OPERATOR_DECISION = PASS
DEPTH_JUSTIFICATION = PASS
PROVIDER_CALLS = 0
```

This file supports a separate execution gate/release; it does not itself authorize or execute W10C001.