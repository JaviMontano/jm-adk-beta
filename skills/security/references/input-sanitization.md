<!-- distilled from alfa skills/input-sanitization -->
<!-- > -->
# Input Sanitization

> "Sanitize at the boundary. Trust nothing that crosses it."

## TL;DR

Implements the Constitution VII sanitization default: strip HTML tags from user input before storage — not escape, not allowlist. Uses native browser APIs (DOMParser) over external libraries. Covers all input contexts: HTML, URL, CSS, JS. Enforces dual-layer validation (client + server). `<script>` and `<style>` tags are removed with their content, not just tag-stripped. Rich text fields are the exception, requiring explicit justification per Constitution XIV (Simple First). [EXPLICIT]

## Procedure

### Step 1: Discover
- Inventory all user-input surfaces: forms, URL parameters, `localStorage` reads, `postMessage` handlers, file uploads
- Identify input context for each surface: HTML display, URL parameter, CSS value, JS evaluation
- Check for existing sanitization patterns in the codebase
- Identify which inputs need rich text (must be justified per Constitution XIV)

### Step 2: Analyze
- Apply sanitization hierarchy per context:
  - **HTML context** (default): Strip all HTML tags, keep text content. DOMParser-based
  - **URL context**: `encodeURIComponent()` for values, validate URL structure
  - **CSS context**: `CSS.escape()` for dynamic values
  - **JS context**: Never insert user data into JS — use `textContent`, never `innerHTML`
- For `<script>` and `<style>` tags: remove tags AND their content (not just tag stripping)
- Design server-side mirror: Cloud Functions validate the same rules before Firestore write
- Rich text exception: if a field requires HTML (e.g., blog editor), justify per XIV and use a restricted allowlist

### Step 3: Execute
- Implement client-side strip function using DOMParser:
  ```javascript
  function stripHTML(input) {
    const doc = new DOMParser().parseFromString(input, 'text/html');
    // Remove script and style elements entirely
    doc.querySelectorAll('script, style').forEach(el => el.remove());
    return doc.body.textContent || '';
  }
  ```
- Apply to all form submissions before sending to backend
- Implement server-side validation in Cloud Functions:
  ```javascript
  // Firestore trigger or callable function
  function validateInput(text) {
    if (typeof text !== 'string') throw new Error('Invalid input type');
    // Strip HTML server-side as defense-in-depth
    const stripped = text.replace(/<script[\s\S]*?<\/script>/gi, '')
                        .replace(/<style[\s\S]*?<\/style>/gi, '')
                        .replace(/<[^>]*>/g, '');
    return stripped.trim();
  }
  ```
- Never use `innerHTML` with user data — always `textContent` or DOMParser
- Add Firestore security rules that reject documents with HTML tags in text fields

### Step 4: Validate
- XSS payload test suite: `<script>alert(1)</script>`, `<img onerror=alert(1)>`, `<svg onload=alert(1)>` — all stripped
- Server-side rejects the same payloads independently of client
- No `innerHTML` assignments with user-controlled data in codebase (grep verify)
- Rich text fields (if any) use explicit allowlist, not full HTML
- Both layers (client + server) agree on output for all test payloads

## Quality Criteria

- [ ] All user-input surfaces inventoried
- [ ] Strip-first default applied (not escape, not allowlist)
- [ ] DOMParser used for client-side stripping (no external libraries)
- [ ] `<script>` and `<style>` removed with content, not just tags
- [ ] Server-side validation mirrors client-side rules
- [ ] No `innerHTML` with user data anywhere in codebase
- [ ] XSS payload test suite passes on both client and server
- [ ] Rich text exceptions justified per Constitution XIV
- [ ] Evidence tags applied to all claims

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Escape instead of strip | Escaped HTML still renders in some contexts | Strip tags, keep text only |
| Client-only validation | Bypassable via DevTools or API calls | Always mirror on server |
| External sanitization library | Dependency bloat for a solved problem | Use native DOMParser |
| Allowlist by default | Maintenance burden, easy to miss patterns | Strip by default, allowlist only for rich text |
| Using `innerHTML` with user data | Direct XSS vector | Use `textContent` or DOMParser |

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

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
