### Multi-phase plan
Define phases around independently verifiable outcomes. For each, record scope,
prerequisites, affected code, verification, result and remaining work. Start with
the highest-risk unknown that could invalidate later phases.

Use how for unfamiliar mechanisms and architect for unsettled structure.
Reuse verified project tooling and describe any required tool that is missing.
Use independent worktrees and bounded native workers where appropriate, or
perform units sequentially. Preserve a durable checkpoint between phases.

Keep implementation, structural cleanup and behavior changes easy to distinguish.
Verify units before combining them, then verify the combined outcome. Create
branches, commits and PRs within the user's requested workflow. Never infer
permission to merge from permission to prepare a stack.
