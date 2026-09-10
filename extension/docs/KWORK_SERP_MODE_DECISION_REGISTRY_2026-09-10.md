# KWORK SERP MODE DECISION REGISTRY

Date: 2026-09-10
Status: **ACTIVE PORTFOLIO REGISTRY**
Governing rule: `KWORK_SERP_MODE_PRODUCTIZATION_GATE_2026-09-10.md`
Research authority: `KWORK_SERP_COVERAGE_MODE_RESEARCH_2026-09-10.md`

This registry records one-time productization decisions. It is not a per-client execution log.

| Kwork | Current SERP mode | Status | Basis |
|---|---|---|---|
| KW-001 — AI-native semantic rebuild | `SELECTIVE_DECISION_SERP` | FROZEN CURRENT METHOD | Existing-site rebuild; accepted KW-001 method uses bounded Search for material intent/page boundaries rather than full per-keyword TOP coverage. |
| KW-002 — greenfield semantic core + architecture | `FULL_SERP_COVERAGE` | OWNER-FROZEN 2026-09-10 | Full current SERP evidence is required for every phrase in the final cleaned/delivery-selected Search set before final SERP-grounded clustering/page architecture. RAW/EXCLUDED/RESERVE are not Search input. |
| KW-003 — Yandex SERP clustering | `PENDING_PRODUCTIZATION_DECISION` | NOT FROZEN | Do not infer FULL merely from product name; prove mode during KW-003 roadmap development against the portfolio research and exact sold promise. |
| KW-004 — niche + competitor opportunity analysis | `PENDING_PRODUCTIZATION_DECISION` | NOT FROZEN | Decide once during productization. |
| KW-005 — Direct + Metrika audit | `PENDING_PRODUCTIZATION_DECISION` | NOT FROZEN | Decide whether ordinary organic Search is base/optional/none during productization. |
| KW-006 — recurring Direct optimization | `PENDING_PRODUCTIZATION_DECISION` | NOT FROZEN | Decide during productization. |
| KW-007 — exact-frequency enrichment | `PENDING_PRODUCTIZATION_DECISION` | NOT FROZEN | Decide during productization; organic SERP must not be assumed necessary. |
| KW-008 — competitor keyword-gap from client export | `PENDING_PRODUCTIZATION_DECISION` | NOT FROZEN | Decide during productization. |

Hard rule:

```text
PENDING_PRODUCTIZATION_DECISION
!= SELECTIVE
!= FULL
!= NONE
```

Future productization must create a local Level-1 authority and then update this registry/readback. Normal client jobs do not reopen the portfolio decision unless a product/version re-open trigger applies.