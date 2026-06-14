# Kata Application — deterministic-agent-loop

## 1. Routing decision

- **Resolved topic**: `deterministic-agent-loop`. [DOC]
- **Why this kata**: the loop halts/continues by scanning model prose
  (`"done"`/`"task complete"`), which is the exact failure this kata prevents —
  non-deterministic control on the textual surface. [INFERENCIA]
- **Rejected alternatives**: `validation-retry-feedback` (about retrying invalid
  outputs, not turn halt); `human-handoff-protocol` (about ending into a human
  payload, not the loop contract). [DOC]
- **Depth**: `deep`.
- **Playbook read**: `references/deterministic-agent-loop.md` (exactly one). [DOC]

## 2. Problem (failure mode)

Halt is decided by `any(p in reply_text for p in ["done","task complete","listo"])`.
A casual "all done" triggers an early silent halt; when the model never emits the
phrase, the loop runs forever. There is no `max_iterations`, so a tool-requesting
loop cannot terminate. [INFERENCIA]

## 3. Correct pattern applied

```python
for i in range(max_iterations):
    resp = create(...)                     # Messages API call
    if resp.stop_reason == "tool_use":
        dispatch(resp)                     # one tool_result per tool_use_id,
        continue                           # reinjected as role=user
    if resp.stop_reason == "end_turn":
        return resp                        # the ONLY clean halt
    raise UnhandledStop(resp.stop_reason)  # max_tokens / pause_turn fail loudly
raise BudgetExceeded(max_iterations)       # never fall out of the loop silently
```
Control now lives in the typed `stop_reason` field plus a bounded budget, never in
the model's prose. [CÓDIGO]

## 4. Anti-pattern removed

```python
DONE = ["done", "task complete", "listo"]
if any(p in reply_text for p in DONE):
    return  # text parse: silent early halt OR infinite loop
```
This branch is deleted. The model's prose is output for the human, not a control
signal for the machine. [DOC]

## 5. Edge cases addressed

| Edge case (from playbook) | How this case handles it | Tag |
|---|---|---|
| `pause_turn` (server-side / long-running tools) | Falls into the `else` → `UnhandledStop`; treat as continuation only after confirming against the live API response. | [SUPUESTO] verify against API |
| `max_tokens` truncation | `UnhandledStop`; caller decides resume vs abort — never an implicit clean halt. | [DOC] |
| Multiple `tool_use` blocks | `dispatch` returns one `tool_result` per `tool_use_id`; omitting one leaves a malformed turn. | [CÓDIGO] |
| Tool raises | Return `tool_result` with `is_error=true`; do not abort the loop. | [SUPUESTO] verify vs error-propagation kata |
| `max_iterations <= 0` | `for` never enters → `BudgetExceeded`; treat as config error. | [INFERENCIA] |

## 6. Out-of-scope (neighboring katas)

- Tool retry/network policy → `validation-retry-feedback`. [DOC]
- Errors crossing agents → `multiagent-error-propagation`. [DOC]
- Ending into a human → `human-handoff-protocol`. [DOC]

## 7. Acceptance checklist (playbook + router)

- [x] Exactly one playbook read; topic matches user intent. [DOC]
- [x] Output follows the playbook's structure. [DOC]
- [x] Zero text-based halt/continue branches. [CÓDIGO]
- [x] Every `stop_reason` branch explicit; default is `raise`, not `return`. [CÓDIGO]
- [x] `max_iterations` present; exhausting it raises `BudgetExceeded` (distinct from
      `UnhandledStop`). [CÓDIGO]
- [x] One Alfa-core tag per claim; no mixed families; `[SUPUESTO]` items carry a
      verification step. [DOC]

## 8. Evidence log

- Halt must route on `stop_reason`, not prose — `[CÓDIGO]` — playbook "Patrón correcto".
- Budget is mandatory, not optional — `[INFERENCIA]` — playbook "Bucle acotado".
- `pause_turn` handling is provisional — `[SUPUESTO]` — verify vs live API response.
