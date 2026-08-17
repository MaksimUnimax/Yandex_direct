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

- every uniquely resolved local Copy control belonging to a supported assistant writing/code block becomes the Yandex Manual action surface;
- the control is Yandex-yellow and visibly labeled `Яндекс`;
- this visual/action state does **not** depend on the text inside the block, protocol marker presence, JSON validity, service, method, credentials, policy, price, provider readiness or whether the block can eventually execute;
- generic assistant-level `Copy response` remains excluded and native.

The native page Copy behavior must remain intact. The extension adds a Manual bridge action to the same local code-block control without preventing the native Copy event.

## 2. Content-script responsibility

The content script is responsible only for the AI-page boundary:

```text
assistant code/writing block
→ uniquely resolve its local Copy control
→ decorate/label that control while Manual ON
→ on click capture the complete block text
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
- native Copy still fires;
- Manual OFF restores the button exactly and removes only bridge-owned label/style/listener state.

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

- Manual OFF: all local code-block Copy controls ordinary;
- Manual ON: all uniquely bound local assistant code-block Copy controls yellow + `Яндекс`, regardless of content;
- generic whole-response Copy always ordinary/non-trigger;
- click on a non-command block: native Copy + explicit bridge error, zero Yandex request;
- click on malformed command block: native Copy + explicit bridge error/result, zero Yandex request;
- click on valid one-command block: native Copy + one accepted bridge command;
- click on multi-command block: native Copy + ordered worker-owned discovery/batch semantics.
