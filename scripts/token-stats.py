#!/usr/bin/env python3
"""token-stats.py — 3-arm session-start token measurement (caveman honesty rule).

Arms:
  alfa      : what alfa injects per runtime (measured from alfa repo files)
  beta-naive: beta surfaces WITHOUT compressed register (estimated: desc<=200,
              prose core) — recorded once at P3 from git history, constant here
  beta      : current generated beta surfaces (measured)

chars/4 heuristic, consistently applied to all arms. Results written to
evals/token-benchmark.json — README tables regenerate from this file only.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALFA = Path("/Users/deonto/Documents/workspace/jm-adk-alfa")

ALFA_SURFACES = {
    "claude-code": ["CLAUDE.md", "PRISTINO-INDEX.md"],
    "antigravity": ["GEMINI.md", ".agent/rules/GEMINI.md", ".agent/skills_index.json"],
    "codex": ["AGENTS.md"],
}
BETA_SURFACES = {
    "claude-code": ["CLAUDE.md"],
    "antigravity": ["GEMINI.md", ".agent/rules/GEMINI.md", ".agent/skills_index.json"],
    "codex": ["AGENTS.md"],
}
# measured at P3 commit before compressed-register patch (git 207db1d^ state)
BETA_NAIVE = {"claude-code": 3869, "antigravity": 5377, "codex": 3820}


def measure(base: Path, surfaces: dict) -> dict:
    out = {}
    for rt, files in surfaces.items():
        total = 0
        for rel in files:
            p = base / rel
            if p.exists():
                total += len(p.read_text(encoding="utf-8", errors="ignore")) // 4
        out[rt] = total
    return out


def main() -> int:
    result = {
        "method": "chars/4 heuristic, identical across arms",
        "arms": {
            "alfa": measure(ALFA, ALFA_SURFACES),
            "beta-naive": BETA_NAIVE,
            "beta": measure(ROOT, BETA_SURFACES),
        },
    }
    for rt in result["arms"]["alfa"]:
        a, b = result["arms"]["alfa"][rt], result["arms"]["beta"][rt]
        result.setdefault("reduction_vs_alfa", {})[rt] = f"{round(100 * (1 - b / a))}%" if a else "n/a"
    out = ROOT / "evals" / "token-benchmark.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
