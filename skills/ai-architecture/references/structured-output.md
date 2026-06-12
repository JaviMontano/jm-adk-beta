<!-- distilled from alfa skills/structured-output -->
<!-- > -->
# Structured Output
> "Method over hacks."
## TL;DR
Make an LLM emit machine-parseable, schema-valid data (JSON/enum/typed fields) reliably enough to feed code without a human in the loop. Constrain at generation, validate after, recover on failure — never trust raw model text as structured data. [EXPLICIT]

## Decision Order (do not skip)
1. **Contract first** — define the target schema (JSON Schema / Pydantic / TS type) before prompting. The schema is the spec; the prompt serves it. [EXPLICIT]
2. **Enforcement tier** — pick the strongest the provider supports: native constrained/tool-call schema > JSON mode (valid JSON, unconstrained shape) > prompt-only "return JSON". Stronger tiers eliminate whole failure classes; do not hand-roll what the API guarantees. [INFERENCE]
3. **Shape** — flat over deeply nested; enums over free strings; explicit nullable over omitted keys. Reserve a top-level error/refusal field so the model has a legal way to say "can't". [EXPLICIT]
4. **Validation** — parse + schema-validate every response in code. A response that doesn't validate is a failure, not a result, regardless of how plausible it looks. [EXPLICIT]
5. **Recovery** — on invalid output: one bounded repair retry feeding the validator error back, then escalate. Never silently coerce or regex-patch malformed JSON into shape. [INFERENCE]

## Decisions & Trade-offs
| Decision | Choose when | Cost of getting it wrong |
|----------|-------------|--------------------------|
| Native constrained / tool schema | Provider supports it (default) | Vendor lock to one schema dialect; some latency overhead |
| JSON mode only | Constrained gen unavailable | Valid JSON but wrong shape — validation must catch it |
| Prompt-only JSON | Last resort, simple shape | Markdown fences, prose preamble, truncation; high parse-fail rate |
| Strict schema (additionalProperties:false) | Downstream code is brittle | Legitimate-but-extra fields rejected; more repair loops |
| Lenient + post-validate | Schema evolves, recall matters | Bad data passes silently if validator is weak |

## Worked Example
Extract `{vendor: str, amount: float, currency: enum[USD,EUR,COP], confidence: 0-1, error: str|null}` from invoices. Use native tool-call schema, `additionalProperties:false`, `currency` as enum. Validate with Pydantic; on `ValidationError`, retry once passing the error text and the offending output back; on second failure set `error` and route to human queue. Log raw output + validator verdict for every call. [INFERENCE]

## Evaluation (gate before ship)
- Run a labeled fixture set (≥30 inputs incl. adversarial/empty/ambiguous); measure schema-valid rate and field-level accuracy, not just "parses". [EXPLICIT]
- Acceptance floor: ≥99% parse-valid after one repair retry; field accuracy meets the task's documented threshold. Re-run on any prompt, schema, or model change. [EXPLICIT]

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and the target schema is known or derivable. [EXPLICIT]
- English-language output unless otherwise specified. [EXPLICIT]
- Schema validity is not semantic correctness — a well-formed JSON can still be wrong; field-accuracy eval, not parse-rate, is the real gate. [INFERENCE]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]

## Anti-Scope
- Not prompt wording/few-shot design → prompt-engineering.md. Not multi-step orchestration → ai-pipeline-architecture.md / rag-patterns.md. Not model selection/fine-tune → fine-tuning-prep.md. [EXPLICIT]

## Procedure
1. **Discover** — gather context, inputs, and the consuming contract. [EXPLICIT]
2. **Analyze** — choose enforcement tier + schema shape per Constitution XIII/XIV. [EXPLICIT]
3. **Execute** — implement constrained generation + validator with evidence tags. [EXPLICIT]
4. **Validate** — run the eval gate; verify quality criteria met. [EXPLICIT]

## Failure Modes & Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to the skill named in Anti-Scope |
| Markdown-fenced / prose-wrapped JSON | Strip to JSON span, validate; if still invalid, repair-retry once |
| Truncated output (hit token cap) | Raise max tokens or split the request; never parse partial JSON |
| Valid JSON, wrong shape | Validation fails by design — repair-retry with the schema error |
| Model refuses / can't comply | Use the reserved error field; do not fabricate a result to fit schema |
| Repair retry also fails | Stop, return error + raw output, escalate to human |
| Provider lacks constrained gen | Degrade to JSON mode + stricter post-validation; tighten eval floor |

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant (XIII/XIV)
- [ ] Schema defined before prompting; strongest available enforcement tier used
- [ ] Every response code-validated; invalid != accepted
- [ ] Bounded repair-retry then escalate; no silent coercion
- [ ] Eval parse-valid rate meets the documented floor
- [ ] Actionable output

## Usage

Example invocations:

- "/structured-output" — Run the full structured output workflow
- "structured output on this project" — Apply to current context
