# Deep Variation — persistent-memory-design

Full design for a long, multi-session, multi-writer investigation where the memory artifact is load-bearing.

## Elaborate every dimension

1. **File contract & path safety**
   - Stable repo-relative path; justify rejection of any `../` escape and cross-repo sharing.
   - Bootstrap behavior when the file is absent (empty state → create skeleton, not an error).

2. **Schema semantics (depth)**
   - Precise admission rules per section; how a claim is promoted Hypotheses → Findings on validation, and demoted on contradiction.
   - Decisions as the contradiction ledger: replace-by-key + log the change; never keep both versions.

3. **Read-once architecture**
   - Bootstrap loader: parse to cached state, set `scratchpad_loaded`, reference thereafter.
   - Explain the prompt-cache mechanics: why re-reading and full rewrites invalidate the cache prefix.

4. **Idempotent write layer**
   - Stable-key scheme per finding; upsert semantics; refusal to write Findings without provenance.

5. **Survival & reconstruction**
   - Concrete `/compact`-and-reset test: reconstruct from file alone, assert equality with pre-compact state.
   - What it means if the agent asks for data that lived only in the conversation (entry filter failed).

6. **Concurrency**
   - Multi-writer policy: upsert order (last-by-key wins) vs simple lock; no blind text merge.

7. **Bounded growth**
   - Pruning resolved Open, collapsing stale Findings; the file is state, not a log.

8. **Acceptance gate**
   - Walk the full validation checklist, each item with evidence; produce the JSON design report and pass `scripts/check.sh`.

Every claim tagged `[DOC]/[CONFIG]/[INFERENCE]/[SUPUESTO]`. Single brand (JM Labs); no invented prices; no client PII. Use `templates/output.md`.
