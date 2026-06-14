# Pre-Close Checklist — Tool Use Design

Run this before declaring a routing-contract report done. Each item maps to one Alfa-core evidence tag.

- [ ] Every description declares input format + output shape + 1–2 examples + reciprocal boundary. [DOC]
- [ ] Overloading resolved with rename + split, not a paragraph. [DOC]
- [ ] Competing tools delegate bidirectionally (no one-way mention). [DOC]
- [ ] Repo strategy is `Grep → Read → Edit`; no `Glob("**/*") + Read all` upfront. [DOC]
- [ ] `read_all_upfront=false` and `glob_all_then_read_all=false`. [DOC]
- [ ] `Edit` failure mode documented: `unique_anchor_required=true`, fallback `read_write_full_rewrite`. [CÓDIGO]
- [ ] Determinism flags set: `offline=true`, `network_required=false`, `deterministic=true`. [DOC]
- [ ] All evidence tags belong to one Alfa-core family. [CONFIG]
- [ ] No client PII, no invented prices, single brand. [CONFIG]
