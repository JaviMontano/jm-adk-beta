<!-- distilled from alfa skills/data-export -->
<!-- > -->
# Data Export
> "Method over hacks."
## TL;DR
Export tabular/structured data to CSV, JSON, or PDF; batch over many records; schedule recurring report generation. Streams large sets, fails closed on partial writes. [DOC]
## Scope
- IN: format conversion, batch jobs, scheduled reports, delivery to file/path. [DOC]
- OUT (anti-scope): live API/streaming feeds, in-place DB mutation, format design/branding (defer to a brand skill), PII redaction policy (assumed upstream). [SUPUESTO]
## Procedure
### Step 1: Discover
- Capture: source, target format(s), row volume, schedule, destination, encoding. [DOC]
- Resolve column set + ordering explicitly; never infer from first row alone. [INFERENCIA]
### Step 2: Analyze
- Choose format per use (see Decisions); evaluate options per Constitution XIII/XIV. [DOC]
- Estimate volume → pick streaming vs in-memory at the threshold below. [INFERENCIA]
### Step 3: Execute
- Write to a temp path, fsync, then atomic-rename to target — no partial files visible. [INFERENCIA]
- Stamp each row/claim with evidence tags where the output asserts derived data. [DOC]
### Step 4: Validate
- Re-open the artifact, assert row count and header against source. [DOC]
## Decisions & trade-offs
| Choice | Use when | Trade-off |
|---|---|---|
| CSV | Spreadsheet/interchange, flat data | No nesting; quoting/encoding hazards [INFERENCIA] |
| JSON | Nested/typed payloads, machine reads | Larger; not spreadsheet-friendly [INFERENCIA] |
| PDF | Human-facing fixed report | Not re-parseable; render cost [INFERENCIA] |
| Stream | rows > ~100k or memory-bound | More code; harder random access [SUPUESTO] |
## Worked example
- Input: 250k-row table → monthly CSV. Stream (>100k), UTF-8 BOM for Excel, RFC-4180 quoting, atomic rename, then assert `wc -l == rows+1`. [INFERENCIA]
## Quality / Acceptance Criteria
- [ ] Output row count == source row count (header excluded). [DOC]
- [ ] Header/column order matches the resolved spec from Step 1. [DOC]
- [ ] Encoding declared (default UTF-8); delimiters/quotes RFC-4180 for CSV. [SUPUESTO]
- [ ] Write is atomic; no partial artifact on failure. [INFERENCIA]
- [ ] Evidence tags applied; Constitution-compliant; output actionable. [DOC]
## Usage
Example invocations:
- "/data-export" — Run the full data export workflow
- "data export on this project" — Apply to current context
## Assumptions & Limits
- Assumes read access to source artifacts (code, docs, configs). [SUPUESTO]
- English-language output unless otherwise specified. [SUPUESTO]
- Does not replace domain-expert judgment for final decisions. [SUPUESTO]
- Assumes PII handling/redaction is enforced upstream, not here. [SUPUESTO]
## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding [SUPUESTO] |
| Conflicting requirements | Flag conflicts explicitly, propose resolution [SUPUESTO] |
| Out-of-scope request | Redirect to appropriate skill or escalate [SUPUESTO] |
| Volume exceeds memory | Switch to streaming write; do not buffer all rows [INFERENCIA] |
| Field contains delimiter/newline | RFC-4180 quote-and-escape; never strip silently [INFERENCIA] |
| Mixed/unknown encoding | Normalize to UTF-8; flag undecodable bytes, do not drop [INFERENCIA] |
| Schedule overlaps prior run | Skip or queue; never run two writers at one target [SUPUESTO] |
| Partial write / crash mid-export | Discard temp; leave prior artifact intact (atomic rename) [INFERENCIA] |
