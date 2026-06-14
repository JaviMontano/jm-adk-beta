# Meta Prompt — persistent-memory-design

Self-check the design **before** handing it to the guardian. For each item, answer yes/no with the evidence and a tag.

## Activation sanity
- Is this genuinely about a **durable memory artifact** (survives compact, validated conclusions, evidence)? If it's really *which session to resume/fork/restart*, stop and route to `session-lifecycle-management`. [DOC]
- Is the request asking for ephemeral notes, a raw-transcript dump, or a high-churn task queue? If so, this skill does not apply. [DOC]

## Design integrity
- Does the file hold **only validated conclusions** — no raw reasoning, no tool dumps? [DOC]
- Is the schema the **fixed four sections**, identical across sessions? [DOC]
- Does every Finding/Decision carry `[src:<source> @ <date>]`? [DOC]
- Is the read protocol **read-once / reference-after**? If I find a per-turn re-read, the bootstrap is wrong. [INFERENCE]
- Are writes **upsert-by-key**? Any full-file rewrite must be flagged — it breaks the prompt cache. [INFERENCE]
- Does state **reconstruct from the file alone** after `/compact` and reset? [DOC]
- Is the path stable and repo-relative (no `../`)? [INFERENCE]
- If multiple writers exist, is concurrency resolved? [INFERENCE]

## Failure modes to catch
- Hypotheses mixed into Findings (contaminates truth state). [INFERENCE]
- Contradicted finding kept alongside its replacement instead of upserted. [INFERENCE]
- File growing unbounded (resolved Open / stale Findings not pruned). [INFERENCE]

## Output of this pass
A short verdict: ready-for-gate or list of fixes, each with evidence and a tag. Never declare green without backing evidence. Single brand (JM Labs); no invented prices; no client PII.
