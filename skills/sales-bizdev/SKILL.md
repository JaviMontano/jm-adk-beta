---
name: sales-bizdev
description: "Sales and business development: prospecting, outreach, dossiers, proposals, pitches, and collateral (ES/EN consulting context). Topics: b2b-outreach, client-dossier, client-prospecting, executive-pitch, lead-generation, proposal-writing, sales-collateral."
params:
  topic:
    enum: [b2b-outreach, client-dossier, client-prospecting, executive-pitch, lead-generation, proposal-writing, sales-collateral]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
  b2b-outreach: references/b2b-outreach.md
  client-dossier: references/client-dossier.md
  client-prospecting: references/client-prospecting.md
  executive-pitch: references/executive-pitch.md
  lead-generation: references/lead-generation.md
  proposal-writing: references/proposal-writing.md
  sales-collateral: references/sales-collateral.md
---

# sales-bizdev

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
