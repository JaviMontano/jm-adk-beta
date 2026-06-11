#!/usr/bin/env python3
"""build-refs.py — Regenerate the load-bearing skill list from alfa.

Scans agents/, commands/, prompts/, hooks/ in the alfa repo for references to
each skill id (directory name under skills/). Joins with the audit ledger and
emits catalog/coverage-matrix.csv with one row per alfa skill:

    alfa_skill, status, severity, referenced_by_count, referenced_by,
    disposition, beta_home, rationale

disposition / beta_home / rationale are left blank for the consolidation map
to fill (consolidation-map.yaml drives the final values via apply-map.py).

Deterministic: no network, no LLM. Usage:
    python3 migrate/build-refs.py --alfa /path/to/jm-adk-alfa [--out catalog/coverage-matrix.csv]
"""
import argparse
import csv
import re
import sys
from pathlib import Path


SCAN_DIRS = ["agents", "commands", "prompts", "hooks"]


def load_ledger(alfa: Path) -> dict:
    ledger = {}
    path = alfa / "docs/audits/skill-review-ledger.csv"
    if not path.exists():
        print(f"WARN: ledger not found at {path}", file=sys.stderr)
        return ledger
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ledger[row["skill"].strip()] = {
                "status": row.get("status", "").strip(),
                "severity": row.get("severity", "").strip(),
            }
    return ledger


def scan_references(alfa: Path, skill_ids: list[str]) -> dict[str, set[str]]:
    """Return skill_id -> set of relative file paths referencing it."""
    # Build one regex pass per file instead of per (file, skill) pair.
    refs: dict[str, set[str]] = {s: set() for s in skill_ids}
    # Word-boundary match on the exact skill id.
    pattern = re.compile(
        r"(?<![\w-])(" + "|".join(re.escape(s) for s in sorted(skill_ids, key=len, reverse=True)) + r")(?![\w-])"
    )
    files = []
    for d in SCAN_DIRS:
        base = alfa / d
        if base.exists():
            files.extend(p for p in base.rglob("*") if p.is_file() and p.suffix in {".md", ".json", ".sh", ".py", ".yaml", ".yml"})
    for fp in files:
        try:
            text = fp.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(fp.relative_to(alfa))
        for m in set(pattern.findall(text)):
            refs[m].add(rel)
    return refs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alfa", required=True, type=Path)
    ap.add_argument("--out", default="catalog/coverage-matrix.csv", type=Path)
    args = ap.parse_args()

    alfa = args.alfa.resolve()
    skills_dir = alfa / "skills"
    skill_ids = sorted(p.name for p in skills_dir.iterdir() if (p / "SKILL.md").exists())
    print(f"skills found: {len(skill_ids)}")

    ledger = load_ledger(alfa)
    refs = scan_references(alfa, skill_ids)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "alfa_skill", "status", "severity", "referenced_by_count",
            "referenced_by", "disposition", "beta_home", "rationale",
        ])
        for sid in skill_ids:
            led = ledger.get(sid, {"status": "not-in-ledger", "severity": ""})
            r = sorted(refs.get(sid, ()))
            w.writerow([
                sid, led["status"], led["severity"], len(r),
                ";".join(r[:20]) + (";…" if len(r) > 20 else ""),
                "", "", "",
            ])

    referenced = sum(1 for s in skill_ids if refs.get(s))
    print(f"referenced (load-bearing): {referenced}")
    print(f"unreferenced: {len(skill_ids) - referenced}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
