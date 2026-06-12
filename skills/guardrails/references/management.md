<!-- distilled from alfa skills/guardrails-management -->
<!-- > -->
# Guardrails Management

> "Rules you declare become rules the system enforces."

## TL;DR

Manages user-declared working rules stored as JSON in `references/guardrails/`. When the user expresses a preference ("always use TypeScript", "never use jQuery"), Pristino detects the intent, confirms with the user, then persists it. Rules load at every session start; the Guardian checks compliance. Confirmation is mandatory before any write; unconfirmed proposals are reported, never stored. [DOC]

## Scope / Anti-Scope

- **In scope**: detect rule intent, classify, confirm, append/deactivate one entry, list active rules. [DOC]
- **Out of scope**: enforcing rules at review time (that is the Guardian/`code-review`), bulk-editing rule files, inferring rules the user did not state, resolving conflicts silently. [DOC]
- This file defines the *workflow*; it does not define the JSON schema (see `assets/rule-schema.json`) or the verification-tag taxonomy (see `references/verification-tags.md`). [DOC]

## Procedure

### Step 1: Discover
- Detect intent to set a working rule (keywords: "always", "never", "from now on", "prefer", "avoid"). [INFERENCIA]
- Read existing guardrails: `references/guardrails/guidelines.json`, `constraints.json`, `guardrails.json`. [CONFIG]
- Check for duplicates or conflicts with existing rules. [DOC]
- Capture source text, proposed scope, evidence tag, and proposed verifiable check **before** any write. [DOC]

### Step 2: Analyze
- Classify the rule type:
  - **Constraint** (hard, "never"): stored in `constraints.json` → `CT-NNN`
  - **Guideline** (default, "always"): stored in `guidelines.json` → `GL-NNN`
  - **Guardrail** (soft, "prefer"): stored in `guardrails.json` → `GR-NNN`
- Generate next ID by scanning the *max* existing numeric suffix in the target file and adding 1 — never reuse the count, because deactivated rules leave gaps. `CT-007` deactivated still reserves 007. [INFERENCIA]
- Apply `assets/classification-policy.json`, `assets/storage-map.json`, and `assets/conflict-policy.json`. [CONFIG]
- Mixed-signal text ("always avoid X") resolves to the **strongest** enforcement level present ("avoid" within "always" → still a guideline unless "never" appears). When ambiguous, ask rather than guess. [SUPUESTO]

### Step 3: Execute
- **Confirm with user**: "I want to confirm: should I save this as a working [guideline/constraint/guardrail]? (yes/no)"
- If confirmed, append entry to the appropriate JSON file:
  ```json
  { "id": "GL-001", "rule": "...", "scope": "...", "check": "...", "type": "guideline", "confirmed": "YYYY-MM-DD", "source": "user-explicit", "active": true }
  ```
- If listing: read all 3 files, display active rules grouped by type.
- If removing: set `"active": false` on the specified rule; never delete the object (preserves audit trail). [DOC]

### Step 4: Validate
- JSON file parses after write (re-read and parse, do not trust the append). [DOC]
- No duplicate rules across files.
- Rule is actionable and verifiable by the Guardian.
- Confirmation was received before storing.
- For JSON operation packets, run `bash skills/guardrails-management/scripts/check.sh`. [CÓDIGO]

## Worked Examples

| User says | Type | File / ID | Stored `check` |
|-----------|------|-----------|----------------|
| "always use TypeScript for new files" | guideline | `guidelines.json` / `GL-012` | "new `.js`/`.jsx` files flagged" |
| "never commit secrets" | constraint | `constraints.json` / `CT-004` | "no `.env`/key patterns in diff" |
| "prefer named exports" | guardrail | `guardrails.json` / `GR-009` | "default exports warned, not blocked" |
| "from now on, make it cleaner" | — | (none) | rejected: not verifiable; ask for a concrete check |

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Append corrupts JSON (trailing comma, partial write) | next session load throws | validate-after-write in Step 4; keep a pre-write copy until parse confirms |
| Two rules same intent, different wording | Guardian double-flags | conflict check on normalized rule text, not exact string |
| ID collision from count-based numbering | two rules share `GL-007` | derive ID from max suffix + 1, not array length |
| Confirmation skipped under "obvious" intent | rule the user never wanted | confirmation is unconditional, no fast-path |
| Silent conflict resolution | user loses policy control | always surface both rules and require a choice |

## Deterministic Assets

- `assets/manifest.json` — every local asset and its consumer. [CONFIG]
- `assets/rule-schema.json` — required rule fields. [CONFIG]
- `assets/classification-policy.json` — maps user language → rule type and ID prefix. [CONFIG]
- `assets/confirmation-policy.json` — requires explicit confirmation before persistence. [CONFIG]
- `assets/conflict-policy.json` — duplicate and conflict checks. [CONFIG]
- `assets/storage-map.json` — maps each type to its canonical JSON file. [CONFIG]
- `assets/report-contract.json` — operation packet fields enforced by the offline validator. [CONFIG]

## Quality Criteria

- [ ] User confirmation received before storing any rule
- [ ] Rule stored in correct file (guideline/constraint/guardrail)
- [ ] ID is unique and sequential (max-suffix + 1, gap-tolerant)
- [ ] JSON re-parses cleanly after write
- [ ] No duplicates across files (normalized-text match)
- [ ] Evidence tags applied (Alfa core set; see `references/verification-tags.md`)
- [ ] Rule includes scope, source, verifiable check, active flag, and evidence tag
- [ ] Unconfirmed proposals are reported but not persisted
- [ ] Removals preserve history by setting `active: false`

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Storing without confirmation | User didn't intend a permanent rule | Always double-confirm |
| Mixing types | "Never" rules in guidelines file | Classify by enforcement level |
| Storing unverifiable rules | Guardian can't check "make it nice" | Rules must be specific and testable |
| Rewriting rule files wholesale | Risky data loss | Append or deactivate one entry at a time |
| Resolving conflicts silently | User loses control of policy | Report conflict and require confirmation |
| Numbering IDs by array length | Collides after a deactivation | Use max numeric suffix + 1 |

## Related Skills

- `session-protocol` — Loads guardrails during bootstrap
- `continuous-learning` — Insights may generate new guardrails
- `code-review` — Guardian checks guardrail compliance

## Usage

Example invocations:

- "/guardrails-management" — Run the full guardrails management workflow
- "guardrails management on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [SUPUESTO]
- Requires English-language output unless otherwise specified. [DOC]
- Does not replace domain expert judgment for final decisions. [DOC]
- Concurrent writes to the same file are not coordinated; a single agent owns the write within a session. [SUPUESTO]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution, require confirmation |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| User says "from now on" but no rule is specific | Ask for a verifiable check |
| Duplicate active rule exists | Do not store; return existing ID |
| User asks to remove a rule | Deactivate by ID, keep audit metadata |
| Target JSON file missing | Create with empty array, then append |
| Rule references a removed/inactive ID | Reject; list active IDs of that type |
