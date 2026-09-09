### Visual parity

Verify the requested visual contract against a preserved baseline.

1. Capture the baseline and relevant states before a migration. Define the
   comparison environment: browser, viewport, pixel ratio, fonts, animations and
   data. Use the project's existing acceptance thresholds; for a new comparison,
   define the contract before editing. Exact pixel parity requires zero diff.
2. Preserve the baseline and comparison settings. Stabilize nondeterminism before
   using screenshots as a gate. Do not change the harness, mask the target area,
   or loosen tolerances after a failure to manufacture a pass.
3. Migrate small units, handling shared primitives before their consumers. Use
   independent workers only when available, permitted and useful.
4. Compare screenshots on the matching surface. Inspect unexpected differences
   and verify relevant interaction and accessibility behavior separately. Repeat
   for actual fixes; do not loop indefinitely on an uncontrolled environment.
5. If parity cannot be established, report the differing states and precise
   environment or tooling gap. An unmet exact-parity requirement stays unmet.
   A suspected incorrect baseline needs an explicit revised requirement before
   replacing it.
6. Use [Opening a PR](opening-a-pr.md) when included in the requested workflow.

Reply with states checked, comparison results, baseline location and remaining
gaps. HTML inspection alone is not visual verification.
