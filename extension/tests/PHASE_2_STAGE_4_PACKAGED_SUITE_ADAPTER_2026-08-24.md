# Phase 2 Stage 4 — governed packaged-suite adapter

Date: 2026-08-24  
Status: **QA HARNESS AUTHORITY / PRODUCT BYTES UNCHANGED**

## Problem exposed by pre-Codex PD-03 preflight

The exact frozen installable ZIP uses the established package layout:

```text
<package-root>/manifest.json
<package-root>/service_worker.js
<package-root>/content_script.js
<package-root>/shared/*
<package-root>/tests/*.test.mjs
```

The reconstructed repository tests intentionally use repository layout while developing:

```text
extension/src/*
extension/tests/*.test.mjs
```

and many tests resolve runtime files through `../src`.

Therefore invoking the tests directly in the installable ZIP root is not a valid test venue: the first pre-Codex attempt returned 41 file-level failures with `ENOENT .../src/...`. This did not prove a product failure because the tested runtime bytes were present at the installable package root exactly as governed.

## Governed solution

Use:

```text
extension/tests/qa_transport/phase2-candidate/run_packaged_suite.py
```

The adapter never rewrites the handoff ZIP and never edits production/test bytes.

It performs:

```text
1. verify exact ZIP SHA-256 and byte count against frozen manifest;
2. verify ZIP integrity, root, file count, entry count and every payload path/bytes/SHA row;
3. fresh-extract the exact ZIP;
4. create a temporary test-only repository layout:
     package runtime bytes -> <temp>/src/**
     package test bytes    -> <temp>/tests/**
5. verify every staged copy has the same byte count and SHA-256 as the manifest row;
6. run node --check over staged JS/MJS;
7. parse staged manifest.json and package.json;
8. run the complete staged `tests/*.test.mjs` suite;
9. delete/recreate work directories on each fresh run as controlled by the caller.
```

This is a QA execution adapter, not a substitute artifact and not a reconstructed product. Product assertions execute against byte-identical files copied from the exact extracted handoff ZIP.

## Two stale QA assertions found during preflight

After staging removed the path-layout failure, the old frozen test set reached 229/231 and exposed exactly two stale assertions introduced before Stage-3 owner/live-tab fences were finalized:

1. `popup_error_boundary_recovery.test.mjs` created an active Autorun without `tab_id`, so the current owner-aware popup correctly disabled Pause for a non-owner/unknown-owner context.
2. `search_manual_worker.test.mjs` attempted conversation-scoped `report_prefix_enabled` mutation without an owner `tab_id`, so the current worker correctly rejected it with `OWNER_TAB_REQUIRED`.

QA-only corrections:

```text
53c415c5f984f004705b401bd788673b0d2064c1
  test: align popup error boundary with Autorun owner tab

84a8ea01f815bb5da28da2b5c9bdc1c456739fdc
  test: pass owner tab for report prefix toggle
```

Local fresh staged validation after those two exact corrections:

```text
two directly affected test files: 16/16 PASS
complete staged suite: 231/231 PASS
fail: 0
skipped: 0
```

No production source file was changed by these corrections.

## Freeze consequence

Root-level `extension/tests/*.test.mjs` are part of the governed handoff ZIP, so changing test bytes invalidates the previous frozen ZIP identity even though production bytes are unchanged.

Required sequence:

```text
QA fixes committed
→ freeze a new exact ZIP from the new QA-source authority
→ deterministic rebuild PASS
→ source suite 231/231 PASS
→ packaged suite via this adapter 231/231 PASS
→ transport round-trip PASS
→ only then authorize Codex complete PD-00..PD-17 campaign
```

The superseded `0f0b035c...` ZIP remains evidence of the first freeze/preflight but is not eligible for final Codex PASS after the packaged-suite QA corrections.
