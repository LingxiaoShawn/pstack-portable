### Autonomous run
Define done, scope, budget, stop conditions and evidence. Work through the
authorized task using a bounded hypothesis/implementation/verification loop.
Use show-me-your-work for decisions a human will review later.

Use durable scheduling only when an actual host capability supports it and
the task authorizes it. Otherwise continue within the active session, checkpoint
at a clean boundary, and explicitly say that continuation requires resuming.
Do not emulate a scheduler with a claim that work will run after the client exits.
Avoid long blocking sleeps that prevent progress updates.

Address in-scope problems. Record out-of-scope improvements rather than silently
opening extra PRs or modifying tools. Stop on genuine missing access, exhausted
budget, an unsafe state, or completion; provide a concrete checkpoint.
