# Quick Variation — ai-quality (depth=quick)

Fast path: resolve one topic, read its playbook, deliver the essentials, gate.
Use when the artifact is small (a single diff hunk, one model output, a short
content sample) or the stakes are low and reversible.

## Steps
1. Resolve `topic` (one enum) and state it in one tagged line. [CÓDIGO]
2. Read only that playbook.
3. Execute the **essential** path:
   - `ai-code-review` / `code-review` → triage BLOCKER/MAJOR on changed hunks
     only; cite file+line; skip diffuse maintainability scan. [CÓDIGO]
   - `llm-evaluation` → one metric + a baseline; reference-free judge if no
     labels; flag as directional if eval set < 30. [INFERENCIA]
   - `ai-assisted-testing` → highest-risk targets only, oracle per test, status
     `proposed`. [CÓDIGO]
   - `ai-safety` / `ai-content-detection` / `ai-documentation` /
     `ai-workflow-automation` / `ai-testing-strategy` → produce the minimum
     valid packet/plan/matrix that still passes the topic's gate. [CONFIG]
4. Run the topic gate; report `pass` / `warn` / `block`.

## Limits of quick mode
- May miss diffuse or slice-level issues; state this in the deliverable's limits
  section. A quick pass is never a clean bill of health. [DOC]
- If quick mode hits a high-severity or irreversible signal, escalate to `deep`
  rather than shipping a thin verdict. [INFERENCIA]
