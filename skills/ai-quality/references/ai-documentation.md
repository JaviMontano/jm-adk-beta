<!-- distilled from alfa skills/ai-documentation -->
<!-- > -->
# AI Documentation
> "Method over hacks."
## TL;DR
Generate documentation only from explicit source evidence, known repository files,
or clearly marked open assumptions. Every output maps each generated section to a
source-evidence id and to validation checks; unverifiable content is removed or
tagged `[OPEN]`, never invented. [EXPLICIT]

## Scope & Anti-Scope
- IN: README, API reference, architecture/usage docs, drift audits — all source-backed. [EXPLICIT]
- OUT: marketing copy, undocumented behavior, live API calls, pricing, or any
  claim without a traceable evidence id. [EXPLICIT]

## Procedure
### Step 1: Source Inventory
- Identify requested doc type, audience, output path, and required source files
  before drafting; closed values come from `assets/doc-type-policy.json`. [CONFIG]
- Record missing, stale, or conflicting inputs as gaps instead of inventing. [EXPLICIT]
### Step 2: Evidence Map
- Create evidence ids for code, existing docs, API specs, configs, tests, and
  user input; allowed source types/statuses from `assets/source-policy.json`. [CONFIG]
- Attach an evidence id to every generated section and claim; a section with
  zero ids is a blocking gap, not a draft. [EXPLICIT]
### Step 3: Generate Packet
- Produce a deterministic documentation packet using
  `assets/documentation-contract.json` (report schema + required checks). [CONFIG]
- Use only closed doc types and source types from local assets. [EXPLICIT]
### Step 4: Validate
- Run `bash skills/ai-documentation/scripts/check.sh` when scripts are present;
  fixtures validate offline via `scripts/validate_ai_documentation_packet.py`. [EXPLICIT]
- Block delivery if required sections lack evidence, if output paths are unsafe,
  or if validation checks are incomplete. [EXPLICIT]

## Acceptance Criteria
- [ ] Source inventory covers all requested docs. [EXPLICIT]
- [ ] Every generated section cites ≥1 evidence id. [EXPLICIT]
- [ ] Unverified claims are removed or tagged `[OPEN]`. [EXPLICIT]
- [ ] Output paths are relative safe docs paths (no `..`, no absolute). [CONFIG]
- [ ] Conflicting sources are recorded with `warn`/`block` status, not silently merged. [EXPLICIT]
- [ ] Validation packet passes the offline script with exit 0. [EXPLICIT]

## Key Decisions & Trade-offs
- **Closed doc/source types (policy assets) over free-form.** Trade-off: less
  flexibility for novel doc kinds, but guarantees deterministic, auditable output
  and blocks taxonomy drift. Extend the policy asset rather than bypass it. [CONFIG]
- **Offline-only validation.** Trade-off: cannot verify against live endpoints,
  but keeps runs reproducible, hermetic, and safe in CI with no network/secrets. [EXPLICIT]
- **Gap-over-guess.** When evidence is absent the packet emits a gap, never a
  plausible-sounding sentence — drift audits stay trustworthy. [EXPLICIT]

## Worked Example
Request: "Create API docs from `openapi.yaml`."
1. Inventory: doc type `api-reference`, audience `developer`, output
   `docs/api/reference.md`, required source `openapi.yaml`. [EXPLICIT]
2. Evidence map: `E1=openapi.yaml#/paths`, `E2=src/handlers/*.ts`. [EXPLICIT]
3. Each endpoint section cites `E1` (contract) + `E2` (implementation); an
   endpoint in `E1` with no `E2` match is tagged `[OPEN]` (spec-only). [EXPLICIT]
4. Validate: `check.sh` confirms every section has an id and the path is safe → packet `pass`. [EXPLICIT]

## Deterministic DoD Assets
- `assets/documentation-contract.json` — report schema and required checks. [CONFIG]
- `assets/source-policy.json` — allowed source types and source statuses. [CONFIG]
- `assets/doc-type-policy.json` — closed documentation target types and audiences. [CONFIG]
- `assets/gap-policy.json` — gap severity and blocking-gap behavior. [CONFIG]
- `assets/path-policy.json` — safe relative output path constraints. [CONFIG]
- `scripts/validate_ai_documentation_packet.py` — validates fixtures offline. [EXPLICIT]

## Assumptions & Limits
- Assumes access to project artifacts: code, docs, configs, API specs, or user-provided snippets. [EXPLICIT]
- Does not call external documentation services or live APIs during validation. [EXPLICIT]
- Does not invent undocumented behavior; unresolved behavior must be tagged `[OPEN]`. [EXPLICIT]
- Determinism assumes pinned policy assets; editing an asset changes accepted output and must be versioned. [CONFIG]

## Edge Cases & Failure Modes
| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Produce a gap-analysis packet listing required sources; do not draft prose. |
| Conflicting source files | Record conflict evidence; set validation status to `warn` or `block` per `gap-policy.json`. |
| Requested unsafe output path | Block; request a safe relative path under `docs/`, `README`, or `api docs`. |
| API docs without API spec | Emit missing-source gap instead of inventing endpoints. |
| Stale doc vs current code (drift audit) | Flag section as stale with both evidence ids; do not auto-rewrite without source. |
| Section cites no evidence id | Treat as blocking gap; never ship an un-cited section. |
| Doc type/source type outside policy | Reject as out-of-taxonomy; extend the policy asset deliberately, do not inline a one-off. |
| Validation script absent | Degrade to manual checklist (Acceptance Criteria) and mark packet `warn`. |

## Usage
- "Generate a README from this repo" — source-backed README packet.
- "Create API docs from this OpenAPI file" — API reference sections with spec+impl ids.
- "Audit documentation drift" — report stale, missing, or conflicting documentation.
