# Step20 rerun assurance statement

Date: 2026-09-04  
Job: OKNO_MSK  
Declared mode: **MODE A — TEST/DEMO REHEARSAL**

## Assurance statement

A fresh Step20 release-assurance rerun was performed on the corrected Step19 physical package after the earlier material defects were fixed.

The rerun did **not** reuse the old Step20 verdict as proof. A new release candidate was frozen, risks were registered before substantive testing, and new current-site, accessibility, independence and provenance controls were executed.

For the declared TEST/DEMO Mode A, the exact tested release candidate is suitable to proceed to the next workflow stage subject to the freshness/expiry condition and the disclosed PDF accessibility residual.

## What was independently/mechanically verified

A separate GitHub Actions route verified:

- exact frozen XLSX/DOCX/PDF identity;
- 48/48 implementation-critical URLs by direct HTTP request;
- 48 HTTP 200 responses, zero redirects and zero transport errors;
- package counts and corrected A012/A027 propagation;
- TEST/DEMO distribution identity;
- DOCX metadata hygiene;
- prohibited claim boundaries;
- exact release-bundle provenance.

The release bundle received a signed GitHub artifact attestation:

```text
attestation id = 45139802
```

The attestation proves build provenance only. It is not evidence that the analytical conclusions are correct.

## Current-content assurance

A separate fresh full-text snapshot retrieved all 48 implementation-critical pages. All 48 returned current text and compatible title/H1 identities.

The analyst then performed deeper current-content review of action-sensitive pages, including the corrected door and French-window actions and the other bounded content-enhancement cases.

No new MATERIAL contradiction was found.

Current-site conclusions are not timeless. They are governed by `STEP_20_RERUN_FRESHNESS_AND_EXPIRY.json` and must be rechecked before handoff if the configured validity window expires or an event trigger occurs.

## Accessibility

- DOCX automated accessibility audit: **0 high / 0 medium / 0 low findings**.
- XLSX structural accessibility review: **PASS** for the declared Mode A; all sheets visible, explicit text labels, no color-only critical states detected in the reviewed surfaces.
- PDF: visually readable but **not tagged**.

The untagged PDF is an accepted MINOR residual only for the declared TEST/DEMO Mode A because the DOCX provides an accessible alternative and no PDF-accessibility compliance requirement exists in the rehearsal contract.

This is **not** a claim that the PDF is accessibility-compliant. A future external job that requires an accessible/tagged PDF must remediate it before release.

## Validation and independence boundaries

The analyst completed scenario-based intended-use validation against 12 realistic recipient tasks.

No real external user/commissioner validation was performed because this is a mock rehearsal. Its state is:

```text
NOT_APPLICABLE_TO_MOCK_REHEARSAL
```

That state is explicitly **not** equivalent to completed real-user validation.

A separate mechanical verifier was used. No separate independent analytical assurer participated, and formal independent analytical assurance is **not claimed**. The declared Mode A permits this limitation. A normal consequential external/client delivery or high-impact mode must use the stronger independence route required by the Level1 Step20 method.

## Defect verdict

```text
BLOCKING = 0
MATERIAL = 0
MINOR ACCEPTED FOR MODE A = 1
```

The single residual is the untagged PDF accessibility state described above.

## Release boundary

A terminal Step20 PASS can be issued only after all enhanced rerun authorities are persisted and read back from GitHub.

Even after PASS, actual handoff/revision completion remains Step21 and is not claimed here.
