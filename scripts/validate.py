#!/usr/bin/env python3
"""Validate real package paths, skills, manifests and portable dependencies."""
import json
import re
from pathlib import Path

import yaml

from build import ROOT, TARGETS, frontmatter


def validate_plugin(root, client):
    meta_dir = ".codex-plugin" if client == "codex" else ".claude-plugin"
    manifest = json.loads((root / meta_dir / "plugin.json").read_text())
    assert manifest["name"] == root.name == "pstack"
    assert (root / manifest["skills"]).is_dir()
    shared = root / "skills/pstack-runtime"
    mapping = json.loads((shared / "skill-map.json").read_text())
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    assert len(skills) == len(mapping) == 51
    names = set()
    for path in skills:
        meta, body = frontmatter(path.read_text())
        name = meta["name"]
        assert name == path.parent.name and re.fullmatch(r"[a-z0-9-]{1,64}", name), path
        assert name not in names, name
        names.add(name)
        assert isinstance(meta["description"], str) and meta["description"].strip(), path
        assert "../pstack-runtime/runtime.md" in body, path
        assert not re.search(r"\.cursor/|grok-4|claude-fable-|claude-opus-|gpt-5\.6|mode: true|is_background:", path.read_text()), path
        if client == "codex":
            ui = yaml.safe_load((path.parent / "agents/openai.yaml").read_text())
            assert isinstance(ui["interface"]["display_name"], str)
    for logical, info in mapping.items():
        path = (shared / info["path"]).resolve()
        assert path.is_relative_to(root.resolve()) and path.is_file(), logical
    for path in (root / "skills").rglob("*.md"):
        prose = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
        prose = re.sub(r"`[^`]*`", "", prose)
        for link in re.findall(r"\]\(([^)]+)\)", prose):
            if ":" in link or link.startswith("#") or any(c in link for c in "<> "):
                continue
            target = (path.parent / link.split("#")[0]).resolve()
            assert target.is_relative_to(root.resolve()), (path, link, "escapes package")
            assert target.exists(), (path, link, "missing target")
    for path in root.rglob("*"):
        assert not path.is_symlink(), path
    return len(skills)


def main():
    for client, target in TARGETS.items():
        print(f"{client}: validated {validate_plugin(ROOT / target, client)} skills and local references")
    claude_market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    for plugin in claude_market["plugins"]:
        assert (ROOT / plugin["source"] / ".claude-plugin/plugin.json").is_file()
    codex_market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    for plugin in codex_market["plugins"]:
        assert (ROOT / plugin["source"]["path"] / ".codex-plugin/plugin.json").is_file()
    print("Both marketplace manifests resolve to complete plugin roots.")


if __name__ == "__main__":
    main()
