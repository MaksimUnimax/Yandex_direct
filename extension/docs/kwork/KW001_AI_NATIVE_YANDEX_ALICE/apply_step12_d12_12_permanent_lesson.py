from pathlib import Path

ROOT=Path('extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE')
method_path=ROOT/'STEP_12_STRUCTURAL_ACTION_METHOD.md'
method=method_path.read_text(encoding='utf-8')
heading='## Defect 12 — upstream OUTSIDE/NO-PAGE state can be contradicted by later verified site evidence'
if heading not in method:
    block=r'''

## Defect 12 — upstream OUTSIDE/NO-PAGE state can be contradicted by later verified site evidence

### What exposed the failure

During the OKNO-MSK correction, full phrase review found a historical outside-scope family that contained a product for which the current site already had a verified public page. Other rejected/outside groups also contained individual phrases that belonged to valid in-scope tasks.

### Why the old behavior seemed reasonable

Step 12 is downstream from semantic cleanup/clustering/page ownership, so accepted upstream states normally deserve strong deference. Reopening every prior decision without cause would create endless instability.

### Why blind inheritance is wrong

Upstream authority is not stronger than contradictory later evidence. A later step often sees more complete phrase membership, page inventory and structural relationships than the earlier step did. If current first-party evidence proves that the business really offers the product/service, preserving an old `OUTSIDE` label merely because it is historical converts provenance into a correctness claim.

### Correct understanding

```text
UPSTREAM STATE
= accepted input until contradicted

LATER MATERIAL CONTRADICTION
→ preserve original history
→ create explicit correction overlay
→ re-evaluate affected phrase/task
→ verify downstream impact
```

Do **not** reverse every outside/no-page state just because a relevant word appears. The same correction run also demonstrated the opposite case: a window-related phrase can actually target another brand/company and therefore remain outside after disambiguation.

### Non-repeat control

Every Step-12 `OUTSIDE_SCOPE` / `NO_STANDALONE_PAGE` family must receive a salvage/contradiction pass before final acceptance:

```text
CURRENT SITE/OFFER CONTRADICTS OLD OUTSIDE?
USEFUL IN-SCOPE PHRASE TRAPPED IN REJECTED UNIT?
OTHER-BRAND / NAVIGATIONAL PHRASE CORRECTLY OUTSIDE?
UNVERIFIED PRODUCT/SERVICE STILL UNVERIFIED?
```

The result must be explicit per phrase or structural subunit: `SALVAGED`, `DEFERRED`, `OUTSIDE_CONFIRMED`, or `NO_STANDALONE_CONFIRMED`.

Why: the goal is neither to protect old labels nor to rescue everything; it is to preserve the user's real task and the business truth under the newest reliable evidence.
'''
    anchor='\n---\n\n# 4. Correct Step-12 working model'
    if anchor not in method: raise RuntimeError('method insertion anchor not found')
    method=method.replace(anchor,block+anchor,1)
method_path.write_text(method,encoding='utf-8')

ledger_path=ROOT/'STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md'
ledger=ledger_path.read_text(encoding='utf-8')
marker='12. **Upstream outside/rejected state can conflict with later verified site evidence.**'
if marker not in ledger:
    anchor='### Root cause\n\nThe first method correctly understood the broad principle'
    add='''12. **Upstream outside/rejected state can conflict with later verified site evidence.** A prior scope/no-page label is accepted only until materially contradicted by later phrase-level or current first-party evidence; preserve history and apply an explicit correction overlay rather than blindly inheriting or blindly reversing the state.\n\n'''
    if anchor not in ledger: raise RuntimeError('ledger Step12 root-cause anchor not found')
    ledger=ledger.replace(anchor,add+anchor,1)
    marker_anchor='STEP12_HIERARCHY_PLAN_REQUIRED_FOR_NEW_OR_SPLIT_PAGES = true\n'
    if marker_anchor in ledger and 'STEP12_UPSTREAM_OUTSIDE_MUST_YIELD_TO_VERIFIED_CONTRADICTION' not in ledger:
        ledger=ledger.replace(marker_anchor,marker_anchor+'STEP12_UPSTREAM_OUTSIDE_MUST_YIELD_TO_VERIFIED_CONTRADICTION = true\n',1)
ledger_path.write_text(ledger,encoding='utf-8')
