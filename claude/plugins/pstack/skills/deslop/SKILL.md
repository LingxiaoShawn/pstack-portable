---
name: deslop
description: Remove unnecessary code introduced by the current task while preserving
  behavior and local conventions.
---

Read [the pstack runtime](../pstack-runtime/runtime.md) before acting; it defines host tools, model fallback, skill lookup and scope.

# Deslop

Review the current task's diff and enough surrounding code to understand it.
Use the actual base branch when available and include staged/unstaged changes.

Look for redundant wrappers, stale scaffolding, repeated state, obvious narrative
comments, avoidable nesting and type escape hatches added just to silence errors.
Keep useful abstractions, real validation, required error handling and meaningful
rationale. Verify a proposed deletion is truly unnecessary.

Apply focused changes within scope. Do not introduce new behavior or quietly fix
unrelated bugs. Run relevant existing checks and inspect the final diff. Stop
when further edits are cosmetic or would increase reading effort.
