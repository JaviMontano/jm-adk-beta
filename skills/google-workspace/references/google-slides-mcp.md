<!-- distilled from alfa skills/google-slides-mcp -->
<!-- > -->
# Google Slides MCP

## TL;DR

Plan and execute Google Slides work through `workspace-mcp` with a read/checklist-first workflow. Compile the plan offline (`scripts/compile-google-slides-mcp.py`), then touch live MCP tools only after scope review and explicit human confirmation for mutations. [DOC]

**Scope of this reference.** Five Slides operations over `workspace-mcp`, least-privilege OAuth, and a human-gated mutation path. [DOC]
**Anti-scope (out of contract).** Drive file management, comments/revisions APIs, Apps Script, exporting to PPTX/PDF, bulk presentation generation, and any MCP tool not in the table below. Route those to the relevant Drive/Docs reference instead. [ASSUMPTION]

## Assumptions

- `workspace-mcp` is configured in `.mcp.json` and exposes the five tools below; OAuth is already granted at a profile from `scope-policy.json`. [ASSUMPTION] Verify: step 2-3 of the Live Checklist.
- A human reviewer is reachable in-session to confirm mutations; if not, stop before any create/batchUpdate. [ASSUMPTION]
- `python3` runs the compiler with no network egress; CI/sandbox without internet is the expected case. [INFERENCE]

## Source Order

1. Read local setup docs: `docs/google-workspace-mcp-setup.md` and `docs/mcp-integration.md`. [DOC]
2. Use primary Google Slides REST docs for operation shape: `presentations.create`, `presentations.get`, `presentations.batchUpdate`, `presentations.pages.get`, `presentations.pages.getThumbnail`. [DOC]
3. `assets/scope-policy.json` for least-privilege scope selection. [CONFIG]
4. `assets/human-confirmation-policy.json` before any `presentations.create` or `presentations.batchUpdate`. [CONFIG]

Conflict rule: local setup docs win over remote REST docs on tool wiring; REST docs win on request/response shape. [INFERENCE]

## Offline First

Run the deterministic compiler before live tools:

```bash
python3 skills/google-slides-mcp/scripts/compile-google-slides-mcp.py \
  --input skills/google-slides-mcp/scripts/fixtures/google-slides-mcp-input.json
```

The compiler reads only local `assets/` and fixture JSON. It makes no Google, OAuth, network, or MCP calls. [CODE] A clean compile is a precondition, not a substitute, for live read-back validation. [INFERENCE]

## Operation Contract

Use ONLY these Slides operations; anything else is anti-scope. [DOC]

| Action | REST method | MCP tool | Mode |
|---|---|---|---|
| `presentations.create` | `POST /v1/presentations` | `mcp__workspace-mcp__create_presentation` | mutating |
| `presentations.get` | `GET /v1/presentations/{presentationId}` | `mcp__workspace-mcp__get_presentation` | read-only |
| `presentations.batchUpdate` | `POST /v1/presentations/{presentationId}:batchUpdate` | `mcp__workspace-mcp__batch_update_presentation` | mutating |
| `presentations.pages.get` | `GET /v1/presentations/{presentationId}/pages/{pageObjectId}` | `mcp__workspace-mcp__get_page` | read-only |
| `presentations.pages.getThumbnail` | `GET /v1/presentations/{presentationId}/pages/{pageObjectId}/thumbnail` | `mcp__workspace-mcp__get_page_thumbnail` | read-only expensive read |

## Safety Rules

- Prefer `https://www.googleapis.com/auth/drive.file` when work is limited to presentations created or opened with this app. [CONFIG]
- Use `https://www.googleapis.com/auth/presentations.readonly` for read-only access across Slides files when `drive.file` is not enough. [CONFIG]
- Avoid `https://www.googleapis.com/auth/drive` and `.../auth/drive.readonly` unless a written exception explains why narrower scopes cannot satisfy the workflow. [CONFIG]
- Require human confirmation for every mutating operation. [CONFIG]
- For `presentations.batchUpdate`, first prove the target presentation is known via a prior `presentations.get` or a same-plan `presentations.create`. [DOC]
- Treat thumbnail `contentUrl` as ephemeral and requester-scoped; never persist it into durable docs, logs, or examples. [DOC]
- Use `writeControl.requiredRevisionId` for collaborative or high-impact updates when a current revision is available. [DOC]

## Failure Modes and Edge Cases

| Symptom | Likely cause | Action |
|---|---|---|
| 403 `insufficientPermissions` on read | scope narrower than data (e.g. `drive.file` on a file this app did not open) | escalate to `presentations.readonly`, document the exception [INFERENCE] |
| 403 on `batchUpdate` after a clean `get` | mutating scope missing though read scope present | request a write profile from `scope-policy.json`, do NOT silently widen to `auth/drive` [INFERENCE] |
| 400 invalid `requiredRevisionId` | presentation edited since last `get` | re-run `get`, re-confirm mutation text, retry [DOC] |
| `batchUpdate` partial apply | one request in the array invalid | treat the whole batch as suspect; read back, never assume atomicity across requests [ASSUMPTION] |
| Thumbnail URL 404 on reuse | `contentUrl` expired (ephemeral) | re-call `get_page_thumbnail`; never cache the URL [DOC] |
| Duplicate presentation created on retry | `create` retried after a timeout that actually succeeded | search before re-creating; `create` is not idempotent [INFERENCE] |

## Assets and Scripts

- `assets/google-slides-mcp-schema.json` — stable offline input contract. [CODE]
- `assets/scope-policy.json` — maps Slides actions to minimum OAuth scope profiles. [CODE]
- `assets/mcp-tool-contract.json` — maps MCP tool names to real Slides REST methods. [CODE]
- `assets/human-confirmation-policy.json` — defines mutation gates. [CODE]
- `assets/google-slides-operation-template.md` — renders deterministic Markdown output. [CODE]
- `scripts/compile-google-slides-mcp.py` — validates structured input, compiles the plan/checklist. [CODE]
- `scripts/check.sh` — runs offline fixture checks. [CODE]

## Live Execution Checklist

1. Compile the offline plan and review validation. [DOC]
2. Confirm `.mcp.json` exposes `workspace-mcp` with the expected tool tier. [DOC]
3. Verify the granted OAuth scope matches the minimum viable scope profile. [DOC]
4. Execute read-only calls first: `get_presentation`, `get_page`, or `get_page_thumbnail`. [DOC]
5. Ask the user to confirm the exact mutation text before calling create or batchUpdate. [DOC]
6. After mutation, read back the presentation or page and compare against the plan. [DOC]

## Worked Example — add a title slide to an existing deck

1. Compile offline with a fixture naming the target `presentationId` and the insert request. [CODE]
2. `get_presentation` → capture current `revisionId` and confirm the target slide exists. [DOC]
3. Present the exact `batchUpdate` body (`createSlide` + `insertText`) to the human; wait for confirmation. [DOC]
4. `batch_update_presentation` with `writeControl.requiredRevisionId` set to the captured `revisionId`. [DOC]
5. `get_page` on the new slide; diff text and layout against the plan; report residual risk if any field differs. [INFERENCE]

## Acceptance Criteria

- Offline compile passes before any live call; no live mutation without a logged human confirmation. [DOC]
- Every live call maps to exactly one row of the Operation Contract; no out-of-table tools used. [DOC]
- Mutating calls are preceded by a proven-known target and followed by a read-back diff. [DOC]
- Selected OAuth scope is the narrowest that satisfies the workflow; any widening carries a written exception. [DOC]
- No thumbnail `contentUrl` persisted anywhere durable. [DOC]

## Output

Return Markdown using `templates/output.md`, with evidence, scope review, operation checklist, validation, and residual risks. Use `templates/output.html` only when the user asks for a standalone HTML report. [DOC]
