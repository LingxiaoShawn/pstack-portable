#!/usr/bin/env python3
"""Build both clients from the pinned snapshot and explicit portable overrides."""
import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MODEL = re.compile(r"(?:claude-fable-[\w.-]+|claude-opus-[\w.-]+|grok-[\w.-]+|gpt-5\.[\w.-]+)")
TARGETS = {"codex": Path("plugins/pstack"), "claude": Path("claude/plugins/pstack")}
MARKETPLACES = {
    Path(".agents/plugins/marketplace.json"): {
        "name": "pstack-portable",
        "interface": {"displayName": "pstack portable"},
        "plugins": [{"name": "pstack", "source": {"source": "local", "path": "./plugins/pstack"},
                     "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                     "category": "Productivity"}],
    },
    Path(".claude-plugin/marketplace.json"): {
        "name": "pstack-portable",
        "owner": {"name": "Lingxiao Zhao; upstream by Lauren Tan"},
        "metadata": {"description": "Portable pstack workflows for readable code and verified handoffs."},
        "plugins": [{"name": "pstack", "source": "./claude/plugins/pstack"}],
    },
}


def frontmatter(content):
    match = re.match(r"\A---\n(.*?)\n---\n?", content, re.S)
    if not match:
        raise ValueError("missing frontmatter")
    return yaml.safe_load(match[1]), content[match.end():].lstrip()


def adapt(content, client, mapping):
    project_skills = ".agents/skills" if client == "codex" else ".claude/skills"
    replacements = {
        "~/.cursor/rules/pstack-models.mdc": ".pstack/config.json",
        "~/.cursor/projects/*/": "unrelated project transcript directories",
        "~/.cursor/plugins/": "the host-advertised plugin installation directory",
        "~/.cursor/skills": f"~/{project_skills}",
        ".cursor/skills": project_skills,
        "`generalPurpose`": "the host's general-purpose worker role",
        "Cursor's built-in for authoring SKILL.md files": "the host's available skill-authoring capability",
        "from the Cursor environment": "advertised by the current host",
        "Otherwise inspect the `mcps/` directory Cursor exposes for enabled MCP servers.": "Otherwise use the available tool descriptions; do not guess a tool metadata directory.",
        "Cursor's built-in babysit skill": "another PR-watching skill",
        "from `cursor-team-kit`": "through the host's available verification tools",
        "readonly strips MCP": "read-only work still uses only authorized available tools",
        "Readonly strips MCPs.": "Read-only tasks must preserve their no-mutation scope.",
        "in plain spoken English": "in the user's language",
        "[PR #123](url)": "`<actual PR URL>`",
        "under the active workspace's `agent-transcripts/` directory (the system prompt names the path)": "from the host-exposed current-project transcript, if available",
        "under the active workspace's `agent-transcripts/` directory (the system prompt names this path)": "from the host-exposed current-project transcript, if available",
    }
    for old, new in replacements.items():
        content = content.replace(old, new)
    content = MODEL.sub("inherit-parent", content)
    for old, new in mapping.items():
        if old != new:
            content = content.replace(f"../{old}/", f"../{new}/")
            content = content.replace(f"skills/{old}/", f"skills/{new}/")
    return "\n".join(line.rstrip() for line in content.splitlines()).rstrip() + "\n"


def files(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in directory.rglob("*") if p.is_file() and "__pycache__" not in p.parts
            and "node_modules" not in p.parts}


def make_plugin(destination, client):
    source = ROOT / "upstream/pstack"
    shutil.copytree(source / "skills", destination / "skills")
    shutil.copytree(ROOT / "overrides/skills", destination / "skills", dirs_exist_ok=True)
    skill_dirs = sorted(p for p in (destination / "skills").iterdir() if (p / "SKILL.md").exists())
    mapping = {p.name: ("pstack" if p.name == "poteto-mode" else "pstack-" + p.name)
               if client == "codex" else p.name for p in skill_dirs}

    for folder in skill_dirs:
        original = source / "skills" / folder.name / "SKILL.md"
        original_meta = frontmatter(original.read_text())[0] if original.exists() else {}
        meta, body = frontmatter((folder / "SKILL.md").read_text())
        meta = {"name": mapping[folder.name], "description": meta["description"]}
        explicit = original_meta.get("disable-model-invocation", False)
        if client == "claude" and explicit:
            meta["disable-model-invocation"] = True
        rendered_meta = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()
        preamble = "Read [the pstack runtime](../pstack-runtime/runtime.md) before acting; it defines host tools, model fallback, skill lookup and scope.\n\n"
        (folder / "SKILL.md").write_text(f"---\n{rendered_meta}\n---\n\n{preamble}{body}")
        if client == "codex":
            agents = folder / "agents"
            agents.mkdir(exist_ok=True)
            data = {"interface": {"display_name": "pstack · " + folder.name,
                                  "short_description": str(meta["description"])[:100]}}
            if explicit:
                data["policy"] = {"allow_implicit_invocation": False}
            (agents / "openai.yaml").write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))

    for p in (destination / "skills").rglob("*.md"):
        p.write_text(adapt(p.read_text(), client, mapping))
    for folder in skill_dirs:
        if folder.name != mapping[folder.name]:
            folder.rename(folder.with_name(mapping[folder.name]))

    runtime_dir = destination / "skills/pstack-runtime"
    shutil.copytree(ROOT / "shared", runtime_dir)
    host = ("Codex: load skills from their advertised paths. Use exec_command or the exposed shell tool for commands, and the available file-edit tools for edits. Use the actual native agent interface only when present; do not assume Claude's Agent/Task schema. Without delegation, complete feasible work in the parent."
            if client == "codex" else
            "Claude Code: use the advertised Skill, Read, Edit/Write, Bash and Agent interfaces as available. Plugin skills are invoked as /pstack:<name>. Native general-purpose workers or the bundled pstack:poteto-agent may be used when available; inherit the parent model by default. Do not send Cursor-only fields such as environment or cloud_base_branch.")
    runtime = (runtime_dir / "runtime.md").read_text().replace("{{CLIENT}}", client).replace("{{HOST_TOOLS}}", host)
    (runtime_dir / "runtime.md").write_text(runtime)
    runtime_meta = {"name": "pstack-runtime", "description": "Resolve pstack's installed skill paths, local preferences, and available host capabilities."}
    (runtime_dir / "SKILL.md").write_text("---\n" + yaml.safe_dump(runtime_meta, sort_keys=False) + "---\n\nRead [the runtime contract](../pstack-runtime/runtime.md). Use skill-map.json to find a pstack workflow. Read configuration with config.py and report dependencies with doctor.py when requested. Neither preferences nor installation grant permissions.\n")
    if client == "codex":
        (runtime_dir / "agents").mkdir()
        (runtime_dir / "agents/openai.yaml").write_text('interface:\n  display_name: "pstack runtime"\n  short_description: "Resolve pstack paths and host capabilities."\n')
    mapping["runtime"] = "pstack-runtime"
    skill_map = {name: {"path": f"../{actual}/SKILL.md", "invoke": "$" + actual if client == "codex" else "/pstack:" + actual}
                 for name, actual in mapping.items()}
    (runtime_dir / "skill-map.json").write_text(json.dumps(skill_map, indent=2) + "\n")
    shutil.copy2(ROOT / "LICENSE", destination / "LICENSE")
    shutil.copy2(ROOT / "upstream.lock.json", destination / "upstream.lock.json")
    manifest = {"name": "pstack", "version": "0.1.0", "description": "Portable pstack workflows for readable code and clear, verified handoffs.",
                "author": {"name": "Lingxiao Zhao; upstream by Lauren Tan"}, "license": "MIT", "skills": "./skills/"}
    if client == "codex":
        manifest["interface"] = {"displayName": "pstack", "shortDescription": "Readable code and clear engineering handoffs.",
                                 "longDescription": "Lauren Tan's pstack adapted for native Codex workflows, with scoped refactoring and HTML briefs.",
                                 "developerName": "Lingxiao Zhao", "category": "Productivity", "capabilities": [],
                                 "defaultPrompt": "Use pstack to complete and explain this change."}
    else:
        agents = destination / "agents"
        agents.mkdir()
        for name, workflow in [("poteto-agent", "poteto-mode"), ("comment-sicko", "no-comments")]:
            (agents / f"{name}.md").write_text(f'---\nname: {name}\ndescription: Follow the portable pstack {workflow} workflow for a scoped task.\nmodel: inherit\n---\n\nRead the bundled skills/{workflow}/SKILL.md and its runtime contract before work. Resolve paths from the installed plugin root. Follow the parent task and host permissions. Return actual evidence and remaining gaps.\n')
    meta_dir = destination / (".codex-plugin" if client == "codex" else ".claude-plugin")
    meta_dir.mkdir(exist_ok=True)
    (meta_dir / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return len(mapping)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    with tempfile.TemporaryDirectory(prefix="pstack-build-") as temp:
        for client, relative in TARGETS.items():
            generated = Path(temp) / client
            count = make_plugin(generated, client)
            target = ROOT / relative
            if args.check:
                if not target.exists() or files(generated) != files(target):
                    stale.append(str(relative))
            else:
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(generated, target)
            print(f"{client}: {count} skills")
        for relative, data in MARKETPLACES.items():
            target = ROOT / relative
            content = json.dumps(data, indent=2) + "\n"
            if args.check:
                if not target.is_file() or target.read_text(encoding="utf-8") != content:
                    stale.append(str(relative))
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale generated packages: " + ", ".join(stale))


if __name__ == "__main__":
    main()
