# WORKFLOW OPERATING RULES — ChatGPT / Codex / Owner

Status: **CURRENT / MANDATORY OPERATING CONTRACT**  
Adopted: 2026-08-19  
Scope: **the current conversation immediately, plus every new or resumed** Yandex Marketing Bridge development, QA, release, handoff and live-acceptance conversation.

## 1. Purpose and immediate effect

This document exists to prevent process regressions even when the product code is correct.

**These rules take effect immediately in the conversation in which they are adopted. They do not require a new chat, restart, handoff, reload or later session.** Every subsequent action in the current conversation must comply with them.

A current, new or resumed conversation must not reconstruct the workflow from chat memory, improvisation or assumptions about tool availability. The workflow is governed here and by `CURRENT_STATE.md` plus the current product contracts.

The intended chain is:

```text
Owner requirement
→ ChatGPT reconstructs current governed state
→ ChatGPT develops/fixes product and tests
→ ChatGPT freezes exact candidate and exact handoff artifact
→ Codex executes the governed regression gate using demonstrated capabilities
→ evidence returns to ChatGPT
→ ChatGPT fixes only proven defects/layers
→ full gate PASS on exact artifact
→ owner receives that exact tested artifact
→ irreducible owner real-profile/live acceptance
```

## 2. Permanent role boundary

### Owner

The owner:

- defines requirements and acceptance intent;
- may paste a prompt to Codex when that is the chosen QA execution channel;
- performs only irreducible real-profile/live acceptance that cannot truthfully be replaced by controlled QA;
- is **not** a development operator, QA harness engineer, file courier, environment installer or repetitive manual tester.

Do not ask the owner to download/upload/move/rename/extract/stage QA files for Codex, install QA dependencies for Codex, manually reconstruct artifacts, run shell commands for QA, or repeat browser actions that qualified controlled automation can perform.

### ChatGPT

ChatGPT owns:

- current-state reconstruction;
- requirement analysis;
- architecture and implementation decisions;
- product code changes;
- test design and test code;
- QA harness design where required;
- focused development testing;
- deterministic packaging/freeze;
- QA transport design;
- gate authoring/maintenance;
- analysis of Codex evidence;
- root-cause classification;
- all product/test/process fixes;
- final handoff preparation.

ChatGPT must not offload missing test design, missing harness design, product fixes or workflow design to Codex or the owner.

### Codex

Codex is the independent QA executor for the governed gate.

Codex may:

- obtain governed inputs through transports/workspaces available to it;
- use its demonstrated shell/repository/browser/test capabilities;
- execute the tests/harness already designed by ChatGPT;
- use technically equivalent invocation paths required by its environment without weakening assertions;
- collect logs, screenshots, traces, hashes and reports;
- classify actual failure evidence.

Codex must not:

- design product fixes;
- edit production code;
- patch tests to make them pass;
- invent missing acceptance criteria;
- silently weaken browser/runtime assertions into source inspection;
- substitute another candidate.

## 3. Environment non-inheritance rule

The following environments are distinct:

```text
ChatGPT conversation/tool environment
ChatGPT sandbox/container
GitHub repository/connectors
Codex Windows workspace/shell/tools
owner real Chrome/profile
```

**Capabilities do not inherit between environments.**

Never infer that Codex lacks a capability because ChatGPT lacks it. Never infer that a file in ChatGPT sandbox is visible to Codex. Never infer that a controlled Codex browser equals the owner's real profile.

Before depending on a capability, establish it from the environment that must actually perform the action.

If a capability was already demonstrated and remains applicable, reuse that fact instead of rediscovering the workflow from scratch. If there is material uncertainty that it still exists, verify it in that environment.

## 4. Mandatory workflow-transition reconstruction

Before **every** stage transition, including the very next action in the current conversation after these rules are changed, ChatGPT must reconstruct the current state from live authority.

Transitions include at minimum:

- current conversation after a rule/governance correction;
- new/resumed conversation;
- requirement → development;
- development → freeze;
- freeze → Codex QA;
- Codex result → repair or handoff;
- failure → next attempt;
- full-gate PASS → owner handoff;
- owner live result → phase close/reopen;
- governance/document update → next engineering or release action.

Required reconstruction record:

```text
LIVE_HEAD = <current main SHA>
PRODUCT_SOURCE = <exact identity/path/hash authority>
HANDOFF_ARTIFACT = <exact filename/SHA/bytes or NONE>
LATEST_FULL_GATE = <PASS/FAIL + exact candidate authority>
PRODUCTION_BYTES_CHANGED_SINCE_GATE = YES|NO
OWNER_LIVE = PASS|FAIL|PENDING
OPEN_BLOCKERS = <list>
AUTHORIZED_NEXT_STAGE = <one stage>
```

Do not proceed from remembered SHA, old candidate names or historical evidence when live GitHub/current evidence can answer the question.

## 5. Authority precedence and conflict handling

Operating precedence:

1. explicit current owner instruction that intentionally changes a requirement/workflow;
2. this `WORKFLOW_OPERATING_RULES.md` for roles/process/environment behavior;
3. `CURRENT_STATE.md` for current stage and exact current identities;
4. current living `PROJECT_PURPOSE.md`, `SPECIFICATION.md`, `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`;
5. `ROADMAP.md` for phase/status narrative;
6. append-only context and historical evidence for provenance.

Historical entries are evidence, not automatic current authority.

If two current canonical documents materially conflict:

```text
STOP
→ identify exact contradiction
→ reconcile current documents
→ record correction
→ reconstruct state again
→ only then continue
```

Do not choose whichever text appears convenient. Do not solve a documentation conflict by private interpretation.

## 6. Minimal-change / root-cause containment protocol

After every failure, ChatGPT must identify the failing layer **before changing anything**.

Allowed layers:

```text
PRODUCT
TEST
HARNESS
ARTIFACT/PACKAGING
TRANSPORT
PROMPT/EXECUTION INSTRUCTION
GOVERNANCE/DOCUMENTATION
OWNER-LIVE-ONLY ENVIRONMENT
```

Mandatory sequence:

```text
1. preserve evidence;
2. establish exact failing assertion/operation;
3. classify the failing layer;
4. establish a concrete root cause supported by evidence;
5. change only the smallest layer(s) proven necessary;
6. do not mutate product bytes for a QA-process failure;
7. rerun the appropriate focused verification;
8. if production bytes changed, freeze a new candidate and invalidate the previous product gate;
9. if production bytes did not change, preserve exact product identity and fix only the failing QA/process layer.
```

Examples:

- `FAIL_ARTIFACT` does not authorize product code changes.
- `FAIL_HARNESS` does not authorize product code changes.
- a bad Codex prompt does not authorize a new candidate.
- a product assertion failure does authorize ChatGPT to fix product code and tests, after which a new freeze/full gate is required.

No broad workflow redesign is allowed merely because one local step failed.

## 7. Owner-correction canonicalization protocol

When the owner corrects ChatGPT, classify the correction immediately **in the current conversation**.

### One-off correction

Applies only to the current action. No permanent documentation change is required unless it exposes a broader invariant.

### Persistent invariant

A correction about roles, workflow, QA, safety, authority, handoff, environment boundaries or repeated behavior is presumed persistent unless clearly local.

For a persistent invariant:

```text
owner correction
→ apply it immediately to the current conversation
→ restate the invariant accurately
→ identify the canonical document that governs it
→ update that document before the same class of mistake can recur
→ search other current canonical docs for conflicting wording
→ reconcile conflicts
→ reconstruct current state
→ continue under the corrected rule immediately
```

Do not leave a persistent owner correction only in chat memory. Do not defer its effect until a future conversation.

## 8. Gate purpose and relationship to development

The pre-delivery gate exists primarily to catch **regressions introduced by ChatGPT's code changes** before the owner receives a candidate.

Development testing and pre-delivery regression are different:

```text
while changing code
→ focused tests for changed behavior + affected dependencies

working candidate frozen
→ exact artifact freeze
→ one complete Codex regression campaign
→ only full PASS allows owner handoff
```

The gate is not paperwork. Passing a subset of tests is not equivalent to passing the product regression firewall.

The exact artifact handed to the owner must be the exact artifact accepted by the complete gate, unless a later governed documentation-only change is explicitly established not to alter product bytes or acceptance assertions.

## 9. Documentation-only changes after a product PASS

A documentation/evidence-only commit does **not automatically** change the tested product bytes.

After any such commit, classify the documentation delta:

- **process/evidence clarification only** — product artifact identity and prior product PASS may remain valid if no acceptance assertion/test requirement changed;
- **acceptance/gate requirement change** — the affected gate evidence must be refreshed, and if the living gate requires a complete fresh campaign, rerun the complete gate;
- **product contract change** — product must be reconciled to the contract, then a new candidate/full gate is required.

Record this classification in `CURRENT_STATE.md`. Never assume either “docs never matter” or “every docs commit invalidates product PASS”.

## 10. Response/action discipline in the owner conversation

These rules apply **now, in the current conversation**, and in all later conversations:

- answer the owner's actual question, not a neighboring question;
- when an action is available and requested, perform it before giving a long explanation;
- do not repeatedly explain already-established roles/process unless needed to resolve a new conflict;
- do not ask the owner to repeat information already available in current conversation or canonical docs;
- do not create unnecessary alternative workflows when the governed workflow already applies;
- use concise progress updates for long tool operations, then return the concrete result;
- after a Codex result, classify it first; do not reflexively invent a new candidate, transport or harness.

## 11. Conversation startup / immediate-current checklist

This checklist applies in three cases:

1. immediately after these rules or another persistent workflow correction are adopted in the current conversation;
2. when a new ChatGPT conversation starts;
3. when an old conversation is resumed after context may have drifted.

Before substantive action:

1. fetch live `main` HEAD;
2. read `extension/docs/README.md`;
3. read this file;
4. read `CURRENT_STATE.md`;
5. read the current product/spec/gate documents relevant to the requested action;
6. inspect latest applicable append-only correction entries when they can alter interpretation;
7. confirm there is no unresolved current-document contradiction;
8. determine the exact authorized next stage;
9. only then act.

If these steps reveal stale or contradictory control-plane documentation, repairing that state is the first task.

## 12. Proven-route QA transport and exact-artifact authorization

These rules are permanent and were added after repeated `FAIL_ARTIFACT` mistakes on 2026-08-19. They govern every future transition from freeze or QA-process repair into Codex QA.

### A. Reuse a demonstrated working route before inventing anything

If an earlier campaign demonstrably transported an exact frozen artifact into Codex and reached actual gate execution, that transport path is a **proven route**.

Before designing, branching, encoding, reconstructing or otherwise inventing a new QA transport, ChatGPT must:

1. identify the latest applicable proven route from live repository/evidence;
2. verify that the capability used by that route is still available to the environment that must use it;
3. reuse that route for the new exact artifact whenever technically possible.

A new transport may be introduced only after evidence establishes why the proven route cannot carry the new exact artifact. Convenience, uncertainty, forgotten context or a limitation of ChatGPT's own current UI/tool surface is not sufficient evidence.

The successful `31cc5f3f…` full-gate campaign is a permanent example: it reached real Codex execution. Later attempts must not disregard that working history and improvise a new transport without first exhausting/reusing the proven mechanism.

### B. No Codex prompt before transport round-trip proof

A successful upload call, Git blob creation, branch commit, file listing, filename match or API `200` is **not proof that the exact artifact reached the transport intact**.

Before ChatGPT is allowed to give the owner a Codex QA prompt, ChatGPT must perform a round-trip proof through the same logical input path Codex will consume:

```text
frozen exact artifact
→ write/publish to Codex-accessible transport
→ read/download/reassemble it back from that transport
→ SHA-256 equals frozen expected SHA
→ byte count equals frozen expected byte count
→ archive opens/integrity check passes
→ extracted path/file identity matches frozen authority where applicable
→ only then authorize Codex prompt
```

If the transport uses an encoded representation, the round-trip proof must decode/reassemble the **exact artifact bytes**, not merely verify the representation text itself.

If ChatGPT cannot complete this round-trip proof, `AUTHORIZED_NEXT_STAGE` cannot be Codex execution through that transport.

The 2026-08-19 14999-byte GitHub object incident is the permanent negative example: `create_blob`/commit success was incorrectly treated as transport proof even though Codex later received a non-ZIP object instead of the frozen 209505-byte ZIP. That class of mistake is forbidden.

### C. Exact-artifact transport precedence

When an exact frozen ZIP already exists, transport choices have mandatory precedence:

```text
1. proven direct exact-ZIP transport;
2. another byte-safe direct exact-ZIP transport with round-trip proof;
3. byte-safe encoding of the EXACT ZIP bytes (for example base64 split into text chunks), followed by independent reassembly to the exact frozen ZIP and SHA/byte/open proof;
4. reconstruction from source/preimage/patch ONLY if no exact-byte artifact transport is actually possible.
```

A connector being unable to render or write arbitrary binary directly does **not** make exact-artifact transport impossible if that connector can carry a byte-safe text representation of the exact ZIP.

Do not transport a source patch and ask Codex to rebuild the primary package merely because binary upload is inconvenient when the exact ZIP bytes can instead be encoded and transported losslessly.

### D. Reconstruction is an exceptional fallback, never the default handoff

If and only if exact artifact bytes genuinely cannot be transported, reconstruction may be used. Before giving a Codex prompt, ChatGPT must prove that the published reconstruction contract is sufficient for an independent consumer to reproduce the expected exact artifact.

Required proof:

```text
published reconstruction inputs only
→ fresh independent reconstruction
→ exact target source identity
→ exact package byte identity
→ expected SHA-256
→ expected byte count
→ archive integrity
```

The independent reconstruction proof may not rely on hidden local state, an unpublished packer implementation or unstated archive defaults.

If the published contract cannot independently reproduce the expected SHA, reconstruction transport is not authorized.

### E. Packaging authority must be executable and byte-complete

For exact-byte reconstruction, prose such as “files 0644, dirs 0755, deflate level 9” is not a sufficient packaging contract.

The canonical packer or its exact executable specification must fix **every byte-affecting field**, including as applicable:

- archive entry order and explicit directory entries;
- root path and separators;
- timestamp/date fields and timezone assumptions;
- compression method, implementation/version where relevant and compression level;
- `create_system` / host OS metadata;
- UNIX file-type bits (`S_IFREG`, `S_IFDIR`) as well as permission bits;
- ZIP `external_attr` values, including DOS directory flag where applicable;
- general-purpose flags;
- filename encoding/UTF-8 flag behavior;
- `extra` fields;
- per-entry comments and archive comment;
- creator/extract version fields where the library exposes or derives them;
- CRC/content bytes;
- any other library/runtime-dependent metadata capable of changing archive bytes.

Prefer transporting the exact artifact to reproducing it. If reproducibility is required, prefer publishing/executing the exact canonical packer code over natural-language instructions.

The 2026-08-19 `8359c6cf…` reconstruction is the permanent negative example: the reconstructed source was `45/45` exact and ZIP size was 209505, but the ZIP SHA differed because the published packaging instructions did not fully specify the UNIX file-type metadata in `external_attr`. A 45/45 source match does not authorize package PASS.

### F. Consumer-conformance test before Codex prompt

When reconstruction or encoded transport is used, ChatGPT must test the **published handoff contract as a consumer would**, not merely rerun the producer's hidden local procedure.

At minimum:

1. start from a fresh location/process;
2. use only the published transport objects/instructions plus explicitly governed preexisting input;
3. do not import unpublished local variables/files/metadata;
4. reconstruct/reassemble;
5. require the exact expected artifact SHA and byte count;
6. open/extract the artifact and verify its governed identity.

Failure of this consumer-conformance test blocks the Codex prompt.

### G. Codex-prompt authorization checklist

Immediately before providing a Codex prompt, ChatGPT must answer YES to all applicable items:

```text
PROVEN_ROUTE_REUSED_OR_PROVEN_IMPOSSIBLE = YES
EXACT_ARTIFACT_FROZEN = YES
TRANSPORT_ROUNDTRIP_SHA_MATCH = YES
TRANSPORT_ROUNDTRIP_BYTES_MATCH = YES
TRANSPORT_ROUNDTRIP_ARCHIVE_OPEN = YES
TRANSPORT_CONSUMER_CONFORMANCE = YES
CODEX_CAN_ACCESS_THE_VERIFIED_INPUT = YES
OWNER_FILE_HANDLING_REQUIRED = NO
PRODUCT_BYTES_CHANGED_DURING_TRANSPORT_FIX = NO
```

Any `NO` blocks the prompt. ChatGPT must not replace a failed checklist item with explanatory prose or make Codex discover the transport defect.

### H. `FAIL_ARTIFACT` retry discipline

After `FAIL_ARTIFACT`:

- preserve the exact product candidate and production hashes unless evidence proves a product defect separately;
- fix only artifact/packaging/transport/prompt layers that actually failed;
- do not create another candidate just to make transport easier;
- do not give the owner another Codex prompt until the repaired transport itself passes the required round-trip/consumer-conformance proof;
- if the failure exposes a missing persistent invariant, canonicalize it here before the next attempt.
