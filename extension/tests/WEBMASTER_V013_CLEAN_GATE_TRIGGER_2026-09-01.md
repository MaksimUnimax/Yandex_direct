# YMB Webmaster v0.1.3 clean-candidate gate trigger

Date: 2026-09-01

Purpose: trigger the pre-delivery workflow on the already committed v0.1.3 production source after the staged source gate passed.

Production source parent commit:
`bccdf16cedd72623de8c83040ca1af3f29d72271`

This file changes no production bytes. The following workflow run must execute with no `.ci/ymb-v013` staging payload, rerun focused Webmaster tests, the full canonical extension regression, version/manifest safety checks, provider-stub guard, deterministic double-build comparison, ZIP integrity, extracted per-file identity, and upload the exact candidate artifact only if all checks pass.
