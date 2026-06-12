# Meta prompt — legal-compliance self-check

Run this reflection before returning any legal-compliance deliverable.

## Routing integrity
- Did I resolve exactly one `topic` and read exactly one playbook? If I touched a
  second playbook "for context," I broke the router — restart the lane.
- For a multi-topic request, did I sequence lanes (one playbook each) rather than
  blend them?

## Evidence integrity
- Does every non-obvious claim carry exactly one Alfa-core tag, spelled one way?
- Is every `[SUPUESTO]` paired with a concrete verification step?
- Did I invent any clause number, control ID, fine, or citation? If so, downgrade to
  `[SUPUESTO]` and flag — or remove it.

## Scope & governance integrity
- Is the verbatim legal disclaimer present and unaltered?
- Did I assert "compliant" / PASS as fact anywhere? Replace with evidence-tagged
  status.
- Did I drift into net-new drafting, litigation strategy, certification, or
  jurisdiction-specific advice? Flag and defer to counsel.

## Lane-specific integrity
- compliance-assessment: 100% requirement coverage? one scoring method across matrix
  and heat map? every roadmap action mapped to a gap ID?
- compliance-framework: every "met" backed by a locatable artifact? version pinned?
- contract-review: every checklist clause addressed/N/A? every High finding has a
  fallback?

If any check fails, fix it before responding — do not ship a partial gate.
