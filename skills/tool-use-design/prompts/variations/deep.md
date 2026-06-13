# Deep Variation — Tool Use Design

Full treatment for a large or three+-tool surface with structural overlap.

## Do

1. **Map responsibilities** across all tools; if three+ overlap, redefine the axis (discover / read / mutate) rather than splitting pairwise.
2. **Author each contract** with purpose · input format · output shape · 2 invocation examples · reciprocal boundary, and cross-link every competing pair bidirectionally.
3. **Resolve every overload** with `rename_split`; record the rename rationale tied to the new axis. [INFERENCIA]
4. **Measure the repo** before adopting any read strategy: estimate Grep hit counts and token load; confirm `read_all` is rejected by data, not just by rule. [SUPUESTO]
5. **Specify Edit safety in depth**: unique-anchor requirement, anchor-expansion step on first failure, `read_write_full_rewrite` as terminal fallback. [CÓDIGO]
6. **Reference policy assets** explicitly: `assets/description-contract-policy.json`, `assets/boundary-policy.json`, `assets/repo-strategy-policy.json`, `assets/edit-safety-policy.json`, `assets/anti-pattern-policy.json`, `assets/tool-use-contract.json`.
7. **Run both offline validators** and attach the gate checklist mapping each criterion to its evidence tag.

## Gate (full)

All acceptance criteria in `SKILL.md` plus a documented token measurement justifying the read strategy. One Alfa-core tag family throughout. [DOC]
