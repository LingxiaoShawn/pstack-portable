#!/usr/bin/env python3
"""Read and initialize pstack preferences without changing host configuration."""
import argparse
import json
import os
from pathlib import Path

DEFAULTS = {"version": 1, "max_workers": 2, "language": "auto", "roles": {}}


def validate(data):
    if not isinstance(data, dict) or set(data) - set(DEFAULTS):
        raise ValueError("config must be an object using version, max_workers, language, roles")
    result = {**DEFAULTS, **data}
    if type(result["version"]) is not int or result["version"] != 1:
        raise ValueError("unsupported config version")
    n = result["max_workers"]
    if type(n) is not int or not 1 <= n <= 8:
        raise ValueError("max_workers must be an integer from 1 to 8")
    if not isinstance(result["language"], str) or not result["language"].strip():
        raise ValueError("language must be a nonempty string")
    roles = result["roles"]
    if not isinstance(roles, dict):
        raise ValueError("roles must be an object")
    for role, model in roles.items():
        models = model if isinstance(model, list) else [model]
        if not role.strip() or not models or any(not isinstance(m, str) or not m.strip() for m in models):
            raise ValueError("role choices must be nonempty model names or lists")
        if len(models) > n:
            raise ValueError("a role panel exceeds max_workers")
    return result


def resolve(project, home=None):
    home = Path.home() if home is None else Path(home)
    paths = [Path(project) / ".pstack/config.json", home / ".config/pstack/config.json"]
    for path in paths:
        if path.exists():
            return validate(json.loads(path.read_text())), path
    return validate({}), None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["show", "init"])
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--scope", choices=["project", "user"], default="project")
    args = parser.parse_args()
    if args.action == "init":
        path = (args.project / ".pstack/config.json" if args.scope == "project"
                else Path.home() / ".config/pstack/config.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("x") as f:
                json.dump(DEFAULTS, f, indent=2)
                f.write("\n")
            os.chmod(path, 0o600)
        except FileExistsError:
            validate(json.loads(path.read_text()))
        print(path)
    else:
        data, source = resolve(args.project)
        print(json.dumps({"source": str(source) if source else "defaults", "config": data}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc))
