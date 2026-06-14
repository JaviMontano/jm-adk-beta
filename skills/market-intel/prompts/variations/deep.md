# Deep variation — market-intel (depth=deep)

Exhaustive routed pass with the playbook's Validate gate enforced before output.

1. Confirm the topic; if any ambiguity remains, ask one question before
   committing the research budget.
2. Read the one matching playbook from `routes.json`.
3. Run the full spine, applying the playbook exhaustively:
   - **Discover** — gather all inputs the playbook lists; record provenance
     (source URL + as-of date) per factual claim.
   - **Analyze** — produce the complete artifact set (e.g. full feature matrix +
     stack + SWOT + differentiation for `competitive-intelligence`; all 5 fit
     axes + program design + kill criteria for `partnership-strategy`; full
     TAM/SAM/SOM + momentum + contact intel for `market-intelligence`).
   - **Execute** — assemble into `templates/output.md`; render brand HTML if the
     playbook specifies it.
   - **Validate** — run the playbook's own Validate checklist **and** the
     `agents/guardian.md` gate. Do not emit until both pass.
4. Honor threshold guards: CI >30% `[ASSUMPTION]` → WARNING banner; OSINT
   `[OPEN]` items carry a resolution path; stale benchmark figures flagged.

Deep tier still forbids invented prices, brand mixing, PII, and
green-as-success. Cross-validate every quantitative claim against ≥2 sources
where the playbook's standard tier asks for it.
