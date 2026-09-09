---
name: arena
description: "Compare distinct solutions to the same task, select a maintainable base, combine useful ideas, and verify."
---

# Arena

Define the artifact and a task-specific rubric before producing candidates.
Prefer two meaningfully different designs to many cosmetic variants.
Use arena when comparing alternatives can resolve a consequential uncertainty
or the user requests a comparison. Do not repeat it merely because a design or
implementation stage calls another skill. Reuse viable existing candidates.

Start with two candidates and one comparison pass unless the requested experiment
needs another size. Give candidates a bounded artifact to produce, not the arena
or parent orchestration instructions; they must not launch their own panels.
Expand only to address a named gap that the existing candidates cannot resolve.

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
