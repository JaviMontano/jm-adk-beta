# Example input — agent-orchestration

A user sends this request to the orchestrator:

> "Our nightly `sync-ledger.sh` job died at step 5 of 8 with a `409 Conflict`
> while POSTing a journal entry to the accounting API. The earlier steps already
> wrote three entries. We need to know whether it is safe to just rerun the job,
> and if not, what to do before any rerun. Be thorough."

Context provided:

- Failed command: `sync-ledger.sh`, step 5/8.
- Error class: `409 Conflict` on a POST (create) endpoint.
- State mutated: yes — 3 journal entries already written this run.
- Last safe checkpoint: step 4 succeeded.
- `depth`: deep (user said "be thorough").

No `topic` was passed explicitly, so the router must infer it.
