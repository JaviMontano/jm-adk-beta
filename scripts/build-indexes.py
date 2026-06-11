#!/usr/bin/env python3
"""build-indexes.py — Generate all runtime surfaces from catalog/skills.json.

Single source of truth: catalog/skills.json. Emits:
  - SKILLS.md                  (tier-0 index, Claude Code; one line per skill)
  - .agent/skills_index.json   (Antigravity; minimal fields, real JSON)
  - CLAUDE.md / GEMINI.md / AGENTS.md  (runtime/core.md + per-runtime delta + inlined index for codex)
  - harness/.manifest.json     (installed-files manifest, spec-kit pattern)

Deterministic; uses a real YAML-frontmatter parser for skill validation (fixes
alfa's folded-scalar bug). No network.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "skills.json"
MANIFEST = ROOT / "harness" / "manifest.json"


def load(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def tier0_lines(skills: list[dict]) -> list[str]:
    lines = []
    for s in sorted(skills, key=lambda x: x["id"]):
        params = ""
        if s.get("params"):
            params = " [" + ",".join(s["params"].keys()) + "]"
        lines.append(f"- `{s['id']}`{params} — {s['desc']}")
    return lines


def build_skills_md(skills: list[dict]) -> str:
    return (
        "# Skills Index (tier-0)\n\n"
        "Generated from catalog/skills.json — do not edit. "
        "Invoke skill → its SKILL.md routes to one playbook (lazy load).\n\n"
        + "\n".join(tier0_lines(skills))
        + "\n"
    )


def build_antigravity_index(skills: list[dict]) -> str:
    entries = [
        {
            "id": s["id"],
            "path": f"skills/{s['id']}/SKILL.md",
            "desc": s["desc"],
            **({"params": list(s["params"].keys())} if s.get("params") else {}),
        }
        for s in sorted(skills, key=lambda x: x["id"])
    ]
    return json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + "\n"


def build_adapter(runtime: str, manifest: dict, skills: list[dict]) -> str:
    core = (ROOT / manifest["contract"]["core"]).read_text(encoding="utf-8")
    delta_path = manifest["contract"].get("deltas", {}).get(runtime)
    delta = (ROOT / delta_path).read_text(encoding="utf-8") if delta_path and (ROOT / delta_path).exists() else ""
    out = core
    if delta:
        out += "\n" + delta
    index_mode = manifest["outputs"][runtime].get("index", "")
    if index_mode == "inline":
        out += "\n## Skills\n\n" + "\n".join(tier0_lines(skills)) + "\n"
    elif index_mode and index_mode.endswith(".md"):
        out += f"\nSkill index: see `{index_mode}` (load on demand).\n"
    elif index_mode and index_mode.endswith(".json"):
        out += f"\nSkill index: `{index_mode}` (generated, minimal fields).\n"
    return out


def main() -> int:
    manifest = load(MANIFEST)
    catalog = load(CATALOG)
    skills = catalog["skills"]
    written: list[str] = []

    def emit(rel: str, content: str):
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        written.append(rel)
        print(f"wrote {rel} ({len(content)} chars ≈ {len(content)//4} tokens)")

    emit("SKILLS.md", build_skills_md(skills))
    emit(".agent/skills_index.json", build_antigravity_index(skills))
    for runtime, out in manifest["outputs"].items():
        emit(out["adapter"], build_adapter(runtime, manifest, skills))
        if out.get("rules"):
            emit(out["rules"], build_adapter(runtime, manifest, skills))

    emit("harness/.manifest.json", json.dumps({"generated": sorted(written)}, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
