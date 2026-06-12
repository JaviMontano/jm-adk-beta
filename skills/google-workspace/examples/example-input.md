# Example Input — google-workspace

A user message handed to the router, with the routing context it carries.

## User request

> "Each completed test run should add a row to the 'Log' tab of my QA tracking
> spreadsheet, and then put a 30-minute review invite on the team calendar for the
> next morning with a Google Meet link. Don't overwrite anything that's already in
> the sheet, and don't send the invite until I say so."

## Provided parameters

- `topic`: not set (must be inferred).
- `depth`: `deep` (two services, a mutation each, downstream automation).

## What the router must extract

- **Surfaces:** Google Sheets (row add) + Google Calendar (event create with
  Meet). Two services → this is a multi-service request, not a single-topic one. [INFERENCE]
- **Mutations:** Sheets append (not update — "don't overwrite") and Calendar
  insert (with invitation send held until explicit confirmation). [DOC]
- **Constraints:** no overwrite → `values.append`, not `values.update`; invite is
  consent-gated → `sendUpdates` only after the user confirms. [DOC]
- **Unknowns to verify:** spreadsheet id, `Log` tab header shape, owner's
  timezone for "next morning", whether the app created/opened the sheet (drives
  `drive.file` vs `spreadsheets`). [ASSUMPTION]

## Expected routing

`topic = google-apis-integration` (Sheets + Calendar in one workflow), `depth =
deep`. The router loads ONLY `references/google-apis-integration.md`. [DOC]
