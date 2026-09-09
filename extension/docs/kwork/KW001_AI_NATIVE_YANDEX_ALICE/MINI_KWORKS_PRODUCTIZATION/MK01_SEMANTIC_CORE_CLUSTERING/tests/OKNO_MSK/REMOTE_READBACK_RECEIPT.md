# MK01 / OKNO_MSK — remote readback receipt

Статус: **PASS / G12 CLOSED FOR REHEARSAL RESULT + QA + METHOD CORRECTIONS**

Дата: **2026-09-09**  
Repository: `MaksimUnimax/Yandex_direct`  
Branch: `roadmap/kwork-productization-2026-08-28`

## История Phase 5 до закрытия G12

| Блок | Remote commit | Readback |
|---|---|---|
| Начальный live branch state | `99f748ecc0ff83afd064d99717c24b93222d3b23` | подтверждён до первой записи |
| Source authority + mock order | `214b32f5721bd65e420b0455386e96f2d42a7ce6` | commit и оба Markdown-файла прочитаны с remote |
| Standalone materialization | `c2d728b8f0411a933909bb51bf3c5fc78fd4d6a8` | manifest, XLSX, compressed universe, execution log прочитаны с remote |
| Corrected QA/method/result block | `9ea0143c4c5370a8e7b49a858596da79076d52a9` | commit, tree, QA JSON, manifest, XLSX, reports и method ledger прочитаны с remote |

При параллельных изменениях branch каждый локальный блок накладывался только после fetch/fast-forward. Force push не применялся.

## Remote identity текущего QA block

```text
remote commit = 9ea0143c4c5370a8e7b49a858596da79076d52a9
commit title = qa(mk01): validate OKNO_MSK standalone rehearsal
local tree = 65ce29a71ed20d4bc91b5578bd3829e38ecb6a13
remote tree = 65ce29a71ed20d4bc91b5578bd3829e38ecb6a13
tree identity = PASS
```

## Ключевые remote artifacts

| Artifact | Remote Git blob | Readback result |
|---|---|---|
| `MK01_REHEARSAL_QA_2026-09-09.json` | `a5455f7b375012283e3dcbad181aa4fb7467c3d6` | PASS, 50 checks, 0 failures |
| `MK01_MATERIALIZATION_MANIFEST_2026-09-09.json` | `d975c55b618603449a19a605fecdf25fba2fa450` | PASS, counts and hashes parsed |
| `MK01_OKNO_MSK_SEMANTIC_CORE_2026-09-09.xlsx` | `4b8d416731ee98fc749c2b01458b2002690d4c6d` | base64 content readable; 648049 bytes in manifest; 7 sheets |
| `MK01_SEMANTIC_UNIVERSE_2026-09-09.tsv.gz` | `93c5473cfb71b4fc9245b9620ee30bc991a21e5b` | base64 content readable; 2840 data rows in manifest |
| `MK01_CLUSTER_SUMMARY_2026-09-09.tsv` | `f232a64ab44ccc5ea686b48c5893becb88000419` | UTF-8 content readable; 59 data rows counted remotely |
| `MK01_WORKBOOK_BUILD_REPORT_2026-09-09.json` | `2bd1b3b3afce4faa44a423ec7547a004faa08741` | readable |
| `VISUAL_QA_RECEIPT_2026-09-09.json` | `d23548f57477e178ca7bbbc48909f575398678de` | readable |
| `QA_REPORT.md` | `3510c52576ab3e2136bad2a14466f1709e79dc6e` | readable; G12 was pending at publication time and is closed by this receipt |
| `RECIPIENT_REVIEW.md` | `d69e034d279a5115f377bd3c94f54ce376878ea7` | PASS content readable |
| `REHEARSAL_METRICS.md` | `8477f4c56a984d1c88cd0fa07781b468eea7d5dd` | measured facts readable |
| `SOURCE_AUTHORITY_AUDIT.md` | `b067f41a5f073b25774fef27424c5c883b6aeee8` | pre-Step5A proof readable |

## Remote count readback

Из remote manifest и remote QA JSON повторно прочитано:

```text
source occurrences = 2965
source universe = 2840
working core = 2185
review / uncertain = 187
excluded = 468
clusters = 59
Search decisions = 75 = 66 universe joins + 9 control anchors
Step5A contamination = 0
provider calls during rehearsal = 0
machine QA = 50 PASS / 0 FAIL
recipient review = PASS
```

## G12 conclusion

```text
SAVE = PASS
COMMIT = PASS
NON_FORCE_REMOTE_UPDATE = PASS
REMOTE_COMMIT_READBACK = PASS
REMOTE_TREE_IDENTITY = PASS
REMOTE_TEXT_READBACK = PASS
REMOTE_XLSX_BLOB_READBACK = PASS
REMOTE_DATASET_COUNT_READBACK = PASS
G12 = PASS
```

Roadmap/final-state commit is created only after this G12 closure and receives its own branch-HEAD readback before Phase 5 is reported complete.
