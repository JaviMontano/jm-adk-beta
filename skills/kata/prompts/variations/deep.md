# Prompt — Deep variation (depth=deep)

Exhaustive path: apply the kata fully and verify at every step.

1. **Resolve `topic`** and state explicitly why the competing keys were rejected. [INFERENCIA]
2. **Read only `references/<topic>.md`** in full — mental model, correct pattern,
   anti-pattern, scope/anti-scope, edge cases, acceptance criteria. No second
   playbook. [INFERENCIA]
3. **Precondition check.** Confirm the playbook's assumptions actually hold for the
   request. If not, STOP and re-route — do not force-fit. [INFERENCIA]
4. **Apply exhaustively**:
   - Instantiate the correct pattern for the request (code/config). [CÓDIGO]
   - Remove the anti-pattern and explain the failure it caused. [DOC]
   - Walk EVERY edge case in the playbook and state how this case handles it. [DOC]
   - Note neighboring katas for out-of-scope concerns instead of absorbing them. [DOC]
5. **Verify at each step** against the playbook's acceptance criteria, item by item;
   pair every `[SUPUESTO]` with a concrete verification step. [DOC]
6. **Full validation gate** (router + playbook criteria + evidence + constitution). [DOC]

Output: a complete filled `templates/output.md` with the edge-case walkthrough and
the per-criterion acceptance table. [DOC]
