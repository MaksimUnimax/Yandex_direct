Yandex Marketing Bridge — ChatGPT ↔ Yandex
Version: 0.1.0
Phase: 1 — Wordstat + unified CORE

Purpose
-------
One controlled Chrome/Chromium extension for ChatGPT-driven Yandex marketing work.
Phase 1 exposes exactly one executable service: Yandex Wordstat.
Future Search/Webmaster/Metrika/Direct adapters are NOT executable in this package.

Core safety model
-----------------
- explicit confirmed ChatGPT conversation binding;
- one RUN = one immutable active SERVICE;
- Phase 1 active service = wordstat;
- local native Copy remains native Copy;
- generic Copy response is not an API trigger;
- Manual and Autorun remain mutually controlled;
- paid/irreversible initiation is never blindly retried after uncertain outcome;
- duplicate command/concurrent delivery paths are single-flight/exactly-once guarded;
- user composer is not silently overwritten;
- secrets stay in extension-local worker storage and are not placed in ChatGPT results.

Job and cost policy
-------------------
A trusted operator Job ID is bound to the current conversation and stamped into results.
Wordstat credential presence and Autorun permission are independent.
If credentials are missing, a valid Wordstat command can return a controlled
WORDSTAT_RESULT_V1 status=SKIPPED reason=NO_CREDENTIALS without a Yandex request.

Operator policy includes hard request and estimated-cost ceilings. Paid requests reserve
budget before external initiation so a crash can conservatively over-count but cannot
under-count and silently permit another paid attempt.

Important: extension cost guards do NOT replace ChatGPT's operating obligation to check
current official Yandex pricing and explain the estimated cost before each executable paid
Wordstat command.

Supported executable protocol
-----------------------------
WORDSTAT_API_V1

Supported methods
-----------------
- getTop
- getDynamics
- getRegionsDistribution
- getRegionsTree

Unknown/future service protocol blocks are not executable in Phase 1.

Development / acceptance
------------------------
The package is migrated from the owner-supplied audited Wordstat Bridge 1.1.5 lifecycle
reference. Four shared modules remain hash-identical to the supplied Business Bridge 2
common reference. New Job/Service/Policy/Cost behavior is covered by additional tests.

Source/static/fresh-ZIP tests do not replace controlled live production ChatGPT acceptance.
See GitHub repository MaksimUnimax/Yandex_direct, extension/docs/ for the canonical project
specification, roadmap, reference audit, and append-only development context.
