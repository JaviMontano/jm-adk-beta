# JM-ADK Constitution v6.0.0

> 18 principios. 4 puertas de calidad. Cero atajos.

---

## I. Foundation

Meta-principles that govern HOW all other principles are applied. These two are the permanent operating pattern for every decision, every line of code, and every artifact.

### 1. Think First, Act Next

No action without understanding.

- **Understand before modifying**: read existing code, identify boundaries of change, THEN write.
- **Decompose before solving**: break complex problems into atomic sub-problems. Address each with explicit reasoning.
- **Specify before implementing**: Constitution (WHY) → Spec (WHAT) → Plan (HOW) → Tasks (WORK) → Tests (PROOF) → Code (SOLUTION). Phase separation is non-negotiable.
- **Verify before committing**: logic check, fact check, completeness check, bias check. Low confidence → seek information, never proceed on assumption.
- **Evidence before assertion**: every claim tagged with its basis — `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]` `[ASSUMPTION]`. If >30% of claims are `[ASSUMPTION]`, the deliverable triggers mandatory clarification.

**Rationale**: The most expensive code solves the wrong problem.

### 2. Simple First, Robust Next

Start with the simplest solution that satisfies the requirement. Add complexity only when the simple version is proven insufficient through evidence.

- **Working beats perfect**: a tested, working solution today > an over-engineered one that takes 3× longer.
- **Progressive refinement**: build minimum viable first. Add complexity where observed failure demands it.
- **No premature abstraction**: three similar lines > a premature utility function. Abstract only when the pattern has repeated enough to prove it.
- **No speculative features**: build for the current requirement. Ensure extensibility (Principle 11) for future needs.
- **Complexity requires justification**: any solution more complex than the simplest alternative MUST document why the simpler approach was insufficient.

**Rationale**: Unnecessary complexity is the primary source of maintenance burden, onboarding friction, and bugs.

---

## II. Product Architecture

What we build and how it behaves for the end user.

### 3. Client-Rendered, Cloud-Backed

The application is client-rendered, backed by managed cloud services.

- Pages render entirely in the browser — no SSR framework.
- Editable content stored in cloud document store, fetched at runtime.
- Static HTML provides shell; cloud provides data.
- Degraded mode when backend unreachable — cached/fallback content, never blank.
- No custom servers — only managed cloud services (Firebase, Hostinger).

### 4. Accessibility-First

Every page must be usable by people with disabilities.

- All interactive elements keyboard-navigable.
- Modals use proper ARIA attributes.
- Skip-to-content links on every page.
- Color contrast meets WCAG 2.1 AA minimum thresholds.
- Images have meaningful alt text.
- Admin interfaces also meet accessibility standards.

### 5. SEO Integrity

Every public page must be discoverable and correctly described.

- Required meta tags: description, robots, canonical, Open Graph, Twitter Card.
- Internal/admin pages marked `noindex`.
- Sitemap reflects actual structure.
- Dynamic content present in DOM before crawl timeout.

### 6. Offline Resilience

Site degrades gracefully when connectivity is impaired.

- Client-side caching for intermittent connectivity.
- Critical content cached for offline after first visit.
- Clear cache invalidation strategy.
- Last known good content displayed — never an error state.

### 7. Component Consistency

Shared UI patterns implemented once, reused everywhere.

- Site-wide elements use web components.
- Modal behavior uses unified system.
- CSS follows token and layering system (Principle 13).
- Backend access through centralized service modules.
- i18n uses single `data-i18n` attribute contract.

---

## III. Engineering Discipline

How we write, verify, and organize code.

### 8. Test-Driven Development

All production code preceded by tests. Red → green → refactor.

- Tests written BEFORE production code.
- ATDD: feature behavior as executable Given/When/Then.
- E2E covers critical user journeys.
- Security rules tested against emulator.
- Assertions MUST NOT be modified to pass — fix the code instead.
- Feature files hash-locked for integrity.
- Tests run in automation (CI/pre-commit).

### 9. BDD Full-Spectrum Quality

BDD scenarios cover every quality angle, not just functional behavior.

- **Coverage angles**: Strategic, Tactical, Operational, Technical, UX, UI, Backend, Middleware, Data, DevSecOps, CI/CD.
- Given/When/Then as specification language, written BEFORE code.
- Traceability: every scenario → requirement (FR-XXX) → success criterion (SC-XXX) → principle.
- **Runner-agnostic**: Playwright for browser, Vitest for code invariants, Firebase Emulator for rules.
- **Socratic debate for ambiguity**: resolve before implementation, record in `tests/clarifications.md`.

### 10. Sequential-First, Parallel-Ready Workflow

Default execution is sequential along the critical path. Parallelism is a controlled optimization.

- **Sequential by default**: tasks execute one after another. Each completes and its output is verified before the next begins.
- **Parallel only when the plan says so**: activated ONLY when the approved plan marks tasks `[PARALLEL-OK]` with zero pre-dependencies, zero co-dependencies, and zero shared mutable state.
- **WIP limit: 3 agents maximum**: no more than 3 concurrent agents at any time.
- **Forward-only execution**: parallel tasks move independently. If a dependency is discovered mid-execution, the dependent task stops and returns to the sequential queue.
- **Branch-per-task isolation**: each task gets its own branch. No two parallel tasks share a branch.
- **Contract-first integration**: parallel tasks agree on interface contracts BEFORE parallel execution begins.
- **Merge in dependency order**: contracts first, then implementations, then integration tests.

**Rationale**: Sequential execution is inherently safer — linear, auditable history. Parallelism saves time but introduces merge risk. WIP ≤ 3 (Kanban theory) maximizes throughput while keeping cognitive load manageable.

### 11. Code Sustainability

Code written for the next maintainer, not the current author.

- Business-readable naming.
- Consistent naming conventions (kebab-case slugs).
- Self-documenting file structure.
- README per significant module.
- No dead code, no magic numbers.
- Extensible without rewrite.
- Modules communicate through documented contracts.

### 12. Indexable & Self-Organizing Repository

Every directory MUST be navigable by reading only index files.

- **README per directory**: every directory MUST contain a README.md explaining purpose, contents, and relationships.
- **Index-driven navigation**: root README links to top-level dirs; each dir README links to children. No orphan folders.
- **Auto-organization**: new directories immediately get README. Files accumulating without structure get organized into named subdirectories.
- **`.gitignore` governance**: every exclusion pattern has a comment explaining why.
- **Staleness prevention**: directories >30 days without updates flagged for review. Empty dirs removed.

---

## IV. Identity & Content

How we look, speak, and manage the source of truth.

### 13. Design System Governance

Neo-Swiss Clean and Soft Explainer (Corporate Clean and Premium). Canonical spec in `references/brand/design-tokens.json`.

- **Aesthetic**: Ilustración vectorial flat y vibrante con grid suizo, mucho espacio en blanco, composición por columnas (texto + visual), figuras humanas sin rostro, formas geométricas suaves, elementos UI (chips, checklists, timers). Sombras suaves y micro-gradientes discretos.
- **Palette** (exclusiva, 6 colores): Navy #122562, Gold #FFD700, Cyan #137DC5, Dark #1F2833, Lavender #BBA0CC, Gray #808080.
- **Typography**: Poppins (titulares), Trebuchet (cuerpo), Futura (notas/footnotes/callouts), JetBrains Mono (código). Sin excepciones.
- **Legibilidad**: texto grande, alto contraste. Nunca texto sobre fondos ruidosos.
- Tokens en single source of truth: `references/brand/design-tokens.json` v2.0.0.

### 14. Brand Voice Integrity

MetodologIA Brand Voice v3.0 (Premium/Deluxe). Spec completa en `references/brand/brand-voice-v3.0.md`.

- **Estructura**: Minto pyramid — conclusión primero, soportes MECE, evidencia verificable, CTA de un paso.
- **Pilares**: P1 (R)Evolución · P2 Intención antes que intensidad · P3 Tecnología como aliada.
- **Gates**: G1 Minto persistente · G2 Evidencia honesta · G3 Español latino neutro · G4 Lista roja · G5 Veracidad de fuentes · G6 Anclaje a pilares.
- **Idioma**: español latinoamericano neutro, trato «tú».
- **Prohibido**: hack, truco, secreto, resultados instantáneos, arquitecto, arquitectura, transformación.
- **Preferir**: método, diseñar/diseño, sistemas, gobernanza, (R)Evolución, Success as a Service.
- **Rúbrica**: 10 criterios × 0-2 = /20. Aprobación: 20/20 o corregir y revalidar.

### 15. Brand Separation

MetodologIA is a distinct brand. No mixing with other brands.

- No references to parent companies in public content.
- Visual identity consistently MetodologIA.
- Program names match defined catalog exactly.

### 16. Content Authority

Editable content has a single source of truth.

- Each content piece lives in exactly one place.
- Migration: authority shifts incrementally — never both simultaneously.
- Content schema documented and validated.
- Bilingual content (ES/EN) stored together.
- Admin changes take effect immediately.

---

## V. Security & Trust

How we protect data, access, and integrity.

### 17. Secure by Default

Access control at data layer. Input sanitized at boundary. Security verified both statically and at runtime.

- Backend security rules enforce least-privilege.
- Managed identity provider for auth.
- No secrets in client-side code.
- Role-based authorization for admin.
- Security rules version-controlled and tested.
- **Input sanitization**: strip HTML tags (DOMParser), not escape, not allowlist. `<script>` and `<style>` removed with content.
- **Dual-layer verification**: static analysis (grep/scan) + runtime inspection (browser evaluation).
- **Audit trail**: log entries use fully qualified paths (collection, document, field, variant).

---

## VI. Evolution

How we learn, improve, and compound knowledge.

### 18. Continuous Learning Loop

Every decision, debate, and discovery feeds back as a reusable insight. The project compounds knowledge over time.

- **Socratic debate as decision engine**: 2+ options with divergent consequences → structured debate → eliminate by contradiction → record surviving answer.
- **Three outputs per debate**: (1) direct answer, (2) refinements to original question, (3) coverage gaps in adjacent territory.
- **Insights capture**: extract reusable patterns to `insights/<domain>.md` with origin, pattern, rationale, trigger conditions, constitutional anchor.
- **Constitution evolution**: recurring ambiguity → amend constitution to prevent recurrence.
- **Insight consultation before debate**: check `insights/` before starting new debate. If prior insight applies, cite it.
- **No knowledge loss**: insights never deleted — updated or superseded with reference to replacement.

**Rationale**: A project that doesn't learn from its own decisions is condemned to re-debate them.

---

## Quality Gates

| Gate | When | Criteria |
|------|------|----------|
| **G0** | Pre-flight | Secrets scan, branch created, Constitution compliance |
| **G1** | After spec | Spec complete (FR/SC/Given-When-Then), evidence tags, checklist |
| **G2** | After plan | Data model, API contracts, security rules, BDD hash-locked, tokens |
| **G3** | Deploy-ready | All tests pass, Lighthouse ≥ 90, emulator tests, a11y audit, brand voice scan |

## Quality Standards

- No broken links or missing assets.
- No console errors in production.
- Mobile and desktop rendering correct.
- Dynamic content within 2s on 3G or fallback.
- Admin input HTML-stripped before storage.
- Security invariants pass static + runtime verification.
- Audit log paths fully qualified.
- Data-layer behavior tested against Emulator.
- Every directory has README.md.
- Both language variants present before publish.
- Design system tokens enforced.
- Brand voice quality gate passed.
- Evidence tags on all technical claims.

## Development Workflow

### Think Phase
1. Read existing code, understand context.
2. Decompose into atomic sub-problems.
3. Verify spec/plan/tests exist.
4. Identify applicable quality gate.

### Act Phase
5. Write tests before code (TDD/ATDD).
6. Implement simplest passing solution.
7. Refactor for clarity (red → green → refactor).
8. Verify against all BDD angles (Principle 9).

### Verify Phase
9. Run full test suite.
10. Check design token compliance.
11. Scan for secrets, red-list terms, naming violations.
12. Verify accessibility.
13. Confirm quality gate met.

### Integration Phase
14. Branch is atomic and mergeable.
15. Resolve conflicts — never force-push.
16. Run tests after rebase.
17. Update sitemap, SEO, README if affected.

## Workspace

The `workspace/` directory is the user's local interaction layer. It is **gitignored**.

```
workspace/
├── .workspace-registry.json       # Global index of all workspaces
├── YYYY-MM-DD-slug/               # Per-task workspace
│   ├── .workspace.json            # Metadata (status, triad, metrics, gate)
│   ├── tasklog.md                 # Auto-maintained audit trail
│   ├── changelog.md               # Semantic versioning per task
│   ├── plan.md                    # Objective, scope, tasks, acceptance criteria
│   └── artifacts/                 # Generated deliverables
└── archive/                       # Completed workspaces
```

Managed by `scripts/workspace-manager.sh` (Alfa) or `src/lib/workspace.ts` (Beta).

## Session Protocol

Every new working session MUST follow this sequence:

1. **Context loading**: CLAUDE.md → Constitution → Guardrails → PRISTINO-INDEX.md
2. **Workspace detection**: check `.jm-adk.json` → read registry → resume or create workspace
3. **State recovery**: read tasklog of active workspace, check pending tasks, identify stale items
4. **Execution**: run task with triad, log actions, advance quality gates
5. **Closure**: summarize decisions, update tasklog, recommend next steps

## Governance

- **Amendments**: require owner approval, version increment, rationale.
- **Conflicts**: accessibility, security, brand separation > convenience.
- **Foundation** (1, 2) governs all other principles.
- **Test discipline** non-negotiable (8, 9).
- **Quality gates** mandatory (G0–G3).
- **Sequential-first** (10): all execution sequential by default. Parallelism requires plan with `[PARALLEL-OK]`, zero dependencies, WIP ≤ 3.
- **Continuous learning** (18): debates → insights → amendments → fewer debates.
- **Indexability** (12): no folder merges without README.

## Principle Cross-Reference

| v6.0.0 | v5.2.0 | Name |
|:------:|:------:|------|
| 1 | XIII | Think First, Act Next |
| 2 | XIV | Simple First, Robust Next |
| 3 | I | Client-Rendered, Cloud-Backed |
| 4 | II | Accessibility-First |
| 5 | III | SEO Integrity |
| 6 | VIII | Offline Resilience |
| 7 | IV | Component Consistency |
| 8 | IX | Test-Driven Development |
| 9 | XV | BDD Full-Spectrum Quality |
| 10 | XVI | Sequential-First Workflow |
| 11 | XII | Code Sustainability |
| 12 | XVIII | Indexable Repository |
| 13 | X | Design System Governance |
| 14 | XI | Brand Voice Integrity |
| 15 | V | Brand Separation |
| 16 | VI | Content Authority |
| 17 | VII | Secure by Default |
| 18 | XVII | Continuous Learning Loop |

---

**Version**: 6.0.0 | **Ratified**: 2026-03-25 | **Previous**: 5.2.0
