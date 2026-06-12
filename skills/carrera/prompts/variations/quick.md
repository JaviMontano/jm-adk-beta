# Prompt — quick variation (carrera, depth=quick)

Fast path. Resolve `topic`, load one playbook, return the essentials of its
contract. Same gates as deep — only the breadth shrinks.

1. Resolve `topic` from the request. Ambiguous → one question, then stop.
2. Read `references/<topic>.md` only.
3. Discover the supplied evidence; assign stable IDs.
4. Produce the minimum viable contract output: e.g. for `negociacion-oferta`,
   the offer table with pass/fail filters + PIVOTE and the single recommendation;
   for `proceso-seleccion-orchestrator`, the board plus exactly one next action;
   for `simulador-entrevista`, one scored question with the weakest-dimension
   next step.
5. Run the validator; report exit status.
6. Stop and ask on any `{VACIO_CRITICO}`.

Keep it lean: skip extended rationale, edge-case enumeration, and counterproposal
drafting unless asked. Never skip: evidence tags, the validator, the no-invented-
numbers rule, and the single-playbook law.

Topic: {{topic}} · Evidence: {{evidence}}
