<!-- distilled from alfa skills/accessibility-writing -->
<!-- > -->
# Accessibility Writing

> Accessible writing helps more people understand, decide, recover, and act.

## TL;DR

Use this skill to turn copy, UI text, docs, image descriptions, error messages, and instructions into accessible writing. It produces clean reader-facing copy plus a separate validation note with assumptions, evidence, unresolved questions, and not-verified items. Do not invent visual details, reading-level measurements, audience facts, legal claims, or cultural context. [EXPLICIT]

**In scope:** alt/long descriptions, microcopy, plain-language rewrites, link text, error copy, inclusive-language review, localization-readiness notes. **Out of scope (redirect, see Related Skills):** runtime a11y testing, WCAG audit evidence, ARIA/focus design, brand persuasion copy, translation itself (we prepare for it, we do not translate unless asked). [DOC]

## Procedure

### Step 1: Discover
- Identify the content type: alt text, UI microcopy, docs, instructions, error copy, link text, localization, or inclusive language review.
- Capture audience, language/locale, channel, brand constraints, reading-level target, and publication risk.
- Inventory assets and source context: image, chart data, screenshot, original text, destination URL, product terminology, code/API names, legal or regulated copy.
- Mark missing inputs as `not verified`; for images or charts, do not infer details that are not visible or provided. [EXPLICIT]

### Step 2: Analyze
- Classify each content item by job-to-be-done: inform, instruct, warn, recover, compare, navigate, or describe.
- For images, choose the right treatment: decorative empty alt, informative alt, functional alt, complex description, caption, or adjacent long description.
- For copy, check plain language, scannability, reading burden, inclusive wording, sensory-only instructions, link purpose, error recovery, and localization fit.
- Separate reader-facing copy from validation evidence so the final text remains usable.

### Step 3: Execute
- Produce accessible rewrites that preserve meaning, reduce jargon, define necessary acronyms, and keep one main idea per sentence or step.
- Write descriptive link text that makes sense out of context and distinguishes repeated links.
- Write error copy with the problem, likely cause when known, recovery action, and non-blaming tone.
- Replace sensory-only or positional instructions with names, labels, roles, headings, or stable identifiers.
- For inclusive language, propose contextual alternatives without silently changing code identifiers, product names, legal terms, or quoted source text.
- If writing to files, do so only when the user explicitly asks for an artifact or patch.

### Step 4: Validate
- Confirm reader-facing copy is clear without internal evidence tags unless the user requested inline annotation.
- Provide a validation table with changed item, issue, rewrite, rationale, evidence/source, assumption, and residual risk.
- Label reading level as measured only if a tool or user-provided measurement was actually used; otherwise mark it as an estimate.
- Reject keyword stuffing, invented image details, unsupported accessibility claims, and edits that erase necessary precision.

## Treatment decisions & trade-offs

Pick alt treatment by the image's job, not its content. Wrong choice is the most common defect. [INFERENCIA]

| Image role | Treatment | Trade-off / why |
|----------|-----------|-----------------|
| Pure decoration (dividers, mood photos) | Empty alt `alt=""` | Describing it adds noise to screen readers; silence is correct. [DOC] |
| Conveys information not in surrounding text | Informative alt (one idea, no "image of") | Redundant alt wastes the user's attention if text already says it. [INFERENCIA] |
| Is a control/link (icon button, logo-as-home-link) | Functional alt = the action, not the picture | A user needs "Search", not "magnifying glass". [DOC] |
| Data-dense (chart, diagram, map) | Short alt + adjacent long description from supplied data only | Cramming a chart into alt loses the data; long description must not invent values. [EXPLICIT] |
| Text inside an image | Transcribe the text verbatim | Paraphrase drops legally/functionally exact wording. [INFERENCIA] |

Plain-language order of operations: cut the unneeded → shorten what stays → define what's required → never delete a warning/constraint/decision criterion to hit a reading-level target. Simplicity that loses safety information is a regression, not an improvement. [DOC]

## Worked examples

These show the before→after shape; adapt wording to the real input. [INFERENCIA]

- **Link text:** `Click here` → `Download the 2026 tariff schedule (PDF, 1.2 MB)` — works out of context, distinguishes from other "here" links, warns of file type/size.
- **Error copy:** `Error 0x80004005` → `We couldn't save your changes because the connection dropped. Your draft is kept locally — reconnect and select Retry.` — problem + cause + recovery + non-blaming.
- **Sensory instruction:** `Tap the green button on the right` → `Select Confirm payment` — uses the label, survives color-blindness and reflowed/RTL layouts.
- **Informative alt:** decorative hero left `alt=""`; a stat graphic → `Returns rose from 12% to 31% between Q1 and Q4 2025` (only because those numbers were supplied).
- **Inclusive language with a code term:** prose says `allowlist`/`blocklist`; the identifier `whitelist_ips` in code stays unchanged, flagged with a rename suggestion for engineering — never silently edited. [EXPLICIT]

## Failure modes (what goes wrong and the guard)

| Failure mode | Guard |
|---|---|
| Hallucinated visual detail to make alt "complete" | If it's not in the asset or supplied data, mark `not verified` and ask. [EXPLICIT] |
| Reading level stated as fact without a tool | Label as estimate; recommend a measurement pass. [DOC] |
| Plain-language pass silently drops a warning | Diff meaning before/after; flag any removed constraint as residual risk. [INFERENCIA] |
| Inclusive edit renames a code/API/legal token | Preserve the token; propose an alias in prose, document the conflict. [EXPLICIT] |
| Evidence tags leak into user-facing copy | Keep tags in the validation note only, unless inline annotation was requested. [DOC] |
| SEO keywords crowd out usefulness | Prioritize the useful description; record the conflict, do not stuff. [DOC] |
| Writes a file the user didn't ask for | No file mutation without an explicit patch/artifact request. [EXPLICIT] |

## Quality Criteria
- [ ] Audience, locale, channel, and content type are explicit or marked `not verified`.
- [ ] Alt text decisions distinguish decorative, informative, functional, complex, and missing-context assets.
- [ ] Plain-language rewrites preserve meaning while reducing unnecessary jargon, passive voice, dense sentences, and unexplained acronyms.
- [ ] Link text, headings, instructions, and errors are specific enough to be understood out of context.
- [ ] Inclusive language changes are contextual and do not silently rename code, APIs, product terms, or quoted text.
- [ ] Reading-level claims are measured or explicitly labeled as estimates.
- [ ] Reader-facing output is separated from evidence/validation notes.
- [ ] Every assumption, unverifiable detail, and requested-but-unsafe change is called out.

## Acceptance criteria (deliverable is done when)
- Reader-facing copy stands alone: no evidence tags, no internal jargon, usable as-shipped. [DOC]
- A separate validation table exists with one row per change: item, issue, rewrite, rationale, evidence/source, assumption, residual risk. [DOC]
- Every non-obvious claim in the validation note carries exactly one tag from a single family; `[SUPUESTO]`/`not verified` items each name a concrete verification step. [DOC]
- No invented image, chart, demographic, or product detail anywhere in the output. [EXPLICIT]
- Reading-level statements are tagged measured or estimate, never an unbacked exact score. [DOC]
- No required code/API/legal/quoted term was silently altered. [EXPLICIT]

## Anti-Patterns

- Inventing image, chart, demographic, or product details to make alt text sound complete
- Stuffing SEO keywords into alt text at the expense of usefulness
- Making a text simpler by deleting critical warnings, constraints, or decision criteria
- Replacing technical terms that are required for the task without defining or preserving them
- Using only color, shape, size, or position to explain an action
- Claiming an exact reading level without measurement
- Putting evidence tags inside final user-facing copy by default

## Related Skills

- `accessibility-testing` — use for axe, keyboard, screen reader, contrast, and motion tests
- `accessibility-audit` — use for broader governance or WCAG audit evidence
- `accessibility-design` — use for component behavior, focus, ARIA, and visual interaction design
- `copywriting` or brand skills — use when persuasion or brand campaign copy is primary

## Usage

Example invocations:

- "/accessibility-writing" — Run the full accessibility writing workflow
- "Write alt text for these product images"
- "Rewrite this onboarding page in plain language"
- "Make this error copy accessible"
- "Review this document for inclusive language and reading burden"


## Assumptions & Limits

- Uses the language and locale of the input unless the user requests otherwise. [EXPLICIT]
- Assumes source text or asset context is available; missing image/chart data must be requested or marked `not verified`. [EXPLICIT]
- Does not certify legal, medical, financial, or regulatory wording; it can improve clarity and flag validation needs. [EXPLICIT]
- Does not replace `accessibility-testing` for runtime behavior, focus, screen reader, or contrast validation. [EXPLICIT]
- Does not mutate files unless the user explicitly asks for a patch or artifact. [EXPLICIT]
- Does not translate content; it prepares localization-ready copy (expansion room, no idioms, no baked-in text-in-image) unless translation is explicitly requested. [EXPLICIT]
- Reading-level output is an estimate unless a measurement tool or user-supplied score is used. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| Image or chart missing | Ask for the asset/data or mark visual details `not verified`; do not hallucinate |
| Decorative image | Recommend empty alt and explain where the visual meaning is carried |
| Complex chart | Provide short alt plus long description structure using only supplied data |
| SEO conflicts with alt usefulness | Prioritize user-useful description and document the conflict |
| Reading level requested without measurement tool | Provide estimate and measurement recommendation, not a guaranteed score |
| Inclusive language conflicts with code/API/legal names | Preserve required terms, suggest aliases or explanatory copy |
| Sensory-only instruction | Rewrite using label, role, heading, or stable identifier |
| Same link text points to different destinations on one page | Differentiate each so they are unambiguous out of context |
| Text baked into an image | Transcribe verbatim; flag for externalizing so it can localize and scale |
| Locale unknown for an idiom-heavy source | Mark `not verified`, avoid idioms, request target locale before final copy |

## Assets

- `assets/deliverable-checklist.md` provides the reusable checklist for final deliverable and guardian review.
