# Skills Index (tier-0)

GENERATED — do not edit by hand. Source of truth: `catalog/skills.json`; regenerate with `python scripts/build-indexes.py` (also rebuilds this header). Hand edits are overwritten on next build. [DOC]

Tier-0 = always-loaded discovery layer: one line per skill so the agent picks a skill WITHOUT reading any SKILL.md. Match the user request to a `id` + description, then load `skills/<id>/SKILL.md` (path is derivable from the id, never listed here). [DOC]

Legend [DOC]:
- `id` — backtick code span; the slug. Open `skills/<id>/SKILL.md` to run it.
- ® — router skill: `params` (topic enum + depth) live in its frontmatter `routes`. Resolve the topic, read exactly ONE playbook under that skill's `references/` — not the whole skill.
- (no ®) — leaf skill: SKILL.md is the full playbook; many carry a `(Pnn)` cadence/process id.
- … — description elided for width; the authoritative full text is the SKILL.md `description`.

Selection contract [DOC]: pick the single best id; if two tie, prefer the more specific; if none fit, fall back to the closest ® router and let its topic param disambiguate; if still unmatched, ask — do NOT invent an id or a path. Anti-scope: this index lists no params, routes, tools, or versions — read the SKILL.md for those.

Counts [INFERENCE]: 73 skills, 35 routers (®), 38 leaf. Sorted by id; stable for diffing.

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
