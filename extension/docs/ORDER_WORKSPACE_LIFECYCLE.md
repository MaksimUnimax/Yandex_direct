# ORDER WORKSPACE LIFECYCLE

Status: canonical operational contract.
Date: 2026-08-12.

## 1. Purpose

Every real customer order must have a durable GitHub working directory so that research progress and API evidence do not depend on one ChatGPT conversation.

## 2. Creation

Before collecting material evidence for a new order, create:

```text
work/<job_id>/
```

Start from `work/_template/` and fill in `JOB.md` and `manifest.json`.

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

Raw evidence should preserve request parameters, timestamps and external response identity sufficient to understand what was collected.

### Normalized

Machine-friendly tables/JSON/CSV derived from raw evidence.

Raw evidence is not replaced by normalized data.

### Analysis

Intermediate ChatGPT conclusions, clustering decisions, negative-keyword decisions, audit findings, mappings and other reasoned working outputs.

### Deliverables

Only customer-facing final or near-final artifacts.

### Logs

Run records and cost/quota ledgers.

## 4. Paid evidence rule

A successfully received paid result must be persisted in the job workspace as soon as practical, before the workflow intentionally abandons its only runtime/chat copy.

The same paid collection should not be repeated merely because:

- a ChatGPT conversation was lost;
- context window changed;
- browser/extension restarted;
- the operator opened another conversation;
- analysis is being resumed later.

Before recollecting paid data, check the job workspace for equivalent existing evidence and decide whether freshness/parameter mismatch genuinely requires a new request.

## 5. Commit cadence

Commit meaningful checkpoints rather than waiting until the end of the entire order.

Recommended checkpoints:

```text
job initialized
service run completed
paid evidence persisted
normalization completed
major analysis milestone
customer deliverable created/updated
order completion cleanup
```

Do not create a commit for every trivial local transformation when it adds no recovery value.

## 6. Service-run boundary

One run equals one service, but all runs for the order use the same job workspace.

Example:

```text
RUN Wordstat  → raw/wordstat + logs
RUN Search    → raw/search + logs
RUN Webmaster → raw/webmaster + logs
RUN Metrika   → raw/metrika + logs
RUN Direct    → raw/direct + logs
```

## 7. Missing service access

If the customer did not provide access to a service:

- do not fabricate evidence;
- record the service as unavailable/not collected;
- continue with available sources;
- do not block unrelated runs;
- clearly state any resulting limitation in analysis/deliverables when material.

## 8. Secrets

Never write secret values to the job workspace.

Allowed:

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
```

## 9. Completion

Before cleanup:

1. verify deliverables are complete;
2. verify customer delivery/acceptance state as applicable;
3. ensure the final useful checkpoint is committed;
4. update job status to COMPLETE if using a final completion commit;
5. remove `work/<job_id>/` from current HEAD.

## 10. Git-history semantics

Normal `git rm`/GitHub deletion removes the directory only from current and future trees. Prior commits continue to contain the historical working data.

This is intentional for the default workflow because the primary requirement is loss prevention and auditability during active work.

If a customer/project requires full historical deletion, stop normal cleanup and use a separately authorized repository-history purge procedure. Do not assume normal folder deletion provides that property.
