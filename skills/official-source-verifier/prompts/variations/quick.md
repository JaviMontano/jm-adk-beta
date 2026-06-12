# Quick Variation — Single-Claim Source Check

For one decision resting on a single claim, when speed matters but authority still must
hold.

## Use when

- One concrete question (e.g. "is branch-delete the default for `gh pr merge`?").
- A secondary source may have triggered it; you need an official confirm/contradict.

## Fast path

1. State the `question` and the one claim it rests on.
2. `WebSearch` → `WebFetch` the single canonical official doc.
3. Record the citation: `url`, `accessed_date` (ISO), short extract, `official=true`.
4. Set the claim `verified` only if the fetched official text supports it; otherwise
   `unverified`.
5. Emit a minimal `decision`: `change_authorized` (true only if `verified`),
   `justified_change`, `blocking_gaps`.

## Non-negotiable even in quick mode

- No `accessed_date` → claim cannot be `verified`.
- Secondary source is `role=lead` only, never authority.
- A doc from the wrong major → `unverified`, flag version conflict.
- Open gap → status is not `pass`.

Tag the claim and decision. Single brand; no invented prices; no client PII.
