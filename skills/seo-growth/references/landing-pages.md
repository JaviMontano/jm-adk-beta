<!-- distilled from alfa skills/landing-pages -->
<!-- > -->
# Landing Pages — Personal Brand Web Presence

> TL;DR: Build a high-quality personal brand or professional landing page — dark-first design, bilingual ES/EN, JM Labs brand system, self-contained HTML ready to deploy.

**Principio Rector:** A landing page is a first impression compressed into 5 seconds. Design for clarity, credibility, and a single action.

**Tagging:** This file uses the Alfa core set — `[EXPLICIT]` (stated/scoped here), `[INFERRED]`/`[INFERENCE]` (derived), `[ASSUMPTION]` (no direct evidence; pair with a verification step). Canon: `references/verification-tags.md`. One tag per claim; never mix families. [DOC]

---

## When to Activate

**Activate when:**
- User says "landing page", "personal brand page", "portfolio site", "create my web page" [EXPLICIT]
- User says "página web personal", "quiero una web", "professional website for me" [EXPLICIT]
- User needs an online presence for job search, consulting, speaking, or freelancing [INFERRED]
- User needs a product or service launch page [EXPLICIT]

**Do NOT activate (anti-scope) — redirect:**

| Request | Why out of scope | Route to |
|---------|------------------|----------|
| Full multi-page site (nav tree, /about, /blog routes) | This skill is single-page only | full web design process [EXPLICIT] |
| E-commerce store (cart, checkout, inventory) | Needs backend + payment | `ecommerce-frontend` [EXPLICIT] |
| Blog / CMS (post feed, authoring) | Needs content store | `blog-cms` [EXPLICIT] |
| Marketing funnel with A/B testing | Needs experiment infra | `conversion-optimization` [EXPLICIT] |
| Authenticated app / dashboard | Needs auth + state | out of scope entirely [EXPLICIT] |

**Boundary rule:** if the ask grows a second route or a server-side data store, stop and hand off — do not bolt routing onto a single-page deliverable. [ASSUMPTION] Verify by asking "does this need more than one URL or a database?" before building.

---

## S1 — Page Types

Identify the page archetype before designing. Each has a different content hierarchy and a different *primary conversion*. Pick exactly one archetype; mixing dilutes the single-action principle. [EXPLICIT]

| Archetype | For | Hero | Core sections | Primary CTA | Conversion event |
|-----------|-----|------|---------------|-------------|------------------|
| **Portfolio** | Designers, developers, writers, creatives | Name + role + one strong visual/project thumbnail | Featured projects with outcomes, tech/skill stack, brief bio | "View my work" / "Hire me" | Contact form submit [EXPLICIT] |
| **Consultant / Freelancer** | Independent consultants, coaches, fractional execs | Name + value prop + credibility signal (clients/results) | Services, process, case studies/testimonials, about, contact | "Book a call" / "Get a proposal" | Calendar booking [EXPLICIT] |
| **Speaker / Thought Leader** | Keynote speakers, podcast guests, presenters | Name + speaking topic + video reel link/thumbnail | Topics/talks, past events, media kit, testimonials, booking | "Book me to speak" / "Download media kit" | Booking or kit download [EXPLICIT] |
| **Executive / Professional** | Job seekers, C-suite candidates, board members | Name + current role + professional photo placeholder | Career highlights (3-5), expertise areas, education, contact | "Download CV" / "Connect on LinkedIn" | CV download / LinkedIn click [EXPLICIT] |
| **Product / Service Launch** | SaaS, courses, events, service launches | Product name + one-line value prop + CTA above fold | Problem, solution, features, pricing/tiers, FAQ, social proof | "Start free trial" / "Join waitlist" / "Buy now" | Trial signup / waitlist join [EXPLICIT] |

**Decision — archetype selection:** drive off the *conversion event the user can actually fulfill today*, not their job title. Trade-off: a job-seeker who also consults could fit Executive or Consultant; choose by which CTA they can honor this week (a live Calendly → Consultant; only a PDF → Executive). [INFERENCE] If unclear, ask one question: "When someone lands, what is the single best thing they can do?"

**Edge — archetype ambiguity:** if two archetypes tie, default to the one with the *lowest-friction* CTA (download > form > booking) to maximize a first conversion, and note the assumption in a code comment. [ASSUMPTION]

---

## S2 — Content Architecture

Universal content hierarchy that works across all page types. Sections are an ordered funnel: each answers the objection the previous one raised. [EXPLICIT]

### Section Map

```
[1] HERO           — Name/product + role/tagline + primary CTA + credibility signal
[2] ABOUT / VALUE  — Who are you? What problem do you solve? Why you?
[3] SERVICES/WORK  — What you offer or what you have built (portfolio/features)
[4] SOCIAL PROOF   — Testimonials, logos, metrics, awards, media mentions
[5] PROCESS / FAQ  — How you work or common questions
[6] CTA BLOCK      — Repeated CTA with urgency or low-friction offer
[7] CONTACT        — Contact form or direct email/calendar link
[8] FOOTER         — Links, legal, social profiles
```

**Why this order** (objection chain): Hero earns 5 seconds → About answers "why you" → Work proves capability → Proof de-risks → Process removes uncertainty → CTA captures intent → Contact closes. Reordering breaks the chain (e.g. pricing before proof reads as presumptuous). [INFERENCE]

**Minimum viable page (Quick mode):** sections [1] and [7] only — Hero + Contact. Everything between is trust-building; drop it only when the visitor already knows the person (LinkedIn supplement, job application follow-up). [EXPLICIT]

### Copywriting Principles

**Hero Headline Formula:** `[Result they want] + [for whom] + [without their pain]`

Worked example: "Strategic product clarity for ambitious startups — without the 6-month consulting engagement."

**Value Proposition Hierarchy:**
1. Primary headline (8 words or fewer, outcome-focused)
2. Subheadline (1-2 sentences, who + how + proof)
3. Supporting bullets (3 max, each starting with a benefit verb)
4. CTA button (action verb + specificity: "Book your free 30-min call")

**Social Proof Formats (ranked by trust level, highest first):**
1. Video testimonial with name + role + company
2. Quote + name + role + company + photo
3. Logo grid (companies you worked with)
4. Specific metric ("Helped 47 companies raise Series A")
5. Media mention ("As featured in...")

**Decision — proof selection:** use the highest tier the user can *substantiate*, never the highest tier available. Trade-off: a fabricated metric or borrowed logo is worse than an honest tier-2 quote — it fails on first reference-check and burns credibility. [INFERENCE] Governance: no invented metrics, client names, or logos the user cannot evidence. [EXPLICIT] If the user has zero proof, ship without section [4] rather than fake it, and flag the gap. [ASSUMPTION]

**Failure modes (copy):**
- Headline describes *you* ("I am a...") instead of the *visitor's outcome* → rewrite to result-first. [INFERRED]
- More than 3 bullets → visitor skims none; cut to the 3 highest-value. [INFERRED]
- Vague CTA ("Learn more", "Submit") → replace with the specific action + payoff. [EXPLICIT]
- Two competing CTAs above the fold → keep one primary; demote the rest to ghost/text links. [INFERENCE]

---

## S3 — JM Labs HTML System

Full implementation spec for the HTML page. Single brand only — never blend JM Labs tokens with another brand's palette in one file. [EXPLICIT]

### Brand Tokens

```css
:root {
  /* Core brand palette */
  --jml-navy:    #122562;   /* primary background sections */
  --jml-gold:    #FFD700;   /* accent, CTAs, highlights */
  --jml-blue:    #137DC5;   /* links, secondary actions, icons */
  --jml-bg:      #0d1b3e;   /* page background (darkest) */
  --jml-surface: rgba(255,255,255,0.05); /* card background */
  --jml-border:  rgba(255,215,0,0.2);   /* gold-tinted borders */

  /* Typography */
  --font-head: 'Poppins', sans-serif;   /* headings: weight 600-900 */
  --font-body: 'Inter', sans-serif;     /* body: weight 400-800 */

  /* Spacing scale */
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 2rem;
  --space-lg: 4rem;
  --space-xl: 8rem;
}
```

**Contrast guard:** gold `#FFD700` on navy `#122562` passes WCAG AA for large text; gold on white (`light` theme) fails — in light mode, CTA text must flip to navy on a gold fill, not gold on light. [INFERENCE] Verify each text/background pair against a 4.5:1 (body) / 3:1 (large) ratio before shipping. [EXPLICIT]

### CSS Classes Reference

| Class | Usage |
|-------|-------|
| `.jml-doc` | Root wrapper for all JM Labs pages |
| `.slide` | Full-viewport hero section |
| `.bridge` | Transitional summary section (navy bg, centered) |
| `.cta` | Call-to-action block with gold button |
| `.mv` | Main value section (content sections) |
| `.ml` | Multi-layout section (2-3 column grids) |
| `.gold` | Gold text accent class |
| `.src` | Evidence chip (explicit/inferred/open) |

### Bilingual Pattern (ES/EN)

```html
<!-- Language toggle button -->
<button class="lang-toggle gold" onclick="toggleLang()">ES | EN</button>

<!-- Bilingual content — show/hide via JS -->
<h1>
  <span data-l="es">Tu Nombre Aqui</span>
  <span data-l="en" style="display:none">Your Name Here</span>
</h1>

<script>
  let lang = 'es';
  function toggleLang() {
    lang = lang === 'es' ? 'en' : 'es';
    document.querySelectorAll('[data-l]').forEach(el => {
      el.style.display = el.dataset.l === lang ? '' : 'none';
    });
    document.documentElement.lang = lang;        // keep <html lang> truthful for SEO/a11y
    try { localStorage.setItem('lang', lang); } catch (e) {}
  }
</script>
```

**Bilingual failure modes:**
- Default-hidden `data-l="en"` spans are still in the DOM, so crawlers and screen readers may read *both* languages. Set `document.documentElement.lang` on toggle (above) and prefer `hidden`/`display:none` over visually-hidden so AT skips the inactive language. [INFERENCE]
- `og:locale` and the meta description are single-language — pick the primary audience language for share previews; toggling JS does not rewrite OG tags. [EXPLICIT]
- Missing translation for one span → visitor sees a blank where text should be. Lint: every `data-l="es"` must have a sibling `data-l="en"`. [ASSUMPTION] Verify by counting both attributes; they must match.

### Dark/Light Mode Toggle

```css
[data-theme="light"] {
  --jml-bg: #f0f4ff;
  --jml-navy: #e8eeff;
  --jml-surface: rgba(18,37,98,0.05);
  color: #122562;
}
```

```html
<button class="theme-toggle"
  onclick="document.documentElement.dataset.theme =
    document.documentElement.dataset.theme === 'light' ? '' : 'light'">
  Dark / Light
</button>
```

**Decision — dark-first default:** ship dark as default (brand identity + lower glare for evening browsing), expose light as a toggle. Trade-off: dark-default can fail print and some corporate-email embeds; document the default in a code comment and ensure light mode is one click away. [INFERENCE] Do NOT auto-switch on `prefers-color-scheme` unless requested — an unexpected light flash off-brand surprises the user. [ASSUMPTION]

### Full HTML Page Template Structure

```html
<!DOCTYPE html>
<html lang="es" data-theme="">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Name] — [Tagline]</title>
  <!-- SEO + OG meta tags (see S4) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;900&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
  <style>/* All CSS inline — fully self-contained */</style>
</head>
<body>
  <a class="skip-nav" href="#hero">Skip to content</a>  <!-- a11y: first focusable -->
  <nav><!-- Minimal: name/logo + lang toggle + theme toggle --></nav>
  <main>
    <section class="slide" id="hero">    <!-- [1] Hero --></section>
    <section class="bridge" id="about">  <!-- [2] About --></section>
    <section class="mv" id="services">   <!-- [3] Services/Work --></section>
    <section class="ml" id="proof">      <!-- [4] Social Proof --></section>
    <section class="mv" id="process">    <!-- [5] Process/FAQ --></section>
    <section class="cta" id="cta">       <!-- [6] CTA Block --></section>
    <section class="mv" id="contact">    <!-- [7] Contact --></section>
  </main>
  <footer><!-- Social links + legal --></footer>
  <script>/* Lang toggle + theme toggle + smooth scroll */</script>
</body>
</html>
```

---

## S4 — SEO & Performance

Target Lighthouse 95+ on Performance, Accessibility, and SEO. [EXPLICIT]

### Meta Tags

```html
<!-- Basic SEO -->
<title>[Name] — [Role] | [City]</title>
<meta name="description" content="[1-2 sentence value proposition. 150 chars max.]">
<link rel="canonical" href="https://[yourdomain.com]/">

<!-- Open Graph (social sharing) -->
<meta property="og:title" content="[Name] — [Role]">
<meta property="og:description" content="[Same as meta description]">
<meta property="og:image" content="https://[domain]/og-image.png">
<meta property="og:url" content="https://[yourdomain.com]">
<meta property="og:type" content="website">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="[Name] — [Role]">
<meta name="twitter:image" content="https://[domain]/og-image.png">

<!-- Schema.org Person markup -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "[Full Name]",
  "jobTitle": "[Title]",
  "url": "https://[domain]",
  "sameAs": ["https://linkedin.com/in/...", "https://twitter.com/..."]
}
</script>
```

**Meta gotchas:**
- `og:image` must be an absolute URL (`https://...`), min 1200×630, < 1 MB, and exist before sharing — relative paths render no preview. [EXPLICIT]
- `canonical` must be the live deployed URL, not a placeholder — a stale `[yourdomain.com]` self-canonicalizes to nothing and tanks indexing. [INFERENCE] Verify post-deploy.
- Use `@type: Product` (with `name`, `offers`) instead of `Person` for the Launch archetype; using `Person` on a product page is a schema mismatch. [EXPLICIT]
- One `<title>` and one `<h1>` per page; the bilingual pattern must not emit two visible `<h1>`s. [INFERRED]

### Performance Rules

- All fonts via Google Fonts with `display=swap` (prevents FOIT) [EXPLICIT]
- No external CSS/JS beyond Google Fonts — fully self-contained file [EXPLICIT]
- Hero section: text + CSS gradient background (no large images above fold) [EXPLICIT]
- Images: WebP format, explicit `width`/`height` attributes (prevents CLS) [EXPLICIT]
- CSS: minified inline, no render-blocking resources [EXPLICIT]
- Contact form: HTML5 native form `action` (Formspree URL) — no JS libraries [EXPLICIT]
- `loading="lazy"` on every below-fold image; eager-load only the hero visual if any. [INFERRED]
- `preconnect` to `fonts.gstatic.com` as well as `fonts.googleapis.com` — the font *files* come from the former. [INFERENCE]

**Performance failure modes:** Google Fonts is render-blocking despite `swap` (blocks first paint on the CSS request) — for max score, self-host or inline a subset; trade-off is a larger file and losing the CDN cache. [INFERENCE] A single hero background image without `width`/`height` is the most common CLS regression. [INFERRED]

---

## S5 — Deploy Options

Three paths from simple to robust. Pick by the *user's* skill and ownership needs, not by lowest cost. [EXPLICIT]

| Option | Best for | SSL / CDN | Custom domain | Cost | Main trade-off |
|--------|----------|-----------|---------------|------|----------------|
| **A — Hostinger** | Non-devs | Free SSL (manual enable) | Yes (DNS panel) | $3–10/mo [EXPLICIT] | Pay monthly; manual file upload; no git history [INFERENCE] |
| **B — Firebase Hosting** | Devs | Free SSL + global CDN | Yes | Free (Spark, static) [EXPLICIT] | Requires Node/CLI + Google account [INFERENCE] |
| **C — GitHub Pages** | Anyone with a repo | Free SSL via CNAME | Yes (CNAME file) | Free [EXPLICIT] | Public repo unless paid; slower cache purge [INFERENCE] |

### Option A — Hostinger
1. Export HTML as `index.html`
2. Upload via Hostinger File Manager to `public_html/`
3. Configure custom domain in DNS panel
4. Enable free SSL in control panel

### Option B — Firebase Hosting
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```

### Option C — GitHub Pages
1. Create repo `username.github.io`
2. Push `index.html` to main branch
3. Enable Pages in repo Settings → Pages → Deploy from branch
4. Add CNAME file for custom domain

**Deploy gotchas:** custom-domain SSL needs DNS propagation (minutes–48h) — verify HTTPS resolves before sharing. [INFERENCE] After deploy, update `canonical`, `og:url`, and `og:image` to the real domain or social previews stay blank. [EXPLICIT] Note: deployment is the *user's* action; this skill produces the file and the steps, not a live site. [EXPLICIT]

---

## Trade-off Matrix

| Mode | Time | Output | Sections | Best For |
|------|------|--------|----------|---------|
| **Quick** | ~1h | Hero + contact only | [1] [7] | Job applications, LinkedIn supplement |
| **Standard** | ~3h | Full 7-section page, bilingual | [1]–[7] | Consultant/freelancer launch |
| **Premium** | ~6h | Full page + CSS animations + SEO schema + deploy guide | [1]–[7] + extras | Executive brand, speaker page |

Time figures are planning estimates, not commitments. [ASSUMPTION] Mode is a scope dial, not a quality dial — Quick still ships valid, accessible, branded HTML; it ships *fewer sections*, not sloppier ones. [EXPLICIT]

---

## Assumptions & Limits

- Single-page only — no routing, no CMS, no database. [EXPLICIT]
- User provides a content brief or answers content prompts. If absent, the page ships with clearly-labeled `[PLACEHOLDER]` copy, never invented biography or fake metrics. [EXPLICIT]
- No real images included — CSS placeholder divs with aspect ratios provided. [EXPLICIT]
- Google Fonts CDN required by default (offline embedding inflates file size); self-hosting is the documented escape hatch for max Lighthouse. [EXPLICIT]
- Contact form needs Formspree or similar — backend not included; without an `action` URL the form is inert. [EXPLICIT]
- Output is HTML/CSS/JS code; deployment and domain purchase are the user's actions. [EXPLICIT]
- No analytics/tracking injected by default — privacy posture is opt-in, and adding it is the user's decision. [ASSUMPTION]
- Single brand (JM Labs) per file; another brand requires its own token set, never a blend. [EXPLICIT]

---

## Edge Cases

| Scenario | Handling |
|----------|---------|
| No photo for hero | CSS avatar: initials in gold circle on navy bg |
| Animation-heavy request | CSS keyframes only — no external libs (self-contained rule); respect `prefers-reduced-motion` to disable for sensitive users [INFERRED] |
| Content only in English | Skip bilingual toggle; single-language version, `<html lang="en">` |
| WCAG accessibility required | aria-labels, alt text, visible focus indicators, skip-nav link, 4.5:1 contrast |
| Wants both dark + light as default | Default dark; light toggle available; document choice in code comment |
| No social proof to show | Omit section [4]; do not fabricate logos/metrics; flag the gap to the user |
| Extremely long name / 40-char headline | Use `clamp()` for fluid type so the hero never overflows or wraps awkwardly [INFERRED] |
| User pastes an unverifiable claim ("#1 in market") | Soften to a defensible phrasing or drop it; flag as `[POR_CONFIRMAR]` in a comment [ASSUMPTION] |
| RTL language requested (e.g. Arabic) | Out of scope for the ES/EN pattern; set `dir="rtl"` and hand off — toggle logic assumes LTR [ASSUMPTION] |

---

## Good vs Bad Example

**BAD hero section:**
> "Welcome to my website. I am a professional with many years of experience."

Why it fails: describes the author, not the visitor's outcome; no specific result, no audience, no proof, generic CTA. [INFERRED]

**GOOD hero section:**
> Headline: "I help Series A startups find product-market fit." · Subheadline: "Product strategist with 11 years in B2B SaaS. Former Head of Product at Rappi." · CTA: "Book a free discovery call"

Why it works: outcome-first headline, audience named, proof (years + named employer) in the subheadline, one specific low-friction CTA. [INFERENCE]

---

## Validation Gate

Ship only when every box is checked. [EXPLICIT]

**Structure & copy**
- [ ] Page type identified; content architecture matches the archetype (S1)
- [ ] Required sections present for the chosen mode (Quick = [1]+[7]; Standard/Premium = [1]–[7])
- [ ] Exactly one `<h1>`; hero headline follows outcome + audience + pain-relief formula
- [ ] One primary CTA above the fold; no competing primary CTAs
- [ ] At least one social proof element — or section [4] omitted with the gap flagged (none fabricated)
- [ ] No invented metrics, client names, or logos

**Brand & i18n**
- [ ] JM Labs tokens applied (navy `#122562`, gold `#FFD700`, blue `#137DC5`); single brand only
- [ ] Bilingual ES/EN toggle via `data-l`, each `es` span paired with an `en` sibling, `<html lang>` updates on toggle — or single-language with correct `lang`
- [ ] Dark/light toggle via `data-theme`; dark default documented in a comment

**SEO & performance**
- [ ] All meta tags present (title, description ≤150 chars, canonical, OG, Twitter Card)
- [ ] Schema.org `Person` (or `Product` for Launch) markup matches the archetype
- [ ] `og:image` absolute URL, 1200×630, exists
- [ ] Fully self-contained (no external CSS/JS beyond Google Fonts)
- [ ] Below-fold images lazy-loaded with explicit `width`/`height`; no above-fold large image
- [ ] Lighthouse Perf/A11y/SEO ≥95 achievable

**Accessibility**
- [ ] Skip-nav link, visible focus indicators, alt text, aria-labels
- [ ] Contrast ≥4.5:1 body / ≥3:1 large text in BOTH themes
- [ ] `prefers-reduced-motion` honored if animations present

**Deploy readiness**
- [ ] Contact form has a real `action` URL (or is clearly marked inert/placeholder)
- [ ] `canonical`/`og:url`/`og:image` point to the real domain (post-deploy check)

---

## Reference Files

- `references/verification-tags.md` — Tagging canon (Alfa core set used here)
- `knowledge/body-of-knowledge.md` — Web design and conversion psychology foundations
- `evals/` — Scored landing page examples

---

## Related Skills

- `cv-enhancement` — Generate the downloadable CV to link from the executive page
- `seo-architecture` — Deeper SEO strategy for content-rich pages
- `b2b-outreach` — Use the landing page as a credibility asset in outreach messages
- `html-brand` — Lower-level JM Labs HTML brand system reference
- `conversion-optimization` — A/B testing and funnel work (out of scope here; hand off)
