<!-- distilled from alfa skills/search-ux -->
<!-- > -->
# Search Ux
> "Method over hacks."
## TL;DR
Search-bar, autocomplete, faceted filtering, zero-results, and ranking patterns for product search UIs. [DOC]
Scope: UX of the search *interface*. Out of scope: relevance-ranking algorithms, index/infra, NLP query parsing — flag those to engineering. [SUPUESTO]

## Procedure
### Step 1: Discover
- Capture query corpus, intent mix (navigational/informational/transactional), result-set size, and device split before designing. [DOC]
### Step 2: Analyze
- Pick patterns per Constitution XIII/XIV; justify each against the trade-offs table below. [DOC]
### Step 3: Execute
- Implement with evidence tags; cover the four failure modes (empty, slow, zero-results, ambiguous). [DOC]
### Step 4: Validate
- Verify against Quality Criteria and Acceptance Criteria. [DOC]

## Core patterns
- **Search bar**: always-visible on search-first products; collapsed icon only when search is secondary. Placeholder states scope ("Search orders"), never instructions. [INFERENCIA]
- **Autocomplete**: debounce 150–300ms; show after ≥2 chars; cap ~8 suggestions; keyboard-navigable (↑↓/Enter/Esc); highlight the matched substring, not the whole row. [DOC]
- **Faceted search**: facets reflect the *current* result set with live counts; multi-select within a facet = OR, across facets = AND; never show a facet that yields zero results. [INFERENCIA]
- **Filters vs. search**: filters narrow a known set (structured); search explores an unknown set (free text). Don't force one to do the other's job. [INFERENCIA]
- **Zero results**: never a dead end — show why, relax the narrowest filter, and offer 2–3 recovery paths (spelling, broaden, popular items). [DOC]

## Decisions & trade-offs
| Decision | Choose when | Trade-off |
|----------|-------------|-----------|
| Instant (as-you-type) results | Small/medium indexed set, low latency | Request volume, flicker; needs debounce + cancel-in-flight [INFERENCIA] |
| Submit-on-Enter | Large set, expensive query | Slower perceived feedback [INFERENCIA] |
| Faceted sidebar | >~20 results, structured attributes | Screen real estate; weak on mobile [SUPUESTO] |
| Single relevance sort | Sparse/varied metadata | Users can't reorder by price/date [INFERENCIA] |

## Quality Criteria
- [ ] Evidence tags applied (Alfa core set; one tag per claim) [DOC]
- [ ] Constitution-compliant (XIII/XIV)
- [ ] Actionable output
- [ ] All four failure modes handled (empty / latency / zero-results / ambiguous query)
- [ ] Keyboard + screen-reader path verified (combobox/listbox ARIA roles) [DOC]

## Usage
Example invocations:
- "/search-ux" — Run the full search ux workflow
- "search ux on this project" — Apply to current context

## Assumptions & Limits
- Assumes access to project artifacts (code, docs, configs) and a representative query log. [SUPUESTO]
- English-language output unless otherwise specified. [SUPUESTO]
- Does not replace domain-expert judgment for final ranking/relevance decisions. [SUPUESTO]
- Covers UI/interaction only; relevance tuning and search infra are out of scope. [SUPUESTO]

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification; show recent/popular searches instead of a blank panel |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request (ranking/infra) | Redirect to engineering or appropriate skill |
| Zero results | Explain cause, auto-relax narrowest filter, offer spelling + broaden paths |
| Slow backend (>1s) | Skeleton/loading state + cancel-in-flight; keep prior results visible |
| Ambiguous / typo'd query | Did-you-mean + best-effort results, never a hard empty state |
