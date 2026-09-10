# MK02 — SERP COVERAGE MODE DECISION

Date: 2026-09-10
Status: **LEVEL-1 / CURRENT PRODUCTIZATION DECISION**

Series gate:

`../MINI_KWORK_SERP_MODE_PRODUCTIZATION_GATE_2026-09-10.md`

Portfolio research:

`../../../../KWORK_SERP_COVERAGE_MODE_RESEARCH_2026-09-10.md`

## Current mode

```text
SERP_COVERAGE_MODE = SELECTIVE_DECISION_SERP
PER_CLIENT_MODE_REPROOF = false
```

## Why

MK02 is an existing-site product that builds a target landing/page structure and reconciles it against the current site, but its current frozen semantic foundation and product scope use ordinary Search only where a material semantic/page boundary requires direct evidence.

MK02 does not currently sell a separate claim that every governed phrase has its own current Yandex TOP fingerprint.

Therefore the current product remains selective unless a future version explicitly changes the sold promise to full-TOP/SERP clustering and passes new economics/rehearsal/QA.

## Required execution behavior

```text
all governed phrases -> semantic/task/page-map accounting
material Search-resolvable boundaries -> direct/reused Search
unprobed rows -> not called direct Search-confirmed
page/structure claims -> must not exceed actual evidence
```

This one-time decision must be reflected in MK02 economics/final freeze. Normal client jobs do not debate the mode again.