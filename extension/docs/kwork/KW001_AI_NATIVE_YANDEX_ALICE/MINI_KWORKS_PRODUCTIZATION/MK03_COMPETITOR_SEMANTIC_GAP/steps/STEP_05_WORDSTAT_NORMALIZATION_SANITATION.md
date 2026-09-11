# MK03 STEP 05 — WORDSTAT DEMAND VALIDATION + NORMALIZATION / SANITATION

## Purpose
Test genuinely new competitor-derived probes in Yandex Wordstat and convert raw provider output into a compact auditable candidate set.

## Why this step exists
Competitor topics must be checked against real Yandex demand, while raw provider rows must not inflate or contaminate the result.

## Inputs
Active competitor-derived seed register; existing normalized analytical pool/provenance when available.

## Required evidence
Authorized Wordstat responses with region/device/operator/request/timestamp/raw evidence/provenance sufficient for persistence and reconciliation.

## Method
For each justified seed:

```text
WORDSTAT RAW
→ preserve losslessly
→ exact/safe normalization + deduplication
→ high-confidence sanitation
→ compare with existing normalized pool
→ NEW_SANITIZED_CANDIDATE | ALREADY_COVERED | REJECT | HOLD
```

Preserve duplicate lineage. Do not auto-exclude low frequency or auto-accept high frequency. Clear off-scope may be rejected with reason; ambiguity remains HOLD.

## Outputs
- competitor Wordstat raw occurrence layer;
- normalized identity mapping;
- sanitation/reason ledger;
- counts: seeds, raw occurrences, normalized uniques, already existing, new normalized, auto-excluded, hold, new sanitized candidates.

## Source authority
`STEP_05A_VOLUME_SANITATION_ADDENDUM_2026-09-10.md`; `DATA_VOLUME_NORMALIZATION_AND_SANITATION_GATE.md`; Step3 persistence authorities.

## Known failures / root causes
- raw rows appended directly;
- duplicate provider occurrences become duplicate keywords;
- competitor presence overrides scope;
- low frequency used as irrelevance rule.

## Non-repeat controls
`NEW PROVENANCE != NEW KEYWORD ID`; RAW is durable evidence, not final analytical set.

## Claim boundary
Wordstat supports demand around the tested seed; it does not alone prove exact intent, client fit, ranking or need for a new page.

## Unknown behavior
Ambiguous/multi-meaning rows remain HOLD; incomplete provider evidence blocks stronger demand conclusions for affected probes.

## PASS gate
Raw→normalized→sanitized counts reconcile exactly; silent drops = 0; all exclusions/collapses have reasons/targets; all new candidates retain competitor lineage.

## Client-facing meaning
“We checked whether competitor-derived directions correspond to real Yandex demand and removed duplicates/noise without losing evidence.”
