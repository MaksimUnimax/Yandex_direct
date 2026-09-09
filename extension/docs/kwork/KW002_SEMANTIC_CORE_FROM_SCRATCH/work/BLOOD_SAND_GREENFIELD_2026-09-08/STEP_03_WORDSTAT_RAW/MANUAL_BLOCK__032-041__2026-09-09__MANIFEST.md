# STEP 03 — exact raw Wordstat block M032–M041

Status: RAW PROVIDER DATA PERSISTENCE ONLY. NO ANALYSIS.
Date: 2026-09-09
Source: exact uploaded big-paste block containing 10 consecutive `WORDSTAT_RESULT_V1` envelopes.

## Exact source integrity

- source bytes: `782995`
- source SHA-256: `2c325758ec60314ba30ccf1c16116328d14d93cbea2d9a5f53ac93f1d6a03e37`
- deterministic gzip bytes (`mtime=0`, level 9): `73423`
- deterministic gzip SHA-256: `77b25daef86d13840672d2564af1cf860c94e7625fe0b510f1d6a59f43f487fb`

The original source is preserved losslessly as four binary gzip parts. Reconstruction is exact:

1. concatenate part01 + part02 + part03 + part04 in binary order;
2. verify the concatenated gzip SHA-256 equals `77b25daef86d13840672d2564af1cf860c94e7625fe0b510f1d6a59f43f487fb`;
3. gunzip;
4. verify the reconstructed source SHA-256 equals `2c325758ec60314ba30ccf1c16116328d14d93cbea2d9a5f53ac93f1d6a03e37` and byte length equals `782995`.

### Parts

| part | bytes | SHA-256 | Git blob SHA |
|---|---:|---|---|
| `MANUAL_BLOCK__032-041__2026-09-09.md.gz.part01` | 20000 | `1edf0312ea0fea5b0044b187d6f577a4a364d0c157a46d55ae5992cf8686e689` | `821481d5adb68bd9c73a4c6417b61fb8b40dbb51` |
| `MANUAL_BLOCK__032-041__2026-09-09.md.gz.part02` | 20000 | `2d929334b048a2b24c267b9fce4c1aefde9a654f75ba0172888b66edb11f7017` | `351e8008cb29e06e99cccfab21e4f83f388aeca2` |
| `MANUAL_BLOCK__032-041__2026-09-09.md.gz.part03` | 20000 | `6c5822e6ffa5b24fc3e0f9cc41c3e079b5a1b21054fcee5e6d639ddbc103ab40` | `cfcc9c9f2cdda8a5c3029050f1befa068389b002` |
| `MANUAL_BLOCK__032-041__2026-09-09.md.gz.part04` | 13423 | `78c9d0d6557e785cd56b3a6b944954a4595b1a59ea994ce03b11c5595b27a1e3` | `1263093ef28f2ecbbe6843ec236a0d2459776072` |

## Factual envelope/index check

This table is only a machine-checked inventory of the exact raw envelopes. It is not semantic/SEO analysis.

| seq | diagnostic | canonical position | seed phrase | request_id | HTTP | status | request_executed | results rows | association rows | totalCount |
|---:|---|---:|---|---|---:|---|---|---:|---:|---:|
| 1 | M032 | 32 | Аум | `wordstat-f6902fef-6fbd-41dc-8889-9349059c7914` | 200 | OK | true | 460 | 16 | 15635 |
| 2 | M033 | 33 | Крест Сварога | `wordstat-daf52ca4-5c1c-47e2-b8f8-e592cf8112ea` | 200 | OK | true | 11 | 18 | 366 |
| 3 | M034 | 34 | Шлем ужаса | `wordstat-f8e4f021-6c96-4162-8eb4-4148bae7b97d` | 200 | OK | true | 177 | 15 | 5599 |
| 4 | M035 | 35 | Эгисхьяльм | `wordstat-b3c2f241-80f3-4250-903a-016d5b9e568d` | 200 | OK | true | 6 | 16 | 104 |
| 5 | M036 | 36 | знак зодиака | `wordstat-0034680f-bda7-46c5-8ba7-1e7cf080f369` | 200 | OK | true | 2000 | 15 | 3512863 |
| 6 | M037 | 37 | знак зодиака Стрелец | `wordstat-cbe3ca4e-056c-4a45-96e8-f561161260fc` | 200 | OK | true | 595 | 13 | 39531 |
| 7 | M038 | 38 | знак зодиака Близнецы | `wordstat-cef67c2a-34a9-4724-bc07-41f11796dd43` | 200 | OK | true | 783 | 15 | 47689 |
| 8 | M039 | 39 | знак зодиака Весы | `wordstat-deefb197-f237-4761-93e3-132608bc6124` | 200 | OK | true | 818 | 19 | 64242 |
| 9 | M040 | 40 | знак зодиака Водолей | `wordstat-03e9a100-bd5c-450c-b9c6-9c65915ec0f9` | 200 | OK | true | 569 | 19 | 37900 |
| 10 | M041 | 41 | знак зодиака Дева | `wordstat-73422929-ec25-4b7d-8ed0-eca43ab784a4` | 200 | OK | true | 952 | 18 | 101545 |

All ten raw envelopes state: `service=wordstat`, `operation=getTop`, `numPhrases=2000`, `regions=["225"]`, `devices=["DEVICE_ALL"]`, `automatic_retry=false`.

No phrases/results/associations were filtered, normalized, deduplicated, interpreted, scored, or otherwise analyzed for this persistence artifact.