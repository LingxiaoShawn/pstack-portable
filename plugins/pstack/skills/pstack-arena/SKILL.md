---
name: pstack-arena
description: Compare distinct solutions to the same task, select a maintainable base,
  combine useful ideas, and verify.
---

Read [the pstack runtime](../pstack-runtime/runtime.md) before acting; it defines host tools, model fallback, skill lookup and scope.

# Arena

Define the artifact and a task-specific rubric before producing candidates.
Prefer two meaningfully different designs to many cosmetic variants.

Give each candidate the same requirements and a separate output directory or
worktree. Use independent workers when available and permitted. Use only supported
model choices. A model-family comparison requires those actual models.

Once candidates finish, inspect each artifact end to end. A fresh reviewer may
compare them using neutral labels and the rubric. Record whether this was
independent review, same-model review, or a single-agent comparison.

Pick the base that best satisfies the contract and is easiest to maintain.
Bring over only the useful ideas from the other candidate, then verify the
combined result. Keep a short record of the choice, rejected alternatives and
verification. Agreement alone is not correctness evidence.
