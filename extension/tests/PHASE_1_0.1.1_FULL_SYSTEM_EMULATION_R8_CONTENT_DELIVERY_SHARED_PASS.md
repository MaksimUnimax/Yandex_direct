# FSE R8 — content / watcher / delivery / shared-function / source-guard regression

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **PASS — 90/90**.

```text
90 tests
90 PASS
0 FAIL
```

Covered:

- full Autorun model status/pause/finish/confirmed-delivery transitions;
- report-prefix N=1/N=3, clamp, due/apply/idempotent-delivery accounting;
- durable Start commit/confirmation/recovery no-redispatch rule;
- claimed/committed Wordstat delivery and worker-session-loss no-retry rule;
- popup presence/source contracts for run/manual/prefix controls;
- command watcher stable explicit Wordstat capture and one accepted block → one core execution;
- worker-owned single-flight Autorun delivery;
- exact production content runtime boot in emulator without source rewriting;
- content low-level identity/turn/toast/visibility branches;
- writing-block, legacy and generic Copy adapters/locality/discovery/decoration;
- Manual observer and execution without double submission;
- composer staging, stable Send target, send picker/profile and delivery confirmation/error branches;
- Auto watcher debounce/MutationObserver/route-resync branches;
- Manual failure after worker claim and sync-triggered recovery failure without replay;
- claimed-delivery reconciliation without a second Send;
- exact reference provenance for untouched shared modules and audited Manual-controls adapter delta;
- reference send constants and click-until-composer-empty loop;
- delivery staged by delivery id and committed before click;
- diagnostics local-only/redaction;
- outgoing SHA-256 verification before recovery staging/reconciliation;
- every exported Autorun, conversation-identity, Manual-controls, composer-send, proven-capture and Wordstat-protocol function plus residual reachable helper branches;
- manifest permissions and direct Yandex host only;
- API key worker-only storage path;
- no arbitrary URL transport;
- native Copy not prevented;
- Manual API side effect starts only from local Copy admission and duplicate in-flight command is fenced;
- result delivery never overwrites user composer text;
- Manual and Autorun remain separate explicit opt-ins.

No real/external Yandex request occurred.
