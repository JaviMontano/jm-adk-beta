#!/usr/bin/env python3
"""update-catalog.py — Sync catalog/skills.json from skills/*/SKILL.md frontmatter.

Law of Single Source: catalog is generated, never hand-edited (except aliases).
Uses a real YAML-ish parser for the frontmatter fields we own (name, description,
params enums) — avoids alfa's folded-scalar bug by reading description as a
single- or double-quoted scalar or plain line.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "skills.json"


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm = m.group(1)
    out = {}
    nm = re.search(r"^name:\s*(.+?)\s*$", fm, re.M)
    if nm:
        out["name"] = nm.group(1).strip("\"'")
    dm = re.search(r"^description:\s*[\"']?(.+?)[\"']?\s*$", fm, re.M)
    if dm:
        out["description"] = dm.group(1)
    params = {}
    pm = re.search(r"^params:\n((?:[ \t]+.*\n?)+)", fm, re.M)
    if pm:
        block = pm.group(1)
        for pname, enum in re.findall(r"^  (\w[\w-]*):\n(?:(?:[ \t]+.*\n)*?)[ \t]+enum:\s*\[(.*?)\]", block, re.M):
            params[pname] = [e.strip() for e in enum.split(",")]
        # also catch inline form: param: {enum: [...]}  (not used yet)
    if params:
        out["params"] = params
    return out


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    aliases = catalog.get("aliases", {})
    skills = []
    for d in sorted((ROOT / "skills").iterdir()):
        sm = d / "SKILL.md"
        if not sm.exists():
            continue
        fm = parse_frontmatter(sm.read_text(encoding="utf-8"))
        desc = fm.get("description", "").strip()
        # Topics enum already lives in params — drop the redundant clause.
        desc = re.sub(r"\s*Topics:.*$", "", desc)
        if not desc:
            print(f"WARN {d.name}: empty description", file=sys.stderr)
        if len(desc) > 54:  # trim at word boundary (compressed register; tier-0 budget — v7 core is larger)
            desc = desc[:54].rsplit(" ", 1)[0].rstrip(",;:") + "…"
        entry = {
            "id": d.name,
            "desc": desc,
            "tier": "router" if (d / "routes.json").exists() else "standalone",
        }
        if fm.get("params"):
            entry["params"] = fm["params"]
        if (d / "evals.json").exists():
            entry["evals"] = True
        skills.append(entry)
    catalog["skills"] = skills
    catalog["aliases"] = aliases
    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"catalog: {len(skills)} skills ({sum(1 for s in skills if s['tier']=='router')} routers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
