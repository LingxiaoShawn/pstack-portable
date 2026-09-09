---
name: swarm
description: Coordinate bounded parallel work over separate slices or candidates,
  with explicit evidence and coverage.
disable-model-invocation: true
---

Read [the pstack runtime](../pstack-runtime/runtime.md) before acting; it defines host tools, model fallback, skill lookup and scope.

# Swarm

State the goal, the slices or race candidates, completion criteria, and output.
Respect the configured max_workers and the host's concurrency limit. A larger
total task count runs in bounded waves.

Give writing workers separate worktrees or non-overlapping files. Each brief
contains the goal, scope, inputs, verification and expected report. Use the native
worker tool and supported arguments described by the runtime. Do not invent a
cloud environment or cloud_base_branch parameter.

For coverage, every required slice needs a result. For races, decide whether to
take the first verified success or compare all candidates before launching.
Inspect actual artifacts, aggregate findings and state failures or missing slices.
If the host has no workers, perform feasible slices sequentially and identify
the result as a single-agent execution. If actual parallel timing or independent
workers are the purpose of the request, report the missing capability instead.
