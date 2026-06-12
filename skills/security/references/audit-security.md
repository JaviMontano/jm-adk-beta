<!-- distilled from alfa skills/audit-security -->
<!-- > -->
# Audit Security

Performs a read-only static security audit of plugin artifacts. Output is a
severity-classified report with exact file evidence, false-positive handling,
remediation actions, coverage, and validator-backed structure. [EXPLICIT]

Scope boundary: static pattern inspection of supplied files only. No runtime
execution, no exploitation, no network egress, no file mutation. [EXPLICIT]

## Deterministic Assets

Read these local files before producing or reviewing a security report:

| Path | Use |
|---|---|
| `assets/activation-policy.json` | Activation, clarification, false-positive, and refusal routing |
| `assets/scan-policy.json` | Six scan categories, severities, statuses, and placeholder policy |
| `assets/report-contract.json` | Required report sections and fields |
| `assets/evidence-policy.json` | Evidence and remediation requirements |
| `references/security-patterns.md` | Human-readable security pattern catalog |
| `scripts/validate_security_report.py` | Offline JSON report validator |
| `scripts/check.sh` | Deterministic positive and negative fixture check |

The validator reads only local JSON files. It does not call the network,
current time, random sources, model providers, or MCP tools. [EXPLICIT]

Asset precedence: when this playbook and an asset JSON disagree, the asset is
authoritative (it is what the validator enforces); fix the playbook, not the
report. [EXPLICIT]

## When To Activate

Activate when the user asks to audit, scan, review, or check a plugin, skill
bundle, hook directory, or explicit file list for security issues. [EXPLICIT]

Do not activate for generic cybersecurity advice, code review, factuality
review, content quality, legal compliance, or non-plugin application security
unless the user supplies a static plugin/file target. [EXPLICIT]

Refuse requests to exploit, weaponize, exfiltrate, or bypass security controls.
A refusal still returns the read-only audit if a valid target was supplied;
refuse only the offensive action, not the scan. [EXPLICIT]

If no target path or file list is supplied, ask for `plugin_root_or_file_list`
instead of inventing a scope. [EXPLICIT]

Edge routing [EXPLICIT]:
- Empty directory or all-skipped target: still emit the full report with zero
  findings and a Coverage section listing why each file was skipped.
- Mixed request ("audit and fix"): perform the audit; surface remediation as a
  plan only — never apply edits (see Assumptions & Limits).
- Target partly outside the supplied root: scan in-scope files, list the rest
  under Coverage as skipped with reason `out_of_scope`.

## Scan Taxonomy

Execute exactly these six categories from `assets/scan-policy.json`, always in
this canonical order:

1. `secret_exposure`
2. `path_security`
3. `hook_injection`
4. `sensitive_files`
5. `script_safety`
6. `external_network`

Every report must list all six categories, even when a category has zero
findings (emit it with an empty finding set, not by omission). [EXPLICIT]

## Severity Policy

Use only `CRITICAL`, `WARNING`, and `INFO`. No other labels are valid. [EXPLICIT]

- `CRITICAL`: live secret exposure, parent-directory traversal in executable
  context, hook command injection, sensitive credential files, or unvalidated
  executable downloads.
- `WARNING`: hardcoded absolute user paths, or unsafe script posture that does
  not directly expose credentials or execute untrusted input.
- `INFO`: placeholders, documentation-only examples, metadata URLs, or manual
  review notes.

Placeholder/example secrets such as `<YOUR_TOKEN>`, `${API_KEY}`,
`sk-REPLACE_ME`, and `AKIAEXAMPLE` must be `INFO` with status `placeholder`,
not `CRITICAL`. [EXPLICIT]

Classification decisions and trade-offs [EXPLICIT]:
- Severity is keyed on *exploitable context*, not pattern shape: a token-shaped
  string in a `.md` code fence labeled as an example is INFO; the same string in
  an executed `.sh` or a committed `.env` is CRITICAL.
- Bias toward INFO + false-positive note over a wrong CRITICAL. Rationale: a
  noisy CRITICAL erodes trust in the whole report and gets the audit dismissed;
  a missed-but-noted item is recoverable on the next pass.
- A path with `..` that never reaches a shell/exec sink is WARNING, not
  CRITICAL — traversal severity requires an executable context.

Decision table:

| Signal | Context | Severity | Status |
|---|---|---|---|
| Real-looking secret | executed script / committed env | CRITICAL | `confirmed` |
| Real-looking secret | doc/example fence | INFO | `placeholder` |
| Placeholder token | anywhere | INFO | `placeholder` |
| `..` traversal | shell/exec sink | CRITICAL | `confirmed` |
| `..` traversal | data path only | WARNING | `confirmed` |
| Hardcoded `/Users/<name>/…` | any | WARNING | `confirmed` |
| Outbound URL | metadata/doc only | INFO | `review` |

## Procedure

1. Confirm activation with `assets/activation-policy.json`.
2. Confirm the target root or explicit file list is inside the requested scope.
3. Execute all six scan categories with static inspection only.
4. For every finding, record stable ID `SEC-NNN`, category, severity, status,
   path, line, pattern, evidence, and remediation.
5. Redact live secrets in prose evidence (mask the middle, keep prefix/suffix);
   preserve enough pattern context for remediation. [EXPLICIT]
6. Add remediation plan entries for every `CRITICAL` and `WARNING` finding.
7. Add false-positive notes for placeholders and documentation-only examples.
8. Report coverage: files scanned, files skipped (with reason), and scan scope.
9. Validate JSON reports with `scripts/validate_security_report.py` when a
   machine-readable artifact is produced.

Determinism rule: same inputs must yield the same IDs, ordering, and counts.
Assign `SEC-NNN` by ascending category order, then ascending (path, line). Do
not reorder by severity. [EXPLICIT]

## Output Contract

Markdown output must include these sections, in this order:

1. `Summary`
2. `Categories Executed`
3. `Findings`
4. `False Positive Notes`
5. `Remediation Plan`
6. `Coverage`
7. `Warnings`

JSON output must match `assets/report-contract.json`. [EXPLICIT]

Worked example (Findings row + matching remediation entry):

```text
SEC-003  hook_injection  CRITICAL  confirmed
  path: hooks/post-commit.sh:12
  pattern: eval "$USER_INPUT"
  evidence: line 12 passes unsanitized $USER_INPUT to eval
  remediation: replace eval with an explicit allowlist dispatch; quote and
               validate inputs before use
```

Each `CRITICAL`/`WARNING` finding ID must appear once in `Findings` and once in
`Remediation Plan`; the validator rejects an orphan in either direction. [EXPLICIT]

## Local Validation

Run the skill check:

```bash
bash skills/audit-security/scripts/check.sh
```

Validate a JSON report:

```bash
python3 -B skills/audit-security/scripts/validate_security_report.py \
  --contract skills/audit-security/assets/report-contract.json \
  --scan-policy skills/audit-security/assets/scan-policy.json \
  --evidence-policy skills/audit-security/assets/evidence-policy.json \
  --report <security-report.json>
```

Interpreting validator failures [EXPLICIT]:
- Non-zero exit means the report is non-conformant — do not ship it; read the
  emitted reason, fix the report, re-run until exit 0.
- A green/zero exit confirms *structure*, not security completeness; it does not
  mean the target is safe. Treat it as a schema gate, never an all-clear.
- `check.sh` exercises a known-bad and known-good fixture; if it fails, the skill
  or its policy assets regressed — fix those before auditing real targets.

## Quality Gate

- All six categories are executed and reported in canonical order.
- Every finding has exact path, positive line number, pattern, evidence tag, and
  remediation.
- Finding IDs are `SEC-NNN`, unique, ascending, and gapless.
- Severity counts in `Summary` match the `Findings` set exactly.
- Placeholder/example secrets are never CRITICAL.
- CRITICAL and WARNING findings have matching remediation plan entries.
- No target files are modified, deleted, quarantined, or executed.

## Failure Modes To Avoid

- Severity inflation: flagging example secrets as CRITICAL (breaks placeholder
  rule, erodes trust). [EXPLICIT]
- Category omission: dropping a zero-finding category instead of emitting it
  empty. [EXPLICIT]
- ID drift: non-gapless or severity-ordered IDs that fail determinism. [EXPLICIT]
- Count mismatch: `Summary` totals diverging from `Findings`. [EXPLICIT]
- Orphan remediation: a CRITICAL/WARNING with no plan entry, or a plan entry
  with no finding. [EXPLICIT]
- Scope leak: following a symlink out of the root, or scanning files the user
  did not supply. [EXPLICIT]
- Leaking a live secret verbatim in prose evidence instead of redacting. [EXPLICIT]

## Assumptions & Limits

- Read-only. This skill never modifies, deletes, quarantines, or executes target
  files. [EXPLICIT]
- Pattern-based static analysis cannot prove absence of obfuscated, encoded, or
  split secrets; report posture, never a guarantee of safety. [EXPLICIT]
- Symlink targets outside the supplied root are out of scope and must be reported
  as skipped (`out_of_scope`) rather than followed. [EXPLICIT]
- Binary, vendored, or generated files are inspected only as opaque blobs; note
  them as skipped when not human-readable. [EXPLICIT]
- This skill reports plugin static security posture; runtime exploitation tests
  require a separate, explicitly authorized workflow. [EXPLICIT]
