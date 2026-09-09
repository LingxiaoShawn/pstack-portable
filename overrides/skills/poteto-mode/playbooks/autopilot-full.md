### Autopilot full
Use orchestrate to assign independent PR-sized units with acceptance criteria.
Each owner builds and verifies its unit in an isolated checkout. Use available
native workers or a disclosed sequential execution, never assumed cloud VMs.

Confirm the user's authorized publishing and merge scope from the request.
At each current PR head, check the diff, CI, reviews, branch state and relevant
behavior. Use an independent verifier if available; do not label self-review as
independent. If independent verification is a required gate and unavailable,
leave the PR ready for that gate.

Merge only the verified head under existing authorization and repository rules.
A changed head invalidates its prior verdict. Track outcomes and unresolved
units in the checkpoint. Without merge authorization, deliver reviewable PRs.
