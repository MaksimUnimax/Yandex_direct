# Exact Yandex Bridge memory comparison

Owner authorized an isolated QA branch and GitHub Actions run on 2026-10-06. No main updates, deployment, Easyscript execution, real credentials or provider operations are part of this task.

Inputs are exact supplied ZIPs, verified before extraction and after testing:
- 0.1.9: de4425a47645d537ef7b69994ef2df0f66c3e9bd6741b0b47884426bdd954c4c
- 0.1.10: 4b9d396dcbe7bb12eed52b91c46f328674a35d1ba02805ad2fe7dc63e2ffdae6

The two original B22 tests are preserved from commit306678f5bc0c9f7910fc4550c7a2d6967b5e34bd. Runtime harness copies only are adapted in prepare.py:
- Current folder-owned job fixture (synthetic folder, no credentials); real worker settings response is retained except folder_id.
- Current harmless unknown-row label accepted.
- V6 uses its original100-refresh case. The old absolute100-tab churn case is replaced by the existing V8 neutral-control differential, as B22 itself did.
- Original idle no-auto-DB-read assertion is NOT removed. Both delivered versions currently have a one-second local refresh; a failure here must be reported as a historical contract mismatch, not automatically as the owner's RAM cause.
- Browser sandbox remains enabled (legacy no-sandbox flag removed).
- Emergency browser-tree RSS watchdog closes only the owned test browser above2GiB; steps have300/600-second time limits and jobs20-minute limit. Versions execute sequentially on GitHub-hosted runners.
- Browser network name resolution is blocked; V8 also rejects worker fetch calls. No real provider/auth/owner-data actions.

Passes cover these selected memory boundaries only. No claim of full extension acceptance, reproduction of the owner's incident, a repaired package or live integration follows automatically. No product files are edited; neutral-control copies are explicitly separate.
