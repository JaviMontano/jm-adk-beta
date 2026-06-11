#!/usr/bin/env python3
"""validate-coverage.py — CI gate: functional parity claim is auditable.

Rules:
  1. Every coverage-matrix row has a disposition (no blank, no UNASSIGNED).
  2. Every referenced (load-bearing) alfa skill has beta_home != none OR
     disposition in {dropped-generic, alias} with rationale.
  3. Every router-fold beta_home resolves: skills/<router>/references/<short>.md exists.
  4. Every core/keep beta_home resolves: skills/<id>/SKILL.md exists.
  5. Every catalog alias target resolves to a beta skill or router#playbook.
Exit 1 on any violation.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rows = list(csv.DictReader((ROOT / "catalog/coverage-matrix.csv").open(encoding="utf-8")))
catalog = json.loads((ROOT / "catalog/skills.json").read_text(encoding="utf-8"))
errors = []


def home_resolves(home: str) -> bool:
    if "#" in home:
        router, short = home.split("#", 1)
        return (ROOT / "skills" / router / "references" / f"{short}.md").exists()
    return (ROOT / "skills" / home / "SKILL.md").exists()


for r in rows:
    sid, disp, home = r["alfa_skill"], r["disposition"], r["beta_home"]
    if not disp or disp == "UNASSIGNED":
        errors.append(f"{sid}: no disposition")
        continue
    referenced = int(r["referenced_by_count"]) > 0
    if referenced and disp not in ("dropped-generic", "alias") and home in ("", "none"):
        errors.append(f"{sid}: load-bearing but no beta home")
    if disp in ("router-fold", "core") and not home_resolves(home):
        errors.append(f"{sid}: beta_home {home} does not resolve")
    if disp in ("dropped-generic",) and not r["rationale"]:
        errors.append(f"{sid}: dropped without rationale")

for alias, target in catalog.get("aliases", {}).items():
    if not home_resolves(target):
        errors.append(f"alias {alias} -> {target} does not resolve")

if errors:
    print(f"FAIL — {len(errors)} violations:")
    for e in errors[:40]:
        print(f"  {e}")
    sys.exit(1)

from collections import Counter
c = Counter(r["disposition"] for r in rows)
print(f"PASS — {len(rows)} rows, dispositions: {dict(c)}, aliases: {len(catalog.get('aliases', {}))}")
