# Reference artifacts

This directory is reserved for immutable reference material used to build Yandex Marketing Bridge.

Canonical supplied baseline recorded on 2026-08-12:

```text
wordstat-bridge-v1.1.5-full-function-environment-audit(4).zip
SHA-256: a39bbe65b046ef6eac5a7890b8afd84e69550db34debf271b7c373d08a1fef1a

WORDSTAT_BRIDGE_DOCUMENTATION_APPEND_ONLY_FULL_FUNCTION_ENVIRONMENT_AUDIT(4).md
SHA-256: 437a69022b31621d7a749e3b92c0faf0c45f3d7be60e1a901cda65c3faf0a25a
```

See `../docs/REFERENCE_BASELINE.md` for provenance and the reference contract.

## Rule

Reference artifacts are evidence, not the writable product source tree. They must not be silently edited to implement the unified bridge.

New implementation belongs under `extension/src/`; unified tests belong under `extension/tests/`.

If an exact binary/reference copy is added here, its recorded hash must match the canonical hash above.
