#!/usr/bin/env python3
"""Install/update the complete Codex skill bundle, preserving unrelated files."""
import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ".pstack-portable-install.json"
OWNER = "pstack-portable"


def digest(path):
    result = {}
    for p in sorted(path.rglob("*")):
        relative = p.relative_to(path)
        if "__pycache__" in relative.parts or "node_modules" in relative.parts:
            continue
        if p.is_symlink():
            raise ValueError(f"Refusing symlink inside managed bundle: {p}")
        if p.is_file():
            result[str(relative)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def install(destination, source, uninstall=False, dry_run=False):
    if not uninstall:
        runtime = source / "pstack-runtime"
        mapping_path = runtime / "skill-map.json"
        if not mapping_path.is_file() or not (source / "pstack/SKILL.md").is_file():
            raise ValueError("Incomplete source bundle; leaving installed skills unchanged")
        mapping = json.loads(mapping_path.read_text())
        if not isinstance(mapping, dict) or not mapping:
            raise ValueError("Invalid source skill map")
        for entry in mapping.values():
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                raise ValueError("Invalid source skill entry")
            path = (runtime / entry["path"]).resolve()
            if not path.is_relative_to(source.resolve()) or not path.is_file():
                raise ValueError("Incomplete or escaping source skill path")
    state_path = destination / STATE
    if state_path.is_symlink():
        raise ValueError("Installation record must not be a symlink")
    state = json.loads(state_path.read_text()) if state_path.exists() else {"owner": OWNER, "entries": {}}
    if not isinstance(state, dict) or state.get("owner") != OWNER or not isinstance(state.get("entries"), dict):
        raise ValueError("Unknown installation record; leaving files unchanged")
    old = state["entries"]
    for name, fingerprint in old.items():
        if not isinstance(name, str) or name in {"", ".", ".."} or Path(name).name != name or "\\" in name:
            raise ValueError("Invalid managed entry name")
        path = destination / name
        if path.is_symlink() or not path.is_dir() or digest(path) != fingerprint:
            raise ValueError(f"Managed files changed locally; preserve or move them before retrying: {path}")
    new = {} if uninstall else {p.name: digest(p) for p in source.iterdir() if p.is_dir()}
    for name in new:
        if (destination / name).exists() or (destination / name).is_symlink():
            if name not in old:
                raise ValueError(f"Unrelated skill already exists; refusing to overwrite: {destination / name}")
    actions = {name: "remove" if name not in new else "update" if name in old else "install"
               for name in sorted(set(old) | set(new))}
    if dry_run:
        return actions
    if not actions:
        return actions
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".pstack-stage-", dir=destination.parent) as temp:
        temp = Path(temp)
        staged = temp / "new"
        backup = temp / "old"
        staged.mkdir()
        backup.mkdir()
        for name in new:
            shutil.copytree(source / name, staged / name)
        moved_old, moved_new = [], []
        original_state = state_path.read_bytes() if state_path.exists() else None
        try:
            for name in old:
                os.replace(destination / name, backup / name)
                moved_old.append(name)
            for name in new:
                os.replace(staged / name, destination / name)
                moved_new.append(name)
            if uninstall:
                state_path.unlink(missing_ok=True)
            else:
                next_state = temp / "state.json"
                next_state.write_text(json.dumps({"owner": OWNER, "version": 1, "entries": new}, indent=2) + "\n")
                os.replace(next_state, state_path)
        except BaseException:
            for name in reversed(moved_new):
                shutil.rmtree(destination / name)
            for name in moved_old:
                os.replace(backup / name, destination / name)
            if original_state is None:
                state_path.unlink(missing_ok=True)
            else:
                state_path.write_bytes(original_state)
            raise
    return actions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, help="Install into this project's .agents/skills; default is user scope")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()
    if args.project is not None and not args.project.is_dir():
        parser.error("--project must name an existing project directory")
    base = args.project.resolve() if args.project else Path.home()
    target = base / ".agents/skills"
    source = ROOT / "plugins/pstack/skills"
    actions = install(target, source, args.uninstall, args.dry_run)
    print(json.dumps({"destination": str(target), "dry_run": args.dry_run, "entries": len(actions), "actions": actions}, indent=2))
    if not args.dry_run and not args.uninstall:
        print("Use $pstack, $pstack-refactor, $pstack-teach or $pstack-brief in Codex. Restart if not discovered.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc))
