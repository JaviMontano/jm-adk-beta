---
name: metodologia
version: 1.0.0
owner: Javier Montaño (MetodologIA)
applies-to: MetodologIA web / commercial deliverables (the public site + client-facing content)
---

# Profile — MetodologIA (web / commercial)

> Source of truth for design tokens, voice, and brand structure = the **live MetodologIA site**.
> This profile carries the deliverable-quality standards extracted from constitution v6
> (Product Architecture, Design System, Brand Voice, Brand Separation, Content Authority)
> plus the commercial no-prices rule. Core (`constitution-v7`) stays domain-neutral; these
> live HERE. Evidence tags follow the harness convention: `[CODE]` `[CONFIG]` `[DOC]` `[INFERENCE]` `[ASSUMPTION]`.

When this profile is active, a deliverable is **not done** until every Acceptance block below passes (Constitution Principle 9).

---

## 1. Design System (canonical brandbook)

Aesthetic: dark-first, premium, glassmorphism over a deep-void blue field; gold as the primary
action color; cyan as the AI accent. `[CONFIG]` source: live site `index.css` + `style.css`.

### Design tokens — adopt EXACTLY (replaces beta's stale navy `#122562` / Trebuchet / Futura)

| Token | Value | Role |
|-------|-------|------|
| `--brand-gold` | `#FFD700` | primary / CTAs / headings accent |
| `--brand-cyan` (ai) | `#00FFFF` | AI accent, hover, secondary CTA |
| `--brand-blue-dark` | `#0A122A` | dark surface / on-gold foreground |
| `--brand-blue-light` | `#1E3A5F` | secondary surface |
| `--brand-gray` | `#B0C4DE` | muted body / borders |
| `--brand-white` | `#FFFFFF` | text on dark |

- **Chart-only accents** `[CONFIG]`: `--chart-1 #FFD700`, `--chart-2 #00FFFF`, `--chart-3 #3B82F6`, `--chart-4 #10B981` (green), `--chart-5 #8B5CF6`. These exist for **data visualization only**.
- **Fonts**: **Poppins** (headers, `font-heading`) + **Inter** (body, `font-body`). No Trebuchet, no Futura.

**Acceptance** `[CONFIG]`: no hardcoded hex/font outside the token set; only the brand palette + two typefaces appear in built CSS; gold/cyan never used as raw text where they fail contrast (see Guardrails).
**Anti-scope**: status/success signals come from icon + label, never from a bare color (see "no green-as-success").

---

## 2. Brand Voice (DUAL, TRILINGUAL ES/EN/PT)

Every published piece exists in **all three languages** (ES/EN/PT). Voice is chosen by **audience**, not by author mood. `[DOC]` source: `requirements_personas.md`, `requirements_empresas.md`.

### 2a. Personas / individuals — *El Sabio Visionario / Mentor Tecnológico*
- Tone: sophisticated, direct, inspiring; metaphors of evolution, operating-system, digital sovereignty. Avoid hollow jargon.
- Keywords: **Amplificación, Soberanía, Evolución, Agente, Estrategia, Futuro**.
- Examples (trilingual):
  - ES: "De Operador a Estratega: tu sistema operativo v3.0."
  - EN: "From Operator to Strategist: your operating system v3.0."
  - PT: "De Operador a Estrategista: o seu sistema operativo v3.0."

### 2b. Empresas / organizations — *El Estratega Corporativo / Arquitecto de Sistemas*
- Tone: executive, data-driven, ROI-focused; authority and certainty.
- Keywords: **Eficiencia, Escalar, Automatización, Gobernanza, Rentabilidad, Innovación**.
- Examples (trilingual):
  - ES: "Escala tu negocio de uno, compite como una agencia."
  - EN: "Scale your business of one, compete like an agency."
  - PT: "Escale o seu negócio de um, concorra como uma agência."

**Acceptance**: voice archetype matches the audience of the page; the three language variants of each piece carry the same claim and CTA.

---

## 3. Brand Structure

- **Pillars**: **Digital Champions** (personas — "Profesionales Amplificados") and **Value-Driven Organizations** (empresas — "Organizaciones Impulsadas por Valor e IA"). `[DOC]` `requirements_sitemap.md`.
- **Tagline**: *"Evolucionar con Método, Revolucionar con TecnologIA."*
- **Brand separation**: MetodologIA is a distinct brand. No references to parent companies in public content; visual identity is consistently MetodologIA; program names match the catalog exactly. Never mix brands in one output.

**Acceptance**: every public route resolves under a declared pillar; no parent-brand reference in public copy.

---

## 4. Guardrails

- **Accessibility (WCAG 2.1 AA)**: keyboard-navigable controls with visible focus ring; ARIA on modals; skip-to-content links; contrast ≥ 4.5:1 body / 3:1 large text & UI; meaningful `alt` (decorative = `alt=""`); admin UIs included. **Edge case** `[INFERENCE]`: gold `#FFD700` on white fails AA for body text — restrict gold to large headings, borders, or icon/CTA fills, never small body copy.
- **Brand coherence**: only the canonical tokens + Poppins/Inter; no palette drift.
- **Voice-by-audience**: Personas voice on `/digital-champions/*`, Empresas voice on `/value-driven-org/*` — never crossed.
- **No green-as-success** `[CONFIG]`: green `#10B981` exists ONLY as the data accent `--chart-4`. It is NEVER a success/status signal in UI or sample code — success is conveyed by an icon + label (e.g. ✓ "Listo / Done / Concluído"), with color drawn from gold/cyan. No sample in this profile may use green to mean "success."
- **Trilingual content authority (ES/EN/PT)**: every published piece exists in all three languages; one source of truth per piece (no split-brain). **Edge case** `[INFERENCE]`: during a migration the old store goes read-only the instant the new one becomes authoritative — overlap forbidden.

**Acceptance**: a11y audit reports zero serious/critical violations; red-list color scan finds zero green-as-success; all three language variants present before publish; no content piece authored in two stores at once.

---

## 5. Product Architecture (this profile builds a client-rendered, cloud-backed site)

- **Client-rendered, cloud-backed**: pages render in the browser (no SSR framework); editable content lives in a cloud document store fetched at runtime; static HTML is the shell, cloud is the data; no custom servers — managed cloud only (Firebase, Hostinger). **Acceptance** `[CONFIG]`: zero SSR framework in deps; first paint works with backend mocked offline. **Anti-scope**: does not rule out build-time static generation or Cloud Functions for non-render tasks.
- **SEO integrity**: every public page exposes description, robots, canonical, Open Graph, Twitter Card; internal/admin pages `noindex`; sitemap reflects actual structure; dynamic content in DOM before crawl timeout. **Acceptance**: sitemap entry count = published-route count.
- **Offline resilience**: client-side caching; critical content cached after first visit; version-keyed stale-while-revalidate invalidation; last-known-good content shown, never a raw error. **Edge case** `[INFERENCE]`: first-ever visit with no cache and no network shows a branded offline notice, not a blank page.
- **Component consistency**: site-wide elements are web components; one unified modal system; CSS follows the token + layering system above; backend access through centralized service modules; i18n via a single `data-i18n` attribute contract. **Acceptance**: no duplicate modal/i18n/service implementation.

---

## 6. Commercial Rule (profile-scoped — NOT core)

No client-facing prices in deliverables. Express effort in **effort units + disclaimers** only — no currency, no rates, no totals. This is the MetodologIA commercial declaration honored by Constitution Principle 8 (Estimation Integrity), not a universal harness law.

**Acceptance**: no currency/rate/total in any client-facing artifact; estimates use effort units and carry their disclaimer.
