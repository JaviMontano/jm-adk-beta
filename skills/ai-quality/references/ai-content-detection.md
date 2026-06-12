<!-- distilled from alfa skills/ai-content-detection -->
<!-- > -->
# AI Content Detection
> Evidence-weighted probabilities, never unsupported accusations.

## TL;DR
Use this skill when the user asks to evaluate whether content may be AI-generated,
to inspect watermark/provenance signals, or to design human-AI hybrid content
review policies. Outputs must describe likelihood, evidence, limitations, and
decision policy without asserting authorship as fact.

## Deterministic Assets
- `assets/detection-report-contract.json` defines the machine-checkable report packet.
- `assets/signal-taxonomy-policy.json` defines allowed signal types and required signal fields.
- `assets/threshold-policy.json` defines classification thresholds and confidence rules.
- `assets/evidence-policy.json` defines evidence requirements and no-unsupported-claim rules.
- `assets/watermark-policy.json` defines watermark/provenance status handling.
- `assets/decision-policy.json` defines allowed actions and non-accusatory language.
- `scripts/validate_ai_content_detection_report.py` validates reports offline.

## Procedure
### Step 1: Activate Intentionally
- Activate for AI-generated content detection, watermark checks, provenance review, or human-AI hybrid content policy.
- Do not activate for general writing, editing, plagiarism detection, SEO, or weather-style unrelated requests.
- Plagiarism/originality vs source corpora is out of scope; this skill assesses *machine-generation likelihood*, not copying. [EXPLICIT]

### Step 2: Establish Scope
- Record content id, content type, reviewed excerpt/source, and review purpose.
- Note whether the user needs policy advice, artifact inspection, or a validated report packet.
- Capture sample size (token/char count) and decision stakes; both drive confidence and the human-review gate (Step 5). [EXPLICIT]

### Step 3: Collect Signals
- Use only available offline signals unless the user explicitly authorizes external detectors.
- Allowed signals include stylometry, metadata, watermark/provenance, model-detector output, citation/source integrity, edit history, and disclosure statements.
- Every signal requires evidence and a score from 0 to 1.
- Score = generation likelihood the signal supports (1 = strongly AI, 0 = strongly human); record direction so opposing signals cannot silently cancel. [EXPLICIT]
- Reject any signal lacking a captured evidence id; an unverifiable signal is omitted, not scored from assumption. [EXPLICIT]

### Step 4: Classify Probabilistically
- Apply `assets/threshold-policy.json`.
- Emit `likely-ai`, `mixed`, `likely-human`, or `inconclusive`.
- Keep `authorship_claim` as `not-determined`; the skill reports likelihood, not identity or intent.

### Step 5: Control False Positives
- Prefer `inconclusive` when evidence is weak or contradictory.
- Require human review for any enforcement, moderation, academic, hiring, or compliance action.
- Include limitations and false-positive notes.
- Non-native-speaker prose and heavily templated/boilerplate text inflate AI scores; flag as a known false-positive vector and down-weight stylometry accordingly. [EXPLICIT]

### Step 6: Validate
- JSON packets must follow `assets/detection-report-contract.json`.
- Run `bash skills/ai-content-detection/scripts/check.sh` before marking local DoD evidence.

## Decisions & Trade-offs
- **Probabilities, not verdicts** — labels are likelihood bands, not authorship facts. Trade-off: less decisive for the user, but bounds legal/reputational exposure from a wrong accusation. [EXPLICIT]
- **Offline-first signals** — external detectors are opt-in only. Trade-off: lower recall, but no unverifiable third-party claim enters the packet and no content leaks to external APIs. [EXPLICIT]
- **Bias toward `inconclusive`** — ambiguity resolves to inconclusive, not to a guess. Trade-off: more "we can't tell" outcomes, but false positives are the costly error in enforcement contexts. [EXPLICIT]
- **`authorship_claim: not-determined` is fixed** — the skill never names or implicates a person, even at high AI likelihood. [EXPLICIT]

## Quality Criteria / Acceptance
- [ ] Every signal has evidence ids and a direction-aware 0..1 score.
- [ ] Classification matches threshold policy and is reproducible from the recorded signals.
- [ ] Watermark claims include evidence or are marked `not-checked` with a reason.
- [ ] Report does not accuse a person or assert authorship as fact (`authorship_claim` = `not-determined`).
- [ ] Decision policy avoids punitive automated action without human review.
- [ ] Contradictory signals lower confidence rather than being dropped.
- [ ] Machine-readable packets pass `scripts/validate_ai_content_detection_report.py`.

## Output Contract
Required top-level JSON fields:
- `schema`: `jm-labs.ai-content-detection.report.v1`
- `content`, `scope`, `evidence`, `signals`, `assessment`, `watermark`, `decision_policy`, `human_ai_strategy`, `validation`, `risks`

## Usage
Example invocations:
- "/ai-content-detection review this article"
- "Check whether this text is likely AI-generated and explain the limits"
- "Design a watermark and disclosure policy for hybrid human-AI content"
- "Validate this AI-content detection report packet"

### Worked Example (abridged)
Input: 900-word essay, no watermark, submitted for an academic integrity query.
- Signals: stylometry burstiness score `0.74` (ev: `sig-style-1`); metadata shows single-paste edit history `0.66` (ev: `sig-meta-1`); citation integrity — two fabricated DOIs `0.81` (ev: `sig-cite-1`); watermark `not-checked` (none present).
- Assessment: `likely-ai`, confidence `medium` (three concordant signals, no contradiction).
- `authorship_claim`: `not-determined`. Decision: route to human review; output uses "the text shows patterns consistent with AI generation," never "the student cheated." [EXPLICIT]

## Assumptions & Limits
- Detection is probabilistic and may be wrong. [EXPLICIT]
- The skill does not identify who authored content. [EXPLICIT]
- External detector claims require captured tool output as evidence. [EXPLICIT]
- High-stakes decisions require human review and documented policy. [EXPLICIT]
- Model-detector accuracy degrades as generators evolve; a stale detector is a false-negative source. [EXPLICIT]
- Absence of a watermark is not evidence of human authorship. [EXPLICIT]

## Anti-Scope
- No authorship attribution, identity inference, or intent claims. [EXPLICIT]
- No automated punishment, account action, or grade change without human sign-off. [EXPLICIT]
- No plagiarism/copy detection, SEO scoring, or general copy-editing. [EXPLICIT]

## Failure Modes
| Failure | Detection | Mitigation |
|---------|-----------|------------|
| Over-confident `likely-ai` on thin evidence | Single signal drives the label | Require >=2 concordant signals or drop to `inconclusive`. |
| Signal without evidence id | Validator flags missing `evidence` ref | Omit the signal; never score from assumption. |
| External detector output pasted as fact | No captured tool output in `evidence` | Mark `not-checked` or require authorized re-run. |
| Accusatory language leaks into output | Decision text names a person/intent | Enforce non-accusatory templates; `authorship_claim` stays `not-determined`. |
| Contradictory signals silently averaged | Confidence stays high despite conflict | Lower confidence and list conflicting signal ids. |

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Short sample | Mark as `inconclusive` unless strong provenance exists. |
| Human edited AI draft | Classify as `mixed` and recommend disclosure strategy. |
| Watermark unavailable | Set watermark status to `not-checked` with reason. |
| Detector score conflicts with metadata | Lower confidence and document contradictory signals. |
| User asks to punish a writer | Require human review and non-accusatory language. |
| Non-native or templated prose | Down-weight stylometry; note false-positive risk explicitly. |
| Mixed-language or translated text | Flag stylometry as low-reliability; lean on provenance/metadata. |
| User demands a yes/no authorship verdict | Decline the binary; return likelihood band plus limits. |
