# Step 11 correction session note

Date: 2026-08-31

This correction session was opened after external method audit identified two non-repeat requirements:

1. Any Bridge or Codex acquisition result used by a job must be persisted to the canonical GitHub job workspace immediately after the interaction and read back/verified before the next acquisition interaction. The reason is durability: a successful provider/Codex interaction is not a durable project result until the full required output is saved and verified; otherwise a later context/tool interruption can lose evidence that cannot be reconstructed cheaply or exactly.
2. Page ownership is not complete at cluster-only granularity. After cluster→owner decisions, the job must materialize the join from the final phrase assignment ledger to ownership so every active assigned phrase has an inspectable `phrase → cluster → target URL/state` row. The reason is auditability and deliverable usability: cluster-level logic is valid, but without the materialized phrase-level map the client/analyst cannot directly verify which phrases belong to each page and QA cannot prove full row coverage.

This note is temporary provenance for the correction run; canonical permanent rules are to be written to the registered Step-11 methodology/lessons artifacts and the corrected Step-11 final report/QA.
