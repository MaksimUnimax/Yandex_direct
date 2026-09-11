# MK03 Phase 5 — analytical PDF exact-file QA

Status: **PASS**

Exact tested file:

`artifacts/MK03_COMPETITOR_SEMANTIC_GAP_OKNO_MSK_2026-09-11.pdf`

- SHA-256: `2fe05ba553528aeb682b7df38ac6318fc6956e9ed6350d87ec8e4d79a635914c`
- bytes: `83502`
- pages: `13`
- parsed pages: `13/13`
- exact-final-byte rendered pages: `13/13`
- page size: A4, portrait
- encryption: none
- embedded Cyrillic fonts: DejaVu Sans and DejaVu Sans Bold
- forbidden client-visible process tokens from the QA denylist: `0`

## Render receipt

| Page | Render SHA-256 |
|---:|---|
| 1 | `445bc6cb4c0ccc2831ce19d997e15c5624059ed5521e34b4e4549c0e93af2707` |
| 2 | `961c4769ea0fcc9625fea647736802f463282b73917d4f5fd7c5d839307f770e` |
| 3 | `ab5215e8b3a133b1080ce4c61fc00ccdac0df3c3df2790a7c7011bdac50ae960` |
| 4 | `23bb0338ce04530551dbab59a8b679e38a9516468d724d67386187dffb9476fb` |
| 5 | `d56f52e929dcda3607f09df411cc617c4bb56ef9efc3e704a8c4c4a642b7098d` |
| 6 | `1f1fe7caacf6253f167669ffbad8b48f1526ff70982ae2aa3ae5c6f985a3766f` |
| 7 | `db0b43712f8140442e8be20735bd2297570a2b2ebf6e51c93e4d1198b3c59b02` |
| 8 | `7bebd5e608c43c8db7802a73e524fbfc97dfb817a1a90b1e6bd54af990506f0e` |
| 9 | `0c3ae259ed8dfff47d1367e395983a62a12442a0e807551e3e4d6cc46624100f` |
| 10 | `b2a54430c66522c896ea236556955214e9d49ed6de3887df7cecae571d4d1b13` |
| 11 | `f83f093e42ea85adef69061c28833923c956e7a198fd9af41c5e660dbf9acc04` |
| 12 | `b3ca476b74d2209474d6967f440da04c4f68876a2934e5bb9b73bfaac99513ea` |
| 13 | `ae77c2516ee63e36d08a16aec44392deee41576e5273e1c84f3ba073fa4104a7` |

## Visual inspection

Every rendered page was inspected. Checks included clipping, overlap, broken Cyrillic glyphs, unreadable tables, orphan headings, isolated table rows, weak page flow and excessive blank pages.

The first build failed visual QA because one `ALREADY_COVERED` explanatory block moved to an almost empty page. That render receipt was invalidated. The register was redesigned as a compact two-column list, the PDF was rebuilt, and all 13 exact final pages were rendered again.

Final verdict:

- clipping: `0`;
- overlaps: `0`;
- broken glyphs: `0`;
- orphan headings/rows: `0`;
- unintended blank pages: `0`;
- unreadable tables: `0`;
- final-byte visual QA: **PASS**.

## Content checks

- all terminal accounting `7 / 23 / 3 / 10` is visible;
- the evidence funnel `75 / 750 / 237 / 9 / 44 / 92 / 43 / 14 / 160 / 9 / 7 / 2 / 81` is visible;
- the 9 actual competitors and their 44-page inspection coverage are visible;
- all 7 confirmed opportunities show an individual Wordstat value;
- all 10 holds and all 3 off-scope directions are visible;
- 63 tested query-domain pairs are distinguished from 18 unknown-outcome pairs;
- the report states that no page-creation decision was made;
- complete row-level detail is explicitly delegated to the XLSX;
- limitations and claim boundaries are client-readable.
