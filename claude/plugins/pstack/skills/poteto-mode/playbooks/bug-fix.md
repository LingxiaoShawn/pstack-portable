### Bug fix

Find the mechanism, make a scoped fix and verify the failure path.

1. Reproduce through the relevant test, CLI, browser or runtime tools available
   in the session. Use a local reproduction or targeted instrumentation when
   useful. If the original environment is inaccessible, state that limit and
   investigate with the supplied evidence; do not claim reproduction.
2. Trace candidate causes and test the hypotheses that distinguish them. Reuse
   existing traces; use how for missing flow and why when historical intent could
   affect the fix. Do not run a full history investigation by default.
3. Fix the demonstrated mechanism while preserving necessary validation and error
   handling. Use architect only for an unresolved structural decision. Implement
   directly or delegate a bounded task when available, permitted and useful.
4. Check the original failure and relevant neighboring behavior. Add a regression
   test when it can catch the defect; confirm it fails before and passes after
   the fix where feasible. Existing tests can suffice when they cover the failure.
   Keep unavailable original-surface verification explicitly unverified.
5. Run required project checks and inspect the final diff. Keep commits reviewable
   within the requested workflow; failing tests do not need a separate commit.
   Use [Opening a PR](opening-a-pr.md) when a PR is requested.

Reply with the broken behavior, cause, fix and actual checks. Include useful
failure evidence without dumping every investigation log.
