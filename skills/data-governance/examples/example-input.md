# Example input — data-governance router

A user message arriving at the router:

> "We're about to share our `customers` and `support_tickets` tables with an
> external analytics vendor for churn modeling. The tickets table has free-text
> notes written by agents, and customers has email, full name, date of birth, and
> postal code. We're under GDPR. Before we export, what do we need to do to the
> data so we're not handing over identifiable records, and how do we handle people
> who later ask us to delete their data?"

Context the router can assume is available on request:
- Schemas / DDL for both tables.
- A representative sample for profiling the free-text `notes` column.
- The org operates in the EU; GDPR is the applicable regime.

Expected routing: this is about PII, masking/anonymization, and consent/erasure
before an export — the weakest-overlap match is **data-privacy-patterns**, not
the generic `data-governance` operating model and not `data-documentation`.
Depth: **deep** (an export with re-identification risk warrants the full ladder
and a re-identification test). [INFERENCE]
