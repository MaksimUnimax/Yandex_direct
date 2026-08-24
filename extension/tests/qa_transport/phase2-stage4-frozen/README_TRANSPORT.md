# Phase 2 Stage 4 exact Git transport mirror

QA-only transport for the already frozen candidate.

Frozen source commit: `1869d17f3cb64417a07088de18dafa5687c83840`

Exact ZIP SHA-256: `0f0b035c6bc04da841d549182c3dcea6e7cf10074eddebafdf1c3a4c21c98411`

Exact ZIP bytes: `170726`

This branch is not a product candidate and does not redefine the frozen source. Its purpose is only to make the exact already-frozen ZIP available through normal Git checkout. `verify_exact_artifact.py` must pass after a fresh checkout before this transport is considered consumer-conformant.
