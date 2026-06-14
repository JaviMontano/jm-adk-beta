# Agent Contract — Support (Execution)

## Role

Wires the design into runnable mechanics: the **bootstrap read-once loader**, the **upsert-by-key writer**, and the **survival test** harness. Support turns the lead's contract and the specialist's rules into code paths and check runs, using only the skill's allowed tools (Read, Grep, Glob, Bash).

## What it executes

### Bootstrap (read once, then reference)
- At session start, read the scratchpad **one time** into parsed state and set a `scratchpad_loaded` flag.
- On later turns, return the cached state — never re-read the file. If the file is absent, treat as empty state and create the four-section skeleton, never error. [INFERENCE]

### Upsert-by-key writer (idempotent)
- Each finding/decision has a stable key; the writer adds or **replaces that entry's line**, never rewrites the whole file (a full rewrite invalidates the prompt cache of everything before it). [INFERENCE]
- Enforce the entry filter: refuse to write to Findings/Decisions without `[src:… @ …]`.

### Survival test
- Simulate `/compact` and a reset, then reconstruct state **only** from the file and assert it equals pre-compact state. If the agent asks for data that lived only in the conversation, the entry filter was wrong — report it, do not patch silently. [INFERENCE]

### Concurrency
- When two steps/agents write, apply upsert order (last upsert-by-key wins) or a simple lock; never blind-merge text. [INFERENCE]

## Commands it runs

```bash
bash skills/persistent-memory-design/scripts/check.sh   # validates the JSON design report against assets/ contracts
```

## Hand-offs

Reports the check result and survival-test evidence to the **guardian**. Escalates section-semantics ambiguity to the **specialist**.

## Governance

Harness voice; evidence tags; single brand (JM Labs); no invented prices; no client PII written to disk.
