# Pristino Beta — Core Contract

Generated adapter (source: runtime/core.md + delta). Do NOT hand-edit — regenerated on every build; manual changes lost. [DOC]

## Identity

Catalog-driven harness. 3 brands, never mixed — identify brand FIRST. [DOC]
- Sofka (enterprise) · MetodologIA (open) · JM Labs (personal).
- [SUPUESTO] Brand inferable from context; if ambiguous, HALT and ask — never default.

## Hard rules

1. Evidence tag on every claim: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]`. Untagged = defect.
2. NEVER prices — FTE-months + disclaimers only. No currency, rates, totals.
3. Read before write; `catalog/skills.json` = single source of truth. Stale read → re-read, never assume.
4. Script-first: any step expressible as a script IS a script under `scripts/`. Prose only for non-deterministic logic.
5. Constitution v6.0.0 enforced in execution phases: extract MUST/MUST NOT, HALT on violation (`references/ontology/constitution-v6.0.0.md`). [DOC]
6. Verification before done — proven by artifact existence, never assertion.

## Skill protocol

- Tier-0 index = one line per skill. Invoke → Read that skill's `SKILL.md` only; never preload siblings.
- Routers (®): resolve `params` from request (ask ONLY if ambiguous), Read exactly ONE playbook from `routes:`. Never load the whole cluster.
- `depth=quick|deep`, default `quick`. Escalate to `deep` only on explicit request or failed `quick`.
- Subagent output compressed (locator / receipt / findings, `references/roles/`).
- Auto-clarity override — normal prose (not compressed) for: security warnings, irreversible actions, ordered sequences.

## Phase gates

- Completion = artifact existence: `scripts/check-prerequisites.sh --phase <p> --json`. Truth is the filesystem, not the log.
- Soft gates warn and continue; hard gates require 100% and BLOCK on miss.
- [SUPUESTO] `--json` is machine-parsed by the orchestrator; non-zero exit = gate failure.

## Anti-scope

- [SUPUESTO] This adapter governs runtime behavior only; building the adapter itself is out of scope (owned by the delta + generator).
- No brand mixing, no price emission, no untagged claims, no whole-cluster reads, no "done" without an artifact. Any = contract breach, HALT.

## Acceptance criteria

- Every claim carries exactly one evidence tag; no price tokens.
- Single brand per output; brand declared before first content line.
- Each phase marked complete has its prerequisite artifacts on disk (gate script verified), not asserted.
- Constitution MUST/MUST NOT extracted and unviolated for every execution-phase action.

## Claude Code delta

Runtime behaviors specific to Claude Code; base ADK runtime applies otherwise. [DOC]

- Hooks (`hooks/hooks.json`) [CONFIG]: session-init, prompt filter, persona calibrate, pre/post tool guards, stop validator. Order is load order; a non-zero pre-tool guard blocks the call, stop validator can veto turn-end. [INFERENCE]
- Skills: auto-discovered from `skills/*/SKILL.md` (missing/malformed frontmatter -> skill skipped, not fatal). MCP via `.mcp.json` (generated; do not hand-edit, regenerate). [CONFIG]
- Subagents: parallel `[P]` tasks via Task tool; read-only agents hint `model: haiku`. [CODE]
- Acceptance: hooks fire in declared order, all skills resolve or are logged-skipped, `.mcp.json` valid, `[P]` tasks run concurrently. [ASSUMPTION]
- Anti-scope: no global Claude config, secrets, or provider/model swap here. [EXPLICIT]

## Skills

`accessibility`® Accessibility: WCAG audit, testing, a11y design, inclusive copy.
`adaptive-investigation-method` Investigar dominios desconocidos: mapeo barato, budget acotado.
`agent-orchestration`® Multi-agent orchestration: workflows, triads, routing, parallel.
`agentic-loop-engineering` Bucle agentico: enruta por stop_reason, budget duro.
`ai-architecture`® AI/LLM architecture: software, pipelines, conops, patterns, audit.
`ai-quality`® AI quality: testing, code review, safety, content detection.
`architecture`® Software architecture: API, DDD, events, realtime, caching.
`brand-output`® Branded output: HTML, DOCX, XLSX, folios, templates (Sofka DS).
`business-analysis`® Business analysis: process modeling, requirements, feasibility.
`carrera`® Carrera: seleccion, entrevistas, negociacion, CV, onboarding.
`claude-md-architecture` Memoria jerarquica CLAUDE.md user/team/module con at-imports.
`context-window-engineering` Ensamblar ventana de contexto del agente, maximizar reuso.
`custom-tooling-extension` Slash command vs skill: decidir y escribir su frontmatter.
`daily-close` Cierre diario: cerrado/pendiente/aprendido + siembra manana.
`data-governance`® Data governance: privacy, data strategy, catalog/documentation.
`data-platform`® Data engineering: pipelines, quality, validation, migration.
`dbr-daily-plan` DBR: <=3 prioridades-tambor del dia, plan diario P09.
`devops-deploy`® CI/CD and release: pipelines, environments, deployment gates.
`docs-writing`® Docs and writing: technical docs, changelogs, diagrams.
`email-comms`® Email systems: transactional sending, templates, newsletters.
`evaluation-confidence-design` Evaluacion con confidence calibrada, stratified sampling.
`firebase`® Firebase: auth, hosting, functions, firestore, emulators.
`frontload-prompt` Reformatea input largo/ambiguo a estructura SPEC.
`google-workspace`® Google Workspace: Sheets, Docs, Drive, Gmail, Calendar.
`guardrails`® Guard layer: tool guards, prompt filter, output contracts.
`hosting-infra`® Hosting/infra: DNS, domains, SSL, CDN, serverless, backup/DR.
`iikit`® Intent Integrity Kit: spec-driven development pipeline.
`integrations`® Third-party integration router: payment + service playbooks.
`jarvis-bootstrap` Bootstrap Jarvis OS: CLAUDE.md/MEMORY.md raiz + estructura minima.
`jarvis-os` Personal Jarvis OS: COOL, detecta sector/estacion, enruta packs.
`kata`® Agentic katas: prompt/loop/tooling patterns from JM Labs.
`lab-session` JM Labs Lab session: 4 archivos canonicos (notas, hipotesis).
`legal-compliance`® Legal/compliance: contract-review, compliance-assessment.
`market-intel`® Market intel: positioning, pricing, sector, benchmarks.
`marketing-content`® Marketing content: copy, calendars, PR, cases, whitepapers.
`mcp-engineering` Configurar MCP servers (scope, env-vars) y contratos de tools.
`message-batch-orchestration` Message Batches API offline: custom_id unico, fragmentacion.
`monthly-audit` Auditoria mensual del jarvis: rubrica 6 preguntas P22, evidencia.
`observability`® Production health: monitoring, logging, alerting, incidents.
`official-source-verifier` Verify decisions vs official sources (ADK, Skills spec, Git).
`persistent-memory-design` Scratchpad en disco: Hypotheses/Decisions/Findings/Open.
`plan-mode-workflow` Gate de dos modos: Plan Mode read-only, firmar, ejecutar.
`pm-delivery`® PM/delivery: budgets, estimation, capacity, roadmaps, OKRs.
`pristino-calibration` Read persona/mode/optimizer signals from persona-calibrate.sh.
`product-analytics`® Product analytics: instrumentation, KPIs, A/B tests, cohorts.
`project-create` Scaffold proyecto Jarvis P-NNN-slug con CLAUDE.md compliant.
`prompt-chaining-design` Descomponer en pase local tipado + pase de integracion.
`prompting-and-meta-prompting` Vague intent into durable, eval-ready prompts + meta-prompts.
`provenance-engineering` Pipelines con provenance tipada: no hay claim sin fuente.
`qbr-quarterly` QBR P13: audita el trimestre vs OKRs y planifica el proximo.
`revisor-veracidad` Audita texto, etiqueta cada afirmacion no reproducible con tag.
`runtime-routing` Route work across Claude, Codex, Gemini, Antigravity, local.
`safe-scripting-and-bash` Safe, portable, dry-run-first Bash for local agentic workflows.
`sales-bizdev`® Sales/bizdev (ES/EN consulting): prospecting and pipeline.
`security`® App security: auth, RBAC, input sanitization, headers/CORS.
`self-correction-loops` Verificacion declarado-vs-calculado con mismatch flag y escalada.
`seo-growth`® SEO/growth: technical SEO, content SEO, landing pages, funnels.
`session-lifecycle-management` Resume vs fork vs fresh segun validez de contexto.
`session-workspace`® Agent session lifecycle: bootstrap, protocol, state management.
`skill-foundry`® Build/certify agentic assets: skills, agents, commands, hooks.
`station-create` Scaffold estacion Jarvis (universal/dedicada) con su CLAUDE.md.
`structured-output-design` Extraccion estructurada: contrato JSON Schema defensivo.
`subagent-orchestration` Hub-and-spoke subagent plans with AgentDefinition.
`task-subfolder` Sub-tarea T-NNN multi-sesion: CLAUDE.md, task.md, log.md (P33).
`testing-qa`® Software testing: bdd, unit, integration, e2e.
`tool-use-design` Tool-description routing contracts with explicit input formats.
`ux-design`® UI/UX: design systems, interaction, onboarding, microcopy.
`ux-research`® User research: interviews, surveys, usability testing.
`validation-retry-design` Extract-validate-retry loops with actionable validation errors.
`wbr-weekly-review` WBR P11: repaso semanal de avances, estancado y friccion; acta.
`web-frontend`® Frontend: react, angular, web-components — one topic.
`weekly-retro` Retro semanal P12: que ayudo, que friccion, promueve mejoras.
`workspace-setup` Dry-run-first local workspace profile plan (.jm-adk.local.json).
