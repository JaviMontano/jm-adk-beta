# Example Input — ai-quality

A near-collision request that the router must disambiguate, not guess.

## User request

> "We just had Claude write a batch of pytest cases for our `pricing/discount.py`
> module, and separately we want to know whether the model's generated
> docstrings in that same PR are actually AI-written boilerplate or hand-edited.
> Can the quality skill handle both? Stakes are moderate — this ships to staging
> Friday, not prod."

## Attached context

- Diff: `pricing/discount.py` (+18 / -2) plus a new `tests/test_discount.py`
  (+64) with 7 generated test cases.
- The generated docstrings under question are in `pricing/discount.py` lines
  10–22 and 40–55.
- No coverage baseline recorded yet for `pricing/`.
- Requested `depth`: not stated.

## Why this is a routing test

The request bundles **two** distinct intents that map to **two different
topics**:
1. "Claude wrote pytest cases … is the test set good?" → AI *generates/justifies*
   tests → `ai-assisted-testing`.
2. "are the docstrings AI-written boilerplate or hand-edited?" → AI-generation
   *likelihood* of content → `ai-content-detection`.

The router must NOT load both playbooks at once into one answer. The correct
behavior is to resolve the **primary** topic, state the second as a follow-up
route, and pick `depth=quick` from the "moderate, staging-not-prod" stakes
signal. The example output shows that resolution.
