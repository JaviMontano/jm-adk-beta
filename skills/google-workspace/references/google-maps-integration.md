<!-- distilled from alfa skills/google-maps-integration -->
<!-- > -->
# Google Maps Integration

## TL;DR

[DOC] Produces an offline plan/checklist for location-aware web applications that need interactive maps, custom markers, marker clustering, location search, geocoding, route directions, privacy controls, and API key restrictions.
[CONFIG] The primary script is `scripts/compile-google-maps-plan.py`; it reads local assets/fixtures only and never calls Google APIs.

## Procedure

### Step 1: Discover

- [CODE] Identify requested features: `interactive_map`, `location_search`, `address_geocoding`, `reverse_geocoding`, `route_directions`, `dense_markers`, `advanced_markers`, and `place_details`.
- [CODE] Check `assets/maps-platform-plan-schema.json` before drafting or compiling a plan.
- [DOC] Use Maps JavaScript API for client-side interactive web maps, markers, custom data layers, and JavaScript map services.
- [DOC] Use Advanced Markers when marker customization, DOM click, keyboard interaction, or HTML/CSS marker content is required.
- [DOC] Use MarkerClusterer when dense marker sets need grouping and zoom-dependent simplification.

### Step 2: Analyze

- [DOC] Select APIs using `assets/api-selection-policy.json`.
- [DOC] Treat Places API (New) as the default Places web-service path and minimize returned fields.
- [DOC] Treat Geocoding API as the address/coordinate/place ID conversion path and cache normalized results where allowed.
- [DOC] Treat Directions API as `Legacy`; require explicit legacy acknowledgement and evaluate newer routing services before production.
- [DOC] Apply `assets/api-key-restriction-policy.json`: separate browser/server keys, one application restriction per key, and API restrictions only for selected services.
- [CONFIG] Do not include monetary prices, currency amounts, or per-request amounts in the plan.

**Decisions & trade-offs:**

- [DOC] Browser key (HTTP-referrer restricted) vs server key (IP restricted): browser keys are visible in client source and cannot hold secrets, so the trade-off is convenience (direct JS API calls) against exposure — mitigate with referrer + API restriction, never API-key-only auth for billable server calls. [SUPUESTO] Assumes the app has at least one server context; pure-static sites accept the wider browser-key blast radius.
- [DOC] Advanced Markers vs legacy `Marker`: Advanced Markers add DOM/keyboard/HTML content and are the accessibility-preferred default; cost is a map-id requirement and vector-map dependency. Choose legacy markers only when a map-id cannot be provisioned. [SUPUESTO]
- [DOC] Geocoding cache vs live lookups: caching cuts quota and latency but risks stale coordinates for moved/renamed places — bound cache by `assets/api-selection-policy.json` retention and re-geocode on user-reported mismatch.

### Step 3: Execute

- [CODE] Fill a JSON input matching `assets/maps-platform-plan-schema.json`.
- [CODE] Run `python3 skills/google-maps-integration/scripts/compile-google-maps-plan.py --input <fixture-or-input.json> --output <plan.md>`.
- [CODE] Include API selection, key restrictions, billing/quota risk checklist, Places/Geocoding/Directions data flow, marker clustering, accessibility, privacy, and human-confirmation gate.
- [CONFIG] Keep `operations.offline_plan_only=true` and `operations.external_api_calls=false`.
- [CONFIG] Require `human_confirmation.status=confirmed` before treating the plan as ready.

[CODE] Worked example — minimal valid input fixture:

```json
{
  "features": ["interactive_map", "location_search", "address_geocoding"],
  "keys": [
    {"name": "browser", "runtime": "browser", "application_restriction": "http_referrer",
     "api_restriction": ["maps_javascript", "places"]},
    {"name": "server", "runtime": "server", "application_restriction": "ip",
     "api_restriction": ["geocoding"]}
  ],
  "operations": {"offline_plan_only": true, "external_api_calls": false},
  "human_confirmation": {"status": "pending"}
}
```

[CODE] Compile, then flip `human_confirmation.status` to `confirmed` only after a human reviews the emitted plan:

```bash
python3 skills/google-maps-integration/scripts/compile-google-maps-plan.py \
  --input fixtures/minimal.json --output plan.md
```

### Step 4: Validate

- [CODE] Run `bash skills/google-maps-integration/scripts/check.sh`.
- [CODE] Run `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill google-maps-integration`.
- [CODE] Run `python3 -B scripts/validate-skill-dod.py --skill google-maps-integration`.
- [CODE] Confirm all generated output claims keep evidence tags.

## Acceptance Criteria

[DOC] The plan is "ready" only when ALL hold:

- [ ] [CODE] Input validated against `assets/maps-platform-plan-schema.json` with zero schema errors.
- [ ] [CODE] Every selected feature maps to exactly one API selection rationale; no feature left unmapped.
- [ ] [CODE] Each key declares one `application_restriction` and `api_restriction` scoped to only its selected services.
- [ ] [CONFIG] `operations.offline_plan_only=true`, `operations.external_api_calls=false`, `human_confirmation.status=confirmed`.
- [ ] [CONFIG] Plan contains no monetary value, currency symbol, or per-request amount.
- [ ] [CODE] `check.sh`, `validate-skill-scripts.py --strict --run-checks`, and `validate-skill-dod.py` all exit 0.
- [ ] [CODE] Every claim in the emitted plan carries an evidence tag.

## Failure Modes

| Failure | Symptom | Mitigation |
|---------|---------|------------|
| [CODE] Schema drift | Compiler rejects input or emits partial plan | Re-validate against `maps-platform-plan-schema.json`; regenerate fixture from current schema. |
| [CONFIG] Over-broad key | One key restricted to many unrelated APIs | Split per runtime; one `application_restriction` + minimal `api_restriction` per key. |
| [CODE] Field over-fetch | Places request asks for full field mask | Restrict to id, display name, formatted address, location. |
| [DOC] Silent legacy use | Directions emitted without `directions_legacy_acknowledged` | Block plan; require explicit acknowledgement and newer-service evaluation note. |
| [CONFIG] Price leakage | Currency/amount appears in plan | Strip; billing risk is qualitative only. |
| [CONFIG] Live-call drift | Skill attempts a real API/Cloud Console call | Refuse; keep `external_api_calls=false`. |
| [DOC] A11y gap | No keyboard path or non-map list | Add marker titles, map summary, and list/table fallback. |

## Quality Criteria

- [ ] [CODE] `assets/manifest.json` lists every local asset and its consumer files.
- [ ] [CODE] The compiler is deterministic, offline, and validated by positive and negative fixtures.
- [ ] [DOC] API selection covers Maps JavaScript API, Advanced Markers, MarkerClusterer, Places API, Geocoding API, and Directions API (Legacy) when triggered.
- [ ] [DOC] API keys are separated by browser/server runtime with application and API restrictions.
- [ ] [CONFIG] Billing/quota risk is checked without monetary prices.
- [ ] [CODE] Accessibility includes keyboard paths, marker titles/accessibility names, map summary, and non-map location list.
- [ ] [CONFIG] Privacy includes consent, retention, redaction, and human confirmation.

## Anti-Patterns

- [DOC] Unrestricted API key exposed to browser traffic.
- [DOC] Browser and server web-service traffic sharing one key.
- [CODE] Geocoding the same address on every page load instead of using a cache policy.
- [CODE] Requesting broad Places fields when the feature needs only ID, display name, formatted address, or location.
- [CONFIG] Producing live API calls from this skill.
- [CONFIG] Including monetary prices in the plan.

## Related Skills

- [INFERENCE] `google-apis-integration` covers broader backend Google API patterns.
- [INFERENCE] `vanilla-javascript` can implement Maps JavaScript API without framework wrappers.
- [INFERENCE] `responsive-design` can support responsive map containers and mobile interaction.
- [INFERENCE] `performance-architecture` can support lazy loading and marker density decisions.

## Usage

Example invocations: [EXPLICIT]

- "/google-maps-integration" — Run the full google maps integration workflow
- "google maps integration on this project" — Apply to current context


## Assumptions & Limits

- [SUPUESTO] Assumes the user can supply requirements as structured JSON or enough context to produce that JSON.
- [CONFIG] Does not call Google APIs, validate real credentials, enable services, or inspect Cloud Console.
- [INFERENCE] Real implementation still needs browser testing, Cloud Console verification, accessibility testing, and privacy/legal review.

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | [CODE] Produce a gap list against `assets/maps-platform-plan-schema.json`. |
| Directions requested | [DOC] Require `directions_legacy_acknowledged=true` and flag Legacy status. |
| Dense marker set | [DOC] Require MarkerClusterer and an alternate list/table. |
| Precise user location | [CONFIG] Require consent, retention, redaction, and human confirmation. |
| API call requested | [CONFIG] Refuse live call and produce offline plan only. |
| Conflicting key restrictions | [CODE] Two keys claim the same runtime/service; flag overlap and force one key per runtime. |
| Feature without supporting API | [CODE] Emit a gap entry; do not silently assume a default API. |
| Geocoding rate/quota pressure | [CODE] Require cache policy + batching note before marking the plan ready. |
