# Phase 5 credential race classification

Status: **FAIL_PRODUCT — frozen candidate superseded**

Affected frozen source: `764e6f63ebd8db1f6e10d0cd03c0169b48318978`

Affected product tree: `a8ef5239a770f0321debd8322dcfadadff88e272`

Affected frozen ZIP SHA-256: `fcfb19c774bc2d3ce2e6ca14b0c5056d48f680ec748a6a1c52ddf89aafa49f54`

Deterministic evidence:

- a stale credential migration write can erase a concurrently completed Direct credential save;
- two concurrent per-service credential saves can lose one service record;
- the installed Direct Manual lifecycle independently observed a `NO_CREDENTIALS` skip after a controlled Direct save during a flaky startup interleaving.

Required product correction:

- serialize credential-store mutations inside the worker runtime;
- re-read the latest credential store inside the serialized mutation before any write;
- make migration persistence participate in the same serialization;
- make settings Backup import participate in the same credential mutation serialization;
- preserve five independent credential records; no credential/token unification.

The old frozen candidate must not be used for owner-live or final Codex PASS.
