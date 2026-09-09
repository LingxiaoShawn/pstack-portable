### Feature

The task owner defines acceptance criteria, integrates implementation and verifies
the result. Direct implementation is appropriate for a small, settled change.

1. Identify the requested behavior and affected callers. Reuse current context;
   use how only for unfamiliar flow.
2. If a consequential structural choice is unresolved, ask architect for a
   design-only result. Use arena only when distinct alternatives would help
   decide. Continue from the chosen design without repeating that exploration.
3. Implement in verifiable units. For broad work, identify dependencies and
   shared writes; delegate independent units only when available, permitted and
   useful. Give workers scope, current evidence and success criteria. The owner
   reads the resulting diffs and checks the combined artifact.
4. Verify the acceptance criteria on the relevant surface and run required
   project checks. An unavailable or inconclusive check remains a stated gap.
5. Review the diff. Use interrogate for consequential risks, contested decisions
   or a requested independent review. Avoid repeating review without a new reason.
6. Commit, push or open a PR when included in the user's workflow; follow
   [Opening a PR](opening-a-pr.md) when applicable.

Reply with what changed, the significant choice and verification. A simple
feature needs no throughput checklist, candidate panel or HTML handoff.
