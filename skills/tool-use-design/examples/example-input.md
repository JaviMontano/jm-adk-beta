# Example Input — Overlapping `analyze` / `process` surface

A small agent ships two file tools whose descriptions a planner cannot route between, plus no repo-read protocol and no Edit fallback.

## Current tool surface

```python
TOOLS = [
    {"name": "analyze", "description": "Analyzes content."},
    {"name": "process", "description": "Processes the file."},
    {"name": "patch",   "description": "Edits a file by replacing text."},
]
```

## Reported symptoms

- The agent frequently asks "should I use `analyze` or `process`?" — the decision should be immediate.
- To "understand the repo" it runs `glob("**/*")` and reads every file, saturating the context window.
- `patch` fails intermittently: the replacement string is not unique and there is no documented fallback.

## Request

Redesign this surface as deterministic routing contracts: explicit input formats, examples, reciprocal boundaries, a `Grep → Read → Edit` strategy with no read-all upfront, and a documented Edit fallback. Emit an offline-validable report.
