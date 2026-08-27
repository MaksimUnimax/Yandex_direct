# AI-native blood_sand — Pass B source manifest

Date: 2026-08-27

```text
frozen_blood_sand_commit = 0da1fdfa65155fe0b22d67838d366e7d214ccbbe
immutable_pass_a_commit = 9501af0da39c671f578f56bb56dad311f2d9c761
pass_b_freeze_commit = d0cad99be1c1cf70ad06d3cf7bf28495daab58b8
fresh_provider_requests = 0
```

Pass B uses exactly the same non-AI baseline frozen in Pass A, then adds canonical consumer-Alice evidence from the frozen `blood_sand` commit.

## Canonical added Pass B sources actually inspected before freeze

```text
marketing/research/R2_PRIMARY_SEARCH_ALICE_COMPARISON_2026-08-26.md
marketing/research/R2_YANDEX_SERP_ALICE_FINAL_REPORT_2026-08-26.md
marketing/data/normalized/alice/20260826T0734Z__pechat_velesa.csv
marketing/data/normalized/alice/20260826__alatyr_obereg.csv
marketing/data/normalized/alice/20260826__obereg_v_mashinu.csv
marketing/data/normalized/alice/20260826__obereg_veles.csv
marketing/data/normalized/alice/20260826__vegvizir.csv
marketing/data/normalized/alice/20260826__podarok_muzhchine_v_mashinu.csv
marketing/data/normalized/alice/20260826__podarok_muzhchine_v_mashinu__CONTEXT_CONTAMINATED.csv
```

The contaminated gift observation is included only as provenance/contamination evidence and remains `EXCLUDED_FROM_PRIMARY`; the clean rerun is canonical.

## Deliberately not used to generate Pass B

Final R3/opportunity outputs were not opened until after Pass B commit `d0cad99...` was created. They may be used only as a post-freeze consistency check.

No web source, fresh provider call, inferred Alice fan-out, or unobserved source URL was promoted to observed evidence.
