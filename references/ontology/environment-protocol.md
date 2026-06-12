# Environment Detection Protocol

Pristino adapts to the runtime by detecting two **independent** axes: the
**runtime mirror** (which instruction family loaded it) and the **model tier**
(what powers it and how much context it admits). Both are detected every session;
neither implies the other (e.g. claude-code can run a Light model; cursor can run
Opus). Evidence tags: `[EXPLICIT]` observed in the runtime, `[INFERENCE]` derived,
`[ASSUMPTION]` unverified default.

## Scope

- **In scope**: detecting runtime + model, selecting triad mode, sizing context
  budget, reporting the detected environment.
- **Out of scope** (anti-scope): authentication, tool installation, MCP server
  provisioning, model routing/selection (the user/host picks the model — Pristino
  only reads its tier). This protocol never *changes* the environment; it observes
  and adapts.

## Runtime Mirror Detection

The runtime family is the one whose homologated instruction mirror actually loaded
the agent. Detection is **file-presence based** `[EXPLICIT]`.

| Instruction File | Runtime family | Detection |
|-----------------|-----|-----------|
| `CLAUDE.md` | claude-family | Claude Desktop, Claude Code, Claude Cowork |
| `GEMINI.md` | gemini-family | Gemini CLI, Gemini Code Assist, Antigravity family |
| `AGENTS.md` | agents-family | OpenAI Codex, Visual Studio-family agents |
| `.cursorrules` | cursor | Cursor IDE |
| `.windsurfrules` | windsurf | Windsurf IDE |
| `.github/copilot-instructions.md` | copilot | Visual Studio / VS Code bridge to AGENTS.md |
| `.agent/rules/GEMINI.md` | antigravity | Antigravity bridge to GEMINI.md |

**Precedence when multiple files are present** (common: a repo ships several
mirrors): pick the family whose loader is actually executing, not the first file
on disk `[INFERENCE]`. Resolve by, in order: (1) host self-identification if the
runtime exposes it; (2) the more specific bridge file over its generic parent
(`.agent/rules/GEMINI.md` → antigravity, not gemini-family; copilot-instructions
→ copilot, not agents-family); (3) presence of the Agent tool ⇒ claude-code.
**On ambiguity or no match**: default to the most conservative family that fits
the visible tooling and report it as `[ASSUMPTION]`; never silently guess Full mode.

## Runtime Capability Matrix

"Runtime-dependent" = the family supports it but the specific host build may not;
verify before relying on it `[ASSUMPTION]`.

| Runtime | Triad Mode | Agent Tool | Subagents | Hooks | MCP | Skill Loading |
|-----|-----------|------------|-----------|-------|-----|--------------|
| **claude-code** | Full (parallel subagents) | Yes | Yes | Yes | Yes | SKILL.md via Read |
| **claude-desktop/cowork** | Claude-family, runtime-dependent | Runtime-dependent | Runtime-dependent | Runtime-dependent | Runtime-dependent | CLAUDE.md |
| **gemini-cli/code-assist** | Sequential prompts | Runtime-dependent | Runtime-dependent | Runtime-dependent | Runtime-dependent | GEMINI.md |
| **cursor** | Checklist | No | No | No | Yes | .cursorrules inline |
| **windsurf** | Checklist | No | No | No | No | .windsurfrules inline |
| **copilot** | Suggestion | No | No | No | No | Instructions inline |
| **antigravity** | Adapter-guided, validation pending | Pending | Pending | No | No | skills_index.json |
| **codex** | Sequential prompts | No | No | No | No | AGENTS.md inline |
| **visual-studio** | Suggestion/checklist | No | No | No | Runtime-dependent | AGENTS.md / Copilot bridge |

**Capability probing, not assumption**: treat the matrix as the expected default,
then confirm the load-bearing capability (Agent tool, MCP, hooks) by attempting a
cheap no-op or reading the host manifest before depending on it. A missing
capability **downgrades** the triad mode (Full → Sequential → Checklist →
Suggestion); it never aborts the session.

## Triad Adaptation by Runtime

The triad (Lead → Support → Guardian) is **always applied**; only its *mechanism*
changes with runtime capability. Lead = domain deliverable; Support = cross-cutting
review (accessibility, security, consistency); Guardian = quality gate + evidence
tagging. Acceptance criterion for every mode: all three perspectives are visible in
the final output, regardless of whether they ran as separate agents or inline passes.

### Full Mode (claude-code)

The Agent tool is available. Pristino launches 3 subagents sequentially (sequential
hand-off preserves context fidelity; parallel is reserved for independent fan-out,
not the dependent triad chain):

```
1. Launch Lead agent (domain specialist)
2. Pass Lead output to Support agent (cross-cutting review)
3. Pass combined output to Guardian agent (quality validation)
4. Synthesize final output
```

### Adapter-Guided Mode (antigravity)

Antigravity loads the Gemini-family mirror through `.agent/rules/GEMINI.md`.
Subagent, function-calling, and multimodal support is **validation pending** until
checked in the target environment `[ASSUMPTION]` — do not assume Full mode here.

```
1. Load GEMINI-family contract
2. Load skills_index.json
3. Apply Lead → Support → Guardian as runtime capabilities allow
4. Fall back to sequential triad in one response when subagents are unavailable
```

### Sequential Prompts Mode (gemini, codex)

No Agent tool. The user drives transitions between triad steps:

```
1. Pristino describes the triad composition
2. Acts as Lead: produces primary deliverable
3. Acts as Support: self-reviews with cross-cutting criteria
4. Acts as Guardian: applies quality gate checklist
5. Outputs final result with all three perspectives applied
```

### Checklist Mode (cursor, windsurf)

No Agent tool. Triad expressed as inline review criteria, all in one response:

```
1. Model generates code (Lead perspective)
2. Model applies cross-cutting checks from rules file (Support criteria)
3. Model runs quality gate checklist (Guardian validation)
```

### Suggestion Mode (copilot)

Limited context. Triad reduced to quality standards baked into suggestions:

```
1. Model suggests code (Lead)
2. Suggestions follow accessibility + security rules (Support criteria embedded)
3. Evidence tags recommended in comments (Guardian standard)
```

## Model Tier Detection

The model tier determines how much context can be loaded. Detect from the host's
declared context window when available `[EXPLICIT]`; otherwise infer from the model
id `[INFERENCE]`. **When the window is unknown, assume Light** and load
conservatively — under-loading degrades gracefully; over-loading truncates the
Constitution mid-session `[ASSUMPTION]`.

| Tier | Context Window | Load | Best For | Example Models |
|------|---------------|------|----------|---------------|
| **Heavy** | > 100K tokens | Full Constitution + Index + History | Architecture, complex analysis, full triad | Claude Opus, Gemini 2.5 Pro, GPT-4o |
| **Medium** | 32K - 100K | Constitution + active skills | Development, code generation | Claude Sonnet, Gemini Flash, Llama 70B, GPT-4o-mini |
| **Light** | < 32K | Active skill only | Quick edits, routing, lookups | Claude Haiku, Gemma 9B, Mistral 7B |

Boundaries are inclusive at the lower edge (exactly 100K → Medium; exactly 32K →
Medium). Tier is about *headroom*, not capability — a Heavy model on a near-full
context behaves as Light; re-tier mid-session if usable headroom drops below the
next threshold `[INFERENCE]`.

### Context Budget by Tier

```
Heavy:  Load PRISTINO.md + constitution-v7.0.0.md + PRISTINO-INDEX.md + full history
Medium: Load PRISTINO.md + constitution-v7.0.0.md + relevant skills only
Light:  Load PRISTINO.md summary + active skill only
```

## Model Provider Matrix

Provider affects **function-calling fidelity** (see Minimum Requirements), not tier.

| Provider | Models | Function Calling | IDEs |
|----------|--------|-----------------|------|
| **Anthropic** | Opus, Sonnet, Haiku | Yes | Claude Code, Cursor, Windsurf |
| **Google** | Gemini 2.5 Pro, Flash | Yes | Gemini, Antigravity, Cursor |
| **OpenAI** | GPT-4o, GPT-4o-mini, o3, o4 | Yes | Copilot, Cursor, Codex |
| **Groq** | Llama 3.3 70B, Mixtral, Gemma | Yes | Open Claw, Cursor |
| **OpenRouter** | All above + DeepSeek, Qwen | Yes | Open Claw, Cursor |
| **Ollama** | Llama, Mistral, CodeLlama | Partial | Local CLI, Cursor |

**Ollama `Partial`**: tool calling is model- and template-dependent and may be
unreliable; treat as advisory mode unless tool calls are verified working `[ASSUMPTION]`.

## Auto-Priming by Environment

At session start, after bootstrap (PRISTINO.md → Constitution → Index):

1. **Detect runtime mirror** from instruction file (apply precedence rules above)
2. **Detect model tier** from available context window (default Light if unknown)
3. **Set triad mode** (full / sequential / checklist / suggestion)
4. **Diagnose user context** via `scripts/diagnose-user-context.py --dry-run`
5. **Load skills** appropriate to the tier
6. **Report** environment to user

```
Environment detected:
  Runtime: claude-code | Triad: full | Model tier: heavy
  Tools: Read, Write, Edit, Glob, Grep, Bash, Agent
  Skills loaded: 116 | Agents available: 103
  User context: ready
  Ready to orchestrate.
```

**Failure handling per step**: if step 4 errors (script missing/non-executable),
report `User context: unavailable` and continue — priming is not blocked by
diagnostics. If runtime or tier is `[ASSUMPTION]`, surface it in the report so the
user can correct it (e.g. `Model tier: light (assumed — window unknown)`).

**Re-priming triggers**: re-run detection when the instruction mirror changes
mid-session, when context headroom crosses a tier boundary, or when a previously
assumed capability is proven present/absent.

## Minimum Requirements

For JM-ADK agents to **execute** (not merely advise), the model MUST support:

- **Function/tool calling** — required for Read, Write, Bash tools
- **System messages** — required for Constitution injection
- **Context >= 8K tokens** — minimum for a single skill + conversation

Models meeting none-to-some of these operate in **advisory mode only** — they
suggest but do not execute. Specifically: no function calling ⇒ advisory; no system
messages ⇒ inject Constitution as a leading user turn (degraded fidelity); window
< 8K ⇒ refuse multi-skill work and route to a single-skill lookup. Advisory mode is
a valid terminal state, not an error — report it and proceed.
