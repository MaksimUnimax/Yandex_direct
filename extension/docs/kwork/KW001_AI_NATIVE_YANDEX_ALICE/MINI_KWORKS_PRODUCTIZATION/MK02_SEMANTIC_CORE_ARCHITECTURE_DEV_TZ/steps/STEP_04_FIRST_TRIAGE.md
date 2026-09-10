# MK02 STEP 04 — FIRST CONSERVATIVE TRIAGE

## PURPOSE
Remove obvious noise/out-of-scope families conservatively while preserving uncertain and potentially useful demand for later row-level decisions.

## WHY THIS STEP EXISTS
Early family screening is useful for control and second-pass planning but becomes dangerous when it is mistaken for final cleanup or page/architecture authority.

## INPUTS
Complete persisted Wordstat occurrence layer; frozen business scope; Step01 business profile.

## REQUIRED EVIDENCE
Phrase/family text, frozen business boundary, occurrence/source context sufficient for obvious screening.

## METHOD
Classify only obvious family-level noise/scope mismatches conservatively. Keep uncertain, related, service, informational, accessory and other plausible tasks for downstream row-level analysis. Do not use frequency alone as exclusion/acceptance. Record named coverage gaps that may justify Step05.

## OUTPUTS
Preliminary triage states; preserved review set; named second-pass information gaps; no silent deletion.

## SOURCE KW-001 AUTHORITY
KW-001 Step4; MK01 Step04.

## KNOWN FAILURE CLASSES
S06 family triage = row cleanup; S07 low frequency = irrelevant; S08 high count/association = relevant.

## ROOT CAUSES
Early operational screening was allowed to masquerade as final semantic truth.

## NON-REPEAT CONTROLS
Three-way conservative routing or equivalent; uncertainty preserved; final row-level acceptance deferred to Step06; no page ownership/architecture decisions here.

## CLAIM BOUNDARIES
Triage is not final relevance, clustering, owner mapping or page creation logic.

## UNKNOWN / BLOCKER BEHAVIOR
Ambiguous families remain review; if a coverage gap is real and decision-relevant, route to Step05 instead of recursively expanding everything.

## PASS GATE
All input occurrences accounted; no low-frequency auto-reject; no association/high-volume auto-keep; named second-pass gaps only; no downstream architecture claims.

## CLIENT-FACING MEANING
«На первом проходе убираем только очевидный мусор и сохраняем всё спорное для дальнейшей проверки, чтобы не потерять полезный спрос слишком рано.»
