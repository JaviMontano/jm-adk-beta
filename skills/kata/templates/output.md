# Kata Application — <topic>

## 1. Routing decision

- **Resolved topic**: `<topic>` (one of the 30 `routes:` keys). [DOC]
- **Why this kata**: <the failure mode in the request that this kata prevents>. [INFERENCIA]
- **Rejected alternatives**: <competing keys and why they don't fit>. [DOC]
- **Depth**: `quick` | `deep`.
- **Playbook read**: `references/<topic>.md` (exactly one). [DOC]

## 2. Problem (failure mode)

<State the concrete failure the request exhibits, mapped to the kata's
"Por qué importa" section.> [INFERENCIA]

## 3. Correct pattern applied

```
<Instantiate the playbook's correct pattern for this request — code/config/prompt.>
```
[CÓDIGO]

## 4. Anti-pattern removed

```
<The improvised/incorrect approach the kata replaces, and the failure it caused.>
```
[DOC]

## 5. Edge cases addressed

| Edge case (from playbook) | How this case handles it | Tag |
|---|---|---|
| <case> | <handling> | [DOC] |

## 6. Out-of-scope (neighboring katas)

- <concern> → defer to `<neighboring-kata>`; not absorbed here. [DOC]

## 7. Acceptance checklist (playbook + router)

- [ ] Exactly one playbook read; topic matches user intent. [DOC]
- [ ] Output follows the playbook's structure, not improvised prose. [DOC]
- [ ] Every acceptance criterion in `references/<topic>.md` is met. [DOC]
- [ ] One Alfa-core tag per non-obvious claim; no mixed families. [DOC]
- [ ] Every `[SUPUESTO]` paired with a verification step. [DOC]
- [ ] Script-first honored; no invented prices; no client PII; single brand. [DOC]

## 8. Evidence log

- <claim> — <tag> — <source: playbook section / repo file>.
