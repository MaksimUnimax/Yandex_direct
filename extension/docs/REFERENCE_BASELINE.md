# REFERENCE BASELINE

Status: canonical reference declaration.
Date recorded: 2026-08-12.

## Supplied reference

The owner supplied the following reference artifacts for Yandex Marketing Bridge development:

1. `wordstat-bridge-v1.1.5-full-function-environment-audit(4).zip`
2. `WORDSTAT_BRIDGE_DOCUMENTATION_APPEND_ONLY_FULL_FUNCTION_ENVIRONMENT_AUDIT(4).md`

These artifacts are not a design suggestion only. They are the concrete reference implementation/baseline from which proven ChatGPT browser-control mechanisms are to be reused or adapted.

## SHA-256

```text
ZIP
A39BBE65B046EF6EAC5A7890B8AFD84E69550DB34DEBF271B7C373D08A1FEF1A

Documentation
437A69022B31621D7A749E3B92C0FAF0C45F3D7BE60E1A901CDA65C3FAF0A25A
```

Hashes are recorded from the exact uploaded files visible in the development session on 2026-08-12.

## Reference package observed structure

The ZIP contains `wordstat-bridge-v1.1.5/` with, among other files:

```text
manifest.json
content_script.js
service_worker.js
popup.html
popup.js
popup.css
package.json
README.txt

shared/
  autorun_model.js
  composer_send.js
  conversation_identity.js
  manual_controls.js
  proven_writing_block_capture.js
  wordstat_protocol.js

tests/
  protocol.test.mjs
  protocol_edges.test.mjs
  manual_mode.test.mjs
  conversation_binding.test.mjs
  conversation_isolation.test.mjs
  autorun_model.test.mjs
  autorun_source.test.mjs
  worker_recovery_integration.test.mjs
  delivery_singleflight_50.test.mjs
  content_runtime_exhaustive.test.mjs
  worker_every_function.test.mjs
  popup_runtime_exhaustive.test.mjs
  ...
```

The supplied archive contains 44 ZIP entries and approximately 704,719 bytes of uncompressed content.

## Reference capabilities to preserve as baseline behavior

The canonical documentation establishes/reference-proves the following architectural concepts that are directly relevant to the unified bridge:

- local writing/code-block Copy as controlled operator surface in manual mode;
- native Copy remains functional;
- generic assistant-level Copy Response is excluded;
- current writing-block and legacy code-block handling;
- conversation-scoped manual state;
- conversation-scoped autorun state;
- Start / Pause / Resume / Finish lifecycle;
- stable assistant-turn/writing-block watcher;
- proven writing-block extraction;
- command protocol validation after extraction;
- in-flight/single-flight duplicate protection;
- owner/conversation isolation;
- composer overwrite protection;
- one Send action without blind click retry loops;
- no blind retry of unresolved paid requests;
- credentials isolated from ChatGPT command/report;
- allowlisted endpoint/method model;
- result prefix separated from clean evidence;
- source tests, exact packaged ZIP tests and real Chrome/production ChatGPT acceptance treated as separate evidence layers.

## Reference immutability rule

Files under `extension/reference/` are reference evidence and must not be silently edited to become the new product.

The new product is developed separately under `extension/src/` and `extension/tests/`.

If a reference file must be annotated, the annotation belongs in `extension/docs/`, not by modifying the reference artifact.

## Documentation history rule

The supplied Wordstat documentation itself is append-only by its own canonical rules. We preserve it as supplied.

The unified project additionally uses `extension/docs/DEVELOPMENT_CONTEXT_APPEND_ONLY.md` as its own append-only chronological development/context log.
