#!/usr/bin/env python3
"""estimate.py — Deterministic effort estimator (Constitution Principle 8: Estimation Integrity).

Estimates are COMPUTED, never guessed. This tool turns a task decomposition into an
effort figure with a confidence band and an explicit source per task — so the number
is defensible, reproducible, and free of token-count or gut-feel inputs.

Method (per task): three-point PERT.
    expected  = (optimistic + 4*likely + pessimistic) / 6
    std_dev   = (pessimistic - optimistic) / 6
Totals sum the expected values; the band is the root-sum-square of the std devs
(tasks assumed independent — see ASSUMPTIONS). Units are caller-defined (hours,
story-points, days) and never currency; pricing is a profile concern, not this tool's.

Every task MUST carry a `basis` — where its three points come from:
    measured  — from a timed prior run / log         (highest trust)
    analogy   — from a comparable past task           (cite the analog)
    expert    — from a named estimator's judgment     (lowest trust; flag it)
A task with no basis is rejected: an unsourced estimate is a defect, not an estimate.

Input: JSON on stdin or via --tasks FILE:
    { "unit": "hours",
      "tasks": [
        { "id": "T1", "desc": "...", "basis": "measured|analogy|expert",
          "source": "where this came from",
          "optimistic": 2, "likely": 4, "pessimistic": 9 }
      ] }

Output: JSON (default) or --format text. Exit 0 on a valid estimate, 1 on a
validation error (missing basis/source, non-monotonic points, empty task list).

Self-test: `python3 scripts/estimate.py --selftest` (no input needed).
"""
from __future__ import annotations

import argparse
import json
import math
import sys

VALID_BASIS = {"measured", "analogy", "expert"}
# Trust multipliers widen the band for weaker bases — an expert guess is not as
# tight as a measured run even when the three points look identical. [INFERENCE]
BASIS_BAND_FACTOR = {"measured": 1.0, "analogy": 1.3, "expert": 1.7}


def validate_task(t: dict) -> list[str]:
    errs: list[str] = []
    tid = t.get("id", "<no-id>")
    if not t.get("id"):
        errs.append("task missing id")
    if t.get("basis") not in VALID_BASIS:
        errs.append(f"{tid}: basis must be one of {sorted(VALID_BASIS)} (unsourced estimate = defect)")
    if not str(t.get("source", "")).strip():
        errs.append(f"{tid}: missing source (where do the three points come from?)")
    for k in ("optimistic", "likely", "pessimistic"):
        if not isinstance(t.get(k), (int, float)):
            errs.append(f"{tid}: {k} must be a number")
    if all(isinstance(t.get(k), (int, float)) for k in ("optimistic", "likely", "pessimistic")):
        o, m, p = t["optimistic"], t["likely"], t["pessimistic"]
        if not (o <= m <= p):
            errs.append(f"{tid}: points must satisfy optimistic <= likely <= pessimistic (got {o}, {m}, {p})")
        if o < 0:
            errs.append(f"{tid}: optimistic must be >= 0")
    return errs


def estimate(payload: dict) -> dict:
    unit = payload.get("unit", "hours")
    tasks = payload.get("tasks", [])
    if not tasks:
        raise ValueError("no tasks: decompose the work first — an estimate without a decomposition is a guess")
    errs: list[str] = []
    for t in tasks:
        errs.extend(validate_task(t))
    if errs:
        raise ValueError("; ".join(errs))

    rows = []
    total_expected = 0.0
    var_sum = 0.0
    for t in tasks:
        o, m, p = float(t["optimistic"]), float(t["likely"]), float(t["pessimistic"])
        expected = (o + 4 * m + p) / 6
        sd = (p - o) / 6 * BASIS_BAND_FACTOR[t["basis"]]
        total_expected += expected
        var_sum += sd * sd
        rows.append({
            "id": t["id"],
            "desc": t.get("desc", ""),
            "basis": t["basis"],
            "source": t["source"],
            "expected": round(expected, 2),
            "std_dev": round(sd, 2),
        })

    total_sd = math.sqrt(var_sum)
    # Confidence label from coefficient of variation (band relative to size). [INFERENCE]
    cv = (total_sd / total_expected) if total_expected else 1.0
    confidence = "high" if cv < 0.15 else "medium" if cv < 0.30 else "low"
    weakest = min((BASIS_BAND_FACTOR[t["basis"]] for t in tasks), default=1.0)
    return {
        "unit": unit,
        "tasks": rows,
        "total_expected": round(total_expected, 2),
        "band_p10_p90": [round(total_expected - 1.2816 * total_sd, 2), round(total_expected + 1.2816 * total_sd, 2)],
        "std_dev": round(total_sd, 2),
        "confidence": confidence,
        "assumptions": [
            "Tasks are independent; std devs combined via root-sum-square. If tasks share a "
            "common risk (one blocker stalls many), the real band is wider. [ASSUMPTION]",
            "Three-point inputs are honest; garbage in, garbage out. Each carries a source for audit. [ASSUMPTION]",
            f"Weakest basis present widens bands by x{max(BASIS_BAND_FACTOR[t['basis']] for t in tasks)}. [CONFIG]",
        ],
        "method": "three-point PERT per task; RSS aggregation; basis-weighted bands. [DOC]",
    }


def to_text(r: dict) -> str:
    lines = [f"Estimate ({r['unit']}) — method: {r['method']}", ""]
    lines.append(f"{'id':<10} {'basis':<9} {'exp':>7} {'sd':>6}  source")
    for t in r["tasks"]:
        lines.append(f"{t['id']:<10} {t['basis']:<9} {t['expected']:>7} {t['std_dev']:>6}  {t['source']}")
    lines += [
        "",
        f"TOTAL: {r['total_expected']} {r['unit']}  (±{r['std_dev']}, {r['confidence']} confidence)",
        f"P10–P90 band: {r['band_p10_p90'][0]} – {r['band_p10_p90'][1]} {r['unit']}",
        "",
        "Assumptions:",
    ]
    lines += [f"  - {a}" for a in r["assumptions"]]
    return "\n".join(lines)


SELFTEST_PAYLOAD = {
    "unit": "hours",
    "tasks": [
        {"id": "T1", "desc": "scaffold module", "basis": "measured", "source": "prior run log 2026-05", "optimistic": 1, "likely": 2, "pessimistic": 4},
        {"id": "T2", "desc": "wire integration", "basis": "analogy", "source": "comparable task in repo X", "optimistic": 3, "likely": 5, "pessimistic": 10},
        {"id": "T3", "desc": "edge-case handling", "basis": "expert", "source": "lead estimate, unverified", "optimistic": 2, "likely": 4, "pessimistic": 12},
    ],
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic effort estimator (decomposition + PERT + sources).")
    ap.add_argument("--tasks", help="JSON file; omit to read stdin")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    ap.add_argument("--selftest", action="store_true", help="run on a built-in fixture and exit")
    args = ap.parse_args()

    if args.selftest:
        payload = SELFTEST_PAYLOAD
    else:
        raw = open(args.tasks, encoding="utf-8").read() if args.tasks else sys.stdin.read()
        if not raw.strip():
            print("ERROR: no input. Provide --tasks FILE or pipe JSON to stdin (or use --selftest).", file=sys.stderr)
            return 1
        payload = json.loads(raw)

    try:
        result = estimate(payload)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2) if args.format == "json" else to_text(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
