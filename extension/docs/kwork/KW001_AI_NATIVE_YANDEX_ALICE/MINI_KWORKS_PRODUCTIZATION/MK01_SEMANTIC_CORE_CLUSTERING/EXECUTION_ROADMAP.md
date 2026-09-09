# MK01 — AUTONOMOUS EXECUTION ROADMAP

Status: **DEFINED / PENDING OKNO_MSK STANDALONE REHEARSAL**

This is the operational sequence for a real MK01 order. It is intentionally smaller than full KW-001 and has no hidden dependency on omitted stages.

## PRECONDITION

Client input must pass `CLIENT_INPUT_CONTRACT.md`: public site + primary region + included scope + exclusions + business/conversion job. No Google or mandatory private Yandex access is required.

## STEP 00 — Freeze order
Persist exactly what was purchased before demand evidence is seen. Output: Level-2 order freeze. No provider acquisition before required fields are frozen.

## STEP 01 — Build current site/business profile
Establish what the public business actually offers and the domain vocabulary needed for relevance/clustering. Output: timestamped site/business/domain profile with coverage limits. Discovery success is not completeness.

## STEP 02 — Build Wordstat acquisition manifest
Design bounded probes that expose demand vocabulary without pre-approving keywords. For each probe preserve expression, region, applicable device/operator mode, information purpose, expected evidence and stop/coverage condition.

## STEP 03 — Acquire and durably preserve Wordstat evidence
For each authorized item: request -> receive useful result -> persist occurrence/provenance -> readback -> count/field/completeness QA -> continue. Output raw/durable evidence, occurrence table, request accounting and normalized join layer. Silent field loss = 0.

## STEP 04 — First triage
Remove obvious scope/noise families while preserving ambiguity. Output explicit family/early-screen reasons. Triage is not full cleanup.

## STEP 05 — Conditional targeted second acquisition
Run only for a named unresolved gap that persisted evidence cannot answer. Output union-compatible new evidence and explicit resolved/unresolved gap state. If no gap: `NOT REQUIRED / NO PROVIDER CALL`.

## STEP 06 — Full row-level cleanup
Every governed phrase receives explicit state + reason + evidence basis + uncertainty. No default KEEP. Accounting QA and semantic QA both required.

## STEP 07 — Freeze semantic universe and Search routes
Preserve active, Search-required, deferred and excluded states plus complete demand/provenance join. Output immutable Search-stage handoff. No page ownership/architecture.

## STEP 08 — Targeted ordinary Yandex Search
Probe only material Search-resolvable semantic boundaries. Preserve exact query, region/time/surface, observed result pattern and exact claim scope. No bulk rank tracking.

## STEP 09 — Task-first clustering
Declare domain profile, taxonomy/count/evidence/uncertainty/QA modes. For a fresh large corpus: task discovery -> cluster contracts -> full assignment -> independent semantic QA -> root-cause correction -> regression. Output phrase→cluster assignments, user-task/intent meaning, unresolved boundaries and cluster summary. No page-architecture leakage.

## STEP 10 — Client materialization and release QA
Freeze current-authority manifest, generate rather than manually patch. Minimum recipient views: scope/how-to-use; full preserved phrase universe; active core; cluster summary; unresolved/Search-required; dictionary/metrics/method/provenance; delivery summary.

Run separately: DATA QA; SEMANTIC QA; WORKBOOK QA; RECIPIENT-LANGUAGE QA; VISUAL QA; OWNER/RECIPIENT TASK QA; PERSISTENCE/REMOTE READBACK QA.

## PRODUCT COMPLETION

Done only when scope frozen + Yandex evidence durable + full governed phrase accounting + uncertainty preserved + targeted Search done where justified + clustering semantic QA PASS + standalone artifact PASS + remote/persisted identity PASS.

Outside completion: page ownership, SEO architecture, competitor gap audit, implementation TZ, Alice/AEO, Google SEO.

## REVISION RULE

After order freeze, material changes to region/site/business families are logged as revisions. Re-run only affected evidence/analysis where justified; do not erase or blindly recollect valid historical evidence.
