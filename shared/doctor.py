#!/usr/bin/env python3
"""Report dependencies without installing tools or contacting services."""
import json
import shutil
import sys

tools = {name: bool(shutil.which(name)) for name in ["git", "python3", "codex", "claude", "bun", "gh", "bash"]}
print(json.dumps({"python": sys.version.split()[0], "tools": tools,
                  "core_ready": tools["git"] and sys.version_info >= (3, 10),
                  "optional_pr_watcher_tools_present": tools["bun"] and tools["gh"],
                  "note": "Tool presence does not verify login, model availability, or host skill loading."}, indent=2))
