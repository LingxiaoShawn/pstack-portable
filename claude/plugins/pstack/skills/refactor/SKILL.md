---
name: refactor
description: Simplify the current change or a named subsystem without changing its
  behavior, focusing on maintainability.
---

Read [the pstack runtime](../pstack-runtime/runtime.md) before acting; it defines host tools, model fallback, skill lookup and scope.

# Refactor

1. Identify the target and relevant callers. Inspect the complete task diff,
   including staged and unstaged work. Establish which edits are yours.
2. Trace unfamiliar logic with how. State the relevant behavior contract:
   outputs, exceptions, side effects, ordering and performance-sensitive behavior.
3. Capture an appropriate baseline. Use existing checks and add a focused
   characterization or before/after comparison only when the risk requires it.
4. Read principle-minimize-reader-load and apply it to the target. Reduce empty
   wrappers, needless branching, duplicated mutable state and speculative layers.
   Keep helpful interfaces, necessary checks and explanatory comments.
5. Make small changes that have a concrete reading or maintenance benefit.
   Keep actual bug fixes distinct. Do not chase a line-count or complexity score.
6. Verify the contract and review the resulting diff. Do not weaken tests or
   thresholds to make the rewrite pass. Preserve unrelated work.
7. Explain the useful structural change and verification. Use brief after the
   final code is settled when a presentation or visual handoff is useful.

For broader structural work, follow the refactoring playbook under poteto-mode.
If a proposed simplification makes the code harder to understand, leave it out.
