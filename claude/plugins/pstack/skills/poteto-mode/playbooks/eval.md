### Eval

Evaluate whether a workflow helps complete realistic tasks, not merely whether
the agent follows its instructions.

1. Define the comparison, acceptance criteria and resource budget before running.
   For productivity claims compare the native client with the same project
   instructions, a minimal guidance variant and the full workflow. Keep task,
   initial commit, model/version, tools and permissions fixed when measuring the
   effect of guidance. Model comparisons require the actual requested models.
2. Use fresh isolated task directories and sessions. Provide the same realistic
   user request and required project context. Keep expected answers and private
   scoring guidance separate. Do not remove legitimate test files or normal
   project terminology to conceal the evaluation.
3. Run within the authorized budget using the actual host capabilities. Parallel
   execution is optional; account for resource contention when timing. Repeat
   trials to estimate variability when making comparative productivity claims.
   A single trial is a smoke check, not evidence of a general improvement.
4. Verify artifacts against objective acceptance checks. Measure completion
   quality, elapsed time, token usage when exposed, user interventions and rework.
   Judge qualitative outcomes using consistent criteria and neutral variant
   labels. A separate reviewer is useful when available and permitted; label
   self-review accurately. Review disagreement is a reason to inspect evidence,
   not proof that a model is biased.
5. Use only host- or user-supplied current-task transcripts for diagnostics. Skill
   calls can help explain an outcome but are not the primary success measure.
   Never invent timing, token counts, reviewers or transcript coverage.
6. Report results, failures, limits and whether the evidence supports adopting
   the variant. Repository packaging tests validate installation and generation;
   they do not establish productivity.

Keep evaluation artifacts outside the working tree unless a reusable fixture or
report is part of the task. Missing capability is a limitation to disclose, not a
reason to silently substitute a different experiment.
