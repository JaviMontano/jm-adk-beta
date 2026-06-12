# Acceptance checklist — project-create

Run before declaring a scaffold done. Maps 1:1 to the guardian's gate.

- [ ] Intent non-empty (else `{VACIO_CRITICO}` stop). [DOC]
- [ ] Slug derived and matches `^[a-z0-9]+(-[a-z0-9]+)*$`. [CONFIG]
- [ ] `P-NNN` reserved as next free id; substitution reported if id was taken. [INFERENCE]
- [ ] Target `02_Proyectos/<slug>/` did not pre-exist (else route, do not scaffold). [DOC]
- [ ] `CLAUDE.md` written missing-only and ≤ 70 lines (Rule-9). [DOC]
- [ ] `MEMORY.md` written missing-only; unknown objective = `{POR_CONFIRMAR}`. [DOC]
- [ ] `TAREAS.md` written missing-only with NOW ≤ 3 tasks. [DOC]
- [ ] No pre-existing file modified without a reviewed `--force` diff. [DOC]
- [ ] Registry entry `P-NNN ↔ slug ↔ path` unique and idempotent. [INFERENCE]
- [ ] One Alfa-core tag family used consistently; no prices, no PII, single-brand. [DOC]
- [ ] Summary reports id, slug, path, files written/skipped, gate verdict, next cadence. [INFERENCE]
