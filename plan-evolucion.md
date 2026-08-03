# Plan de Evolución — Pristino Beta (gobernanza + orquestación + routing)

> Plan robusto, fásico, iterable, anti-perderse. Ejecutar una fase por vez.
> Cada fase = atómica, verificable, reversible (rollback = `git revert`).
> **Fuente de verdad del progreso = la tabla de estado (§0).** Al reanudar,
> leer §0 → próxima fase PENDING → ejecutar §<fase> → commit → actualizar §0.

---

## §0 — Tabla de estado (leer primero al reanudar)

| Fase | Título | Status | Commit | Notas |
|------|--------|--------|--------|-------|
| P0 | README remediation | PENDING | — | stale v6→v7, budgets, layout, ICM section |
| P1 | docs governance (index + ADR-0002 + debt update) | PENDING | — | hand-edit docs/, no regen |
| P2 | Elevar modelo ICM a core.md (shared) + budget bump | PENDING | — | SOURCE edit + regen + budget verify (crítico) |
| P3 | Optimizar routing/orquestación (manifest --enforce, router, session-init) | PENDING | — | script edits, no regen |
| P4 | Sensor de consistencia de gobernanza + gate p7 | PENDING | — | nuevo script |
| P5 | Alinear agents/ + commands/ a ICM | PENDING | — | hand-edit, no regen |
| P6 | Verificación final + commit + PR | PENDING | — | cierre |

**Convención de status:** `PENDING` → `IN_PROGRESS` (asignar + `git checkout -b`) → `DONE` (commit hash aquí). Una fase `DONE` tiene su commit en la columna Commit.

---

## §1 — Reglas duras (aplicar a cada fase)

1. **NUNCA hand-editar generated files.** `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.agent/rules/GEMINI.md`, `SKILLS.md`, `.agent/skills_index.json`, `.mcp.json` son generados por `scripts/build-indexes.py` desde fuente. Cambios manuales se pierden en regen. Para cambiar conducta: editar fuente canonical (`runtime/core.md`, `runtime/delta-*.md`, `catalog/skills.json`, `harness/manifest.json`) → regenerar.
2. **Source antes que output.** Editar fuente → regen (`python3 scripts/build-indexes.py`) → verificar budgets → commit. Nunca al revés.
3. **Budget = blocker pre-release.** Tras cualquier cambio a `core.md`/deltas/`manifest.json`: correr `python3 scripts/check-token-budget.py`. Si falla, la fase NO está DONE. Budgets actuales: claude 2601/3000, antigravity 3812/4000, codex 2386/2600. Headroom: claude 399, antigravity 188, codex 214.
4. **Una fase = un branch = un commit.** `git checkout -b feat/evolucion-p<N>` desde `main` (o desde la rama de la fase previa si encadenadas). Commit al final. Mensaje termina con `Co-Authored-By: Claude <noreply@anthropic.com>`.
5. **Edit-source principle (ICM).** Si un output está mal, arreglar el contract/fuente, no el output.
6. **Verificación antes de DONE.** artifact existence (gates), no aserto. Correr §6 harness completo.
7. **Anti-scope.** No mezclar brands, no estimaciones sin computar, no claims sin evidence tag, no "done" sin artifact.
8. **Caveman honesty.** Números en docs generados solo desde `evals/` committed, nunca hand-typed.

---

## §2 — Riesgos y mitigaciones

| Riesgo | Prob | Impacto | Mitigación |
|--------|------|---------|------------|
| Overflow budget antigravity/codex al editar core.md | Alta (P2) | Blocker | Medir antes/después; bump budget documentado si necesario; preferir compactar core.md antes que inflar |
| Hand-editar generated file por hábito | Media | Anti-scope breach | §1 regla 1; `git status` antes de commit debe mostrar solo fuente |
| Introducir stale ref (v6 vs v7) | Media | Inconsistencia docs | P4 sensor lo detecta; correr al final de cada fase |
| Perderse entre fases al reanudar | Media | Progreso estancado | §0 tabla + §7 resume protocol; commit por fase |
| Regen produce diff inesperado | Baja | Confusión | `git diff` post-regen; si diff no coincide con fuente editada, abortir y diagnosticar |

---

## §3 — Estado actual auditado (baseline, 2026-08-03)

Gaps encontrados (evidence-tagged), a cerrar por fases:

- `[DOC]` README.md L33: "Constitution v6.0.0" → repo es v7.0.0. WRONG.
- `[CONFIG]` README token table: 2301/3614/2281 → actual 2601/3812/2386. STALE.
- `[CONFIG]` README L82: "check-token-budget.py fails (3075/2600)" → ahora PASS. STALE.
- `[DOC]` README Layout: omite `agents/`, `commands/`, `evals/`, `discovery/`, `project/`. INCOMPLETE.
- `[DOC]` README: sin mención ICM routing (first-prompt-router, workspace-bootstrap, stage-context-manifest, 5-layer model). MISSING.
- `[DOC]` core.md: sin modelo ICM (5 layers, one-stage-one-job, edit-source, stage-context-manifest). Vive solo en `delta-claude.md`; codex/antigravity heredan vía ref frágil ("fields: delta-claude § First-prompt routing"). FRÁGIL.
- `[DOC]` Sin ADR-0002 (decisión compliance audit + constitution-must slice). MISSING.
- `[CONFIG]` Sin sensor de consistencia (stale v6/v7, budget table vs evals/, README vs core). MISSING.
- `[DOC]` `docs/harness-debt-findings.md`: no marca constitution-must slice + manifest como resueltos. STALE.

**Ya bueno (no tocar):** gates p0-p6 READY, coverage 611, evals 36/36, generated files limpio (no hand-edits), ICM routing funcional en 3 runtimes, stage-context-manifest sensor operativo (4/4 stages <8000t).

---

## §4 — Fases

### P0 — README remediation

**Objetivo:** README.md consistente con estado actual + expone ICM routing.

**Source edits (hand, NO generated):**
- `README.md`:
  - L33: "Constitution v6.0.0" → "Constitution v7.0.0"; agregar `references/ontology/constitution-must.md` (slice fino L3).
  - Token table: reemplazar 2301/3614/2281 con 2601/3812/2386 (leer de `evals/token-benchmark.json` via `python3 scripts/token-stats.py` — no hand-typing; si `evals/` no tiene los números post-PR#5, correr `token-stats.py` primero para actualizar).
  - L82: borrar/bloque "check-token-budget.py fails" → reemplazar con "PASS (claude 2601/3000, antigravity 3812/4000, codex 2386/2600)".
  - Layout: agregar `agents/` (21 defs), `commands/` (5), `evals/` (token-benchmark), `discovery/` + `project/` (active-plugin), `migrate/` (throwaway, deleted at GA).
  - Nueva sección "## ICM routing (first prompt)" — explica `first-prompt-router.sh` (detecta create/resume/new/resume_task/ambiguous), `workspace-bootstrap.sh` (instancia workspace), `stage-context-manifest.sh` (Inputs table ejecutable, budget 2-8k/stage enforced), 5-layer model, link ADR-0001 + ADR-0002.
  - Status: actualizar a "p0-p6 READY, budgets PASS, ICM routing + compliance audit done (PR #5)".

**Regen:** NONE (README no es generated).

**Verificación:** `grep -c "v6.0.0" README.md` == 0 (excepto histórico); `python3 scripts/token-stats.py` (confirmar evals actualizado); leer README completo.

**Acceptance:** README sin stale refs v6; token table coincide con `evals/token-benchmark.json`; Layout completo; sección ICM presente; links a ADR-0001/0002 válidos.

**Rollback:** `git revert <commit>`.

---

### P1 — docs governance (index + ADR-0002 + debt update)

**Objetivo:** docs/ como capa de gobernanza navegable + decision record de la compliance audit.

**Source edits (hand, NO generated):**
- `docs/decisions/0002-icm-compliance-audit.md` (NEW): Context (auditoría vs paper arXiv 2603.16021v2 via NotebookLM), Decision (stage-context-manifest sensor = Inputs table ejecutable; constitution-must slice = configure-the-factory; template completeness), Consequences (budget enforced no claim; all runtimes heredan vía P2; anti-scope respetado), Rejected (hand-editar generated / cargar constitution entera).
- `docs/GOVERNANCE.md` (NEW): índice de gobernanza — constitution (v7 + must slice), core.md, deltas, manifest, profiles, ADRs (0001, 0002), debt-findings, gates (p0-p6). Un mapa de "qué gobierna qué".
- `docs/harness-debt-findings.md` (EDIT): marcar constitution-must slice + stage-context-manifest + ICM routing como RESUELTOS (cross-out + fecha 2026-08-03 + ref PR #5).
- `docs/README.md` (EDIT): agregar link a `GOVERNANCE.md` + ADR-0002.

**Regen:** NONE.

**Verificación:** `find docs/decisions -name "0002*"`; leer GOVERNANCE.md; `grep -c "RESUELTO" docs/harness-debt-findings.md`.

**Acceptance:** ADR-0002 existe con rationale; GOVERNANCE.md linkea todos los docs de gobernanza; debt-findings marca resueltos.

**Rollback:** `git revert`.

---

### P2 — Elevar modelo ICM a core.md (shared) + budget bump

**Objetivo:** ICM workspace model (5 layers, one-stage-one-job, edit-source, stage-context-manifest) como contrato shared en `core.md` — los 3 runtimes lo heredan de first-class, no vía ref frágil a delta-claude.

**Riesgo:** CRÍTICO budget. core.md alimenta los 3 adapters. Headroom: claude 399, antigravity 188, codex 214. Añadir ~150t a core.md → antigravity 3962 (OK), codex 2536 (OK, 64 headroom), claude 2751 (OK). Si la sección supera 188t, antigravity overflow → requiere bump.

**Source edits:**
- `runtime/core.md`: nueva sección `## Workspace model (ICM)` — compacta (~150t):
  - 5-layer hierarchy (L0 CLAUDE.md identidad / L1 workspace CONTEXT.md routing / L2 stage CONTEXT.md contract / L3 references+config factory / L4 output working).
  - one-stage-one-job, plain-text interface, edit-source principle.
  - `scripts/stage-context-manifest.sh <stage>` = Inputs table ejecutable (compute L0-L4 stack, warn >8000t; paper arXiv 2603.16021v2 §3.2).
  - paper ref: arXiv 2603.16021v2 (ICM).
- `runtime/delta-claude.md`: la sección "First-prompt routing" queda como per-runtime routing specifics (sensor stop-validator); el modelo ICM shared ya vive en core. Compactar si solapa.
- `harness/manifest.json`: si antigravity overflow, bump `antigravity.sessionStartMax` 4000→4200 (documentar rationale en ADR-0002 addendum o commit msg: ICM modelo shared es permanente, justifica headroom). Verificar codex (si <50 headroom tras add, bump 2600→2700).

**Regen:** `python3 scripts/build-indexes.py`.

**Verificación (obligatoria tras regen):**
- `python3 scripts/check-token-budget.py` — los 3 OK. Si falla, NO DONE.
- `git diff CLAUDE.md AGENTS.md GEMINI.md` — el cambio reflejado en los 3 (modelo ICM aparece en los 3 adapters).
- `python3 scripts/validate-coverage.py` — 611 PASS.
- `python3 scripts/validate-evals.py` — 36/36 OK.
- `bash scripts/check-prerequisites.sh --phase p6` — READY.

**Acceptance:** `grep -c "Workspace model (ICM)" CLAUDE.md AGENTS.md GEMINI.md` == 3 (los 3 heredan); budgets PASS; gates READY.

**Rollback:** `git revert` (regen reversible: checkout fuente + regen).

---

### P3 — Optimizar routing/orquestación

**Objetivo:** routing + orquestación más robustos y ejecutables.

**Source edits (scripts, NO generated):**
- `scripts/stage-context-manifest.sh`: agregar `--enforce` mode — exit 1 si over-budget o si referenced file missing (gate, no solo sensor). Default sigue sensor (exit 0). Permite usar como gate hard en 04_validate.
- `scripts/first-prompt-router.sh`: refinements — detectar T-NNN con `task.md` faltante (no solo checkboxes); emitir `ROUTE-STAGE` (stage path sugerido desde intent) además de ROUTE-MODE.
- `scripts/session-init.sh`: tras ROUTE-* lines, si `last_stage` detectado, emitir `ROUTE-HINT: run scripts/stage-context-manifest.sh <last_stage> before loading context`.
- `workspace/_template/04_validate/CONTEXT.md`: step 0 ya corre manifest; cambiar a `--enforce` (gate hard en validate).

**Regen:** NONE (scripts no son generated; template es source, no generated).

**Verificación:**
- `bash scripts/stage-context-manifest.sh --selftest` — 4/4 <8000t.
- `bash scripts/stage-context-manifest.sh workspace/_template/01_discovery --enforce; echo $?` — 0 (under budget).
- `bash scripts/first-prompt-router.sh --selftest` — exit 0.
- Gates p0-p6 READY.

**Acceptance:** `--enforce` mode funciona (exit 1 on over-budget); router emite ROUTE-STAGE; session-init emite manifest hint.

**Rollback:** `git revert`.

---

### P4 — Sensor de consistencia de gobernanza + gate p7

**Objetivo:** detectar stale refs y inconsistencias docs-vs-source automáticamente.

**Source edits:**
- `scripts/check-governance-consistency.sh` (NEW): checks —
  - README.md no referencia "Constitution v6" (debe ser v7).
  - README token table coincide con `evals/token-benchmark.json` (parsear ambos, comparar).
  - `runtime/core.md` constitution ref == `references/ontology/` version.
  - README Layout dirs existen en filesystem.
  - ADRs en `docs/decisions/` nombrados secuencialmente (0001, 0002, ...).
  - Exit 1 si cualquier check falla (gate); exit 0 si OK. `--json` mode.
- `scripts/check-prerequisites.sh`: agregar `p7)` REQUIRED=(scripts/check-governance-consistency.sh); actualizar usage `p0..p7`.

**Regen:** NONE.

**Verificación:**
- `bash scripts/check-governance-consistency.sh` — exit 0 tras P0-P2 aplicados (consistencia lograda).
- `bash scripts/check-prerequisites.sh --phase p7` — READY.
- Gates p0-p7 READY.

**Acceptance:** sensor corre limpio; gate p7 READY; stale v6 detectable (test inyectando "v6" temporal → exit 1).

**Rollback:** `git revert`.

---

### P5 — Alinear agents/ + commands/ a ICM

**Objetivo:** definiciones de agentes y commands reflejan ICM routing + manifest.

**Source edits (hand, review-then-edit):**
- `agents/README.md` + 21 agent files: revisar si mencionan routing/workspace; si callan, agregar nota "sigue ICM routing (first-prompt-router → stage → stage-context-manifest)". Editar solo los que orquestan (harness-maintainer, dev-coordinator, governance-guardian, context-optimizer, input-analyst, investigator). Los especializados (brand, estimation) quizá no tocan.
- `commands/` (5): revisar `session.md`, `pristino.md` — si definen flow, alinear con first-prompt routing. `brand.md`, `iikit.md`, `jarvis.md` — probablemente no tocan (dominio específico).
- Criterio: editar SOLO si hay inconsistencia o silencio sobre routing. No inflar.

**Regen:** NONE (agents/commands no son generated por build-indexes — verificar con `grep build-indexes.py` que no los lista).

**Verificación:**
- `grep -rl "first-prompt-router\|stage-context-manifest" agents/ commands/` — los orquestadores lo mencionan.
- Gates p0-p7 READY.

**Acceptance:** agentes orquestadores referencian ICM routing; commands de flow alineados; sin inflar los especializados.

**Rollback:** `git revert`.

---

### P6 — Verificación final + commit + PR

**Objetivo:** cierre. Verificación completa + PR único (o por fase si se prefiere).

**Pasos:**
- Correr §6 harness completo (p0-p7, budgets, coverage, evals, manifest selftest, consistency sensor).
- `git status` limpio (solo fuente tocada, generated solo via regen en P2).
- Si fases encadenadas en una rama: un PR con todos los commits. Si分支 por fase: PRs separados o squash.
- `gh pr create` — body termina `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
- Actualizar §0 tabla con commit hash final.

**Acceptance:** PR mergeable; todos gates verdes; §0 tabla toda DONE.

**Rollback:** N/A (cierre).

---

## §5 — Orden de dependencias

```
P0 (README) ──┐
              ├─→ P4 (consistency sensor) → P6
P1 (docs) ────┤
              │
P2 (core.md ICM) ─→ P3 (routing opt) ─→ P4 ─→ P6
              │
P5 (agents/commands) ──────────────────→ P6
```

- P0 y P1 independientes (paralelizables conceptualmente, pero ejecutar secuenciales para commits limpios).
- P2 antes de P3 (P3 usa manifest que P2 eleva).
- P4 después de P0+P2 (sensor valida lo que esos arreglaron).
- P5 independiente (puede ir en cualquier punto post-P2).
- P6 último.

---

## §6 — Harness de verificación (correr tras cada fase)

```bash
cd /Users/deonto/Agentic_Space/jm-adk-beta
# Gates (agregar p7 tras P4)
for p in p0 p1 p2 p3 p4 p5 p6 p7; do bash scripts/check-prerequisites.sh --phase $p 2>&1 | tail -1; done
# Budgets (blocker si falla)
python3 scripts/check-token-budget.py
# Coverage
python3 scripts/validate-coverage.py
# Evals
python3 scripts/validate-evals.py
# ICM stage manifest (tras P2/P3)
bash scripts/stage-context-manifest.sh --selftest
# Governance consistency (tras P4)
bash scripts/check-governance-consistency.sh
# Generated files clean (no hand-edits fuera regen)
git diff --name-only CLAUDE.md AGENTS.md GEMINI.md SKILLS.md
```

**Hard gates (blocker):** budgets, coverage, evals, check-prerequisites. **Soft gates (warn):** consistency (hasta P4 que lo vuelve hard).

---

## §7 — Protocolo de reanudación (anti-perderse)

1. `cd /Users/deonto/Agentic_Space/jm-adk-beta && git status` — confirmar rama/estado.
2. Leer §0 tabla de estado → identificar próxima fase con status `PENDING` (o `IN_PROGRESS`).
3. Leer §4 → la subsección de esa fase (objetivo, edits, regen, verificación, acceptance, rollback).
4. `git checkout -b feat/evolucion-p<N>` (o continuar rama existente si encadenada).
5. Marcar fase `IN_PROGRESS` en §0 (editar `plan-evolucion.md`).
6. Ejecutar edits de fuente. Respetar §1 reglas duras (NUNCA hand-edit generated).
7. Si la fase toca fuente generated (P2): regen (`build-indexes.py`).
8. Correr §6 harness de verificación. Si algo falla: fix fuente → re-verificar. No marcar DONE con gate rojo.
9. Commit: mensaje termina `Co-Authored-By: Claude <noreply@anthropic.com>`.
10. Actualizar §0: status `DONE` + commit hash. Push.
11. Volver a paso 2 (próxima fase PENDING) hasta P6.

**Señal de pérdida:** si no sabes qué fase sigue → §0 tabla. Si no sabes qué editar → §4 subsección + §1. Si budgets fallan → §2 riesgo 1 (compactar fuente antes que inflar; bump documentado si necesario).

---

## §8 — Meta

- **Confianza plan:** 0.85 [CONFIANZA]. Gaps auditados con evidence tags; fases atómicas; budget risk P2 identificado con mitigación. <0.5 sería escalar; 0.85 → proceder, flag incertidumbre en P2 (budget compactar vs bump).
- **Bias scan:** anchoring en estado actual (no buscar gaps fuera de lo leído — mitigado: auditoría cubrió README+core+deltas+docs+agents+commands); confirmation (no asumir que P2 cabe sin medir — mitigado: §2 riesgo 1 exige medir). Availability (sobre-indexar PR #5 — mitigado: fases cubren gobernanza pre-PR#5 también).
- **Creado:** 2026-08-03. **Fuente plan:** este archivo. **No borrar** — es el tracker durable de la evolución.