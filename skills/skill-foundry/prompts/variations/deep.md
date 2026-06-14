# Deep variation: exhaustive route with verification

For high-stakes or ambiguous requests. Every step verified; tie-breakers explicit.

```
Route this request through skill-foundry at depth=deep.

Intent: <full description, e.g. "take skill X to production and prove the gain">

Do:
1. DISCOVER — restate intent; list candidate topics it could match.
2. ANALYZE — apply SKILL.md tie-breakers to each candidate; record why the
   losers are rejected. If still tied, ask ONE disambiguating question.
   (e.g. "production-ize end-to-end" → assembly-skill, NOT x-ray or certify alone.)
3. EXECUTE — read ONLY references/<resolved-topic>.md; run its exhaustive path;
   run every deterministic script it ships, capturing exit codes.
4. VALIDATE — run the playbook rubric (incl. constitution v6.0.0) AND the shared
   gate; for quality routes, compute the certification level
   (MOAT/CERTIFIED/CONDITIONAL/BLOCKED) from policy assets.

Output: candidate list + rejection rationale, resolved topic, script evidence,
verdict/artifact, full gate results. One Alfa-set tag per non-obvious claim;
preserve [EXPLICIT]/[INFERRED] from the playbook.
```

Use when: the request spans multiple possible routes, is a quality decision, or
must withstand review. Never collapse the candidate analysis to skip a tie-break. [DOC]
