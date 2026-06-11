#!/usr/bin/env python3
"""apply-map.py — Fill disposition/beta_home/rationale in coverage-matrix.csv.

Sources of truth:
  - skills/*/routes.json        → router-fold (alfa id -> beta router)
  - skills/<id>/SKILL.md        → core/keep-as-is (same id exists in beta)
  - catalog/consolidation-map.yaml dropped_generic + duplicate_pairs → dropped/alias
  - everything else: referenced>0 → UNASSIGNED (must be resolved); else dropped-unreferenced

Also updates catalog/skills.json aliases (loser of duplicate pairs + absorbed ids).
Prints the UNASSIGNED load-bearing list — P3 is not done until it is empty.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MATRIX = ROOT / "catalog" / "coverage-matrix.csv"
CMAP = ROOT / "catalog" / "consolidation-map.yaml"
CATALOG = ROOT / "catalog" / "skills.json"


def yaml_list_after(text: str, key: str) -> list[str]:
    """Parse a simple '- item' list under a top-level key (no nesting)."""
    m = re.search(rf"^{key}:\n((?:[ \t]+-[ \t]*.+\n?)+)", text, re.M)
    if not m:
        return []
    return [re.sub(r"^[ \t]+-[ \t]*", "", ln).strip() for ln in m.group(1).strip().splitlines()]


def yaml_pairs(text: str) -> list[tuple[str, str]]:
    m = re.search(r"^duplicate_pairs:.*?\n((?:[ \t]+-[ \t]*\[.+\]\n?)+)", text, re.M | re.S)
    if not m:
        return []
    pairs = []
    for ln in m.group(1).strip().splitlines():
        items = re.findall(r"\[([^\]]+)\]", ln)
        if items:
            a, b = [x.strip() for x in items[0].split(",")[:2]]
            pairs.append((a, b))
    return pairs


def main() -> int:
    cmap_text = CMAP.read_text(encoding="utf-8")
    dropped_generic = set(yaml_list_after(cmap_text, "dropped_generic"))
    dup_pairs = yaml_pairs(cmap_text)
    manual_aliases: dict[str, str] = {}
    mm = re.search(r"^manual_aliases:.*?\n((?:[ \t]+[\w-]+:[ \t]*\S+\n?)+)", cmap_text, re.M | re.S)
    if mm:
        for ln in mm.group(1).strip().splitlines():
            k, v = ln.strip().split(":", 1)
            manual_aliases[k.strip()] = v.strip()

    # alfa id -> (beta_home, disposition)
    assign: dict[str, tuple[str, str, str]] = {}

    # router folds
    for rj in sorted((ROOT / "skills").glob("*/routes.json")):
        router = rj.parent.name
        for short, meta in json.loads(rj.read_text(encoding="utf-8")).items():
            assign[meta["alfa"]] = (f"{router}#{short}", "router-fold", f"playbook in skills/{router}/references/{short}.md")

    # standalone / keep-as-is (same id in beta)
    for d in (ROOT / "skills").iterdir():
        if (d / "SKILL.md").exists() and d.name not in assign:
            assign.setdefault(d.name, (d.name, "core", "standalone skill in beta"))

    # duplicate pairs: loser -> alias of winner's home
    aliases: dict[str, str] = {}
    for aid, home in manual_aliases.items():
        if aid not in assign:
            assign[aid] = (home, "alias", "manual alias (winner not standalone in beta)")
        aliases[aid] = home
    for winner, loser in dup_pairs:
        home = assign.get(winner, (winner, "", ""))[0]
        if loser not in assign:
            assign[loser] = (home, "alias", f"duplicate of {winner}")
        aliases[loser] = home
    # absorbed ids also get aliases for old references
    for aid, (home, disp, _) in assign.items():
        if disp == "router-fold":
            aliases[aid] = home

    rows = list(csv.DictReader(MATRIX.open(encoding="utf-8")))
    unassigned = []
    for row in rows:
        sid = row["alfa_skill"]
        referenced = int(row["referenced_by_count"]) > 0
        if sid in assign:
            row["beta_home"], row["disposition"], row["rationale"] = assign[sid]
        elif sid in dropped_generic:
            row["disposition"] = "dropped-generic"
            row["beta_home"] = "none"
            row["rationale"] = "restates base-model knowledge; referencers rewired to nearest router"
        elif not referenced:
            row["disposition"] = "dropped-unreferenced"
            row["beta_home"] = "none"
            row["rationale"] = "pending+unreferenced; alfa is the archive"
        else:
            row["disposition"] = "UNASSIGNED"
            row["beta_home"] = ""
            row["rationale"] = ""
            unassigned.append(sid)

    with MATRIX.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    catalog["aliases"] = dict(sorted(aliases.items()))
    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    from collections import Counter
    c = Counter(r["disposition"] for r in rows)
    print(dict(c))
    print(f"aliases: {len(aliases)}")
    if unassigned:
        print(f"\nUNASSIGNED load-bearing ({len(unassigned)}):")
        for s in unassigned:
            print(f"  {s}")
        return 1
    print("all load-bearing skills assigned ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
