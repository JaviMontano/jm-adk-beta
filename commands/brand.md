---
name: brand
description: "Branded output: /brand <html|docx|xlsx|folio> <source.md> — MetodologIA DS tokens from references/brand/"
argument-hint: "<format> <source>"
---
# /brand

Wrapper over `skills/brand-output` router (topic=format). Tokens: `references/brand/design-tokens.json`. [DOC]

**Contract.** Input: `<format>` ∈ {html, docx, xlsx, folio}; `<source>` = readable `.md` path. Output: branded artifact beside source. [EXPLICIT]
**Gate (brand FIRST).** Resolve MetodologIA BEFORE rendering — never mix two brands in one artifact; ask if unstated. [EXPLICIT]
**Preconditions.** `<source>` exists; format is supported; tokens file resolves. On any miss → halt with the failing check, do not partial-render. [INFERENCE]
**Anti-scope.** No price/cost figures. No green as a success signal in samples. No client personal data. Single brand per call. [EXPLICIT]
**Acceptance.** Artifact uses only `design-tokens.json` values (no hardcoded hex/fonts); declared brand matches gate; cross-refs and code blocks preserved verbatim. [INFERENCE]
**Edge cases.** Unknown format → list the four and halt. Missing source → halt. Brand ambiguous → ask. Token key absent → fail loud, never substitute a default color. [ASSUMPTION]
