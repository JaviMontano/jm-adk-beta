<!-- distilled from alfa skills/portfolio-sites -->
<!-- > -->
# Portfolio Sites

> "Your portfolio is your reputation made visible." — Unknown

## TL;DR

Guides the creation of portfolio and showcase websites featuring project galleries, detailed case studies, smooth scroll animations, and functional contact forms. Use when building personal portfolios, agency showcases, or creative professional websites. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the portfolio owner's goals (job search, freelance clients, agency branding)
- Collect project assets (screenshots, descriptions, tech stacks, outcomes)
- Review personal brand elements (colors, typography, tone of voice)
- Determine required sections (about, projects, skills, testimonials, contact)

### Step 2: Analyze
- Plan project showcase format (grid gallery, carousel, filterable cards)
- Design case study template (challenge → approach → solution → results)
- Choose animation strategy (CSS transitions, Framer Motion, GSAP)
- Evaluate hosting and domain setup (custom domain, SSL)

### Step 3: Execute
- Build responsive layout with hero section and clear navigation
- Implement project gallery with category filtering and modal/page detail views
- Create case study pages with before/after visuals and measurable outcomes
- Add subtle scroll animations (fade-in, parallax) that enhance without distracting
- Build contact form with validation and email delivery (Formspree, Cloud Function)
- Optimize images with lazy loading and responsive srcset

### Step 4: Validate
- Test performance — portfolio must load fast (it's your first impression)
- Verify all project links, images, and external URLs work
- Check mobile layout — recruiters often view on phones
- Confirm contact form delivers messages and shows success/error feedback

## Quality Criteria

- [ ] Projects showcase measurable outcomes, not just screenshots
- [ ] Page loads in under 2 seconds with optimized media assets
- [ ] Animations are smooth (60fps) and respect prefers-reduced-motion
- [ ] Contact form works reliably with spam protection
- [ ] Evidence tags applied to all claims

## Anti-Patterns

- Over-animating — making the portfolio about effects instead of work
- Missing project context (just screenshots without explaining the problem solved)
- Using a template without customization (looks generic to reviewers)

## Related Skills

- `image-optimization` — critical for fast-loading galleries
- `scroll-interaction` — tasteful scroll-driven animations

## Usage

Example invocations:

- "/portfolio-sites" — Run the full portfolio sites workflow
- "portfolio sites on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
