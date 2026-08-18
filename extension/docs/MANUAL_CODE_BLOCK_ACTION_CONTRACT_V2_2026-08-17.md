# Manual code-block action contract v2 — Yandex Marketing Bridge

Date: 2026-08-17
Status: **OWNER-DIRECTED CURRENT CONTRACT**
Supersedes earlier Phase-1 visual/manual assumptions wherever they conflict with this file.

## 1. Owner decision

Manual mode is a DOM/action-surface mode, not a pre-validation mode.

When Manual is OFF:

- all ordinary ChatGPT local code-block Copy controls remain native/ordinary;
- the bridge does not arm a Manual API action.

When Manual is ON for the confirmed bound conversation:

- every uniquely resolved local Copy control belonging to a supported assistant writing/code block remains native and receives exactly one separate adjacent Yandex Manual sibling action;
- the separate sibling is Yandex-yellow and visibly labeled `Яндекс`;
- this visual/action state does **not** depend on the text inside the block, protocol marker presence, JSON validity, service, method, credentials, policy, price, provider readiness or whether the block can eventually execute;
- generic assistant-level `Copy response` remains excluded and native.

The native page Copy behavior must remain intact. The extension adds a separate Manual bridge action adjacent to the local code-block control without mutating or replacing the native Copy control/event.

## 2. Content-script responsibility

The content script is responsible only for the AI-page boundary:

```text
assistant code/writing block
→ uniquely resolve its local Copy control
→ preserve native Copy and create/label one separate Yandex sibling while Manual ON
→ on Yandex sibling click capture the complete block text
→ submit the complete block text to worker/core
```

The content script MUST NOT pre-filter Manual blocks by:

- `WORDSTAT_API_V1` or any other service prefix;
- `isCommandText()`;
- JSON parse success;
- operation allowlist;
- service routing;
- credential state;
- provider/policy/cost state.

No Manual parse/validation error is allowed to terminate as a content-only toast. Once the trusted conversation/block click has been admitted, command discovery/validation errors are worker-owned and must become an observable chat result/error with zero external request when appropriate.

## 3. DOM binding contract

The DOM adapter must be independent of command text.

Required properties:

- support current writing-block DOM;
- support legacy `#code-block-viewer` DOM;
- support ordinary generic code-block DOM;
- resolve button↔block locality structurally, not by API marker text;
- prefer the smallest unambiguous local code-block container;
- exclude the generic whole-assistant-response Copy action;
- fail closed when one button cannot be mapped uniquely to one block;
- rescan after Manual activation and relevant DOM mutation;
- restore the exact native button state when Manual turns OFF or runtime disposes.

Manual diagnostics must expose enough evidence to localize a gray/unarmed control without operator DOM investigation. At minimum:

```text
manual_enabled
conversation_key
assistant_container_count
code_block_candidate_count
local_copy_candidate_count
bound_block_count
decorated_button_count
adapter_ids
failure_reason_counts
```

## 4. Yandex visual contract

The local code-block Copy action in Manual ON state must be visually analogous to the proven Ozon Manual Copy action, adapted to Yandex branding:

- Yandex-yellow action state;
- visible text label `Яндекс` on the local action control;
- existing native Copy icon/content is not destructively replaced;
- native Copy and Yandex sibling are different independently clickable DOM elements;
- only the Yandex sibling owns the Bridge Manual click listener;
- native Copy performs native copying only and dispatches zero `WS_EXECUTE_MANUAL_BLOCK`;
- Manual OFF removes only Bridge-owned sibling controls/listeners/timers; native Copy needs no restoration.

This is a state/action indicator. It is not proof that block contents are a valid executable API command.

## 5. Worker/core ownership after click

The complete clicked block text is the input to worker/core.

Worker/core then performs, in order:

```text
trusted sender/conversation/manual gates
→ full-block command discovery
→ structural JSON extraction
→ service registry routing
→ strict service validation
→ policy/credential/cost gates
→ ordered execution
→ durable result/error state
→ final delivery
```

If no supported executable command exists in the clicked block, the user must receive an explicit `YMB_ERROR_V1`/controlled bridge error with `request_executed:false`. Silent no-op is forbidden.

If a marker exists but JSON/contract validation fails, the failure is worker-owned and chat-visible with zero provider request for that item.

## 6. Multi-command block behavior

The target behavior follows the proven Ozon batch architecture:

- scan the full clicked block for every registered service marker in source order;
- separators between commands are not protocol syntax: comma, whitespace, Markdown, prose or adjacency may occur;
- extract exactly one complete JSON object after each marker using balanced-brace/string-aware parsing;
- malformed material at one marker must not consume later markers;
- valid commands execute strictly one at a time;
- no hidden parallel provider fan-out;
- completed provider results are persisted before moving to the next item;
- recovery never replays a completed provider initiation;
- one final combined delivery is preferred for one accepted Manual block/batch.

Phase 1 may execute only registered/accepted Wordstat operations. Future Search/Webmaster/Metrika/Direct markers may be recognized only after their service phase is enabled. `one RUN = one SERVICE` remains a hard Autorun safety rule; cross-service execution is not silently introduced by this contract.

## 7. Reference lineage used for this correction

The owner-directed Yandex contract deliberately reuses the proven Ozon architectural lessons while adapting product semantics:

- Ozon v0.1.5 moved Manual parsing/validation ownership out of the content script and into the worker-owned observable result lifecycle;
- Ozon v0.1.9 unified Manual and Autorun around command discovery → ordered queue → strict serial provider execution → one final batch delivery;
- Ozon v0.1.10 tied visual readiness to its own worker readiness policy, but Yandex Manual v2 intentionally differs: Yandex visual arming is controlled by Manual ON plus unambiguous local DOM binding only;
- Ozon v0.1.11 corrected current generic code-block binding, rescanning and decorated-button diagnostics after a live gray-Copy failure.

The Yandex difference is intentional: **a yellow `Яндекс` button means “this code block is armed for Manual bridge inspection,” not “this block has already passed protocol validation.”**

## 8. Acceptance consequences

Earlier Phase-1 tests that expected non-command local code-block Copy controls to stay gray while Manual ON are superseded.

New required visual behavior:

- Manual OFF: native local Copy controls remain ordinary and no Yandex sibling exists;
- Manual ON: all uniquely bound local assistant code-block Copy controls remain native and receive exactly one separate yellow `Яндекс` sibling, regardless of content;
- generic whole-response Copy always ordinary/non-trigger;
- click on a non-command block: native Copy + explicit bridge error, zero Yandex request;
- click on malformed command block: native Copy + explicit bridge error/result, zero Yandex request;
- native Copy click: native copy only, zero Bridge dispatch;
- Yandex sibling click on non-command: explicit Bridge controlled error, zero provider request;
- click on valid one-command block: native Copy remains independent and one Yandex sibling click admits one accepted bridge command;
- click on multi-command block: Yandex sibling + ordered worker-owned discovery/batch semantics.

## 9. Owner-directed contract correction — 2026-08-18

The following semantics supersede any earlier wording that described the native
local Copy itself as becoming the Yandex action:

- Manual OFF: native ChatGPT local Copy remains exactly native; no Bridge-owned Yandex sibling exists.
- Manual ON with a confirmed conversation and unique block binding: Bridge creates exactly one separate adjacent/sibling Yandex action per eligible block.
- The sibling has `data-ymb-manual-action="true"`, yellow visual state, and visible label `Яндекс`.
- The native Copy is only the structural anchor for block locality; it is a different DOM element from the sibling and has no Bridge Manual listener/effect.
- Clicking native Copy performs native copy only. Clicking the Yandex sibling captures the complete bound block and submits it to worker/core.
- DOM mutation is idempotent: a newly appearing uniquely bound block gets exactly one sibling, never duplicates.
- Manual OFF/dispose removes only Bridge-owned Yandex siblings/listeners/timers; native Copy is not restored because it was never mutated.
- A committed Manual delivery remains fenced until the matching sent user-turn confirmation exists.
- Post-commit reconciliation is bounded confirmation-only: no second Send, no second `WS_EXECUTE_MANUAL_BLOCK`, and no provider/API replay.
- Confirmation completes the operation and admits the next user-authorized Manual action; an unresolved boundary remains fenced.
