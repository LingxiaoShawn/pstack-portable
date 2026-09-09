### Perf issue

Tie a performance fix to measurements on the workload that matters.

1. Capture a repeatable baseline on a realistic workload using available
   profiling, tracing or benchmark tools. Record the metric and variability.
   Without measurement, describe the hypothesis and verification gap.
2. Reuse the current flow model; use how where it is incomplete. Let the trace
   guide hypotheses: eliminate unnecessary work, reduce input size, batch fixed
   costs, cache with explicit invalidation, or move work off the critical path.
   Consider behavior and resource costs before adding concurrency or redundancy.
3. Make a scoped change for a specific measured cause. Use architect only when
   the structural choice is consequential and unresolved, requesting design-only
   output. Implement directly or delegate a bounded unit when useful and permitted.
4. Compare before and after under equivalent conditions. Run regression checks,
   inspect the diff and retain only changes supported by the evidence. A noisy
   or wrong-surface result is inconclusive.
5. Commit or use [Opening a PR](opening-a-pr.md) within the requested workflow.

For sustained experimentation use [Hillclimb](hillclimb.md). Reply with workload,
baseline and final metric, variability, delta and evidence location.
