# work/ — active order workspace

This directory contains **only active customer/Kwork orders**.

Each order gets its own directory:

```text
work/<job_id>/
```

Recommended naming:

```text
YYYYMMDD-kwork-<short-slug>-<sequence>
```

Example:

```text
work/20260812-kwork-dentistry-direct-001/
```

## Required lifecycle

```text
create job directory
→ record brief/manifest
→ collect raw evidence by service
→ commit important results promptly
→ normalize/analyze
→ create deliverables
→ deliver order
→ verify completion
→ delete work/<job_id>/ from current repository tree
```

## Why raw evidence is committed

Results from paid API calls are valuable evidence. Once received, they should not exist only in:

- ChatGPT conversation history;
- browser runtime;
- temporary extension memory;
- clipboard/composer.

Persist raw paid evidence to the job directory before relying on it later. This prevents accidental repeat spending after context loss or restart.

## Recommended job tree

```text
work/<job_id>/
├─ JOB.md
├─ manifest.json
├─ context/
├─ raw/
│  ├─ wordstat/
│  ├─ search/
│  ├─ webmaster/
│  ├─ metrika/
│  └─ direct/
├─ normalized/
├─ analysis/
├─ deliverables/
└─ logs/
   ├─ runs/
   └─ cost-ledger/
```

Git does not track empty directories; create folders only when they gain content or use the template files as needed.

## Prohibited content

Never commit:

- API keys;
- OAuth access/refresh tokens;
- passwords;
- cookies/session secrets;
- private credential exports;
- authorization headers.

Use aliases/IDs where necessary and keep credentials only in the extension's trusted local storage.

## Deletion semantics

Normal order cleanup removes `work/<job_id>/` from current HEAD. Previous Git commits still contain prior versions. Historical purge is a separate exceptional procedure.
