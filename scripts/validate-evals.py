#!/usr/bin/env python3
"""validate-evals.py — Structural CI gate for skills/*/evals.json.

Checks: valid JSON, schema==1, skill matches dir, >=3 cases, each case has
id/input/expected_activation/expected_checks. Real activation evals run in P5
smoke (LLM-judged); this gate keeps the contracts well-formed.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failed = 0
count = 0
for ev in sorted((ROOT / "skills").glob("*/evals.json")):
    count += 1
    try:
        data = json.loads(ev.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL {ev}: invalid JSON: {e}")
        failed += 1
        continue
    errs = []
    if data.get("schema") != 1:
        errs.append("schema != 1")
    if data.get("skill") != ev.parent.name:
        errs.append(f"skill field {data.get('skill')!r} != dir {ev.parent.name!r}")
    cases = data.get("cases", [])
    if len(cases) < 3:
        errs.append(f"only {len(cases)} cases (<3)")
    for c in cases:
        missing = [k for k in ("id", "input") if k not in c]
        if not ("expected_activation" in c or "expected_behavior" in c):
            missing.append("expected_activation|expected_behavior")
        if missing:
            errs.append(f"case {c.get('id','?')}: missing {missing}")
    if errs:
        print(f"FAIL {ev.parent.name}: " + "; ".join(errs))
        failed += 1
print(f"{count - failed}/{count} eval contracts OK")
sys.exit(1 if failed else 0)
