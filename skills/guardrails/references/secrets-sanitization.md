<!-- distilled from alfa skills/secrets-sanitization -->
<!-- > -->
# Secrets Sanitization (Gate G0)

**TL;DR**: Scans project artifacts for exposed credentials, API keys, passwords, tokens, and sensitive data. Implements Gate G0: no pipeline execution proceeds with unmasked secrets. Detects patterns across configuration files, documents, and code artifacts, then masks or flags findings for remediation.

**Tagging.** This file uses the Alfa core set (`[DOC]` `[CÓDIGO]` `[CONFIG]` `[INFERENCIA]` `[SUPUESTO]`) plus the legacy operational tags already in use here (`[EXPLICIT]` = contractually mandated behavior; `[PLAN]` = procedural step; `[METRIC]` = measurable gate). Do not introduce other taxonomies. Canon: `references/verification-tags.md`. [DOC]

## Deterministic Safety Contract

- `assets/secrets-report-contract.json` defines the G0 report shape.
- `assets/token-pattern-policy.json` defines token-like patterns that must be masked.
- `assets/g0-block-policy.json` defines hard-stop behavior for unmasked secrets.
- `scripts/validate_secrets_sanitization_report.py` validates reports offline.
- `scripts/check.sh` runs positive and negative fixtures.

Fail closed when a report claims pass while a critical finding is unresolved, a token-like value is unmasked, or evidence is missing. [EXPLICIT]

**Fail-closed precedence** (apply top-down; first match wins): [EXPLICIT]
1. Evidence missing or report shape invalid against `secrets-report-contract.json` → BLOCK (cannot prove safety).
2. Any unmasked value matching `token-pattern-policy.json` → BLOCK regardless of stated severity.
3. Any unresolved Critical finding → BLOCK.
4. Report `gate: PASS` with zero Critical and all token-like values masked → ALLOW.

A report that asserts PASS but trips rules 1–3 is itself a G0 failure — never trust the self-declared verdict over the evidence. [INFERENCIA]

## Principio Rector
Un solo secreto expuesto puede comprometer todo el proyecto. Gate G0 es un hard stop: si se detectan credenciales sin enmascarar en cualquier artefacto del proyecto, el pipeline se detiene hasta que se remedien. La seguridad no es una fase — es una precondición. [EXPLICIT]

## Anti-Scope (what G0 is NOT)
- **Not secret management.** Detects exposure only; rotation, vaulting, and issuance belong to a dedicated vault (Vault, AWS/GCP/Azure Secret Manager). [EXPLICIT]
- **Not a git-history scanner.** Inspects the working tree only; history needs `git log -p`, `trufflehog`, or BFG. [SUPUESTO]
- **Not a decryptor.** Cannot see inside encrypted blobs; only flags encoding patterns. [INFERENCIA]
- **Not a binary scanner.** Text artifacts only; binaries need separate tooling. [EXPLICIT]
- **Not a compliance attestation.** A G0 PASS means "no unmasked secrets found by these patterns," not "the project is secure." Absence of evidence ≠ evidence of absence. [INFERENCIA]

## Assumptions & Limits
- Workspace path is provided and readable; an unreadable path is `[VACIO_CRITICO]` → stop, do not emit PASS. [PLAN]
- Pattern library covers common formats (AWS, Azure, GCP, JWT, GitHub, Slack, private keys). Novel/custom token shapes may evade it. [PLAN]
- False-positive rate is managed through context rules + allowlist; residual FP/FN is accepted and logged. [SUPUESTO]
- Encoded/obfuscated/encrypted secrets evade pattern matching by construction — a clean scan does not clear them. [INFERENCIA]
- Detection is best-effort, not exhaustive: tune for recall on Critical patterns (missing a live key is worse than a false alarm). [INFERENCIA]

## Usage

```bash
# Full secrets scan of project workspace
/pm:secrets-sanitization $ARGUMENTS="--path /project/workspace"

# Scan specific file types only
/pm:secrets-sanitization --type targeted --glob "**/*.{md,yaml,json,env}"

# Remediation verification after masking
/pm:secrets-sanitization --type verify --baseline scan-report-v1.md
```

**Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `$ARGUMENTS` | Yes | Path to project workspace |
| `--type` | No | `full` (default), `targeted`, `verify` |
| `--glob` | No | File pattern to scan |
| `--baseline` | No | Previous scan report for verification |
| `--severity` | No | Minimum severity to report: `critical`, `high`, `medium` |

**Mode trade-offs:** `full` maximizes recall, costs the most scan time — use at phase/release gates. `targeted` is fast but narrows coverage; only safe when the changed-file set is known (e.g. a PR diff), since secrets hide outside the obvious globs. `verify` re-scans against a `--baseline` to confirm remediation closed prior findings and introduced no new ones; it must FAIL if any baseline Critical persists. [INFERENCIA]

## Service Type Routing
`{TIPO_PROYECTO}` variants:
- **Agile**: G0 scan integrated into sprint CI pipeline; secrets detected pre-commit and in PR reviews
- **Waterfall**: G0 scan at each phase gate; formal remediation sign-off before proceeding to next phase
- **SAFe**: G0 enforced at ART level; system demo artifacts scanned; cross-team credential sharing patterns audited
- **Kanban**: G0 as entry policy on the board; no work item moves to "In Progress" with unmasked secrets
- **PMO**: G0 governance policy across all portfolio projects; centralized secrets management audit schedule
- **Hybrid**: G0 applied uniformly regardless of methodology component; both iterative and phase-gate artifacts scanned

## Protocol (consolidated)
Inputs: workspace path, configuration/environment files, documentation and deliverables, integration specifications.

1. **Enumerate** — Glob `**/*.{env,yaml,yml,json,conf,cfg,properties}` (config) and `**/*.{md,txt,doc}` (docs); never scan `.env`-only. Honor `.gitignore`-style excludes for `node_modules`, build dirs, and vendored deps to cut noise. [PLAN]
2. **Load patterns** — Read `token-pattern-policy.json` (API keys, passwords, tokens, certificates, private keys). [PLAN]
3. **Pre-grep indicators** — Grep prefixes `AKIA`, `sk-`, `ghp_`, `xoxb-`, `Bearer `, `-----BEGIN` as cheap first-pass signals before full matching. [PLAN]
4. **Context analysis** — Distinguish real secrets from false positives using surrounding context (placeholders, `EXAMPLE`, `${VAR}` interpolation, docs allowlist). [PLAN]
5. **Severity classification** — Critical = live/production credentials; High = test/staging credentials or real-shaped values in non-prod; Medium = pattern-only matches with no confirmed live value. [METRIC]
6. **Mask** — Apply the masking convention (below) in any artifact that will persist. [PLAN]
7. **Remediate** — Emit specific, per-finding-type remediation with an assigned owner. [PLAN]
8. **Gate decision** — Apply the fail-closed precedence; state PASS/FAIL explicitly. [METRIC]
9. **Report** — Compile the scan report per `secrets-report-contract.json`, describing findings **without** reproducing any secret value. [EXPLICIT]

## Masking Convention
- Preserve a non-sensitive prefix for identification, redact the rest: `AKIA****************` , `ghp_****…****` , `sk-…last4`. Reveal at most the first 4 and never the last secret-bearing characters of a live credential. [INFERENCIA]
- Replace the body with a fixed-width sentinel (`****`); never echo true length if length itself is sensitive (e.g. private-key PEM bodies → collapse to `-----BEGIN … REDACTED … END-----`). [INFERENCIA]
- Reference findings by `path:line` + masked token, never by raw value — the report and logs must stay safe to share. [EXPLICIT]

## Severity Decision Table
| Signal | Severity | Why |
|--------|----------|-----|
| Matches live-credential format AND not a known placeholder AND in prod path | Critical | Active compromise risk [INFERENCIA] |
| Real-shaped value in test/staging artifact, or commented-out | High | Exploitable if promoted; lateral-movement risk [INFERENCIA] |
| Pattern match only (e.g. base64 of right length), no confirmed live value | Medium | Possible secret; needs human triage [SUPUESTO] |
| Matches allowlisted example/doc placeholder | None (filtered) | Documented false positive [INFERENCIA] |

When context is ambiguous, escalate one level (favor over-reporting) and tag the call `[SUPUESTO]`. [EXPLICIT]

## Edge Cases & Failure Modes
1. **Active production credentials found** — CRITICAL. Notify the security team immediately; recommend rotation within 24h. Never place the actual credential in the report. [PLAN] [EXPLICIT]
2. **High false-positive rate** — Refine context rules; add a project-scoped allowlist for known-safe patterns (example keys in docs). Allowlist entries are auditable and time-stamped, never silent. [INFERENCIA] [EXPLICIT]
3. **Secrets in git history** — Working-tree scan misses these. Recommend `git log -p` / `trufflehog` / BFG; flag as out-of-scope, not as PASS. [SUPUESTO] [EXPLICIT]
4. **Encrypted or base64-encoded secrets** — Flag base64 strings matching key-length patterns as Medium; document that truly encrypted content is undetectable. [INFERENCIA] [EXPLICIT]
5. **Secret split across lines / templated** — Concatenated or `${VAR}`-interpolated secrets may evade single-line regex. Treat interpolation markers as "deferred to runtime"; flag only literal values. [INFERENCIA]
6. **Report itself leaks** — A naive finding that quotes the matched line re-exposes the secret. The report MUST carry masked tokens only; an unmasked value in the report is itself a Critical finding. [EXPLICIT]
7. **Allowlist abuse** — A too-broad allowlist silently downgrades real secrets. Allowlist patterns must be specific (full placeholder string), never prefix-only. [INFERENCIA]

## Example: Good vs Bad

**Good — thorough G0 scan:**

| Attribute | Value |
|-----------|-------|
| Files scanned | 342 files across 12 file types |
| Findings | 3 findings: 1 Critical, 1 High, 1 Medium |
| False positive rate | 2 false positives identified and filtered |
| Remediation | Specific steps per finding with owner assigned |
| Gate decision | FAIL — Critical finding requires remediation before proceed |
| Report | Findings described without exposing actual secrets |

**Worked finding (masked):**
```
[CRITICAL] config/prod.env:14  AWS access key  AKIA****************
  → owner: platform-team  action: rotate in IAM within 24h, purge from file, move to vault
[MEDIUM]  docs/integration.md:88  base64 blob, 40 chars  bGl2ZS1***…  → human triage
gate: FAIL  reason: 1 unresolved Critical (rule 3)
```

**Bad — superficial scan:**
Scan of only `.env` files, ignoring documentation, YAML, and JSON. No severity classification, no context analysis. A narrow scan gives false confidence — secrets hide in unexpected places (README examples, CI configs, integration docs). [EXPLICIT]

## Deliverables
- G0 security scan report (pass/fail), conformant to `secrets-report-contract.json`.
- Findings register: severity + `path:line` + masked token.
- Remediation action items with owners.
- Updated artifacts with masked secrets.

## Validation Gate (acceptance criteria)
- [ ] All in-scope file types scanned, not just `.env` [PLAN]
- [ ] Every finding classified Critical/High/Medium [METRIC]
- [ ] Zero unresolved Critical findings for G0 PASS (hard requirement) [METRIC]
- [ ] Zero unmasked token-like values anywhere, **including the report itself** [METRIC]
- [ ] Report conforms to `secrets-report-contract.json` and exposes no raw secret [EXPLICIT]
- [ ] Remediation steps specific per finding type, each with an owner [PLAN]
- [ ] False positives documented in an auditable, specific allowlist [INFERENCIA]
- [ ] Gate decision stated explicitly (PASS/FAIL) with the triggering rule cited [PLAN]
- [ ] Findings include `path:line` (masked value) [METRIC]
- [ ] Out-of-scope vectors (git history, binaries, encrypted blobs) listed, not silently passed [INFERENCIA]
- [ ] Evidence ratio ≥90% [PLAN]/[METRIC], <10% [SUPUESTO] [PLAN]
- [ ] Scan execution logged for audit trail (path, pattern-policy version, timestamp) [PLAN]
- [ ] `scripts/check.sh` green on positive AND negative fixtures [METRIC]

## Escalation Triggers
- Active production credentials found in artifacts
- G0 failure blocking pipeline execution
- Secret exposure in shared/public documents
- Recurring secret exposure after remediation (same secret resurfaces → process failure, not a one-off)

## Additional Resources

| Resource | When to Read | Location |
|----------|-------------|----------|
| Body of Knowledge | Secret detection patterns and tools | `references/body-of-knowledge.md` |
| State of the Art | Modern secrets management practices | `references/state-of-the-art.md` |
| Knowledge Graph | G0 gate in pipeline security | `references/knowledge-graph.mmd` |
| Use Case Prompts | Secret scanning scenarios | `prompts/use-case-prompts.md` |
| Metaprompts | Custom detection pattern design | `prompts/metaprompts.md` |
| Sample Output | Reference G0 scan report | `examples/sample-output.md` |
| Verification Tags | Tag canon and homologation | `references/verification-tags.md` |

## Output Configuration
- **Language**: Spanish (Latin American, business register)
- **Evidence**: [DOC], [CÓDIGO], [CONFIG], [INFERENCIA], [SUPUESTO], plus legacy [EXPLICIT], [PLAN], [METRIC] (canon: `references/verification-tags.md`)
- **Branding**: #2563EB royal blue, #F59E0B amber (NEVER green), #0F172A dark
