# Meta prompt — agent-orchestration

Use this to self-audit a routing decision before executing, or to grade another
agent's orchestration run. [DOC]

## Routing audit questions

1. **Single match?** Does the request map to exactly one topic under the
   narrowest-match rule, or do two routes genuinely tie? If tied → ask, don't
   guess. [ASSUMPTION]
2. **In enum?** Is the chosen topic one of the 10 enum values? An invented topic
   is rejected by the catalog parser. [CONFIG]
3. **One playbook?** Was exactly one `references/*.md` loaded, not the cluster? [CONFIG]
4. **Right altitude?** Is this actually orchestration, or a single-agent /
   content / domain task that should route elsewhere? [INFERENCE]

## Execution audit questions

5. **Spine complete?** Did Discover → Analyze → Execute → Validate all run? [DOC]
6. **Script-first?** If the topic ships a deterministic check, was it run rather
   than hand-asserted? [CONFIG]
7. **Trade-off recorded?** Is the rejected option documented (so resume/audit
   does not re-litigate)? [INFERENCE]

## Governance audit questions

8. **Tags.** Every non-obvious claim tagged, single core-set family, EN/ES
   consistent? [DOC]
9. **Constitution v6.0.0** enforcement applied? [CONFIG]
10. **No false green** — no gate declared "passed" before the Guardian pass? [DOC]
11. **No invented prices, no client PII, single brand?** [DOC]

## Verdict

Emit PASS / PARTIAL / BLOCK with the first failing question cited. Treat a
green positive run alone as insufficient. [DOC]
