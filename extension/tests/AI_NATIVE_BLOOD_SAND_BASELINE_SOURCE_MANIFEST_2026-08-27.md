# AI-native blood_sand — Pass A source authority / execution erratum

Date: 2026-08-27

Status: **ORIGINAL MANIFEST SUPERSEDED FOR ACTUAL PASS A / VALID SEALED BASELINE FROZEN**

## 1. Why this erratum exists

The original draft of this manifest attempted to define an Alice-free allowlist directly against `MaksimUnimax/blood_sand` commit:

```text
0da1fdfa65155fe0b22d67838d366e7d214ccbbe
```

During the first genuinely clean Pass A attempt, that design failed closed. Two documents previously admitted as "business/customer" inputs themselves contained AI/Alice-derived text:

```text
marketing/RESEARCH_BASELINE_2026-08-01.md
marketing/research/CUSTOMER_EVIDENCE_AUTO_PENDANTS_2026-08-01.md
```

The clean chat correctly returned `INVALID_BASELINE_LEAKAGE`; no baseline output was written from that attempt.

This means the original broad allowlist must **not** be reused as the execution authority for Pass A.

## 2. Valid Pass A execution authority

The defect was corrected by extracting only neutral assortment framing plus measured Wordstat and ordinary Yandex Search observations into a sealed projection inside `Yandex_direct`:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_PASS_A_SEALED_BASELINE_PACKET_2026-08-27.md
```

Hardened clean-chat handoff:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_PASS_A_CLEAN_CHAT_HANDOFF_2026-08-27.md
```

The clean context was prohibited from opening `blood_sand`, using repository search, web, memory/personal context, or any source other than those two gate files.

Valid frozen Pass A:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_PASS_A_2026-08-27.md
commit = 9501af0da39c671f578f56bb56dad311f2d9c761
extra_source_opened = false
fresh_provider_requests = 0
```

Therefore the sealed packet, not the original broad source list, is the canonical non-AI evidence projection for the executed comparative experiment.

## 3. What the sealed packet contains

Only evidence that can be safely treated as Alice-free for this experiment:

```text
neutral product/use-case frame
measured Wordstat demand / quoted precision / representative dynamics / device evidence
ordinary Yandex Search provider observations
ordinary Search secondary observations
```

It contains no Alice answer text, Alice source/fan-out evidence, R3 opportunity decisions, H/A/C/O Alice-derived values, or cross-surface ledger fields.

## 4. Frozen upstream provenance

The sealed observations were extracted from the frozen project authority:

```text
repository = MaksimUnimax/blood_sand
commit = 0da1fdfa65155fe0b22d67838d366e7d214ccbbe
```

Relevant upstream non-AI measurements include the canonical R1 Wordstat and ordinary Yandex Search observations from that commit. The sealed packet exists specifically so future baseline execution does not need to browse mixed-provenance source files.

## 5. Pass B expansion

Only after Pass A commit `9501af0d...` was immutable, Pass B added canonical consumer-Alice evidence.

Pass B source authority:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_PASS_B_SOURCE_MANIFEST_2026-08-27.md
```

Pass B freeze:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_AI_NATIVE_PASS_B_2026-08-27.md
commit = d0cad99be1c1cf70ad06d3cf7bf28495daab58b8
```

Final comparison:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_COMPARISON_2026-08-27.md
verdict = AI_NATIVE_COMPARATIVE_GATE_PASS
```

## 6. Permanent anti-leakage lesson

For future controlled comparative baselines, do not trust a file merely because its creation date predates a later AI research stage. Validate the actual file content/provenance first, or use a sealed projection whose allowed fields are explicit.

Preferred pattern:

```text
mixed project repository
→ provenance audit
→ sealed baseline packet
→ clean context
→ immutable baseline
→ only then reveal treatment evidence
```

The failed first attempt is retained as evidence that the fail-closed rule worked correctly.
