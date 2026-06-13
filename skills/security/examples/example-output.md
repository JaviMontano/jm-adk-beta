# Example output — security router (audit-security, deep)

## Routing
- **Resolved topic**: audit-security
- **Route loaded**: references/audit-security.md (exactly one)
- **Depth**: deep
- **Disambiguation note**: "audit existing code" → `audit-security`, not
  `testing` (no tests requested) and not `architecture` (single file, not posture). [INFERENCE]

## Scope
- **In scope**: `hooks/post-commit.sh` (the one supplied file).
- **Out of scope**: rest of the repo — not supplied; read-only, no mutation. [EXPLICIT]

## Findings
All six categories executed in canonical order; only non-empty rows shown.

| ID | Category | Severity | Status | Path:Line | Evidence | Tag |
|----|----------|----------|--------|-----------|----------|-----|
| SEC-001 | secret_exposure | INFO | placeholder | hooks/post-commit.sh:2 | comment token `<YOUR_TOKEN>` — example placeholder | [CODE] |
| SEC-002 | secret_exposure | CRITICAL | confirmed | hooks/post-commit.sh:5 | live-looking `ghp_aB3d…bCd` in an executed `curl` (masked) | [CODE] |
| SEC-003 | hook_injection | CRITICAL | confirmed | hooks/post-commit.sh:4 | `eval "$USER_INPUT"` runs unsanitized argument | [CODE] |
| SEC-004 | external_network | INFO | review | hooks/post-commit.sh:5 | outbound `https://api.example.com/notify` | [DOC] |

Categories with zero findings (still reported): `path_security`,
`sensitive_files`, `script_safety`. [EXPLICIT]

## False-positive notes
- SEC-001: `<YOUR_TOKEN>` is a placeholder in a comment, not a live secret →
  INFO/`placeholder`, never CRITICAL. [EXPLICIT]

## Remediation plan
| Finding ID | Action | Layer | Tag |
|-----------|--------|-------|-----|
| SEC-002 | Remove the hardcoded token; read it from an environment secret at runtime and rotate the exposed key. | config | [DOC] |
| SEC-003 | Replace `eval` with an explicit allowlist dispatch; quote and validate `$1` before use. | static | [DOC] |

## Verification evidence
- Static (Layer 1): `grep -rPl '(ghp_[0-9a-zA-Z]{36})' hooks/` → 1 hit (line 5);
  `grep -n 'eval ' hooks/post-commit.sh` → line 4. [CODE]
- Runtime (Layer 2): skipped — no served target for a shell hook; recorded as
  skipped, not passed. [DOC]
- Validator: `python3 -B scripts/validate_security_report.py …` → exit 0
  (structure conformant; not a safety all-clear). [CODE]

## Coverage
- Files scanned: `hooks/post-commit.sh` (1).
- Files skipped: none supplied beyond the target.

## Quality gate
- [x] One route, one playbook
- [x] All claims tagged (Alfa core set)
- [x] Placeholder kept INFO; live token CRITICAL — severity by context
- [x] IDs ascending/gapless; Summary (2 CRITICAL, 2 INFO) == Findings; no orphan remediation
- [x] No green-as-success; target unmodified; no exploit produced
- [x] No unresolved {VACIO_CRITICO}

## Go / No-Go
**Decision**: NO-GO — two CRITICAL findings (exposed live token, `eval`
injection) must be remediated and the key rotated before publish. [DOC]
