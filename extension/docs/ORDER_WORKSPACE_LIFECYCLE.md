# ORDER WORKSPACE LIFECYCLE

Status: canonical external operational contract.
Updated: 2026-08-12.

## 1. Purpose

Every real customer order may have a durable GitHub working directory so research progress and API evidence do not depend on one ChatGPT conversation.

**This lifecycle is executed by ChatGPT/development workflow through connected GitHub capabilities. It is not a Chrome-extension runtime feature.**

The Yandex Marketing Bridge does not know or require `job_id`, GitHub token, repository, branch, commit or workspace path.

## 2. Creation

When a real order needs durable workspace evidence, ChatGPT/development workflow creates:

```text
work/<job_id>/
```

This step is outside the Bridge and must never block a valid Bridge API command merely because the workspace does not yet exist.

## 3. Evidence classes

### Raw

Exact or minimally wrapped external evidence received from a service.

Examples:

```text
raw/wordstat/
raw/search/
raw/webmaster/
raw/metrika/
raw/direct/
```

Raw evidence should preserve request parameters, timestamps and response identity sufficient to understand what was collected.

### Normalized

Machine-friendly tables/JSON/CSV derived from raw evidence. Raw evidence is not replaced by normalized data.

### Analysis

Intermediate ChatGPT conclusions, clustering decisions, negative-keyword decisions, audit findings, mappings and other reasoned working outputs.

### Deliverables

Customer-facing final or near-final artifacts.

### Logs

External workflow run notes and cost/quota ledgers as useful. These are not the extension's internal secret/runtime storage.

## 4. Paid evidence rule

A successfully received paid result should be persisted in the order workspace as soon as practical before the workflow intentionally abandons its only usable copy.

The same paid collection should not be repeated merely because:

- a ChatGPT conversation was lost;
- context window changed;
- browser/extension restarted;
- the operator opened another conversation;
- analysis is resumed later.

Before recollecting paid data, check existing order evidence and decide whether freshness/parameter mismatch genuinely requires another paid request.

## 5. Commit cadence

Commit meaningful recovery checkpoints rather than waiting until the end of the entire order.

Recommended checkpoints:

```text
order initialized
service collection completed
paid evidence persisted
normalization completed
major analysis milestone
deliverable created/updated
order completion cleanup
```

Do not create a commit for every trivial transformation when it adds no recovery value.

## 6. Service-run boundary

The extension's one-RUN-one-service rule is independent from the external order workspace.

Example external organization:

```text
Wordstat RUN evidence  → raw/wordstat + logs
Search RUN evidence    → raw/search + logs
Webmaster evidence     → raw/webmaster + logs
Metrika evidence       → raw/metrika + logs
Direct evidence        → raw/direct + logs
```

The Bridge itself does not receive the workspace path.

## 7. Missing service access

If customer access to a service is unavailable:

- do not fabricate evidence;
- record it as unavailable/not collected where relevant;
- continue with available sources;
- do not block unrelated Bridge RUNs;
- state material limitations in analysis/deliverables.

## 8. Secrets

Never write secret values to the GitHub order workspace.

Allowed examples:

```text
credential_available = true
counter_id
campaign_id
host_id
client alias
```

Forbidden:

```text
OAuth token
refresh token
API key
password
session cookie
authorization header
Export settings backup containing secrets
```

## 9. Completion

Before cleanup:

1. verify deliverables are complete;
2. verify customer delivery/acceptance state as applicable;
3. ensure the final useful checkpoint is committed;
4. update order status to COMPLETE if used;
5. remove `work/<job_id>/` from current HEAD.

## 10. Git-history semantics

Normal Git deletion removes the directory only from current/future trees; earlier commits remain in repository history.

Full historical purge is a separate exceptional procedure and is not implied by ordinary cleanup.
