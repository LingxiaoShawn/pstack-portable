### Hillclimb

Improve one measurable outcome through controlled experiments.

1. Define the realistic workload, metric, improvement direction, regression
   checks and target. Reuse current traces. Use the user's target and budget;
   otherwise choose a finite initial experiment budget and state the assumption.
   A minimum attempt count is needed only when the requested experiment requires
   it, not as a default condition for success.
2. Establish a sensitive, repeatable measurement harness and a baseline. Control
   relevant workload and environment differences, and repeat samples enough to
   estimate noise. Freeze the harness and regression thresholds for comparisons.
3. Keep a compact decision log for a sustained run: hypothesis, change,
   measurement, checks and keep/revert decision. Use a temporary or existing
   ignored location unless a repository artifact is useful and in scope.
4. Test one hypothesis at a time. Implement directly or use isolated workers
   when useful and permitted. Inspect each diff, measure using the same harness,
   and run the regression checks before keeping a change. Revert only the
   experimental edits when an attempt fails; preserve unrelated work.
5. Keep measured improvements beyond noise that preserve the contract. Verify
   the combined result after integrating successful independent experiments.
   Report a simplification with unchanged performance as such, not a speed win.
6. Stop when repeat measurements support the target, the budget is exhausted,
   or further experiments have little expected benefit. Revisit the hypothesis
   on a plateau without spinning through arbitrary attempts. Never lower the
   target or regression gate to declare success; report an unmet target plainly.
7. Commit or use [Opening a PR](opening-a-pr.md) within the requested workflow.

Reply with baseline and final measurements, variability, accepted changes,
verification and any remaining target gap. Include the experiment log when useful.
