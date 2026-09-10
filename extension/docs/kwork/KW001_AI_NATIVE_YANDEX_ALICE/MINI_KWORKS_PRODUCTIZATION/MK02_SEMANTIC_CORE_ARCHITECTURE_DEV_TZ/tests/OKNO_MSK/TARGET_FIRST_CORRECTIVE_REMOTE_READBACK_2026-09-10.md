# MK02 target-first corrective release — remote readback

Date: 2026-09-10
Status: **PASS**

## Publication

- Repository: `MaksimUnimax/Yandex_direct`.
- Branch: `roadmap/kwork-productization-2026-08-28`.
- Force update: **not used**.
- Concurrent remote commit preserved before publication: `bd4341fb53c36439c83b2a95ebd945d839304c0c`.
- Client-package commit: `78b5adaa8e2001e78032bf09968cf7a51de95a04`.
- QA/methodology commit: `2f30cfbe663482db1972ad17f839efdd4bdb83d9`.
- Read-back remote tree: `1b95f382b7b2b11306fea1b41eb493786a093a13`.
- Matching local release tree: `1b95f382b7b2b11306fea1b41eb493786a093a13`.

Ordinary HTTPS push could not obtain container credentials. After explicit owner authorization, the same two commits were published through the authorized GitHub connection as a fast-forward update. The connector-created commit identities differ from the original local identities, but their complete trees and every changed blob are identical.

## Changed-blob readback

All 14 changed paths were fetched from remote commit `2f30cfbe663482db1972ad17f839efdd4bdb83d9`. Result: **14/14 PASS**.

| Block | Paths | Remote blob comparison |
|---|---:|---:|
| Client files | 3 | 3/3 match |
| Client generators | 2 | 2/2 match |
| Build reports | 2 | 2/2 match |
| Machine/physical/recipient QA and validator | 4 | 4/4 match |
| Methodology and execution log | 3 | 3/3 match |
| **Total** | **14** | **14/14 match** |

## Client-file byte identities

| File | Bytes | Git blob SHA | SHA-256 |
|---|---:|---|---|
| `SEMANTIC_CORE_AND_TARGET_SEO_STRUCTURE_OKNO_MSK_2026-09-10.xlsx` | 526798 | `4fa8ed59f209524b963b6be5f62b99deae80e2e2` | `b889a682c424d101599863faabfa58fa308eddc3e8d6c7b6082bb23394c68f29` |
| `TARGET_SEO_ARCHITECTURE_REPORT_OKNO_MSK_2026-09-10.pdf` | 112331 | `01926d96003856beb7cd3fb532b41f68a6ccee06` | `c5104a3367545e3b7d9faa72b4c6961cd32d971f5f6bde8c8a33d411b1884717` |
| `TARGET_PAGE_SPECIFICATION_TZ_OKNO_MSK_2026-09-10.pdf` | 250880 | `2d9032cf4dee7c44bfcbe54b535ae858b5fd83bb` | `b40cde729464205dc417c3cbdbfab7a340d8e7cae3f2d2431f0a2e09ba7ac2a7` |

## QA readback

- Target-contract machine validator: 17/17 PASS.
- Source accounting: 2 840 = 2 185 working + 187 review + 468 excluded.
- Target-first authorities: 2 185 phrase routes, 161 cluster/task routes, 60 target roles, 60 full page specifications.
- Reconciliation: 48 keep, 7 optimize, 4 route/link change, 1 recheck.
- Physical-change delta: 14 rows and remains a subset of the 60 full page specifications.
- Physical QA: XLSX 13/13 sheets; PDFs 22/22 + 71/71 pages.
- Recipient QA: PASS.
- Client-visible internal/process-token hits: 0.
- New provider calls: 0.

## Release decision

The historical current-site-first package remains preserved as superseded evidence. The corrected target-first package is the active MK02 Phase-7 client delivery. Phase 7 is closed as PASS; the next allowed action is Phase 8 price, limits and economics.
