---
name: architect
description: "Design types, interfaces and module boundaries when consequential structural choices remain open, or when the user asks for a design."
---

# Architect

Resolve the structural decisions that would be expensive to reverse. A settled
local change does not need a separate architecture exercise.

## Scope and ownership

For a design request, return a design. When another workflow calls architect,
return the requested design stage to that task owner; do not implement or restart
its workflow. For an explicit design-and-build request owned here, continue into
implementation after choosing the design. Honor a requested checkpoint; otherwise
continue authorized work without adding an approval gate.

## Ground

Reuse current traces, acceptance criteria and constraints from the caller.
Inspect missing context with how. Use why only when historical intent could
change the decision. Identify the callers, data ownership, failure behavior and
compatibility requirements that the design must preserve.

## Sketch and choose

Start from a realistic caller example, then sketch the types, signatures and
module boundaries needed to support it. Keep speculative code out of production
files; use prose or a separate sketch until implementation is in scope.

Compare meaningful alternatives when the choice is consequential or uncertain.
A short tradeoff comparison may be enough; use arena for independently produced
artifacts when the extra work will help, or when requested. Start with two
candidates and one comparison pass. Use only available, permitted workers and
model choices. A candidate receives [runner-prompt.md](references/runner-prompt.md)
and the task context, not instructions to run this whole workflow.

Use [design-red-flags.md](references/design-red-flags.md) as diagnostic questions,
not automatic rejection criteria. Prefer an interface that hides relevant
complexity without burdening callers. Choose against acceptance criteria and
specific tradeoffs, not consensus or the number of models consulted.

Return a compact design and verification approach. For a substantial design,
use [rationale-template.md](references/rationale-template.md); omit sections that
do not help the decision. Name unresolved risks and the next implementation step.

## Implement when owned here

If this task includes implementation, fill in the chosen design in verifiable
units and check the combined result. Reopen a design decision when new evidence
invalidates it. Adjust the affected part first; repeated workarounds may justify
a larger redesign, but an isolated edge case does not require another panel.
