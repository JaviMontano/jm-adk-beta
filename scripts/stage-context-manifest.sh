#!/usr/bin/env bash
# stage-context-manifest.sh — ICM Layer 2 Inputs table made executable.
#
# Computes the FULL per-stage context stack a la paper (arXiv 2603.16021v2)
# §3.2 Fig.1: L0 (repo CLAUDE.md) + L1 (workspace CONTEXT.md) + L2 (stage
# CONTEXT.md) + L3 (reference files from the Inputs table) + L4 (working
# artifacts from the Inputs table), with a token sum (chars/4 heuristic,
# same as build-indexes.py / check-token-budget.py).
#
# Paper: "Layer 2 is the control point. The Inputs table makes selection
# explicit, editable, auditable." The paper leaves it as static markdown and
# only CLAIMS the 2-8k budget. This harness makes the table COMPUTABLE and
# ENFORCES the budget — the orchestrator runs this script before loading
# context, so "prevention rather than compression" is verified, not assumed.
# That is "igual o mejor" than the paper.
#
# Usage:
#   stage-context-manifest.sh <stage_dir>                  # human-readable
#   stage-context-manifest.sh <stage_dir> --json            # machine
#   stage-context-manifest.sh <stage_dir> --enforce         # GATE: exit 1 on over-budget/missing
#   stage-context-manifest.sh <stage_dir> --json --enforce # both
#   stage-context-manifest.sh --selftest                   # dry-run sanity
#
# Default = SENSOR (always exits 0, warns on stderr). --enforce = GATE
# (exit 1 if over-budget >8000t OR a referenced Inputs file is missing).
# 04_validate runs --enforce so the budget the paper only CLAIMS becomes a
# hard pre-release gate. Edit-source: fix the stage CONTEXT.md Inputs table,
# not this script.

set -uo pipefail

# --- arg parse (flags in any order; first positional = stage) ---
STAGE=""
JSON_FLAG=""
ENFORCE_FLAG=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --selftest)
      for s in 01_discovery 02_spec 03_build 04_validate; do
        echo "SELFTEST stage=$s"
        "$0" "workspace/_template/$s"
        echo
      done
      exit 0
      ;;
    --json)    JSON_FLAG="--json"; shift ;;
    --enforce) ENFORCE_FLAG="--enforce"; shift ;;
    -*) echo "stage-context-manifest: unknown flag: $1 (ignoring)" >&2; shift ;;
    *)  STAGE="$1"; shift ;;
  esac
done

if [[ -z "$STAGE" ]]; then
  echo "usage: $0 <stage_dir> [--json] [--enforce]   |   $0 --selftest" >&2
  exit 0
fi
STAGE="${STAGE%/}"
CTX="$STAGE/CONTEXT.md"
if [[ ! -f "$CTX" ]]; then
  echo "STAGE-MANIFEST-ERROR: no CONTEXT.md in $STAGE" >&2
  # missing stage contract is a structural failure — gate even in sensor mode
  [[ -n "$ENFORCE_FLAG" ]] && exit 1 || exit 0
fi

python3 - "$CTX" "$STAGE" "$JSON_FLAG" "$ENFORCE_FLAG" <<'PY'
import sys, json, re
from pathlib import Path
ctx_path, stage, json_flag, enforce_flag = \
    Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]

def toks(p: Path) -> int:
    return len(p.read_text()) // 4 if p.exists() and p.is_file() else 0

# --- Resolve L0/L1/L2 base (always-loaded structural layers) ---
# Repo root = nearest ancestor with CLAUDE.md (generated adapter) or .git.
repo_root = stage
for _ in range(8):
    if (repo_root / "CLAUDE.md").exists() or (repo_root / ".git").exists():
        break
    if repo_root.parent == repo_root:
        break
    repo_root = repo_root.parent
l0 = repo_root / "CLAUDE.md"
# Workspace root = stage parent if it has CONTEXT.md (L1).
ws_root = stage.parent if (stage.parent / "CONTEXT.md").exists() else stage
l1 = ws_root / "CONTEXT.md"
l2 = ctx_path
base = [("L0", "identity", l0), ("L1", "routing", l1), ("L2", "contract", l2)]

# --- Parse L3/L4 from the Inputs table ---
text = ctx_path.read_text()
m = re.search(r'^##\s+Inputs\s*(.*?)(?=^##\s|\Z)', text, re.S | re.M)
items, missing = [], []
if m:
    for line in m.group(1).splitlines():
        mm = re.match(r'-\s+Layer\s+(\d)\s+\((working|reference)\):\s+`?([^`]+)`?',
                      line)
        if not mm:
            continue
        layer, kind, raw = int(mm.group(1)), mm.group(2), mm.group(3).strip()
        # skip prose-only entries (no slash, no dot-ext, has spaces) — not files
        looks_path = ("/" in raw) or (raw.endswith(".md")) or \
                     (raw.endswith(".json")) or (raw.endswith(".sh"))
        if not looks_path:
            continue
        resolved = (stage / raw).resolve()
        exists = resolved.exists() and resolved.is_file()
        items.append({"layer": layer, "kind": kind, "path": str(resolved),
                      "exists": exists, "tokens": toks(resolved)})
        if not exists:
            missing.append(str(resolved))

base_toks = sum(t for _, _, p in base for t in [toks(p)])
in_toks = sum(i["tokens"] for i in items)
total = base_toks + in_toks
over = total > 8000

if json_flag == "--json":
    print(json.dumps({"stage": str(stage), "base": [
        {"layer": b[0], "kind": b[1], "path": str(b[2]),
         "tokens": toks(b[2])} for b in base],
        "inputs": items, "base_tokens": base_toks, "inputs_tokens": in_toks,
        "total_tokens": total, "budget": 8000, "over_budget": over,
        "missing": missing, "enforce": enforce_flag == "--enforce"}))
else:
    print(f"STAGE: {stage}")
    for b in base:
        print(f"  {b[0]} {b[1]:9s} {'OK ' if b[2].exists() else 'MISS'} {toks(b[2]):5d}t  {b[2]}")
    for i in items:
        print(f"  L{i['layer']} {i['kind']:9s} {'OK ' if i['exists'] else 'MISS'} {i['tokens']:5d}t  {i['path']}")
    gate = "GATE" if enforce_flag == "--enforce" else "sensor"
    print(f"TOTAL: {total}t / 8000  {'OVER-BUDGET' if over else 'ok'}  ({gate}; base {base_toks} + inputs {in_toks})")
    if missing:
        print(f"MISSING ({len(missing)}): " + "; ".join(missing), file=sys.stderr)
# Gate signal: exit 1 if over-budget OR missing referenced file. Sensor mode
# (no --enforce) is caught by the bash wrapper, which forces exit 0 below.
sys.exit(1 if (over or missing) else 0)
PY
rc=$?
if [[ "$ENFORCE_FLAG" == "--enforce" ]]; then
  exit "$rc"          # GATE: propagate 1 on over-budget/missing
else
  exit 0              # SENSOR: always 0
fi