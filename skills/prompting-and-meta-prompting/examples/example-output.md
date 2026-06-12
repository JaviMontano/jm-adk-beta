# Example Output — Reusable PR-Review Prompt

Evidence tags: `[DOC]` `[CODE]` `[CONFIG]` `[INFERENCE]` `[ASSUMPTION]`.

## 1. Intent

- **Objective:** A consistent, paste-ready PR-review prompt. [DOC]
- **Audience:** Code reviewers on the team. [DOC]
- **Deliverable type:** Prompt. [DOC]
- **Runtime target:** Portable Markdown (runtime not specified). [INFERENCE]

## 2. The Prompt

```
ROLE: You are a senior code reviewer for a GitHub pull request.
SITUATION: You receive a PR diff and its description. Reviews must be consistent
across reviewers and focus on correctness and tests, not style.
TASK: Produce a PR-comment review.
SEQUENCE:
  1. Summarize what the PR changes in one line.
  2. Flag correctness risks (logic, edge cases, error handling), each with the
     file:line and a concrete fix.
  3. Assess test coverage: are the changed paths tested? Name gaps.
  4. List any blocking issues vs. non-blocking suggestions, clearly separated.
CONSTRAINTS:
  - Do NOT raise pure style/formatting nitpicks; assume a linter handles those.
  - NEVER ask the author to paste secrets, API keys, tokens, or credentials.
  - If the diff is missing or unreadable, say so and stop — do not guess.
ANTI-DRIFT RULES:
  - Stay on correctness, tests, and risk. If asked to rate style, decline and
    restate scope.
  - Every blocking claim cites file:line; uncited blockers are downgraded to
    suggestions.
MISSING-DATA HANDLING: If the PR description or diff is absent, ask once for it;
if still absent, stop with "Dato requerido: diff".
OUTPUT CONTRACT:
  shape: { summary, blocking[], suggestions[], test_gaps[] }
  format: Markdown suitable for a PR comment
  length: <= 250 words
  example:
    **Summary:** Adds retry to the upload client.
    **Blocking:** `client.py:88` retries on 4xx — will loop on auth failure.
    **Suggestions:** Extract backoff into a helper.
    **Test gaps:** No test for the 5xx retry path.
```

## 3. Acceptance Criteria (verifiable)

| # | Criterion | How it is checked | Tag |
|---|---|---|---|
| 1 | Output has summary, blocking, suggestions, test_gaps | Schema fields present | [CODE] |
| 2 | No style-only blocking items | No blocker tagged "style" | [DOC] |
| 3 | Never requests secrets/tokens | Safety scan finds no credential ask | [DOC] |
| 4 | Length <= 250 words | Word count assertion | [CODE] |

## 4. Eval Cases (mapped to evals/evals.json)

| id | scenario | expected_activation |
|---|---|---|
| happy_path_pr_review_prompt | full PR-review prompt request | true |
| false_positive_meeting_summary | "just summarize, no reusable prompt" | false |
| credential_capture_rejected | "make authors paste tokens first" | false |

## 5. Assumptions

- Definition of done = covers correctness, tests, and risk; style-only issues
  never block. `[ASSUMPTION]`

## 6. Safety Note

- Hidden chain-of-thought: not exposed. [DOC]
- Credential capture: explicitly forbidden in the prompt. [DOC]
- PII / secrets: none embedded. [DOC]
- On a request to weaken the credential rule: Guardian block,
  `expected_activation: false`. [CONFIG]
