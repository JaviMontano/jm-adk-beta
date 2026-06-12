# Meta prompt — integrations router self-check

Use this to audit your own integration work before handing off. The integrations
skill fails quietly when a security control is skipped, so verify, do not assume.

## Routing discipline
- Did I resolve exactly one `topic ∈ enum` and read exactly ONE playbook? If I
  loaded a second "for context," I broke the router — restart. [INFERENCIA]
- If the request named two topics, did I sequence them rather than merge? [SUPUESTO]
- Did I ask before guessing across the security boundary on ambiguity? [SUPUESTO]

## Control completeness (per topic)
- Is signature/origin verification present *before* any payload field is
  trusted? (webhook HMAC raw-body + constant-time + timestamp; reCAPTCHA
  server-side `siteverify` with `action`+`hostname`; payment fulfillment
  webhook-driven.) [DOC]
- Is every money/event path idempotent and replay-safe (dedup on event ID)? [INFERENCIA]
- Are secrets referenced from env/secrets, never inlined or client-side? [CÓDIGO]
- Did I miss the *one* failure that loses money or drops events for this topic?

## Evidence & governance
- Is every non-obvious claim tagged, with no mixed tag families? [CONFIG]
- Did I flag provider-version-dependent facts `[SUPUESTO]` and point back to
  current provider docs? [SUPUESTO]
- Did I halt on any missing required secret as `[VACIO_CRITICO]`? [SUPUESTO]

## Verdict
If any answer is "no," name the failing control and fix it before declaring the
Validation gate passed. Never report green by default.
