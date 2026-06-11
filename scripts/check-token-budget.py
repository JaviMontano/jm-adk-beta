#!/usr/bin/env python3
"""check-token-budget.py — CI gate: generated session-start surfaces must fit budgets.

Token estimate: chars/4 heuristic (documented; benchmark script measures real).
Exit 1 on any violation.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
manifest = json.loads((ROOT / "harness/manifest.json").read_text(encoding="utf-8"))

# What each runtime injects at session start.
SURFACES = {
    "claude-code": ["CLAUDE.md"],  # index inlined
    "antigravity": ["GEMINI.md", ".agent/rules/GEMINI.md", ".agent/skills_index.json"],
    "codex": ["AGENTS.md"],
}

failed = False
for runtime, budget in manifest["tokenBudgets"].items():
    total = 0
    for rel in SURFACES.get(runtime, []):
        p = ROOT / rel
        if p.exists():
            total += len(p.read_text(encoding="utf-8")) // 4
    limit = budget["sessionStartMax"]
    status = "OK" if total <= limit else "FAIL"
    if total > limit:
        failed = True
    print(f"{runtime}: {total} / {limit} tokens — {status}")

sys.exit(1 if failed else 0)
