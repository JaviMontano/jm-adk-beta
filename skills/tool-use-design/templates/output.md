# Routing-Contract Report — {tool surface name}

## 1. Surface inventory

| Tool | Current description | Overload flag |
|------|---------------------|---------------|
| {name} | {verbatim current text} | {none / overlaps with X} |

## 2. Detected overlaps

- {tool A} ⇄ {tool B}: {one line on why a planner confuses them}. Resolution: `rename_split`. [INFERENCIA]

## 3. Rewritten contracts

For each tool:

### {tool name}
- **Purpose**: {one sentence}.
- **Input format**: {types / shape, e.g. "regex or literal string"}.
- **Output shape**: {what it returns}.
- **Examples**:
  1. `{invocation 1}`
  2. `{invocation 2}`
- **Reciprocal boundary**: "Use this for {A}. For {B}, use {other tool}." (and {other tool} points back here). [DOC]

## 4. Repo strategy

- Sequence: `grep` → `read` → `edit`.
- `read_all_upfront`: false
- `glob_all_then_read_all`: false

## 5. Edit safety

- `unique_anchor_required`: true
- On first non-unique-anchor failure: expand anchor with adjacent context.
- Fallback: `read_write_full_rewrite`. [CÓDIGO]

## 6. Determinism flags

- `offline`: true
- `network_required`: false
- `deterministic`: true

## 7. Report JSON (machine-validable)

```json
{
  "tools": [
    {
      "name": "",
      "purpose": "",
      "input_format": "",
      "output_shape": "",
      "examples": ["", ""],
      "boundary": { "delegates_to": "", "reciprocal": true }
    }
  ],
  "overload_resolution": "rename_split",
  "repo_strategy": ["grep", "read", "edit"],
  "read_all_upfront": false,
  "glob_all_then_read_all": false,
  "edit_safety": {
    "unique_anchor_required": true,
    "fallback": "read_write_full_rewrite"
  },
  "flags": { "offline": true, "network_required": false, "deterministic": true }
}
```

## 8. Gate checklist (criterion → evidence tag)

- [ ] ≥2 contracts each with purpose/input/examples/boundary — [DOC]
- [ ] reciprocal boundaries bidirectional — [DOC]
- [ ] overload resolved as rename_split — [DOC]
- [ ] repo sequence = grep, read, edit — [DOC]
- [ ] read_all blockers false — [DOC]
- [ ] Edit safety + fallback — [CÓDIGO]
- [ ] determinism flags set — [DOC]
- [ ] single Alfa-core tag family — [CONFIG]
