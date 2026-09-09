# MK01 — CLIENT PDF REPORT CORRECTION QA

Status: **CONTENT / DATA / VISUAL / RECIPIENT QA PASS; BINARY REPO UPLOAD NOT EXPOSED BY CURRENT GITHUB CONNECTOR**

Scope: add a real recipient PDF report to the already validated MK01 XLSX without changing accepted semantic data.

Provider calls: 0. Semantic data changes: 0.

## Result

Validated client PDF:

`MK01_OKNO_MSK_CLIENT_REPORT_2026-09-09.pdf`

- pages: 6;
- byte size: 58,723;
- openable: PASS;
- encrypted: NO;
- scanned PDF: NO;
- ASCII-safe normalization is visually identical to the validated render (`changed_pages = 0`);
- SHA-256: `cfa8ab83e4c9885c3f488c8ea3041b3b231d60036437d842ba5cb8ded0b6e924`;
- source partition: `2840 / 2185 / 187 / 468`;
- groups: 59;
- group examples: taken from current cluster authority;
- Yandex-only boundary: explicit;
- Google/page architecture/competitor/AI scope leakage: 0.

## Git persistence state

Remote Git contains and has readback for:

- `CLIENT_REPORT_SPEC.md`;
- `CLIENT_REPORT_SOURCE_2026-09-09.md`;
- `build_mk01_client_report.py`;
- `CLIENT_REPORT_ARTIFACT_MANIFEST_2026-09-09.json` with exact byte size and SHA-256;
- this QA record;
- all product/deliverable/Step-10 rules requiring XLSX + PDF.

The currently exposed GitHub connector actions accept UTF-8 text contents but do **not** expose a local binary-file parameter for writing the finished PDF. Therefore this QA does not claim a direct remote binary-PDF readback that did not occur. The finished binary PDF is supplied to the owner/client as the actual artifact; the repository preserves its exact source, generator, validated hash and QA evidence.

When work is executed in an environment with normal local Git/file push capability, the binary PDF should also be committed/read back under the test/client release path.

## QA ledger

| ID | Check | Result |
|---|---|---|
| R01 | PDF exists and opens | PASS |
| R02 | Page count 4–8 | PASS — 6 |
| R03 | All 6 pages rendered and visually inspected | PASS |
| R04 | No clipping/overlap/broken glyphs | PASS |
| R05 | Site and region correct | PASS |
| R06 | 2965 Wordstat observations correct | PASS |
| R07 | 2840 preserved phrases correct | PASS |
| R08 | 2185 working-core count correct | PASS |
| R09 | 187 review count correct | PASS |
| R10 | 468 excluded count correct | PASS |
| R11 | 59 total / 54 working groups correct | PASS |
| R12 | Real cluster examples only | PASS |
| R13 | Wordstat broad-count limitation explicit | PASS |
| R14 | Yandex-only boundary explicit | PASS |
| R15 | Google excluded | PASS |
| R16 | Query→URL/architecture/TZ not claimed | PASS |
| R17 | Competitor Step5A not claimed | PASS |
| R18 | Alice/Neuro/AI not claimed | PASS |
| R19 | Internal Stage/Step/authority/provenance terminology absent | PASS |
| R20 | Initial `phrase keys` jargon defect corrected before release | PASS |
| R21 | XLSX remains primary working artifact | PASS |
| R22 | Separate TXT removed from client package definition | PASS |
| R23 | Handoff template now attaches XLSX + PDF | PASS |
| R24 | Roadmap + per-step Step 10 updated to generate XLSX + PDF | PASS |
| R25 | Report sources point to official Yandex methodology pages | PASS |
| R26 | Report source/generator/hash/QA persisted and read back remotely | PASS |
| R27 | Direct binary-PDF Git write/readback | NOT AVAILABLE THROUGH CURRENT CONNECTOR; NOT CLAIMED |

## Defects closed

### E36 — spreadsheet usability was mistaken for complete client communication

A seven-sheet XLSX is a valid working artifact but does not by itself give a non-analyst client a compact explanation of what was researched, how the result was formed and what the key numbers mean.

Correction: mandatory 4–8 page PDF report added to every MK01 delivery.

### E37 — internal QA vocabulary leaked into PDF draft

The first rendered report used the internal English term `phrase keys` in a client-visible bullet.

Correction: replaced with normal Russian wording and added explicit PDF-language/jargon scan to the release gate.

## Final client package

```text
1. seven-sheet XLSX semantic core
2. concise client PDF report
3. short Kwork/chat handoff message attaching both
```

No standalone TXT client report.
