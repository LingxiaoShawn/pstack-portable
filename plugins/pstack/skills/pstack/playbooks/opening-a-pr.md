### Opening a PR
Proceed when the user's task or existing authorization includes opening a PR.
Inspect the current branch and working tree, choose the correct base, and isolate
new work in a branch/worktree when needed. Preserve unrelated edits. Never use
hard reset as a cleanup shortcut.

Run deslop on the scoped diff and relevant verification. Use technical-writing
and unslop for a concise title and body: concrete problem, resulting behavior,
meaningful validation and remaining gaps. Keep refactoring separable from
behavior changes where that improves review.

Use installed GitHub tools or authenticated gh to publish the branch and create
the PR. Do not invent a remote URL. If a destination repository is missing, finish
the local reviewable change and request that specific destination.
