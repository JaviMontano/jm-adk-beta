# Quick variation: fast single-route dispatch

For unambiguous requests where the topic is obvious. Essentials path only.

```
Route this request through skill-foundry at depth=quick.

Intent: <one line, e.g. "certify the skill at ./skills/nda-review">

Do:
1. Resolve topic from routes.json triggers (here: certify-skill).
2. Read ONLY references/<topic>.md.
3. Run the playbook's essentials path.
4. Run the playbook gate + shared gate; report dod=pass/fail.

Output: resolved topic, route read, verdict/artifact, gate line. Tag claims
[DOC]/[INFERENCE]. Single brand, no prices, no green-as-success.
```

Use when: the asset kind and action are stated plainly and only one enum value
can match. If you find yourself wanting to read a second reference, stop — switch
to the deep variation or ask a disambiguating question. [DOC]
