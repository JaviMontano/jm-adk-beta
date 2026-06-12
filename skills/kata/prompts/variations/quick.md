# Prompt — Quick variation (depth=quick)

Fast path: resolve, read one playbook, apply essentials, run the validation gate.

1. **Resolve `topic`** in one pass. If ambiguous between two keys, ask once with
   both options; otherwise proceed. [DOC]
2. **Read only `references/<topic>.md`.** No second playbook. [INFERENCIA]
3. **Apply essentials**: the correct pattern + remove the anti-pattern. Skip
   exhaustive edge-case enumeration, but do NOT skip the validation gate. [DOC]
4. **Validation gate (mandatory even in quick)**:
   - Exactly one playbook read; topic matches intent. [DOC]
   - Output follows the playbook's structure. [DOC]
   - The playbook's top acceptance criteria are met. [DOC]
   - One Alfa-core tag per claim; no mixed families. [DOC]

Output: a lean filled `templates/output.md` — resolved topic, pattern applied,
anti-pattern removed, acceptance checklist. Tag every non-obvious claim. [DOC]
