---
name: principle-boundary-discipline
description: Place validation where trust, ownership or state guarantees change; keep
  domain logic separate from transport and framework wiring.
disable-model-invocation: true
---

Read [the pstack runtime](../pstack-runtime/runtime.md) before acting; it defines host tools, model fallback, skill lookup and scope.

# Boundary discipline

Validate external data and narrow it into domain types at entry points such as
CLI parsing, configuration, network responses and persisted state. Keep domain
logic independent of framework wiring where that improves clarity and testing.

Inside a validated, stable domain, reuse established invariants instead of
repeating checks at every call. Types alone do not establish runtime guarantees:
mutable shared state, asynchronous work, casts, plugins, old serialized data and
foreign-language boundaries may invalidate an earlier assumption. Check where a
guarantee changes or enforce it structurally, such as an atomic state transition.

Separate malformed input from expected domain failures and broken invariants.
Preserve useful error propagation and necessary runtime assertions. Do not remove
a check merely because its function is called internally.

Expose domain concepts rather than leaking transport details when the public
contract benefits. Prefer pure transforms for business rules when practical,
without extracting trivial wrappers solely to satisfy a layering rule.
