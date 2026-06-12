<!-- distilled from alfa skills/newsletter-design -->
<!-- > -->
# Newsletter Design

> "Method over hacks. Evidence over assumption."

## TL;DR

Designs recurring newsletters end-to-end: positioning and content architecture, the subject/preheader pair, section layout, engagement-metric instrumentation, send-time and cadence optimization, and list-health hygiene. Produces a content template plus a measurement plan, not just a one-off HTML email. Outputs follow MetodologIA brand standards and evidence tagging. Use when standing up a new newsletter or diagnosing one with declining open/click rates. [EXPLICIT]

Boundary: this skill decides *what* the newsletter contains and *how engagement is measured*. The actual HTML/MJML build is `email-template-builder`; delivery and authentication are `email-sending`. [EXPLICIT]

## Procedure

### Step 1: Discover
- Define the single job-to-be-done: why a subscriber stays subscribed (one sentence). A newsletter without one is a content dump and churns. [EXPLICIT]
- Capture cadence (weekly/biweekly/monthly), audience segment(s), and the sender identity (person vs brand — person-from names typically lift opens). [EXPLICIT]
- Pull baselines if the newsletter exists: open rate, click rate (CTR), click-to-open (CTOR), unsubscribe rate, spam-complaint rate, list size and growth. Without baselines you cannot prove improvement. [EXPLICIT]
- Inventory content sources (blog, product updates, curated links) and who supplies each. [EXPLICIT]

### Step 2: Analyze
- Pick a content architecture and justify it (XIII Think First, XIV Simple First):
  - **Single-feature** — one story, one CTA. Highest clarity/CTOR; best for product/announcement. [EXPLICIT]
  - **Digest** — 3–6 curated items with one-line summaries. Scannable; best for curation/community. [EXPLICIT]
  - **Editorial** — a written lead plus links. Builds voice/loyalty; highest authoring cost. [EXPLICIT]
  - Trade-off: more sections raise total clicks but dilute any single CTA and lengthen authoring time. Default to fewer sections unless data shows multi-topic demand. [EXPLICIT]
- Design the subject + preheader as a pair (the preheader is the second subject line, not filler). Plan an A/B test on the subject for any list large enough for significance. [EXPLICIT]
- Define one primary CTA per issue; secondary links are navigation, not goals. [EXPLICIT]
- Choose send time/day from the audience's timezone and past engagement, not folklore. [EXPLICIT]

### Step 3: Execute
- Write the content template: fixed sections, ordering, and a one-line purpose per section so future issues stay consistent. [EXPLICIT]
- Lead with value above the fold; place the primary CTA before the first scroll. [EXPLICIT]
- Add UTM parameters to every link so clicks attribute in analytics; without them CTR is unmeasurable downstream. [EXPLICIT]
- Specify the segmentation and any A/B split, then hand the layout to `email-template-builder` for the HTML/MJML build. [EXPLICIT]
- Apply evidence tags to all claims; use the brand template for HTML outputs (references/brand/). [EXPLICIT]

### Step 4: Validate
- Confirm the measurement plan is wired: opens, CTR, CTOR, unsubscribe, and complaint rate all captured per issue and comparable to baseline. [EXPLICIT]
- Verify one clear primary CTA, working unsubscribe, and present plain-text/preheader. [EXPLICIT]
- Check evidence-tag coverage and Constitution compliance. [EXPLICIT]

## Engagement Metrics

Targets are directional reference points, not guarantees — your benchmark is your own trend, not an absolute. [EXPLICIT]

| Metric | What it tells you | Healthy direction |
|--------|-------------------|-------------------|
| Open rate | Subject/preheader + sender + deliverability | Rising; falling opens often mean deliverability, not bad copy [EXPLICIT] |
| CTR (clicks/delivered) | Whether content drove action | Rising with stable opens |
| CTOR (clicks/opens) | Content/CTA quality, isolated from deliverability | Most honest content signal [EXPLICIT] |
| Unsubscribe rate | Cadence/relevance mismatch | Low and stable; a spike flags a content or frequency problem |
| Spam-complaint rate | Consent/expectation breakdown | Near zero; even small rates harm sender reputation [EXPLICIT] |

Note: Apple Mail Privacy Protection inflates opens by pre-fetching images, so treat opens as a soft signal and lean on CTOR for content decisions. [EXPLICIT]

## Quality Criteria

- [ ] One stated job-to-be-done and one primary CTA per issue
- [ ] Subject + preheader designed as a pair; A/B planned where list size allows
- [ ] Every link carries UTM parameters; metrics comparable to a baseline
- [ ] Send time/cadence justified by audience data, not assumption
- [ ] Follows Constitution principles; evidence tags on all claims
- [ ] No redundancy or padding

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Acting without understanding | Wastes effort on wrong solution | Think First (XIII) |
| Over-engineering | Complexity without value | Simple First (XIV) |
| Missing evidence tags | Claims without basis | Tag every assertion |
| Multiple co-equal CTAs | Splits attention, lowers CTOR | One primary CTA; rest are navigation |
| Optimizing opens in isolation | Apple MPP inflates them | Judge content by CTOR; opens for deliverability only |
| Never pruning the list | Dead addresses depress rates and reputation | Sunset/re-engage inactive subscribers |
| Buying or scraping addresses | Spam complaints, blocklisting | Grow via opt-in only |

## Related Skills

- `email-template-builder` — turns this content design into responsive HTML/MJML
- `email-sending` — delivery, authentication (SPF/DKIM/DMARC), and bounce handling
- `email-templates` — reusable bulletproof layout patterns

## Usage

Example invocations:

- "/newsletter-design" — Run the full newsletter design workflow
- "newsletter design on this project" — Apply to current context

Worked example — *declining opens on a monthly digest*: baseline open 22%, CTOR 9%, unsubscribe 0.3%. Opens drifting down over four issues while CTOR holds steady points to deliverability (authentication or list rot), not weak content. Action: audit SPF/DKIM/DMARC via `email-sending`, sunset 6-month-inactive subscribers, and run a subject A/B — do *not* rewrite all the content, because CTOR shows engaged readers still click. [EXPLICIT]

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Assumes an ESP/analytics stack that reports opens, clicks, and unsubscribes; without it, metric targets are advisory only [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Covers design and measurement, not the HTML build or delivery infrastructure (see Related Skills) [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
| New newsletter, no baseline | Set provisional targets from segment norms; flag first 2–3 issues as calibration, not pass/fail [EXPLICIT] |
| List too small for A/B significance | Skip the split; iterate on one variant and judge by trend across issues [EXPLICIT] |
| Open rate collapses, CTOR steady | Treat as deliverability (auth/list rot), not content — route to `email-sending` [EXPLICIT] |
| Unsubscribe/complaint spike | Pause sends, review cadence and last issue's relevance before resuming [EXPLICIT] |
