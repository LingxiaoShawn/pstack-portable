# Architect candidate

Produce one design candidate for the supplied task, acceptance criteria, current
code evidence and assigned output location. This is a bounded design task. Do not
invoke architect or arena, spawn another panel, implement production code, or
change files outside the assigned output.

Show a realistic caller example first, then the types, signatures, data ownership
and module boundaries it requires. Explain the principal tradeoff. Use
[rationale-template.md](rationale-template.md) for substantial designs, keeping
only relevant sections. Mark unverified assumptions.

Consider error behavior, compatibility, concurrent writes and repeated or
interrupted operations where they affect the task. Prefer enforceable invariants
and interfaces that hide complexity. Retain runtime checks for values or state
that types and earlier validation cannot guarantee.

Follow the assigned design direction when provided. Otherwise choose and explain
one viable direction. Return your artifact and unresolved questions to the owner;
the owner compares candidates. Do not assume other models or reviewers exist.
