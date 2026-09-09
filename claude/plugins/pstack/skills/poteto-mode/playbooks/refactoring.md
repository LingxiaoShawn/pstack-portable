### Refactoring

Improve structure while preserving the relevant behavior contract.

1. Identify callers, outputs, errors, side effects, ordering and any compatibility
   or performance constraints. Reuse current evidence; use how for unknown flow.
2. Establish an appropriate baseline. Use existing behavioral coverage, adding a
   focused characterization test or before/after comparison where the risk
   warrants it. Formatting or a trivial rename does not require a new harness.
3. Describe the concrete reading or maintenance benefit. Keep useful interfaces,
   validation and rationale. Use architect for a consequential unresolved shape,
   requesting design-only output; crossing a function boundary is not sufficient.
4. Refactor in small verifiable steps. Migrate in-scope callers together. Retain
   compatibility paths when external consumers or staged rollout require them,
   with a clear reason; remove obsolete paths when their obligations are gone.
   Use mechanical helpers or bounded workers only when useful and permitted.
5. Verify the preserved contract and required project checks, then read the final
   diff. Do not relax assertions or thresholds to accommodate an unintended
   behavior change. If a bug is discovered, distinguish it and address it only
   when the task authorizes fixes.
6. Explain the structural benefit and verification. Commit or open a PR within the
   requested workflow, using [Opening a PR](opening-a-pr.md) when applicable.

Do not chase line count or require a rewrite when the existing shape is clearer.
