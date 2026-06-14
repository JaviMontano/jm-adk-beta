<!-- distilled from alfa skills/brand-html -->
<!-- > -->
# Brand HTML / Web Generation

## Purpose

Generate self-contained, accessible, responsive HTML/CSS artifacts that are
deterministically tied to a brand configuration. The skill may write the
requested HTML artifact, but validation is read-only and must pass the local
contract before delivery. [CONFIG]

**Determinism boundary.** Same brand config + same content + same `artifact_date`
must yield byte-identical HTML. No randomness, no inferred dates, no remote
fetches at generate time — those break reproducibility and the offline gate. [INFERENCIA]

**Anti-scope.** Not a site builder. One self-contained file per call; no SPA,
routing, build step, JS framework, server, or multi-page navigation graph. If
the request needs any of those, say so and stop — do not partially deliver. [CONFIG]

## Deterministic Resources

- `assets/manifest.json` declares all deterministic assets. [CÓDIGO]
- `assets/activation-policy.json` defines activation, routing, and false
  positives. [CÓDIGO]
- `assets/brand-html-contract.json` defines required artifact structure,
  dependency boundaries, token rules, and validator checks. [CÓDIGO]
- `assets/favicon-policy.json` and `assets/favicon.svg` define deterministic
  browser favicon behavior. [CÓDIGO]
- `assets/fallback-brand-config.json` defines explicit fallback tokens when no
  brand config is supplied. [CÓDIGO]
- `assets/evidence-policy.json` defines evidence tags and report requirements.
  [CÓDIGO]
- `scripts/check.sh` validates valid and invalid HTML fixtures offline. [CÓDIGO]

## When To Activate

Activate when the user asks for a branded HTML page, landing page, responsive
web page, styled HTML report, single-file web artifact, CSS-variable brand page,
or HTML generated from brand tokens. [CONFIG]

Do not activate for DOCX, XLSX, PDF, slides, token extraction-only tasks, or
generic brand strategy without an HTML artifact request. Route those to the
appropriate document or brand skill. [CONFIG]

## Inputs

| Input | Required | Default if absent | Failure if malformed |
|---|---|---|---|
| Page type / content outline / report sections | yes | — | `{VACIO_CRITICO}`→ no content to render, stop and ask |
| Brand config path or inline tokens | no | fallback config (see below) | bad JSON → fall back, note `[SUPUESTO]` |
| Language + direction (`ltr`/`rtl`) | no | `lang="en"`, `dir="ltr"` | unknown dir → default `ltr`, flag it |
| `artifact_date` (caller-supplied) | no | omit any date entirely | never infer current date — gate rejects |
| External-font permission | no | disabled (self-contained) | links present without permission → strip, note |

Content is the only hard input. Everything else has a deterministic default so the
skill never blocks on optional fields. [INFERENCIA]

## Brand Configuration

Search order:

1. Path passed as argument.
2. `./brand-config.json` in the working directory.
3. `references/brand/design-tokens.json` when the current repo brand applies.
4. `assets/fallback-brand-config.json` when no brand config exists.

First match wins; stop searching. Never read `~/.claude/brand-config.json` or
hidden user-level files for this skill — user-level config would make output
non-reproducible across machines. [CONFIG]

**Partial config.** Merge supplied tokens over fallback defaults per-key; a
config missing only `colors.muted` keeps its other values and inherits `#475569`.
Record each inherited key as `[SUPUESTO]` so the gap is auditable. [INFERENCIA]

Required token groups:

```json
{
  "brand": { "name": "", "wordmark": "", "tagline": "" },
  "colors": { "primary": "", "black": "", "white": "", "background": "", "muted": "" },
  "typography": { "display": "", "body": "", "mono": "", "fontLinks": [] },
  "spacing": { "radiusSm": "", "radiusMd": "", "radiusLg": "", "maxWidth": "" }
}
```

## Output Contract

Return exactly one HTML artifact or one Markdown response containing exactly one
fenced `html` block. The HTML must include:

- `<!DOCTYPE html>`, `<html lang="...">`, `<head>`, `<style>`, and `<main>`.
- `<link rel="icon" type="image/svg+xml" href="...">` in `<head>`.
- CSS variables for every brand color and font used.
- Semantic landmarks: `<header>`, `<nav>` when navigation exists, `<main>`,
  `<section>`, and `<footer>`.
- Responsive CSS with at least one `@media` query.
- No unresolved `{{PLACEHOLDER}}` tokens.
- No base64 images.
- No external JavaScript.
- No remote font links unless the supplied config explicitly allows them.
- No current date/time unless `artifact_date` is supplied.
- Favicon must be SVG, square/self-contained, not remote, and not base64.

## Token Rules

- Use CSS variables such as `--brand-primary`, `--brand-bg`, `--brand-black`,
  `--brand-white`, `--brand-muted`, `--font-display`, and `--font-body`.
- Hardcoded hex colors are allowed only inside the `:root` token declaration or
  in the explicit fallback config comment. [CONFIG]
- Reuse token variables everywhere else.
- Fallback defaults are `#2563EB`, `#0F172A`, `#FFFFFF`, `#F8FAFC`, `#475569`,
  and `system-ui`.

## Accessibility And Layout

- Body text contrast must be at least WCAG AA (4.5:1 normal, 3:1 large/bold)
  when deterministically checkable from the resolved hex tokens. If a token is a
  named color or unresolved at check time, record a deterministic limitation
  rather than guessing pass/fail. [CONFIG]
- Use semantic headings in order; never skip a level (`h1`→`h3` fails). [DOC]
- Avoid ALL CAPS headings in markup; use `text-transform: uppercase` so screen
  readers still receive natural casing. [INFERENCIA]
- Include responsive constraints for grids/cards (`minmax`, `flex-wrap`).
- For RTL content set `dir="rtl"` on `<html>` and prefer logical properties
  (`margin-inline-start`, `padding-block`) over physical ones. [CONFIG]

## Worked Example (minimal valid skeleton)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,...">
  <style>
    :root { --brand-primary:#2563EB; --brand-bg:#F8FAFC;
            --brand-black:#0F172A; --font-body:system-ui; }
    body { background:var(--brand-bg); color:var(--brand-black);
           font-family:var(--font-body); }
    .grid { display:grid; gap:1rem; grid-template-columns:1fr; }
    @media (min-width:48rem){ .grid{ grid-template-columns:repeat(3,1fr);} }
  </style>
</head>
<body>
  <header><h1>Title</h1></header>
  <main><section class="grid">…</section></main>
  <footer>…</footer>
</body>
</html>
```

Note the favicon `href` uses an inline SVG data URI (allowed) — not a base64
*image* and not remote. Hex appears only inside `:root`; every consumer uses
`var(--…)`. This skeleton passes the gate. [INFERENCIA]

## Validation Gate (authoritative checklist)

This is the single source of pass/fail; the Output Contract above states the
*shape*, this states the *checks*. Run before delivery; never report green by
default — only when each box is verified. [CONFIG]

- [ ] Brand config or fallback tokens explicitly declared in `:root`.
- [ ] CSS variables present AND referenced (declared-but-unused is a finding).
- [ ] Single-file, self-contained; no external CSS/JS/font/image refs unless config allows.
- [ ] SVG favicon link exists, square, self-contained, not remote, not base64.
- [ ] No base64 images; no `<script src>` or inline `<script>`.
- [ ] No unresolved `{{PLACEHOLDER}}` tokens.
- [ ] Semantic landmarks present (`<header> <main> <footer>`, `<nav>` if nav exists).
- [ ] At least one `@media` query.
- [ ] Heading order unbroken; no markup ALL CAPS.
- [ ] Contrast passes WCAG AA or records a deterministic limitation.
- [ ] No date/time unless `artifact_date` supplied.
- [ ] `bash skills/brand-html/scripts/check.sh` passes (validates valid+invalid fixtures offline). [CÓDIGO]

## Failure Modes (detect → response)

| Symptom | Cause | Response |
|---|---|---|
| Gate flags remote asset | font link / image URL slipped in | strip it, inline or drop; re-run gate. Never ship remote. |
| Contrast indeterminate | token is named color or `var()` chain | record limitation `[SUPUESTO]`, advise browser QA — do not assert pass. |
| Hardcoded hex outside `:root` | literal color in a rule | replace with `var(--…)`; add token to `:root` if new. |
| `{{X}}` survives in output | unsupplied content field | stop `{VACIO_CRITICO}`; ask for the value, never fabricate. |
| Request implies SPA/routing/multi-page | out of scope (see Anti-scope) | decline the out-of-scope part, deliver the single-file subset only. |
| Two valid topics (e.g. html-brand) | ambiguous route | router decides; this playbook assumes brand-html already resolved. [INFERENCIA] |

## Assumptions & Limits

- HTML/CSS only — no SPA, routing, database, DOCX, XLSX, PDF, or slides. [CONFIG]
- External fonts disabled by default; deterministic delivery prefers self-contained
  artifacts. Enabling them trades reproducibility/offline-safety for typography
  fidelity — a deliberate, config-gated choice. [CONFIG]
- Static validation cannot prove rendered fidelity; layout/visual QA still needs
  browser inspection when the user asks for pixel correctness. [CONFIG]
- Contrast gate only covers deterministically resolvable token pairs; gradients,
  overlays, and image-backed text are out of its reach. [INFERENCIA]

## Usage

- `/brand-html landing-page ./brand-config.json`
- `Generate a responsive branded HTML report using these tokens`
- `Create RTL branded HTML for Arabic content`
