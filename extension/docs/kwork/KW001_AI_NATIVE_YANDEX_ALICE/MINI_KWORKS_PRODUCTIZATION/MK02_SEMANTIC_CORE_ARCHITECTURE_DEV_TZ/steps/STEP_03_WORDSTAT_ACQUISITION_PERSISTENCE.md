# MK02 STEP 03 — WORDSTAT ACQUISITION + DURABLE PERSISTENCE

## PURPOSE
Collect Yandex Wordstat evidence under the frozen plan and preserve a complete auditable occurrence layer before analysis continues.

## WHY THIS STEP EXISTS
A successful provider/tool response is not project evidence until the useful returned data are durably stored, reconciled and readable. Losing occurrence/source detail later can trigger unnecessary recollection or false frequency claims.

## INPUTS
Step02 acquisition manifest; region/mode parameters; current provider/cost authorization.

## REQUIRED EVIDENCE
Returned phrases/counts/roles and sufficient request/source provenance; raw or durable raw-equivalent evidence; completeness/truncation state where available.

## METHOD
Execute only authorized requests. Persist every governed returned occurrence, not only accepted examples. Keep normalized unique phrases separate from raw occurrence history. Record request/source identity, region, device/operator mode, time and provider limitations. Perform save/readback/reconciliation before the next material acquisition interaction.

## OUTPUTS
Durable Wordstat occurrence dataset; raw/equivalent evidence; request/checkpoint ledger; normalized union-compatible layer; reconciliation receipt.

## SOURCE KW-001 AUTHORITY
KW-001 Step3; `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md`; evidence-quality/provider-cost policy; MK01 Step03.

## KNOWN FAILURE CLASSES
S04 provider success = completed evidence; S05 dedupe erased history; S20 missing client-visible data triggered recollection; M11-01 transient acquisition.

## ROOT CAUSES
Tool execution state was mistaken for durable project state and immediate analytical convenience replaced future audit/reuse needs.

## NON-REPEAT CONTROLS
Complete occurrence preservation; normalized layer separate; save/readback before next acquisition; exact provider/mode semantics retained; no silent truncation.

## CLAIM BOUNDARIES
Wordstat count is demand evidence in the observed mode; it does not prove intent, page owner, new-page need or traffic.

## UNKNOWN / BLOCKER BEHAVIOR
Truncation/incomplete persistence blocks stronger completeness claims. Missing saved evidence is not repaired by guessing; repeat calls require explicit authorization/information need.

## PASS GATE
Executed request count reconciles to manifest; governed occurrence rows preserved; duplicate normalization does not erase source history; region/mode/provenance present; persistence/readback PASS.

## CLIENT-FACING MEANING
«Сохраняем не только итоговые ключи, но и откуда и в каком режиме пришли данные Яндекс Вордстата, чтобы дальнейшие решения можно было проверить и не пересобирать заново без необходимости.»
