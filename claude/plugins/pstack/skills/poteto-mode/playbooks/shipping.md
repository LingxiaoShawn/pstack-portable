### Shipping
Resolve the user's requested branch or PR sequence and its publishing/merge
authorization. Inspect every proposed PR at its current head: intent, diff,
required checks, reviews and behavior evidence. Use an independent verifier
when available or required; absence of that gate is not a pass.

Follow branch protections and repository rules. Merge only the contiguous
verified sequence whose dependencies have landed. Immediately before each
merge, recheck that its head has not changed and that the forge still permits
the operation. Use installed forge tools or authenticated gh.

Do not force-push, bypass checks or assume green status alone proves correctness.
Report the actual merged heads, unresolved blockers and any remaining verification.
