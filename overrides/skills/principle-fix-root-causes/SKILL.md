---
name: principle-fix-root-causes
description: "Trace a defect to its mechanism and fix the violated contract while retaining necessary validation and containment."
---

# Fix root causes

Reproduce the symptom where feasible, then trace the inputs and state changes
that cause it. Use targeted instrumentation when evidence is missing. Prefer the
smallest fix that restores the violated contract and verify the original failure.

A guard is appropriate when the contract permits absence, data crosses a boundary,
state can become stale, or containment prevents damage. A guard that silently
hides an impossible internal state may mask the defect; fix the producer or make
the failure explicit. A mitigation can be useful while a root cause remains open:
label its limits and keep the unresolved cause visible.

For restart failures, investigate persisted state, schema changes, caches and
partial writes. Clearing a file is evidence for a hypothesis, not proof that
deleting user state is the fix.

Check related paths for the same demonstrated mechanism. Repair affected callers
within scope; do not expand a focused fix into unrelated cleanup. Keep comments
that explain a real constraint or temporary mitigation.
