# Prompt Deliverable — {objective_short}

Evidence tags used: `[DOC]` `[CODE]` `[CONFIG]` `[INFERENCE]` `[ASSUMPTION]`.

## 1. Intent

- **Objective:** {single testable objective}
- **Audience:** {who consumes the output}
- **Deliverable type:** {prompt | system prompt | meta-prompt | prompt system}
- **Runtime target:** {model/runtime, or "portable Markdown"}

## 2. The Prompt

```
ROLE: {role}
SITUATION: {context the model can rely on}
TASK: {what to produce}
SEQUENCE:
  1. {ordered step}
  2. {ordered step}
CONSTRAINTS:
  - {testable constraint}
ANTI-DRIFT RULES:
  - {constraint embedded in the prompt}
MISSING-DATA HANDLING: {placeholder | ask | stop}
OUTPUT CONTRACT:
  shape: {schema/template}
  format: {markdown | json | ...}
  length: {bounds}
  example: {minimal example}
```

## 3. Acceptance Criteria (verifiable)

| # | Criterion | How it is checked | Tag |
|---|---|---|---|
| 1 | {criterion} | {schema field / script assertion} | [DOC] |
| 2 | {criterion} | {schema field / script assertion} | [CODE] |

## 4. Eval Cases

| id | input scenario | expected_activation | expected_checks |
|---|---|---|---|
| happy_path | {scenario} | true | {checks} |
| minimal_input | {scenario} | false | required_inputs, guardian_block |
| conflicting_requirements | {scenario} | false | conflict_detection, guardian_block |
| false_positive | {out-of-scope scenario} | false | activation_scope |
| unsafe_injection | {injection scenario} | false | safety_boundaries, guardian_block |

## 5. Assumptions

- {assumption} `[ASSUMPTION]`

## 6. Safety Note

- Hidden chain-of-thought: not exposed. [DOC]
- Credential capture / unsafe automation: refused. [DOC]
- PII / secrets in prompt or examples: none. [DOC]
- On safety or requirement conflict: Guardian block, `expected_activation: false`. [CONFIG]

## 7. Offline Validation (when a JSON report exists)

```bash
bash skills/prompting-and-meta-prompting/scripts/check.sh
```
Result: {pass | fail + reason}. [CODE]
