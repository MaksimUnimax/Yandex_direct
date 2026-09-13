# B19 — owner waiver: independent Codex gate skipped

Date: 2026-09-13
Repository: `MaksimUnimax/Yandex_direct`
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`

## Owner decision

The owner explicitly instructed in the main ChatGPT conversation: **skip the Codex gate** (`пропускаем кодекс гейт`).

This is an owner waiver of the independent Codex pre-delivery campaign for the already frozen B19 Yandex Marketing Bridge 0.1.6 candidate.

This waiver MUST NOT be recorded as Codex PASS. The truthful classification is:

```text
INDEPENDENT_CODEX_GATE = WAIVED_BY_OWNER
INDEPENDENT_CODEX_GATE_EXECUTED = NO
INDEPENDENT_CODEX_GATE_PASS = NO
```

## Exact candidate covered by the waiver

- version: `0.1.6`
- install ZIP: `Yandex-Marketing-Bridge-0.1.6.zip`
- install ZIP SHA-256: `81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2`
- install ZIP bytes: `220045`
- extracted tree SHA-256: `b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86`
- product files: `67`
- final package run: `34737506830`
- final package artifact id: `10311695957`
- final package artifact: `ymb-0.1.6-final-owner-candidate`

No production bytes are changed by this waiver.

## Existing completed qualification retained

The owner waiver does not erase or rewrite completed B19 development qualification:

- canonical Node gate: PASS;
- resource Chrome gate: PASS;
- deferred Search controlled-network Chrome gate: PASS;
- deterministic package gate: PASS;
- fresh extraction identity: PASS;
- fresh-extracted Chrome checks: PASS;
- direct GitHub artifact transport/readback: PASS;
- exact ZIP latest recheck: PASS;
- real Yandex provider calls during qualification: `0`;
- real owner credentials used: `false`;
- owner browser/profile touched: `false`.

The skipped layer is only the separate independent Codex PD-00..PD-17 execution campaign.

## Release decision after explicit owner waiver

Because the owner explicitly waived the only remaining independent Codex release blocker, project state may advance without claiming that gate passed:

```text
INDEPENDENT_CODEX_GATE = WAIVED_BY_OWNER
RELEASE_ALLOWED = YES_BY_OWNER_WAIVER
OWNER_INSTALLABLE_HANDOFF = ALLOWED_WITH_WAIVER_DISCLOSURE
```

Any future report or recovery must preserve the distinction between **development qualification PASS** and **independent Codex gate WAIVED/NOT EXECUTED**.

If a future owner instruction reinstates independent QA, use `B19_FINAL_PD_EXECUTION_MAP.md` and `B19_INDEPENDENT_CODEX_GATE_PROMPT.md` on the same exact ZIP unless production bytes have changed.
