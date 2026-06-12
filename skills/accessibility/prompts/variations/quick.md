# Quick Prompt — accessibility (depth=quick)

Fast path for the highest-impact WCAG 2.1 AA criteria only. Use when the user wants
a triage, not an exhaustive pass.

1. **Route** to one topic (audit / design / testing / writing). Load only that
   playbook. Do not load two.
2. **Confirm** target + assumed AA level in one line. If no target/asset, return the
   required-inputs gap list and stop.
3. **Hit the top criteria** for the topic:
   - audit/testing: keyboard operability (2.1.1), focus visible (2.4.7), text
     contrast (1.4.3), name/role/value (4.1.2). Run axe-core if a runnable target
     exists, then a keyboard smoke pass.
   - design: native-first semantics, keyboard map + focus return for the in-scope
     pattern, text/non-text contrast tokens.
   - writing: correct alt treatment by image job, descriptive link text, error copy
     with cause + recovery.
4. **Report** each finding with its WCAG criterion, a one-line fix, and one evidence
   tag. Mark anything untested `not verified`.
5. **Status**: `pass` / `conditional` / `fail` / `not verified`. Never call a clean
   scan "accessible". Flag that this was a quick pass, not full conformance.
