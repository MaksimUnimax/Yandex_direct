# B19 — exact 0.1.6 final package / fresh-extraction checkpoint

Date: 2026-09-13.

This checkpoint freezes the exact owner-candidate package bytes **before independent Codex acceptance**. It is not yet permission to hand the ZIP to the owner.

## Exact production

- Version: `0.1.6`
- Product tree SHA-256: `b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86`
- Product files: `67`
- Deferred Operation host permission: enabled exactly once
- `chrome.alarms`: absent
- Deferred Search: Manual-only
- Background deferred polling: disabled

## Exact deterministic installable ZIP

Filename:

`Yandex-Marketing-Bridge-0.1.6.zip`

SHA-256:

`81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2`

Bytes: `220045`

The package builder produced two independent deterministic ZIP outputs A/B with the same bytes. Fresh extraction was checked path-by-path and byte-by-byte against the canonical 67-file source tree. Extracted tree identity is exactly the production tree above.

The ZIP has one root directory:

`Yandex-Marketing-Bridge-0.1.6/`

CRC verification: PASS.

## Canonical package qualification run

GitHub Actions run: `34737506830`

Artifact:

- id: `10311695957`
- name: `ymb-0.1.6-final-owner-candidate`
- artifact SHA-256: `07d9b9e70181983172b7af448e07e087ec9551144905562e506053670c40b059`
- artifact bytes: `225323`

The artifact contains the exact installable ZIP plus package/source hashes and browser evidence.

### Fresh-extracted Chrome qualification

The tests installed **fresh-extracted bytes from the deterministic ZIP**, not the repository source directory.

Resource group:

- cases: `16`
- failures: `0`
- remaining processes: `0`
- peak owned Chrome RSS: `1811652 KiB`

Deferred-network group:

- cases: `9`
- failures: `0`
- remaining processes: `0`
- peak owned Chrome RSS: `1304112 KiB`

Whole package gate:

- browser failures: `0`
- peak owned Chrome RSS: `1811652 KiB`
- emergency safety limit: `2097152 KiB`
- real Yandex provider calls: `0`
- controlled provider fixtures only
- `FINAL_PACKAGE_GATE.pass = true`

The network group covers the accepted Manual deferred contour:

`start -> searchAsync POST -> persisted operation ID -> Operation GET -> saved raw -> normalize -> normal delivery`

plus command-injection containment, Manual-off blocking, and UNKNOWN/no-auto-retry behavior.

## Preserved package QA failures

The first two package workflows are deliberately not relabeled PASS:

1. attempt 1 built the deterministic ZIP and proved extraction identity but tried to consume `$GITHUB_ENV` variables in the same shell step; browser tests never ran. `FAIL_HARNESS`.
2. attempt 2 again proved the same ZIP SHA/bytes and exact extraction, then the resource harness failed before product assertions because the controlled B15 fixture was saved as `fixture.html` while the preserved harness expected `b15_fixture.html`. The finalizer correctly rejected zero browser cases. `FAIL_HARNESS`.
3. attempt 3 supplied both QA-only fixture names and completed resource + network browser qualification. PASS.

No production byte changed between these package attempts.

## Development gates already passed on the same production tree

- Node gate: original 132, Wordstat/Debug/backup 78, full network contract 99, modules 254, export 84, delivery/recovery 69, JS syntax 61 — zero fail/skip/cancel.
- Real-Chrome full resource gate on canonical source: PASS.
- Real-Chrome deferred network gate on canonical source: PASS.
- Deterministic ZIP / fresh extraction / fresh-extracted Chrome resource + network: PASS.

## Remaining release boundary

The exact package above is now ready for **independent Codex pre-delivery QA**. Development QA does not substitute for that independent verdict.

Until independent PASS is returned on this exact ZIP SHA:

```text
B19_FINAL_PACKAGE_GATE = PASS
INDEPENDENT_CODEX_GATE = NOT_RUN
RELEASE_ALLOWED = NO
OWNER_INSTALLABLE_HANDOFF = FORBIDDEN
```

Any production-byte modification after this checkpoint invalidates this package SHA and requires a new package/fresh-extraction gate and independent verdict.

## ПРОСТЫМИ СЛОВАМИ

Полная 0.1.6 уже собрана в настоящий ZIP. ZIP дважды собрался одинаково, распаковался без отличий, и именно распакованная сборка прошла Chrome-проверку памяти/файлов и нового deferred Search. Сейчас меня держит только одно правило: независимый Codex должен принять **этот конкретный ZIP с SHA `81d47a...`**. До этого я файл владельцу не выдаю.
