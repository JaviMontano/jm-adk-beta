# Body of Knowledge — ai-quality

Domain knowledge for the `ai-quality` router: how to assess, test, review,
evaluate, and harden code and AI output. The router's job is correct
**single-topic resolution** and disciplined delegation; this BOK captures the
concepts, standards, and decision rules that make that resolution defensible. [DOC]

## 1. The nine topics and their boundaries

| Topic | Verb it answers | Hard boundary (what it is NOT) |
|-------|-----------------|--------------------------------|
| `ai-testing-strategy` | *Plan* how to verify an AI system | Not test code; not pipeline architecture. |
| `ai-assisted-testing` | AI *generates* tests/fuzz/mutation | Not running tests in prod; not human review. |
| `ai-code-review` | AI *reviews* a diff | Not auto-fixing/merging; not human-only review. |
| `code-review` | Human/tool *reviews* a diff | Not security pentest depth; not release-gate enforcement. |
| `llm-evaluation` | *Score* model output quality | Not fine-tuning; not latency/cost benchmarking; not red-teaming. |
| `ai-safety` | *Harden* against harm | Not a live-model attestation; not pentest. |
| `ai-content-detection` | *Estimate* AI-generation likelihood | Not authorship attribution; not plagiarism detection. |
| `ai-documentation` | *Generate* source-backed docs | Not marketing copy; not undocumented behavior. |
| `ai-workflow-automation` | *Plan* an LLM-in-the-loop workflow | Not executing/scheduling; not picking a model provider. |

## 2. Routing decision rules (the disambiguation core)

The most common collisions and their tie-breakers: [INFERENCIA]
- **Scores vs writes vs reviews:** AI *judges/scores* output → `llm-evaluation`;
  AI *authors/runs* tests → `ai-assisted-testing`; AI *reviews* a diff →
  `ai-code-review`.
- **AI vs human review:** the reviewer being an AI model → `ai-code-review`; a
  human or a deterministic linter/tool → `code-review`.
- **Strategy vs execution:** "what should we test and how do we gate it" →
  `ai-testing-strategy`; "write me these tests" → `ai-assisted-testing`.
- **Detection vs evaluation:** "is this AI-written?" → `ai-content-detection`;
  "is this output good/grounded?" → `llm-evaluation`.
- A genuine tie is the only case where the router asks one clarifying question;
  otherwise it resolves silently. [CÓDIGO]

## 3. Cross-cutting standards (true for every topic)

1. **Spine:** Discover → Analyze → Execute → Validate. No topic ships without a
   Validate phase. [DOC]
2. **Evidence-first, Alfa core set:** `[CÓDIGO]` (inspected code/diff/test/CI),
   `[CONFIG]` (policy/standard/acceptance criteria), `[DOC]` (supplied
   doc/spec), `[INFERENCIA]` (reasoned risk from cited evidence), `[SUPUESTO]`
   (an assumption to surface, never a blocker). One family per deliverable. [DOC]
3. **Offline determinism:** validation forbids live network, wall-clock, and RNG
   so a check is reproducible in CI. Stub to fixed inputs. [CONFIG]
4. **Baseline/reference discipline:** a score, label, or finding with no
   baseline, reference, or evidence id is *not a result*. [DOC]
5. **Green ≠ safe.** A passing validator certifies *well-formedness*, never live
   correctness or safety. Never report green as a guarantee. [INFERENCIA]
6. **Read before write/judge; read-only on review targets.** [CONFIG]

## 4. Per-topic key concepts (quick reference)

- **Testing strategy:** 6 test types × 6 layers = 36-cell matrix; data-quality
  testing is the highest-leverage layer; fairness metrics are mutually exclusive
  (demographic parity vs equal opportunity) so you pick by domain harm. [EXPLICIT]
- **Assisted testing:** oracle ladder (assertion → metamorphic → property →
  snapshot-as-last-resort); mutation testing guards against tautological tests;
  coverage floors are per-module, not a global average. [EXPLICIT]
- **Code review (AI & human):** fixed severities (BLOCKER/MAJOR/MINOR/NIT or
  blocker/major/…); decision equals the worst severity present; no pass/fail
  claim without an executed command; one finding per root cause. [EXPLICIT]
- **LLM evaluation:** reference-based vs reference-free chosen by failure cost;
  groundedness = supported-claims / total-claims; pin and disclose the judge;
  human-spot-check ≥20 items or all failures. [EXPLICIT]
- **AI safety:** risk → control → jailbreak test → metric chain with no orphan
  ids; critical risks can't rely on `allow` alone; over-refusal is a guardrail
  metric, not a sign of success. [EXPLICIT]
- **Content detection:** direction-aware 0..1 signal scores; bias toward
  `inconclusive`; `authorship_claim` fixed at `not-determined`; non-native and
  templated prose are false-positive vectors. [EXPLICIT]
- **AI documentation:** evidence id per section; closed doc/source taxonomies;
  gap-over-guess; safe relative output paths. [EXPLICIT]
- **Workflow automation:** gate-before-effect; bounded retries + fallback;
  input/output contracts on every AI step; no circular handoffs. [EXPLICIT]

## 5. Anti-patterns (router-level)

- Loading more than one playbook ("just in case"). [SUPUESTO]
- Answering from the router without reading any playbook. [SUPUESTO]
- Guessing an ambiguous topic instead of disambiguating. [INFERENCIA]
- Mixing tag families, or untagged prose. [DOC]
- Reporting a passing offline check as a safety/correctness guarantee. [INFERENCIA]
