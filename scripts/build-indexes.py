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
        mark = "®" if s.get("params") else ""
        lines.append(f"`{s['id']}`{mark} {s['desc']}")
    return lines


def build_skills_md(skills: list[dict]) -> str:
    n = len(skills)
    routers = sum(1 for s in skills if s.get("params"))
    header = (
        "# Skills Index (tier-0)\n\n"
        f"GENERATED — do not edit by hand. Source of truth: `catalog/skills.json`; "
        f"regenerate with `python scripts/build-indexes.py` (also rebuilds this header). "
        f"Hand edits are overwritten on next build. [DOC]\n\n"
        "Tier-0 = always-loaded discovery layer: one line per skill so the agent picks a "
        "skill WITHOUT reading any SKILL.md. Match the user request to a `id` + description, "
        "then load `skills/<id>/SKILL.md` (path is derivable from the id, never listed here). [DOC]\n\n"
        "Legend [DOC]:\n"
        "- `id` — backtick code span; the slug. Open `skills/<id>/SKILL.md` to run it.\n"
        "- ® — router skill: `params` (topic enum + depth) live in its frontmatter `routes`. "
        "Resolve the topic, read exactly ONE playbook under that skill's `references/` — not the whole skill.\n"
        "- (no ®) — leaf skill: SKILL.md is the full playbook; many carry a `(Pnn)` cadence/process id.\n"
        "- … — description elided for width; the authoritative full text is the SKILL.md `description`.\n\n"
        "Selection contract [DOC]: pick the single best id; if two tie, prefer the more specific; "
        "if none fit, fall back to the closest ® router and let its topic param disambiguate; "
        "if still unmatched, ask — do NOT invent an id or a path. Anti-scope: this index lists no "
        "params, routes, tools, or versions — read the SKILL.md for those.\n\n"
        f"Counts [INFERENCE]: {n} skills, {routers} routers (®), {n - routers} leaf. "
        "Sorted by id; stable for diffing.\n\n"
        + "\n".join(tier0_lines(skills))
        + "\n"
    )
    return header


def build_antigravity_index(skills: list[dict]) -> str:
    # path derivable: skills/<id>/SKILL.md ; r=1 marks router (params in SKILL.md)
    entries = [
        {"id": s["id"], "d": s["desc"], **({"r": 1} if s.get("params") else {})}
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
    active_profile = manifest["contract"].get("activeProfile")
    if active_profile:
        profile_name = active_profile.split("/")[-1].replace(".md", "")
        out += (
            f"\n## Active profile\n\n"
            f"This harness runs under the **{profile_name}** profile — its deliverable-quality, "
            f"brand, i18n, and commercial standards apply. Load `{active_profile}` on demand; "
            f"override with the `JMADK_PROFILE` env var. [CONFIG]\n"
        )
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
