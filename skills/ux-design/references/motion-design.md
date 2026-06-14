<!-- distilled from alfa skills/motion-design -->
<!-- > -->
# Motion Design
> "Method over hacks."
## TL;DR
Page transitions, scroll-triggered animation, parallax, and the durations/easings/performance budget that make them feel intentional instead of laggy. Animate `transform`/`opacity` only; respect `prefers-reduced-motion`. [EXPLICIT]

In scope: choreography (timing, easing, stagger), enter/exit transitions, scroll/parallax, perf budget. Out (anti-scope): per-element interaction feedback → `micro-interactions`; loading/skeleton states → `empty-states`; iconography motion specifics → `iconography`. [SUPUESTO]

## Procedure
### Step 1: Discover
- Catalog the moments needing motion (route change, element enter/exit, scroll reveal, state change). Capture intent per moment: orient, give feedback, or delight. [EXPLICIT]
- Record device floor and any brand motion tokens already defined. [EXPLICIT]
### Step 2: Analyze
- Pick duration/easing from the table per moment; justify deviations. Decide what does NOT move (motion is a scarce signal). [EXPLICIT]
### Step 3: Execute
- Animate only `transform` and `opacity` (GPU-composited, no layout/paint). Add `prefers-reduced-motion` fallback and tag each decision. [EXPLICIT]
### Step 4: Validate
- Verify against Quality Criteria and Acceptance Criteria below on the device floor, not a dev laptop. [EXPLICIT]

## Timing & Easing Reference
| Moment | Duration | Easing | Rationale |
|--------|----------|--------|-----------|
| Hover / small state | 100–150ms | ease-out | Feels instant; entry decelerates [EXPLICIT] |
| Enter (element appears) | 200–300ms | ease-out (decelerate) | Arrives and settles [EXPLICIT] |
| Exit (element leaves) | 150–200ms | ease-in (accelerate) | Leaves faster than it enters [EXPLICIT] |
| Page / route transition | 300–400ms | ease-in-out | Large surface needs more travel [EXPLICIT] |
| Scroll reveal | 400–600ms | ease-out | Slower read as content enters viewport [EXPLICIT] |

Trade-off: durations >400ms read as "premium" but block perceived responsiveness on repeated actions — reserve for one-shot transitions, never for frequent interactions. [SUPUESTO]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Only `transform`/`opacity` animated; no animation of `width`/`height`/`top`/`left`/`box-shadow` [EXPLICIT]
- [ ] `prefers-reduced-motion: reduce` collapses motion to instant or a cross-fade ≤120ms [EXPLICIT]
- [ ] Sustains 60fps (frame budget ≤16ms) on the device floor [EXPLICIT]
- [ ] Constitution XIII/XIV-compliant; actionable output

## Acceptance Criteria
- Every animated moment names its intent (orient / feedback / delight) and its duration+easing source. [EXPLICIT]
- Parallax/scroll effects are throttled via `requestAnimationFrame` or IntersectionObserver — never a raw `scroll` handler doing layout reads. [EXPLICIT]
- Reduced-motion path verified, not assumed. [EXPLICIT]

## Worked Example
Card grid reveal on scroll: each card `opacity:0; transform:translateY(16px)` → animates to `opacity:1; translateY(0)` over 400ms ease-out, staggered 60ms per card (cap total stagger ≈300ms so the last card is not left behind the fold). Trigger via IntersectionObserver at 15% visibility, fire once. Under reduced-motion: cards render at final state, no translate, optional 100ms fade. [EXPLICIT]

## Usage

Example invocations:

- "/motion-design" — Run the full motion design workflow
- "motion design on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and an agreed device/perf floor. [EXPLICIT]
- Requires English-language output unless otherwise specified. [EXPLICIT]
- Token values are platform-agnostic guidance, not a substitute for a brand motion spec when one exists. [SUPUESTO]
- Does not replace domain expert judgment for final decisions. [EXPLICIT]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| `prefers-reduced-motion: reduce` set | Disable parallax/large transitions; allow ≤120ms fades only [EXPLICIT] |
| Low-end / dropped frames on device floor | Cut stagger, shorten durations, drop parallax before sacrificing 60fps [SUPUESTO] |
| Many elements animating at once | Stagger or batch; never animate >~10 layout-affecting nodes simultaneously [SUPUESTO] |
