# Example input — market-intel

A concrete request that exercises routing to `partnership-strategy` at
`depth=quick`.

---

> We run a B2B methodology product (MetodologIA) sold to mid-market delivery
> teams. I want to extend reach through co-marketing. Score these three
> candidates and tell me which to pursue, with kill criteria:
>
> 1. **Agile-coaching newsletter** — 8,000 subscribers, same ICP (delivery
>    leads), no product overlap.
> 2. **BI consultancy** — sells dashboards to data teams; partial ICP overlap,
>    adjacent offer.
> 3. **A competing PM tool** — same ICP, directly competing product.
>
> Don't give me dollar commissions — just the structure. Quick pass is fine.

---

## Why this routes to `partnership-strategy`

- Cue words: "co-marketing", "score candidates", "which to pursue", "kill
  criteria" → partner qualification, not positioning or pricing. [INFERENCIA]
- Unambiguous: no second topic contends, so the router proceeds without asking. [INFERENCIA]
- `depth=quick`: user said "quick pass" → deliver the fit-score table only,
  defer full program design. [CONFIG]
- Governance trip-wire embedded: "don't give me dollar commissions" — reward
  shape must be expressed as structure, never figures. [CONFIG]
