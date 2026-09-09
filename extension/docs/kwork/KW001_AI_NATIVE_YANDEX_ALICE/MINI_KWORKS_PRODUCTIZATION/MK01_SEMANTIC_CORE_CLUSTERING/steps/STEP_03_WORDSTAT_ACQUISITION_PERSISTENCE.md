# MK01 STEP 03 — WORDSTAT ACQUISITION / PERSISTENCE

## PURPOSE
Acquire Yandex demand and preserve the complete usable occurrence/provenance evidence required downstream.

## WHY THIS STEP EXISTS
KW-001 proved that a technically successful provider request can still fail analytically if rows, provenance or raw-equivalent evidence are not durably saved.

## INPUTS
Frozen acquisition manifest, region/mode, persistence destination and request accounting model.

## REQUIRED EVIDENCE
Provider returns plus request/source metadata.

## METHOD
For each authorized call: request → preserve every useful returned occurrence → preserve phrase/count/role/seed/request/region/device/operator/time/source/raw-equivalent/completeness fields where available → save → remote/readback → accounting/schema QA → only then next material provider call. Raw occurrences and normalized phrase layer remain separate.

## OUTPUTS
Durable raw/equivalent evidence, occurrence table, provenance/demand table, request accounting and normalized join layer.

## SOURCE KW-001 AUTHORITY
Step3 lessons; `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md`; `EVIDENCE_QUALITY_AND_PROVIDER_COST_POLICY.md`.

## KNOWN FAILURE CLASSES
E04 provider success=completion; E05 only examples/accepted saved; E06 dedupe destroyed occurrence history.

## ROOT CAUSES
Transient response treated as database; schema optimized for immediate analysis; normalized phrase confused with source occurrence.

## NON-REPEAT CONTROLS
`HTTP SUCCESS != COLLECTION COMPLETE`; save/readback before next paid action; preserve full universe; dedupe only in a separate normalized layer.

## CLAIM BOUNDARIES
Wordstat demand does not prove business fit, intent, page ownership, ranking or traffic.

## UNKNOWN / BLOCKER BEHAVIOR
Truncation/provider limits or missing required persistence fields remain explicit. Do not silently label an incomplete route complete.

## PASS GATE
Every returned governed occurrence is persisted with deterministic provenance; request accounting reconciles; silent field loss=0; readback PASS.

## CLIENT-FACING MEANING
«Собираю спрос через Wordstat и сохраняю не только итоговые ключи, но и данные, по которым можно проверить, откуда взялась частотность и почему запрос попал в исследование.»
