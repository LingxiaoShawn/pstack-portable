---
name: setup-pstack
description: Configure portable pstack preferences and check available tools in Codex
  or Claude Code.
---

Read [the pstack runtime](../pstack-runtime/runtime.md) before acting; it defines host tools, model fallback, skill lookup and scope.

# Setup pstack

The package works without setup. Default to the active model, at most two workers,
and the user's language. Do not ask the user to select from another vendor's model list.

Read ../pstack-runtime/runtime.md and run:
```sh
python3 <skills-directory>/pstack-runtime/doctor.py
python3 <skills-directory>/pstack-runtime/config.py show --project <project-directory>
```
Resolve the paths from this skill's installed location, not guessed cache paths.

When asked to save preferences, initialize the selected scope with config.py init
and edit that one config file. Preserve existing values the user did not change.
Set role models only from capabilities actually exposed by the host. Use
inherit-parent when there is no supported override. A configured panel is bounded
by max_workers and the host limit. The JSON config is read by pstack; it does not
modify the client's model settings or declare native subagent roles.

Report the active configuration and any missing optional capability. Do not
install Bun, gh, browser tools, change permissions, or register services just
because the optional dependency check lists them.
