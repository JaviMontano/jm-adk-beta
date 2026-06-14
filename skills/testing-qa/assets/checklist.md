# testing-qa — Routing & Gate Checklist

Run top-to-bottom before declaring a testing-qa deliverable done.

## Route (pick one)
- [ ] Single named test type → that topic.
- [ ] "Where to invest / what to test" → `test-strategy`.
- [ ] Spec-first Given/When/Then driving a browser → `bdd-full-spectrum` (not e2e).
- [ ] Load / latency / throughput → `performance-testing` (even if framed "E2E under load").
- [ ] "Increase coverage", no type named → `unit-testing`.
- [ ] Exactly ONE playbook Read; ambiguous two-enum tie → asked once.

## Scope
- [ ] Concrete target named (repo path / route / URL / FR-SC spec).
- [ ] No runnable target → gap report, not a hypothetical test.
- [ ] Assertion routed to the cheapest layer that catches the bug.

## Spine
- [ ] Discover, Analyze, Execute, Validate all present.
- [ ] `depth` respected (quick = essentials, deep = exhaustive).
- [ ] Validate step RAN, with command output attached.

## Evidence & gate
- [ ] Every non-obvious claim has one tag, single family.
- [ ] Thresholds from baseline/standard (CrUX p75, >=80% diff), not guessed.
- [ ] CI gate verified to BLOCK on breach (not warn).
- [ ] Green not asserted as success without evidence; flake quarantined, not retried green.

## Governance
- [ ] No client PII; no invented prices; single brand.
