---
name: poteto-mode
description: "Use pstack for deliberate implementation, refactoring, investigation, and clear evidence-backed handoffs."
---

# Poteto mode

Work toward the user's actual outcome. Scale the process to the change.

1. Identify the task and load the matching playbook from playbooks/. Read-only
   questions stay read-only. Keep the user's existing authorization and scope.
2. For unfamiliar code, use how to trace the actual flow; use why when historical
   intent matters. Design changes with architect when the structure is unsettled,
   not automatically for every function call.
3. Establish the behavior or acceptance criteria that the change must satisfy.
   Implement in small verifiable units. Use a bounded plan for multi-step work.
4. Review the diff; use deslop when a focused cleanup is useful. Use no-comments only
   to remove noise; retain meaningful constraints and rationale.
5. Verify the result against the real artifact. State what was checked and what
   remains unverified. Opening a PR, merging, deployment and external messages
   happen only when included in the user's task or existing authorization.
6. Lead the reply with the outcome in the user's language. Explain the significant
   choice plainly. Use brief for a requested presentation or useful visual handoff.

Reuse results from earlier stages while their inputs are current. A small change
with a settled design can go directly to implementation and relevant checks.
When calling architect inside implementation work, request design-only output;
this task owner continues implementation and verification. A called stage never
restarts this whole workflow. Follow the runtime's exploration limits.

Read the runtime contract before dispatch. Use actual host workers only when
available and appropriate. Otherwise work locally and sequentially. The parent
owns the result, reads the diffs, and verifies the combined artifact. Do not
present self-review as independent review.

## Principles

Load the relevant principle skill only when it changes a concrete decision:
- principle-minimize-reader-load: reduce indirection and state the reader must track.
- principle-model-the-domain: put domain knowledge in a clear data shape.
- principle-subtract-before-you-add: remove obsolete paths before adding mechanisms.
- principle-test-behavior-not-implementation: verify externally meaningful behavior.
- principle-prove-it-works: inspect actual results and preserve evidence.
- principle-sequence-verifiable-units: keep substantial changes reviewable.
- principle-boundary-discipline: keep responsibilities and ownership clear.
The remaining upstream principles are available through the skill map.

## Select a playbook

- Questions and explanations: investigation.md. Human teaching: teach.
- Defect: bug-fix.md. Measured slowness: perf-issue.md.
- New behavior: feature.md. Structure-only work: refactoring.md or refactor.
- Design experiment: prototype.md. Iterative measurement: hillclimb.md.
- Captured traces: trace-forensics.md. Live symptoms: runtime-forensics.md.
- Visual comparison: visual-parity.md.
- Skills: authoring-a-skill.md. Skill evaluation: eval.md.
- PR checks: babysit.md. Explicitly authorized merge: shipping.md.
- Long active task: autonomous-run.md. Multiple work units: orchestrate.md.
- Independent PR queue: autopilot-full.md. Reviewable stack: autopilot-stack.md.
- Resume: session-pickup.md. Stop or handoff: pause-safely.md.
- Multi-phase change: multi-phase-plan.md. Disk cleanup: worktree-cleanup.md.
- PR requested: opening-a-pr.md.
- No good fit: figure-it-out.

If the user asks for this style across the conversation, continue applying it to
relevant tasks until they opt out. This is conversation guidance, not a promise
of a sticky client mode across restarts. Never print an inventory of principles
as the human-facing explanation.
