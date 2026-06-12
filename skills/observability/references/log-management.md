<!-- distilled from alfa skills/log-management -->
<!-- > -->
# Log Management
> "Method over hacks."
## TL;DR
Structured logging, levels, retention, and search patterns so a single request
is traceable end-to-end and incidents are diagnosable from logs alone. [EXPLICIT]

## Scope
- In: log schema, level discipline, retention/PII, query patterns, sampling.
- Anti-scope: metrics and tracing live in `monitoring-setup.md`; paging and
  on-call live in `alerting-strategy.md`. Logs feed both but don't replace them. [EXPLICIT]

## Procedure
### Step 1: Discover
- Inventory log sources, current formats, volume/day, retention, and consumers
  (humans, SIEM, dashboards). Identify the request/correlation ID, if any. [EXPLICIT]
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV. Decide structured vs free-text,
  level thresholds, retention tiers, and PII handling against cost/compliance. [EXPLICIT]
### Step 3: Execute
- Emit structured JSON with evidence tags on derived claims; thread a
  `correlation_id` through every hop; redact PII at the emit boundary. [EXPLICIT]
### Step 4: Validate
- Verify quality criteria met: one request traceable across services, levels
  used correctly, no secrets/PII in the stream. [EXPLICIT]

## Structured log schema (minimum)
`timestamp` (ISO-8601 UTC), `level`, `service`, `correlation_id`, `message`,
`context{}`. Never log secrets, tokens, full PANs, or passwords. [EXPLICIT]

## Level discipline
| Level | Use for | Pages? |
|---|---|---|
| ERROR | Failed operation needing intervention | Maybe |
| WARN | Degraded / retried / approaching limit | No |
| INFO | Business-significant state change | No |
| DEBUG | Diagnostic detail, off in prod by default | No |
Reserve ERROR for actionable failures; routine 4xx is INFO/WARN — ERROR noise erodes paging trust. [INFERENCIA]

## Retention & sampling
- Tiers: hot 7–14d (searchable), warm 30–90d (archived), cold per compliance. Confirm exact windows with legal/security. [SUPUESTO]
- Sample high-volume DEBUG/INFO; never sample ERROR/WARN. Keep a 1.0 sample of any error request so the full trace survives. [INFERENCIA]

## Search patterns
- Pivot on `correlation_id` to reconstruct one request across services.
- Filter `level>=WARN` for triage; facet by `service` to localize blast radius.
- Alert on log-derived rates (ERROR/min) via `alerting-strategy.md`, not lines. [EXPLICIT]

## Worked example
Checkout 500s spike: grab one failing request's `correlation_id` from the edge,
search all services, find `payment-svc` WARN "retry exhausted" 200ms before the
ERROR. Root cause sits in the WARN. [INFERENCIA]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] One request traceable end-to-end via `correlation_id`
- [ ] No secrets/PII in the log stream
- [ ] Levels and retention tiers explicitly chosen, not defaulted silently

## Usage
Example invocations:
- "/log-management" — Run the full log management workflow
- "log management on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs). [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]
- Retention windows are placeholders until legal/compliance confirms. [SUPUESTO]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| No correlation ID exists | Introduce one before scaling logging effort |
| PII detected in existing logs | Stop, redact at source, flag for review |
| Log volume exceeds budget | Sample low-value levels; never sample errors |
