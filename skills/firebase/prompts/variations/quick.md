# Quick variation — firebase

Use when `depth=quick`: deliver the essentials for the resolved topic, fast.

## Do
- Resolve ONE topic and read ONE playbook.
- Give the minimal correct answer: the rule snippet, the index entry, the function
  signature, or the config diff that solves the request.
- Keep evidence tags; flag any assumption as `[SUPUESTO]`.

## Skip (defer to deep)
- Exhaustive failure-mode tables, full C4 diagrams, multi-feature cost models.

## Example shape
> Topic: firestore-security-rules (quick). Add an owner-only rule for `notes/{id}`:
> ```
> allow read, write: if request.auth != null
>   && request.auth.uid == resource.data.ownerId;
> ```
> Test allow+deny in the emulator before deploy. [EXPLICIT]

Still required even in quick mode: deny-by-default respected, emulator test named,
no price quoted, single playbook only.
