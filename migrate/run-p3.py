#!/usr/bin/env python3
"""run-p3.py — Execute the P3 grouping: distill new routers + extend existing ones.

Reads catalog/consolidation-map-p3.yaml (simple subset parser), verifies the 222
ids match /tmp/unassigned.txt when present, then drives migrate/distill-skill.py.
Existing routers are re-distilled with previous routes.json absorbs + additions.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "catalog" / "consolidation-map-p3.yaml"
DISTILL = ROOT / "migrate" / "distill-skill.py"


def parse() -> tuple[dict, dict, list, list]:
    text = MAP.read_text(encoding="utf-8")
    routers: dict[str, dict] = {}
    for m in re.finditer(r"^  ([\w-]+):\n    desc: \"(.*?)\"\n    absorb: \[(.*?)\]", text, re.M | re.S):
        routers[m.group(1)] = {
            "desc": m.group(2),
            "absorb": [s.strip() for s in m.group(3).replace("\n", " ").split(",") if s.strip()],
        }
    existing: dict[str, list] = {}
    em = re.search(r"^existing:\n((?:  [\w-]+: \[.*?\]\n)+)", text, re.M)
    if em:
        for line in em.group(1).strip().splitlines():
            k, v = line.strip().split(": ", 1)
            existing[k] = [s.strip() for s in v.strip("[]").split(",") if s.strip()]
    standalone = []
    sm = re.search(r"^standalone: \[(.*?)\]", text, re.M)
    if sm and sm.group(1).strip():
        standalone = [s.strip() for s in sm.group(1).split(",")]
    dropped = []
    dm = re.search(r"^dropped_generic_p3: \[(.*?)\]", text, re.M)
    if dm:
        dropped = [s.strip() for s in dm.group(1).split(",")]
    return routers, existing, standalone, dropped


def main() -> int:
    routers, existing, standalone, dropped = parse()
    all_ids = [s for r in routers.values() for s in r["absorb"]]
    all_ids += [s for v in existing.values() for s in v] + standalone + dropped
    dupes = {x for x in all_ids if all_ids.count(x) > 1}
    print(f"total ids: {len(all_ids)}; dupes: {dupes or 'none'}")
    if dupes:
        return 1

    for name, spec in routers.items():
        subprocess.run(
            [sys.executable, str(DISTILL), "--mode", "router", "--router", name,
             "--desc", spec["desc"], "--absorb", *spec["absorb"]],
            check=True, cwd=ROOT,
        )

    for name, additions in existing.items():
        rj = ROOT / "skills" / name / "routes.json"
        prev = [v["alfa"] for v in json.loads(rj.read_text(encoding="utf-8")).values()]
        # keep original desc from SKILL.md
        skill_md = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        dm = re.search(r'^description: "(.*?) Topics:', skill_md, re.M)
        desc = dm.group(1) if dm else name
        subprocess.run(
            [sys.executable, str(DISTILL), "--mode", "router", "--router", name,
             "--desc", desc, "--absorb", *prev, *additions],
            check=True, cwd=ROOT,
        )

    if standalone:
        subprocess.run([sys.executable, str(DISTILL), "--mode", "core", "--absorb", *standalone], check=True, cwd=ROOT)

    print(f"dropped-generic (p3): {len(dropped)} — append to consolidation-map.yaml dropped_generic")
    return 0


if __name__ == "__main__":
    sys.exit(main())
