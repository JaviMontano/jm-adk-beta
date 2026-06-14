# Adaptive Investigation Report — Auth Validation in a Monorepo

## Goal
Locate the node that verifies the auth token (signature + expiry) in a ~4000-file backend monorepo. [DOC]

## Budget
| Field | Value |
|---|---|
| Total (hard) | 8 reads |
| Used | 2 |
| Remaining | 6 |
| Termination guaranteed by | hard budget |

## Surface map (cheap)
Built with `Glob`/`Grep -l` only; zero budget spent. 11 candidate nodes. [CÓDIGO]

| Node | Region | How discovered | Candidate? |
|---|---|---|---|
| `middleware/auth.ts` | entrypoint | `Glob **/auth*` | yes |
| `lib/jwt/verify.ts` | lib | `Grep -l "verify|expiresAt"` | yes |
| `services/session/*` | service | `Glob **/session/**` | yes |
| `tests/auth/*.spec.ts` | test | `Glob **/auth*.spec.*` | yes (low) |

## Ranked hypotheses
| # | Hypothesis | Target node(s) | Value/cost | Confirms if… | Invalidates if… |
|---|---|---|---|---|---|
| H1 | Validation lives in the auth middleware | `middleware/auth.ts` | high | it verifies signature+expiry inline | it only guards and delegates |
| H2 | Validation lives in the JWT lib | `lib/jwt/verify.ts` | med | it checks signature+expiry | it only decodes |
| H3 | Validation lives in session service | `services/session/*` | low | session creation verifies token | — |

## Deep-dive log
| Step | Node | Budget after | Verdict | Evidence | Tag |
|---|---|---|---|---|---|
| 1 | `middleware/auth.ts` | 7 | invalidated (partial) | exports `requireAuth`, but calls `verifyToken()` from `lib/jwt/verify` — guards, does not validate | [CÓDIGO] |
| 2 | `lib/jwt/verify.ts` | 6 | confirm | `verifyToken` checks HMAC signature and `exp` claim, throws on expiry | [CÓDIGO] |

## Re-plan log
| Re-plan | Invalidated hypothesis | Triggering evidence | New top hypothesis |
|---|---|---|---|
| R1 | H1 | `middleware/auth.ts` delegates to `lib/jwt/verify.verifyToken` | H2 → `lib/jwt/verify.ts` |

## Findings
- **`middleware/auth.ts`** — exposes `requireAuth`, but delegates the actual check; it is a guard, not the validator. `[CÓDIGO]`
- **`lib/jwt/verify.ts`** — `verifyToken()` validates the HMAC signature and the `exp` claim, raising on an expired/invalid token. This is the resolving node. `[CÓDIGO]`

## Deliverable
Auth tokens are validated in **`lib/jwt/verify.ts`** by `verifyToken()`, which checks the HMAC signature and the `exp` expiry claim. The middleware `middleware/auth.ts` (`requireAuth`) only enforces the guard and delegates to it. Resolved in 2 deep-dives. [CÓDIGO]

## Stop reason
- `goal_resolved` after the second deep-dive. Remaining budget 6 — efficiency, not waste. [INFERENCIA]

## Coverage & residual risks
- Coverage: targeted, not exhaustive — `services/session/*` and tests were not deep-dived because H1→H2 resolved the goal. [INFERENCIA]
- Residual: if a second token type (refresh token) exists, it may be validated elsewhere; out of scope for this `goal`. `[SUPUESTO]`

---
Single brand: JM Labs. No invented prices. No client PII. Discover-not-mutate.
