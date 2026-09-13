# B19 — owner installable handoff after explicit Codex-gate waiver

Date: 2026-09-13
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`

## Owner waiver basis

The owner explicitly instructed: `пропускаем кодекс гейт`.

The independent Codex gate therefore remains truthfully classified as `WAIVED_BY_OWNER`, not PASS and not executed.

Owner waiver record:
`B19_OWNER_WAIVER_SKIP_INDEPENDENT_CODEX_GATE_2026-09-13.md`

Post-waiver cursor:
`B19_POST_WAIVER_RECOVERY_CURSOR_2026-09-13.json`

## Exact handoff package

The handoff package is the already-frozen B19 owner candidate, downloaded directly from GitHub Actions artifact `10311695957` / run `34737506830` and extracted without rebuilding.

Exact install ZIP:

- filename: `Yandex-Marketing-Bridge-0.1.6.zip`
- SHA-256: `81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2`
- bytes: `220045`
- ZIP integrity: PASS, no compressed-data errors
- extracted product tree authority: `b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86`
- product files: `67`

Outer Actions artifact re-read in the handoff session:

- filename: `ymb-0.1.6-final-owner-candidate.zip`
- SHA-256: `07d9b9e70181983172b7af448e07e087ec9551144905562e506053670c40b059`
- ZIP integrity: PASS

No production files were rebuilt or modified for handoff.

## Qualification disclosure

Completed qualification retained as PASS:

- development Node regression;
- real-Chrome resource qualification;
- controlled deferred Search network qualification;
- deterministic package qualification;
- fresh extraction identity and fresh-extracted Chrome checks;
- direct artifact transport/readback;
- exact handoff-session SHA/size/CRC recheck.

Skipped by owner decision:

- independent Codex PD-00..PD-17 gate.

Therefore the package may be handed to the owner only with the truthful disclosure:

```text
INDEPENDENT_CODEX_GATE = WAIVED_BY_OWNER
INDEPENDENT_CODEX_GATE_EXECUTED = NO
DEVELOPMENT_AND_PACKAGE_QUALIFICATION = PASS
OWNER_INSTALLABLE_HANDOFF = ALLOWED_BY_OWNER_WAIVER
```
