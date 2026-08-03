#!/usr/bin/env bash
# check-governance-consistency.sh — governance docs-vs-source consistency gate.
#
# Detects stale references and drift between governance docs and source:
#   1. README must not reference stale "Constitution v6" (must be v7).
#   2. README token table matches evals/token-benchmark.json (no hand-typed drift).
#   3. runtime/core.md constitution ref resolves to an existing ontology file.
#   4. README Layout dirs all exist on the filesystem (no phantom dirs advertised).
#   5. ADRs in docs/decisions/ are sequential (0001, 0002, ... no gaps).
#
# Exit 1 if any check fails (gate); exit 0 if all pass. --json mode.
# Edit-source: fix the stale doc/source, not this script.
#
# Usage:
#   scripts/check-governance-consistency.sh           # human
#   scripts/check-governance-consistency.sh --json    # machine

set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
JSON=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON=1; shift ;;
    *) echo "check-governance-consistency: unknown arg: $1" >&2; shift ;;
  esac
done

python3 - "$ROOT" "$JSON" <<'PY'
import sys, json, re
from pathlib import Path
root, json_mode = Path(sys.argv[1]), int(sys.argv[2])
readme = root / "README.md"
core = root / "core.md" if (root / "core.md").exists() else (root / "runtime/core.md")
evals = root / "evals/token-benchmark.json"
decisions = root / "docs/decisions"
ontology = root / "references/ontology"

fails = []

# 1. No stale "Constitution v6" reference in README.
if readme.exists():
    rtext = readme.read_text()
    if re.search(r'constitution[-\s]*v6', rtext, re.I):
        fails.append("readme-stale-constitution-v6: README references Constitution v6 (must be v7)")

# 2. README token table matches evals/token-benchmark.json.
if readme.exists() and evals.exists():
    rtext = readme.read_text()
    bench = json.loads(evals.read_text())
    beta = bench.get("arms", {}).get("beta", {})
    # README row: | <Runtime> | **<measured>** | <cap> |
    readme_vals = {}
    for runtime in ("Claude Code", "Antigravity", "Codex"):
        m = re.search(rf'\| {re.escape(runtime)}\s*\|\s*\**([\d,]+)\*', rtext)
        if m:
            readme_vals[runtime] = int(m.group(1).replace(",", ""))
    mapping = {"Claude Code": "claude-code", "Antigravity": "antigravity", "Codex": "codex"}
    for disp, key in mapping.items():
        if disp in readme_vals and key in beta:
            if readme_vals[disp] != beta[key]:
                fails.append(f"readme-token-drift: README {disp}={readme_vals[disp]} != evals beta.{key}={beta[key]}")
        elif disp not in readme_vals:
            fails.append(f"readme-token-missing: README token table has no {disp} measured row")

# 3. runtime/core.md constitution ref resolves to an existing ontology file.
if core.exists():
    ctext = core.read_text()
    m = re.search(r'references/ontology/(constitution-v[\d.]+\.md)', ctext)
    if m:
        ref = ontology / m.group(1)
        if not ref.exists():
            fails.append(f"core-constitution-ref-missing: core.md references {m.group(1)} but file not in references/ontology/")
    else:
        fails.append("core-constitution-ref-absent: runtime/core.md has no references/ontology/constitution-vX.Y.Z.md reference")

# 4. README Layout dirs exist on filesystem.
if readme.exists():
    rtext = readme.read_text()
    layout = re.search(r'^##\s+Layout\s*```(.*?)```', rtext, re.S | re.M)
    if layout:
        advertised = set()
        for line in layout.group(1).splitlines():
            mm = re.match(r'^(\w+)/\s', line)
            if mm:
                advertised.add(mm.group(1) + "/")
        for d in sorted(advertised):
            if not (root / d.rstrip("/")).is_dir():
                fails.append(f"readme-layout-phantom-dir: README Layout advertises {d} but it is absent on disk")

# 5. ADRs sequential (no gaps).
if decisions.is_dir():
    nums = sorted(int(p.stem.split("-")[0]) for p in decisions.glob("*.md")
                  if re.match(r'^\d{4}', p.stem))
    if nums:
        expected = list(range(nums[0], nums[-1] + 1))
        if nums != expected:
            fails.append(f"adr-sequence-gap: docs/decisions/ ADR numbers {nums} are not sequential (expected {expected})")

ok = len(fails) == 0
if json_mode:
    print(json.dumps({"ready": ok, "checks_run": 5, "failures": fails}))
else:
    if ok:
        print("governance-consistency: READY (5 checks pass)")
    else:
        print("governance-consistency: BLOCKED")
        for f in fails:
            print(f"  - {f}")
sys.exit(0 if ok else 1)
PY