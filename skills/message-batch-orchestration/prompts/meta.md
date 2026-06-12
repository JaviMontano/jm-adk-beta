# Meta prompt — message-batch-orchestration

Use this to decide **whether** the batch-orchestration skill applies and to set
depth before running `prompts/primary.md`.

## Activation test

Activate when ALL hold:
- The load is **offline / latency-tolerant** (no user waiting in line).
- There are many items that share a **stable business ID** usable as `custom_id`.
- Selective retry / fail isolation is wanted or implied.

Do NOT activate when ANY hold:
- The path is interactive or streaming (`false_positive_realtime`).
- The task is unrelated to batching (e.g. DB schema design → `false_positive_unrelated`).
- The user asks to skip uniqueness, drop `custom_id`, or disable fail isolation
  → reject rather than activate-and-degrade.

## Depth selection

- `quick` (default): assemble → create → poll → fragment → selective retry, no
  evidence report.
- `deep`: full run plus the JSON evidence report validated through
  `scripts/check.sh`, edge-case handling (`expired`/`canceled`, crash resume,
  all-fail last attempt), and explicit checkpointing.

## Self-correction

If, mid-run, you find yourself: calling `messages.create()` in a loop over
offline items; using an index as `custom_id`; or retrying the whole batch after
a partial failure — stop and return to the canonical lifecycle in SKILL.md.

## Governance reminders

Single brand (JM Labs); evidence tags from one family; no invented prices (cost
only as the documented ~50% batch saving); no client PII in examples.
