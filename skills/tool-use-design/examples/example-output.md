# Example Output — Routing-Contract Report for the `analyze`/`process`/`patch` surface

## 1. Surface inventory

| Tool | Current description | Overload flag |
|------|---------------------|---------------|
| analyze | "Analyzes content." | overlaps with process; generic verb |
| process | "Processes the file." | overlaps with analyze; generic verb |
| patch | "Edits a file by replacing text." | no uniqueness rule, no fallback |

## 2. Detected overlaps

- `analyze` ⇄ `process`: both claim a file with no input format or boundary; a planner cannot route. Resolution: `rename_split` on a discover/read axis. [INFERENCIA]

## 3. Rewritten contracts

### search_code  (was: part of analyze)
- **Purpose**: Find files or symbols by pattern across the repo.
- **Input format**: a regex or literal string.
- **Output shape**: matching paths + line numbers.
- **Examples**: `search_code(pattern="def handle_payment")`; `search_code(pattern="TODO")`.
- **Reciprocal boundary**: "Use this FIRST to locate. To read a known file's contents, use `read_file`." [DOC]

### read_file  (was: process)
- **Purpose**: Read the full contents of ONE known file path.
- **Input format**: an absolute path.
- **Output shape**: the file's text.
- **Examples**: `read_file(path="/repo/src/payments.py")`.
- **Reciprocal boundary**: "Use AFTER `search_code` has located the file. Do NOT use to discover files — that is `search_code`'s job." [DOC]

### edit_file  (was: patch)
- **Purpose**: Replace an exact, UNIQUE anchor string in a file.
- **Input format**: path, old_string (must be unique), new_string.
- **Output shape**: confirmation or a uniqueness failure.
- **Examples**: `edit_file(path="/repo/src/payments.py", old_string=unique_anchor, new_string=patched)`.
- **Reciprocal boundary**: "FAILS if old_string is not unique. Fallback: `read_file` then `write_file` for a full rewrite." [CÓDIGO]

## 4. Repo strategy

Sequence `grep → read → edit`. `read_all_upfront=false`, `glob_all_then_read_all=false`. The prior `glob("**/*") + read all` (~200k tokens) is removed. [SUPUESTO]

## 5. Edit safety

`unique_anchor_required=true`. On first non-unique failure, expand the anchor with adjacent context; terminal fallback `read_write_full_rewrite`. [CÓDIGO]

## 6. Report JSON

```json
{
  "tools": [
    {"name": "search_code", "purpose": "Find files or symbols by pattern.", "input_format": "regex or literal", "output_shape": "paths + line numbers", "examples": ["search_code(pattern=\"def handle_payment\")"], "boundary": {"delegates_to": "read_file", "reciprocal": true}},
    {"name": "read_file", "purpose": "Read one known file path.", "input_format": "absolute path", "output_shape": "file text", "examples": ["read_file(path=\"/repo/src/payments.py\")"], "boundary": {"delegates_to": "search_code", "reciprocal": true}},
    {"name": "edit_file", "purpose": "Replace a unique anchor.", "input_format": "path, old_string, new_string", "output_shape": "confirmation or failure", "examples": ["edit_file(path=\"/repo/src/payments.py\", old_string=anchor, new_string=patched)"], "boundary": {"delegates_to": "read_file", "reciprocal": true}}
  ],
  "overload_resolution": "rename_split",
  "repo_strategy": ["grep", "read", "edit"],
  "read_all_upfront": false,
  "glob_all_then_read_all": false,
  "edit_safety": {"unique_anchor_required": true, "fallback": "read_write_full_rewrite"},
  "flags": {"offline": true, "network_required": false, "deterministic": true}
}
```

## 7. Gate result

All criteria pass: 3 contracts with reciprocal boundaries, overload resolved as `rename_split`, sequence `grep, read, edit`, read-all blocked, Edit fallback documented, determinism flags set, single Alfa-core tag family. [DOC]
