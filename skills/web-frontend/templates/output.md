# Frontend Implementation Result — <topic>

## 1. Routing decision
- **Topic resolved:** `<one of the 15 enum values>`
- **Depth:** `quick | deep`
- **Why this topic (disambiguation):** <one line; tag the inference> [INFERENCIA]
- **Playbook loaded:** `references/<topic>.md` (exactly one)
- **Out-of-scope handed off:** <none | named boundary skill>

## 2. Stack confirmed
| Fact | Value | Source |
|------|-------|--------|
| Framework + version | <e.g. React 19 / App Router> | [CONFIG] |
| Bundler | <Vite / Webpack / none> | [CONFIG] |
| Browser targets | <e.g. es2020, no IE11> | [SUPUESTO] |
| Capability caveats | <e.g. no RSC on this SPA> | [INFERENCIA] |

## 3. Decisions & trade-offs
| Decision | Chosen option | Trade-off accepted | Tag |
|----------|---------------|--------------------|-----|
| <from playbook's table> | <option> | <cost> | [INFERENCIA] |

## 4. Implementation
<Code / config produced — files touched, key snippets. Keep scoped to this one topic.>

```
<representative snippet>
```
Effect: <what it changes and why> [CÓDIGO]

## 5. Validation gate report
| Gate | Threshold | Verifier | Evidence | Result |
|------|-----------|----------|----------|--------|
| Single playbook loaded | exactly 1 | review | <ref> | pass/fail |
| Build/run clean | no errors | build cmd | <output> | pass/fail |
| <topic gate, e.g. initial bundle> | << 250KB gz> | `size-limit` | <number> | pass/fail |
| Accessibility (if UI) | WCAG 2.1 AA | axe-core | <0 serious> | pass/fail |
| Lighthouse (if UI) | > 90 all | Lighthouse | <scores> | pass/fail |
| Evidence tags present | 1/claim | review | — | pass/fail |
| Single brand / no PII | true | review | — | pass/fail |

**Verdict:** `pass | fail | blocked` — <if not pass, list the gap; never green-as-success>

## 6. Follow-ups / re-invoke
- <Separate second need that warrants a fresh invocation of a different topic, if any>

---
Evidence taxonomy: `[CÓDIGO]` `[CONFIG]` `[DOC]` `[INFERENCIA]` `[SUPUESTO]` — one per non-obvious claim, no Jarvis mixing. Constitution v6.0.0; script-first.
