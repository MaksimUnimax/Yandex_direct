# STEP 03 — exact Wordstat raw block M042–M051

This manifest records persistence only. No provider phrase row was filtered, deduplicated, normalized, classified, or semantically analyzed.

## Source integrity

- Source: owner-supplied exact manual Wordstat delivery block for canonical items 42–51.
- Uncompressed raw bytes: `703355`
- Uncompressed raw SHA-256: `98a4fa9966d95f0149f45a635ffe7c1737a63512c7a8946d4c8de8c826af5fed`
- Deterministic gzip bytes: `66784`
- Deterministic gzip SHA-256: `ba220113f04060d60e717468ee9256bfd603630e2803bb05aa3fc29f85e4f194`

Reconstruction:

```bash
cat MANUAL_BLOCK__042-051__2026-09-09.md.gz.part01 \
    MANUAL_BLOCK__042-051__2026-09-09.md.gz.part02 \
    MANUAL_BLOCK__042-051__2026-09-09.md.gz.part03 \
    MANUAL_BLOCK__042-051__2026-09-09.md.gz.part04 \
    MANUAL_BLOCK__042-051__2026-09-09.md.gz.part05 \
    MANUAL_BLOCK__042-051__2026-09-09.md.gz.part06 \
    MANUAL_BLOCK__042-051__2026-09-09.md.gz.part07 \
    MANUAL_BLOCK__042-051__2026-09-09.md.gz.part08 \
    > MANUAL_BLOCK__042-051__2026-09-09.md.gz
sha256sum MANUAL_BLOCK__042-051__2026-09-09.md.gz
gunzip -c MANUAL_BLOCK__042-051__2026-09-09.md.gz > MANUAL_BLOCK__042-051__2026-09-09.md
sha256sum MANUAL_BLOCK__042-051__2026-09-09.md
wc -c MANUAL_BLOCK__042-051__2026-09-09.md.gz MANUAL_BLOCK__042-051__2026-09-09.md
```

Expected checks:
- gzip SHA-256 = `ba220113f04060d60e717468ee9256bfd603630e2803bb05aa3fc29f85e4f194`
- gzip bytes = `66784`
- raw SHA-256 = `98a4fa9966d95f0149f45a635ffe7c1737a63512c7a8946d4c8de8c826af5fed`
- raw bytes = `703355`

## Part inventory

| Part | Bytes | SHA-256 | Git blob SHA |
|---|---:|---|---|
| part01 | 5000 | `63c74a37a18a6d416412013fa796df649d729cdde426eb9bca43aa675822bb96` | `a03a8c050bbcfcc5334ff870f95b02b2ceffe8ba` |
| part02 | 5000 | `31946d6fc214a40b330e8b62c58f5ddda4f27d2366e7ccacb50efc54c1f9ae8c` | `4ede0ed82f8817f23117658aa7a392ba6c9208f9` |
| part03 | 10000 | `60b4c94fda711e328352b2af57e77995e182ae5eb63ed92f554662541c953868` | `6a377c3eb9e987fa8a4e12fa715fecc00143da10` |
| part04 | 10000 | `a09f1d1e7f7a15fc874f27b86d0bc45916cfe6761ddef7c558501382da74cc40` | `811076c9a117e10553afcc1b6dffe1ce2fc66b5f` |
| part05 | 10000 | `f287b7e561cce9a79ca99d073ac159e145cc5f7a6a57fbef89ad6e31ee0d546f` | `c0edf3c31566b9d24094efb754812fd96dfb7c9b` |
| part06 | 10000 | `d15f7a4190cbb2ece53ca9ce09adec4177cb7ad959f5ade3c6b615d1eba50468` | `65508dd0a9c8960f0cc84a737ad6de16a9b2dd17` |
| part07 | 10000 | `1472a63381e3ef3de7fe732749368a93014e3b5bb3c6ba4ec2f08f326cba7d55` | `364e7d855668371da9b9eef76566558345269e3f` |
| part08 | 6784 | `9aa2b31caa4fafba1e9d888daefe5f248f90843f42dd131159ad9f3b30f5c9cf` | `d38b25dbc43c7d399cf4f1f4eae1dd57476a2329` |

## Exact envelope inventory

Common request authority for all ten envelopes: `service=wordstat`, `operation=getTop`, `numPhrases=2000`, `regions=["225"]`, `devices=["DEVICE_ALL"]`, `automatic_retry=false`, `request_executed=true`.

| Canonical item | Phrase | Request ID | HTTP / status | results rows | associations rows | totalCount / raw result |
|---:|---|---|---|---:|---:|---|
| 42 | `знак зодиака Козерог` | `wordstat-d39bb2e9-2b97-4c7e-b1af-264d9b86df69` | 200 / OK | 548 | 16 | `34189` |
| 43 | `знак зодиака Овен` | `wordstat-07c630e8-dd95-4e74-a036-9d01f3a9ecbc` | 200 / OK | 593 | 15 | `37752` |
| 44 | `знак зодиака Лев` | `wordstat-d09d1a74-900c-4107-9770-054cf4c0b592` | 200 / OK | 1074 | 14 | `108619` |
| 45 | `знак зодиака Рак` | `wordstat-bd7fb281-180a-4973-a05c-103b4d7b96a4` | 200 / OK | 987 | 14 | `67198` |
| 46 | `знак зодиака Рыбы` | `wordstat-cff4bf6c-1272-43d5-8af8-dad9643796d6` | 200 / OK | 915 | 18 | `68815` |
| 47 | `знак зодиака Скорпион` | `wordstat-57268c34-c203-4ea9-9f28-0cef4284d00d` | 200 / OK | 809 | 17 | `57861` |
| 48 | `знак зодиака Телец` | `wordstat-24ddaafc-4e79-4bec-9130-f97e7c0e1175` | 200 / OK | 594 | 15 | `37962` |
| 49 | `(амулет|оберег|талисман) RSOTM` | `wordstat-264f6931-a835-4b2e-8ca2-82999484277c` | 200 / OK | — | — | exact provider `result:{}` |
| 50 | `(амулет|оберег|талисман) Soldier Of Fortune` | `wordstat-619ef51a-c0a8-4a6b-9f7e-4f1709aae204` | 200 / OK | — | — | exact provider `result:{}` |
| 51 | `(амулет|оберег|талисман) Бусидо Путь Воина` | `wordstat-2e63726e-3660-4838-b5d4-b56bbfcb00f5` | 200 / OK | — | — | exact provider `result:{}` |

The three empty `{}` provider results are preserved as returned and are not reclassified as provider errors.
