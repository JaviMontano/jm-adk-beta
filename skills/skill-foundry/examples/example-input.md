# Example input

A user message arriving at skill-foundry:

> "We just finished reworking our `cold-call-prep` skill. Can you take it all the
> way to production for me — run the audit, fix what's broken, and give me a
> shippable verdict — and prove the quality actually went up versus the old
> version?"

Foundry-relevant signals:
- **Asset kind:** skill.
- **Action:** production-ize end-to-end ("audit, fix, shippable verdict") +
  prove a quality gain ("versus the old version").
- **Depth:** deep — multi-step, must withstand a ship/no-ship decision.
- **Target:** `./skills/cold-call-prep`.

This is the classic tie-break between `assembly-skill`, `x-ray-skill`, and
`certify-skill`. The phrase "all the way to production" + "fix what's broken"
means the full pipeline, not audit-only or certify-only. The "prove quality went
up versus old version" is a benchmark concern that `assembly-skill` can fold in,
so it stays a single route rather than splitting. [INFERENCE]
