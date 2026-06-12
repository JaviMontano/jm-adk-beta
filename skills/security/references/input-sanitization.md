<!-- distilled from alfa skills/input-sanitization -->
<!-- > -->
# Input Sanitization

> "Sanitize at the boundary. Trust nothing that crosses it."

## TL;DR

Implements the Constitution VII sanitization default: strip HTML tags from user input before storage — not escape, not allowlist. Native browser APIs (DOMParser) over external libraries. Covers all input contexts: HTML, URL, CSS, JS. Enforces dual-layer validation (client + server). `<script>` and `<style>` tags are removed *with their content*, not just tag-stripped. Rich text fields are the sole exception, requiring explicit justification per Constitution XIV (Simple First). [DOC]

**Decision — strip over escape (trade-off).** Stripping is lossy (a user typing `a < b` loses `< b`) but eliminates a whole class of context-confusion bugs; escaping preserves intent but stays a live XSS vector if the value ever lands in a non-HTML sink (URL, CSS, attribute). For plain-text fields the lossiness is acceptable; that is why rich text is the carved-out exception, not the default. [INFERENCIA]

## Anti-Scope

- Not an output-encoding library: this strips at the *write* boundary. Output sinks still owe context-correct encoding. [DOC]
- Not a WAF, rate limiter, or auth control — orthogonal concerns. [DOC]
- Not SQL/NoSQL injection defense: parameterize queries; stripping HTML does not sanitize query structure. [INFERENCIA]
- Does not cover binary/file-content scanning (malware, polyglots) — only text fields. [SUPUESTO] *Verify: confirm no field stores raw file bytes treated as text.*

## Procedure

### Step 1: Discover
- Inventory all user-input surfaces: forms, URL parameters, `localStorage` reads, `postMessage` handlers, file uploads, **and indirect surfaces** — webhook payloads, imported CSV/JSON, third-party API responses rendered to DOM. [DOC]
- Identify input context for each surface: HTML display, URL parameter, CSS value, JS evaluation, HTML *attribute*, SVG. [DOC]
- Check for existing sanitization patterns in the codebase (`grep -rn "innerHTML\|DOMParser\|dangerouslySetInnerHTML"`). [CODE]
- Identify which inputs need rich text (must be justified per Constitution XIV).

### Step 2: Analyze
- Apply sanitization hierarchy per context:
  - **HTML context** (default): Strip all HTML tags, keep text content. DOMParser-based.
  - **HTML attribute context**: never interpolate raw user data into an attribute; set via `element.setAttribute` with a stripped value, never by string-building markup. [INFERENCIA]
  - **URL context**: `encodeURIComponent()` for values; validate scheme against an allowlist (`https:`/`mailto:`) to block `javascript:` and `data:` URIs. [DOC]
  - **CSS context**: `CSS.escape()` for dynamic values.
  - **JS context**: Never insert user data into JS — use `textContent`, never `innerHTML`.
- For `<script>` and `<style>` tags: remove tags AND their content (not just tag stripping).
- Design server-side mirror: Cloud Functions validate the same rules before Firestore write.
- Rich text exception: if a field requires HTML (e.g., blog editor), justify per XIV and use a restricted allowlist (prefer a vetted sanitizer such as DOMPurify for rich text *only* — the no-external-library rule is waived here because hand-rolling an allowlist sanitizer is the riskier path). [INFERENCIA]

### Step 3: Execute
- Implement client-side strip function using DOMParser:
  ```javascript
  function stripHTML(input) {
    if (typeof input !== 'string') return '';
    const doc = new DOMParser().parseFromString(input, 'text/html');
    // Remove script and style elements entirely (content + tag)
    doc.querySelectorAll('script, style').forEach(el => el.remove());
    return doc.body.textContent || '';
  }
  ```
- Apply to all form submissions before sending to backend.
- Implement server-side validation in Cloud Functions:
  ```javascript
  // Firestore trigger or callable function
  function validateInput(text) {
    if (typeof text !== 'string') throw new Error('Invalid input type');
    // Strip HTML server-side as defense-in-depth.
    // Loop until stable to defeat nested/overlapping tags (see Edge Cases).
    let prev, stripped = text;
    do {
      prev = stripped;
      stripped = prev.replace(/<script[\s\S]*?<\/script>/gi, '')
                     .replace(/<style[\s\S]*?<\/style>/gi, '')
                     .replace(/<[^>]*>/g, '');
    } while (stripped !== prev);
    return stripped.trim();
  }
  ```
- Never use `innerHTML` with user data — always `textContent` or DOMParser.
- Add Firestore security rules that reject documents with HTML tags in text fields.

### Step 4: Validate
- XSS payload test suite (all must be stripped): `<script>alert(1)</script>`, `<img onerror=alert(1)>`, `<svg onload=alert(1)>`, `<scr<script>ipt>alert(1)</script>`, `<a href="javascript:alert(1)">`, malformed `<img src=x onerror=alert(1)//`. [DOC]
- Server-side rejects the same payloads independently of client.
- No `innerHTML` assignments with user-controlled data in codebase (grep verify).
- Rich text fields (if any) use explicit allowlist, not full HTML.
- Both layers (client + server) agree on output for all test payloads (golden-file diff). [INFERENCIA]

## Quality Criteria

- [ ] All user-input surfaces inventoried (including indirect: webhooks, imports, 3rd-party responses)
- [ ] Strip-first default applied (not escape, not allowlist)
- [ ] DOMParser used for client-side stripping (no external libraries, rich-text exception aside)
- [ ] `<script>` and `<style>` removed with content, not just tags
- [ ] Server-side validation mirrors client-side rules and is idempotent under repeated application
- [ ] No `innerHTML` with user data anywhere in codebase
- [ ] XSS payload test suite passes on both client and server (incl. nested-tag and `javascript:` URI cases)
- [ ] Rich text exceptions justified per Constitution XIV
- [ ] Evidence tags applied to all claims

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Escape instead of strip | Escaped HTML still renders in some contexts | Strip tags, keep text only |
| Client-only validation | Bypassable via DevTools or API calls | Always mirror on server |
| External sanitization library (plain text) | Dependency bloat for a solved problem | Use native DOMParser |
| Hand-rolled allowlist for rich text | Sanitizer bypasses are subtle and frequent | Use a vetted lib (DOMPurify) for rich text only |
| Allowlist by default | Maintenance burden, easy to miss patterns | Strip by default, allowlist only for rich text |
| Single-pass regex strip on server | Nested tags (`<scr<script>ipt>`) survive one pass | Loop replace until output is stable |
| Using `innerHTML` with user data | Direct XSS vector | Use `textContent` or DOMParser |
| Allowing any URL scheme | `javascript:`/`data:` URIs execute | Allowlist `https:`/`mailto:` schemes |

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| Mutation XSS (mXSS) | Browser re-parses "clean" markup into live nodes | Strip to text; never round-trip rich HTML through `innerHTML` |
| Client/server drift | Client passes, server stores raw, or vice versa | Shared test vectors; treat server as source of truth |
| Double-encoding | `&amp;lt;script&amp;gt;` decoded later into a tag | Strip on the decoded value, decode-then-strip once |
| Over-stripping | Legitimate `<`, math, code snippets lost | Designate field as rich text and justify per XIV |

## Related Skills

- `security-testing` — Broader security testing including sanitization verification
- `dual-layer-verification` — Static + runtime verification of security invariants
- `form-engineering` — Form UX patterns that integrate sanitization
- `firestore-security-rules` — Server-side rule enforcement

## Usage

Example invocations:

- "/input-sanitization" — Run the full input sanitization workflow
- "input sanitization on this project" — Apply to current context

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs). [DOC]
- Requires English-language output unless otherwise specified. [DOC]
- Assumes a browser runtime exposes `DOMParser`; in Node/SSR contexts the client strip is unavailable — server `validateInput` is then the only enforced layer. [SUPUESTO] *Verify: confirm execution environment per surface.*
- Stripping assumes plain-text intent; any field needing markup must be reclassified as rich text. [INFERENCIA]
- Does not replace domain expert judgment for final decisions. [DOC]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Return empty string (client) / request clarification before proceeding |
| Nested / overlapping tags (`<scr<script>ipt>`) | Server loops replace until stable; DOMParser handles client-side natively |
| `javascript:` / `data:` URI in a link field | Reject via scheme allowlist, not tag strip |
| Non-string input (number, object, null) | Type-guard early; throw server-side, coerce to `''` client-side |
| Unicode/homoglyph tag tricks (`<＜script>`) | Normalize (NFKC) before stripping; DOMParser parses real tags only |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
