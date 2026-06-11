#!/usr/bin/env python3
"""distill-skill.py — Port alfa skills into beta's compact anatomy.

Modes:
  --mode router --router <id> --absorb <alfa-skill>...   For each absorbed skill:
      strip frontmatter from its SKILL.md, write body to
      skills/<router>/references/<short>.md (short = alfa id minus router prefix).
      Then (re)generate skills/<router>/SKILL.md with params+routes frontmatter.
  --mode core --absorb <alfa-skill>...                   Copy SKILL.md (trim to
      <=150 lines preserving frontmatter+body head) + evals/evals.json if present.

Deterministic. Boilerplate dirs (README, agents/, knowledge/, examples/,
prompts/, templates/, assets/) are never copied — replaced by shared library.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALFA = Path("/Users/deonto/Documents/workspace/jm-adk-alfa")


def split_frontmatter(text: str) -> tuple[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return "", text
    return m.group(1), m.group(2)


def fm_field(fm: str, key: str) -> str:
    m = re.search(rf"^{key}:\s*[\"']?(.+?)[\"']?\s*$", fm, re.M)
    return m.group(1) if m else ""


def short_name(alfa_id: str, router: str) -> str:
    for prefix in (f"{router}s-", f"{router}-"):
        if alfa_id.startswith(prefix):
            return alfa_id[len(prefix):]
    return alfa_id


def do_router(router: str, absorbed: list[str], desc: str) -> None:
    rdir = ROOT / "skills" / router
    refs = rdir / "references"
    refs.mkdir(parents=True, exist_ok=True)
    routes = {}
    for aid in absorbed:
        src = ALFA / "skills" / aid / "SKILL.md"
        if not src.exists():
            print(f"WARN missing {aid}", file=sys.stderr)
            continue
        fm, body = split_frontmatter(src.read_text(encoding="utf-8"))
        sn = short_name(aid, router)
        adesc = fm_field(fm, "description")
        header = f"<!-- distilled from alfa skills/{aid} -->\n"
        if adesc:
            header += f"<!-- {adesc} -->\n"
        (refs / f"{sn}.md").write_text(header + body.strip() + "\n", encoding="utf-8")
        routes[sn] = {"playbook": f"references/{sn}.md", "desc": adesc, "alfa": aid}
        print(f"  {aid} -> skills/{router}/references/{sn}.md")

    route_lines = "\n".join(f"  {k}: references/{k}.md" for k in sorted(routes))
    topics = ", ".join(sorted(routes))
    skill_md = f"""---
name: {router}
description: "{desc} Topics: {topics}."
params:
  topic:
    enum: [{', '.join(sorted(routes))}]
    required: true
    infer: from user request; ask only if ambiguous
  depth:
    enum: [quick, deep]
    default: quick
routes:
{route_lines}
---

# {router}

Router skill. Resolve `topic` from the request, then Read EXACTLY ONE playbook
from `routes:`. Never load the whole cluster. `depth=deep` → apply the playbook
exhaustively with verification at each step; `quick` → essentials only.

Spine: Discover → Analyze → Execute → Validate.
Quality gates: constitution v6.0.0 (enforcement), evidence tags, script-first rule.
"""
    (rdir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    # route metadata for catalog updates
    (rdir / "routes.json").write_text(json.dumps(routes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote skills/{router}/SKILL.md ({len(routes)} routes)")


def do_core(absorbed: list[str], max_lines: int = 150) -> None:
    for aid in absorbed:
        src = ALFA / "skills" / aid
        if not (src / "SKILL.md").exists():
            print(f"WARN missing {aid}", file=sys.stderr)
            continue
        dst = ROOT / "skills" / aid
        dst.mkdir(parents=True, exist_ok=True)
        text = (src / "SKILL.md").read_text(encoding="utf-8")
        lines = text.splitlines()
        if len(lines) > max_lines:
            lines = lines[:max_lines] + ["", f"<!-- trimmed from {len(text.splitlines())} lines; full version: alfa skills/{aid}/SKILL.md -->"]
        (dst / "SKILL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        ev = src / "evals" / "evals.json"
        if ev.exists():
            (dst / "evals.json").write_text(ev.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"  {aid} -> skills/{aid}/ (SKILL.md{' + evals.json' if ev.exists() else ''})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["router", "core"], required=True)
    ap.add_argument("--router")
    ap.add_argument("--desc", default="")
    ap.add_argument("--absorb", nargs="+", required=True)
    args = ap.parse_args()
    if args.mode == "router":
        if not args.router:
            ap.error("--router required")
        do_router(args.router, args.absorb, args.desc)
    else:
        do_core(args.absorb)
    return 0


if __name__ == "__main__":
    sys.exit(main())
