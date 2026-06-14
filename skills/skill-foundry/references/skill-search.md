<!-- distilled from alfa skills/skill-search -->
<!-- > -->
# Skill Search

> "Method over hacks. Evidence over assumption."

## TL;DR

BM25 full-text search over `PRISTINO-INDEX.md` skill names + descriptions, returning ranked candidates. Orchestration-layer skill used internally by Pristino and the adk-orchestrator to route a request to the right skill — it does NOT execute the matched skill. Protocol details in `PRISTINO.md`. [EXPLICIT]

## What it does / does not do

- DOES: rank existing indexed skills by lexical relevance to a query; return top-N with scores + confidence. [EXPLICIT]
- DOES NOT: invoke the chosen skill, create new skills, or do semantic/embedding search (BM25 is lexical only). [EXPLICIT]
- DOES NOT: search arbitrary files — scope is the index, not the repo. [EXPLICIT]

## Procedure

### Step 1: Discover
- Take the query string + any caller-supplied context (active brand, working dir). [EXPLICIT]
- Load `PRISTINO-INDEX.md`; abort with a clear error if missing or empty (see Edge Cases). [EXPLICIT]

### Step 2: Analyze (rank)
- BM25 over the `name` + `description` fields of each index entry. [EXPLICIT]
- Tie-break by name match > description match, then by index order (stable). [EXPLICIT]
- Map raw BM25 score to confidence; gate per Constitution XIII/XIV. [EXPLICIT]

### Step 3: Execute (return)
- Emit ranked top-N (default 5) as `{rank, slug, score, confidence}`; never auto-run the winner. [EXPLICIT]
- Tag every returned claim with an evidence marker. [EXPLICIT]

### Step 4: Validate
- Confirm top candidate confidence >= 0.95; if below, return candidates flagged "low confidence — confirm before routing". [EXPLICIT]

## Scoring & acceptance criteria

- [ ] Index loaded and parsed; entry count > 0. [EXPLICIT]
- [ ] Results sorted descending by score; deterministic for identical query + index. [EXPLICIT]
- [ ] Each result carries score, confidence, and an evidence tag. [EXPLICIT]
- [ ] Top confidence >= 0.95 OR explicitly flagged as low-confidence. [EXPLICIT]
- [ ] Output is candidate list only — no skill executed as a side effect. [EXPLICIT]

## Related Skills

- See `PRISTINO.md` for the full orchestration protocol (routing, handoff to the matched skill).

## Usage

- "/skill-search <query>" — rank indexed skills for the query.
- "skill search on this project" — rank using current working-dir context as the query.

Worked example: query `"redact PII from a PDF"` → top result `{rank:1, slug:"pii-redaction", score:8.7, confidence:0.97}` [EXPLICIT]; caller (Pristino) then decides whether to invoke it. A near-tie (e.g. two PDF skills within ~0.5 BM25) returns both so the router disambiguates.

## Assumptions & Limits

- Assumes `PRISTINO-INDEX.md` is current; stale index → stale matches (no freshness check here). [EXPLICIT]
- Lexical BM25 only: synonyms and paraphrases score poorly (query "remove" won't match description "strip"). [SUPUESTO]
- English-language index + query unless otherwise specified. [EXPLICIT]
- Ranking is advisory; final routing/expert judgment stays with the caller. [EXPLICIT]

## Edge Cases & failure modes

| Scenario | Handling |
|----------|----------|
| Empty / minimal query | Request clarification before ranking — BM25 on <2 tokens is noise. [EXPLICIT] |
| Index missing or empty | Hard error: "PRISTINO-INDEX.md absent/empty — cannot search"; do not fall back to repo scan. [EXPLICIT] |
| No entry scores above threshold | Return empty set + "no confident match"; never invent a slug. [EXPLICIT] |
| Top-2 within tie-break margin | Return both, mark "ambiguous — caller disambiguates". [EXPLICIT] |
| Conflicting context vs query | Surface conflict explicitly; rank on the query, note the override. [EXPLICIT] |
| Out-of-scope (wants execution/creation) | Redirect: search ranks, `PRISTINO.md` routes, skill-foundry creates. [EXPLICIT] |
