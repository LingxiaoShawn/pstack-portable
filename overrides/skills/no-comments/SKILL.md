---
name: no-comments
description: "Clean noisy comments while preserving necessary explanations, constraints, documentation and tool directives."
---

# Comment cleanup

Use the user's scope or the current task's diff. Remove comments that merely
narrate obvious operations, are stale, or repeat the same fact in several places.
Keep public API documentation, license notices, tool directives, subtle rationale,
external constraints and necessary warnings.

Before deleting a warning or a constraint, investigate its basis through how or
why. If its purpose is uncertain, keep it and state the uncertainty; ambiguity
does not authorize deletion. Encoding a constraint in a type or meaningful test
may be useful when within scope, but do not create a broad rewrite just to remove
a comment. Do not weaken lint suppressions without resolving their cause.

Use a fresh review only when available and useful. Verify accepted edits and
report meaningful improvements without treating deletion count as the objective.
