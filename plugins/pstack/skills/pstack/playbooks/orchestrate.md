### Orchestrate
Break the requested program into units with explicit dependencies, input refs,
owned paths, completion checks and status. Keep one durable project-local
checkpoint. The optional scripts/orch/orch ledger can manage this state when
Bun is available; it does not schedule or host agents.

Use the host's native workers in bounded waves when supported and permitted.
Isolate writing work. The coordinator can implement a small unit directly rather
than creating another layer. Read every terminal report and inspect relevant
diffs and evidence before combining work. Missing slices stay visible.
Serialize edits to a shared branch and verify the combined result.

Record each accepted unit's actual commit or artifact, checks, and next dependency.
Do not infer liveness from a stale transcript. Before exiting, reconcile workers,
record pending external work, and write resumption instructions. A restarted
client must recheck git and PR state rather than trust old agent identifiers.
Use autonomous-run only with a real host wake mechanism or an active session.
