### Autopilot stack
Build a linear series of reviewable changes using the multi-phase-plan and
orchestrate playbooks. Record each branch's parent and the precise reviewed head.
Keep dependency order explicit and serialize restacks on the same stack.

Verify each unit and the combined state. Use the existing forge integration;
Graphite and a vendor-specific cloud are not requirements. Preserve unrelated
working-tree changes by using separate worktrees.

Deliver the ordered PRs and remaining gates for the user to land. Do not merge
a request that says to build a stack for review. Scheduling follows the runtime
contract; checkpoint pending work rather than promising unattended progress.
